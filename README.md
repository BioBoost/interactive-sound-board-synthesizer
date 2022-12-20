# sound board interactive audio

## introduction

This is the synthesizer and main program of the project.

### installation & setup

#### install synthesizer
```bash
python3 -m pip install synthesizer
```

#### install audio package
```bash
apt install portaudio19-dev
pip install pyaudio
```

#### install mqtt and numpy
```bash
pip install paho-mqtt
pip install numpy
```

#### before starting the program
```bash
pulseaudio -k
pulseaudio -D
```

## code

```text
Het project bevat 3 python files:
-   main.py:
        Maakt gebruikt van de MQTT/Synthesize class om het programma te runnen.

-   mqttclient.py
        Custom class die de paho-mqtt libary bevat , die verantwoordelijk is voor de MQTT communicatie

-   synthesize.py:
        Custom class die de synthesizer libary bevat , die verantwoordelijk is voor het sorteren en afspelen van de noten
```

### main.py

Import eerst de classes van de andere python files.

```python
#import the MQTT and Synthesize class
from mqttclient import MQTT
from synthesize import Synthesize
```

Maak instancies aan van de classes.
geef de nodige variables mee aan mqtt default constructor om te kunnen connecteren met de MQTT broker.
synthesizer class moet meegeven worden aan de mqtt class zodat later de function van deze instantie kan aanroepen.

```python
#synthesizer class
synth = Synthesize()

#mqtt connect to broker
mqtt = MQTT("pi-of-terror",1883,60,synth)
```

Subscribe aan de topics voor de frontend en de topic waar de devices zie bekend maken.
Start de mqtt loop zodat deze blijft draaien als het programma aan het runnen is.
Mqtt class stuurt ook zijn huidige configuratie door om de vue frontend de default waarden van de classen te geven.

```python
#sub to topics of frontend and devices
mqtt.subscribe("test/devices/","test/frontend/volume",'test/frontend/octave','test/frontend/wave','test/frontend/frequency','test/frontend')
#start de mqtt loop
mqtt.start()
#send Huidige config
mqtt.SendConfig()
```

het programma zal continue twee functions oproepen:
-   mqtt.sensorValues():
        Deze functie is verantwoordelijk voor de esp's sensor te starten en stopen
-   synth.PlayNotes():
        speelt de notes af

```python
while(True):
    #get values en activate sensor
    mqtt.sensorValues()
    #play the current notes
    synth.PlayNotes()
```

```python
```

### mqttclient.py

Import de nodige libraries

```python
import paho.mqtt.client as mqtt
import numpy as np
import time
import json
```

```python
class MQTT:
    #init class MQTT
    def __init__(self, broker , port , stopseconds, synth):
        #devices
        self.__availableDevices = []
        self.__activeDevices = []
        #average of the sensor values
        self.__unfiltered_values = []
        self.__settingAVG = 10

        #mqtt with esp
        self.__currentDevice = 0
        self.__status = False
        #instantie van de synthesizer class
        self.__synth = synth
        #instantie van de paho mqtt class
        self.__client = mqtt.Client()
        #connect to broker
        self.__client.connect(broker, port, stopseconds)
```

```python
def ActivateDevice(self , device):
    if device not in self.__activeDevices:
        self.devicesTopics(device)
        self.__activeDevices.append(device)
        self.__availableDevices.remove(device)
        time.sleep(0.5)
```

```python
def devicesTopics(self,device):
    #sub to all device topics
    self.subscribe(f'test/{device}/sensor')
    return self
```

```python
def sensorValues(self):
    if(self.__currentDevice >= len(self.__activeDevices)):
            self.__currentDevice = 0

    if(self.__status == False and len(self.__activeDevices) != 0):
        self.sensorStart(self.__activeDevices[self.__currentDevice])
        self.__status = True

    if(len(self.__unfiltered_values) == self.__settingAVG):
        if(self.__currentDevice == len(self.__activeDevices)):
            self.__currentDevice = 0
        self.sensorStop(self.__activeDevices[self.__currentDevice])
        print('stopped reading values')
        print(f'the values {self.__unfiltered_values}')
        self.sensorAVG()
        time.sleep(0.001)
```

```python
def sensorAVG(self):
    avg = 0
    print("getting avg")
    #dit is nodig om te avg te kunnen berekenen
    for j in range(0, len(self.__unfiltered_values)):
        self.__unfiltered_values[j] = float(self.__unfiltered_values[j])
    avg = round(np.average(self.__unfiltered_values),2)
    print(f'avg is: {avg}')
    self.__synth.SortNotes(avg,self.__currentDevice)
    self.__unfiltered_values.clear()
    self.__currentDevice += 1
    #reset values
    self.__status = False
    avg = 0
    time.sleep(0.0001)
```

```python
def sensorStart(self,device):
    self.publisch(f"test/{device}/status",1)
    time.sleep(0.001)
```

```python
def sensorStop(self,device):
    self.publisch(f"test/{device}/status",0)
    time.sleep(0.001)
```

```python
def SendConfig(self):
    config = {
        'activedevices': self.__activeDevices,
        'volume': self.__synth.getVolume(),
        'frequentie': self.__synth.getFrequnetie()
    }
    self.__client.publish("test/config", payload=json.dumps(config), retain=True)
```

```python
def subscribe(self, *topics):
    #sub to all given topics
    for topic in topics:
        self.__client.subscribe(topic)
        print(f"subscribed to {topic}")
    time.sleep(0.001)
```

```python
def publisch(self,topic,message):
    print(f'publish {message} to {topic}')
    self.__client.publish(topic,message)
    time.sleep(0.001)
```

```python
def unSubscribe(self, *topics):
    #deze functie wordt niet gebruikt maar kan handig zijn voor later
    for topic in topics:
        print(f'unsubscribing from {topic}')
        self.__client.unsubscribe(topic)
```

```python
#result of connection to broker
def on_connect(self , client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
```

```python
def on_message(self ,client, userdata, msg):
    #sensor message from mqtt
    #online device message from mqtt
    if('test/devices/' == msg.topic):
        if msg.payload.decode() not in self.__availableDevices:
            self.__availableDevices.append(msg.payload.decode())
            self.ActivateDevice(msg.payload.decode())
            print(f"device [{msg.payload.decode()}] is online")
            self.SendConfig()

    if(f'sensor' in msg.topic and self.__status == True): #and self.__status == True
            if(len(self.__unfiltered_values) != self.__settingAVG):#and self.__readStatus == True
                self.__unfiltered_values.append(msg.payload.decode())
                print(f"value [{msg.payload.decode()}] received from sensor")
            time.sleep(0.001)
        
    #message to change wave of the synth
    elif('test/frontend/wave' in msg.topic):
        self.__synth.SetWave(msg.payload.decode())
        print(f"changing wave to {msg.payload.decode()}")
        self.SendConfig()

    #message to change vomule of the synth
    elif('test/frontend/volume' == msg.topic):
        self.__synth.setVolume(float(msg.payload.decode()) * 0.01)
        print(f'changing volume {float(msg.payload.decode()) * 0.01}')
        self.SendConfig()

    #message to change frequency of the synth
    elif('test/frontend/frequency' == msg.topic):
        self.__synth.setFrequentie(float(msg.payload.decode()) * 0.01)
        print(f'changing Frequentie {float(msg.payload.decode()) * 0.01}')
        self.SendConfig()
        
    #message to change octave of the synth
    elif('test/frontend/octave' == msg.topic):
        self.__synth.SetOctave(msg.payload.decode())
        print(f"changing Octave to [{msg.payload.decode()}]")
        self.SendConfig()

    #message to publish the current config to the frontends
    elif('test/frontend' == msg.topic):
        self.SendConfig()
        print(f"sending config to new user")
```

```python
def getDevices(self):
    return self.__activeDevices
```

```python
def getAvailableDevices(self):
    return self.__availableDevices
```

```python
def start(self):
    self.__client.loop_start()
    # we call from client object , the on_connect method and we overwrited
    self.__client.on_connect = self.on_connect
    self.__client.on_message = self.on_message
```

### synthesizer

```python
from synthesizer import Player, Synthesizer, Waveform
```

```python
class Synthesize:
	def __init__(self):
		self.__volume = 0.5
		self.__notes = []

		self.__octave4 = {0:(0) , 1:(256.8912) , 2:(272.13184) , 3:(288.3152) , 4:(305.5984) , 5:(323.6672) , 6:(342.99296) , 7:(363.26144) , 8:(384.944) , 9:(407.88352) , 10:(432.08) , 11:(457.84768) , 12:(485.02944)}
		self.__octave2 = {0:(0) , 1:(64.2228) , 2:(68.03296) , 3:(72.0788) , 4:(76.3996) , 5:(80.91536) , 6:(85.74824) , 7:(90.81536) , 8:(96.236) , 9:(101.97088) , 10:( 108.02) , 11:(114.46192) , 12:(121.25736)}
		self.__octave = self.__octave4
		self.__frequentie = 0.5

		self.__player = Player()
		self.__wave = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
		#open audio stream
		self.__player.open_stream()
```

```python
def SetWave(self,wave):
		wave = int(wave)
		if wave == 0:
			self.__wave = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
			print('changed wave to sinus')
		elif wave == 1:
			self.__wave = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=False)
			print('changed wave to triangle')
		elif wave == 2:
			self.__wave = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=False)
			print('changed wave to square')
		elif wave == 3:
			self.__wave = Synthesizer(osc1_waveform=Waveform.sawtooth, osc1_volume=1.0, use_osc2=False)
			print('changed wave to sawtooth')
		return self
```

```python
def SetOctave(self,octave):
	if octave == 4:
		self.__octave = self.__octave4
	elif octave == 2:
		self.__octave = self.__octave2
	return self
```

```python
def setVolume(self , volume):
	if volume == 0:
		volume = 0.1
	self.__volume = volume
	return self
```

```python
def getVolume(self):
	return self.__volume
```

```python
def setFrequentie(self , frequentie):
	self.__frequentie = frequentie
	return self
```

```python
def getFrequnetie(self):
	return self.__frequentie
```

```python
def SortNotes(self, value,index):
	#round de waarde en zet om naar een getal tussen 0 - 12
	if(len(self.__notes) < index + 1):
		self.__notes.append(self.__octave[round(value * 12)])
	else:
		self.__notes[index] =  self.__octave[round(value * 12)]
	if(len(self.__notes) != 0):
		print(self.__notes)
```

```python
def PlayNotes(self):
	if(len(self.__notes) != 0):
		print(self.__notes)
	if len(self.__notes) is not 0:
		for note in self.__notes:
			self.__wave._osc1._volume = float(self.getVolume())
			self.__player.play_wave(self.__wave.generate_constant_wave(note, self.__frequentie))
```
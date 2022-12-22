# sound board interactive audio

made by [<img src="https://github.com/TristanDeLil.png" width="25">Tristan De Lil](https://github.com/TristanDeLil)

## introduction

This is the synthesizer and main program of the project.

### important 

You must first connect your bluetooth device first then activate the activate you pulseaudio demons. 
After that start the main.py program before you turn on the esps and make sure it's the first to connect to the accespoint or network.
Run the python script nokia.py in the testsound folder if you wanne test you sound quality.

### installation & setup

#### update system

```bash
sudo apt update && sudo apt full-upgrade -y
```

#### install python
Do note that the python version it was made on was Python 3.7.3
I am not responsible if it doesn't work on other versions

```bash
sudo apt install python3
or 
sudo apt install python3.7.3
```

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
#### installing mosquitto broker

```bash
sudo apt install -y mosquitto mosquitto-clients
```
### enable mosquitto broker

```bash
sudo systemctl enable mosquitto.service
sudo systemctl status mosquitto.service
```

Name of the broker:
```bash
hostname -I
```
Normal mqtt broker port is 1883.

#### allow websocket on the broker

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Add websocket port

```bash
listener 8080
protocol websockets
```

test websocket connection via MQTT explorer

[!image](/img/ws.PNG)

### connecting to the accespoint on the other raspberry pi / or your own network

#### Add network 
```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

```bash
network={
   ssid="<name network>"
   psk="<password>"
}
```

```bash
ctrl + o
ctrl + x
sudo reboot
```

#### get static ip address

```bash
sudo nano /etc/dhcpcd.conf
```

```bash
interface [INTERFACE] wlan0/eth0
static ip_address=[STATIC IP ADDRESS YOU WANT]/[the subnet of the ip address]
static_routers=[ROUTER IP]
static domain_name_servers=[DNS IP]
```

```bash
ctrl + o
ctrl + x
sudo reboot
```

### connect to a bluetooth device

```bash
sudo systemctl start bluetooth
sudo bluetoothctl
power on
scan on
```

after finding you devices MAC address

```bash
trust <MAC address>
connect <MAC address>
quit
```

if done correctly your bluetooth device should connect automatically with your pi on start up

### some usefull links
```text
[wifi setup](https://raspberrypihq.com/how-to-connect-your-raspberry-pi-to-wifi/)
[static ip](https://www.tomshardware.com/how-to/static-ip-raspberry-pi)
[bluetooth](https://linuxhint.com/setup-bluetooth-raspberry-pi/)
```

## code

This project contains 3 python files:
-   main.py:
        Maakt gebruikt van de MQTT/Synthesize class om het programma te runnen.

-   mqttclient.py
        Custom class die de paho-mqtt libary bevat , die verantwoordelijk is voor de MQTT communicatie

-   synthesize.py:
        Custom class die de synthesizer libary bevat , die verantwoordelijk is voor het sorteren en afspelen van de noten


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

### mqttclient.py

Import de nodige libraries

```python
import paho.mqtt.client as mqtt
import numpy as np
import time
import json
```

default constructor van de MQTT class bevat alle variabelen en connect met de broker

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

Verwijdered het selecterde device van avaiableDevices array en steekt het in de activeDevices array als het er al niet in staat.
Roept ook de devicesTopices() functie aan.

```python
def ActivateDevice(self , device):
    if device not in self.__activeDevices:
        self.devicesTopics(device)
        self.__activeDevices.append(device)
        self.__availableDevices.remove(device)
        time.sleep(0.5)
```

subscribed naar de topic waar de Device zijn data naar zal publishen.

```python
def devicesTopics(self,device):
    #sub to all device topics
    self.subscribe(f'test/{device}/sensor')
    return self
```

Deze functie is verantwoordelijk voor het sturen van de start/stop naar de esp's om hun sensor meetingen te starten en door te sturen.
Controleert ook of de self.__unfiltered_values array nog niet vol zit anders berekent hij de average van de gemeten waarden.

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

Als deze Functie wordt aangeroepen overloopt hij de unfiltered_values array en zet hij deze om naar een float array.
Daar na neemt hij de average van deze aangepaste array en wordt het afgerond op 2 cijfers na de komma.
De average wordt dan door gestuurt naar de SortNotes samen met de index om de note aan te passen.
Hier achter reset hij de waarden zodat de volgende meeting kan beginnen.

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

publish een 1 op de device topic /status zodat de sensor begin met meeten.

```python
def sensorStart(self,device):
    self.publisch(f"test/{device}/status",1)
    time.sleep(0.001)
```

publish een 0 op de device topic /status zodat de sensor stopt met meeten.

```python
def sensorStop(self,device):
    self.publisch(f"test/{device}/status",0)
    time.sleep(0.001)
```

Stuurt de huidoge configuratie naar de topic /config nadat hij het in json formaat heeft omgezet.

```python
def SendConfig(self):
    config = {
        'activedevices': self.__activeDevices,
        'volume': self.__synth.getVolume(),
        'frequentie': self.__synth.getFrequnetie()
    }
    self.__client.publish("test/config", payload=json.dumps(config), retain=True)
```

Subscribes naar alle geven topics en print het terug uit welke topics hij heeft gesubscribed.
De *topics zorgt ervoor dat er meerdere topic tegelijker tijd kunnen mee worden gegeven zonder zorgen te maken over out-of-index errors.

```python
def subscribe(self, *topics):
    #sub to all given topics
    for topic in topics:
        self.__client.subscribe(topic)
        print(f"subscribed to {topic}")
    time.sleep(0.001)
```

Published een message naar een gegeven topic en print het uit.
De functie schermt het orginele paho mqtt publish functie af.

```python
def publisch(self,topic,message):
    print(f'publish {message} to {topic}')
    self.__client.publish(topic,message)
    time.sleep(0.001)
```

Deze functie kan worden gebruikt om van één of meerdere topics te unsubscriben.
Wordt niet niet meer gebruikt. 

```python
def unSubscribe(self, *topics):
    #deze functie wordt niet gebruikt maar kan handig zijn voor later
    for topic in topics:
        print(f'unsubscribing from {topic}')
        self.__client.unsubscribe(topic)
```

Deze functie geeft een result code terug na het verbinden of proberen te verbinden met de MQTT broker.

```python
#result of connection to broker
def on_connect(self , client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
```

De on_message() functie is het belangerijkste van de MQTT class.
Het controleert de topics waar er waarden naar toe zij gestuurt en controleert.

MAC addressen worden in availableDevices gestoken en onmiddelijk geactiveert.
Sensor values worden in de unfiltered array gestoken.

En het zorgt er voor dat de synthesizer properties kunnen worden aangepast 
via de frontend en de nieuwe config kan worden gepublished. 

```python
def on_message(self ,client, userdata, msg):
    #online device message from mqtt
    if('test/devices/' == msg.topic):
        if msg.payload.decode() not in self.__availableDevices:
            self.__availableDevices.append(msg.payload.decode())
            self.ActivateDevice(msg.payload.decode())
            print(f"device [{msg.payload.decode()}] is online")
            self.SendConfig()

    #sensor message from mqtt
    if(f'sensor' in msg.topic and self.__status == True):
            if(len(self.__unfiltered_values) != self.__settingAVG):
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

geeft alle active devices weer.

```python
def getDevices(self):
    return self.__activeDevices
```

geeft alle available devices weer.

```python
def getAvailableDevices(self):
    return self.__availableDevices
```

Start functie activeert de MQTT loop en zorgt er voor dat de on_connect 
& on_message blijven lopen terwijl het programma draait.

```python
def start(self):
    self.__client.loop_start()
    self.__client.on_connect = self.on_connect
    self.__client.on_message = self.on_message
```

### synthesizer

Import de synthesizer class

```python
from synthesizer import Player, Synthesizer, Waveform
```

```python
class Synthesize:
	def __init__(self):
		#the propeties of the notes
		self.__frequentie = 0.5
		self.__volume = 0.5
		self.__notes = []

		#the octaves in Linked lists
		self.__octave4 = {0:(0) , 1:(256.8912) , 2:(272.13184) , 3:(288.3152) , 4:(305.5984) , 5:(323.6672) , 6:(342.99296) , 7:(363.26144) , 8:(384.944) , 9:(407.88352) , 10:(432.08) , 11:(457.84768) , 12:(485.02944)}
		self.__octave2 = {0:(0) , 1:(64.2228) , 2:(68.03296) , 3:(72.0788) , 4:(76.3996) , 5:(80.91536) , 6:(85.74824) , 7:(90.81536) , 8:(96.236) , 9:(101.97088) , 10:( 108.02) , 11:(114.46192) , 12:(121.25736)}
		self.__octave = self.__octave4
		
		#to play the notes
		self.__player = Player()
		self.__wave = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
		#open audio stream
		self.__player.open_stream()
```

Fuctie om wave propertie aan te passen naar een sinus/triangle/square/sawtooth geluids golf.

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

Verandert het octave die wordt afgespeelt.

```python
def SetOctave(self,octave):
	if octave == 4:
		self.__octave = self.__octave4
	elif octave == 2:
		self.__octave = self.__octave2
	return self
```

Funtie die wordt gebruikt om het volume aan te passen.

```python
def setVolume(self , volume):
	if volume == 0:
		volume = 0.1
	self.__volume = volume
	return self
```

Geeft de waarde van het volume terug.

```python
def getVolume(self):
	return self.__volume
```

setFrequentie Maakt het mogelijk om de frequentie van de golf aan te passen.

```python
def setFrequentie(self , frequentie):
	self.__frequentie = frequentie
	return self
```

Geeft de frequentie terug.

```python
def getFrequnetie(self):
	return self.__frequentie
```

Sorteert de notes zodat die op de juiste plaats komen te staan en met de juiste octave waarden.

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

Speelt de noten achter elkaar of niet als er geen devices verbonden zijn.
En geeft weer welke octave waarde de noot heeft

```python
def PlayNotes(self):
	if(len(self.__notes) != 0):
		print(self.__notes)
	if len(self.__notes) is not 0:
		for note in self.__notes:
			self.__wave._osc1._volume = float(self.getVolume())
			self.__player.play_wave(self.__wave.generate_constant_wave(note, self.__frequentie))
```
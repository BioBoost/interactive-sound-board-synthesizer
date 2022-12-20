import paho.mqtt.client as mqtt
import numpy as np
import time
import json

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

    def ActivateDevice(self , device):
        if device not in self.__activeDevices:
            self.devicesTopics(device)
            self.__activeDevices.append(device)
            self.__availableDevices.remove(device)
            time.sleep(0.5)

    def devicesTopics(self,device):
        #sub to all device topics
        self.subscribe(f'test/{device}/sensor')
        return self

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

    def sensorStart(self,device):
        self.publisch(f"test/{device}/status",1)
        time.sleep(0.0001)

    def sensorStop(self,device):
        self.publisch(f"test/{device}/status",0)
        time.sleep(0.0001)

    def SendConfig(self):
        config = {
            'activedevices': self.__activeDevices,
            'volume': self.__synth.getVolume(),
            'frequentie': self.__synth.getFrequnetie()
        }
        self.__client.publish("test/config", payload=json.dumps(config), retain=True)

    def subscribe(self, *topics):
        #sub to all given topics
        for topic in topics:
            self.__client.subscribe(topic)
            print(f"subscribed to {topic}")
        time.sleep(0.001)

    def publisch(self,topic,message):
        print(f'publish {message} to {topic}')
        self.__client.publish(topic,message)
        time.sleep(0.001)

    def unSubscribe(self, *topics):
        #deze functie wordt niet gebruikt maar kan handig zijn voor later
        for topic in topics:
            print(f'unsubscribing from {topic}')
            self.__client.unsubscribe(topic)

    #result of connection to broker
    def on_connect(self , client, userdata, flags, rc):
         print(f"Connected with result code {rc}")

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
        
    def getDevices(self):
        return self.__activeDevices

    def getAvailableDevices(self):
        return self.__availableDevices


    def start(self):
        self.__client.loop_start()
        # we call from client object , the on_connect method and we overwrited
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message
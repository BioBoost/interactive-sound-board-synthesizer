import paho.mqtt.client as mqtt
import numpy as np
import time
import json

class MQTT:
    #init class MQTT
    def __init__(self, broker , port , stopseconds, synth):
        self.__availableDevices = []
        self.__activeDevices = []
        self.__topics = []
        self.__unfiltered_values = []
        self.__values = []
        self.__currentDevice = 0
        self.__currentMAC = ""

        self.__gettingAVG = False

        self.__readStatus = False
        self.__status = False
        self.__synth = synth
        self.__client = mqtt.Client()
        self.__client.connect(broker, port, stopseconds)

    def ActivateDevice(self , device):
        if device not in self.__activeDevices:
            self.devicesTopics(device)
            self.__activeDevices.append(device)
            self.__availableDevices.remove(device)
            time.sleep(1)

    def devicesTopics(self,device):
        #sub to all device topics
        #print(f'connecting to topics of {device}')
        self.subscribe(f'test/{device}/sensor')
        return self

    def sensorValues(self):
        #if(len(self.__activeDevices) != 0):
            #print(f'current length {len(self.__unfiltered_values)}')
        if(self.__currentDevice >= len(self.__activeDevices)):
                self.__currentDevice = 0

        if(self.__status == False and len(self.__activeDevices) != 0):
            self.sensorStart(self.__activeDevices[self.__currentDevice])
            self.__currentMAC = self.__activeDevices[self.__currentDevice]
            self.__status = True
            self.__readStatus = True

        if(len(self.__unfiltered_values) == 10):#and self.__readStatus == True
            if(self.__currentDevice == len(self.__activeDevices)):
                self.__currentDevice = 0
            #self.__readStatus = False
            self.sensorStop(self.__activeDevices[self.__currentDevice])
            print('stopped reading values')
            print(f'the values {self.__unfiltered_values}')
            self.sensorAVG()
            time.sleep(1)
            #self.sensorAVG()
            #time.sleep(1)
        
    def sensorAVG(self):
        self.__gettingAVG = True
        avg = 0
        #print("getting avg")
        #dit is nodig om te avg te kunnen berekenen
        for j in range(0, len(self.__unfiltered_values)):
            self.__unfiltered_values[j] = float(self.__unfiltered_values[j])
        avg = round(np.average(self.__unfiltered_values),2)
        print(f'avg is: {avg}')
        #print(self.__currentDevice)
        self.__synth.SortNotes(avg,self.__currentDevice)
        #self.sensorStop(device)
        self.__unfiltered_values.clear()
        self.__currentDevice += 1
        #reset values
        self.__status = False
        avg = 0
        self.__gettingAVG = False
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
                if(len(self.__unfiltered_values) != 10):#and self.__readStatus == True
                    self.__unfiltered_values.append(msg.payload.decode())
                time.sleep(0.001)
                
        #message to change wave of the synth
        if('test/frontend/wave' in msg.topic):
            self.__synth.SetWave(msg.payload.decode())
            print(f"changing wave to {msg.payload.decode()}")
            self.SendConfig()

        if('test/frontend/volume' == msg.topic):
            self.__synth.setVolume(float(msg.payload.decode()) * 0.01)
            print(f'changing volume {float(msg.payload.decode()) * 0.01}')
            self.SendConfig()

        if('test/frontend/frequency' == msg.topic):
            self.__synth.setFrequentie(float(msg.payload.decode()) * 0.01)
            print(f'changing Frequentie {float(msg.payload.decode()) * 0.01}')
            self.SendConfig()
        
        if('test/frontend/octave' == msg.topic):
            self.__synth.SetOctave(msg.payload.decode())
            print(f"changing Octave to [{msg.payload.decode()}]")
            self.SendConfig()

        if('test/frontend' == msg.topic):
            self.SendConfig()
            print(f"sending config to new user")
        
    def getTopics(self):
        return self.__topics

    def getDevices(self):
        return self.__activeDevices

    def getValues(self):
        return self.__values

    def getAvailableDevices(self):
        return self.__availableDevices

    def getSynth(self):
        return self.__synth

    def start(self):
        self.__client.loop_start()
        # we call from client object , the on_connect method and we overwrited
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message
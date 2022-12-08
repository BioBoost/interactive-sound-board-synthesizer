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
        self.__notes = []
        self.__status = False
        self.__synth = synth
        self.__client = mqtt.Client()
        self.__client.connect(broker, port, stopseconds)

    #test class while waiting for backend
    def selectAllDevices(self):
        for device in self.__availableDevices:
            self.ActivateDevice(device)

    def ActivateDevice(self , device):
        if device not in self.__activeDevices:
            self.__activeDevices.append(device)
            self.devicesTopics(device)
            self.__availableDevices.remove(device)
            time.sleep(0.1)

    def devicesTopics(self,device):
        #sub to all device topics
        print(f'connecting to topics of {device}')
        self.subscribe(f'test/{device}/sensor')
        return self 
    
    def sensorValues(self):
        currentDevice = 0
        avg = 0
        for device in self.__activeDevices:
            if(currentDevice == len(self.__activeDevices)):
                currentDevice = 0
            if(self.__status == False):
                self.sensorStart(device)
                self.__status = True
            print(len(self.__unfiltered_values))
            if(len(self.__unfiltered_values) == 10):
                #print("getting avg")
                for j in range(0, len(self.__unfiltered_values)):
                    self.__unfiltered_values[j] = float(self.__unfiltered_values[j])
                #if(len(self.__notes) < currentDevice + 1):
                #    self.__notes.append(np.average(self.__unfiltered_values))
                #else:
                #    self.__notes[currentDevice] = np.average(self.__unfiltered_values)
                #print(f'{self.__notes}')
                avg = np.average(self.__unfiltered_values)
                #print(f'avg is: {avg}')
                self.__synth.SortNotes(avg,currentDevice)
                self.sensorStop(device)
                self.__unfiltered_values.clear()
                currentDevice += 1
                #reset values
                self.__status = False
                avg = 0
                time.sleep(0.001)

    def sensorStart(self,device):
        self.publisch(f"test/{device}/status",1)

    def sensorStop(self,device):
        self.publisch(f"test/{device}/status",0)

    def SendAllAvailableDevices(self):
        self.publisch(f"test/frontend/",self.__availableDevices)

    def SendConfig(self):
        config = {
            'avaiabledevices': self.__availableDevices,
            'activedevices': self.__activeDevices,
            'volume': self.__synth.getVolume(),
            'frequentie': self.__synth.getFrequnetie()
        }
        self.__client.publish("test/config", payload=json.dumps(config), retain=True)

    def subscribe(self, *topics):
        #sub to all given topics
        for topic in topics:
            if topic not in self.__topics:
                self.__client.subscribe(topic)
                print(f"subscribed to {topic}")
            #check if topic is not already in topics
            if topic not in self.__topics and 'devices' not in topic:
                self.__topics.append(topic)
            
    def publisch(self,topic,message):
        print(f'publish {message} to {topic}')
        self.__client.publish(topic,message)

    #result of connection to broker
    def on_connect(self , client, userdata, flags, rc):
         print(f"Connected with result code {rc}")

    def on_message(self ,client, userdata, msg):
        #sensor message from mqtt
        if('sensor' in msg.topic):
            if(len(self.__unfiltered_values) < 10):
                self.__unfiltered_values.append(msg.payload.decode())
                #print(f"value from sensor [{msg.topic}]: {msg.payload}")

        #online device message from mqtt
        if('test/devices/' == msg.topic):
            if msg.payload.decode() not in self.__availableDevices:
                self.__availableDevices.append(msg.payload.decode())
                print(f"device [{msg.payload.decode()}] is online")
        
        #message to change wave of the synth
        if('wave' in msg.topic):
            self.__synth.SetWave(msg.payload.decode())
            print(f"changing wave to [{msg.payload.decode()}]")

        if('test/frontend/available' == msg.topic):
                self.SendAllAvailableDevices()

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
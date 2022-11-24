import paho.mqtt.client as mqtt
import numpy as np

class MQTT:
    #init class MQTT
    def __init__(self, broker , port , stopseconds):
        self.__availableDevices = []
        self.__devices = []
        self.__topics = []
        self.__values = []
        self.__client = mqtt.Client()
        self.__client.connect(broker, port, stopseconds)
        
    def selectDevices(self , device):
        self.__devices.append(device)
        self.devicesTopics(device)

    def devicesTopics(self):
        #sub to all device topics
        for device in self.__devices:
            print(f'connecting to topics of {device}')
            self.subscribe(f'test/{device}/sensor')
        return self 
    
    def sensorValues(self):
        temp_values = []

        for i in range(self.__devices):
            self.sensorStart(self.__devices[i])
            if len(temp_values) >= 10:
                temp_values.append(self.sensor_message(self.__devices[i]))
            else:
                self.__values.insert(i,np.mean(temp_values))
            self.sensorStop(self.__devices[i])

    def sensorStart(self,device):
        self.publisch(f"test/{device}/status",1)

    def sensorStop(self,device):
        self.publisch(f"test/{device}/status",0)

    def subscribe(self, *topics):
        #sub to all given topics
        for topic in topics:
            self.__client.subscribe(topic)
            print(f"subscribed to {topic}")
            #check if topic is not already in topics
            if topic not in self.__topics and 'devices' not in topic:
                self.__topics.append(topic)
            
    def publisch(self,topic,message):
        print(f'publish {message} to {topic}')
        self.__client.publish(topic,message)

    def sensor_message(self ,client, userdata, msg, device):
        if(f'{device}/sensor' in msg.topic):
            print(f"value received [{msg.topic}]: {msg.payload}")
            return msg.payload.decode()

    #result of connection to broker
    def on_connect(self , client, userdata, flags, rc):
         print(f"Connected with result code {rc}")

    def on_message(self ,client, userdata, msg):
        #for i in range(0,len(self.__topics)):
        #    if(msg.topic == self.__topics[i]):
        #        self.__values.insert(i,msg.payload.decode())
        #        print(f"value received [{msg.topic}]: {msg.payload}")

        if('devices' in msg.topic):
            if msg.payload.decode() not in self.__availableDevices:
                self.__availableDevices.append(msg.payload.decode())
                print(f"device [{msg.payload.decode()}] is online")

    def getTopics(self):
        return self.__topics

    def getDevices(self):
        return self.__devices

    def getValues(self):
        return self.__values

    def getAvailableDevices(self):
        return self.__availableDevices

    def start(self):
        self.__client.loop_start()
        # we call from client object , the on_connect method and we overwrited
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message

    
        
    

# defines a node in a singly linked list

import numpy as np
import random as random
import paho.mqtt.client as mqtt

# defines a singly linked list
class MQTT:
    #De values we define from the main 
    def __init__(self, broker = None, port = None, stopseconds = None):
        self.__broker = broker # current Node 
        self.__port = port
        self.__stopseconds = stopseconds
        self.client = mqtt.Client()
        self.client.connect(broker, port, stopseconds)
        
    
    def subcribe(self, topic1, topic2, topic3 ):
        self.client.subscribe(topic1)
        self.client.subscribe(topic2)
        self.client.subscribe(topic3)

    def on_connect(client, userdata, flags, rc):
         print("Connected with result code "+str(rc))

    def on_message(client, userdata, msg):
        if(msg.topic == 'test/soundboard/esp1'):
            volume = msg.payload.decode()
            print(f"Message received [{msg.topic}]: {msg.payload}")
        
        if(msg.topic == 'test/soundboard/esp2'):
            pitch = msg.payload.decode()
            print(f"Message received [{msg.topic}]: {msg.payload}")

    def get_client(self): 
        return self.client

    def get_userdata(self): 
        return self.userdata

    def get_msg(self): 
        return self.msg
    
    def get_flags(self): 
        return self.flags

    def set_client(self, client): 
        self.client = client
        #self.client.on_connect = on_connect
        #self.client.on_message = on_message


    def client_start(self):
        self.client.loop_start()

    
        
    

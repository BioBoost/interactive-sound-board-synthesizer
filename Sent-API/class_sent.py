# defines a node in a singly linked list

import paho.mqtt.client as mqtt

class MQTT:
    #De values we define from the main 
    def __init__(self, broker , port , stopseconds):
        self.__topic1 = 1
        self.__topic2 = 1
        self.__topic3 = 1
        self.__topic4 = 1
        self.__client = mqtt.Client()
        self.__client.connect(broker, port, stopseconds)
        
    # We can expand to multple topics from the main
    def subcribe(self, topics):
        for topic in topics: 
            self.__client.subscribe(topic)
           
    def on_connect(self , client, userdata, flags, rc):
         print("Connected with result code "+ str(rc))

    def on_message(self ,client, userdata, msg):
        if(msg.topic == 'test/soundboard/esp1'):
            self.topic1 = msg.payload.decode()
            print(f"Message received [{msg.topic}]: {msg.payload}")
        
        if(msg.topic == 'test/soundboard/esp2'):
            self.topic2 = msg.payload.decode()
            print(f"Message received [{msg.topic}]: {msg.payload}")

        if(msg.topic == 'test/soundboard/esp3'):
            self.topic3 = msg.payload.decode()
            print(f"Message received [{msg.topic}]: {msg.payload}")

        if(msg.topic == 'test/soundboard/esp4'):
            self.__topic4 = msg.payload.decode()
            print(f"Message received [{msg.topic}]: {msg.payload}")


    # We use get to call the value of every topic, soo we van do what we want. 
    # We normalize from esp the value
    def getTopic1(self):
        return self.__topic1

    def getTopic2(self):
        return self.__topic2

    def getTopic3(self):
        return self.__topic3

    def getTopic4(self):
        return self.__topic4

    def start(self):
        self.__client.loop_start()
        # we call from client object , the on_connect method and we overwrited
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message

    
        
    

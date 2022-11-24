import paho.mqtt.client as mqtt

class MQTT:
    #init class MQTT
    def __init__(self, broker , port , stopseconds):
        self.__devices = []
        self.__topics = []
        self.__values = []
        self.__client = mqtt.Client()
        self.__client.connect(broker, port, stopseconds)
    
    def devicesTopics(self):
        #sub to all device topics
        for device in self.__devices:
            print(f'connecting to topics of {device}')
            self.subscribe(f'test/esp_{device}/sensor')
        return self 
    
    def subscribe(self, *topics):
        #sub to all given topics
        for topic in topics:
            self.__client.subscribe(topic)
            print(f"subscribed to {topic}")
            #check if topic is not already in topics
            if topic not in self.__topics and 'devices' not in topic:
                self.__topics.append(topic)
            #print to which topic you subbed
            

    #result of connection to broker
    def on_connect(self , client, userdata, flags, rc):
         print(f"Connected with result code {rc}")

    def on_message(self ,client, userdata, msg):
        for i in range(0,len(self.__topics)):
            if(msg.topic == self.__topics[i]):
                self.__values.insert(i,msg.payload.decode())
                print(f"value received [{msg.topic}]: {msg.payload}")

        if('devices' in msg.topic):
            if msg.payload.decode() not in self.__devices:
                self.__devices.append(msg.payload.decode())
                print(f"device [{msg.payload.decode()}] is online")
                self.devicesTopics()

    def getTopics(self):
        return self.__topics

    def getDevices(self):
        return self.__devices

    def getValues(self):
        return self.__values

    def start(self):
        self.__client.loop_start()
        # we call from client object , the on_connect method and we overwrited
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message

    
        
    

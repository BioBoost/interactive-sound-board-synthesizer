import time
from synthesizer import Player, Synthesizer, Waveform
import numpy as np
import random as random
import paho.mqtt.client as mqtt
#For address calling
import ctypes


#Voor later expand 
def run(): 
      mqtt = MQTT("mqtt.devbit.be",1883, 60)
      mqtt.subcribe("test/soundboard/esp1", "test/soundboard/esp2", "test/soundboard/esp3")
      mqtt.on_message()
      mqtt.on_connect()
      #Run the code run()


#Make a class to save the instance 
class ESP:
      #Constructor not needed we get and set values 

    def get_volume(self): 
        return str(self.__volume)

    def get_pitch(self): 
        return self.__pitch

    def set_volume(self, volume): 
        self.__volume = volume

    def set_pitch(self, pitch): 
        self.__pitch = pitch

    
#Call the values
import ctypes
#initialize the variable 
Volume = 0
#Get the memory address of volume
MemoryAddressVolume=id(Volume)

print(MemoryAddressVolume)
#Get the value at at memory address that was 4
ActualValue=ctypes.cast(MemoryAddressVolume,ctypes.py_object).value
print(ActualValue)


client = mqtt.Client()
save = ESP()

client.connect("mqtt.devbit.be",1883,60)
client.subscribe("test/soundboard/esp1")
client.subscribe("test/soundboard/esp2")
#client.subscribe("test/soundboard/esp3")

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
 
  
def on_message(client, userdata, msg):

    
    if(msg.topic == 'test/soundboard/esp1'):
          save.set_volume = msg.payload
          print(f"Message received [{msg.topic}]: {msg.payload}")
          
    
    if(msg.topic == 'test/soundboard/esp2'):
          save.set_pitch1 = msg.payload
          print(f"Message received [{msg.topic}]: {msg.payload}")

    if(msg.topic == 'test/soundboard/esp3'):
          save.set_pitch2 = msg.payload
          print(f"Message received [{msg.topic}]: {msg.payload}")

  

client.loop_start()

# we call from client object , the on_connect method and we overwrited
client.on_connect = on_connect
client.on_message = on_message


while(True):
      print('Buzzy...')
      #Get the memory address
      print(save.get_volume)
      print(save.get_pitch)
      
      time.sleep(1)
    

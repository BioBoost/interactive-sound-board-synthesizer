import time
from synthesizer import Player, Synthesizer, Waveform
import numpy as np
import random as random
import paho.mqtt.client as mqtt
#For address calling
import ctypes
#import the MQTT class
#from mqttclient import MQTT

player = Player()
player.open_stream()
sin = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)

currentChord = 0

#deze code trekt op nieks ma tis een gewone om iets te testen
def playChords(currentChord):
	chord =[329.63, 293.66, 369.9 , 277.18,246.94,293.66,329.63,493.88,440.00,277.18,329.63,440.00]
	
	if save.getChord() >= len(chord):
		save.setChord(0)
	
	#niet aan raken tot mqtt in orde is
	sin._osc1._volume = float(save.getVolume())
	player.play_wave(sin.generate_constant_wave(chord[save.getChord()], save.getDuration()))
	save.setChord(save.getChord() + 1)
	print(save.getChord())

#Voor later expand 
def run(): 
      mqtt = MQTT("mqtt.devbit.be",1883, 60)
      mqtt.subcribe("test/soundboard/esp1", "test/soundboard/esp2", "test/soundboard/esp3")
      mqtt.on_message()
      mqtt.on_connect()
      #Run the code run()


#Make a class to save the instance 
class ESP:
    #default waarde 1 
	def __init__(self):
		self.__volume = 1
		self.__duration = 1
		self.__pitch = 1 #afblijven van de pitch hier moet code nog voor getest worden
		self.__chord = 0

	def setVolume(self , volume):
		self.__volume = volume
		return self

	def setDuration(self , duration):
		self.__duration = duration
		return self

	def setPitch(self , pitch):
		self.__pitch = pitch
		return self

	def getVolume(self):
		return self.__volume

	def getDuration(self):
		return self.__duration

	def getPitch(self):
		return self.__pitch

	def getChord(self):
		return self.__chord
	
	def setChord(self, val):
		self.__chord = val
		return self
    

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
          save.setVolume(msg.payload) 
          print(f"Message received [{msg.topic}]: {msg.payload}")
    if(msg.topic == 'test/soundboard/esp2'):
          save.setDuration(msg.payload) 
          print(f"Message received [{msg.topic}]: {msg.payload}")

    if(msg.topic == 'test/soundboard/esp3'):
          #save.setPitch(msg.payload)
          print(f"Message received [{msg.topic}]: {msg.payload}")

  

client.loop_start()

# we call from client object , the on_connect method and we overwrited
client.on_connect = on_connect
client.on_message = on_message


while(True):
      print('Buzzy...')
      #Get the memory address
      print(save.getVolume())
      print(save.getDuration())
      playChords(currentChord)
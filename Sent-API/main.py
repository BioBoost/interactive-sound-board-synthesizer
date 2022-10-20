import time
#from synthesizer import Player, Synthesizer, Waveform
import numpy as np
import random as random
#For address calling
import ctypes

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

#initialize the variable 
Volume = 0
#Get the memory address of volume
MemoryAddressVolume=id(Volume)

from class_sent import MQTT

mqtt = MQTT("mqtt.devbit.be",1883, 60)
topics = ["test/soundboard/esp1", "test/soundboard/esp2", "test/soundboard/esp3", "test/soundboard/esp4"]
mqtt.subcribe(topics)
mqtt.start()


while(True):
      print('Buzzy...')
      time.sleep(1)
    

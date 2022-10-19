import time
from synthesizer import Player, Synthesizer, Waveform
import numpy as np
import random
import paho.mqtt.client as mqtt

# This is the Subscriber
#define volume

class ESP:
  def __init__(self):
    self.__volume = 1
    self.__duration = 1
    self.__pitch = 1

  def setVolume(self , volume):
    self.__volume = volume

  def setDuration(self , duration):
    self.__duration = duration

esp1 = ESP()

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("test/soundboard/esp1")
  client.subscribe("test/soundboard/esp2")
  client.subscribe("test/soundboard/esp3")

#Topic 
# switch(topic):
    #case test/soundboard/esp1: 
        #Sla je waarde op msg.payload.decode()


def on_message(client, userdata, msg):
  if msg.payload.decode():
    print(msg.payload.decode())
    esp1.volume = msg.payload.decode()
    client.disconnect()
    
client = mqtt.Client()
client.connect("mqtt.devbit.be",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

#stream audio
player = Player()
player.open_stream()


duration = 0.3
#generate a sawtooth wave sound
triangle = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=False)
#generate a sin wave sound
sin = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
#generate a square wave sound
square = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=False)
#generate a sawtooth wave sound
sawtooth = Synthesizer(osc1_waveform=Waveform.sawtooth, osc1_volume=1.0, use_osc2=False)

#play chord
def pitch2frequentie(pitch): 
    return 2**((pitch-69)/12) * 440 # See https://en.wikipedia.org/wiki/Pitch_(music)#Labeling_pitches

nokia = [88, 86, 78, 80, 85, 83, 74, 76, 83, 81, 73, 76, 81]
pitch2 = [50, 60, 70, 80, 90, 80, 100, 20, 10, 81, 73, 76, 81]
chord =[329.63, 293.66, 369.9 , 277.18,246.94,293.66,329.63,493.88,440.00,277.18,329.63,440.00]
chord = np.array(chord)
i = 0

print("print value of volume")
print(esp1.volume)


for note in chord:
    sin._osc1._volume = float(esp1.volume)
    player.play_wave(sin.generate_constant_wave(note, 0.5))
    
#while True:
    #print("check")
    #i = (i + 1) % len(chord)
    #player.play_wave(sin.generate_chord(chord , duration))
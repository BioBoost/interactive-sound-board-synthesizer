from pydub import AudioSegment
from pydub.playback import play
import time
from synthesizer import Player, Synthesizer, Waveform
import numpy as np

#player = Player()
#player.open_stream()

#def frequentie(pitch):
#    return 440 * 2^((pitch-9)/2)
duration = 3.0

#generate a sawtooth wave sound
triangle = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=False)
#generate a sin wave sound
sin = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
#generate a square wave sound
square = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=False)
#generate a sawtooth wave sound
sawtooth = Synthesizer(osc1_waveform=Waveform.sawtooth, osc1_volume=1.0, use_osc2=False)

#load files from soundfiles
sound = AudioSegment.from_file("./soundfiles/BassAmbSlap.mp3")
sound2 = AudioSegment.from_file("./soundfiles/elgitar.wav")

#overlay the sound


#test sound bass
volume = 0
time.sleep(1)
#play louder music
while True:
    volume += 5
    play(sound + volume)

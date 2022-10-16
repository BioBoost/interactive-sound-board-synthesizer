from pydub import AudioSegment
from pydub.playback import play
import time
from synthesizer import Player, Synthesizer, Waveform
import numpy as np

player = Player()
player.open_stream()

def frequentie(pitch):
    return 440 * 2^((pitch-9)/2)

duration = 3.0

#generate a sawtooth wave sound
triangle = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=False)
#generate a sin wave sound
sin = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
#generate a square wave sound
square = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=False)
#generate a sawtooth wave sound
sawtooth = Synthesizer(osc1_waveform=Waveform.sawtooth, osc1_volume=1.0, use_osc2=False)

sound1 = AudioSegment.from_file("./soundfiles/BassAmbSlap.mp3")
sound2 = AudioSegment.from_file("./soundfiles/elgitar.wav")
combined = sound1.overlay(sound2)
combined.export("./soundfiles/combined.wav", format='wav')

play(sound1)
time.sleep(1)
play(sound2)
time.sleep(1)
play(combined)
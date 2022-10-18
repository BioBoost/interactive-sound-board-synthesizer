import time
from synthesizer import Player, Synthesizer, Waveform
import numpy as np

player = Player()
player.open_stream()



duration = 3.0

#generate a sawtooth wave sound
triangle = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=False)
#generate a sin wave sound
sin = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
#generate a square wave sound
square = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=False)
#generate a sawtooth wave sound
sawtooth = Synthesizer(osc1_waveform=Waveform.sawtooth, osc1_volume=1.0, use_osc2=False)

#combined = np.concatenate((sin.generate_constant_wave(440.0, 3.0),triangle.generate_constant_wave(440.0, 3.0)))

#player.play_wave(combined)

#player.play_wave(square.generate_constant_wave(440.0, 3.0))

#player.play_wave(sawtooth.generate_constant_wave(440.0, 3.0))

#player.play_wave(triangle.generate_constant_wave(440.0, 3.0))

#play chord
chord = ["C3", "E3", "G3"]

C = 261.63
Chash = 277.18
D = 293.66

while True:
    player.play_wave(triangle.generate_chord(chord , duration))
    time.sleep(1)

def frequentie(pitch):
    return 440 * 2^((pitch-9)/2)
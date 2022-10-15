from synthesizer import Player, Synthesizer, Waveform
import numpy as np
player = Player()
player.open_stream()

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
player.play_wave(np.concatenate((sin.generate_constant_wave(440.0, 3.0),triangle.generate_constant_wave(440.0, 3.0))))
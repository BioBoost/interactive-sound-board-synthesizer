import matplotlib.pyplot as plt
import numpy as np
import math
import IPython.display as ipd

player = Player()
player.open_stream()

sr = 22050

def makesine(freq, dur):
    t = np.linspace(0, dur, math.ceil(sr*dur))
    x = np.sin(2 * np.pi * freq * t)
    return x

def addsyn(freq, dur, amplist):
    i = 1
    t = np.linspace(0, dur, math.ceil(sr*dur))
    ### initialize a new output
    out = np.zeros(t.size)
    for amp in amplist:
        ### make a sine waveform with this max amplitude
        ### frequency is the integer multiple 
        x = np.multiply(makesine(freq*i, dur), amp)
        ### sum it to the output
        out = out + x
        i+=1
    ### making sure the maximum amplitude does not exeed 1
    if np.max(out)>abs(np.min(out)):
        out = out / np.max(out)
    else:
        out = out / -np.min(out)
    return out

def p2f(pitch):
    freq = 2**((pitch-69)/12) * 440 # See https://en.wikipedia.org/wiki/Pitch_(music)#Labeling_pitches
    return freq

def playmelody(notes, durs, harmonics):
    i = 0
    output = np.array(())
    for i in range(len(notes)):
        y = addsyn(p2f(notes[i]), durs[i], harmonics)
        output = np.concatenate((output, y))
    return output

p = [88, 86, 78, 80, 85, 83, 74, 76, 83, 81, 73, 76, 81]
d = np.multiply([.5, .5, 1, 1, .5, .5, 1, 1, .5, .5, 1, 1, 4], 0.6)
h = [0.141, 0.200, 0.141, 0.112, 0.079, 0.056, 0.050, 0.035, 0.032, 0.020]
print(d)
x = playmelody(p, d, h)

player.play_wave(x)
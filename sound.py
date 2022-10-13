import pyaudio
import numpy as np
import time

p = pyaudio.PyAudio()

volume = 0.3     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 10.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

def sin(fs , duration , f , volume):
    return volume * (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

def paino(fs,duration,f):
    return 0

def testsin(f):
    w = 2*np.pi*f
    return 0.6 * np.sin(1 * w * duration) * np.exp(-0.0015*w*duration)

def get_wave(freq, duration=0.5):
    '''
    Function takes the "frequecy" and "time_duration" for a wave 
    as the input and returns a "numpy array" of values at all points 
    in time
    '''
    
    amplitude = 4096
    t = np.linspace(0, duration, int(fs * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave

# To get a 1 second long wave of frequency 440Hz
a_wave = get_wave(440, 1)



# generate samples, note conversion to float32 array
sample1 = sin(fs,duration,f,volume)
sample2 = testsin(f)
# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)


# play. May repeat with different volume values (if done interactively)


while True:
    #stream.write(sample1)
    stream.write(a_wave)
    time.sleep(100)



stream.stop_stream()
stream.close()

p.terminate()
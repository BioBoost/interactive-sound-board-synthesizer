import random

notes = [
  523.2,
  554.3,
  587.3,
  622.2,
  659.2,
  698.4,
  739.9,
  783.9,
  830.6,
  880.0,
  932.3,
  987.7
]




from synthesizer import Player, Synthesizer, Waveform


player = Player()
player.open_stream()
synthesizer = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=False)

bpm = 240

for i in range(360):
  index = random.randint(0, len(notes)-1)
  player.play_wave(synthesizer.generate_constant_wave(notes[index], 60.0/bpm))
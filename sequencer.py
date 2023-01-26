from synthesizer import Player, Synthesizer, Waveform
import threading

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

class Sequencer:
  def __init__(self, size):
    self.player = Player()
    self.bpm = 120
    self.wave_form = Waveform.sine
    self.sequence = [None] * size

  def start(self):
    self.player.open_stream()
    self.create_synthesizer()
    print("Starting sequencer thread")
    self.keep_playing = True
    self.thread = threading.Thread(target=self.sequencer)
    self.thread.start()

  def set_bpm(self, bpm):
    self.bpm = bpm

  def set_note(self, index, note):
    if index < len(self.sequence) and note < len(notes):
      self.sequence[index] = notes[note]

  def stop(self):
    self.keep_playing = False
    self.thread.join()

  def create_synthesizer(self):
    self.synthesizer = Synthesizer(self.wave_form, osc1_volume=1.0, use_osc2=False)

  def sequencer(self):
    i = 0
    while self.keep_playing:
      if (len(self.sequence) > 0):
        if self.sequence[i] != None:
          self.player.play_wave(self.synthesizer.generate_constant_wave(self.sequence[i], 60.0/self.bpm))
        i = (i + 1) % len(self.sequence)

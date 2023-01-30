from synthesizer import Player, Synthesizer, Waveform
import threading
import time

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
    self.mutex = threading.Lock()

  def start(self):
    self.player.open_stream()
    self.create_synthesizer()
    print("Starting sequencer thread")
    self.keep_playing = True
    self.thread = threading.Thread(target=self.sequencer)
    self.thread.start()

  def set_bpm(self, bpm):
    self.bpm = bpm

  def set_note(self, sequenceIndex, noteIndex):
    if sequenceIndex < len(self.sequence) and noteIndex < len(notes):
      self.sequence[sequenceIndex] = notes[noteIndex]

  # def set_sequence(self, noteIndices=[]):
  #   self.mutex.acquire()
  #   self.sequence = []
  #   for i in noteIndices:
  #     if i < len(notes):
  #       self.sequence.append(notes[i])
  #   self.mutex.release()

  def stop(self):
    self.keep_playing = False
    self.thread.join()

  def create_synthesizer(self):
    self.synthesizer = Synthesizer(self.wave_form, osc1_volume=1.0, use_osc2=False)

  def sequencer(self):
    i = 0
    while self.keep_playing:
      self.mutex.acquire()
      if (len(self.sequence) > 0):
        note = self.sequence[i]
        i = (i + 1) % len(self.sequence)
        self.mutex.release()
        if note != None:
          self.player.play_wave(self.synthesizer.generate_constant_wave(note, 60.0/self.bpm))
      else:
        self.mutex.release()
        time.sleep(60.0/self.bpm)

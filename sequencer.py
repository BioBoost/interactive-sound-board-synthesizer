from synthesizer import Player, Synthesizer, Waveform
import threading
import time

class Sequencer:
  def __init__(self, sequenceSize, notes):
    self.mutex = threading.Lock()
    self.player = Player()
    self.set_bpm(120)
    self.set_wave_form(Waveform.sine)
    self.size = sequenceSize
    self.sequence = [None] * sequenceSize
    self.notes = notes

  def start(self):
    self.player.open_stream()
    self.keep_playing = True
    self.thread = threading.Thread(target=self.__sequencer)
    self.thread.start()

  def set_bpm(self, bpm):
    self.bpm = bpm

  def set_note(self, sequenceIndex, noteIndex):
    if sequenceIndex < len(self.sequence) and noteIndex < len(self.notes):
      self.mutex.acquire()
      self.sequence[sequenceIndex] = self.notes[noteIndex]
      self.mutex.release()

  def set_wave_form(self, waveForm):
    self.mutex.acquire()
    self.synthesizer = Synthesizer(waveForm, osc1_volume=0.5, use_osc2=False)
    self.mutex.release()

  def stop(self):
    self.keep_playing = False
    self.thread.join()

  def __sequencer(self):
    i = 0
    while self.keep_playing:
      self.mutex.acquire()
      note = self.sequence[i]
      i = (i + 1) % self.size
      self.mutex.release()
      if note != None:
        self.player.play_wave(self.synthesizer.generate_constant_wave(note, 60.0/self.bpm))
      else:
        time.sleep(60/self.bpm)

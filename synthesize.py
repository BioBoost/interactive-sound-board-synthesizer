from synthesizer import Player, Synthesizer, Waveform
#Make a class to save the instance 

class Synthesize:
	def __init__(self):
		self.__volume = 0.5
		self.__duration = 0.5
		self.__pitch = 1 #afblijven van de pitch hier moet code nog voor getest worden
		self.__chord = 0
		self.__player = Player()
		self.__sin = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
		self.__player.open_stream()
		

	def setVolume(self , volume):
		self.__volume = volume
		return self

	def setDuration(self , duration):
		self.__duration = duration
		return self

	def setPitch(self , pitch):
		self.__pitch = pitch
		return self

	def getVolume(self):
		return self.__volume

	def getDuration(self):
		return self.__duration

	def getPitch(self):
		return self.__pitch

	def playChords(self):
		
		Octave4 = [261 , 277.18 , 293.66 , 311.13 , 329.63 , 349.23 , 369.99 , 392 , 415.3 , 440 , 466.16 , 493.88]
		if self.__chord >= len(Octave4):
			self.__chord = 0
		
		#niet aan raken tot mqtt in orde is
		self.__sin._osc1._volume = float(self.getVolume())
		self.__player.play_wave(self.__sin.generate_constant_wave(Octave4[self.__chord], self.getDuration()))
		self.__chord += 1
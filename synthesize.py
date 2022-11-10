from synthesizer import Player, Synthesizer, Waveform
import numpy as np


class Synthesize:
	def __init__(self):
		self.__volume = 0.5
		self.__duration = 1
		self.__pitch = 1 #afblijven van de pitch hier moet code nog voor getest worden
		self.__currentchord = 0
		self.__chord = [0,0,0]

		self.__esp1 = 0
		self.__esp2 = 0
		self.__esp3 = 0
		self.__esp4 = 1

		self.__octave4 = {0:(0) , 1:(256.8912) , 2:(272.13184) , 3:(288.3152) , 4:(305.5984) , 5:(323.6672) , 6:(342.99296) , 7:(363.26144) , 8:(384.944) , 9:(407.88352) , 10:(432.08) , 11:(457.84768) , 12:(485.02944)}
		self.__octave2 = [64.2228 , 68.03296 , 72.0788 , 76.3996 , 80.91536 , 85.74824 , 90.81536 , 96.236 , 101.97088 , 108.02 , 114.46192 , 121.25736]

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

	#esp1
	def setEsp1(self , esp1):
		self.__esp1 = esp1
		return self
	
	def getEsp1(self):
		return self.__esp1

	#esp2
	def setEsp2(self , esp2):
		self.__esp2 = esp2
		return self
	
	def getEsp2(self):
		return self.__esp2

	#esp3
	def setEsp3(self , esp3):
		self.__esp3 = esp3
		return self
	
	def getEsp3(self):
		return self.__esp3

	#esp4
	def setEsp4(self , esp4):
		self.__esp4 = esp4
		return self
	
	def getEsp4(self):
		return self.__esp4


	def selectChords(self):
		#note1 = round(float(note1) * 12)
		#if note1 < 1:
			#note1 = 1
		
		note1 = round(float(self.__esp1) * 12)
		note2 = round(float(self.__esp2) * 12)
		note3 = round(float(self.__esp3) * 12)

		self.__chord[0] = self.__octave4[int(note1)]
		self.__chord[1] = self.__octave4[int(note2)]
		self.__chord[2] = self.__octave4[int(note3)]
		#print(self.__chord)
		return self

	def playChords(self):
		for note in self.__chord:
			self.__sin._osc1._volume = float(self.getVolume())
			self.__player.play_wave(self.__sin.generate_constant_wave(note, self.__esp3))
			self.__currentchord += 1


	def playChordstest(self):
		
		Octave4 = [256.8912 , 272.13184 , 288.3152 , 305.5984 , 323.6672 , 342.99296 , 363.26144 , 384.944 , 407.88352 , 432.08 , 457.84768 , 485.02944]
		Octave2 = [64.2228 , 68.03296 , 72.0788 , 76.3996 , 80.91536 , 85.74824 , 90.81536 , 96.236 , 101.97088 , 108.02 , 114.46192 , 121.25736]
		if self.__currentchord >= len(Octave4):
			self.__currentchord = 0
		#niet aan raken tot mqtt in orde is
		self.__sin._osc1._volume = float(self.getVolume())
		self.__player.play_wave(self.__sin.generate_constant_wave(Octave4[self.__currentchord], self.getDuration()))
		#self.__player.play_wave(self.__sin.generate_constant_wave(Octave2[self.__currentchord], self.getDuration()))
		self.__currentchord += 1
from synthesizer import Player, Synthesizer, Waveform
import numpy as np

class Synthesize:
	def __init__(self):
		self.__volume = 0.5
		self.__duration = 0.5
		self.__pitch = 1 #afblijven van de pitch hier moet code nog voor getest worden
		self.__currentchord = 0
		self.__chord = [1,1]

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

	def selectChords(self,note1):
		octave4 = {1:(256.8912) , 2:(272.13184) , 3:(288.3152) , 4:(305.5984) , 5:(323.6672) , 6:(342.99296) , 7:(363.26144) , 8:(384.944) , 9:(407.88352) , 10:(432.08) , 11:(457.84768) , 12:(485.02944)}
		note1 = round(float(note1) * 12)
		if note1 < 1:
			note1 = 1
		self.__chord[0] = octave4[int(note1)]

		#print(self.__chord)
		return self

	def playChords(self):
		#Octave4 = [256.8912 , 272.13184 , 288.3152 , 305.5984 , 323.6672 , 342.99296 , 363.26144 , 384.944 , 407.88352 , 432.08 , 457.84768 , 485.02944]
		for note in self.__chord:
			self.__sin._osc1._volume = float(self.getVolume())
			self.__player.play_wave(self.__sin.generate_constant_wave(note, self.getDuration()))
			self.__currentchord += 1


	def playChordstest(self):
		
		Octave4 = [256.8912 , 272.13184 , 288.3152 , 305.5984 , 323.6672 , 342.99296 , 363.26144 , 384.944 , 407.88352 , 432.08 , 457.84768 , 485.02944]

		if self.__currentchord >= len(Octave4):
			self.__currentchord = 0
		
		#niet aan raken tot mqtt in orde is
		self.__sin._osc1._volume = float(self.getVolume())
		self.__player.play_wave(self.__sin.generate_constant_wave(Octave4[self.__currentchord], self.getDuration()))
		self.__currentchord += 1
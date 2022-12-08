from synthesizer import Player, Synthesizer, Waveform

class Synthesize:
	def __init__(self):
		self.__volume = 0.5
		self.__notes = []

		self.__octave4 = {0:(0) , 1:(256.8912) , 2:(272.13184) , 3:(288.3152) , 4:(305.5984) , 5:(323.6672) , 6:(342.99296) , 7:(363.26144) , 8:(384.944) , 9:(407.88352) , 10:(432.08) , 11:(457.84768) , 12:(485.02944)}
		self.__octave2 = {0:(0) , 1:(64.2228) , 2:(68.03296) , 3:(72.0788) , 4:(76.3996) , 5:(80.91536) , 6:(85.74824) , 7:(90.81536) , 8:(96.236) , 9:(101.97088) , 10:( 108.02) , 11:(114.46192) , 12:(121.25736)}

		self.__frequentie = 1

		self.__player = Player()
		self.__wave = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
		#open audio stream
		self.__player.open_stream()
	
	def SetWave(self,wave):
		if wave == "sinus":
			self.__wave = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
		elif wave == "triangle":
			self.__wave = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=False)
		elif wave == "square":
			self.__wave = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=False)
		elif wave == "sawtooth":
			self.__wave = Synthesizer(osc1_waveform=Waveform.sawtooth, osc1_volume=1.0, use_osc2=False)
		return self
		
	def setVolume(self , volume):
		if volume == 0:
			volume = 0.1
		self.__volume = volume
		return self

	def getVolume(self):
		return self.__volume

	def setFrequentie(self , frequentie):
		self.__frequentie = frequentie
		return self

	def getFrequnetie(self):
		return self.__frequentie

	def SortNotes(self, value,index):
		#round de waarde en zet om naar een getal tussen 0 - 12
		#print(f'avg value is: {value}')
		#print(f'index is: {index}')
		if(len(self.__notes) < index + 1):
			self.__notes.append(self.__octave4[round(value * 12)])
		else:
			self.__notes[index] =  self.__octave4[round(value * 12)]

	def PlayNotes(self):
		#print(self.__notes)
		if len(self.__notes) is not 0:
			for note in self.__notes:
				self.__wave._osc1._volume = float(self.getVolume())
				self.__player.play_wave(self.__wave.generate_constant_wave(note, self.__frequentie))
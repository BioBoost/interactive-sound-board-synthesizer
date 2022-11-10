from synthesizer import Player, Synthesizer, Waveform

class Synthesize:
	def __init__(self):
		self.__volume = 0.5
		self.__notes = [0,0,0]

		self.__esp1 = 0
		self.__esp2 = 0
		self.__esp3 = 0
		self.__esp4 = 1

		self.__octave4 = {0:(0) , 1:(256.8912) , 2:(272.13184) , 3:(288.3152) , 4:(305.5984) , 5:(323.6672) , 6:(342.99296) , 7:(363.26144) , 8:(384.944) , 9:(407.88352) , 10:(432.08) , 11:(457.84768) , 12:(485.02944)}
		self.__octave2 = {0:(0) , 1:(64.2228) , 2:(68.03296) , 3:(72.0788) , 4:(76.3996) , 5:(80.91536) , 6:(85.74824) , 7:(90.81536) , 8:(96.236) , 9:(101.97088) , 10:( 108.02) , 11:(114.46192) , 12:(121.25736)}

		self.__player = Player()
		#generate a triangle wave sound
		self.__triangle = Synthesizer(osc1_waveform=Waveform.triangle, osc1_volume=1.0, use_osc2=False)
		#generate a sin wave sound
		self.__sin = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
		#generate a square wave sound
		self.__square = Synthesizer(osc1_waveform=Waveform.square, osc1_volume=1.0, use_osc2=False)
		#generate a sawtooth wave sound
		self.__sawtooth = Synthesizer(osc1_waveform=Waveform.sawtooth, osc1_volume=1.0, use_osc2=False)
		#open audio stream
		self.__player.open_stream()
		

	def setVolume(self , volume):
		self.__volume = volume
		return self

	def getVolume(self):
		return self.__volume

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
		#zorgt ervoor dat de frequentie nooit nul is
		if esp4 == 0:
			esp4 = 0.1
		self.__esp4 = esp4
		return self
	
	def getEsp4(self):
		return self.__esp4

	def selectNotes(self):
		#round de waarde en zet om naar een getal tussen 0 - 12
		note1 = round(float(self.__esp1) * 12)
		note2 = round(float(self.__esp2) * 12)
		note3 = round(float(self.__esp3) * 12)
		#zet noten in volgorde
		self.__notes[0] = self.__octave4[int(note1)]
		self.__notes[1] = self.__octave4[int(note2)]
		self.__notes[2] = self.__octave4[int(note3)]
		return self

	def playNotes(self):
		for note in self.__notes:
			self.__sin._osc1._volume = float(self.getVolume())
			self.__player.play_wave(self.__sin.generate_constant_wave(note, self.__esp3))
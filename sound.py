#import the MQTT class
from mqttclient import MQTT
from synthesize import Synthesize
import time

synth = Synthesize()

mqtt = MQTT("mqtt.devbit.be",1883, 60)
mqtt.subcribe("test/soundboard/esp1", "test/soundboard/esp2", "test/soundboard/esp3", "test/soundboard/esp4")
mqtt.start()

while(True):
	print('Buzzy...')
	#get values
	synth.setEsp1(mqtt.getTopic1())
	synth.setEsp2(mqtt.getTopic2())
	synth.setEsp3(mqtt.getTopic3())
	synth.setEsp4(mqtt.getTopic4())
	#select notes
	synth.selectChords()
	#play notes
	synth.playChords()
	print('')
#import the MQTT and Synthesize class
from mqttclient import MQTT
from synthesize import Synthesize

#synthesizer class
synth = Synthesize()

#mqtt class
mqtt = MQTT("mqtt.devbit.be",1883,60)
#subscribe to all topics
mqtt.subcribe("test/soundboard/esp1", "test/soundboard/esp2", "test/soundboard/esp3", "test/soundboard/esp4")
mqtt.start()

while(True):
	print('Destroying audio demons')
	#get values
	synth.setEsp1(mqtt.getTopic1())
	synth.setEsp2(mqtt.getTopic2())
	synth.setEsp3(mqtt.getTopic3())
	synth.setEsp4(mqtt.getTopic4())
	#select notes
	synth.selectNotes()
	#play notes
	synth.playNotes()
	print('')
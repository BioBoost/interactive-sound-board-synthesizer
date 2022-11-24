#import the MQTT and Synthesize class
from mqttclient import MQTT
from synthesize import Synthesize
import time
#synthesizer class
synth = Synthesize()

#mqtt connect to broker
mqtt = MQTT("mqtt.devbit.be",1883,60)
#get all available devices
mqtt.subscribe("test/devices/")
#subscribe to all topics
mqtt.start()

while(True):
    print(mqtt.getDevices())
    print(mqtt.getTopics())
    time.sleep(1)
	#print('Destroying audio demons')
	#get values
	#synth.setEsp1(mqtt.getTopic1())
	#synth.setEsp2(mqtt.getTopic2())
	#synth.setEsp3(mqtt.getTopic3())
	#synth.setEsp4(mqtt.getTopic4())
	#select notes
	#synth.selectNotes()
	#play notes
	#synth.playNotes()
	#print('')	
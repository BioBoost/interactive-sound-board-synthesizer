#import the MQTT and Synthesize class
from mqttclient import MQTT
from synthesize import Synthesize
import time
#synthesizer class
synth = Synthesize()

#mqtt connect to broker
mqtt = MQTT("172.16.102.216",1883,60)
#get all available devices
mqtt.subscribe("test/devices/")
mqtt.start()

while(True):
    print("")
    #print(f'all available devices{mqtt.getAvailableDevices()}')
    mqtt.selectAllDevices()
    #print(f'all connected devices {mqtt.getDevices()}')
    #print(f'all topics {mqtt.getTopics()}')
    mqtt.sensorValues()
    print("")
    time.sleep(10)
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
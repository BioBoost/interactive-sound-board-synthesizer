#import the MQTT class
from mqttclient import MQTT
from synthesize import Synthesize

synth = Synthesize()

mqtt = MQTT("mqtt.devbit.be",1883, 60)
mqtt.subcribe("test/soundboard/esp1", "test/soundboard/esp2", "test/soundboard/esp3", "test/soundboard/esp4")
mqtt.start()
      
while(True):
	print('Buzzy...')
	synth.setVolume(mqtt.getTopic1())
	synth.setDuration(mqtt.getTopic2())
	print(synth.getVolume())
	print(synth.getDuration())
	synth.playChords()
	print('')
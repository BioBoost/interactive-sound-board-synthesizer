#import the MQTT and Synthesize class
from mqttclient import MQTT
from synthesize import Synthesize
import time
#synthesizer class
synth = Synthesize()

#mqtt connect to broker
mqtt = MQTT("pi-of-terror",1883,60,synth)
#get all available devices
mqtt.subscribe("test/devices/","test/frontend/volume",'test/frontend/octave','test/frontend/wave','test/frontend/frequency','test/frontend')
mqtt.start()

mqtt.SendConfig()

while(True):
    mqtt.sensorValues()
    synth.PlayNotes()
    #if(len(mqtt.getDevices()) != 0):
    #    print(f'all devices {mqtt.getDevices()}')
    time.sleep(0.08)
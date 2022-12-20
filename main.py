#import the MQTT and Synthesize class
from mqttclient import MQTT
from synthesize import Synthesize

#synthesizer class
synth = Synthesize()

#mqtt connect to broker
mqtt = MQTT("pi-of-terror",1883,60,synth)
#sub to topics of frontend and devices
mqtt.subscribe("test/devices/","test/frontend/volume",'test/frontend/octave','test/frontend/wave','test/frontend/frequency','test/frontend')
#start de mqtt loop
mqtt.start()
#send Huidige config
mqtt.SendConfig()

while(True):
    #get values en activate sensor
    mqtt.sensorValues()
    #play the current notes
    synth.PlayNotes()
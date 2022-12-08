#import the MQTT and Synthesize class
from mqttclient import MQTT
from synthesize import Synthesize
import time
#synthesizer class
synth = Synthesize()

#mqtt connect to broker
mqtt = MQTT("pi-of-terror",1883,60,synth)
#get all available devices
mqtt.subscribe("test/devices/")
mqtt.start()

while(True):
    mqtt.selectAllDevices()
    mqtt.sensorValues()
    #mqtt.SendConfig()
    synth.PlayNotes()
    print("")
    time.sleep(0.001)
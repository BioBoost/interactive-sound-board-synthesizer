import paho.mqtt.client as mqtt
from enum import Enum
import json
import time

lastTime = time.perf_counter()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("sonic/modules/measurements")
  client.publish('sonic/modules/esp32-sonic-e36270/commands', '{ "cmd": "measure" }')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  global lastTime

  # print(msg.topic+" "+str(msg.payload))
  jsonData = json.loads(msg.payload)

  currentTime = time.perf_counter()
  timeDiff = currentTime - lastTime
  lastTime = currentTime
  timeDiff = round(1000 * timeDiff)

  if (jsonData['distance'] > 0):
    print("Distance: " + str(jsonData['distance']) + "\t\tdT: " + str(timeDiff) + "ms")
  else:
    print("Invalid distance")

  client.publish('sonic/modules/esp32-sonic-e36270/commands', '{ "cmd": "measure" }')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.devbit.be", 1883, 30)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

# Conclusion:
# Round trip for a single measurement is 50ms on average but can sometimes take 150ms to 200ms
# Distance: 16            dT: 78ms
# Distance: 15            dT: 126ms
# Distance: 15            dT: 51ms
# Distance: 13            dT: 50ms
# Distance: 12            dT: 50ms
# Distance: 12            dT: 53ms
# Distance: 154           dT: 83ms
# Distance: 171           dT: 137ms
# Distance: 132           dT: 82ms
# Distance: 140           dT: 167ms
# Distance: 172           dT: 58ms
# Distance: 153           dT: 48ms
# Distance: 147           dT: 48ms
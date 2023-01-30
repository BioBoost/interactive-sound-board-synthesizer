from enum import Enum
import paho.mqtt.client as mqtt
import json
from dataclasses import dataclass
from threading import Lock
import time
import copy

class DeviceStatus(Enum):
  IDLE = 1              # No updates yet, just registered
  UPDATING = 3          # Publish is send, waiting for update
  UPDATED = 4           # Received update
  INVALID = 6           # Received a 0 distance (which is invalid) or device timed out, whatever

@dataclass
class Device:
  id: str = ""
  distance: int = 0
  state: DeviceStatus = DeviceStatus.IDLE

class SonicApi:
  def __init__(self, broker, baseTopic, brokerPort=1883):
    self.broker = broker
    self.brokerPort = brokerPort
    self.baseTopic = baseTopic
    self.iDeviceUpdate = 0
    self.registeredDevices = []
    self.updateRequestTime = 0

  def connect(self):
    self.client = mqtt.Client()
    self.client.on_connect = self.__on_connected
    self.client.on_message = self.__on_message
    self.client.connect(self.broker, self.brokerPort, 30)
    self.client.loop_start()

  # The device update system just updates the next device in line
  # You can call this method slow or fast but it can never update
  # faster than the devices provide updates.
  def request_next_device_update(self, timeoutMs=2000):
    if len(self.registeredDevices) == 0: return

    # First we check if device is still awaiting update
    device = self.registeredDevices[self.iDeviceUpdate]

    # if device.state == DeviceStatus.UPDATING:
    #   elapsedTime = time.perf_counter() - self.updateRequestTime
    #   if (1000*elapsedTime) >= timeoutMs:
    #     print("Timed out with " + str(int(1000*elapsedTime)))
    #     device.state = DeviceStatus.INVALID
    # else:
    if device.state != DeviceStatus.UPDATING:
      self.iDeviceUpdate = (self.iDeviceUpdate + 1) % len(self.registeredDevices)
      device = self.registeredDevices[self.iDeviceUpdate]
      # if device.state != DeviceStatus.TIMED_OUT:
      message = { "cmd": "measure" }
      device.state = DeviceStatus.UPDATING
      self.client.publish(self.baseTopic + "/modules/" + device.id + "/commands", json.dumps(message))
      self.updateRequestTime = time.perf_counter()

  def disconnect(self):
    self.client.loop_stop()

  def __on_connected(self, client, userdata, flags, rc):
    print("Connected to MQTT broker")
    self.__subscribe_to_modules()
    self.client.publish('sonic/modules/esp32-sonic-e36270/commands', '{ "cmd": "measure" }')

  # New device discovered or just alive message
  def __on_hello_message(self, client, userdata, msg):
    jsonData = json.loads(msg.payload)
    id = jsonData['id']

    print("Received hello from " + id)

    device = self.__get_device_by_id(id)
    if device == None:
      self.__register_device(Device(id=id))
    elif device.state == DeviceStatus.INVALID:
      device.state == DeviceStatus.IDLE

  def __register_device(self, device):
    print("Registering new device")
    # self.mutex.acquire()    # Because we change the actual device list !
    self.registeredDevices.append(device)
    # self.mutex.release()

  def __on_measurement_message(self, client, userdata, msg):
    jsonData = json.loads(msg.payload)
    id = jsonData['id']
    
    device = self.__get_device_by_id(id)
    if device == None:
      print("Got measurement for unknown device")
      return

    distance = jsonData['distance']
    if distance > 0:
      device.distance = distance
      device.state = DeviceStatus.UPDATED
      print("Received distance of " + str(distance))
      # TODO: Schedule call to callback for device update

  def __on_message(self, client, userdata, msg):
    print("Received unknown message from broker @ " + msg.topic)
    jsonData = json.loads(msg.payload)

    if (jsonData['distance'] > 0):
      print("Distance: " + str(jsonData['distance']))
    else:
      print("Invalid distance")

    client.publish('sonic/modules/esp32-sonic-e36270/commands', '{ "cmd": "measure" }')


  def __subscribe_to_modules(self):
    print("Subscribing to modules topic")
    self.client.subscribe(self.baseTopic + "/modules/hello")
    self.client.message_callback_add(self.baseTopic + "/modules/hello", self.__on_hello_message)
    self.client.subscribe(self.baseTopic + "/modules/measurements")
    self.client.message_callback_add(self.baseTopic + "/modules/measurements", self.__on_measurement_message)

  def __get_device_by_id(self, id):
    for device in self.registeredDevices:
      if device.id == id:
        return device
    
    return None

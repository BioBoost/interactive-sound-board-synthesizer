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

class Device:
  id: str = ""
  distance: int = 0
  state: DeviceStatus = DeviceStatus.IDLE

  def __init__(self, id):
    self.id = id
    self.mutex = Lock()

  def set_state(self, state):
    self.mutex.acquire()
    self.state = state
    self.mutex.release()

  def get_state(self):
    self.mutex.acquire()
    state = self.state
    self.mutex.release()
    return state

  def __str__(self):
    self.mutex.acquire()
    output = "{" + str(self.id) + "} " + str(self.distance) + "cm | state = " + str(self.state)
    self.mutex.release()
    return output

  def __repr__(self):
    return self.__str__()

class SonicApi:
  def __init__(self, broker, baseTopic, brokerPort=1883):
    self.broker = broker
    self.brokerPort = brokerPort
    self.baseTopic = baseTopic
    self.iDeviceUpdate = 0
    self.registeredDevices = []
    self.updateRequestTime = 0
    self.mutex = Lock()     # This is just for the array registeredDevices (adding or getting items)
                            # Devices themselves are protected internally
    self.updateRequestTime = time.perf_counter()
    self.updateCallback = None

  def connect(self):
    self.client = mqtt.Client()
    self.client.on_connect = self.__on_connected
    self.client.on_message = self.__on_message
    self.client.connect(self.broker, self.brokerPort, 30)
    self.client.loop_start()

  def set_update_callback(self, function):
    self.updateCallback = function

  # The device update system just updates the next device in line
  # You can call this method slow or fast but it can never update
  # faster than the devices provide updates.
  def request_next_device_update(self, timeoutMs=300):
    if self.__get_number_of_devices() == 0: return

    # First we check if device is still awaiting update
    device = self.__get_device_by_index(self.iDeviceUpdate)

    if device.state == DeviceStatus.UPDATING:
      elapsedTime = time.perf_counter() - self.updateRequestTime
      if (1000*elapsedTime) >= timeoutMs:
        print("Timed out with " + str(int(1000*elapsedTime)))
        device.state = DeviceStatus.INVALID
    else:
      self.iDeviceUpdate = (self.iDeviceUpdate + 1) % self.__get_number_of_devices()
      device = self.__get_device_by_index(self.iDeviceUpdate)
      message = { "cmd": "measure" }
      device.set_state(DeviceStatus.UPDATING)
      self.client.publish(self.baseTopic + "/modules/" + device.id + "/commands", json.dumps(message))
      self.updateRequestTime = time.perf_counter()

  def disconnect(self):
    self.client.loop_stop()

  def __on_connected(self, client, userdata, flags, rc):
    print("Connected to MQTT broker")
    self.__subscribe_to_modules()

  # New device discovered or just alive message
  def __on_hello_message(self, client, userdata, msg):
    jsonData = json.loads(msg.payload)
    id = jsonData['id']

    print("Received hello from " + id)

    device = self.__get_device_by_id(id)
    if device == None:
      self.__register_device(Device(id=id))
    elif device.get_state() == DeviceStatus.INVALID:
      device.set_state(DeviceStatus.IDLE)

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
      device.set_state(DeviceStatus.UPDATED)
      self.__call_update_callback(device)
    else:
      device.set_state(DeviceStatus.INVALID)

  def __call_update_callback(self, device):
    if self.updateCallback != None:
      self.updateCallback(device.id, device.distance)

  def __on_message(self, client, userdata, msg):
    print("Received unknown message from broker @ " + msg.topic)

  def __subscribe_to_modules(self):
    print("Subscribing to modules topic")
    self.client.subscribe(self.baseTopic + "/modules/hello")
    self.client.message_callback_add(self.baseTopic + "/modules/hello", self.__on_hello_message)
    self.client.subscribe(self.baseTopic + "/modules/measurements")
    self.client.message_callback_add(self.baseTopic + "/modules/measurements", self.__on_measurement_message)

  def __register_device(self, device):
    print("Registering new device: " + device.id)
    self.mutex.acquire()    # Because we change the actual device list !
    self.registeredDevices.append(device)
    self.mutex.release()

  def __get_number_of_devices(self):
    self.mutex.acquire()
    count = len(self.registeredDevices)
    self.mutex.release()
    return count

  def __get_device_by_index(self, index):
    device = None
    self.mutex.acquire()
    if index < len(self.registeredDevices):
      device = self.registeredDevices[index]
    self.mutex.release()
    return device

  def __get_device_by_id(self, id):
    device = None
    self.mutex.acquire()
    for dev in self.registeredDevices:
      if dev.id == id:
        device = dev
    self.mutex.release()
    return device
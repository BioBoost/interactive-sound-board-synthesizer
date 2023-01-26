from enum import Enum
import paho.mqtt.client as mqtt
import json
from dataclasses import dataclass
from threading import Lock
import time

class DeviceStatus(Enum):
  IDLE = 1              # No updates yet, just registered
  UPDATING = 3          # Publish is send, waiting for update
  UPDATED = 4           # Received update
  TIMED_OUT = 5

# IDLE (or UPDATED) => UPDATING => UPDATED or TIMED_OUT

@dataclass
class Device:
  id: str = ""
  distance: int = 0
  state: DeviceStatus = DeviceStatus.IDLE

# TODO: How do we detect disconnected devices ?

class SonicApi:
  def __init__(self, broker, baseTopic):
    self.broker = broker
    self.brokerPort = 1883
    self.baseTopic = baseTopic
    self.registeredDevices = []
    self.iUpdateIndex = 0
    self.mutex = Lock()

  def connect(self):
    self.client = mqtt.Client()
    self.client.on_connect = self._on_connected
    self.client.on_message = self._on_message
    self.client.connect(self.broker, self.brokerPort, 30)
    self.client.loop_start()
    self._subscribe_to_modules()

  def disconnect(self):
    self.client.loop_stop()

  def _on_connected(self, client, userdata, flags, rc):
    print("Connected to MQTT broker")
    self._publish_controller_active()

  def _on_message(self, client, userdata, msg):
    print("Received message from broker @ " + msg.topic)
    jsonData = json.loads(msg.payload)

    # Detect if new device
    self.mutex.acquire()

    if msg.topic == self.baseTopic + "/modules/hello":
      self._register_device(jsonData)
      # self.registeredDevices[jsonData['id']] = Device(id=jsonData['id'])
    elif msg.topic == self.baseTopic + "/modules/measurements":
      device = self._get_device_by_id(jsonData['id'])
      if device != None:
        device.distance = jsonData['distance']
        device.state = DeviceStatus.UPDATED
      else:
        print("Got update from unknown device")

    self.mutex.release()

  # The device update system just updates the next device in line
  # You can call this method slow or fast but it can never update
  # faster than the devices provide updates.
  def request_next_device_update(self, timeoutMs=2000):
    if len(self.registeredDevices) == 0: return

    self.mutex.acquire()
    
    # First we check if device is still awaiting update
    if self.registeredDevices[self.iUpdateIndex].state == DeviceStatus.UPDATING:
      elapsedTime = time.perf_counter() - self.updateRequestTime
      if (1000*elapsedTime) > timeoutMs:
        self.registeredDevices[self.iUpdateIndex].state = DeviceStatus.TIMED_OUT
    else:
      self.iUpdateIndex = (self.iUpdateIndex + 1) % len(self.registeredDevices)
      device = self.registeredDevices[self.iUpdateIndex]
      if device.state != DeviceStatus.TIMED_OUT:
        message = { "cmd": "measure" }
        device.state = DeviceStatus.UPDATING
        self.client.publish(self.baseTopic + "/modules/" + device.id + "/commands", json.dumps(message))
        self.updateRequestTime = time.perf_counter()
    
    self.mutex.release()

  def _get_device_by_id(self, id):
    # TODO: Crashes with TypeError: 'module' object is not subscriptable
    # devices = list(filter(lambda d : d.id == json['id'], self.registeredDevices))
    # if len(devices) == 0:
    #   return None
    # else:
    #   return devices[0]

    for device in self.registeredDevices:
      if device.id == id:
        return device
    
    return None

  def _register_device(self, json):
    existing = self._get_device_by_id(json['id'])

    if existing != None:
      existing[0].state = DeviceStatus.IDLE
    else:
      self.registeredDevices.append(Device(id=json['id']))
  
  def get_registered_devices(self):
    return self.registeredDevices

  def _publish_controller_active(self):
    message = {
      "ip": "_here_comes_ip",
      "version": "v0.1",
      "who": "synthesizer"
    }
    self.client.publish(self.baseTopic, json.dumps(message))

  def _subscribe_to_modules(self):
    print("Subscribing to modules topic")
    self.client.subscribe(self.baseTopic + "/modules/hello")
    self.client.subscribe(self.baseTopic + "/modules/measurements")

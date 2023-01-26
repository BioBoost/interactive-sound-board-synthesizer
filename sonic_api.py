import paho.mqtt.client as mqtt
import json

class SonicApi:
  def __init__(self, broker, baseTopic):
    self.broker = broker
    self.brokerPort = 1883
    self.baseTopic = baseTopic

  def connect(self):
    self.client = mqtt.Client()
    self.client.on_connect = self._on_connected
    self.client.on_message = self._on_message
    self.client.connect(self.broker, self.brokerPort, 30)
    self.client.loop_start()
    self.subscribe_to_modules()

  def disconnect(self):
    self.client.loop_stop()

  def _on_connected(self, client, userdata, flags, rc):
    print("Connected to MQTT broker")
    self.publish_controller_active()

  def _on_message(self, client, userdata, msg):
    print("Received message from broker")
  
  def publish_controller_active(self):
    message = {
      "ip": "_here_comes_ip",
      "version": "v0.1",
      "who": "synthesizer"
    }
    self.client.publish(self.baseTopic, json.dumps(message))

  def subscribe_to_modules(self):
    print("Subscribing to modules topic")
    self.client.subscribe(self.baseTopic + "/modules")

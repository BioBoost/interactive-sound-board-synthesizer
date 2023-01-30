import sequencer as sq
import time
import signal
import sonic_api as sapi

keep_listening = True

def handler(signum, frame):
    msg = "Ctrl-c was pressed. Closing the app ..."
    print(msg, end="", flush=True)
    keep_listening = False
    sequencer.stop()
    exit()
 
signal.signal(signal.SIGINT, handler)

# sequencer.set_bpm(120)
# sequencer.set_note(0, 3)
# sequencer.set_note(1, 5)
# sequencer.set_note(2, 7)
# sequencer.set_note(3, 2)

sonicApi = sapi.SonicApi("mqtt.devbit.be", "sonic")
sonicApi.connect()

deviceMapping = {
  'esp32-sonic-f10f7c': ('note', 0),
  'esp32-sonic-e2c6c4': ('note', 1),
  'esp32-sonic-e29abc': ('note', 2),
  'esp32-sonic-e36270': ('note', 3),
  # 'xxx': ('bpm')
}

sequencer = sq.Sequencer(4)
sequencer.start()

while keep_listening:
  time.sleep(0.05)
  sonicApi.request_next_device_update()
  print(sonicApi.get_active_devices())

  devices = sonicApi.get_active_devices()
  for device in devices:
    distance = min([device.distance, 100])
    if device.id in deviceMapping:
      config = deviceMapping[device.id]
      if config[0] == 'note':
        index = config[1]
        noteIndex = int(len(sq.notes) * distance / 100.0)
        sequencer.set_note(index, noteIndex)
      # elif npm
    else:
      print("No device mapping found for " + device.id)

import sequencer as sq
import notes as nt
import time
import signal
import sonic_api as sa

notes = nt.BASIC_NOTES        # Choose notes here

keep_listening = True

def handler(signum, frame):
  global keep_listening

  msg = "Ctrl-c was pressed. Closing the app ..."
  print(msg, end="", flush=True)
  keep_listening = False
  sequencer.stop()
  exit()
 
signal.signal(signal.SIGINT, handler)

sequencer = sq.Sequencer(4, notes)
sequencer.set_bpm(360)
sequencer.start()

sonics = sa.SonicApi("141.105.126.62", "sonic")
sonics.connect()

deviceMapping = {
  'esp32-sonic-f10f7c': ('note', 0),
  'esp32-sonic-e2c6c4': ('note', 1),
  'esp32-sonic-e29abc': ('note', 2),
  'esp32-sonic-e36270': ('note', 3),
  # 'xxx': ('bpm')
}

def on_device_update(id, distance):
  print("Update: " + str(id) + " | " + str(distance))

  distance = min([distance, 100])
  if id in deviceMapping:
    config = deviceMapping[id]
    if config[0] == 'note':
      index = config[1]
      noteIndex = int(len(notes) * distance / 100.0)
      sequencer.set_note(index, noteIndex)

sonics.set_update_callback(on_device_update)

while keep_listening:
  sonics.request_next_device_update()
  # print(sonics.registeredDevices)
  time.sleep(0.1)

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

sonics = sa.SonicApi("192.168.1.99", "sonic")
sonics.connect()

deviceMapping = {
  'esp32-sonic-f10f7c': ('note', 0),
  'esp32-sonic-e2c6c4': ('note', 1),
  'esp32-sonic-e29abc': ('note', 2),
  'esp32-sonic-e36270': ('note', 3),
  'esp32-sonic-e37fa4': ('bpm', 0)
}

bpms = [ 30, 60, 120, 240, 360, 480]

def on_device_update(id, distance):
  distance = min([distance, 100])
  if id in deviceMapping:
    config = deviceMapping[id]
    if config[0] == 'note':
      index = config[1]
      noteIndex = int((len(notes)-1) * distance / 100.0)
      sequencer.set_note(index, noteIndex)
    elif config[0] == 'bpm':
      bpmIndex = int((len(bpms)-1) * distance / 100.0)
      sequencer.set_bpm(bpms[bpmIndex])
  else:
    print("No device mapping for " + id)

sonics.set_update_callback(on_device_update)

while keep_listening:
  sonics.request_next_device_update()
  # print(sonics.registeredDevices)
  time.sleep(0.1)

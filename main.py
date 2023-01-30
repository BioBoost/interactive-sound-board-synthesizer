import sequencer as sq
import notes
import time
import signal
import sonic_api as sa

keep_listening = True

def handler(signum, frame):
  global keep_listening

  msg = "Ctrl-c was pressed. Closing the app ..."
  print(msg, end="", flush=True)
  keep_listening = False
  sequencer.stop()
  exit()
 
signal.signal(signal.SIGINT, handler)

sequencer = sq.Sequencer(4)
sequencer.set_bpm(360)
# sequencer.start()

sonics = sa.SonicApi("141.105.126.62", "sonic")
sonics.connect()


# sequencer.set_note(0, 65)
# sequencer.set_note(1, 84)
# sequencer.set_note(2, 34)
# sequencer.set_note(3, 14)

while keep_listening:
  sonics.request_next_device_update()
  print(sonics.registeredDevices)
  time.sleep(0.1)

import sequencer as sq
import time
import signal
import sonic_api as sapi

keep_listening = True
# sequencer = sq.Sequencer(4)
# sequencer.start()

def handler(signum, frame):
    msg = "Ctrl-c was pressed. Closing the app ..."
    print(msg, end="", flush=True)
    keep_listening = False
    # sequencer.stop()
    exit()
 
signal.signal(signal.SIGINT, handler)

# sequencer.set_bpm(360)
# sequencer.set_note(0, 3)
# sequencer.set_note(1, 5)
# sequencer.set_note(1, 7)
# sequencer.set_note(1, 2)

sonicApi = sapi.SonicApi("mqtt.devbit.be", "sonic")
sonicApi.connect()



while keep_listening:
  print("Doing nothing")
  time.sleep(1)
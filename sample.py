import time
from gpiozero import MotionSensor
from signal import pause
from datetime import datetime
import RPi.GPIO as GPIO

pir = MotionSensor(4)

import threading
import queue

q = queue.Queue()

PIN_GPIO = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_GPIO, GPIO.OUT)
DELAY = 30

# TODO: actually turn on/off light
def turn_off(item):
    print(f'turning off light {item}')
    GPIO.output(PIN_GPIO, True)

def turn_on(item):
    print(f'turning on, Finished {item}')
    GPIO.output(PIN_GPIO, False)

def worker():
    last_on = datetime.now()
    while True:
        item = q.get()
        if (item - last_on).seconds > DELAY:
            turn_off(item)
            time.sleep(DELAY)
            turn_on(item)
            last_on = item
        else:
            print('skipping')
        q.task_done()

def on_motion(x):
    q.put(datetime.now())

pir.when_motion = on_motion
pir.when_no_motion = lambda x: print(x,'no motion')

print('starting...')
threading.Thread(target=worker, daemon=True).start()

pause()




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

def turn_off():
    GPIO.output(PIN_GPIO, True)

def turn_on():
    GPIO.output(PIN_GPIO, True)

def worker():
    while True:
        item = q.get()
        # TODO: actually turn on/off light
        if (datetime.now() - item).seconds < 30:
            print(f'turning off light {item}')
            #turn_off()
            time.sleep(20)
            #turn_on()
            print(f'turning on, Finished {item}')
        q.task_done()

def on_motion(x):
    q.put(datetime.now())

pir.when_motion = on_motion
pir.when_no_motion = lambda x: print(x,'no motion')

threading.Thread(target=worker, daemon=True).start()

pause()



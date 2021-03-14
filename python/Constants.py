#!/usr/bin/env python3
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from threading import Thread
from time import sleep, time
from sys import stderr

BLACK = 5
WHITE = 25
STOP = False

btn = Button()

def wait_stop_thread():
    global STOP
    sound = Sound()
    while True:
        btn.wait_for_bump('left')
        STOP = True
        print("STOPPING...", file=stderr)
        sound.beep()
        sleep(1)

stop_th = Thread(target=wait_stop_thread)
stop_th.setDaemon(True)
stop_th.start()




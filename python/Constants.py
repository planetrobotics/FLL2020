#!/usr/bin/env python3
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from threading import Thread
from time import sleep, time
from sys import stderr

# constant values for robot Marty
BLACK = 5
WHITE = 25
STOP = False #STOP variable helps us to stop the robot without stopping the program

btn = Button()

#Stop the robot if left button is pressed
#This stops the robot without stopping the code!
def wait_stop_thread():
    '''Function to set STOP = True if left button is pressed'''
    global STOP
    sound = Sound()
    while True:
        btn.wait_for_bump('left')
        STOP = True
        print("STOPPING...", file=stderr)
        sound.beep()
        sleep(1)

#Stop thread runs as daemon and waits for the left button press
stop_th = Thread(target=wait_stop_thread)
stop_th.setDaemon(True)
stop_th.start()




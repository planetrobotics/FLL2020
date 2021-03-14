#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, MoveSteering
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
#from ev3dev.ev3 import *
#import ev3dev.fonts as fonts
from time import sleep, time
import math
# from BasicFunctions import * 
from ev3dev2.button import Button 
from ev3dev2.sound import Sound
import os
os.system('setfont Lat15-TerminusBold14')
# os.system('setfont Lat15-TerminusBold32x16')

while
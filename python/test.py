#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, MoveSteering
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from time import sleep, time
import math
from BasicFunctions import *

lineFollowPID(degrees =  DistanceToDegree(150), kp = 0.75, ki = 0.01, kd = 20, color = ColorSensor(INPUT_3))

acceleration(degrees = DistanceToDegree(55), finalSpeed=50)
accelerationMoveBackward(degrees=DistanceToDegree(55), finalSpeed=50)


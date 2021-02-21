#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, MoveSteering
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from time import sleep, time
import math
from BasicFunctions import *


acceleration(degrees = DistanceToDegree(55), finalSpeed=80)
GyroTurn(steering=-100, angle=20)
GyroTurn(steering=100, angle=20)
accelerationMoveBackward(degrees=DistanceToDegree(55), finalSpeed=100)

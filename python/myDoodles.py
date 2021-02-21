#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, MoveSteering
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
# from ev3dev.ev3 import *
# import ev3dev.fonts as fonts
from time import sleep, time
import math
from BasicFunctions import *


deg = DistanceToDegree(20)
lineFollow(degrees=deg, GAIN=0.75, color=ColorSensor(INPUT_3))
lineFollowTillIntersection(GAIN=0.75, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))

robot= MoveSteering(OUTPUT_B, OUTPUT_C)
gyro=GyroSensor(INPUT_2)
colorleft = ColorSensor(INPUT_1)
colorright = ColorSensor(INPUT_4)
lmB = LargeMotor(OUTPUT_B)
lmR = LargeMotor(OUTPUT_C)

acceleration(65, 50, 1, 5.4, MoveSteering(OUTPUT_B, OUTPUT_C), LM=lmB)
while colorleft.reflected_light_intensity < 70:
    robot.on_for_degrees(speed=20, steering = 0, degrees = DistanceToDegree(2))
    robot.on_for_degrees(speed=-20, steering = 0, degrees = DistanceToDegree(0.5))
while colorleft.reflected_light_intensity > 10:
    robot.on_for_degrees(speed=20, steering = 0, degrees = DistanceToDegree(2))
    robot.on_for_degrees(speed=-20, steering = 0, degrees = DistanceToDegree(0.5))
while colorleft.reflected_light_intensity < 70:
    robot.on_for_degrees(speed=20, steering = 0, degrees = DistanceToDegree(2))
    robot.on_for_degrees(speed=-20, steering = 0, degrees = DistanceToDegree(0.5))

robot.on_for_degrees(speed=-30, steering=-5, degrees=DistanceToDegree(20))
GyroTurn(50, 90, gyro, robot)
robot.on_for_degrees(speed=-30, steering=0, degrees=DistanceToDegree(90))
GyroTurn(angle=90, steering=100)


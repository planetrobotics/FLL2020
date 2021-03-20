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

robot = MoveSteering(OUTPUT_A, OUTPUT_B)
colorLeft = ColorSensor(INPUT_1)
colorRight = ColorSensor(INPUT_3)
gyro = GyroSensor(INPUT_2)

motorB = LargeMotor(OUTPUT_B)

gyro.reset()

GyroDrift()

show_text("Robot Run 3")

GyroTurn(steering=-50, angle=5)
acceleration(degrees=DistanceToDegree(20), finalSpeed=30)
lineFollowPID(degrees=DistanceToDegree(80), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))
lineFollowPID(degrees=DistanceToDegree(30), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))
accelerationMoveBackward(degrees = DistanceToDegree(5), finalSpeed=50, steering=0)

acceleration(degrees=DistanceToDegree(26), finalSpeed=50, steering=3)

motorB.on_for_seconds(speed=15, seconds=10)

accelerationMoveBackward(degrees = DistanceToDegree(10), finalSpeed=20, steering=0)
GyroTurn(steering=-50, angle=90)
robot.on_for_seconds(steering=0, speed=-10, seconds=2)

#accelerationMoveBackward(degrees = DistanceToDegree(200), finalSpeed=100, steering=1)
acceleration(degrees=DistanceToDegree(26), finalSpeed=50, steering=0)



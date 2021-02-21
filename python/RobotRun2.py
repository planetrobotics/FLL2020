#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, MoveSteering
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from time import sleep, time
import math
from BasicFunctions import *
# from ev3dev.ev3 import *
# import ev3dev.fonts as fonts

robot = MoveSteering(OUTPUT_A, OUTPUT_B)
colorLeft = ColorSensor(INPUT_1)
colorRight = ColorSensor(INPUT_3)
motorA = LargeMotor(OUTPUT_A)


acceleration(degrees=DistanceToDegree(60), finalSpeed=50, steering=2)
while colorLeft.reflected_light_intensity > 10:
    robot.on(steering=2, speed=20)
robot.off()

acceleration(degrees=DistanceToDegree(13), finalSpeed=20, steering=2)

while colorLeft.reflected_light_intensity < WHITE:
    #robot.on_for_degrees(speed=20, steering = 0, degrees = DistanceToDegree(2))
    MoveForwardWhite(distanceInCm=2)
    robot.on_for_degrees(degrees=DistanceToDegree(0.5), steering=2, speed=-10)
robot.off()

counter = 0
while counter < 5:
    robot.on_for_degrees(speed=20, steering = 0, degrees = DistanceToDegree(2))
    robot.on_for_degrees(degrees=DistanceToDegree(0.5), steering=2, speed=-10)
    counter += 1
robot.off()

robot.on_for_degrees(degrees=DistanceToDegree(10), steering=-30, speed=-20)
GyroTurn(steering=-100, angle=40)
acceleration(degrees=DistanceToDegree(10), finalSpeed=20)
GyroTurn(steering=-100, angle=40)

# wall square
robot.on_for_seconds(steering=5, speed=-10, seconds=2)

acceleration(degrees=DistanceToDegree(55), finalSpeed=30, steering=1)

# while colorRight.reflected_light_intensity < 50:
#     robot.on(steering=50, speed=10)
# robot.off()

#lineFollow(degrees=DistanceToDegree(40), GAIN=0.9, color=ColorSensor(INPUT_3))
lineSquare()

GyroTurn(steering=-45, angle=85)

lineFollowRightPID(degrees=DistanceToDegree(25), kp = 1.25, ki = 0.01, kd = 5)
GyroTurn(steering=-40, angle=30)
acceleration(DistanceToDegree(100), finalSpeed=50)

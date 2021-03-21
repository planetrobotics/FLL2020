#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, MoveSteering
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from time import sleep, time
import math
from BasicFunctions import *
import Constants
from sys import stderr

def Robotrun3():
    robot = MoveSteering(OUTPUT_A, OUTPUT_B)
    colorLeft = ColorSensor(INPUT_1)
    colorRight = ColorSensor(INPUT_3)
    motorA = LargeMotor(OUTPUT_A)
    motorD = LargeMotor(OUTPUT_D)
    motorC = LargeMotor(OUTPUT_C)

    motorC.off(brake=True)
    motorD.off(brake=True)

    Constants.STOP = False
    GyroDrift()
    show_text("Robot Run 3")

    GyroTurn(steering=-50, angle=45)

    acceleration(degrees=DistanceToDegree(17), finalSpeed=20)

    lineFollowPID(degrees=DistanceToDegree(20), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))

    GyroTurn(steering=-50, angle=65)
    lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))

    lineFollowPID(degrees=DistanceToDegree(20), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))

    lineFollowPID(degrees=DistanceToDegree(18), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    #lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))

    #accelerationMoveBackward(degrees=DistanceToDegree(5), finalSpeed=20)
    motorC.on_for_seconds(speed=20, seconds=1, brake=True)

    GyroTurn(steering=100, angle=60)
    acceleration(degrees=DistanceToDegree(45), finalSpeed=20)

    motorD.on_for_seconds(speed=-25, seconds=0.5, brake=False)

    accelerationMoveBackward(degrees=DistanceToDegree(10), finalSpeed=30)

    while Constants.STOP == False:
        GyroTurn(steering=100, angle=20)
        GyroTurn(steering=-100, angle=20)


#Robotrun3()


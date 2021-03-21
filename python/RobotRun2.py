#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, MoveSteering
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from time import sleep, time
import math
from BasicFunctions import *

#robot accelerates forward turns left and right then accelerates back to base
def Robotrun2():

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
    show_text("Robot Run 2")

    acceleration(degrees = DistanceToDegree(50), finalSpeed=30)
    accelerationMoveBackward(degrees=DistanceToDegree(50), finalSpeed=100)

    motorC.off(brake=False)
    motorD.off(brake=False)

#Robotrun2()

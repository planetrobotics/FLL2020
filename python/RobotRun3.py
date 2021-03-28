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

#Robot run 3:
# Here we are doing Boccia share, Boccia balls in target area and robot dance
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
    GyroDrift() #check gyro drift at the start of each run
    show_text("Robot Run 3")

    #Turn left and move forward to align with line outside the base
    GyroTurn(steering=-50, angle=45)
    acceleration(degrees=DistanceToDegree(17), finalSpeed=20)

    #Follow the line up to intersection
    lineFollowPID(degrees=DistanceToDegree(20), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))

    #left turn to align with line, then line follow till next intersection
    GyroTurn(steering=-50, angle=65)
    lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))

    #Line follow some more for intersection near Boccia share mission
    lineFollowPID(degrees=DistanceToDegree(20), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))
    lineFollowPID(degrees=DistanceToDegree(18), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    #lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))

    #Move left arm to send Boccia ball accross. Move right arm if we want to use different color
    #accelerationMoveBackward(degrees=DistanceToDegree(5), finalSpeed=20)
    motorC.on_for_seconds(speed=20, seconds=1, brake=True)

    #Turn right and move to Boccia target region
    GyroTurn(steering=100, angle=60)
    acceleration(degrees=DistanceToDegree(45), finalSpeed=20)

    #Drop the Boccia balls in target region
    motorD.on_for_seconds(speed=-25, seconds=0.5, brake=False)

    #Move backward and start robot dance
    accelerationMoveBackward(degrees=DistanceToDegree(10), finalSpeed=30)
    while Constants.STOP == False:
        GyroTurn(steering=100, angle=20)
        GyroTurn(steering=-100, angle=20)


#Robotrun3() #testing, testing


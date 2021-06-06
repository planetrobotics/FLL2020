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
import Constants

def Robotrun4():
    robot = MoveSteering(OUTPUT_A, OUTPUT_B)
    tank = MoveTank(OUTPUT_A, OUTPUT_B)
    colorLeft = ColorSensor(INPUT_1)
    colorRight = ColorSensor(INPUT_3)
    gyro = GyroSensor(INPUT_2)
    motorC = LargeMotor(OUTPUT_C)
    motorD = LargeMotor(OUTPUT_D)
    motorB = LargeMotor(OUTPUT_B)
    motorA = LargeMotor(OUTPUT_A)

    gyro.reset()

    GyroDrift()

    show_text("Robot Run 2")

    #GyroTurn(steering=-50, angle=5)
    acceleration(degrees=DistanceToDegree(30), finalSpeed=30)
    lineFollowPID(degrees=DistanceToDegree(30), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    acceleration(degrees=DistanceToDegree(5), finalSpeed=30)
    accelerationMoveBackward(degrees = DistanceToDegree(7), finalSpeed=50, steering=0)
    motorC.on_for_seconds(speed=15, seconds=1, brake=False)
    GyroTurn(steering=50, angle=20)
    acceleration(degrees=DistanceToDegree(20), finalSpeed=30)
    GyroTurn(steering=-55, angle=20)
    acceleration(degrees=DistanceToDegree(10), finalSpeed=30)

    lineFollowPID(degrees=DistanceToDegree(15), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))
    lineFollowPID(degrees=DistanceToDegree(30), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    gyro.reset()
    lineFollowTillIntersectionPID(kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))
    accelerationMoveBackward(degrees = DistanceToDegree(5), finalSpeed=50, steering=0)
    

    acceleration(degrees=DistanceToDegree(22), finalSpeed=50, steering=3)
    acceleration(degrees=DistanceToDegree(3), finalSpeed=50, steering=0)
    #motorC.on_for_seconds(speed=15, seconds=5)
    if False == Constants.STOP:
        tank.on_for_seconds(left_speed=1.5, right_speed=20, seconds=5.5)
    #motorB.on_for_seconds(speed=15, seconds=10)

    accelerationMoveBackward(degrees = DistanceToDegree(15), finalSpeed=20, steering=0)

    GyroTurn(steering=-50, angle=gyro.angle)
    MoveBackwardBlack(10)
    GyroTurn(steering=-100, angle=75)
    # wall square
    if False == Constants.STOP:
        robot.on_for_seconds(steering=5, speed=-15, seconds=2)

    acceleration(degrees=DistanceToDegree(30), finalSpeed=50, steering=0)
    GyroTurn(steering=100, angle=73)

    motorC.on_for_seconds(speed=-13, seconds=1.5, brake=True)
    #motorC.off(brake=False)
    sleep(0.1)
    motorC.off(brake=True)
    acceleration(degrees=DistanceToDegree(1), finalSpeed=20, steering=0)

    accelerationMoveBackward(degrees = DistanceToDegree(10), finalSpeed=20, steering=0)
    GyroTurn(steering=-100, angle=10)

    if False == Constants.STOP:
        motorC.on_for_seconds(speed=20, seconds=2)
        GyroTurn(steering=-100, angle=65)
    acceleration(degrees=DistanceToDegree(27), finalSpeed=50, steering=0)
    lineSquare()

    GyroTurn(steering=100, angle=10)
    acceleration(degrees=DistanceToDegree(22), finalSpeed=30, steering=0)

    if False == Constants.STOP:
        motorD.on_for_degrees(speed=-20, degrees=150)
        motorD.on_for_seconds(speed=20, seconds=2, brake=False)
        GyroTurn(steering=-100, angle=10)
    accelerationMoveBackward(degrees = DistanceToDegree(20), finalSpeed=20, steering=0)
    lineSquare()

    if False == Constants.STOP:
        GyroTurn(steering=-40, angle=85)
    
    lineFollowRightPID(degrees=DistanceToDegree(30), kp=1.25, ki=0.01, kd=5, color=colorLeft)
    lineFollowTillIntersectionRightPID(kp=1.25, ki=0.01, kd=5, color=colorLeft, color2=colorRight)
    lineFollowRightPID(degrees=DistanceToDegree(39), kp=1.25, ki=0.01, kd=5, color=colorLeft)

    GyroTurn(steering=50, angle=20)
    lineFollowPID(degrees=DistanceToDegree(12), kp=1.25, ki=0.01, kd=5, color=colorLeft)
    lineSquare()

    GyroTurn(steering=100, angle=80)
    motorC.on_for_seconds(speed=-10, seconds=1, brake=False)
    acceleration(degrees=DistanceToDegree(7), finalSpeed=30, steering=0)
    motorC.on_for_seconds(speed=10, seconds=2, brake=True)
    GyroTurn(steering=50, angle=75)

    while Constants.STOP == False:
        GyroTurn(steering=100, angle=20)
        GyroTurn(steering=-70, angle=20)

    return
    if False == Constants.STOP:
        GyroTurn(steering=-50, angle=20)
    acceleration(degrees=DistanceToDegree(100), finalSpeed=100, steering=0)

    motorC.off(brake=False)
    motorD.off(brake=False)

#Robotrun4()

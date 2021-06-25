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

    Constants.STOP = False

    gyro.reset()

    GyroDrift()

    gyro.reset()

    show_text("Robot Run 2")

    motorC.off(brake=True)

    #GyroTurn(steering=-50, angle=5)
    acceleration(degrees=DistanceToDegree(30), finalSpeed=30)
    lineFollowPID(degrees=DistanceToDegree(30), kp=1.3, ki=0.01, kd=15, color=ColorSensor(INPUT_3))
    acceleration(degrees=DistanceToDegree(5), finalSpeed=30)
    accelerationMoveBackward(degrees = DistanceToDegree(7), finalSpeed=50, steering=0)
    motorC.on_for_seconds(speed=15, seconds=1, brake=False)
    GyroTurn(steering=50, angle=20)
    acceleration(degrees=DistanceToDegree(20), finalSpeed=30)
    GyroTurn(steering=-55, angle=22)
    acceleration(degrees=DistanceToDegree(17), finalSpeed=30)
    gyro.mode = "GYRO-ANG"
    while gyro.value() < -10 and False == Constants.STOP:
        motorA.on(speed = 20)
    
    lineFollowPID(degrees=DistanceToDegree(15), kp=1.3, ki=0.01, kd=15, color=ColorSensor(INPUT_3))    
    lineFollowTillIntersectionPID(kp=1.3, ki=0.01, kd=15, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))
    lineFollowPID(degrees=DistanceToDegree(10), kp=1.3, ki=0.01, kd=15, color=ColorSensor(INPUT_3))
    lineFollowTillIntersectionPID(kp=1.3, ki=0.01, kd=15, color=ColorSensor(INPUT_3), color2=ColorSensor(INPUT_1))

    if gyro.angle > 2 and False == Constants.STOP:
        GyroTurn(steering=-50, angle=gyro.angle)
    elif gyro.angle < -2 and False == Constants.STOP:
        ang = -1 * gyro.angle
        GyroTurn(steering=50, angle=ang)
    accelerationMoveBackward(degrees = DistanceToDegree(5), finalSpeed=50, steering=0)

    acceleration(degrees=DistanceToDegree(12), finalSpeed=50, steering=2.5)

    motorC.on_for_degrees(speed=-25, degrees=150, brake=True)
    motorD.on_for_degrees(speed=-25, degrees=150, brake=True)

    acceleration(degrees=DistanceToDegree(12), finalSpeed=45, steering=4)
    #acceleration(degrees=DistanceToDegree(12), finalSpeed=45, steering=5)

    #Moving treadmill
    if False == Constants.STOP:
        tank.on_for_seconds(left_speed=1, right_speed=20, seconds=5.5)
    #motorB.on_for_seconds(speed=15, seconds=10)

    motorC.on_for_seconds(speed=25, seconds=2, brake=False)
    motorD.on_for_seconds(speed=25, seconds=2, brake=False)

    accelerationMoveBackward(degrees = DistanceToDegree(5), finalSpeed=20, steering=0)
    while colorLeft.reflected_light_intensity < Constants.WHITE:
        robot.on(steering=0, speed=-20)
    accelerationMoveBackward(degrees = DistanceToDegree(2), finalSpeed=10, steering=0)

    GyroTurn(steering=-50, angle=gyro.angle)
    MoveBackwardBlack(10)

    ang = -1 * (90 + gyro.angle)
    GyroTurn(steering=-100, angle=ang)

    # wall square
    if False == Constants.STOP:
        robot.on_for_seconds(steering=5, speed=-10, seconds=2.7, brake=False)

    # moving towards row machine    
    acceleration(degrees=DistanceToDegree(30), finalSpeed=50, steering=0)
    
    GyroTurn(steering=100, angle=68)
    #acceleration(degrees=DistanceToDegree(1), finalSpeed=20, steering=0)

    motorC.on_for_seconds(speed=-13, seconds=1.5, brake=True)
    #motorC.off(brake=False)
    sleep(0.1)
    motorC.off(brake=True)
    acceleration(degrees=DistanceToDegree(1), finalSpeed=20, steering=0)

    accelerationMoveBackward(degrees = DistanceToDegree(10), finalSpeed=20, steering=0)
    GyroTurn(steering=-100, angle=10)

    #DOING Row Machine
    if False == Constants.STOP:
        motorC.on_for_seconds(speed=20, seconds=2)
        ang = 90 + gyro.angle
        GyroTurn(steering=-100, angle=ang)
    
    acceleration(degrees=DistanceToDegree(28), finalSpeed=50, steering=0)
    lineSquare()

    #Moving towards weight machine
    GyroTurn(steering=100, angle=3)
    acceleration(degrees=DistanceToDegree(22), finalSpeed=30, steering=0)

    if False == Constants.STOP:
        motorD.on_for_degrees(speed=-20, degrees=160)
        motorD.on_for_seconds(speed=20, seconds=2, brake=True)
        #GyroTurn(steering=-100, angle=7)
    accelerationMoveBackward(degrees = DistanceToDegree(20), finalSpeed=20, steering=0)
    lineSquare()

    if False == Constants.STOP:
        GyroTurn(steering=-40, angle=85)
    
    lineFollowRightPID(degrees=DistanceToDegree(30), kp=1.3, ki=0.01, kd=15, color=colorLeft)
    lineFollowTillIntersectionRightPID(kp=1.3, ki=0.01, kd=15, color=colorLeft, color2=colorRight)
    lineFollowRightPID(degrees=DistanceToDegree(33), kp=1.3, ki=0.01, kd=15, color=colorLeft)

    if False == Constants.STOP:
        GyroTurn(steering=50, angle=20)
    acceleration(degrees=DistanceToDegree(12), finalSpeed=30, steering=2)
    lineSquare()

    if False == Constants.STOP:
        GyroTurn(steering=100, angle=75)
    motorC.on_for_seconds(speed=-10, seconds=1, brake=False)
    acceleration(degrees=DistanceToDegree(6.5), finalSpeed=30, steering=0)
    motorC.on_for_seconds(speed=10, seconds=2, brake=True)

    if False == Constants.STOP:
        GyroTurn(steering=50, angle=75)
    acceleration(degrees=DistanceToDegree(5), finalSpeed=30, steering=0)

    while Constants.STOP == False:
        acceleration(degrees=DistanceToDegree(3), finalSpeed=31, steering=0)
        accelerationMoveBackward(degrees = DistanceToDegree(3), finalSpeed=30, steering=0)

    motorC.off(brake=False)
    motorD.off(brake=False)

#Robotrun4()
 
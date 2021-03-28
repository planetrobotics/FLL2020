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
# from ev3dev.ev3 import *
# import ev3dev.fonts as fonts

#This is our first robot run
# In this run, we do step counter up to yellow
# Then we align towards the pullup bar and pass under pullup bar
# Then robot drops few Boccia balls in target area
# Then robot follows the line towards Bench
# Then robot lifts up the basketball and flattens the bench before returning home
def Robotrun1():
    robot = MoveSteering(OUTPUT_A, OUTPUT_B)
    colorLeft = ColorSensor(INPUT_1)
    colorRight = ColorSensor(INPUT_3)
    motorA = LargeMotor(OUTPUT_A)
    motorD = LargeMotor(OUTPUT_D)
    motorC = LargeMotor(OUTPUT_C)

    motorC.off(brake=True)
    motorD.off(brake=True)
    Constants.STOP = False

    GyroDrift() #check gyro drift at the start of every robot run
    show_text("Robot Run 1")

    #Wall square and move forward till first line intersection
    acceleration(degrees=DistanceToDegree(70), finalSpeed=50, steering=2)
    while colorLeft.reflected_light_intensity > 10 and False == Constants.STOP:
        robot.on(steering=2, speed=20)
    robot.off()

    #Move forward towards step counter
    acceleration(degrees=DistanceToDegree(13), finalSpeed=20, steering=2)

    #Move back and forth until the left sensor encounters white
    while colorLeft.reflected_light_intensity < Constants.WHITE and False == Constants.STOP:
        #robot.on_for_degrees(speed=20, steering = 0, degrees = DistanceToDegree(2))
        #print("RobotRun2 stop=" + str(Constants.STOP), file=stderr)
        MoveForwardWhite(distanceInCm=2)
        robot.on_for_degrees(degrees=DistanceToDegree(0.75), steering=2, speed=-10)
    robot.off()

    #Move back and forth until the left sensor encounters black
    while colorLeft.reflected_light_intensity > Constants.BLACK and False == Constants.STOP:
        #robot.on_for_degrees(speed=20, steering = 0, degrees = DistanceToDegree(2))
        #print("RobotRun2 stop=" + str(Constants.STOP), file=stderr)
        MoveForwardBlack(distanceInCm=2)
        robot.on_for_degrees(degrees=DistanceToDegree(0.75), steering=2, speed=-10)
    robot.off()

    #counter = 0
    #while counter < 5 and False == Constants.STOP:
    #    robot.on_for_degrees(speed=20, steering = 0, degrees = DistanceToDegree(2))
    #    robot.on_for_degrees(degrees=DistanceToDegree(0.75), steering=2, speed=-10)
    #    counter += 1
    #robot.off()

    #Series of movements to turn left after step counter mission and then wall square to align with pullup bar
    accelerationMoveBackward(degrees=DistanceToDegree(10), steering=-15, finalSpeed=-20)
    GyroTurn(steering=-100, angle=40)
    acceleration(degrees=DistanceToDegree(10.5), finalSpeed=20)
    while colorRight.reflected_light_intensity < Constants.WHITE and False == Constants.STOP:
        robot.on(speed=10, steering=0)
    robot.off()
    acceleration(degrees=DistanceToDegree(2), finalSpeed=20)
    GyroTurn(steering=-100, angle=50)

    # wall square
    robot.on_for_seconds(steering=5, speed=-10, seconds=2)

    #Go under pullup bar and then line square
    acceleration(degrees=DistanceToDegree(55), finalSpeed=30)
    #lineFollowPID(degrees=DistanceToDegree(40), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_3))
    lineSquare()

    #doing bociaa mission
    acceleration(degrees=DistanceToDegree(22), finalSpeed=30, steering=0.5)
    motorD.on_for_seconds(speed=-25, seconds=0.5, brake=False)
    #motorD.on_for_degrees(speed=30, degrees=15, brake=True)

    #Go backward after Boccia and then line square again
    accelerationMoveBackward(degrees=DistanceToDegree(20), finalSpeed=30)
    lineSquare()

    #Turn towards slide and line follow until next intersection. Slide person will be knocked out by Bobby attachment
    GyroTurn(steering=-45, angle=85)
    lineFollowPID(degrees=DistanceToDegree(18), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_1))
    acceleration(degrees=DistanceToDegree(5), finalSpeed=20)

    #Turn towards next line and follow the line, then square on the line near intersection
    GyroTurn(steering=50, angle=20)
    #motorD.on_for_degrees(speed=30, degrees=15, brake=True)
    lineFollowPID(degrees=DistanceToDegree(12), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_1))
    lineSquare()
    acceleration(degrees=DistanceToDegree(5), finalSpeed=20, steering=5)
    lineFollowPID(degrees=DistanceToDegree(30), kp=1.25, ki=0.01, kd=5, color=ColorSensor(INPUT_1))

    #Turn towards basketball
    GyroTurn(steering=100, angle=40)

    #Lift the basket using right side arm attachment
    motorD.on_for_seconds(speed=20, seconds=0.5, brake=True)
    motorD.on_for_seconds(speed=-25, seconds=0.5, brake=False)

    #Turn towards bench and flatten the bench using left side arm attachement
    GyroTurn(steering=-100, angle=90)
    motorC.on_for_degrees(speed=-10, degrees=30, brake=True)

    #Turn towards home and move at 100 speed
    GyroTurn(steering=100, angle=50)
    acceleration(degrees=DistanceToDegree(70), finalSpeed=100, steering=0)

    motorC.off(brake=False)
    motorD.off(brake=False)

    
#Robotrun1() #testing, testing

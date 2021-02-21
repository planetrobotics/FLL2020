#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, MoveSteering
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
# from ev3dev.ev3 import *
# import ev3dev.fonts as fonts
from time import sleep, time
import math

BLACK = 5
WHITE = 25

def stopRobot():
    robot = MoveSteering(OUTPUT_A, OUTPUT_B)
    robot.off()

def DistanceToDegree(distanceInCm, diameter = 8.16):
    """Function to calculate degrees for given distance in centimeters
        Input distanceInCm = distance to travel in centimeters
        Input diameter = wheel diameter in centimeters, 8.16 is default
    """
    return distanceInCm * (360 / (math.pi * diameter))

def GyroTurn(steering, angle, gyro = GyroSensor(INPUT_2), steer_pair = MoveSteering(OUTPUT_A, OUTPUT_B)):
    """Function to do precise turns using gyro sensor
        Input steering and angle to turn. Angle must be a +ve value
        gyro: gyro sensor if different than default
        steer_pair: MoveSteering if different than default
    """
    gyro.mode='GYRO-ANG'
    steer_pair.on(steering = steering, speed = 15)
    gyro.wait_until_angle_changed_by(abs(angle))
    steer_pair.off()

def lineSquare(leftMotor = LargeMotor(OUTPUT_A), 
            rightMotor = LargeMotor(OUTPUT_B), 
            robot = MoveSteering(OUTPUT_A, OUTPUT_B), 
            colorLeft = ColorSensor(INPUT_1), colorRight = ColorSensor(INPUT_3)):
    '''Function to square the robot precisely on a black line'''

    colorLeft.mode = 'COL-REFLECT'
    colorRight.mode = 'COL-REFLECT'
    
    counter = 0
    while counter < 2:
        while colorLeft.reflected_light_intensity >= BLACK and colorRight.reflected_light_intensity >= BLACK:
            robot.on(steering = 0, speed = 10)
        robot.off()

        while colorLeft.reflected_light_intensity <= WHITE:
            leftMotor.on(speed=-10)
        leftMotor.off()

        while colorRight.reflected_light_intensity <= WHITE:
            rightMotor.on(speed=-10)
        rightMotor.off()

        while colorLeft.reflected_light_intensity >= BLACK:
            leftMotor.on(speed=10)
        leftMotor.off()

        while colorRight.reflected_light_intensity >= BLACK:
            rightMotor.on(speed=10)
        rightMotor.off()

        counter += 1

def PIDMath(error, lasterror, kp = 1, ki = 0, kd = 0):
    Proportional = error * kp
    Integral = (error + lasterror) * ki
    Derivative = (error - lasterror) * kd
    PID = Proportional + Integral + Derivative
    return PID

def lineFollowTillIntersectionPID(kp = 1.0, ki = 0, kd = 0, color = ColorSensor(INPUT_1), color2 = ColorSensor(INPUT_3), 
                            robot = MoveSteering(OUTPUT_A, OUTPUT_B)):
    """Function to follow a line till it encounters intersection"""
    
    color.mode = 'COL-REFLECT'
    color2.mode = 'COL-REFLECT'
    lasterror = 0
    while color2.reflected_light_intensity <= WHITE:
        error = color.reflected_light_intensity - ((WHITE + BLACK)/2)  # colorLeft.reflected_light_intensity - colorRight.reflected_light_intensity
        # correction = error * GAIN  # correction = PID(error, lasterror, kp, ki, kd)
        correction = PIDMath(error=error, lasterror = lasterror, kp=kp, ki=ki, kd=kd)
        if correction > 100: correction = 100
        if correction < -100: correction = -100
        robot.on(speed = 20, steering = correction)
        lasterror = error
    robot.off()

def lineFollowPID(degrees, kp = 1.0, ki = 0, kd = 0, color = ColorSensor(INPUT_1), 
                robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    """Function to follow line using color sensor on right side of line"""

    color.mode = 'COL-REFLECT'
    motorA.reset()
    motorA.position = 0

    lasterror = 0
    while motorA.position < degrees:
        error = color.reflected_light_intensity - ((WHITE + BLACK)/2)  # colorLeft.reflected_light_intensity - colorRight.reflected_light_intensity
        #correction = error * GAIN  # correction = PID(error, lasterror, kp, ki, kd)
        correction = PIDMath(error=error, lasterror = lasterror, kp=kp, ki=ki, kd=kd)
        if correction > 100: correction = 100
        if correction < -100: correction = -100
        robot.on(steering = correction, speed = 20)
        lasterror = error
    robot.off()

def lineFollowRightPID(degrees, kp = 1.0, ki = 0, kd = 0, color = ColorSensor(INPUT_1), 
                    robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    """Function to follow line using color sensor on right side of line"""

    color.mode = 'COL-REFLECT'
    motorA.reset()
    motorA.position = 0

    lasterror = 0
    while motorA.position < degrees:
        error = ((WHITE + BLACK)/2) - color.reflected_light_intensity  # colorLeft.reflected_light_intensity - colorRight.reflected_light_intensity
        #correction = error * GAIN  # correction = PID(error, lasterror, kp, ki, kd)
        correction = PIDMath(error=error, lasterror = lasterror, kp=kp, ki=ki, kd=kd)
        if correction > 100: correction = 100
        if correction < -100: correction = -100
        robot.on(steering = correction, speed = 20)
        lasterror = error
    robot.off()


def acceleration(degrees, finalSpeed, steering = 0, robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    """Function to accelerate the robot and drive a specific distance"""

    motorA.reset()
    motorA.position = 0
    accelerateDegree = degrees * 0.8
    # declerationDegree = degrees * 0.2'
    speed = 0
    while motorA.position < degrees:
        if motorA.position < accelerateDegree:
            if speed < finalSpeed:
                speed += 5
                robot.on(steering = steering, speed = speed)
                sleep(0.1)
            else:
                robot.on(steering = steering, speed = finalSpeed)
                sleep(0.01)
        else:
            if speed > 10:
                speed -= 5
                robot.on(steering = steering, speed = speed)
                sleep(0.05)
            else:
                robot.on(steering = steering, speed = speed)
                sleep(0.01)
    
    robot.off()



def accelerationMoveBackward(degrees, finalSpeed, steering = 0, robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    motorA.reset()
    motorA.position = 0

    lowestSpeed = -1 * abs(finalSpeed)
    speed = 0
    while abs(motorA.position) < degrees:
        if speed > lowestSpeed:
            speed -= 5
            robot.on(steering = steering, speed = speed)
            sleep(0.1)
        else:
            robot.on(steering = steering, speed = lowestSpeed)
            sleep(0.01)
    
    robot.off()


def MoveForwardWhite(distanceInCm, colorLeft = ColorSensor(INPUT_1), robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    deg = DistanceToDegree(distanceInCm)
    motorA.reset()
    motorA.position = 0
    while colorLeft.reflected_light_intensity < WHITE and motorA.position < deg:
        robot.on(speed=20, steering = 0)
    robot.off()

def MoveForwardBlack(distanceInCm, colorLeft = ColorSensor(INPUT_1), robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    deg = DistanceToDegree(distanceInCm)
    motorA.reset()
    motorA.position = 0
    while colorLeft.reflected_light_intensity > BLACK and motorA.position < deg:
        robot.on(speed=20, steering = 0)
    robot.off()




#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MoveTank, MoveSteering
from ev3dev2.motor import LargeMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.display import Display
from textwrap import wrap
from threading import Thread
import Constants
# from ev3dev.ev3 import *
# import ev3dev.fonts as fonts
from time import sleep, time
import math
from sys import stderr

# Function to stop the robot during testing on ssh terminal
def stopRobot():
    robot = MoveSteering(OUTPUT_A, OUTPUT_B)
    robot.off()

#############################################################################################################

def DistanceToDegree(distanceInCm, diameter = 8.16):
    """Function to calculate degrees for given distance in centimeters
        Input distanceInCm = distance to travel in centimeters
        Input diameter = wheel diameter in centimeters, 8.16 is default
    """
    return distanceInCm * (360 / (math.pi * diameter)) 

#############################################################################################################

def GyroDrift(gyro=GyroSensor(INPUT_2)):
    '''
    Checking if the Gyro sensor's output is drifing and moving when the actual sensor is not. 
    we need to do this becuase if the sensor is drifting then our GyroTurn's will not work correctly
    '''
    sound = Sound() #Creating sound Shortcut
    gyro.mode = 'GYRO-RATE' #setting gyro mode
    while math.fabs(gyro.rate) > 0: #while gyro is drifting loop, if it is not drifting then the loop will not take place
        show_text("Gyro drift rate: " + str(gyro.rate)) #Showing the rate of how much gyro is drifting
        sound.beep() # Beep to indicate that it is displaying current value
        sleep(0.5) #waiting for value to change
    gyro.mode='GYRO-ANG' #reseting gyro mode for our use in other functions

#############################################################################################################

def GyroTurn(steering, angle, gyro = GyroSensor(INPUT_2), steer_pair = MoveSteering(OUTPUT_A, OUTPUT_B)):
    """Function to do precise turns using gyro sensor
        Input steering and angle to turn. Angle must be a +ve value
        gyro: gyro sensor if different than default
        steer_pair: MoveSteering if different than default
    """

    if True == Constants.STOP: return #
    gyro.mode='GYRO-ANG' #setting gyro value mode
    steer_pair.on(steering = steering, speed = 15) #starting to turn using MoveSteering. If steering equals 50 then it will do a pivot turn, if it is 100 then it will do a spin turn
    gyro.wait_until_angle_changed_by(abs(angle)) #keeps turning until the correct angle is reached
    steer_pair.off() #stopping the turning after target angle is reached

#############################################################################################################

def MoveLeftMotor(leftMotor = LargeMotor(OUTPUT_A), colorLeft = ColorSensor(INPUT_1)): # Function for moving the left motor for our linesquare
    while colorLeft.reflected_light_intensity > Constants.BLACK and False == Constants.STOP: #while loop for moving until it reaches the black line
        leftMotor.on(speed=10) #moving until it reaches the black line
    leftMotor.off() #Turning off motor because it reached it's goal


def MoveRightMotor(rightMotor = LargeMotor(OUTPUT_B), colorRight = ColorSensor(INPUT_3)): #Function for moving the right motor for our linesquare
    while colorRight.reflected_light_intensity > Constants.BLACK and False == Constants.STOP: #while loop for moving until it reaches the black line
        rightMotor.on(speed=10) #moving until it reaches the black line
    rightMotor.off() #Turning off motor because it reached it's goal

def lineSquare(leftMotor = LargeMotor(OUTPUT_A), 
            rightMotor = LargeMotor(OUTPUT_B), 
            robot = MoveSteering(OUTPUT_A, OUTPUT_B), 
            colorLeft = ColorSensor(INPUT_1), colorRight = ColorSensor(INPUT_3)): # look below for what this is doing
    '''Function to square the robot precisely on a black line'''
    if True == Constants.STOP: return
    colorLeft.mode = 'COL-REFLECT' #setting colorsenso mode
    colorRight.mode = 'COL-REFLECT' #setting colorsensor mode
    
    counter = 0 # setting that we've linesquared 0 times so far
    while counter < 2 and False == Constants.STOP: # linesquare 2 times
        left = Thread(target=MoveLeftMotor)
        right = Thread(target=MoveRightMotor) # Linesquare left and right motor at the same time using thread 
        left.start() #starting the Thread
        right.start() # starting the Thread
        left.join() #join so we wait for this thread to finish
        right.join() #join so we wait for this thread to finish
        accelerationMoveBackward(steering=0, finalSpeed=20, degrees=DistanceToDegree(1)) # move backward so we can do it again for extra precision
        counter += 1

#############################################################################################################

def PIDMath(error, lasterror, kp = 1, ki = 0, kd = 0): # PID math function that we use for PID linefollower
    '''PID math function that we use for PID linefollower'''
    Proportional = error * kp #Proportional value
    Integral = (error + lasterror) * ki #Integeral math
    Derivative = (error - lasterror) * kd #Derivative Math
    PID = Proportional + Integral + Derivative #Final PID value calculation
    return PID # return the final value

#############################################################################################################

def lineFollowTillIntersectionPID(kp = 1.0, ki = 0, kd = 0, color = ColorSensor(INPUT_1), color2 = ColorSensor(INPUT_3), 
                            robot = MoveSteering(OUTPUT_A, OUTPUT_B)):
    """Function to follow a line till it encounters intersection""" # *an intersection is a line that is going through the line that the robot is following
    
    color.mode = 'COL-REFLECT' #setting color mode
    color2.mode = 'COL-REFLECT' #setting color mode
    lasterror = 0 
    while color2.reflected_light_intensity <= Constants.WHITE and False == Constants.STOP:
        error = color.reflected_light_intensity - ((Constants.WHITE + Constants.BLACK)/2)  # colorLeft.reflected_light_intensity - colorRight.reflected_light_intensity
        # correction = error * GAIN  # correction = PID(error, lasterror, kp, ki, kd)
        correction = PIDMath(error=error, lasterror = lasterror, kp=kp, ki=ki, kd=kd)
        if correction > 100: correction = 100
        if correction < -100: correction = -100
        robot.on(speed = 20, steering = correction)
        lasterror = error
    robot.off()

#############################################################################################################
def lineFollowPID(degrees, kp = 1.0, ki = 0, kd = 0, color = ColorSensor(INPUT_1), 
                robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    """Function to follow line using color sensor on right side of line"""

    color.mode = 'COL-REFLECT'
    motorA.reset() # Reseting motor degrees
    motorA.position = 0 # Same thing

    lasterror = 0
    while motorA.position < degrees and False == Constants.STOP:
        error = color.reflected_light_intensity - ((Constants.WHITE + Constants.BLACK)/2)  # colorLeft.reflected_light_intensity - colorRight.reflected_light_intensity
        #correction = error * GAIN  # correction = PID(error, lasterror, kp, ki, kd)
        correction = PIDMath(error=error, lasterror = lasterror, kp=kp, ki=ki, kd=kd)
        if correction > 100: correction = 100
        if correction < -100: correction = -100
        robot.on(steering = correction, speed = 20)
        lasterror = error
    robot.off()

#############################################################################################################

def lineFollowRightPID(degrees, kp = 1.0, ki = 0, kd = 0, color = ColorSensor(INPUT_1), 
                    robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    """Function to follow line using color sensor on right side of line"""

    color.mode = 'COL-REFLECT'
    motorA.reset()
    motorA.position = 0

    lasterror = 0
    while motorA.position < degrees and False == Constants.STOP:
        error = ((Constants.WHITE + Constants.BLACK)/2) - color.reflected_light_intensity  # colorLeft.reflected_light_intensity - colorRight.reflected_light_intensity
        #correction = error * GAIN  # correction = PID(error, lasterror, kp, ki, kd)
        correction = PIDMath(error=error, lasterror = lasterror, kp=kp, ki=ki, kd=kd)
        if correction > 100: correction = 100
        if correction < -100: correction = -100
        robot.on(steering = correction, speed = 20)
        lasterror = error
    robot.off()

#############################################################################################################

def acceleration(degrees, finalSpeed, steering = 0, robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)): # Function to accelerate while moving so the robot can get traction before moving fast
    """Function to accelerate the robot and drive a specific distance"""

    motorA.reset() #reseting how many degrees the robot has moved
    motorA.position = 0 # setting how many degrees the robot has moved

    accelerateDegree = degrees * 0.8
    # declerationDegree = degrees * 0.2'
    speed = 0 #starting speed
    while motorA.position < degrees and False == Constants.STOP: #while the robot hasen't moved the target amount of degree's(distance)
        if motorA.position < accelerateDegree and False == Constants.STOP: 
            if speed < finalSpeed: # while the robot hasen't accelerated to the target speed
                speed += 5 #speed up
                robot.on(steering = steering, speed = speed) # Start Moving
                sleep(0.1) #wait so that it doesn't accelerate immidiatly
            else:
                robot.on(steering = steering, speed = finalSpeed)# otherwise just keep moving
                sleep(0.01)
        elif False == Constants.STOP:
            if speed > 10:
                speed -= 5
                robot.on(steering = steering, speed = speed)
                sleep(0.05)
            else:
                robot.on(steering = steering, speed = speed)
                sleep(0.01)
    
    robot.off() # Stop Moving

#############################################################################################################

def accelerationMoveBackward(degrees, finalSpeed, steering = 0, robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    motorA.reset()
    motorA.position = 0

    lowestSpeed = -1 * abs(finalSpeed)
    speed = 0
    while abs(motorA.position) < degrees and False == Constants.STOP:
        if speed > lowestSpeed and False == Constants.STOP:
            speed -= 5
            robot.on(steering = steering, speed = speed)
            sleep(0.1)
        elif False == Constants.STOP:
            robot.on(steering = steering, speed = lowestSpeed)
            sleep(0.01)
    
    robot.off()

#############################################################################################################
def MoveForwardWhite(distanceInCm, colorLeft = ColorSensor(INPUT_1), robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    '''Function to move forward until we see white. 
    This is used for step counter mission'''

    deg = DistanceToDegree(distanceInCm)
    motorA.reset()
    motorA.position = 0
    while colorLeft.reflected_light_intensity < Constants.WHITE and motorA.position < deg and False == Constants.STOP:
        #print("stop=" + str(Constants.STOP), file=stderr)
        robot.on(speed=25, steering = 0)
    robot.off()

#############################################################################################################
def MoveForwardBlack(distanceInCm, colorLeft = ColorSensor(INPUT_1), robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    '''Function to move forward until we see black. 
    This is used for step counter mission'''
    deg = DistanceToDegree(distanceInCm)
    motorA.reset()
    motorA.position = 0
    while colorLeft.reflected_light_intensity > Constants.BLACK and motorA.position < deg and False == Constants.STOP:
        #print("stop=" + str(Constants.STOP), file=stderr)
        robot.on(speed=25, steering = 0)
    robot.off()

############################################################################################################
def MoveBackwardBlack(distanceInCm, colorLeft = ColorSensor(INPUT_1), robot = MoveSteering(OUTPUT_A, OUTPUT_B), motorA = LargeMotor(OUTPUT_A)):
    '''Function to move forward until we see black. 
    This is used for step counter mission'''
    deg = DistanceToDegree(distanceInCm)
    motorA.reset()
    motorA.position = 0
    while colorLeft.reflected_light_intensity > Constants.BLACK and motorA.position < deg and False == Constants.STOP:
        #print("stop=" + str(Constants.STOP), file=stderr)
        robot.on(speed=-25, steering = 0)
    robot.off()

#############################################################################################################
#The show_text code is copied from ev3python.com
def show_text(string, font_name='courB24', font_width=15, font_height=24): # A function to show text on the robot's screen 
    '''Function to show a text on EV3 screen.
    This code is copied from ev3python.com'''
    lcd = Display() # Defining screen
    lcd.clear() # Clearing the screen so there isnt already text
    strings = wrap(string, width=int(180/font_width)) #
    for i in range(len(strings)):
        x_val = 89-font_width/2*len(strings[i])
        y_val = 63-(font_height+1)*(len(strings)/2-i)
        lcd.text_pixels(strings[i], False, x_val, y_val, font=font_name)
    lcd.update()



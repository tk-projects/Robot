#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:39:56 2020

@author: pi
"""
import pandas as pd
from adafruit_servokit import ServoKit
import adafruit_motor.servo

import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

kit = ServoKit(channels=16)
pca.frequency=50

#Pin IDs
vl1=0; vl2=1; vr1=2; vr2=3; hl1=4; hl2=5; hr1=6; hr2=7; hg1=8
pinId=[vl1, vl2 ,vr1, vr2, hl1, hl2, hr1, hr2, hg1];


def LoadCalibration(path):
    CalStrArr=open(path).readlines()
    CalDict={}
    
    for i in range(0,len(CalStrArr)):
        CalStrRow=CalStrArr[i].split('=')
                
        # Header
        CalibratableName=CalStrRow[0]
        
        # Values
        try:
            list(map(float,CalStrRow[1].rstrip('\n').split(',')))
            CalRow= list(map(float,CalStrRow[1].rstrip('\n').split(',')))
            CalDict.update({CalibratableName:CalRow});
            continue

        except ValueError:
            CalRow=list(map(str,CalStrRow[1].rstrip('\n').split(',')))
            CalDict.update({CalibratableName:CalRow});
            continue
        
    #Create Dataframe    
    Cal=pd.DataFrame(CalDict)
    
    # Set Calibration  
    for i in range(0,len(Cal)):
        Servo.id(i).calibrate(Cal)

    print("\nSet the following calibration: \n\n %s " % (Cal))
    return Cal

    
class ServoClass(object):
    def __init__(self):
        self._id=None
        self.angleVal=None
        
    def id(self, id):
        self._id=int(id)
        return self
    
    @property
    def Angle(self):       
        angleVal=kit.servo[self._id].angle
        return angleVal
        
    @Angle.setter
    def Angle(self, val):
        
        angleOffset=Cal['Angle_Offset'][self._id]
        angleMax=Cal['Angle_max'][self._id]
        angleMin=Cal['Angle_min'][self._id]
        angleFac=Cal['Angle_Factor'][self._id]
        
        val=int(val*angleFac)+int(angleOffset)
        
        if val>angleMax:
            val=angleMax
        if val<angleMin:
            val=angleMin
        
        kit.servo[self._id].angle=val
        print(val)
        print(angleOffset)
        val=val+angleOffset
        #print(val)
        return val
    
    def calibrate(self,Cal):
        angleRange=Cal['Angle_Range'][self._id];
        pwm_min=Cal['PWM_min'][self._id];
        pwm_max=Cal['PWM_max'][self._id];
        
        kit.servo[self._id].actuation_range = angleRange;
        kit.servo[self._id].set_pulse_width_range(pwm_min, pwm_max);
        
    
        
Servo=ServoClass()
Cal=LoadCalibration('/home/pi/Robot/RobotSW/Calibration/ServoCalibration.txt')
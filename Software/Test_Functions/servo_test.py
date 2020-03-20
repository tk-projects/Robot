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

idxServo=0

kit = ServoKit(channels=16)
pca.frequency=50
#servo=adafruit_motor.servo.Servo(0)


#Pin IDs
vl1=0; vl2=1; vr1=2; vr2=3; hl1=4; hl2=5; hr1=6; hr2=7; hg1=8
pinId=[vl1, vl2 ,vr1, vr2, hl1, hl2, hr1, hr2, hg1];

## Calibration
#Servo ID
ID=[0, 1, 2, 3, 4, 5, 6, 7, 8]
ServoPos=['vl1','vl2','vr1','vr2','hl1','hl2','hr1','hr2','hg1'];
pwmMaxArr=[2950, 2791, 2835, 2735, 2850, 2000, 2000, 2000, 2000];
pwmMinArr=[371, 371 , 371 ,371 ,341 ,1000 ,1000 ,1000 ,1000];
angleOffsetArr=[0,0,0,0,0,0,0,0,0];
angleMaxArr=[0,0,0,0,0,0,0,0,0];
angleMinArr=[0,0,0,0,0,0,0,0,0];
angleRangeArr=[180, 180, 180, 180, 180, 180, 180, 180, 180]

Cal=pd.DataFrame({'Servo_Position':ServoPos,
                  'Pin_ID':pinId,
                  'PWM_max':pwmMaxArr,
                  'PWM_min':pwmMinArr,
                  'Angle_Offset':angleOffsetArr,
                  'Angle_max':angleMaxArr,
                  'Angle_min':angleMinArr,
                  'Angle_Range':angleRangeArr})

def LoadCalibration(path):
    CalStrArr=open(path).readlines()
    CalDict={}
    for i in CalStrArr:
        CalStrRow=i.split('=')
        
        # Header
        CalibratableName=CalStrRow[0]
        
        # Values
        try:
            CalRow= list(map(float,CalStrRow[1].split(',')))
        
        except:
            CalRow=list(map(str,CalStrRow[1].split(',')))
        
        CalDict.update({CalibratableName:CalRow});
        Cal=pd.DataFrame(CalDict)
    return Cal
        #df=pd.DataFrame({CalibratableName:CalRow})
    
    #for i in range(0:len(Cal['Pin_ID'])):
        #Servo.id(i).calibrate()  


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
        
        val=val+angleOffset
        
        if val>angleMax:
            val=angleMax
        if val<angleMin:
            val=angleMin
        
        kit.servo[self._id].angle=val+angleOffset
        return val
    
    def calibrate(self):
        angleRange=Cal['Angle_Range'][self._id];
        pwm_min=Cal['PWM_min'][self._id];
        pwm_max=Cal['PWM_max'][self._id];
        
        kit.servo[self._id].actuation_range = angleRange;
        kit.servo[self._id].set_pulse_width_range(pwm_min, pwm_max);
        
    
        
Servo=ServoClass()

#servo.id(42).angle(2)
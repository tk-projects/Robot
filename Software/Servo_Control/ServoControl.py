#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 13:51:01 2020

@author: pi
"""

import pandas as pd
from adafruit_servokit import ServoKit
import adafruit_motor.servo
import numpy as np

import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

kit = ServoKit(channels=16)
pca.frequency=50

# Load Constants etc.

# Pin IDs
vl1=0; vl2=1; vr1=2; vr2=3; hl1=4; hl2=5; hr1=6; hr2=7; hg1=8
pinId=[vl1, vl2 ,vr1, vr2, hl1, hl2, hr1, hr2, hg1];


class ServoClass(object):
    def __init__(self):
        self._id=None
        self.angleVal=None
        self.alpha = None
        self.beta = None
        
    def id(self, id):
        self._id=int(id)
        return self
    
    @property
    def Angle(self):       
        angleOffset=Cal['Angle_Offset'][self._id]
        angleMax=Cal['Angle_max'][self._id]
        angleMin=Cal['Angle_min'][self._id]
        angleFac=Cal['Angle_Factor'][self._id]
        
        angleVal=(kit.servo[self._id].angle-angleOffset)/angleFac
        if angleVal<0:
            angleVal=0
        return int(round(angleVal))
        
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
        
        
#        while True:
#            for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
#                my_servo.angle = angle
#                time.sleep(0.05)
#            for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
#                my_servo.angle = angle
#                time.sleep(0.05)
        
        
        kit.servo[self._id].angle=val
        #print(val)
        #print(angleOffset)
        val=val+angleOffset
        return val
    
    def calibrate(self, Cal):
        angleRange=Cal['Angle_Range'][self._id];
        pwm_min=Cal['PWM_min'][self._id];
        pwm_max=Cal['PWM_max'][self._id];
        
        kit.servo[self._id].actuation_range = angleRange;
        kit.servo[self._id].set_pulse_width_range(pwm_min, pwm_max);
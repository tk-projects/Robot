#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 13:47:50 2020

@author: pi
"""

# Load fuctions
exec(open("/home/pi/Robot/LoadCalibration.py").read(), globals())
exec(open("/home/pi/Robot/ServoControl.py").read(), globals())

Servo=ServoClass()
Cal=LoadCalibration('/home/pi/Robot/RobotSW/Calibration/ServoCalibration.txt')



def toDeg(a):
    alpha_deg=a*360/(2*np.pi)
    return alpha_deg

def toRad(a):
    alpha_rad=a*2*np.pi/360
    return alpha_rad

def stand(height):
        h=height;   
        # calculate alpha, angle btw upper thigh and body
        h2 = (l1**2-l2**2-h**2)/(2*h);
        h1 = h-h2;
        
        alpha=toDeg(np.arccos(h1/l2))+90;
        beta=180-toDeg(np.arccos(h2/l2))-toDeg(np.arccos(h1/l2));
        
        return [alpha, beta]



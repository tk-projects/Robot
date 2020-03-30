#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 13:47:50 2020

@author: pi
"""

# Load fuctions
exec(open("/home/pi/Robot/LoadCalibration.py").read(), globals())
exec(open("/home/pi/Robot/ServoControl.py").read(), globals())
exec(open("/home/pi/Robot/LegControle.py").read(), globals())
exec(open("/home/pi/Robot/RobotControl.py").read(), globals())

Servo=ServoClass()
Cal=LoadCalibration('/home/pi/Robot/RobotSW/Calibration/ServoCalibration.txt')



def toDeg(a):
    alpha_deg=a*360/(2*np.pi)
    return alpha_deg

def toRad(a):
    alpha_rad=a*2*np.pi/360
    return alpha_rad

# Initialize Stand:
#height=21.5   # height at init.
#initStand(height)

Robot=RobotClass()
Robot.Stand(21)
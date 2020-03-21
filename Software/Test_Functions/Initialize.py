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

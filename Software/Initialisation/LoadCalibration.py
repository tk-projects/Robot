#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 13:43:08 2020

@author: pi
"""

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
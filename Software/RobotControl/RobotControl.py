#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 12:44:38 2020

@author: pi
"""


# Robot properties
class RobotClass(object):
    def __init__(self):
        self.height=21
        
        
    def Stand(self, heightSp, vel=1):
        legs=['vl','vr','hl','hr']
        heightStart=self.height
        
        Step=vel
        
        #determine direction:
        if heightSp-heightStart<0:
            direction=-1
        else:
            direction=1
        
        #change units from cm to mm:
        heightSpMm=int(round(heightSp*10));
        heightStartMm=int(round(heightStart*10));
        heightActMm=heightStartMm

        print('\nheight at start=',heightStartMm)
        print('\nheigt set point\n', heightSpMm)
        
        while True:
            if heightActMm<heightSpMm:
                direction=1
            else:
                direction=-1
            
            if abs(heightSpMm-heightActMm)<Step:
                heightActMm=heightSpMm                  # Check if step distance is bigger than difference to set point
            else:
                heightActMm=heightActMm+direction*Step
            
            for leg in legs:
                offs=0
                if leg=='hl' or leg=='hr':
                    offs=0 
                LegStand(leg, heightActMm/10+offs)
                
            self.height=heightActMm/10
            
            if heightActMm==heightSpMm:
                break
            time.sleep(0.00001)
        return self.height
            
        
    def initStand(self):
        legs=['vl','vr','hl','hr']
        height=self.height
        for leg in legs:
            offs=0
            if leg=='hl' or leg=='hr':
                offs=0
            LegStand(leg, height+offs)
            self.heigth=height
        return self.height
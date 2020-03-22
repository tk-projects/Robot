#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 16:34:57 2020

@author: pi
"""

# Leg Control

def LegStand(leg, height):
        # get servo indices from leg
        LegUp = leg+'1';
        LegLow = leg+'2';

        LegUpId = sorted(list(Cal['Servo_Pos']),key=len).index(LegUp);
        LegLowId = sorted(list(Cal['Servo_Pos']),key=len).index(LegLow);
        print(LegUpId)
        
        # calculate alpha, angle btw upper thigh and body
        h=height;
        h2 = (l1**2-l2**2-h**2)/(-2*h);
        h1 = h-h2;
        print(h1,h2)
        alpha=toDeg(np.arccos(h1/l1))+90;
        beta=180-toDeg(np.arccos(h1/l1))-toDeg(np.arccos(h2/l2));

        # min. angle alpha or max height for stability
        h_max=22
        alphaOff=52
        betaOff=48
        alphaFin=alpha-alphaOff
        betaFin=beta-betaOff
        print('\n Upper Leg %s' %(LegUpId))
        print("alpha = %s " % (alphaFin))
        print('\n Lower Leg %s' %(LegLowId))
        print(" beta = %s " % (betaFin))
        
        Servo.id(LegUpId).Angle=alphaFin
        Servo.id(LegLowId).Angle=betaFin
        
        return [alpha, beta]
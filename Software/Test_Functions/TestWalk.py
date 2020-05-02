#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 11:42:19 2020

@author: pi
"""

# Robot test walk:

Robot.Stand(22,0.45)
Robot.Stand(17,0.45)
Robot.Stand(22,0.45)

for i in range(1,5):
    LegStep2(['vr','hl','vl','hr'],2, 22, DelayArr=[0,0.4,1,0.98],vel=1.5)
    
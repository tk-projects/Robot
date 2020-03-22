#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 17:29:14 2020

@author: pi
"""

# Robot Control

def Stand(height):
    legs=['vl','vr','hl','hr']
    
    for leg in legs:
        offs=0
        if leg=='hl' or leg=='hr':
            offs=0.5
            
        LegStand(leg, height+offs)

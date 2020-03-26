#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 16:34:57 2020

@author: pi
"""
import time
# Leg Control

def LegStandVel(leg, height,angleStep=1):
        # get servo indices from leg
        LegUp = leg+'1';
        LegLow = leg+'2';

        LegUpId = sorted(list(Cal['Servo_Pos']),key=len).index(LegUp);
        LegLowId = sorted(list(Cal['Servo_Pos']),key=len).index(LegLow);
        
        # calculate alpha, angle btw upper thigh and body
        h=height;
        h2 = (l1**2-l2**2-h**2)/(-2*h);
        h1 = h-h2;
        #print(h1,h2)
        alpha=toDeg(np.arccos(h1/l1))+90;
        beta=180-toDeg(np.arccos(h1/l1))-toDeg(np.arccos(h2/l2));

        # min. angle alpha or max height for stability
        h_max=22
        alphaOff=52     # Offset since alpha is not starting at "0", not starting from horizontal pos.
        betaOff=48      # Offset since beta is not starting at "0", not starting from horizontal pos.
        
        alphaFin=int(round(alpha-alphaOff))
        betaFin=int(round(beta-betaOff))
        
        print('\n Upper Leg %s' %(LegUpId))
        print("alpha = %s " % (alphaFin))
        print('\n Lower Leg %s' %(LegLowId))
        print(" beta = %s " % (betaFin))
        
        #Servo.id(LegUpId).Angle=alphaFin
        #Servo.id(LegLowId).Angle=betaFin
        
        # Determine current servo angle
        angleStartLegUp=Servo.id(LegUpId).Angle;
        angleStartLegLow=Servo.id(LegLowId).Angle;
        
        # Determine moving direction:
        directionLegUp=0;
        directionLegLow=0;
        
 
        i=1;
        
        angleCurLegUp=angleStartLegUp;
        angleCurLegLow=angleStartLegLow;
        
        angleSetLegUp=angleStartLegUp;
        angleSetLegLow=angleStartLegLow;
        
        print('\n angle Setpoints:', alphaFin,betaFin)
        print('\n angle Starting points:', angleStartLegUp,angleStartLegLow)
        
        while True:            
            # Determine moving direction:
            if angleCurLegUp<alphaFin:
                directionLegUp=1;
            else:
                directionLegUp=-1;
            
            if angleCurLegLow<betaFin:
                directionLegLow=1;
            else:
                directionLegLow=-1;
            
            
            if angleSetLegUp == alphaFin:
                angleSetLegUp = alphaFin;
            
            else:
                angleSetLegUp = angleCurLegUp+angleStep*directionLegUp;
                
                a=alphaFin-angleSetLegUp
                if abs(a)<angleStep:   
                    angleSetLegUp=alphaFin
                    print('\nalpha reached!',angleSetLegUp)
            
            if angleSetLegLow == betaFin:
                angleSetLegLow = betaFin;
            else:
                angleSetLegLow = angleCurLegLow+angleStep*directionLegLow;
                
                b=betaFin-angleSetLegLow
                if abs(b)<angleStep:           
                    angleSetLegLow=betaFin
                    print('\nbeta reached!',angleSetLegLow)
            
            print('\nalpha:',angleSetLegUp,'beta:',angleSetLegLow,'    ', i)
            print('\nalpha:',angleSetLegUp,'beta:',angleSetLegLow,'    ', i)
            
            if angleSetLegUp == alphaFin and angleSetLegLow == betaFin:
                break
            
            
            # Current angle
            angleCurLegUp=angleSetLegUp
            angleCurLegLow=angleSetLegLow
            i=i+1
            if i>150:
                break
            Servo.id(LegUpId).Angle=angleSetLegUp
            Servo.id(LegLowId).Angle=betaFin
            time.sleep(0.01)
        return [alphaFin, betaFin]
    
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
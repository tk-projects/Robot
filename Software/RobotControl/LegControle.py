#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 16:34:57 2020

@author: pi
"""
import numpy as np;
from sympy import*

# Leg Geometry
l1=6.7 # length in cm from joint to joint of the upper thigh
l2=15.5 # length in cm from joint to joint of the lower thigh
r1=l1
r2=l2

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
                    #print('\nalpha reached!',angleSetLegUp)
            
            if angleSetLegLow == betaFin:
                angleSetLegLow = betaFin;
            else:
                angleSetLegLow = angleCurLegLow+angleStep*directionLegLow;
                
                b=betaFin-angleSetLegLow
                if abs(b)<angleStep:           
                    angleSetLegLow=betaFin
                    #print('\nbeta reached!',angleSetLegLow)
            
            #print('\nalpha:',angleSetLegUp,'beta:',angleSetLegLow,'    ', i)
            #print('\nalpha:',angleSetLegUp,'beta:',angleSetLegLow,'    ', i)
            
            if angleSetLegUp == alphaFin and angleSetLegLow == betaFin:
                break
            
            
            # Current angle
            angleCurLegUp=angleSetLegUp
            angleCurLegLow=angleSetLegLow
            i=i+1
            
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
        #print(LegUpId)
        
        # min. angle alpha or max height for stability
        h_max=22
        # calculate alpha, angle btw upper thigh and body
        h=min(height,h_max);
        h2 = (l1**2-l2**2-h**2)/(-2*h);
        h1 = h-h2;
        #print(h1,h2)
        alpha=toDeg(np.arccos(h1/l1))+90;
        beta=180-toDeg(np.arccos(h1/l1))-toDeg(np.arccos(h2/l2));
        print(alpha);
        print(beta);
        
        alphaOff=52
        betaOff=48
        alphaFin=alpha-alphaOff
        betaFin=beta-betaOff
        #print('\n Upper Leg %s' %(LegUpId))
        print("alpha = %s " % (alphaFin))
        #print('\n Lower Leg %s' %(LegLowId))
        print(" beta = %s " % (betaFin))
        
        Servo.id(LegUpId).Angle=alphaFin
        Servo.id(LegLowId).Angle=betaFin
        
        return [alpha, beta]
    
    
def LegStep(legArr,StepWidth, height, DelayArr=[1,1,1,1],vel=5):
    
    d=StepWidth;
    h=min(height,22);
    legNum=len(legArr)
    print(legNum)
       # to calculate the angles of upper and lower thigh, both thighs will be be represented by two circles
       # each circle has the radius of the length of one thigh, then the intersection line between both circles will be calculated
       
       # intersection line: y = -d/h*x - (r1²-r2²+d²+h²)/(2*h)
       # of the two circles dont intersect which each other, the step distance is two high and can not be realised
       # therefore the distance between both circles will be calculated:  
    m = sqrt(d**2+h**2);
    mLim = l1+l2;
    dMax=sqrt(mLim**2-h**2);
    d=min(StepWidth,dMax);
    
       # Program sequence:
       # 1. Angle Calculation (StepAngleCalc)
       # 2. Lifting of the leg (LegLift)
       # 3. Step down (LegStepDown)
       # 4. Move to init. Position (initPos or LegStand)
    [alphaStep, betaStep] = StepAngleCalc(d,h);
    [alphaInit, betaInit] = StepAngleCalc(0,h);
    
    alphaLift=alphaStep-15;
    betaLift=betaStep;
    angleStep=vel;
       
    LegIdArr=[];                                # Array with the ids of the servos
    legMovemntProgArr=np.zeros([legNum,1])     # Array to track movement progress
    legLiftDoneArr=np.zeros([legNum,1]);        # Array to track wether lifting was completed
    legStepdownDoneArr=np.zeros([legNum,1]);    # Array to track wether stepping down was completed
    legInitPosDoneArr=np.zeros([legNum,1]);     # Array to track wether init pos. was completed
    angleCurLegUpArr=[];                        # Array to store starting angles of the upper thigh servos
    angleCurLegLowArr=[];                       # Array to store starting angles of the low er thigh servos
    legUpIdArr=[];
    legLowIdArr=[];
    legProg=0;
    t=0
    # Get starting position and other parameters of the individual thigs:
    for j in range(0,len(legArr)):
        leg=legArr[j]
        legUp = leg+'1';
        legLow = leg+'2';
        
        legUpId = sorted(list(Cal['Servo_Pos']),key=len).index(legUp);
        legLowId = sorted(list(Cal['Servo_Pos']),key=len).index(legLow);
        legUpIdArr.append(legUpId)
        legLowIdArr.append(legLowId)
        
        
        legUpStartAngle=Servo.id(legUpId).Angle;
        legLowStartAngle=Servo.id(legLowId).Angle;
        legUpIdArr.append(legUpId);
        legLowIdArr.append(legLowId);
        angleCurLegUpArr.append(legUpStartAngle);
        angleCurLegLowArr.append(legLowStartAngle);

        
    print('__________________________________________________________________________________________________________\n__________________________________________________________________________________________________________')     
    print('\n\nStarting Angles:','alpha',angleCurLegUpArr,' beta ',angleCurLegLowArr)
    print('\nAngle set points:','\n','alphaLift' ,alphaStep,' betaLift ',betaStep-15)
    print('\nalphaStep' ,alphaStep,' betaStep ',betaStep)
   
    while True:
       t+=1;
       print(t)
       for i in range(0,len(legArr)):
           leg=legArr[i];
           angleCurLegUp=angleCurLegUpArr[i];
           angleCurLegLow=angleCurLegLowArr[i];
           
           #Monitor movement progress
           print('delay',DelayArr[i],'   progress',legMovemntProgArr[min(0,i-1)])
           
           # Check if delay to previous leg movement is over
           if DelayArr[i]<=(legMovemntProgArr[max(0,i-1)]+0.01):
               print('delayed')
               print(int(sum(legMovemntProgArr)),len(legArr))
               continue
               
           # if the movement is completed continue with next leg
           if legMovemntProgArr[i]>=1:      
               continue    
           
           # Leg lift
           if legLiftDoneArr[i]==0:
               print('\n |\033[4mLifting\033[0m|')
               alphaFin=alphaStep;
               betaFin=betaStep-15;

           else: 
               # Step down:
               if legStepdownDoneArr[i]==0:
                   print('\n                |\033[4mStep Down\033[0m|')
                   alphaFin=alphaStep;
                   betaFin=betaStep;
                   legProg=alphaStep+betaStep-15
                   
               # Move to init pos:
               else:
                   print('\n                          |\033[4mMove to init Position\033[0m|')
                   alphaFin=alphaInit;
                   betaFin=betaInit;
                   legProg=2*alphaStep+betaStep+betaStep-15
           
           # Define directions:
           if angleCurLegUp<alphaFin:
                directionLegUp=1;
           else:
                directionLegUp=-1;
            
           if angleCurLegLow<betaFin:
                directionLegLow=1;
           else:
                directionLegLow=-1;
           
           print('\n',directionLegUp,directionLegLow) 
           
           if angleCurLegUpArr[i]==alphaFin:
               angleSetLegUp=alphaFin
           else:
               angleSetLegUp = angleCurLegUp+angleStep*directionLegUp;
                
           a=alphaFin-angleSetLegUp;
           if abs(a)<angleStep:   
               angleSetLegUp=alphaFin;
               print('\nalpha reached!',angleSetLegUp)
            
          
           if angleCurLegLowArr[i]==betaFin:
               angleSetLegLow=betaFin
           else:
               angleSetLegLow = angleCurLegLow+angleStep*directionLegLow;
               
           b=betaFin-angleSetLegLow;
           if abs(b)<angleStep:           
               angleSetLegLow=betaFin;
               print('\nbeta reached!',angleSetLegLow)
               

           print('\nleg:',leg,'\nalpha:',angleSetLegUp,'beta:',angleSetLegLow,'    ', i)
           print('alpha:',angleSetLegUp,'beta:',angleSetLegLow,'    ', i)
            
           # Track movement Progress:
           if angleSetLegUp == alphaStep and angleSetLegLow == betaStep-15:
               legLiftDoneArr[i]=1
               print('Lifting done')
               print('\n\nalphaStep' ,alphaStep,' betaStep ',betaStep)
               input('press key')
           
           if legLiftDoneArr[i]==1:
               if angleSetLegUp == alphaStep and angleSetLegLow == betaStep:
                   legStepdownDoneArr[i]=1
                   print('Step down done')
                   input('press key')
               #if legStepdownDoneArr[i]==1 and angleSetLegUp == alphaInit and angleSetLegLow == betaInit:
                   
           # Set current angle
           angleCurLegUpArr[i]=angleSetLegUp
           angleCurLegLowArr[i]=angleSetLegLow
            
           legMovemntProgArr[i]=(legProg+angleSetLegUp+angleSetLegUp)/(2*alphaStep+betaStep+betaStep-15+alphaInit+alphaInit);
           print(str(legMovemntProgArr[i]));
           print(str(legMovemntProgArr));
           Servo.id(legUpIdArr[i]).Angle=angleSetLegUp
           Servo.id(legLowIdArr[i]).Angle=betaFin

       if int(sum(legMovemntProgArr))==len(legArr):
           break
       time.sleep(0.2)
               
               
           
   

def StepAngleCalc(StepWidth, height):
    # Calculate intersection pionts:
    # intersection line: y = -d/h*x - (r1²-r2²+d²+h²)/(2*h)
    # Calculate intersection with first ciclce (from upper tigh)
    h=height;
    d=StepWidth;
    
    A=(r1**2-r2**2+d**2+h**2)/(2*h);
    x=symbols("x",real=True);
    
    # Nullstellen
    zeros=solve(x**2*(1+d**2/h**2)-2*d/h*x*A+A**2-r1**2,x);
    print(zeros);

    # chose one of the intersection points, smaller one
    # and calculate coordinates
    x=min(zeros);
    x=float(x);
    y=sqrt(r1**2-x**2);
    a=x/r1;
    print(toDeg(np.arcsin(a)))
    alpha=toDeg(np.arcsin(a));
    alphaTot=90-toDeg(np.arcsin(a));
    
    
    beta=toDeg(np.arccos((d-x)/r2))
    betaTot=90+alpha+beta
    print('\n',beta)
    print('alpha=',alphaTot,'  beta=',betaTot);
    
    alphaOff=52
    betaOff=48
    
    alphaFin=int(round(alphaTot-alphaOff))
    betaFin=int(round(betaTot-betaOff))
    
    return [alphaFin, betaFin]
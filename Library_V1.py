# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:56:04 2020

@author: Gohar Shoukat
Function Definition File
"""
import math
import numpy as np
import scipy.optimize
import pandas as pd
#Data input
#Design significant wave height 

#Design Peak=absolute period
def absolute_frequency(Tp):
    w_a=2*math.pi/Tp
    return w_a
    
'''
k is return from function diffraction parameter from
phi in radians
Velocity function calculates the horizontal velocity based on 
water depth characterization. 
parameter x passed from function depth
Time is relative time period
x=0 shallow, x=1 Deep, x=2 intermediate        

'''

        
#surface current velocity u
#gravitational acceleration g
#diffraction parameter kc
#wave length = L

def diffraction_parameter(g, h, tide, u_c, w_a):
    def solve_for_k(k):
        f=u_c*k+math.sqrt(g*k*math.tanh(k*(h+tide)))-w_a
        return f
    
    x=scipy.optimize.fsolve(solve_for_k,0)
    
    
    def L():
        wave_length = 2*math.pi/x
        return wave_length
    
    y = L()

    
    
    return (x, y)


#water depth h
#deep, shallow, intermediate

def depth(L, h, x=-1):

    ratio = h/L
    if ratio <= 1/20:
        x=0  #
        print ("Shallow Water")
     
    elif ratio >= 1/2:
          print ("Deep Water")
          x=1
    elif ratio>1/20 and ratio<1/2:
          print ("Intermediate Water")
          x=2
    return ratio, x


#Needed to determine if diffraction is important or not. 
    #determine if structure is small or not. 
    #small structure has value<0.5 and vice versa for large structures
    #function returns a True Boolean value for a large structure
#diameter of structure = d
    
def diffraction_theory(d, L):
    characterization = math.pi*d/L
    if characterization > 0.5:
        return True
    else:
        return False


#x is passed on from function depth. it signals the function touse
        #the correct equation
        #L is passed on from diffraction parameter which is the wavelength
        #phi is the angle between th current and wave
        #H is the significant wave height
        #T_r is the relative time period
        #K is the diffraction parameter and is different from KC
        #h is the total depth
        #delta defines the stepping difference

def horizontal_velocity_acceleration_amplitude (g, H, T_r, k, phi, tide, x, L, h, delta,
                                    wave_amplitude, absolute_angular_velocity,
                                    time):
    
    #Find the wave equation to satisfy the condition
        #-H/2<z<H/2, properties equal to surface level conditions. 
        #first find wave equation by integrating the velocity equation 
        #u = H/2 sin (wt)
        #s = -H/2 w cos wt
    s = H/2 * ( np.cos(-absolute_angular_velocity * time))

#velocity to be calculated at intervals of delta
#size function used to determine the size of array
#z = 0 @ surface and z = max at seabed
    z = np.arange(-h-tide,0+delta+wave_amplitude,delta)
    size = len(z)
    #if the delta z value is kept to be 0.1, 0 doesnt show in the z array
    #to avoid the problem, the exponent is enforced to be 0
    z = np.around(z, decimals = 3)
    length_time = len(time)
    #u0 is horizontal velocity amplitude
    u0 = np.zeros((size, length_time))
    if x==0:
        u = (H/2)*math.sqrt(g/h)*math.cos(phi)
        
    elif x==1:
        for i in range(int(size+1)):
            u [i] = math.pi*H/T_r*math.exp(k*z[i])*math.cos(phi)
            
    elif x==2:
         sigma = np.zeros(size)
         #horizontal acceleration amplitude accel0
         accel0 = np.zeros((size,length_time))
         #remove values for velocity above sea sruface. 
         for i in range(int(size)):
             sigma [i] = k*(z[i]+h+tide)
        
         sigma2 = np.where(z<0 , sigma, sigma[z == 0])
         
         for j in range(int(length_time)):
             for i in range(size):
                 u0 [i, j] = (g*H*T_r/(2*L))*\
                                             np.cosh(sigma2[i])/np.cosh(k*(h+tide))
                                             
                 accel0 [i,j] = g*H*math.pi/L*np.cosh(sigma2[i])/np.cosh(k*(h+tide))
                


         
    return u0, z, s, sigma2, accel0
    
        

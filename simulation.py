"""
Created on Sat Jul 17 12:43:30 2021

@author: olaf_
"""

import numpy as np

class Simulation:
   
    def __init__(self, missionProfile):
       
        # Driver parameters
        self.decmax = 1 # Maximum deceleration in m/s/s [VECTO]
        self.accmax = 1 # Maximum acceleration in m/s/s [VECTO]
        
        # Environmental constants
        self.g = 9.81 # Gravity constant in m/s/s [VECTO]
        self.rho = 1.188 # Air density in kg/m/m/m [VECTO]
        
        self.preprocessing(missionProfile)
    
    def preprocessing(self, missionProfile):
        
        # Unpack missionprofile        
        s = missionProfile["<s>"].values # Distance in m
        v = missionProfile["<v>"].values/3.6 # Speed in m/s
        grad = missionProfile["<grad>"].values # Gradient in %
        stop = missionProfile["<stop>"].values # Stop duration in s
        
        # Calculate distance step along route
        ds = np.diff(s)
        
        # Generate array with dec phases
        i2 = np.where(np.diff(v)<0)[0]+1 #ends of deceleration phases
        i1 = np.append([0], i2[:-1]) #start of deceleration phases
        v_target = np.zeros(len(v))
        for i1, i2 in zip(i1,i2):
            v_target[i1:i2] = np.minimum(
                v[i1:i2], # drive cycle speed
                np.sqrt(v[i2]**2+2*self.decmax*(s[i2]-s[i1:i2]))) #deceleration speed
                
        self.s = s
        self.v = v
        self.grad = grad
        self.stop = stop
        self.vtarget = v_target
        self.ds = ds
    
    def run(self, veh, gvw):
        s = [0]
        t = [0]
        v = [0]
        p = []
        for (stop, ds, vtarget, grad) in zip(
                self.stop, self.ds, self.vtarget[1:], self.grad):
            
            # If the vehicle is stopped, add extra entry to list
            if stop>0:
                s.append(s[-1])
                t.append(t[-1]+stop)
                v.append(0)
                p.append(0)   
            
            # Determine target acceleration
            atarget = (vtarget**2-v[-1]**2)/2/ds #target acceleration
            
            # Determine power limited maximum acceleration
            f_roll = gvw*self.g*veh.fr*np.cos(np.arctan(grad/100)) #Rolling resistance in N
            f_drag = 0.5*self.rho*veh.cd_a*v[-1]**2 #Drag resistance in N
            f_incl = gvw*self.g*np.sin(np.arctan(grad/100)) #Inclination resistance in N
            f_max = veh.motor_power/v[-1] if v[-1]>0 else 1e9  #Max driving force in N
            apower = (f_max*veh.eta-f_roll-f_drag-f_incl)/gvw #Max acceleration in m/s/s
            
            # Determine acceleration and new states
            a = min(atarget, apower, self.accmax) #Applied acceleration in m/s/s
            v_new = np.sqrt(v[-1]**2+2*a*ds) #New vehicle speed in m/s
            t_new = t[-1] + 2*ds/(v[-1]+v_new) #New time since start in s
            f_res = gvw*a+f_roll+f_drag+f_incl
            p_new = f_res*v[-1]*veh.eta**np.sign(-f_res) #Applied power in W
            
            # Append new states to lists
            s.append(s[-1]+ds)
            t.append(t_new)
            v.append(v_new)
            p.append(p_new)
            
        p_bat = np.maximum(p,-veh.motor_power) # Remove sections relying on mechanical breaking
        e_operation = sum(p_bat*np.diff(t)) # Calculate Energy Demand
        con = e_operation/3600/s[-1] # Consumption in kWh/km
        v_avg = s[-1]/t[-1]*3.6 # Average speed in km/h
        p.append(0) # Append power value to create equal length lists


        return con, v_avg, s, t, v, p
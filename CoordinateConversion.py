# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 16:42:30 2018
Provides functions for conversion of points in the collision space of the 
Bunimovich stadium.
This provides a library of functions that transform points in the collision 
space to and from cartesian and spherical.

@author: Randy
"""
import math

def thetaphiTOxybeta(theta, phi, lam):
    """ theta := polar angle of the location where a collision occurs.
        phi   := angle of the postcollisional velocity vector WRT the inward
                 normal vector.
        lam   := the ratio of twice the length of the billiard table to its
                 radius.
        This function takes (theta, phi) and produces the x,y pair representing
        that location in cartesian coordinates. It also finds beta, the polar
        angle of the direction of the velocity vector.
    """
    # Calculate the reference angle associated with this insance of a
    # Bunimovich Stadium. This angle will be used to determine on which wall
    # the point resides.
    ref = math.atan(float(2)/lam)
    halfLam = float(lam)/2
    theta = mod2pi(theta)
    
    # Note: if lam = 2 then ref = 0.785398163397 = pi/4  
    # See if the point is on the top or bottom side.    
    # Top side
    if  theta >= ref and theta <= math.pi - ref:
         x = float(1)/math.tan(theta)
         y = 1
         beta = 3*math.pi/2 + phi
         return (x, y, beta)
         
    # Bottom side
    if math.pi + ref <= theta and theta <= 2*math.pi - ref:
        x = -float(1)/math.tan(theta)
        y = -1
        beta = math.pi/2 + phi
        return (x, y, beta)
    
    # Calculate values needed for locations in either cap.
    cos = math.cos(theta)
    sin = math.sin(theta)
    
    # Left cap
    if math.pi - ref < theta and math.pi + ref > theta:
        rho = -halfLam*cos + math.sqrt(1 - math.pow(sin*halfLam,2))
        x   = rho*cos
        y   = rho*sin
        vx = -(x + halfLam)*math.cos(phi) + y*math.sin(phi)
        vy = -(x + halfLam)*math.sin(phi) - y*math.cos(phi)
        beta = mod2pi(math.atan2(vy,vx))
        return (x, y, beta)
        
    # Right cap
    if (0 <= theta and theta < ref) or \
    (2*math.pi - ref < theta and theta <= 2*math.pi):
        rho = halfLam*cos + math.sqrt(1 - math.pow(sin*halfLam,2))
        x   = rho*cos
        y   = rho*sin
        vx = -(x - halfLam)*math.cos(phi) + y*math.sin(phi)
        vy = -(x - halfLam)*math.sin(phi) - y*math.cos(phi)
        beta = mod2pi(math.atan2(vy,vx))
        return (x, y, beta)
#-------------------------------------------------- End of thetaphiTOxybeta
        
    
#  (x,y, beta) |-----> (theta, phi)
def xybetaTOthetaphi(x, y, beta, lam):
    """ (x,y) := The cartesian coodinates of the collision.
        beta  := The polar angle of the velocity vector.
        This function takes a (x,y,beta) tripple and produces a
        theta phi pair.
    """
    # Calculate theta
    theta = mod2pi(math.atan2(y, x))
    # This value is commonly used...
    halfLam = float(lam)/2
    
    # We shall calculate psi \in [0, pi]. This is the angle between the 
    # post collisional velocity vector and the positively oriented tangent to
    # the stadium's boundary. We calculate psi to find phi.
    # Right cap
    if x > halfLam:
        # switched sign of y*cos(beta) and the second term too.
        psi = math.acos(-y*math.cos(beta) + (x - halfLam)*math.sin(beta))
    # The Sides
    elif x >= -halfLam:
        # Top Side
        if y == 1:
            psi = beta - math.pi
        elif y == -1:
            psi = beta
        else:
            # If the x-coordinate is between -halfLambda and halfLambda 
            # inclusive then the y-coordinate must be 1 or -1 because
            # the billiard must have intersected one of the flat walls.
            # So if y is neither of these values an error message should be
            # displayed.
            print "An attempt was made to convert x,y to theta,phi but"
            print "the x-value corresponds to a side of the stadia and"
            print "the y-value does not! The bad values are: "
            print "[x,y,beta] = " + str([x,y,beta])
    # Left cap
    else:
        psi = math.acos(-y*math.cos(beta) + (x + halfLam)*math.sin(beta)) 
    # Use psi to find phi
    phi = psi - math.pi/2
    return (theta, phi)
#--------------------------------------------------- End xybetaTOthetaphi
    

def mod2pi(angle):
    """ Takes an angle and returns the coterminal angle in [0,2pi).
    """
    while angle < 0:
        angle = angle + 2*math.pi
    while angle >= 2*math.pi:
        angle = angle - 2*math.pi
    return angle

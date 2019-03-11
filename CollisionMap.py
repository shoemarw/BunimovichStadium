# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 14:12:38 2018
Computes collisions by iterating the collision map. Implements the stadia's
Collision map to find the successive collision of a given collision. Uses 
CoordinateConversion.py.

@author: Randy
"""

import math
from CoordinateConversion import mod2pi

def collisionLoop(x, y, beta, iterations, lam):
    """ Calls the collision map 'iterations' times on the initial condition 
        (x,y,b). Each calculated collision is saved in a list which is returned
        by this function.
    """
    # This value sets an error tolerance when comparing two "equal" values
    global epsilon
    epsilon = math.pow(10,-7)
    global delta
    delta = math.pow(10,-6)
    
    # This value is used frequently in most of the functions.
    global halfLam
    halfLam = float(lam)/2     
       
    points = [(x,y,beta)]
    
    # Iteratively call the collision map. Save the collision points returned.
    while iterations > 0:
        (x,y,beta) = collisionMap(x,y,beta)
        points.append((x,y,beta))
        iterations = iterations - 1
        
    return points

def collisionMap(x,y,beta):
    """ Calculates the next collision given the previous collision specified
        by x,y,beta. The next collision is returned as x1,y1,b1. This function
        uses the 4 boolean flags described below.
    """
    # ::The COLLISION variable::
    # This variable indicates where the previous collision was, within the 
    # collision testers it is set to where the collision is. The key describing
    # the values for this variable and what they mean are as follows:
    # 0 indicates that the variable has just been reset/ collision location
    # unknown.
    # 1 indicates that the collision was with the left cap.
    # 2 indicates that the collision was with the upper side.
    # 3 indicates that the collision was with the right cap.
    # 4 indicates that the collision was with the lower side.
    # Set the variable to zero to indicate that the location of the previous
    # collision is unknown.
    collision = 0
    
    beta = mod2pi(beta)
    
    # Check for the special case where the billiard is traveling horizontally.
    if beta == 0 or beta == math.pi:
        return horizontalPath(x,y,beta)
    
    # Check for the special case where the billiard is traveling vertically.
    if abs(beta - math.pi/2) < delta or abs(beta - 3*math.pi/2) < delta:
        return verticalPath(x,y,beta)
    
    # See which part of the billiard table the initial condition (a collision) 
    # resides. Then set collision to the appropriate value.    
    # See which part of the table the initial condition resides.
    if x < -halfLam:
        # left cap.
        collision = 1
    elif x <= halfLam:
        if y > 0:
            # Upper side.
            collision = 2
        if y < 0:
            # Lower side.
            collision = 4
    else:
        # right cap.
        collision = 3    
       
    if not collision == 2 :
        # Run collision test for upper side.
        point = upperSideCollisionTest(x,y,beta)
        if point != None:
            return point
    
    if not collision == 4:
        # Run collision test for lower side.
        point = lowerSideCollisionTest(x,y,beta)
        if point != None:
            return point
 
    point = leftCapCollisionTest(x,y,beta, collision)
    if point != None:
        return point
 
    point = rightCapCollisionTest(x,y,beta, collision)
    if point != None:
        return point
    
    print "The collision map did not detect a collision for the input: "
    print "[x,y,beta] = " + str([x,y,beta])
    return (0,0,0)
###################################################END Collision Map##########
    

def upperSideCollisionTest(x,y,beta):
    """ This function checks for a collision with the upper side. If one is
        detected, then calculate the coordinates where it occurs and the 
        billiard's new direction. The input is the coordinate of the billiard's
        previous collision along with the slope of the line representing the
        path. The coordinates of the new collision are returned along with the
        angle specifying the direction. If no collision was detected then None
        is returned.
    """
    # Set the slope of the line representing the path of the billiard.
    m = math.tan(beta)
    # See where the billiard's path intersects the line y=1.
    # If this occurs in the proper range then a collision with
    # the upper side has occurred.
    intersection = (1-float(y))/m + x
    if -halfLam <= intersection and intersection <= halfLam:
        x1 = intersection
        y1 = 1
        # find the components of the post-collisional velocity vector.
        vpx = math.cos(beta)
        vpy = -math.sin(beta)
        # use the post collisional velocity vector to find the new direction 
        # angle
        beta1 = math.atan2(vpy,vpx)
        return (x1, y1, mod2pi(beta1))
    return None

##############################################END upperSideCollisionTest()####
    
def lowerSideCollisionTest(x,y,beta):
    """ Tests for collision with LS. IF one occurs return the new collisions 
        coordinates with the billiards new direction. Otherwise return None.
    """
    # Set the slope of the line representing the path of the billiard.
    m = math.tan(beta)
    # See where the billiard's path intersects the line y=1.
    # If this occurs in the proper range then a collision with
    # the upper side has occurred.
    intersection = (-1-float(y))/m + x
    if -halfLam <= intersection and intersection <= halfLam:
        x1 = intersection
        y1 = -1
        # find the components of the post-collisional velocity vector.
        vpx = math.cos(beta)
        vpy = -math.sin(beta)
        # use the post collisional velocity vector to find the new direction 
        # angle
        beta1 = math.atan2(vpy,vpx)
        return (x1, y1, mod2pi(beta1))
    return None

############################################END lowerSideCollisoinTest()######
    
def leftCapCollisionTest(x,y,beta,collision):
    """ Tests for a collision with the upper left cap. If one is detected,
        the new x,y, and beta-values are computed and returned. If not, then
        None is returned.
    """
    # Set the slope of the line representing the path of the billiard.
    m = math.tan(beta)
    # Set variables used to test for a collision
    mSquare = math.pow(m,2)
    a = mSquare + 1
    b = 2*m*y - 2*mSquare*x + 2*halfLam
    c = mSquare*math.pow(x,2) - 2*m*y*x + math.pow(y,2) \
        + math.pow(halfLam,2) - 1
    bSquare = math.pow(b,2)
    discr = bSquare - 4*a*c
    # Ensure that the discriminant is non-negative!
    if discr < 0:
        return None
    # 
    square = math.sqrt(discr)
    a2 = 2*a
    # Find the two potential x-values of a collision with the upper left cap.
    d = (-b + square)/a2
    e = (-b - square)/a2
    # See if the previous collision was in the left cap.
    if collision == 1 :
        # The previous collision was in the left cap. See which 
        # potential x-value was the x-value of the previous collision.
        # The other potential x-value must belong to the new collision.
        # Set collision to 1  to indicate that a collision with left cap
        # was detected so that the new y-value and direction can be computed
        # below.
        if abs(x-e) < epsilon and d < -halfLam:
            x1 = d
            collision = 1

        elif abs(x-d) < epsilon and e < -halfLam:
            x1 = e
            collision = 1
        else:
            # The previous collision was in the upper left cap and the
            # old x-value does not correspond to one of the solutions of the
            # billiard's path intersecting the cap.
            collision = 0
    else:
        # The previous collision was not in the upper left cap. Test potential
        # x-values to see if they lie on the upper left cap.
        if -halfLam -1 <= d and d < -halfLam:
            # A collision was detected, set the new x-value, collision to 1 
            # so the new y-value and direction can be computed below.
            x1 = d
            collision = 1
        elif -halfLam -1 <= e and e < -halfLam:
            # A collision was detected, set the new x-value, collision to 1 
            # so the new y-value and direction can be computed below.
            x1 = e
            collision = 1
    # If a collision was detected we must compute the new y-value and direction
    # Otherwise we return None as specified.
    if collision == 1:
        # Set the new y-value
        y1 = m*(x1 - x) + y
        # Calculate the components of the pre-collisional velocity vector
        vmx = math.cos(beta)
        vmy = math.sin(beta)
        # Calculate the components of the inward normal vector
        nx = -(x1 + halfLam)
        ny = -y1
        # calculate the dot product of the pre-collisional velocity vector and 
        # the inward normal
        dot = vmx*nx + vmy*ny
        # Calculate the components of the post-collisional velocity vector
        vpx = vmx - 2*dot*nx
        vpy = vmy - 2*dot*ny
        # Calculate the direction angle of the post-collisional velocity vector
        beta1 = math.atan2(vpy, vpx)
        return (x1, y1, mod2pi(beta1))
    return None

#####################################End Left Cap Collision Tester

def rightCapCollisionTest(x,y,beta, collision):
    """ Tests for a collision with the upper right cap. If one is detected,
        then the new x,y, and beta-values are computed and returned. If not,
        then None is returned. 
    """
    # Set the slope of the line representing the path of the billiard.
    m = math.tan(beta)
    # Set variables used to test for a collision
    mSquare = math.pow(m,2)
    a = mSquare + 1
    b = 2*m*y - 2*mSquare*x - 2*halfLam
    c = mSquare*math.pow(x,2) - 2*m*y*x + math.pow(y,2) \
        + math.pow(halfLam,2) - 1
    bSquare = math.pow(b,2)
    discr = bSquare - 4*a*c
    # Ensure that the discriminant is non-negative!
    if discr < 0:
        return None
    square = math.sqrt(discr)
    a2 = 2*a
    # Find the two potential x-values of a collision with the upper right cap.
    d = (-b + square)/a2
    e = (-b - square)/a2
    # Check if the previous collision was with the upper right cap.
    if collision == 3:
        # The previous collision was in the upper right cap. See which 
        # potential x-value was the x-value of the previous collision.
        # The other potential x-value must belong to the new collision.
        # Set collision to 3 to indicate that a collision with upper right cap
        # was detected so that the new y-value and direction can be computed
        # below.
        if abs(x-d) < epsilon and e > halfLam:
            x1 = e
            collision = 3
        elif abs(x-e) < epsilon and d > halfLam:
            x1 = d
            collision = 3
        else:
            # The previous collision was in the upper right cap and the
            # old x-value does not correspond to one of the solutions of the
            # billiard's path intersecting the cap.
            collision = 0
    else:
        # The previous collision was not in the right cap. Test the potential
        # x-values to see if they lie on the right cap.
        if halfLam <= d and d <= halfLam + 1 + epsilon:
            # A collision was detected, set the new x-value, collision to 3
            # so the new y-value and direction can be computed below.
            x1 = d
            collision = 3
        elif halfLam <= e and e <= halfLam + 1 + epsilon:
            # A collision was detected, set the new x-value, collision to 3 
            # so the new y-value and direction can be computed below.
            x1 = e
            collision = 3
    # If a collision was detected we must compute the new y-value and direction
    # Otherwise we return None as specified.
    if collision == 3:
# Set the new y-value
        y1 = m*(x1 - x) + y
        # Calculate the components of the pre-collisional velocity vector
        vmx = math.cos(beta)
        vmy = math.sin(beta)
        # Calculate the components of the inward normal vector
        nx = -(x1 - halfLam)
        ny = -y1
        # calculate the dot product of the pre-collisional velocity vector and 
        # the inward normal
        dot = vmx*nx + vmy*ny
        # Calculate the components of the post-collisional velocity vector
        vpx = vmx - 2*dot*nx
        vpy = vmy - 2*dot*ny
        # Calculate the direction angle of the post-collisional velocity vector
        beta1 = math.atan2(vpy, vpx)
        return (x1, y1, mod2pi(beta1))
    return None

#####################################End Right Cap Collision Tester
    

def horizontalPath(x,y,beta):
    """ This function calculates the next collision for a particle traveling
        in a purely horizontal direction. (the set where this happens should
        have a measure of zero)
    """
    # The billiard is traveling horizontally so the next collision has the 
    # same y-value and the x-value is reflected about the y-axis.
    y1 = y
    x1 = -x
    
    # Check for the special case where the billiard is traveling along the
    # x-axis. If it is it shall bounce back along the same path.
    if y == 0:
        if beta == 0:
            beta1 = math.pi
        elif beta == math.pi:
            beta1 = 0
        return (x1, y1, mod2pi(beta1))
    
    # Check if the billiard is traveling from left to right.
    # Notice that the billiard can not collide with a flat wall because
    # it is traveling horizontally, which is parallel to the flat walls.
    if beta == 0:
        # This is the angle between the billiard's path and the inward normal.
        # Since beta is zero, the direction between the path's line and the
        # inward normal is just the inward normal's angle.
        alpha = math.acos(x1 - halfLam)
        # Check if the billiard is traveling towards the upper right cap.
        if y > 0:
            # To get the new direction of the billiard we use the
            # direction of the inward normal and rotate it ccw by alpha.
            beta1 = math.pi + math.asin(y1) + alpha
        # Check if the billiard is traveling towards the lower right cap.
        elif y < 0:
            # To get the new direction of the billiard we use the direction
            # of the inward normal and rotate it clockwise by alpha.
            beta1 = math.pi + math.asin(y1) - alpha
        # Notice that we don't have to consider the case where y=0 because it 
        # is handled in the first if statement of this function.
        # Return the new point in the collision space.
        return (x1, y1, mod2pi(beta1))
    
    # Check if the billiard is traveling from right to left.
    if beta == math.pi:
        # Find the angle between the billiard's path and the inward normal.
        alpha = math.acos(-(x1 + halfLam))
        # Check if the billiard is traveling towards the upper left cap.
        if y > 0:
            # To get the new direction of the billiard take the inward normal's
            # direction and rotate if clockwise by alpha.
            beta1 = 2*math.pi - math.asin(y1) - alpha
        # Check if the billiard is traveling towards the lower left cap.
        if y < 0:
            beta1 = -math.asin(y1) + alpha
        # Return the new point in the collision space.
        return (x1, y1, mod2pi(beta1))
############################################################END horizontalPath

    
def verticalPath(x,y,beta):
    """ This function calculates the next collision for a particle traveling
        in a purely vertical direction.
    """
    # The x-value will remain unchanged.
    x1 = x
    y1 = -y
    # See if the billiard is in the left cap.
    if x < -halfLam:
        # See if the billiard is moving up.
        if abs(beta - math.pi/2) < delta:
            # This gives the polar angle with respect to the circle's origin
            # of the new collision point.
            thetahat = math.acos(x1 + halfLam)
            # This gives the new direction of the billiard. This formula was
            # derived using basic geometry and the fact that the previous path
            # was parallel with the y-axis (which allowed for simplifications)
            beta1 = mod2pi(math.pi + 2*thetahat)
        # See if the billiard is moving down
        if abs(beta == 3*math.pi/2) < delta:
            thetahat = 2*math.pi - math.acos(x1 + halfLam)
            beta1 = mod2pi(2*thetahat - 5*math.pi/2)
        return (x1, y1, mod2pi(beta1))
    
    # See if the billiard is traveling between flat walls
    if x <= halfLam:
        # See if the billiard is traveling towards the upper side. If so it
        # will just be reflected back to where it came from.
        if abs(beta - math.pi/2) < delta:
            beta1 = 3*math.pi/2
        else:
            beta1 = math.pi/2
        return (x1, y1, mod2pi(beta1))
    
    # See if the billiard is in the right cap
    else:
        if abs(beta - math.pi/2) < delta:
            thetahat = math.acos(x1 - halfLam)
            beta1 = mod2pi(math.pi/2 + 2*thetahat)
        elif abs(beta == 3*math.pi/2) < delta:
            thetahat = 2*math.pi - math.acos(x1 - halfLam)
            beta1 = mod2pi(2*thetahat - 5*math.pi/2)
        return (x1, y1, mod2pi(beta1))
    
###############################################################END verticalPath  
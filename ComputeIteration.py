# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 14:08:19 2018

Functions for taking a range of theta-phi values and producting images of these
sets for display on the sphere. We use image in the sense of the image of a set
under a function. Uses pointSampling, coordinateConversion, and 
BilliardCollisions_VectorEq.

@author: Randy
"""
from PointSampling import evenSpacingSample
from PointSampling import randomSample
from CoordinateConversion import thetaphiTOxybeta
from CoordinateConversion import xybetaTOthetaphi
from CollisionMap import collisionLoop

def image_const_theta(philow, phihigh, samples, theta, iterations, lam, \
                      sampleType):
    """ low        := the lower bound of the desired range of phi values.
        high       := the upper bound of the desired range of phi values.
        num        := the number of desired phi values.
        theta      := the the theta value for each point.
        iterations := the number of iterations desired.
        lam        := the parameter that characherizes a Bunimovich Stadium.
        sampleType := specifies the sampling technique to be used.
                      'even' for evenly spaced, 'random' for uniform random.
        Uses evenly spaced samples for now... Theta is constant, only
        phi varies. The range for phi is [low, high].
    """
    if sampleType == 'even':
        # Get evenly spaced phi values
        phiArray = evenSpacingSample(philow, phihigh, samples)
    elif sampleType == 'random':
        phiArray = randomSample(philow, phihigh, samples)
    images = []
    # store the cartesian coodinates of the trajectories
    cartesianImages = []
    # build an list of lists. The inner list is the collision points on 
    # iteration i. the outer list is a list of iterations.
    for k in range(iterations):
        images.append([])
    for i in range(samples):
        phi = phiArray[i]
        # Get the cartesian values associated with the theta-phi pair
        (x, y, beta) = thetaphiTOxybeta(theta, phi, lam)
        # Iterate collisions using (x, y, beta) as seeds.
        # This returns the trajectory of (x,y,beta)
        points = collisionLoop(x, y, beta, iterations, lam)
        # Store this trajectory in cartesianImages
        cartesianImages.append(points)
        # Convert each point in the trajectory into a theta-phi pair.
        for j in range(iterations):
            (xi, yi, betai) = points[j]
            # Convert the point and store its associated theta-phi pair as
            # the j^th collision in the trajectory of the i^th sampled point.
            # each point is stored as a theta phi pair.
#            print "(i,j) = (" + str(i) + "," + str(j) + ")"
            images[j].append(xybetaTOthetaphi(xi, yi, betai, lam))
    
    return images,cartesianImages   

def image_const_phi(thetalow, thetahigh, samples, phi, iterations, lam, \
                    sampleType):
    """ low        := the lower bound of the desired range of theta values.
        high       := the upper bound of the desired range of theta values.
        sample     := the number of desired theta values.
        phi        := the the phi value for each point.
        iterations := the number of iterations desired.
        lam        := the parameter that characherizes a Bunimovich Stadium.
        sampleType := specifies the sampling technique to be used.
                      'e' for evenly spaced, 'u' for uniform random.
        The range for phi is [low, high].
    """
    if sampleType == 'even':
        # Get evenly spaced theta values
        thetaarray = evenSpacingSample(thetalow, thetahigh, samples)
    elif sampleType == 'random':
        thetaarray = randomSample(thetalow, thetahigh, samples)
    images = []
    # This will store the cartesian coodinates of the trajectories
    cartesianImages = []
    # build an list of lists. The inner list is the collision points on 
    # iteration i. the outer list is a list of iterations.
    for k in range(iterations):
        images.append([])
    for i in range(samples):
        theta = thetaarray[i]
        # get the cartesian values associated with this theta-phi pair
        (x, y, beta) = thetaphiTOxybeta(theta, phi, lam)
        # Iterate collisions using (x, y, beta) as seeds.
        # This returns the trajectory of (x,y,beta)
        points = collisionLoop(x, y, beta, iterations, lam)
        # Store this trajectory in cartesianImages
        cartesianImages.append(points)
        # Convert each point in the trajectory into a theta-phi pair.
        for j in range(iterations):
            (xi, yi, betai) = points[j]
            # Convert the point and store its associated theta-phi pair as
            # the j^th collision in the trajectory of the i^th sampled point.
            # each point is stored as a theta phi pair.
            images[j].append(xybetaTOthetaphi(xi, yi, betai, lam))
    
    return images,cartesianImages
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 22:48:10 2019
This file hold all the the text for messages displayed in the Bunimovich Stadia
Evolution GUI
@author: Randy
"""

TEXT = """
Welcome to the Bunimovich Stadia Evolution Viewer. What follows is a description and tutorial for this software. It is assumed that the user is familiar with the Bunimovich stadium billiard and its properties. This software allows the user to view trajectories of nearby collision points under iteration of the stadia's collision map. 

Points in the collsion space are of the form (theta, phi). Theta is a parameter for the arclength of the stadia in the range [0,2pi]. Phi is the angle that the billiard's post-collisional velocity vector makes with the inward normal vector at theta on the boundary. Phi is in the range (-pi/2, pi/2)

This software allows users to specify a set of 'close' collision points and see how their relationship to each other evolves over a desired number of iterations of the collision map. These 'close' collision points all have the same theta or phi value while the other (phi or theta respectively) is allowed to vary in a specified range. With in this range a specified number of collision points are sampled. These points are then passed into the collision map and the desired number of iterations are computed. The trajectories computed are then displayed to the user.

HOW TO USE THIS SOFTWARE:
    
The top drop down menu, labeled "constant variable", allows the user to specify which variable will be held constant for all 'close' points. The variable selected will have the constant value specified in the text entry box labeled "Value of Constant Variable". The variable that is not selected will be the one that is allowed to vary.

The first text entry box, labeled "Value of Constant Variable", allows the user to specify the constant variable's value. The value must be in the appropriate range specified above (0 <= theta <= 2pi) and (-pi/2 < phi < pi/2). 

The second text box, labeled "Mean Value of Sampled Variable", allows the user to specify a value to be the middle of the range for the variable allowed to vary.

The second drop down menu, labeled "Sampled Variable Range", allows the user to specify the range of the varying variable. For example, if pi/4 is picked and the mean value specified for the variable is is 0.785 then points will be sampled in the range [0.785 - pi/4, 0.785 + pi/4].

The third drop down menu, labeled "Number of samples", allows the user to specify the number of samples to be used in the computations.

The fourth drop down menu, labeled "Sampling Method", allows the user to specify how the samples are selected. "even" yeilds evely spaced samples in the specified interval while "random" selects points randomly.

The fifth drop down menu, labeled "Number of iterations", allows the user to specify the number of iterations of the collsion map to be computed.

The sixth drop down menu, labeled "First iteration to display", allows the user to specify the first iteration to be displayed. The iteration selected and those between this one and the last are all displayed. For example if "Number of Iterations" is set to 10 and "First Iteration to Display" is set to 4 then pictures of the output for iterations 4-10 will be displayed. Notice that the first iteration to display must be less than the number of iterations.

At the bottom is a button. Once all fields are correctly filled in click this button to generate the visual data.

For additional questions email shoemarw@dukes.jmu.edu and include "Bunimovich Stadia Evolution GUI" in the subject line.
""" 

ITERMESSAGE = """
ILLEGAL INPUT DETECTED

The first iteration must be less than the number of iterations!

Please Fix this.
"""

THETAMESSAGE = """
ILLEGAL INPUT DETECTED

The range of theta values must be in [0,2pi)!
    
So the mean theta value +- the range must be within [0,2pi) but the range entered is not with in [0,2pi).
    
Please fix this.
"""

PHIMESSAGE1 = """
ILLEGAL INPUT DETECTED

It must be the case that -pi/2 < phi < pi/2 but phi is outside of this range.

Please fix this.
"""

PHIMESSAGE2 = """
ILLEGAL INPUT DETECTED

The range of phi values must be in (-pi/2, pi/2)!

So the mean phi value +- the range must be within (-pi/2,pi/2) but the range entered is not with in (-pi/2,pi/2).

Please fix this.
"""
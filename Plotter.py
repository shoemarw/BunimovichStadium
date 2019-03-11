# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 12:42:50 2019
This code is used by the Bunimovich Stadia Evolution Viewer GUI to do plotting.
It produces plots in the cylindrical, spherical, and stadia views. Uses 
ComputeIteration.py
@author: Randy
"""

import gc
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import matplotlib.patches as mpatches
from mpl_toolkits import mplot3d
from ComputeIteration import image_const_phi
from ComputeIteration import image_const_theta
import math
import numpy as np

def plotter(const, samples, sampleParamLow, sampleParamHi, param, \
                    iterations, start, lam, sampleType, plotType):
    """ const          := is 'phi' (constant phi) xor 'theta' (constant theta).
        samples        := the number of samples of the parameter to be varied.
        sampleParamLow := lower bound for sampled values of the varied param.
        sampleParamHi  := upper bound for sampled values of the varied param.
        param          := the value of the constant parameter.
        iterations     := the number of iterations of the collision map.
        lam            := the ration of the stadias side to radius.
        sampleType     := the type of technique to use for sampling.
                          'even' for evenly spaced
                          'random' for uniformly random
        plotType       := which type of plot(s) is/are to be produced.
                       possible values:
                           'c'   for cylinder view only
                           's'   for spherical view only
                           'b'   for Bunimovich stadia view only
                           'cs'  for cylinder and spherical views
                           'cb'  for cylinder and stadia views
                           'sb'  for spherical and stadia views
                           'csb' for all three views
                           
    """
    pi = math.pi # We can always use some pi!
    
    ## Generate the data to be used in all plot views ##
    if const == 'phi':
        # the constant parameter is phi, the varied parameter is theta.
        var = 'theta'
        images, cartesianImage = image_const_phi(sampleParamLow, \
                sampleParamHi, samples, param, iterations,  lam, sampleType)
                                            
    elif const == 'theta':
        # the constant parameter is theta, the varied parameter is phi.
        var = 'phi'
        images, cartesianImage = image_const_theta(sampleParamLow, \
                sampleParamHi, samples, param, iterations,  lam, sampleType)
    else:
        print "Invalid constant parameter."
    
    print "Computation finished, preparing image..."
    
    ## Create a string to uniquely name the output pdf ##
    name = "const_" + const + "_" + str(param) + "_samples_" + str(samples) + \
           "_" + var + "_" + str(sampleParamLow) + "to" + str(sampleParamHi)
    name = "_" + name + "iters_" + str(iterations) + "_sType_" + sampleType
    
## ---------------------- CYLINDER VIEW ------------------------------ ##
    # Check if the cylinder view is to be presented.
    if "c" in plotType:
        # Create a pdf for output
        ppC = PdfPages("cylinder" + name + ".pdf")
        # Proceed to present the cylinder view.
        for iteration in range(start ,iterations):
            fig = plt.figure(figsize=(6,4))
            ax = plt.subplot(111)
            plt.suptitle("Iteration " + str(iteration), fontsize=16)
            
            ax.yaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
            ax.yaxis.set_major_locator(tck.MultipleLocator(base=1.0))
            ax.xaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
            ax.xaxis.set_major_locator(tck.MultipleLocator(base=1.0))
            
            ax.set_xlim([-0.01, 2])
            ax.set_ylim([0, 1])
            ax.plot(0, 0, ms=0)
            
            points = images[iteration]
            # Go through the points plotting them as we go
            for i in range(1,samples):
                dist = abs(points[i-1][0] - points[i][0])
                # See if the regular distance is shorter than the compliment of
                # the distances.
                if dist < (2*pi - dist):
                    # "no wrapping"
                    # The points must be plotted normally
                    x = [points[i-1][0]/pi, points[i][0]/pi]
                    y = [(points[i-1][1] + pi/2)/pi, (points[i][1] + pi/2)/pi]
                    plt.plot(x, y)#33333333333333333333333333333333333333333333333
                else:
                    # "wrapping"
                    # The points must be plotted so that the line between them
                    # goes the "other way" around the cylinder.
                    # Get the average of the two psi values of the points.
                    # Then shift up by pi/2 to turn the phi value into a psi
                    # value.
                    psiaverage = (points[i-1][1] + points[i][1])/2 + pi/2
                    # Figure out which point has a higher theta value
                    if points[i-1][0] < points[i][0]:
    
                        #p_i has a higher theta value, it must be connected to
                        #(2pi, psiaverage)
                        x = [points[i][0]/pi, 2]
                        y = [(points[i][1] + pi/2)/pi, psiaverage/pi]
                        plt.plot(x, y)################################################
                        #p_i-1 has a lower theta value, it must be connected to
                        #(0, psiaverage)
                        x = [0, points[i-1][0]/pi]
                        y = [psiaverage/pi, (points[i-1][1] + pi/2)/pi]
                        plt.plot(x, y)############################################
                    else:
                        #p_i has a lower theta value so it must be connected to
                        #(0, psiaverage)
                        x = [0, points[i][0]/pi]
                        y = [psiaverage/pi, (points[i][1] + pi/2)/pi]
                        plt.plot(x, y)##################################################
                        #p_i-1 has a higher theta value,it must be connected to
                        #(2pi, psiaverage)
                        x = [points[i-1][0]/pi, 2]
                        y = [(points[i-1][1] + pi/2)/pi, psiaverage/pi]
                        plt.plot(x, y)################################################# 'r'
            ppC.savefig(fig)
            plt.close(fig)
            gc.collect()
        ppC.close()
        print "Cylinder Plotting Complete"

## ---------------------- STADIA VIEW ------------------------------ ##       
    if "b" in plotType:
        # Create a pdf for output
        ppB = PdfPages("stadia" + name + ".pdf")
        # Proceed to present the stadia view.
        fig = plt.figure(figsize=(6,4))
        x1, y1 = [-1, 1], [1, 1]
        x2, y2 = [-1, 1], [-1, -1]
        plt.plot(x1, y1, c='b')
        plt.plot(x2, y2, c='b')
        
        ax = plt.subplot(111)
        rightCap = mpatches.Wedge((1, 0), 1, -90, 90, width=.015, fc='b')
        leftCap = mpatches.Wedge((-1, 0), 1, 90, -90, width=.015, fc='b')
        
        ax.plot(0, 0, ms=0)
        ax.add_artist(rightCap)
        ax.add_artist(leftCap)
    
        ax.set_xlim([-2.1, 2.1])
        ax.set_ylim([-1.5, 1.5])
        ax.plot(0, 0, ms=0)
        
        for iteration in range(start, iterations):
            fig = plt.figure(figsize=(6,4))
            x1, y1 = [-1, 1], [1, 1]
            x2, y2 = [-1, 1], [-1, -1]
            plt.plot(x1, y1, c='b')
            plt.plot(x2, y2, c='b')
            plt.suptitle("Iteration " + str(iteration), fontsize=16)
            
            ax = plt.subplot(111)
            rightCap = mpatches.Wedge((1, 0), 1, -90, 90, width=.015, fc='b')
            leftCap = mpatches.Wedge((-1, 0), 1, 90, -90, width=.015, fc='b')
            
            ax.plot(0, 0, ms=0)
            ax.add_artist(rightCap)
            ax.add_artist(leftCap)
        
            ax.set_xlim([-2.1, 2.1])
            ax.set_ylim([-1.5, 1.5])
            ax.plot(0, 0, ms=0)
            for sample in range(samples):
                x = [cartesianImage[sample][iteration][0], \
                     cartesianImage[sample][iteration+1][0]]
                y = [cartesianImage[sample][iteration][1], \
                     cartesianImage[sample][iteration+1][1]]
                print 'x = ' + str(x)
                print 'y = ' + str(y)
                plt.arrow(x[0], y[0], (x[1]-x[0]), (y[1]-y[0]), color = 'r', \
                    length_includes_head = True, shape='full', head_width=.05)
            ppB.savefig(fig)
        #    plt.close(fig)
        #    gc.collect()
        ppB.close()
        print "Stadia Plotting Complete."
            
## ---------------------- SPHERICAL VIEW ------------------------------ ##
    if "s" in plotType:
        # Create a sphere
        ppS = PdfPages("sphere" + name + ".pdf")
        r = 1
        pi = np.pi
        cos = np.cos
        sin = np.sin
        phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0*pi:100j]
        xxx = r*sin(phi)*cos(theta)
        yyy = r*sin(phi)*sin(theta)
        zzz = r*cos(phi)
        
        for iteration in range(start ,iterations):
            points = images[iteration]
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
    
            ax.plot_surface(xxx, yyy, zzz,  rstride=1, cstride=1, color='c', \
                            alpha=0.3, linewidth=0)
            # Go through the points plotting them as we go
            for i in range(1,samples):
                # Get the theta and phi values
                theta_im1 = points[i-1][0]
                theta_i   = points[i][0]
                phi_im1   = points[i-1][1] + pi/2
                phi_i     = points[i][1] + pi/2
                # Calculate the 3d Cartesian values corresponding to the
                # theta phi values.
                xx_im1    = math.sin(phi_im1)*math.cos(theta_im1)
                xx_i      = math.sin(phi_i)*math.cos(theta_i)
                yy_im1    = math.sin(phi_im1)*math.sin(theta_im1)
                yy_i      = math.sin(phi_i)*math.sin(theta_i)
                zz_im1    = math.cos(phi_im1)
                zz_i      = math.cos(phi_i)
                
                dist = abs(points[i-1][0] - points[i][0])
                # See if the regular distance is shorter than the compliment of
                # the distances.
                if dist < (2*pi - dist):
                    # "no wrapping"
                    # The points must be plotted normally
                    x = [xx_im1, xx_i]
                    y = [yy_im1, yy_i]
                    z = [zz_im1, zz_i]
                    ax.plot3D(x,y,z)
                else:
                    # "wrapping"
                    # The points must be plotted so that the line between them
                    # goes the "other way" around the cylinder.
                    # Get the average of the two psi values of the points.
                    # Create an intermediate point to prevent wrapping it
                    # has a theta value of 0.
                    phiaverage = (points[i-1][1] + points[i][1])/2 + pi/2
                    xx0 = math.sin(phiaverage)
                    yy0 = 0
                    zz0 = math.cos(phiaverage)
                    
                    # Connect p_i-1 to xx0 and plot
                    x = [xx_im1, xx0]
                    y = [yy_im1, yy0]
                    z = [zz_im1, zz0]
                    ax.plot3D(x,y,z)
                    
                    # Connect p_i to xx0 and plot
                    x = [xx_i, xx0]
                    y = [yy_i, yy0]
                    z = [zz_i, zz0]
                    ax.plot3D(x,y,z)
    
            ax.set_xlim([-1,1])
            ax.set_ylim([-1,1])
            ax.set_zlim([-1,1])
            ax.set_aspect("equal")
            plt.tight_layout()
            ppS.savefig(fig)
            plt.close(fig)
            gc.collect()
        ppS.close()           
        print "Spherical Plotting Complete"
    return 1
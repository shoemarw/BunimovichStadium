# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 12:58:30 2018

Handles sampling given numerical ranges.

@author: Randy
"""
import numpy as np

def evenSpacingSample(low, high, num):
    """ Samples evenly spaced points in the interval [low, high].
        Returns num number of evenly spaced points in [low, high].
        USES NUMPY.
    """
    return np.arange(low, high, (high-low)/float(num)).tolist()

def randomSample(low, high, num):
    """ 'Randomly' samples points in the interval [low, high].
        Returns num # of randomly sampled points in [low, high].
        USES NUMPY
    """
    # generate num random numbers between 0 and 1.
    sample = np.random.rand(num)
    # find the range of numbers
    rangee = high - low
    # scale every number in the array by rangee
    sample = rangee*sample
    # shift the array of numbers into the interval [low, high]
    sample = sample + low
    sample = sample.tolist()
    sample.sort()
    return sample
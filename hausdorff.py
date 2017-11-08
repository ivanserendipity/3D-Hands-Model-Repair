#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:19:22 2017

@author: Serendipity
"""
from scipy.spatial.distance import directed_hausdorff
import numpy as np

def total_Square_Error(a,b):
    
    t_err = 0
    for j in range(len(a)):
        error = 100.0
        for i in range(len(b)):
            cur_target = b[i]
            tar_x = cur_target[0]
            tar_y = cur_target[1]
            tar_z = cur_target[2]
    
            cur_err = np.square(a[j][0]-tar_x) + np.square(a[j][1]-tar_y) + np.square(a[j][2]-tar_z)
            
            if error > cur_err:
                error = cur_err
        
        t_err += error
    
    return t_err
    
def hausdorff_err(a,b):
    return directed_hausdorff(a,b)[0]
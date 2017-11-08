#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 15:45:20 2017

@author: Serendipity
"""

import numpy as np

def cal_loss(ori,predt,index):
    loss = 0.0
    
    for i in range(0,len(index)-2,3):
        cur_loss = np.square(ori[index[i]] - predt[index[i]]) + np.square(ori[index[i+1]] - predt[index[i+1]]) + np.square(ori[index[i+2]] - predt[index[i+2]])
        
        loss += cur_loss
        
    return loss
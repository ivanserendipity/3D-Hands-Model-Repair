#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 16:16:45 2017

@author: Serendipity
"""

import numpy as np
import re
import sys

def write_m(points,faces,vert_dict,filepath):
    wfile = open(filepath,'w')
    
    for i in range(0,len(points) - 2,3):
        if(points[i] != 0 or points[i+1] != 0 or points[i+2] != 0):
            for fake_ind, real_ind in vert_dict.items():
                if int(real_ind) == int((i+3)/3):
                    p1 = "%.64f" % points[i]
                    p2 = "%.64f" % points[i+1]
                    p3 = "%.64f" % points[i+2]
                    wfile.write("Vertex %d  %e %e %e\n" % (fake_ind,float(p1.rstrip("0")),float(p2.rstrip("0")),float(p3.rstrip("0"))))
        
    count = 1
    
    for row in range(0,len(faces)):
            if(faces[row][0] != -1):
                wfile.write("Face %d  %d %d %d\n" % (count,faces[row][0],faces[row][1],faces[row][2]))
                count = count + 1

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 20:35:58 2017

@author: Serendipity
"""

import random
import numpy as np

def random_holes(points,faces,vert_dict,rate):
    np.random.seed(55)
    num_holes = int((len(points[0])/3) * rate)
    print num_holes
    rm_verts = np.zeros((num_holes,2))
    rm_verts.astype(int)
    
    #define a array for generating random num
    ran_num_pool = np.arange(1238).tolist()
    
    for i in range(0,num_holes):
        random_index = ran_num_pool[random.randint(0,len(ran_num_pool) - 1)]
        
        for fake_ind,real_ind in vert_dict.items():
            if(real_ind == random_index):
                rm_verts[i][0] = int(real_ind)
                rm_verts[i][1] = int(fake_ind)
                ran_num_pool.remove(random_index)
    
    for row in range(0,len(points)):
        for i in range(0,len(rm_verts)):
            vert_ind = int(rm_verts[i][0])
            points[row][vert_ind*3 - 3] = 0
            points[row][vert_ind*3 - 2] = 0
            points[row][vert_ind*3 - 1] = 0


    for row in range(0,len(faces)):
            row_del = False
            for tar in range(0,len(rm_verts)):
                if(int(faces[row][0]) == int(rm_verts[tar][1]) or int(faces[row][1]) == int(rm_verts[tar][1]) or int(faces[row][2]) == int(rm_verts[tar][1])):
                    faces[row][0] = -1
                    faces[row][1] = -1
                    faces[row][2] = -1
                    row_del = True
                    break
        

    return points,faces
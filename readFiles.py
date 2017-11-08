#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 09:50:12 2017

@author: Serendipity
"""

import glob
import re
import numpy as np

#read original datasets from directory
def read_m_files(path):
    files = glob.glob(path+"/*/Parts__1.m")

    row = len(files)
    col = 0
    with open(files[0]) as f:
        lines = f.readlines()
        col = len(lines)
    
    vertexes = np.zeros(shape=(row,col*3))
    
    for i in range(0,len(files)):
        cur_file = open(files[i],'r')
        
        lines = cur_file.readlines()
        index = 0
        for line in lines:
            strs = line.split()
            vertexes[i][index] = float(strs[2])
            vertexes[i][index+1] = float(strs[3])
            vertexes[i][index+2] = float(strs[4])
            index = index + 3
    
    
    return vertexes

#read single m file
def read_m_file(path):
    f = open(path,'r')
    
    row = 0
    lines = f.readlines()
    
    for line in lines:
        strs = line.split()
        if(strs[0] == 'Vertex'):
            row = row + 1
        else:
            break
    
    points = np.zeros(shape=(row,3))
    count = 0
    for line in lines:
        strs = line.split()
        if(strs[0] == 'Vertex'):
            points[count][0] = float(strs[2])
            points[count][1] = float(strs[3])
            points[count][2] = float(strs[4])
            count = count + 1
        else:
            break
        
    return points

#read m file with a hole

def read_hole_m(fpath,vert_dict,point):
    
    f = open(fpath)
    
    lines = f.readlines()
    
    for i in range(len(point)):
        point[i] = 0
    
    for line in lines:
        strs = line.split()
        
        if(strs[0] == 'Vertex'):
            index = vert_dict[int(strs[1])]
            index = (index-1)*3
            point[index] = float(strs[2])
            point[index+1] = float(strs[3])
            point[index+2] = float(strs[4])
    
    return point

#read faces    
def read_face(path):
    f = open(path,'r')
    vert_dict = {}
    lines = f.readlines()
    face_nums = 0
    for line in lines:
        strs = line.split()
        
        if(strs[0] == 'Face'):
            face_nums = face_nums + 1
    
    
    faces = np.zeros((face_nums,3))
    faces = faces.astype(int)
    index = 0
    count = 1
    for line in lines:
        strs = line.split()
        if(strs[0] == 'Vertex'):
            vert_dict[int(strs[1])] = count
            count = count + 1
            
            
        if(strs[0] == 'Face'):
            faces[index][0] = int(strs[2])
            faces[index][1] = int(strs[3])
            faces[index][2] = int(strs[4])
            index = index+1
    
    return faces,vert_dict

      
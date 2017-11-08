#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:27:41 2017

@author: Serendipity
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


import tensorflow as tf
from random_holes_generator import random_holes
from m_writer import write_m
from readFiles import read_m_files,read_face,read_hole_m
from loss_calculator import cal_loss



#Gradient Descent parameters
steps = 1000
learning_rate = 0.001
    
m_file_dir = "/Users/Serendipity/Documents/master_project/human_body_data/male/SPRING_MALE_m_edges/"

face_path = "/Users/Serendipity/Documents/master_project/human_body_data/obj_m_edges/SPRING0001/Parts__1.m"

m_input_path = "/Users/Serendipity/Desktop/min_test_data/1023/2302_continous.m"
m_output_path = "/Users/Serendipity/Desktop/min_test_data/1023/min_2301_continous.m"


datas = read_m_files(m_file_dir)

datas_test = np.copy(datas[0:300])

datas_hole = np.copy(datas[0:300])

datas_train = np.copy(datas[300:])

faces,vert_dict = read_face(face_path)

ori_faces = list(faces)

pca = PCA(400)

T = pca.fit_transform(datas_train)


hole_point = read_hole_m(m_input_path,vert_dict,datas_hole[0])
hole_face,_= read_face(m_input_path)

print 'pca ok \n'

#random holes generate

'''
datas_hole,faces = random_holes(datas_hole.tolist(),faces.tolist(),vert_dict,0.63)


m_path = "/Users/Serendipity/Desktop/min_test_data/1023/2302_continuous.m"
write_m(datas_hole[0],faces,vert_dict,m_path)
'''

# remove 0 from datas[0]

indices = [] #remain the index that has not been removed

hole_index = [] # record index that has been removed

data_reduce = list(hole_point)
for ind in range(len(hole_point)):
    if(hole_point[ind] == 0):
        data_reduce.remove(0)
        hole_index.append(ind)
    else:
        indices.append(ind)

        
X = tf.Variable(np.random.rand(1,400).astype(np.float32),name = 'X')
Y_True = tf.constant(np.asarray(data_reduce).astype(np.float32))

print 'Variable X is created\n'

sess = tf.Session()

# pca components for inverse
C = tf.constant(pca.components_.astype(np.float32))

M = tf.constant(pca.mean_.astype(np.float32))

#pre-process Y_Test
Y_Test = tf.add(tf.matmul(X,C),M)

Y_Test = tf.reshape(Y_Test,[3714,])

Y_Test = tf.gather(Y_Test,indices)

#loss function
loss = tf.reduce_sum(tf.square(Y_True - Y_Test))

print 'Loss function defined\n'

optimizer = tf.train.GradientDescentOptimizer(learning_rate)

print 'Optimizer defined\n'

train_x = optimizer.minimize(loss)

print 'train_x \n'

init_op = tf.global_variables_initializer()

sess.run(init_op)

for n in range(steps):
    _,x_val = sess.run([train_x,X])
    
    if( n % 500 == 0):
        print 'Iterator : %i, loss: %f' %(n+1,sess.run(loss))



res = np.asarray(pca.inverse_transform(x_val))[0]

wfile = open(m_output_path,'w')

count = 1

for i in range(0,len(res) - 2,3):
    for fake_ind, real_ind in vert_dict.items():
                if int(real_ind) == int((i+3)/3):
                    wfile.write("Vertex %d  %e %e %e\n" % (fake_ind,res[i],res[i+1],res[i+2]))


for f_r in range(0,len(ori_faces)):
        wfile.write("Face %d  %d %d %d\n" % (count,ori_faces[f_r][0],ori_faces[f_r][1],ori_faces[f_r][2]))
        count = count + 1
        
wfile.flush()
wfile.close()

print 'Total loss is %f' %(cal_loss(datas_test[0],res,hole_index))
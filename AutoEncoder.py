#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 19:04:28 2017

@author: Serendipity
"""

import tensorflow as tf
import numpy as np


learning_rate = 0.001
steps = 30000

hidden_layer1 = 100

#hidden_layer2 = 200

input_size = 400

X = tf.placeholder("float",[None,input_size])

encoder_weights = {
           'encoder_h1':tf.Variable(tf.random_normal([input_size,hidden_layer1])),
           # 'encoder_h2':tf.Variable(tf.random_normal([hidden_layer1,hidden_layer2])),
           }
           
decoder_weights = {
                   #'decoder_h1':tf.Variable(tf.random_normal([hidden_layer2,hidden_layer1])),
                    'decoder_h2':tf.Variable(tf.random_normal([hidden_layer1,input_size])),
}

encoder_bias = {
                'encoder_b1':tf.Variable(tf.random_normal([hidden_layer1])),
                #'encoder_b2':tf.Variable(tf.random_normal([hidden_layer2])),
                }
                
decoder_bias = {
                #'decoder_b1':tf.Variable(tf.random_normal([hidden_layer1])),
                'decoder_b2':tf.Variable(tf.random_normal([input_size])),
                }

def encoder(x):
    layer_1 = tf.nn.tanh(tf.add(tf.matmul(x,encoder_weights['encoder_h1']),
                                   encoder_bias['encoder_b1']))
    
    #layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1,encoder_weights['encoder_h2']),encoder_bias['encoder_b2']))
    return layer_1

def decoder(x):
    layer_1 = tf.nn.tanh(tf.add(tf.matmul(x,decoder_weights['decoder_h2']),
                                   decoder_bias['decoder_b2']))
    
    #layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1,decoder_weights['decoder_h2']),decoder_bias['decoder_b2']))
    
    return layer_1

encoder_op = encoder(X)
decoder_op = decoder(encoder_op)

y_pred = decoder_op
y_true = X

loss = tf.reduce_mean(tf.square(y_true - y_pred))
optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(loss)

init = tf.global_variables_initializer()

def train(data):
    with tf.Session() as sess:
        sess.run(init)
        
        for i in range(0,steps):
            
            _,l = sess.run([optimizer,loss],feed_dict = {X:data})
            
            if i % 500 == 0 :
                print('Step %i:Minibatch loss: %f' % (i,l))
        
        saver = tf.train.Saver()
        save_path = saver.save(sess,'/Users/Serendipity/Documents/master_project/tf_model/ae_l2.ckpt')
        print("Model saved in file: %s" % save_path)
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 19:05:57 2021

@author: erri


Questo script analizza le immagini di differenza di saturazione e calcola,
impostate le soglie per di attività per monte e valle, il rapporto W_Active/W
nello spazio e nel tempo 
"""
# Import libraries
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Set working directory and run parameters
run = 'q20_2rgm2'
dt = 1 # set dt between photos [min]
chart_name = 'Q=2.0 l/s'
w_dir = os.getcwd() # Set Python script location as w_dir
path_in = os.path.join(w_dir, 'input_images', run)
path_out = os.path.join(w_dir, 'output_images', run)

# Set directory
if os.path.exists(path_in):
    pass
else:
    os.mkdir(path_in)
    
if os.path.exists(path_out):
    pass
else:
    os.mkdir(path_out)

# List file in input images directory
filenames = os.listdir(path_in)

# Set differencing value treshold 
thr_up = 8
thr_dwn = 14

#Set flume Width [mm]
W = 600

# Set pixel dimension [mm]
px = 0.96

active_W = []
active_W_percentuale = []

fig1, ax1 = plt.subplots()
fig1.set_dpi(300)
ax1.set_title('Wactive/W [-]'+ chart_name) #'+run)
ax1.set_xlabel('Coordinata longitudinale [m]')
ax1.set_ylim(0,1.1)
ax1.set_ylabel('Wactive/W [-]')

for filename in sorted(filenames):
    path = os.path.join(path_in, filename) # Build path
    if os.path.isfile(path): # If filename is a file (and not a folder)
        img = Image.open(path) # Set image
        np_img = np.array(img) # Convert image in np.array
        # Set different threshold for upstream and downstraem images
        if filename.endswith('cropped0.png'): # Upstream image
            thr = thr_up
        elif filename.endswith('cropped1.png'): # Downstream image
            thr = thr_dwn
        active_img = np_img>=thr # Create map with values >= thr
        dim_x, dim_y = np_img.shape
        cross_section = np.zeros(dim_y) # Initialize vector
        
        for i in range (0,dim_y):
            cross_section[i]=np.count_nonzero(active_img[:,i])
        #print(np.mean(cross_section))
        active_W = np.append(active_W, np.mean(cross_section))  
        active_W_perc = (np.mean(cross_section)*px/W)*100
        active_W_percentuale = np.append(active_W_percentuale, active_W_perc)
        print(filename, np_img.shape, 'threshold=',thr, 'Active_W=', f"{np.mean(cross_section)*px:.3f}", 'Active_W%', active_W_perc)
        # print(active_W_perc)
        X = np.linspace(0, dim_y, dim_y)
        
        ax1.plot(X*px/1000, cross_section*px/W, lw=0.1)


#Plot Active Width %   
T = np.linspace(0, dt*len(active_W) , len(active_W)) # Time vector
    
fig2, ax = plt.subplots()
fig2.set_dpi(300)
ax.set_title('Wactive/W [-]'+ chart_name) #'+run)
ax.set_xlabel('Tempo [min]')
ax.set_ylabel('Wactive/W ')
ax.plot(T[10:-10], active_W_percentuale[10:-10]/100, marker="o", markersize=2)

print('Active_W%_Mean=',np.mean(active_W_percentuale[10:-10]))
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:24:15 2022

@author: Kellen Cheng
"""

import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import matplotlib.patches as patches

cap = cv2.VideoCapture(0)
first = True
test_frame = None
test_mask = None

while(True):
    # Frame-by-frame
    ret, frame = cap.read()
    
    # Find blue objects in our video feed
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # HSV Color Range for Blue
    # lower_blue = np.array([100,150,20]) # RGB = 17, 51, 0
    # upper_blue = np.array([140,255,255]) # RGB = 0, 255, 85
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # RGB Color Range for Blue
    lower_blue = np.array([17,51,0]) # RGB = 17, 51, 0
    upper_blue = np.array([65,105,225]) # RGB = 0, 255, 85
    mask = cv2.inRange(hsv, np.array([0,0,190]), np.array([140,255,255]))
    
    # Find the maximum contour and draw a rectangle over it
    contour, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    if len(contour) != 0:
        c = max(contour, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
    
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

height, width, dim = frame.shape
img_vec = np.reshape(frame, [height * width, dim] )

kmeans = KMeans(n_clusters=3)
kmeans.fit(img_vec)

# %% KMeans Next Steps
unique_l, counts_l = np.unique(kmeans.labels_, return_counts=True)
sort_ix = np.argsort(counts_l)
sort_ix = sort_ix[::-1]

fig = plt.figure()
ax = fig.add_subplot(111)
x_from = 0.05

for cluster_center in kmeans.cluster_centers_[sort_ix]:
    cluster_center = [int(i) for i in cluster_center]
    ax.add_patch(patches.Rectangle( (x_from, 0.05), 0.29, 0.9, alpha=None,
                                    facecolor='#%02x%02x%02x' % (cluster_center[2], cluster_center[1], cluster_center[0] ) ) )
    x_from = x_from + 0.31

plt.show()


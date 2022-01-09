# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:24:15 2022

@author: Kellen Cheng

Dominant color finding code can be credited towards the following:
https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097

- Functions that are utilized are the same and are pulled from the source
- Altered the pipeline regarding image conversion before Kmeans analysis, such
  that image channels are manually reversed for intuitive sense (line 95)
  
Baseline video feed control loop code can be credited towards the following:
https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/
py_video_display.html

- Overall structure is retained
- Color segmentation capacity is added to track the color range of Blue
- Additionally, the above line method is utilized for both HSV and RGB ranges
- Other changes include adding code that can draw real-time contour boxes around
  the tracked object 
"""

import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import matplotlib.patches as patches

# %% Dominant Color Tutorial Functions
def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

# %% Video Feed Control Loop
cap = cv2.VideoCapture(0)
first = True
test_frame = None
test_mask = None

while(True):
    # Frame-by-frame
    ret, frame = cap.read()
    
    # Find blue objects in our video feed
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # HSV
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # RGB
    
    # HSV Color Range for Blue
    lower_blue = np.array([100,150,20]) # RGB = 17, 51, 0
    upper_blue = np.array([140,255,255]) # RGB = 0, 255, 85
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # RGB Color Range for Blue
    # lower_blue = np.array([17,51,0]) # RGB = 17, 51, 0
    # upper_blue = np.array([65,105,225]) # RGB = 0, 255, 85
    # mask = cv2.inRange(hsv, np.array([0,0,190]), np.array([140,255,255]))
    
    # Find the maximum contour and draw a rectangle over it
    contour, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    # Draw contours on the live frames before displaying
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

# %% Kmeans Dominant Colors
img = frame[..., ::-1] # Reverse the channels to get to RGB

img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
clt = KMeans(n_clusters=5) #cluster number
clt.fit(img)

hist = find_histogram(clt)
bar = plot_colors2(hist, clt.cluster_centers_)

plt.axis("off")
plt.imshow(bar)
plt.show()
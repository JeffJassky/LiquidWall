#!/usr/bin/env python
from __future__ import division
import sys
import time
from Quartz.CoreGraphics import *   # imports all of the top-level symbols in the module
from freenect import sync_get_depth as get_depth
from bisect import insort
from math import sqrt
import numpy as np

zeros = lambda length: [0 for _ in range(length)]
global depth #Makes the depth global

#Sets the size of the sensor
sensorWidth = 640
sensorHeight = 480

#Sets the size of the screen
screenWidth = 800
screenHeight = 600

#Mean filter caches
yList = zeros(10)
xList = zeros(10)
most_recent = (0, 0)

def get_min_pos_kinect_original():
    
    (depth,_) = get_depth()

    # print depth;
    
    minVal = np.min(depth) #This is the minimum value from the depth image
    minPos = np.argmin(depth) #This is the raw index of the minimum value above
    xPos = np.mod(minPos, sensorWidth) #This is the x component of the raw index
    yPos = minPos//sensorWidth #This is the y component of the raw index
        
    xList.append(xPos)
    del xList[0]
    xPos = int(np.mean(xList))
    yList.append(yPos)
    del yList[0]
    yPos = int(np.mean(yList))


    return ((sensorWidth - xPos) * (screenWidth / sensorWidth), yPos * (screenHeight / sensorHeight))


def get_min_pos_kinect():
    (depth,_) = get_depth()
    minPos = np.argmin(depth) #This is the raw index of the minimum value above
    xPos = np.mod(minPos, sensorWidth) #This is the x component of the raw index
    yPos = minPos//sensorWidth #This is the y component of the raw index
    return ((sensorWidth - xPos-10) * (screenWidth / sensorWidth),yPos * (screenHeight / sensorHeight))

def distance_from_last(pos):
    return sqrt((pos[0] - most_recent[0])**2 + (pos[1] - most_recent[1])**2)

def get_min_pos_kinect2():
    global most_recent
    positions = []
    for i in xrange(10):
        handPosition = get_min_pos_kinect()
        insort(positions,(distance_from_last(handPosition), handPosition[0], handPosition[1]))

    positions = positions[:8]  

    xPos = int(np.mean([p[1] for p in positions]))
    yPos = int(np.mean([p[2] for p in positions]))
    most_recent = (xPos, yPos)

    return ((sensorWidth - xPos-10) * (screenWidth / sensorWidth),yPos * (screenHeight / sensorHeight))


def mouseEvent(type, posx, posy):
    theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, theEvent)
def mousemove(posx,posy):
    mouseEvent(kCGEventMouseMoved, posx,posy);
def mouseclickdn(posx,posy):
    mouseEvent(kCGEventLeftMouseDown, posx,posy);
def mouseclickup(posx,posy):
    mouseEvent(kCGEventLeftMouseUp, posx,posy);
def mousedrag(posx,posy):
    mouseEvent(kCGEventLeftMouseDragged, posx,posy);


ourEvent = CGEventCreate(None); 
currentpos=CGEventGetLocation(ourEvent);    # Save current mouse position

time.sleep(5);
mouseclickdn(screenWidth - 10, screenHeight - 10);
while True:
    handPosition = get_min_pos_kinect_original();
    mousedrag(handPosition[0],handPosition[1]);
    print handPosition;

# mouseclickup(60, 300);
# time.sleep(1);

# mousemove(int(currentpos.x),int(currentpos.y)); # Restore mouse position
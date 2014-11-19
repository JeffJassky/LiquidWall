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

movementThreshold = 100;
cacheBufferSize = 10;

#Sets the size of the sensor
sensorWidth = 640
sensorHeight = 480
topMargin = 10
rightMargin = 10
bottomMargin = 10
leftMargin = 10

#Sets the size of the projector
screenWidth = 800
screenHeight = 600

#Don't adjust these
yList = zeros(cacheBufferSize)
xList = zeros(cacheBufferSize)
isMouseDown = false;

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

def getCursorPosition():
    (depth,_) = get_depth()
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
    return ((sensorWidth - xPos) * (screenWidth / sensorWidth), yPos * (screenHeight / sensorHeight));

def getAmountMoved():
    return sqrt((xList[0] - ylist[0])**2 + (cursorPosition[1] - cursorPosition[1])**2)

while True:
    cursorPosition = getCursorPosition();
    amountMoved = getAmountMoved();
    if(amountMoved >= movementThreshold && isMouseDown === false){
        mouseclickdn(cursorPosition[0], cursorPosition[1]);
        isMouseDown = true;
    }else if(amountMoved < movementThreshold && isMouseDown === true){
        mouseclickup(cursorPosition[0], cursorPosition[1]);
        isMouseDown = false;
    }
    if(isMouseDown){
        mousedrag(cursorPosition[0],cursorPosition[1]);
    }
    print cursorPosition;
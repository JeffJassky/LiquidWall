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



pos = (1,2,3,4,5);
print np.mean(pos);
print np.average(pos, weights=range(5,0,-1));
print np.average(pos, weights=range(5,0,-1));


from __future__ import division
import math
from array import array
from physical_constants import *

# Given a body at a point (x, y) in the orbital plane and with
# velocity (vx, vy), and with the star receiving a kick velocity
# kickSpeed, this function assigns a flat-random direction in 3-space
# to the velocity. A tuple (a, e) is returned for the new eccentricity 
# and semi-major axis.

def NewAE(m, x, y, vx, vy, kickSpeed):
	dxk = math.random()
	dyk = math.random()
	dzk = math.random()
	
	r = (x, y, 0)
	rdot = (vx - 

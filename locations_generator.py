from __future__ import division
import math
from array import array

def LocationsGenerator(a, e, m, M):

	# gravitational constant
	G = 6.67 * 10**-11 

	# reduced mass
	mu = (m * M) / (m + M) 

	# total energy
	E = -1 * ((G * M * m) / (2 * a))

	# orbital period
	period = math.sqrt((4 * (math.pi**2) * a**3)/(G * (M + m)))

	# angular momentum per unit mass
	L = math.sqrt(G * M * a * (1 - e**2))

	# number of discrete orbit locations, as a function of e.
	steps = math.floor(1 / (0.07 * (1 - e)))

	# timestep
	dt = period / steps

	output = array()


	# initialize incremental step parameters
	step = 1
	t = 0
	theta = 0
	while step < steps:
		pass

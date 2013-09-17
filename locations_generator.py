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
	dtheta = None
	while step < steps:
		r = (a * (1 - e**2))/(1 + e * math.cos(theta))
		x = r * math.cos(theta)
		y = r * math.sin(theta)
		dx = (a * e * (1 - e**2) * math.cos(theta) * math.sin(theta))/((1 + e * math.cos(theta))**2) - (a * (1 - e**2)) * math.sin(theta) / (1 + e * math.cos(theta))
		dy = (a * e * (1 - e**2) * math.cos(theta))/(1 + e * math.cos(theta)) + (a * e * (1 - e**2) * (math.sin(theta))**2) / (1 + e * (math.cos(theta))**2)
		V = math.sqrt((2/mu) * ((G * m * M) / r + E))
		vx = V/math.sqrt(dx**2 + dy**2) * dx
		vy = V/math.sqrt(dx**2 + dy**2) * dy
		output.append([x, y, vx, vy])
		step += 1
		if (L/(r**2)) * dt < 2:
			dtheta = (L/r**2) * dt
		else:
			dtheta = 2
		theta += dtheta
		t += dt




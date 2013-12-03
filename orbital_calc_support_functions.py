from __future__ import division
from physical_constants import * # includes gravitational constant, G
import math, numpy, scipy
from scipy import stats


# Generates, for a specified two-body orbit, a list of orbital radii and 
# velocites (in the reduced-mass system), where each point is a constant- 
# time away from its predecessor. This list is necessary for random sampling
# because all non-circular orbits have constantly varying radii and velocites,
# and there is no closed-form expression for x(t) and v(t) in the two-body
# problem. This list must be pregenerated for each test orbit.

def LocationsGenerator(a, e, m, M):

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

	output = list()

	# initialize incremental step parameters
	step = 1
	t = 0
	theta = 0
	dtheta = None
	
	# step around the orbital path once.
	while step < steps:
		r = (a * (1 - e**2))/(1 + e * math.cos(theta))
		x = r * math.cos(theta)
		y = r * math.sin(theta)
		dx = (a * e * (1 - e**2) * math.cos(theta) * math.sin(theta))/((1 + e * math.cos(theta))**2) - (a * (1 - e**2)) * math.sin(theta) / (1 + e * math.cos(theta))
		dy = (a * e * (1 - e**2) * math.cos(theta))/(1 + e * math.cos(theta)) + (a * e * (1 - e**2) * (math.sin(theta))**2) / (1 + e * (math.cos(theta))**2)
		V = math.sqrt((2/mu) * ((G * m * M) / r + E))
		vx = V/math.sqrt(dx**2 + dy**2) * dx
		vy = V/math.sqrt(dx**2 + dy**2) * dy

		# put values into 3d vectors (with z value 0)
		aPosition = numpy.array([float(x), float(y), 0])
		aVelocity = numpy.array([float(vx), float(vy), 0])
		output.append(numpy.array([aPosition, aVelocity]))
		step += 1
		if (L/(r**2)) * dt < 2:
			dtheta = (L/r**2) * dt
		else:
			dtheta = 2
		theta += dtheta
		t += dt

	return output

# Generates a uniformly random point on the unit sphere. I found this algorithm 
# at http://mathworld.wolfram.com/SpherePointPicking.html . Or try googling
# 'random point on unit sphere'.
def GenerateRandom3Vector():

	# generate two random numbers on (-1, 1); skip those where
	# u**2 + v**2 >= 1.
	u, v = 100, 100
	while u**2 + v**2 >= 1:
		try:
			u = (numpy.random.random() - 0.5) * 2
			v = (numpy.random.random() - 0.5) * 2
		except ValueError as e:
			print e, "u = {}, v = {}".format(u, v)

	# compute coordinates
	x = 2 * u * math.sqrt(1 - u**2 - v**2)
	y = 2 * v * math.sqrt(1 - u**2 - v**2)
	z = 1 - 2 * (u**2 + v**2)

	return numpy.array([x, y, z])


# Given a body at radius vector (x, y, z) and velocity vector (vx, vy, 0),
# this function computes and returns a tuple (a, e) 
# representing the two-body semi-major axis and eccentricity.
def NewAE(m, M, r_vec, v_vec):

	# reduced mass.
	mu = (m * M) / (m + M)

	# energy.
	E = - (G * m * M) / numpy.linalg.norm(r_vec) + (0.5) * mu * numpy.linalg.linalg.dot(v_vec, v_vec)

	# semi-major axis a.
	a = - (G * m * M) / (2 * E)

	# angular momentum.
	J = mu * numpy.cross(r_vec, v_vec)

	# eccentricity
	e = numpy.sqrt(1 - (numpy.linalg.norm(J)**2)/(mu**2 * (m + M) * G * a))

	return (a, e)

# generates a float (scalar) representing the kick speed supernovae give 
# neutron stars. This has been observationally determined to match a 
# Maxwell distribution with a mean of 300 km/s and sigma of 190 km/s.
def GenerateRandomKickSpeed(fScale):
	return scipy.stats.maxwell.rvs(scale=fScale)



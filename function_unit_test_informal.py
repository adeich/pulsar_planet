import orbital_calc_support_functions as oc
import physical_constants as pc
import numpy as np
import single_monte_carlo



def test_locations_gen():
	sTestFileName = 'TestLocations.txt'

	LocationsList = oc.LocationsGenerator(pc.aEarthSun, pc.eEarth, pc.mEarth, pc.mSun)
	print "Orbit points: {}.".format(len(LocationsList))

	f = open(sTestFileName, 'w')
	f.write(str(LocationsList))
	f.close()


	import matplotlib.pyplot as plt
	plt.plot([x[0][0] for x in LocationsList], [x[0][1] for x in LocationsList], 'ro')
	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# ax.imshow()
	plt.show() 

def test_rand_3vec():
	randVec = oc.GenerateRandom3Vector 

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	n = 100
	# for c, m, zl, zh in [('r', 'o', -2, -2), ('b', '^', -2, -2)]:
	for i in range(30):
		vec = randVec()
		xs, ys, zs = vec
		ax.scatter(xs, ys, zs, c='b')
	
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	plt.show()

def test_newAE():
	fEarthOrbitVelocity = 29 * 1000 
	return str(oc.NewAE(pc.mEarth, pc.mSun, np.array([0, pc.aEarthSun, 0]),
				 np.array([fEarthOrbitVelocity, 0, 0])))	

def test_single_monte_carlo():
	output = single_monte_carlo.SingleMonteCarlo(pc.aEarthSun, 0.1, pc.mEarth, pc.mSun, 
													1000)

	print str(output)
		
	output = single_monte_carlo.SingleMonteCarlo(pc.aEarthSun, 0.1, pc.mEarth, pc.mSun, 
													1000)

	return output
	# print str(output.getAverageBoundPlanetTuple())
	


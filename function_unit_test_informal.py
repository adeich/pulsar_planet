import orbital_calc_support_functions as oc
import constants as pc
import numpy as np
import monte_carlo
import time


class Stopwatch:

	def __init__(self):
		self.startTime = None
		self.endTime = None

	def start(self):
		self.startTime = time.time()

	def reset(self):
		self.startTime = 0

	def getCurrentTime(self):
		return time.time() - self.startTime

	def stopAndReturnTime(self):
		self.endTime = time.time()
		return self.endTime - self.startTime


		

def test_locations_gen():
	sTestFileName = 'TestLocations.txt'

	#LocationsList = oc.LocationsGenerator(pc.aEarthSun, pc.eEarth, pc.mEarth, pc.mSun)
	LocationsList = oc.LocationsGenerator(50000000000.0, 1.0, 5.9999999999999999e+24, 1.9000000000000001e+30)
	# print "Orbit points: {}.".format(len(LocationsList))

	f = open(sTestFileName, 'w')
	f.write('\n'.join([str(x[2]) for x in LocationsList]))
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

def test_monte_carlo(iNumIterations):
		
	oStopwatch = Stopwatch()
	oStopwatch.start()

	result_object = monte_carlo.SingleRawMonteCarloResult(pc.aEarthSun, 0.1, pc.mEarth, pc.mSun, 
													iNumIterations)

	fTotalTime = oStopwatch.stopAndReturnTime()

	lBoundPlanetAnalysis = result_object.GenerateAnalysisOfBoundPlanets()

#	print 'a planet tuple: ' + str(lBoundPlanetTuples)
	print 'total time: ' + str(fTotalTime)
	print 'which means {} seconds/planet.'.format(fTotalTime/iNumIterations)
	print 'total planets: ' + str(result_object.GetTotalPlanets())
	lStrings = sorted(['{0:{1}}\t\t{2}'.format(x + ":", 40, y) for x, y in lBoundPlanetAnalysis.items()])
	print '\n'.join(lStrings)
	print '\n'
	#print 'median bound planet rel vel: ' + str(result_object.GetMedianBoundPlanetRelVelMag())
	#print 'median bound planet: ' + str(result_object.GetMedianBoundPlanetTuple())
	#print 'Mean unbound planet: ' + str(result_object.GetMeanUnboundPlanetTuple())

	

if __name__ == '__main__':
	#test_locations_gen()
	#test_monte_carlo(10)
	#test_monte_carlo(100)
	#test_monte_carlo(1000)
	test_monte_carlo(10000)

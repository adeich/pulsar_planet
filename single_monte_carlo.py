import numpy as np
import orbital_calc_support_functions as oc
import physical_constants as pc
from collections import namedtuple

def SingleMonteCarlo(a0, e0, m0, M0, iNumPoints):

	# Generate a list of orbit points and velocities: [[array(x, y, z), array(vx, vy, vz)], ...]
	lLocations = oc.LocationsGenerator(a0, e0, m0, M0)

	# Create a monte carlo results object.
	ResultsObject = SingleMonteCarloResult(dGridPoint = {
													'semimajoraxis': a0,
													'eccentricity': e0,
													'massOfPlanet': m0,
													'massOfStar': M0})
	
	# Iterate for the number of monte carlo simulation points.
	iCurrentOrbitPosition = 0
	iIteration = 0
	while iIteration < iNumPoints:

		# cycle around the orbital locations.
		iCurrentOrbitPosition = (iCurrentOrbitPosition + 1) %  len(lLocations)
		iIteration += 1

		# Get a and e for current orbit location.
		tCurrentOrbitLocation = lLocations[iCurrentOrbitPosition][0]
		tCurrentOrbitVelocity = lLocations[iCurrentOrbitPosition][1]

		# Random unit vector in direction uniformly spread around sphere.
		tNormalizedRandom3Vector = oc.GenerateRandom3Vector()

		# Observationally-determined distribution.
		fKickSpeed = oc.GenerateRandomKickSpeed(190 * 10**3)

		# New relative velocity = v0vector + (kickspeed * directionvector)
		tVelocity = np.add(tCurrentOrbitVelocity, np.multiply(fKickSpeed, tNormalizedRandom3Vector))

		# plug everything in to find properties of new orbit.
		tnewAE = oc.NewAE(m0, M0, tCurrentOrbitLocation, tVelocity)

		# record data in results object
		tBoundPlanetData = None
		if oc.bIsOrbitBound(tnewAE):
			tBoundPlanetData = oc.OneBoundPlanet(
				eccentricity_initial = e0,
				eccentricity_final = tnewAE.eccentricity,
				semimajoraxis_initial = a0,
				semimajoraxis_final = tnewAE.semimajoraxis,
				radius_at_supernova = tCurrentOrbitLocation,		
				velocity_at_supernova = tCurrentOrbitVelocity,
				kickspeed = fKickSpeed
			)
		ResultsObject.addPlanet(tBoundPlanetData)		

	return ResultsObject


# Example of dGridDimensionDict: {eccentricity: linspace(0, 1, 0.1), semimajoraxis: arange()}
def PerformSingleMonteCarloAtEachGridPoint(dGridDimensionDict, iNumPointsPerLocation):
	pass



# each grid point gets its own result object. 
class SingleMonteCarloResult:
	def __init__(self, dGridPoint):
		self.dGridPoint = dGridPoint
		self.iTotalTries = 0
		self.lBoundPlanets = []

	def addPlanet(self,tBoundPlanet=None):
		self.iTotalTries += 1
		if tBoundPlanet:
			if not isinstance(tBoundPlanet, oc.OneBoundPlanet):
				raise TypeError
			self.lBoundPlanets.append(tBoundPlanet)

	def getTotalPlanets(self):
		return self.iTotalTries

	def getBoundPlanetTupleList(self):
		return self.lBoundPlanets

	def getAverageBoundPlanetTuple(self):
		return OneBoundPlanet(map(np.mean, zip(*self.lBoundPlanets))) 	


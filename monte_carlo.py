import numpy as np
import orbital_calc_support_functions as oc
from constants import dField_codes as codes 
from constants import ParamSpaceCoder as PSC
from collections import namedtuple
import csv

# Perform a single monte carlo simulation for a specified set of two-body parameters.
# The element of randomness for each point is introduced by the GenerateRandom3Vector
# and GenerateRandomKickSpeed functions.

# the simulation at each grid point gets its own result object. 
class SingleRawMonteCarloResult:

	# Run the simulation as the final step of the object init.
	def __init__(self, a0, e0, m0, M0, iNumIterations):
		self.dParamDict = {'a':a0, 'e':e0, 'm':m0, 'M':M0}
		self.iNumIterations = iNumIterations
		self.dUnboundPlanetData = {'total_rel_vel':0, 'total_kick_speed': 0, 'total_abs_theta':0}
		self.lBoundPlanets = [] 
		self.RunSingleMonteCarlo(self.lBoundPlanets, self.dUnboundPlanetData, self.iNumIterations, self.dParamDict)

	def RunSingleMonteCarlo(self, lBoundPlanetList, dUnboundPlanetDict, iNumIterations, dParamDict):

		# Generate a list of orbit points and velocities: [[array(x, y, z), array(vx, vy, vz)], ...]
		d = dParamDict
		lLocations = oc.LocationsGenerator(d['a'], d['e'], d['m'], d['M'])

		# Iterate for the number of monte carlo simulation points.
		iCurrentOrbitPosition = 0
		for iIteration in range(iNumIterations):

			# cycle around the orbital locations.
			iCurrentOrbitPosition = (iCurrentOrbitPosition + 1) %  len(lLocations)

			# Get a and e for current orbit location.
			tCurrentOrbitLocation = lLocations[iCurrentOrbitPosition][0]
			tCurrentOrbitVelocity = lLocations[iCurrentOrbitPosition][1]

			# Random unit vector in direction uniformly spread around sphere.
			tNormalizedRandom3Vector = oc.GenerateRandom3Vector()

			# Observationally-determined distribution.
			fKickSpeed = oc.oPrecompiledRandom.GenerateRandomKickSpeed() # oc.GenerateRandomKickSpeed(190 * 10**3)  # meters / sec

			# New relative velocity = v0vector + (kickspeed * directionvector)
			tVelocity = np.add(tCurrentOrbitVelocity, np.multiply(fKickSpeed, tNormalizedRandom3Vector))

			# plug everything in to find properties of new orbit.
			tnewAE = oc.NewAE(d['m'], oc.mNeutronStar, tCurrentOrbitLocation, tVelocity)

			# record data in results object
			tBoundPlanetData = None
			if oc.bIsOrbitBound(tnewAE):
				tBoundPlanetData = oc.OneBoundPlanet(
					eccentricity_initial = d['e'],
					eccentricity_final = tnewAE.eccentricity,
					semimajoraxis_initial = d['a'],
					semimajoraxis_final = tnewAE.semimajoraxis,
					radius_at_supernova = tCurrentOrbitLocation,		
					velocity_at_supernova = tCurrentOrbitVelocity,
					kickspeed = fKickSpeed,
					tRelativeVelocity = tVelocity,
					orbit_location_theta = lLocations[iCurrentOrbitPosition][2]
				)
				lBoundPlanetList.append(tBoundPlanetData)		
			else:
				dUnboundPlanetDict['total_rel_vel'] += np.absolute(np.linalg.norm(tVelocity))
				dUnboundPlanetDict['total_kick_speed'] += fKickSpeed
				dUnboundPlanetDict['total_abs_theta'] += np.absolute(np.pi - lLocations[iCurrentOrbitPosition][2])


	def GenerateAnalysisOfBoundPlanets(self):
		lRelativeVelocityMagnitudes = [np.absolute(np.linalg.norm(tPlanet.tRelativeVelocity)) for tPlanet in self.lBoundPlanets]
		lThetaDistFromPi = [np.absolute(np.pi - tPlanet.orbit_location_theta) for tPlanet in self.lBoundPlanets]
		lKickVelocities = [tPlanet.kickspeed for tPlanet in self.lBoundPlanets]

		dOutput = {}

		# get hash values from dict in constants.py file.
		dOutput[codes['hashed location in parameter space']] = PSC.GenerateParamSpaceCode(self.dParamDict, self.iNumIterations)
		dOutput[codes['number of simulation points']] = self.iNumIterations
		dOutput[codes['number of bound planets']] = len(self.lBoundPlanets)
		dOutput[codes['unbound kick speed, avg']] = self.dUnboundPlanetData['total_kick_speed']/float(self.iNumIterations)
		dOutput[codes['unbound rel vel, avg']] = 	self.dUnboundPlanetData['total_rel_vel']/float(self.iNumIterations)
		dOutput[codes['unbound theta dist from pi, avg']] = self.dUnboundPlanetData['total_abs_theta']/float(self.iNumIterations)
		dOutput[codes['bound absolute angle from pi, median']] = np.median(lThetaDistFromPi)
		dOutput[codes['bound absolute angle from pi, std']] = np.std(lThetaDistFromPi)
		dOutput[codes['bound absolute angle from pi, avg']] = np.mean(lThetaDistFromPi)
		dOutput[codes['bound kick velocity, median']] = np.median(lKickVelocities)
		dOutput[codes['bound kick velocity, avg']] = np.mean(lKickVelocities)
		dOutput[codes['bound kick velocity, std']] = np.std(lKickVelocities)
		dOutput[codes['bound abs rel velocity, median']] = np.median(lRelativeVelocityMagnitudes)
		dOutput[codes['bound abs rel velocity, avg']] = np.mean(lRelativeVelocityMagnitudes)
		dOutput[codes['bound abs rel velocity, std']] = np.std(lRelativeVelocityMagnitudes)

		return dOutput

	def GetTotalPlanets(self):
		return self.iNumIterations

	def GetNumberOfBoundPlanets(self):
		return len(lBoundPlanetList)

	def AppendBoundPlanetsToCSVFile(self, sFileName):
		with open(sFileName, 'a') as oFile:
			oFileWriter = csv.writer(oFile, delimiter=',')
			for tPlanetTuple in self.lBoundPlanets:
				oFileWriter.writerow(tPlanetTuple)
		
#
# HDF5
# pickle
# save state

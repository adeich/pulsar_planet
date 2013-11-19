import numpy as np
import orbital_calc_support_functions as oc
import physical_constants as pc


def SingleMonteCarlo(a0, e0, m0, M0, iNumPoints, bLogLocations=False):

	# Generate a list of [[array(x, y, z), array(vx, vy, vz)], ...]
	lLocations = oc.LocationsGenerator(a0, e0, m0, M0)
	
	iTotalBoundOrbits = 0

	# a list for holding the optionally logged bound-orbit descriptors.
	lBoundPointProperties = []
	
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

		# Observationally-calibrated gaussian.
		fKickSpeed = oc.GenerateRandomKickSpeed(190 * 10**3)

		# New relative velocity = v0vector + (kickspeed * directionvector)
		tVelocity = np.add(tCurrentOrbitVelocity, np.multiply(fKickSpeed, tNormalizedRandom3Vector))

		# plug everything in to find properties of new orbit.
		tnewAE = oc.NewAE(m0, M0, tCurrentOrbitLocation, tVelocity)
	
		# Record if new orbit is bound.
		if tnewAE[1] < 1:
			iTotalBoundOrbits += 1
			if bLogLocations:
				lBoundPointProperties.append([tnewAE, tCurrentOrbitLocation, tCurrentOrbitVelocity])

	return (float(iTotalBoundOrbits)/iNumPoints, lBoundPointProperties)

		

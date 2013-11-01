def SingleMonteCarlo(a0, e0, m0, M0, iNumPoints, bLogLocations=False):
	lLocations = LocationsGenerator(a0, e0, m0, M0)
	lOutputs
	iCurrentOrbitPosition = 0
	while iTotalPoints < iNumPoints:

		# cycle around the orbital locations.
		iCurrentOrbitPosition = (iCurrentOrbitPosition + 1) %  len(lLocations)

		# Generate new a and e.
		tCurrentOrbitLocation = lLocations[iCurrentOrbitPosition][0]
		tCurrentOrbitVelocity = lLocations[iCurrentOrbitPosition][1]
		tNormalizedRandom3Vector = GenerateRandom3Vector()
		fKickSpeed = GenerateRandomKickSpeed()
		tVelocity = ComputeNewVelocity(tCurrentOrbitVelocity, tNormalizedRandom3Vector, fKickSpeed)
		tnewAE = GenerateNewAE(m0, M0, tCurrentOrbitLocation, tVelocity)

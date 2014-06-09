import unittest
import orbital_calc_support_functions as oc
import constants as pc
import numpy as np
import monte_carlo

class TestFunctions(unittest.TestCase):

	def setUp(self):
		self.tBoundPlanet = oc.OneBoundPlanet(
 				eccentricity_initial = 0, 
        eccentricity_final = 1,
        semimajoraxis_initial = 2, 
        semimajoraxis_final = 3,
        radius_at_supernova = np.array([4,5,6]),
        velocity_at_supernova = np.array([7,8,9]),
        kickspeed = 10
			)
		self.tAandE = oc.AandE(semimajoraxis=5, eccentricity=0)

	def test_bIsOrbitBound(self):
		self.tAandECircular = oc.AandE(semimajoraxis = 10, eccentricity = 0)
		self.assertTrue(oc.bIsOrbitBound(self.tAandECircular), True)

if __name__ == '__main__':
	unittest.main()



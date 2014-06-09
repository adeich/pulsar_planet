from bidict import bidict

# gravitational constant
G = 6.67 * 10**-11 

aEarthSun = 1.5 * 10**11 # m
eEarth = 0.72  # unitless
mEarth = 6.0 * 10**24 # kg
mSun =  1.9 * 10**30 # kg

mNeutronStar = 1.4 * mSun

# for normalizing data fields and for reference in printing to file.
dField_codes = bidict({
	'hashed location in parameter space': 'LOCATION',
	'number of simulation points': 'num',
	'unbound kick speed, avg': 'U_KS_A',
	'unbound rel vel, avg': 'U_RV_A',
	'unbound theta dist from pi, avg': 'U_TDP_A',
	'bound absolute angle from pi, median': 'B_AAP_M',
	'bound absolute angle from pi, std': 'B_AAP_S',
	'bound absolute angle from pi, avg': 'B_AAP_A',
	'bound kick velocity, median': 'B_KV_M',
	'bound kick velocity, avg': 'B_KV_A',
	'bound kick velocity, std': 'B_KV_S',
	'bound abs rel velocity, median': 'B_ARV_M',
	'bound abs rel velocity, avg': 'B_ARV_A',
	'bound abs rel velocity, std': 'B_ARV_S'
})

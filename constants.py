from bidict import bidict
import re

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
	'number of bound planets': 'numB',
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

class ParamSpaceCode:

	def __init__(self):
		# in this regex, the (?P<xxx>) business names a group xxx.
		self.regex = re.compile('a(?P<a>.*)_e(?P<e>.*)_m(?P<m>.*)_M(?P<M>.*)_I(?P<I>.*)')

	# input dParamPoint is a dictionary.
	def GenerateParamSpaceCode(self, dParamPoint, iNumIters):
		return 'a{a}_e{e}_m{m}_M{M}_I{I}'.format(a = dParamPoint['a'], e = dParamPoint['e'],
			m = dParamPoint['m'], M = dParamPoint['M'], I = iNumIters)

	def ParseParamSpaceCode(self, sCode):
		result = self.regex.search(sCode)
		return result.groupdict()

	def test(self):
		dParamPoint = {'a':1, 'e':22, 'm': 333, 'M': 4444}
		sCode = self.GenerateParamSpaceCode(dParamPoint, 5000)
		dNewParamPoint = self.ParseParamSpaceCode(sCode)
		for sKey, value in dParamPoint.iteritems():
			if not int(dNewParamPoint[sKey]) == int(value):
				raise BaseException('{}!={} dict1: {}, code: {}, dict2: {}'.format(
					dNewParamPoint[sKey], value, dParamPoint, sCode, dNewParamPoint))
		print 'test ran.' 

ParamSpaceCoder = ParamSpaceCode()

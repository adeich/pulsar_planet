import time
import datetime
from itertools import product as CartesianProduct
from numpy import linspace
import monte_carlo
import constants as PC
import CustomCSVFileWriter as CSV

class stopwatch:
	def __init__(self):
		self.start_time = time.time() 
	def start(self):
		self.start_time = time.time()
	def getTimeElapsed(self):
		return time.time() - self.start_time


def PrintUpdate(tGridPoint, lFullGrid, fDurationOfMostRecent):
	# figure out where we are in grid.
	iIndex = [i for i, v in enumerate(lFullGrid) if v == tGridPoint][0]
	fPercent = 100 * (float(iIndex) / len(lFullGrid))
	print "{:2.1f}% completed ({})/({}). time was {} seconds. Est. time remaining: {}. ".format(
		fPercent,
		iIndex, 
		len(lFullGrid),
		fDurationOfMostRecent,
		str(datetime.timedelta(seconds = fDurationOfMostRecent * (len(lFullGrid) - iIndex)))
		)

def PerformOverParamGrid(eDict, aDict, mDict, MDict, iNumIters, oFile):

	# write a header line to the file.
	oFile.write(CSV.GenerateCSVHeader()); oFile.write('\n')

	# check that dParamDict contains valid keys.
	for dParamDict in [eDict, aDict, mDict, MDict]:
		for sParameter in ['lowerBound', 'upperBound', 'number']:
			if not sParameter in dParamDict:
				raise BaseError('{} key missing from function parameter {}.'.format(
					sParameter, dParamDict))
	# check that eccentricity is within the range of e for a bounded ellipse. 
	if eDict['lowerBound'] < 0 or eDict['lowerBound'] >= 1: 
		raise BaseException("eccentricity must be in range 0<=e<1.") 
	if eDict['upperBound'] < 0 or eDict['lowerBound'] >= 1: 
		raise BaseException("eccentricity must be in range 0<=e<1.") 

	# convert a dict (e.g. eDict) into an evenly spaced list of floats.
	def MakeSpacedList(SpacingDict):
		fStart = SpacingDict['lowerBound']
		fStop = SpacingDict['upperBound']
		iNumber = SpacingDict['number']
		return linspace(fStart, fStop, num=iNumber, endpoint=True)
		
	# the order of these dicts is fixed for now; see index references below.
	gridGenerator = CartesianProduct(
			MakeSpacedList(aDict),
			MakeSpacedList(eDict),
			MakeSpacedList(mDict),
			MakeSpacedList(MDict))

	# It's ok to copy all of generator output to memory because it's relatively 
	# small (< 1000 tuples)
	lFullGrid = [tPoint for tPoint in gridGenerator]

	oStopwatch = stopwatch()

	for tGridPoint in lFullGrid:
 		oStopwatch.start()
		try:
			oInstance = monte_carlo.SingleRawMonteCarloResult(
				a0=tGridPoint[0], e0=tGridPoint[1], m0=tGridPoint[2], M0=tGridPoint[3], 
				iNumIterations = iNumIters)
			# oFile.write('{}'.format(str(oInstance.GenerateAnalysisOfBoundPlanets())))
			csv_line = CSV.GenerateCSVString(oInstance.GenerateAnalysisOfBoundPlanets())
			oFile.write(csv_line); oFile.write('\n')
			PrintUpdate(tGridPoint, lFullGrid, oStopwatch.getTimeElapsed()) 
			
		except BaseException:
			print "grid point: {}".format(str(tGridPoint))
			raise 
	print "Completed. Results in {}".format(oFile.name)
		

if __name__ == '__main__':
	with open('ResultsData.csv', 'w') as oFile:
		PerformOverParamGrid(
			eDict = {'lowerBound':0.01, 'upperBound':0.95, 'number':20}, # e must be 0<=e<1!
			aDict = {'lowerBound':PC.aEarthSun/3, 'upperBound':PC.aEarthSun*10, 'number':50},
			mDict = {'lowerBound':PC.mEarth, 'upperBound':PC.mEarth*100, 'number':4},
			MDict = {'lowerBound':PC.mSun, 'upperBound':PC.mSun*5, 'number':2},
			iNumIters = 10000,
			oFile = oFile
		)

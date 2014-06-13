from constants import dField_codes as codes


# this defines the ordering of what appears on the csv line.
# These strings, though wordy, are the keys of a dictionary.
lLineContent = [
	'hashed location in parameter space',
	'number of simulation points',
	'number of bound planets',
	'unbound kick speed, avg',
	'unbound rel vel, avg',
	'unbound theta dist from pi, avg',
	'bound absolute angle from pi, median',
	'bound absolute angle from pi, std',
	'bound absolute angle from pi, avg',
	'bound kick velocity, median',
	'bound kick velocity, avg',
	'bound kick velocity, std',
	'bound abs rel velocity, median',
	'bound abs rel velocity, avg',
	'bound abs rel velocity, std'
]


# for each line print out:
# coordinates in parameter space
# number of simpoints


def GenerateCSVHeader():
	return ', '.join([codes[x] for x in lLineContent])

def GenerateCSVString(dataDict):
	return ', '.join([str(dataDict[codes[x]]) for x in lLineContent]) 
		



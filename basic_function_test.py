import locations_generator
import physical_constants as pc

sTestFileName = 'TestLocations.txt'

LocationsList = locations_generator.LocationsGenerator(pc.aEarthSun, pc.eEarth, pc.mEarth, pc.mSun)
print "Orbit points: {}.".format(len(LocationsList))

f = open(sTestFileName, 'w')
f.write(str(LocationsList))
f.close()


import matplotlib.pyplot as plt
plt.plot([x[0] for x in LocationsList], [y[1] for y in LocationsList], 'ro')
fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.imshow()
plt.show() 

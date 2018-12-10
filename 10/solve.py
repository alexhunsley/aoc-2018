# solve.py 10
#

from copy import deepcopy
from functools import reduce

f = open("input.txt")
# f = open("sampleInput.txt")

coords = []
vels = []

# JJXZHKFP
for line in f.readlines():
	split = line.split('<')

	coord = list(map(str.strip, split[1].split('>')[0].split(',')))
	vel = list(map(str.strip, split[2].split('>')[0].split(',')))

	coord = list(map(int, coord))
	vel = list(map(int, vel))

	coords.append(coord)
	vels.append(vel)

def outputGrid(minX, maxX, minY, maxY, atTime):
	coordsAtTime = deepcopy(coords)

	# could use map here, if we stored velocities in same tuple as the coords
	for i in range(0, len(coordsAtTime)):
		coordsAtTime[i][0] += vels[i][0] * atTime
		coordsAtTime[i][1] += vels[i][1] * atTime

	for y in range(minY, maxY + 1):
		for x in range(minX, maxX + 1):		
			if [x, y] in coordsAtTime:
				print('#', end='')
			else:
				print('.', end='')
		print('\n', end='')

# we track how the bounding box changes over time
globalMinX = reduce(min, [c[0] for c in coords])
globalMinY = reduce(min, [c[1] for c in coords])
globalMaxX = reduce(max, [c[0] for c in coords])
globalMaxY = reduce(max, [c[1] for c in coords])

globalMinSizeX = globalMaxX - globalMinX
globalMinSizeY = globalMaxY - globalMinY

minimumXFoundAtTime = -1
minimumYFoundAtTime = -1

# once we hit minimum size of points, that's probably
# the answer, but allow a 'timeout' for new minima to appear
giveUpNSecondsAfterMinimumStopsReducing = 100

time = 0
coordsWorking = deepcopy(coords)

while True:
	# should probably make or find a minmax function (that gives back tuple (min, max) for given list)
	minX = reduce(min, [c[0] for c in coordsWorking])
	maxX = reduce(max, [c[0] for c in coordsWorking])
	minY = reduce(min, [c[1] for c in coordsWorking])
	maxY = reduce(max, [c[1] for c in coordsWorking])

	sizeX = maxX - minX
	sizeY = maxY - minY

	if sizeX < globalMinSizeX:
		globalMinSizeX = sizeX
		globalMinX = minX
		globalMaxX = maxX
		minimumXFoundAtTime = time

	if sizeY < globalMinSizeY:
		globalMinSizeY = sizeY
		globalMinY = minY
		globalMaxY = maxY
		minimumYFoundAtTime = time

	if ((time - minimumXFoundAtTime) > giveUpNSecondsAfterMinimumStopsReducing and (time - minimumYFoundAtTime) > giveUpNSecondsAfterMinimumStopsReducing):
		print('Giving up at time %d because both minimums stopped reducing for %d secs' % (time, giveUpNSecondsAfterMinimumStopsReducing))
		break

	# could use map here, if we stored velocities in same tuple as the coords
	for i in range(0, len(coordsWorking)):
		coordsWorking[i][0] += vels[i][0]
		coordsWorking[i][1] += vels[i][1]

	time += 1


print(' Part 1 solution:')
outputGrid(globalMinX, globalMaxX, globalMinY, globalMaxY, minimumXFoundAtTime)
print('\n')
print(' Part 2: %d seconds' % minimumXFoundAtTime)

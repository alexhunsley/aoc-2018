# solve.py 10
#

from collections import Counter, defaultdict
from itertools import chain
import pprint
from copy import copy, deepcopy
from itertools import repeat
from functools import reduce

f = open("input.txt")
# f = open("sampleInput.txt")

coords = []
vels = []

for line in f.readlines():
	print('line= ', line)
	split = line.split('<')

	coord = list(map(str.strip, split[1].split('>')[0].split(',')))
	vel = list(map(str.strip, split[2].split('>')[0].split(',')))

	coord = list(map(int, coord))
	vel = list(map(int, vel))

	print('c=', coords)
	print('v =', vels)
	# print(coords, vels)

	# x = int(line[10:16].strip())
	# y = int(line[17:24].strip())
	# vx = int(line[36:38].strip())
	# vy = int(line[40:42].strip())

	coords.append(coord)
	vels.append(vel)

print('READ COORDS, VELS: ', coords, vels)
def outputGrid(minX, maxX, minY, maxY, atTime):
	coordsAtTime = deepcopy(coords)

	print('copied corods at time: ', coordsAtTime[0:5])

	for i in range(0, len(coordsAtTime)):
		coordsAtTime[i][0] += vels[i][0] * atTime
		coordsAtTime[i][1] += vels[i][1] * atTime

	print(coordsAtTime[0:5])

	for y in range(minY, maxY + 1):
		for x in range(minX, maxX + 1):		
			if [x, y] in coordsAtTime:
				print('#', end='')
			else:
				print('.', end='')
		print('\n', end='')

# track how the bounding box changes over time
# sizes = []
bounds = []

globalMinX = reduce(min, [c[0] for c in coords])
globalMinY = reduce(min, [c[1] for c in coords])
globalMaxX = reduce(max, [c[0] for c in coords])
globalMaxY = reduce(max, [c[1] for c in coords])

globalMinSizeX = globalMaxX - globalMinX
globalMinSizeY = globalMaxY - globalMinY

print(' global min size x, y at beginning: ', globalMinSizeX, globalMinSizeY)

# time allowed for expand

minimumXFoundAtTime = -1
minimumYFoundAtTime = -1
giveUpNSecondsAfterMinimumStopsReducing = 100

time = 0
coordsWorking = deepcopy(coords)

while True:
	if (time % 10000) == 0:
		print('tick, s = %d' % time)

	minX = reduce(min, [c[0] for c in coordsWorking])
	maxX = reduce(max, [c[0] for c in coordsWorking])
	minY = reduce(min, [c[1] for c in coordsWorking])
	maxY = reduce(max, [c[1] for c in coordsWorking])

	sizeX = maxX - minX
	sizeY = maxY - minY
	# sizes.append([sizeX, sizeY])

	if sizeX < globalMinSizeX:
		globalMinSizeX = sizeX
		globalMinX = minX
		globalMaxX = maxX
		minimumXFoundAtTime = time
		# print('found new minX, time = %d, %d' % (globalMinSizeX, time))

	if sizeY < globalMinSizeY:
		globalMinSizeY = sizeY
		globalMinY = minY
		globalMaxY = maxY
		minimumYFoundAtTime = time
		# print('found new minY, time = %d, %d' % (globalMinSizeY, time))

	if ((time - minimumXFoundAtTime) > giveUpNSecondsAfterMinimumStopsReducing and (time - minimumYFoundAtTime) > giveUpNSecondsAfterMinimumStopsReducing):
		print('giving up at time %d due to both minimums stopped reducing for %d secs' % (time, giveUpNSecondsAfterMinimumStopsReducing))
		break

	for i in range(0, len(coordsWorking)):
		coordsWorking[i][0] += vels[i][0]
		coordsWorking[i][1] += vels[i][1]

	time += 1


print('minSizex, y = ', globalMinSizeX, globalMinSizeY)
print(' time since mins X, Y found: %d, %d' % (time - minimumXFoundAtTime, time - minimumYFoundAtTime))
print(' minimumXFoundAtTime, Y: ', minimumXFoundAtTime, minimumYFoundAtTime)
print('. so we found minX, maxX, minY, maxY = ', globalMinX, globalMaxX, globalMinY, globalMaxY)
# just assume we find the minimum at the same time for both X and Y, and use the X!

# for p in range(-5, 5):
# 	outputGrid(globalMinX, globalMaxX, globalMinY, globalMaxY, minimumXFoundAtTime + p)
outputGrid(globalMinX, globalMaxX, globalMinY, globalMaxY, minimumXFoundAtTime)


print('FINAL COORDS:', coords)

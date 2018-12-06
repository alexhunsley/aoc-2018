# solve.py 6
#
import sys
from operator import methodcaller
from functools import reduce
from collections import Counter, defaultdict
from tqdm import tqdm

# part 2 plan:
# for each Y coordinate we scan down over, calc the total manhattan dist to all targets from leftmost X (-10000 or thereabouts). Then move (the dist - 10000) right; that's left-most point L.
# repeat similarly for the right R. Then add (R - L + 1) points to the area total, continue.
#
# TIP: calc the initial manhatten dist. then for each step right your M dist actually decrements by <number of targets>...

# part 2
safeRegionMaxDistance = 10000

coords = []

lineIndex = 0

f = open("input.txt")

for line in f.readlines():
	coordsAsList = list(map(int, line.rstrip().replace(' ', '').split(',')))
	coords.append(coordsAsList)
	lineIndex += 1

minX = reduce(min, [item[0] for item in coords])
maxX = reduce(max, [item[0] for item in coords])
minY = reduce(min, [item[1] for item in coords])
maxY = reduce(max, [item[1] for item in coords])

sampleXLeft = minX - safeRegionMaxDistance
sampleXRight = maxX + safeRegionMaxDistance

startYScan = minY - safeRegionMaxDistance
endYScan = maxY + safeRegionMaxDistance

print
print


# border = 1

#for part 2 use this:
border = 10000

closestTargetToCoordDict = defaultdict(set)

safeSquareCount = 0

for y in tqdm(range(minY - border, maxY + 1 + border)):
	for x in range(minX - border, maxX + 1 + border):
		dists = [(abs(x - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]

		if sum(dists) < safeRegionMaxDistance:
			safeSquareCount += 1

		distancesCounter = Counter(dists)
		minDist = min(distancesCounter)

		duplicateDistances = [dist for dist in distancesCounter if distancesCounter[dist] > 1]
		uniqueDistancesSorted = [dist for dist in distancesCounter if distancesCounter[dist] == 1]
		uniqueDistancesSorted.sort()

		assert uniqueDistancesSorted

		if (uniqueDistancesSorted[0] == 0):
			# don't forget to add a closest count for the actual square containing a target
			closestTargetToCoordDict[indexOfClosestCoord].add((x, y))
			# print(chr(ord('A') + indexOfClosestCoord), end='')
			continue

		# any duplicate distances at all, and we consider there is no 'closest'
		#. --- nope, stupid question wording. It's dupes of only the closest distance that causes '.' to appear!
		if distancesCounter[minDist] > 1:
			# print('.', end='')
			continue

		indexOfClosestCoord = dists.index(uniqueDistancesSorted[0])

		closestTargetToCoordDict[indexOfClosestCoord].add((x, y))
		# print(indexOfClosestCoord, end='')
	# print('')


sortedTargetDict = sorted(closestTargetToCoordDict, key=lambda x:len(closestTargetToCoordDict[x]), reverse=True)
targetIndexCoveringMostArea = sortedTargetDict[0]

# print('initial dict: ', closestTargetToCoordDict)
# print('sorted target dict: ', sortedTargetDict)
# print('target covering most area: ', targetIndexCoveringMostArea)

targetCoordsWithInfiniteArea = list(filter(lambda c: c[0] == minX or c[0] == maxX or c[1] == minY or c[1] == maxY, coords))

# print(' inf area tarfs: ', list(targetCoordsWithInfiniteArea))

targetIndexesWithInfiniteArea = list(map(lambda targetCoord: coords.index(targetCoord), targetCoordsWithInfiniteArea))
# targetIndexesWithInfiniteArea = list(map(lambda targetCoord: targetCoord, targetCoordsWithInfiniteArea))
# print(' inf area target indexes: ', targetIndexesWithInfiniteArea)

sortedTargetAreasWithoutInfiniteAreas = [x for x in sortedTargetDict if x not in targetIndexesWithInfiniteArea]

# print('sorted areas, minus infinte: ', sortedTargetAreasWithoutInfiniteAreas)
print(' Part 1: area of largest region: ', len(closestTargetToCoordDict[ sortedTargetAreasWithoutInfiniteAreas[0] ]))
print(' Part 2: safe square count: ', safeSquareCount)

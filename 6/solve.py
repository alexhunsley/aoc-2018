# solve.py 6
#
import sys
from operator import methodcaller
from functools import reduce
from collections import Counter, defaultdict
from tqdm import tqdm

# part 2 plan:
#
# Basic idea:
# for each Y coordinate we scan down over (from minY - 10000 to maxY + 10000), calc the 
# total manhattan dist to all targets from minX - 1. Then move (10000 - totalDist)/numTargets to left; 
# that's left-most point L which is within range.
# Repeat similarly for the right R (using maxX + 1). Then add (R - L + 1) points to the area total.
#
# Worked example:
# minX = 21. There are 5 targets. Suppose for a given Y: 
# manhattanDist(minX-1, Y) = 9989.
# For each decrement of X from that point, the manhattanDist will increase by 5.
# Therefore, we want to move left by floor((9999 - 9989)/numTargets) = 2.
# So in general, move left by floor((maxDist - manhattanDist(minX-1, Y)) / numTargets).
# And on the right, we move right by floor((maxDist - manhattanDist(maxX+1, Y)) / numTargets)
#
#
# Refinment on the basic idea:
# Let 'target bounds area' (TBA) be the bounding region for all the targets.
#
# Calcs in TBA are non-trivial, but this area is small.
#
# Outside the TBA, we can do a much more efficient calculation:
# calc L' = manhattanDist(minX, minY),
#      R' = manhattanDist(maxX, minY).
# As you move up, L' and R' move towards TBA at rate of numTargets for every Y step up.
# Hence, we have a triangle shape above TBA that we can easily calculate the area for!
# So you get all that coverage for just 2 manhattan distance calcs.
#  (-- not sure it's worth the bother. Try just the basic scan in part 1 first.)
#

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

print
print


# border = 1

#for part 2 use this:
border = 0

closestTargetToCoordDict = defaultdict(set)

# safeSquareCount = 0

for y in tqdm(range(minY - border, maxY + 1 + border)):
	for x in range(minX - border, maxX + 1 + border):
		dists = [(abs(x - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]

		# if sum(dists) < safeRegionMaxDistance:
		# 	safeSquareCount += 1

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

# print(' Part 2: safe square count: ', safeSquareCount)

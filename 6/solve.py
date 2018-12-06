# solve.py 6
#
import sys
from operator import methodcaller
from functools import reduce
from collections import Counter, defaultdict



# contents = f.readlines()

# f.close()

# # temp, just to keep stuff simpler

# print(contents)
# # contents = [[line§] for lineIndex in range(0, 3)]
# # contents = [list(lineIndex) for lineIndex in range(0, len(contents))]
# # contents = [[lineIndex].append(contents[lineIndex]) for lineIndex in range(0, len(contents))]

# # print('new contents: ', contents)
# # sys.exit(1)

# # map in py3 returns an iterable!

# # contents = [[lineIndex, contents[lineIndex]] for lineIndex in range(0, len(contents))]
# # print('with line indexes: ', contents)

# # the inner map converts the list of coordinates from string pairs to int pairs
# # coords = list(map(lambda line: list(map(int, line.rstrip().replace(' ', '').split(','))), contents))
# coords = list(map(lambda lineIndex: list(map(int, contents[lineIndex].rstrip().replace(' ', '').split(','))), range(0, len(contents))))

coords = []

lineIndex = 0

f = open("input.txt")

for line in f.readlines():
	coordsAsList = list(map(int, line.rstrip().replace(' ', '').split(',')))
	coords.append(coordsAsList)
	lineIndex += 1

# coords = coords[0:2]
# coords = [(10,10), (11, 14), (12,12)]
# coords = [(10,10), (19, 18), (12,11)]

# coords = [
# 	[1, 1],
# 	[1, 6],
# 	[8, 3],
# 	[3, 4],
# 	[5, 5],
# 	[8, 9]
# ]

print('coords: ', coords)
# sys.exit(1)

# print("it is", [item for item in coords])

minX = reduce(min, [item[0] for item in coords])
maxX = reduce(max, [item[0] for item in coords])
minY = reduce(min, [item[1] for item in coords])
maxY = reduce(max, [item[1] for item in coords])

print('bounds: ', minX, minY, maxX, maxY)

print
print

border = 1

closestTargetToCoordDict = defaultdict(set)


# for y in range(4, 5):
for y in range(minY - border, maxY + 1 + border):
	for x in range(minX - border, maxX + 1 + border):
		# pass

		dists = [(abs(x - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]

		# print('x,y =', x, y)
		# print(' dists =', dists)

		distancesCounter = Counter(dists)
		minDist = min(distancesCounter)
		# minDist = min(distancesCounter, key=distancesCounter.get)
		# print('minDist=',minDist)

		duplicateDistances = [dist for dist in distancesCounter if distancesCounter[dist] > 1]
		# uniqueDistancesSorted = [dist for dist in distancesCounter if distancesCounter[dist] == 1]
		uniqueDistancesSorted = [dist for dist in distancesCounter if distancesCounter[dist] == 1]
		uniqueDistancesSorted.sort()

		assert uniqueDistancesSorted

		if (uniqueDistancesSorted[0] == 0):
			# don't forget to add a closest count for the actual square containing a target
			closestTargetToCoordDict[indexOfClosestCoord].add((x, y))
			print(chr(ord('A') + indexOfClosestCoord), end='')
			continue

		# any duplicate distances at all, and we consider there is no 'closest'
		#. --- nope, stupid question wording. It's dupes of the closest distances that cause '.' to appear!

		# print('distances counter = ', distancesCounter)
		# print('minDist =',minDist)
		if distancesCounter[minDist] > 1:
			# print('got a dupe! dists = ', distancesCounter)
			print('.', end='')
			continue

		indexOfClosestCoord = dists.index(uniqueDistancesSorted[0])

		closestTargetToCoordDict[indexOfClosestCoord].add((x, y))
		print(indexOfClosestCoord, end='')
	print('')

# for i in sorted(closestTargetToCoordDict, key=lambda x:len(closestTargetToCoordDict[x]), reverse=True):
# 	print(i)


sortedTargetDict = sorted(closestTargetToCoordDict, key=lambda x:len(closestTargetToCoordDict[x]), reverse=True)
targetIndexCoveringMostArea = sortedTargetDict[0]

print('initial dict: ', closestTargetToCoordDict)
print('sorted target dict: ', sortedTargetDict)
print('target covering most area: ', targetIndexCoveringMostArea)

targetCoordsWithInfiniteArea = list(filter(lambda c: c[0] == minX or c[0] == maxX or c[1] == minY or c[1] == maxY, coords))

print(' inf area tarfs: ', list(targetCoordsWithInfiniteArea))


targetIndexesWithInfiniteArea = list(map(lambda targetCoord: coords.index(targetCoord), targetCoordsWithInfiniteArea))
# targetIndexesWithInfiniteArea = list(map(lambda targetCoord: targetCoord, targetCoordsWithInfiniteArea))
print(' inf area target indexes: ', targetIndexesWithInfiniteArea)


sortedTargetAreasWithoutInfiniteAreas = [x for x in sortedTargetDict if x not in targetIndexesWithInfiniteArea]

print('sorted areas, minus infinte: ', sortedTargetAreasWithoutInfiniteAreas)
print(' area of largest region: ', len(closestTargetToCoordDict[ sortedTargetAreasWithoutInfiniteAreas[0] ]))

# call total area for each coord


# we can't discount the infinite area items yet - need to take them into account when calculating the distances.
# we remove them from consideration when considering the highest area region




# for x in range()
# methodcaller("int")
# print(stuff)


# minX = 9999
# maxX = -9999
# minY = 9999
# maxY = -9999

# for coord in coords:
# 	minX = min(coord[0], minX)
# 	minY = min(coord[1], minY)
# 	maxX = max(coord[0], maxX)
# 	maxY = max(coord[1], maxY)

# print('AB\n'.rstrip() + "X")

# print("it is", [item[0] for item in list(coords)])

# print(reduce((lambda x, y: x * y), [1, 2, 3, 4]))
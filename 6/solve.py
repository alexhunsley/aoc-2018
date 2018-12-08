# solve.py 6
#
import sys
from operator import methodcaller
from functools import reduce
from collections import Counter, defaultdict
from tqdm import tqdm
import math

# hmm. the 4 targets file has no finite areas, but this script finds a finite area. So my infinite
# area detection isn't quite working.
# To properly detect infinite area targets, we could scan the rectangular border of the bounding region;
# any target closest to those squares is an infinite area.

# part 2 plan:  (THIS IS NOT NEEDED FOR INPUT DATA! SAFE AREA IS WITHIN TARGET AREA BOUNDS!)
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

# If True, we see grid display.
# Otherwise, a tqdm progress is shown.
outputGrid = False

# safeRegionMaxDistance = 50
safeRegionMaxDistance = 10000

coords = []

lineIndex = 0

f = open("input.txt")
# f = open("input_4targets.txt")
# f = open("input_3targets_noFiniteAreas.txt")
# f = open("input_4targets.txt")
# f = open("input_1target_noFiniteAreas.txt")

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


# P2
# # feep.pgm
# 24 7
# 15

def gridPrint(str):
	if outputGrid:
		print(str, end='')

def solvePart1and2():
	border = 0

	# image output
	imgWidth = maxX - minX + 1 + 2 * border
	imgHeight = maxY - minY + 1 + 2 * border
	maxGreylevels = len(coords)
	img = open("map.ppm", "w")
	img.write("P3\n%d %d\n%d\n" % (imgWidth, imgHeight, maxGreylevels))


	closestTargetToCoordDict = defaultdict(set)

	# safeSquareCount = 0

	if outputGrid:
		yIterator = range(minY - border, maxY + 1 + border)
	else:
		yIterator = tqdm(range(minY - border, maxY + 1 + border))
	
	numSafeSquares = 0
	for y in yIterator:
		for x in range(minX - border, maxX + 1 + border):
			dists = [(abs(x - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]

			isInsideSafeArea = False
			if sum(dists) < safeRegionMaxDistance:
				isInsideSafeArea = True
				numSafeSquares += 1

			distancesCounter = Counter(dists)
			minDist = min(distancesCounter)

			duplicateDistances = [dist for dist in distancesCounter if distancesCounter[dist] > 1]
			uniqueDistancesSorted = [dist for dist in distancesCounter if distancesCounter[dist] == 1]
			uniqueDistancesSorted.sort()

			# uniqueDistancesSorted can legitimately be empty
			# assert uniqueDistancesSorted
			# any duplicate distances at all, and we consider there is no 'closest'
			#. --- nope, stupid question wording. It's dupes of only the closest distance that causes '.' to appear!
			if not uniqueDistancesSorted or distancesCounter[minDist] > 1:
				gridPrint('.')
				img.write('0 0 0  ') # write black pixel for no closest target
				continue

			indexOfClosestCoord = dists.index(uniqueDistancesSorted[0])

			if (uniqueDistancesSorted[0] == 0):
				# don't forget to add a closest count for the actual square containing a target
				closestTargetToCoordDict[indexOfClosestCoord].add((x, y))

				gridPrint(chr(ord('A') + indexOfClosestCoord))

				img.write('%d 0 0  ' % maxGreylevels) # write red pixel for actual target location

				continue

			closestTargetToCoordDict[indexOfClosestCoord].add((x, y))
			gridPrint(indexOfClosestCoord)

			img.write('%d %d %d  ' % (indexOfClosestCoord+1, indexOfClosestCoord+1, indexOfClosestCoord+1))
		gridPrint('\n')
		img.write('\n')

	img.close()

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

	if not sortedTargetAreasWithoutInfiniteAreas:
		print(' Part 1: Oops, there are no finite areas in this data set!')
	else:
		# print('sorted areas, minus infinte: ', sortedTargetAreasWithoutInfiniteAreas)
		print(' Part 1: area of largest region: ', len(closestTargetToCoordDict[ sortedTargetAreasWithoutInfiniteAreas[0] ]))

	print('Part 2: num safe squares: %d' % numSafeSquares)
	# print(' Part 2: safe square count: ', safeSquareCount)


def solvePart2():
	# +1 needed? Might as well. It's on the correct side of safeness/overkill
	border = int((safeRegionMaxDistance / len(coords)) + 1)
	print('border = %d' % border)
	# image output
	imgWidth = maxX - minX + 1 + 2 * border
	imgHeight = maxY - minY + 1 + 2 * border
	maxGreylevels = len(coords)
	img = open("map.ppm", "w")
	img.write("P3\n%d %d\n%d\n" % (imgWidth, imgHeight, maxGreylevels))


	closestTargetToCoordDict = defaultdict(set)

	# safeSquareCount = 0

	# if outputGrid:
	# 	yIterator = range(minY - border, maxY + 1 + border)
	# else:
	# 	yIterator = tqdm(range(minY - border, maxY + 1 + border))
	yIterator = range(minY - border, maxY + 1 + border)

	totalSafeSquares = 0

	for y in yIterator:
		# topLeft = (minX, y)
		x = minX

		# left side
		distsL = [(abs(x - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]

		totalDistsLeftSide = sum(distsL)

		if totalDistsLeftSide >= safeRegionMaxDistance:
			# TODO just calc this area manually; all bets are off for the optimisation 
			# if edge of safety is within the target bounding area 
			leftmostXCoordWithinSafeDistance = 0	
			pass
		else:
			leftmostXCoordWithinSafeDistance = x - math.floor((safeRegionMaxDistance - 1 - totalDistsLeftSide) / len(coords))

			checkDistsL = [(abs(leftmostXCoordWithinSafeDistance - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]
			checkTotalDistsL = sum(checkDistsL)

			print("LEFT y: %d totalDists: %d   leftMost safe X: %d  totalDistAtLeftmost: %d" 
				% (y, totalDistsLeftSide, leftmostXCoordWithinSafeDistance, checkTotalDistsL))

		# right side
		x = maxX
		distsR = [(abs(x - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]

		totalDistsRightSide = sum(distsR)

		if totalDistsRightSide >= safeRegionMaxDistance:
			# TODO just calc this area manually; all bets are off for the optimisation 
			# if edge of safety is within the target bounding area 
			rightmostXCoordWithinSafeDistance = 0	
			pass
		else:
			rightmostXCoordWithinSafeDistance = x + math.floor((safeRegionMaxDistance - 1 - totalDistsRightSide) / len(coords))

			checkDistsR = [(abs(leftmostXCoordWithinSafeDistance - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]
			checkTotalDistsR = sum(checkDistsR)

			print("RIGHT y: %d totalDists: %d   rightMost safe X: %d  totalDistAtRightmost: %d" 
				% (y, totalDistsRightSide, rightmostXCoordWithinSafeDistance, checkTotalDistsR))

		numSquaresSafe = rightmostXCoordWithinSafeDistance - leftmostXCoordWithinSafeDistance + 1
		print("num safe squares: %d" % numSquaresSafe)
		if numSquaresSafe > 0:
			totalSafeSquares += numSquaresSafe

	print("Part 2: num safe squares: %d" % totalSafeSquares)

solvePart1and2()
# solvePart2()

# getting 63187 but that's wrong; too high


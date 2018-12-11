# solve.py
#

# Input: 9221

#
# Part 2:
#
# More efficient square summing:
# (yeah, we knew this was coming!)
#
# For square size S, maintain a horiz sum of S starting at some X.
# To move right, subtract leftmost item, add rightmost. 
# Likewise, for moving down, we have a list of these horizontal sums.
# We chop off start of list and add to end to move downwards.
#
# Before doing a right move, copy the horiz sum list so we can restore later.
#
# POSSIBLE OPTIMISATIONS:
#
# I call makeSumData for creating sumdata for each square size. Instead, we could just modify the previous sumData
# to make square size n+1 each time (order n rather than n^2).
#

from collections import Counter, defaultdict
from itertools import chain
from pprint import pprint
from copy import copy, deepcopy
from itertools import repeat
from functools import reduce
import sys
from operator import sub, add
from tqdm import tqdm

serialNumber = 9221
powerGrid = []

gridWidth = 300
gridHeight = 300


# powergrid is a 2d array, addressed as powerGrid[y][x].
# x, y are 1 based, as per the question
#
# returns a 'sumData': [sumList, x, y, squareSize]
def makeSumData(x, y, squareSize, powerGrid):
	sums = [sum(powerGrid[y - 1][x-1:x-1+squareSize]) for y in range(y, y + squareSize)]
	return [sums, x, y, squareSize]

# update the given sumlist according to a right-wise move
# gridDate is the power readings grid
def moveSumListRight(sumData, gridData):
	[sumList, x, y, squareSize] = sumData
	newX = x + 1
	# print('new x = %d (%d)' % (newX, newX + squareSize - 1) )
	if (newX + squareSize - 1) > gridWidth:
		print('moveSumListRight: Got given an x too large for grid for a right move! x = %d' % x)
		sys.exit(1)

	newColumn = newX + squareSize - 1

	amountsToRemove = [gridData[yy][x - 1] for yy in range(y - 1, y - 1 + squareSize)]
	amountsToAdd = [gridData[yy][newColumn - 1] for yy in range(y - 1, y - 1 + squareSize)]

	sumList = map(sub, sumList, amountsToRemove)
	sumList = list(map(add, sumList, amountsToAdd))
	
	return [sumList, newX, y, squareSize]


def moveSumListDown(sumData, gridData):
	[sumList, x, y, squareSize] = sumData
	newY = y + 1
	if (newY + squareSize - 1) > gridHeight:
		print('moveSumListDown: Got given a y too large for grid for a down move! y = %d' % y)
		sys.exit(1)

	# remove sumlist item from start of list, add new one at the end
	sumList = sumList[1:]
	summy = sum(gridData[y - 1 + squareSize][x-1:x-1+squareSize])

	sumList.append(summy)
	return [sumList, x, newY, squareSize]


def getPowerLevel(x, y, serialNumber):
	rackId = (x + 10)
	power = (rackId * y + serialNumber) * rackId

	if power < 100:
		powerPart = 0
	else:
		powerPart = int(str(power)[-3])

	powerPart -= 5
	return powerPart

for y in range(1, gridHeight + 1):
	row = []
	for x in range(1, gridWidth + 1):
		row.append(getPowerLevel(x, y, serialNumber))
	powerGrid.append(row)

# Part 1 is solved in a naive straightfoward manner
def solvePart1():
	powers = {}
	maxPower = -1
	tlX = -1
	tlY = -1

	for y in range(1, gridHeight - 1):
		for x in range(1, gridWidth - 1):
			power = 0
			for offsetX in range(0, 3):
				for offsetY in range(0, 3):
					power += powerGrid[y - 1 + offsetY][x - 1 + offsetX]
			if power > maxPower:
				maxPower = power
				tlX = x
				tlY = y

	print(' Part 1: coord = %d, %d' % (tlX, tlY))

# Part 2 needs a different approach, as the part 1 approach would just take too long.
# Although we could use scipy or numpy etc, I think part of the point is to solve
# the optimisation issue yourself.
def solvePart2():
	maxPowerSumData = None
	maxPower = None

	for squareSize in tqdm(range(1, 301)):
		sumData = makeSumData(1, 1, squareSize, powerGrid)

		for y in range(1, gridHeight + 2 - squareSize):
			if y > 1:
				sumData = moveSumListDown(sumData, powerGrid)

			workingSumData = deepcopy(sumData)

			for x in range(1, gridWidth + 2 - squareSize):
				if x > 1:
					workingSumData = moveSumListRight(workingSumData, powerGrid)

				sumList = workingSumData[0]
				powerSum = sum(sumList)
				if maxPower == None or powerSum > maxPower:
					maxPower = powerSum
					maxPowerSumList = workingSumData

	pt2x = maxPowerSumList[1]
	pt2y = maxPowerSumList[2]
	pt2squareSize = maxPowerSumList[3]
	print(' Part 2: max power = %d, for %d,%d,%d' % (maxPower, pt2x, pt2y, pt2squareSize))

solvePart1()
solvePart2()

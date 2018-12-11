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

from collections import Counter, defaultdict
from itertools import chain
from pprint import pprint
from copy import copy, deepcopy
from itertools import repeat
from functools import reduce
import sys
from operator import sub, add

gridWidth = 300
gridHeight = 300

enableLog = True

def logPrint(str):
	if enableLog:
		print(str, end='')

# powergrid is a 2d array, addressed as powerGrid[y][x].
# x, y are 1 based, as per the question
#
# returns a 'sumData': [sumList, x, y, squareSize]
def makeSumList(x, y, squareSize, powerGrid):
	# we want a list of sums, e.g. for squareSize = 3, we might have [3, 18, 9]
	sums = [reduce(lambda x, y: x+y, powerGrid[y - 1][x-1:x-1+squareSize]) for y in range(y, y + squareSize)]
	return [sums, x, y, squareSize]

# update the given sumlist according to a right-wise move
# gridDate is the power readings grid
def moveSumListRight(sumData, gridData):
	[sumList, x, y, squareSize] = sumData
	# print('got ', sumList, x, y, squareSize)
	# print('griddata = %s' % gridData)
	newX = x + 1
	# print('new x = %d (%d)' % (newX, newX + squareSize - 1) )
	if (newX + squareSize - 1) > gridWidth:
		print('moveSumListRight: Got given an x too large for grid for a right move! x = %d' % x)
		sys.exit(1)

	newColumn = newX + squareSize - 1

	# print('y range = %s' % range(y - 1, y - 1 + squareSize))
	# print('newColumn = %d' % newColumn)
	# print('gridY = %s' % gridData[y])
	# update sums
	amountsToRemove = [gridData[yy][x - 1] for yy in range(y - 1, y - 1 + squareSize)]
	# print('amountsToRemove = %s' % amountsToRemove)
	amountsToAdd = [gridData[yy][newColumn - 1] for yy in range(y - 1, y - 1 + squareSize)]
	# print('amountsToAdd = %s' % amountsToAdd)

	sumList = map(sub, sumList, amountsToRemove)
	sumList = list(map(add, sumList, amountsToAdd))
	
	# print('new sumlist: %s' % sumList)

	return [sumList, newX, y, squareSize]


def moveSumListDown(sumData, gridData):
	[sumList, x, y, squareSize] = sumData
	# print('got ', sumList, x, y, squareSize)
	# print('griddata = %s' % gridData)
	newY = y + 1
	# print('new y = %d (%d)' % (newY, newY + squareSize - 1) )
	if (newY + squareSize - 1) > gridHeight:
		print('moveSumListDown: Got given a y too large for grid for a down move! y = %d' % y)
		sys.exit(1)

	# remove sumlist item from start of list, add new one at the end
	sumList = sumList[1:]

	vals = gridData[y - 1 + squareSize][x-1:x-1+squareSize]
	summy = reduce(lambda x, y: x+y, vals)
	# print('down move: vals, sum =%s, %s' % (vals, summy))

	sumList.append(summy)
	# print(' after move down, sumlist = %s' % sumList)
	return [sumList, x, newY, squareSize]

def testSumLists():
	sampleGrid = [[0,1,2],
	              [3,4,5],
	              [6,7,8]]

	print(makeSumList(1, 1, 2, sampleGrid) )
	print(makeSumList(2, 1, 2, sampleGrid) )
	print(makeSumList(1, 2, 2, sampleGrid) )

def testSumListsMove():
	global gridWidth
	global gridHeight

	gridWidth = 4
	gridHeight = 4
	
	sampleGrid4 = [[0,1,2,3],
	              [4,5,6,7],
	              [8,9,10,11],
	              [12,13,14,15]]
	#ORIG: 3, 5, 27
	#new expected after right move: 6, 18, 30
	s = makeSumList(1, 1, 3, sampleGrid4)
	print('starting sumlist = %s' % s)

	moveRightSumlist = moveSumListRight(s, sampleGrid4)
	print('move right sumlist = %s' % moveRightSumlist)

	moveDownSumlist = moveSumListDown(s, sampleGrid4)
	print('move down sumlist = %s' % moveDownSumlist)

	sys.exit(1)

# for testing
# testSumListsMove()

# testSumLists()

# reduce(lambda x, y: x+y, metadata)

# serialNumber = 9221

# x = 33
# y = 45

# Find the fuel cell's rack ID, which is its X coordinate plus 10.
# Begin with a power level of the rack ID times the Y coordinate.
# Increase the power level by the value of the grid serial number (your puzzle input).
# Set the power level to itself multiplied by the rack ID.
# Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
# Subtract 5 from the power level.

# rackId = (x + 10)
# power = rackId * y
# power = rackId + serialNumber
# power *= rackId

serialNumber = 9221

# gridWidth = 5
# gridHeight = 5

def getPowerLevel(x, y, serialNumber):
	# return (y - 1) * gridWidth + x - 1	
	rackId = (x + 10)
	power = (rackId * y + serialNumber) * rackId

	if power < 100:
		powerPart = 0
	else:
		powerPart = int(str(power)[-3])

	powerPart -= 5
	# print(' power, powerPart = %s, %s' % (power, powerPart))
	return powerPart

print(getPowerLevel(122, 79, 57))
print(getPowerLevel(217, 196, 39))
print(getPowerLevel(101, 153, 71))

cols = []
for y in range(1, gridHeight + 1):
	row = []
	for x in range(1, gridWidth + 1):
		row.append(getPowerLevel(x, y, serialNumber))
	cols.append(row)

# print('done, data =%s', cols)
# print('thart cioord = %d' % cols[1][3])
# sys.exit(1)

# up to here:
# 5x5 is structured as:
# [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21, 22, 23, 24]]
# i.e. data[y][x] is how you index it.

# correct:
# print('that square = %d' % cols[32][44])
# print('that square = %d' % cols[32][45])
# print('that square = %d' % cols[32][46])

# print('that square = %d' % cols[33][44])
# print('that square = %d' % cols[33][45])
# print('that square = %d' % cols[33][46])

def solvePart1():
	powers = {}
	maxPower = -1
	tlX = -1
	tlY = -1
	# calc powers, naive way
	for y in range(1, gridHeight - 1):
		for x in range(1, gridWidth - 1):
			power = 0
			for offsetX in range(0, 3):
				for offsetY in range(0, 3):
					# -1 for the 1 based stuff!
					power += cols[y - 1 + offsetY][x - 1 + offsetX]
			if power > maxPower:
				maxPower = power
				tlX = x
				tlY = y

	# print('max pow = %d, coords %d %d' % (maxPower, tlX, tlY))
	print(' Part 1: coord = %d, %d' % (tlX, tlY))


solvePart1()

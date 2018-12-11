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
from tqdm import tqdm

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
def makeSumData(x, y, squareSize, powerGrid):
	# we want a list of sums, e.g. for squareSize = 3, we might have [3, 18, 9]
	# TODO just call sum here! no need for reduce
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

	print(makeSumData(1, 1, 2, sampleGrid) )
	print(makeSumData(2, 1, 2, sampleGrid) )
	print(makeSumData(1, 2, 2, sampleGrid) )

def testSumListsMove():
	global gridWidth
	global gridHeight

	gridWidth = 4
	gridHeight = 4
	
	sampleGrid4 = [[0,1,2,3],
	              [4,5,6,7],
	              [8,9,10,11],
	              [12,13,14,15]]

	# s = makeSumData(1, 1, 1, sampleGrid4)
	# s = makeSumData(1, 1, 2, sampleGrid4)
	s = makeSumData(1, 1, 2, sampleGrid4)
	print('starting sumlist = %s' % s)

	moveRightSumlist = moveSumListRight(s, sampleGrid4)
	print('move right sumlist = %s' % moveRightSumlist)

	moveRightSumlist = moveSumListRight(moveRightSumlist, sampleGrid4)
	print('2nd move right sumlist = %s' % moveRightSumlist)

	moveDownSumlist = moveSumListDown(s, sampleGrid4)
	print('move down sumlist = %s' % moveDownSumlist)

	moveDownSumlist = moveSumListDown(moveDownSumlist, sampleGrid4)
	print('2nd move down sumlist = %s' % moveDownSumlist)

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

# serialNumber = 9221
serialNumber = 18

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

# debug cols
#checks out:
# dbgX = 32
# dbgY = 44

# dbgX = 0
# dbgY = 0
# for y in range(dbgY, dbgY+6):
# 	print('y:%d %s' % (y, cols[y][dbgX:dbgX+6]))

# s = makeSumData(1, 1, 3, cols)
# print('starting sumlist = %s' % s)

# moveRightSumlist = moveSumListRight(s, cols)
# print('move right sumlist = %s' % moveRightSumlist)

# moveRightSumlist = moveSumListRight(moveRightSumlist, cols)
# print('2nd move right sumlist = %s' % moveRightSumlist)

# moveRightThenDownSumlist = moveSumListDown(moveRightSumlist, cols)
# print('2nd move right then down sumlist = %s' % moveRightThenDownSumlist)

# moveDownSumlist = moveSumListDown(s, cols)
# print('move down sumlist = %s' % moveDownSumlist)

# moveDownSumlist = moveSumListDown(moveDownSumlist, cols)
# print('2nd move down sumlist = %s' % moveDownSumlist)

# moveDownThenRightSumlist = moveSumListRight(moveDownSumlist, cols)
# print('2nd move down then right sumlist = %s' % moveDownThenRightSumlist)

# sys.exit(1)

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


def solvePart2():
	maxPowerSumData = None
	maxPower = None

	print(cols[45][33:33+5])
	print(cols[46][33:33+5])
	print(cols[47][33:33+5])
	print(cols[48][33:33+5])
	print(cols[49][33:33+5])

	print('======== blip')
	print(cols[33][45:45+5])
	print(cols[34][45:45+5])
	print(cols[35][45:45+5])
	print(cols[36][45:45+5])
	print(cols[37][45:45+5])

	# REMINDER: 44,32 CORRESPONDS to 33, 45 as stated in puzzle! off by 1, and y, x ordering.
	print('zap: %d' % cols[44][32])
	print('zap: %d' % cols[45][33])
	print('zap: %d' % cols[46][34])
	# try large square for now
	# for squareSize in tqmd(range(1, 300)): #301):

	for squareSize in tqdm(range(1, 301)):
	# print('============================ squareSize: %d' % squareSize)
		sumData = makeSumData(1, 1, squareSize, cols)

		for y in range(1, gridHeight + 2 - squareSize):
			if y > 1:
				sumData = moveSumListDown(sumData, cols)

			workingSumData = deepcopy(sumData)

			for x in range(1, gridWidth + 2 - squareSize):
				if x > 1:
					workingSumData = moveSumListRight(workingSumData, cols)

				sumList = workingSumData[0]
				powerSum = sum(sumList)
				# print('working on x, y = %d, %d, sumData = %s, total power = %d' % (x, y, sumData[1:], powerSum))
				if maxPower == None or powerSum > maxPower:
					maxPower = powerSum
					# don't store the actual sumlist, skip that bit
					maxPowerSumList = workingSumData

	pt2x = maxPowerSumList[1] #- 1
	pt2y = maxPowerSumList[2] #- 1
	pt2squareSize = maxPowerSumList[3]
	print(' Part 2: max power = %d, for %d,%d,%d' % (maxPower, pt2x, pt2y, pt2squareSize))

	#Part 2: max power = 21, for [270, 2, 4]
	#270,2,4 is incorrect!
solvePart1()
solvePart2()

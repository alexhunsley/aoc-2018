# solve.py 13
#
# We are using 0 based coords internally.
#
# do carts always appear on straight sections in the input? I assume so.
#
# Observation: if we store all +, / and \ locations, we can disregard 
# the straight section markers | and -. So more efficient sparse 
# storage of where the former 3 items occur.
#

from collections import Counter, defaultdict
from itertools import chain
import pprint
from copy import copy, deepcopy
from itertools import repeat
from functools import reduce
import sys

enableLog = True

def logPrint(str):
	if enableLog:
		print(str)

# lines = [x.strip() for x in f.readlines()]

carts = []

cartStartsToVelocities = {'>': [ 1,  0],
					      '<': [-1,  0],
					      '^': [ 0, -1],
					      'v': [ 0,  1]
}

lines = []
allCartChars = ''.join(cartStartsToVelocities.keys())

crossingLocs = []
slashLocs = []
bslashLocs = []

crossingDirections = [[]]

def rotateVelLeft(v):
	return [v[1], -v[0]]

def rotateVelRight(v):
	return [-v[1], v[0]]

# test = [1, 0]
# for i in range(0, 5):
# 	print(test)
# 	test = rotateVelRight(test)
# 	# test = rotateVelLeft(test)
# sys.exit(1)

def adjustCartVelocityForCrossing(cartData):
	behav = cartData[2]
	if behav == 0:
		cartData[1] = rotateVelLeft(cartData[1])
	elif behav == 1:
		# no change, keep on going straight ahead
		pass
	else:
		cartData[1] = rotateVelRight(cartData[1])
	
	# bump up behaviour flag (3 kinds of behaviour)
	cartData[2] = (cartData[2] + 1) % 3

def adjustCartVelocityForSlash(cartData):
	# if moving vertically, a rotate right does it. Otherwise, rot left.
	if cartData[1][1] != 0:
		cartData[1] = rotateVelRight(cartData[1])
	else:
		cartData[1] = rotateVelLeft(cartData[1])


def adjustCartVelocityForBSlash(cartData):
	if cartData[1][1] != 0:
		cartData[1] = rotateVelLeft(cartData[1])
	else:
		cartData[1] = rotateVelRight(cartData[1])


def readInput():
	global mapSize
	global lines

	# f = open("input.txt")
	f = open("shortExample.txt")

	lines = f.readlines()
	mapSize = (len(lines[0].rstrip("\r\n")), len(lines))
	print('map size =', mapSize)

	lineIndex = 0
	for l in lines:
		print("%s" % l, end='')

		# find all occurence of cart chars
		for (cartChar, startVel) in cartStartsToVelocities.items():
			cartXPositions = [pos for pos, char in enumerate(l) if char == cartChar]
			for cartXPos in cartXPositions:
				# final 0 is the behaviour index (for + crossings)
				carts.append([[cartXPos, lineIndex], startVel, 0])

		# read +
		crossingPositions = [pos for pos, char in enumerate(l) if char == '+']
		for crossPos in crossingPositions:
			print('================= adding a cross oc: %s' % [crossPos, lineIndex])
			crossingLocs.append([crossPos, lineIndex])


		# read /
		slashPositions = [pos for pos, char in enumerate(l) if char == '/']
		print('=== read slash positions:', slashPositions)
		for slashPos in slashPositions:
			slashLocs.append([slashPos, lineIndex])

		# read \
		bslashPositions = [pos for pos, char in enumerate(l) if char == '\\']
		print('=== read bslash positions:', bslashPositions)
		for bslashPos in bslashPositions:
			bslashLocs.append([bslashPos, lineIndex])

		lineIndex += 1

# returns True if collision
def doTimestep():
	global carts
	global crossingLocs
	newCartLocs = []
	for lineNum in range(0, mapSize[1]):
		# find all carts on this line, try to move them
		print('processing line ', lineNum)
		cartsOnThisLine = [c for c in carts if c[0][1] == lineNum]
		print('carts on this line: ', cartsOnThisLine)
		for c in cartsOnThisLine:
			# special char?
			print('c locs = %s' % crossingLocs)
			if c[0] in crossingLocs:
				print(' processing a CROSS at %s' % c[0])
				adjustCartVelocityForCrossing(c)
			if c[0] in slashLocs:
				print(' processing a SLASH at %s' % c[0])
				adjustCartVelocityForSlash(c)
			if c[0] in bslashLocs:
				print(' processing a B-SLASH at %s' % c[0])
				adjustCartVelocityForBSlash(c)


			newLoc = [c[0][0] + c[1][0], c[0][1] + c[1][1]]
			print('check for loc %s in cart locs %s' % (newLoc, [cc[0] for cc in carts]))
			# collision?
			collidedCarts = [cart for cart in carts if cart[0] == newLoc]
			if collidedCarts:
				return newLoc
			collidedCarts = [ncart for ncart in newCartLocs if ncart[0] == newLoc]
			if collidedCarts:
				return newLoc
			newCartLocs.append([newLoc, c[1], c[2]])
	carts = newCartLocs
	return None

def solvePart1():
	while (not doTimestep()):
		pass

readInput()
print('after read input, carts = ', carts)
print('after read input, cLocs= ', crossingLocs)

def printMap():
	cartLocs = [ c[0] for c in carts ]

	for y in range (0, mapSize[1]):
		for x in range (0, mapSize[0]):
			if [x, y] in cartLocs:
				print('*', end='')
			else:
				print(lines[y][x], end='')
		print('')


for i in range(0, 20):
	printMap()
	collisionCoord = doTimestep()
	print('after timestep %d, carts = %s' % (i, carts))
	if collisionCoord != None:
		print(' Part 1: Collision at at %s (time = %s)' % (collisionCoord, i))
		sys.exit(1)
	print('----------------------------------------------------------')

# sys.exit(1)
# solvePart1()


print('\n====end')
print("carts = %s" % carts)
print("crossLocs = %s" % crossingLocs)
print("slashLocs = %s" % slashLocs)
print("bslashLocs = %s" % bslashLocs)



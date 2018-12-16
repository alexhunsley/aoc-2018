# solve.py 13
#
# Carts always appear on straight sections in the input.
#
# Observation: if we store all +, / and \ locations, we can disregard 
# the straight section markers | and -. So can have more efficient sparse 
# storage of where the former 3 items occur.
#

import sys
from copy import deepcopy
from types import SimpleNamespace
from enum import IntEnum

class CrossingBehaviour(IntEnum):
			TURNLEFT = 0
			STRAIGHTON = 1
			TURNRIGHT = 2


# SimpleNamespace to represent a cart object:
# pos, vel, behavIndex, id

# inputFile = "debugEx1.txt"
# inputFile = "debugEx2.txt"
# inputFile = "debugEx3.txt"
# inputFile = "debugEx4.txt"
inputFile = "input.txt"
# inputFile = "shortExample.txt"


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

def rotateVelLeft(v):
	return [v[1], -v[0]]

def rotateVelRight(v):
	return [-v[1], v[0]]

def adjustCartVelocityForCrossing(cartData):
	if cartData.behavIndex == CrossingBehaviour.TURNLEFT:
		cartData.vel = rotateVelLeft(cartData.vel)
	elif cartData.behavIndex == CrossingBehaviour.STRAIGHTON:
		# no change, keep on going straight ahead
		pass
	else: # cartData.behavIndex == CrossingBehaviour.TURNRIGHT
		cartData.vel = rotateVelRight(cartData.vel)
	
	# bump up behaviour flag (3 kinds of behaviour)
	cartData.behavIndex = (cartData.behavIndex + 1) % 3

def adjustCartVelocityForSlash(cartData):
	# if moving vertically, a rotate right does it. Otherwise, rot left.
	if cartData.vel[1] != 0:
		cartData.vel = rotateVelRight(cartData.vel)
	else:
		cartData.vel = rotateVelLeft(cartData.vel)


def adjustCartVelocityForBSlash(cartData):
	if cartData.vel[1] != 0:
		cartData.vel = rotateVelLeft(cartData.vel)
	else:
		cartData.vel = rotateVelRight(cartData.vel)

def readInput():
	global mapSize
	global lines

	f = open(inputFile)

	lines = f.readlines()
	mapSize = (len(lines[0].rstrip("\r\n")), len(lines))
	print('map size =', mapSize)

	cartIndex = 0
	for lineIndex, l in enumerate(lines):
		# find all occurence of cart chars to create carts
		for (cartChar, startVel) in cartStartsToVelocities.items():
			cartXPositions = [pos for pos, char in enumerate(l) if char == cartChar]
			for cartXPos in cartXPositions:
				#'processed' property is used during a processing scan, to avoid moving something twice
				c = SimpleNamespace(pos=[cartXPos, lineIndex], vel=startVel, behavIndex=CrossingBehaviour.TURNLEFT, processed=False, id=cartIndex)
				carts.append(c)
				cartIndex += 1

		# read + items
		crossingPositions = [pos for pos, char in enumerate(l) if char == '+']
		for crossPos in crossingPositions:
			# print('================= adding a cross oc: %s' % [crossPos, lineIndex])
			crossingLocs.append([crossPos, lineIndex])


		# read / items
		slashPositions = [pos for pos, char in enumerate(l) if char == '/']
		# print('=== read slash positions:', slashPositions)
		for slashPos in slashPositions:
			slashLocs.append([slashPos, lineIndex])

		# read \ items
		bslashPositions = [pos for pos, char in enumerate(l) if char == '\\']
		# print('=== read bslash positions:', bslashPositions)
		for bslashPos in bslashPositions:
			bslashLocs.append([bslashPos, lineIndex])

def vecAdd(a, b):
	return map(sum, zip(a,b))

seenFirstCrash = False

def doTimestep():
	global seenFirstCrash
	global carts
	global oldCarts
	stopAfterThisTick = False
	if len(carts) == 1:
		stopAfterThisTick = True

	global crossingLocs

	for c in carts:
		c.processed = False

	for lineNum in range(0, mapSize[1]):
		cartsOnThisLine = [c for c in carts if not(c.processed) and c.pos[1] == lineNum]

		# sort carts on line by ascending X
		cartsOnThisLine.sort(key=lambda g: g.pos[0])

		while cartsOnThisLine:
			c = cartsOnThisLine.pop(0)
			c.processed = True

			if c.pos in crossingLocs:
				# print(' processing a CROSS at %s' % c[0])
				adjustCartVelocityForCrossing(c)
			if c.pos in slashLocs:
				# print(' processing a SLASH at %s' % c[0])
				adjustCartVelocityForSlash(c)
			if c.pos in bslashLocs:
				# print(' processing a B-SLASH at %s' % c[0])
				adjustCartVelocityForBSlash(c)

			newLoc = list(vecAdd(c.pos, c.vel))

			collidedCarts = [b for b in carts if b.pos == newLoc]
			if collidedCarts:
				cCart = collidedCarts[0]

				if not seenFirstCrash:
					seenFirstCrash = True
					print(' Part 1: first crash loc =', newLoc)

				carts.remove(cCart)
				carts.remove(c)
				
				if cCart in cartsOnThisLine:
					cartsOnThisLine.remove(cCart)
				if c in cartsOnThisLine:
					cartsOnThisLine.remove(c)
				if cCart in carts:
					carts.remove(cCart)
				if c in carts:
					carts.remove(c)
				
			c.pos = newLoc

	if len(carts) == 1:
		print('DID FINAL TICK. final cart state is: ', carts[0])
		sys.exit(1)

	return None

def solvePart1and2():
	loopIndex = 0
	while (True):
		loopIndex += 1

		if loopIndex % 200 == 0:
			print('loop: %d, num carts = %d' % (loopIndex, len(carts)))

		doTimestep()

def printMap():
	cartLocs = [ c.pos for c in carts ]
	for y in range (0, mapSize[1]):
		for x in range (0, mapSize[0]):
			if [x, y] in cartLocs:
				cartItem = [c for c in carts if c.pos == [x, y]][0]
				print('%s' % cartItem.id, end='')
			else:
				line = lines[y][x]
				print(line, end='')
		print('')

readInput()
solvePart1and2()

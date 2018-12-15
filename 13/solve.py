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
from copy import deepcopy
from types import SimpleNamespace

# SimpleNamespace to represent a cart object:
# pos, vel, behavIndex, id, 

# inputFile = "debugEx1.txt"
# inputFile = "debugEx2.txt"
# inputFile = "debugEx3.txt"
# inputFile = "debugEx4.txt"
inputFile = "input.txt"
# inputFile = "shortExample.txt"

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
	if cartData.behavIndex == 0:
		cartData.vel = rotateVelLeft(cartData.vel)
	elif cartData.behavIndex == 1:
		# no change, keep on going straight ahead
		pass
	else: # cartData.behavIndex == 3
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

	lineIndex = 0
	cartIndex = 0
	for l in lines:
		# print("%s" % l, end='')

		# find all occurence of cart chars
		for (cartChar, startVel) in cartStartsToVelocities.items():
			cartXPositions = [pos for pos, char in enumerate(l) if char == cartChar]
			for cartXPos in cartXPositions:
				# final 0 is the behaviour index (for + crossings)

				#pos, vel, behav mode (0-2), processed, id
				#'processed' is used during a processing scan, to avoid moving something twice
				c = SimpleNamespace(pos=[cartXPos, lineIndex], vel=startVel, behavIndex=0, processed=False, id=cartIndex)
				carts.append(c)
				cartIndex += 1

		# read +
		crossingPositions = [pos for pos, char in enumerate(l) if char == '+']
		for crossPos in crossingPositions:
			# print('================= adding a cross oc: %s' % [crossPos, lineIndex])
			crossingLocs.append([crossPos, lineIndex])


		# read /
		slashPositions = [pos for pos, char in enumerate(l) if char == '/']
		# print('=== read slash positions:', slashPositions)
		for slashPos in slashPositions:
			slashLocs.append([slashPos, lineIndex])

		# read \
		bslashPositions = [pos for pos, char in enumerate(l) if char == '\\']
		# print('=== read bslash positions:', bslashPositions)
		for bslashPos in bslashPositions:
			bslashLocs.append([bslashPos, lineIndex])

		lineIndex += 1

def vecAdd(a, b):
	return map(sum, zip(a,b))

seenFirstCrash = False

# returns True if collision
def doTimestep():
	global seenFirstCrash
	global carts
	global oldCarts
	stopAfterThisTick = False
	if len(carts) == 1:
		stopAfterThisTick = True

	global crossingLocs

	# reset processing status for every cart
	for c in carts:
		c.processed = False


	for lineNum in range(0, mapSize[1]):
		cartsOnThisLine = [c for c in carts if not(c.processed) and c.pos[1] == lineNum]
		# print('carts on this line:', cartsOnThisLine)

		# sort ascending X
		cartsOnThisLine.sort(key=lambda g: g.pos[0])

		while cartsOnThisLine:
			c = cartsOnThisLine.pop(0)
			# print('   single cart:', c)
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
			# print('new loc for %d is = %s' % (c.id, newLoc))
			# print('>>> checking for coll: this = %s, all = ' % c)
			# for p in carts:
			# 	print(p)
			collidedCarts = [b for b in carts if b.pos == newLoc]
			if collidedCarts:
				cCart = collidedCarts[0]

				if not seenFirstCrash:
					seenFirstCrash = True
					print(' Part 1: first crash loc =', newLoc)

				# print('coll cart: ', cCart)
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


				# print('>>> AFTER REMOVE crashed ones: all = ')
				# for p in carts:
				# 	print(p)
				
			c.pos = newLoc

	if stopAfterThisTick:
		printMap()
		print('DID FINAL TICK. final cart state is then = ', carts[0])
		sys.exit(1)

	return None

#part 2: 65,42 is wrong.
#65,43 also.
def solvePart1():
	while (not doTimestep()):
		pass

readInput()
print('after read input, # carts = ', len(carts))
# print('after read input, cLocs= ', crossingLocs)


def mapStr():
	s = ''
	cartLocs = [ c.pos for c in carts ]

	for y in range (0, mapSize[1]):
		for x in range (0, mapSize[0]):
			if [x, y] in cartLocs:
				cartItem = [c for c in carts if c.pos == [x, y]][0]
				# print('matched:', cartItem)
				s += '%s' % cartItem[3]
			else:
				s += lines[y][x]
		s += '\n'
	return s


def printMap():
	cartLocs = [ c.pos for c in carts ]

	for y in range (0, mapSize[1]):
		for x in range (0, mapSize[0]):
			if [x, y] in cartLocs:
				cartItem = [c for c in carts if c.pos == [x, y]][0]
				# print('matched:', cartItem)
				print('%s' % cartItem.id, end='')
			else:
				line = lines[y][x]
				# line = lines[y][x].replace('|', ' ').replace('-', ' ')
				print(line, end='')
		print('')
		# print('startLine:', end='')


# doTimestep()
# printMap()
# sys.exit(1)

loopIndex = 0
while (True):
	loopIndex += 1

	if loopIndex % 200 == 0:
		print('loop: %d, num carts = %d' % (loopIndex, len(carts)))

	doTimestep()


#44, 57 is not right.
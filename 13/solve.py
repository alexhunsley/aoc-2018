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


enableLog = True

def logPrint(str):
	if enableLog:
		print(str)

# f = open("input.txt")
f = open("shortExample.txt")

lines = f.readlines()
# lines = [x.strip() for x in f.readlines()]

carts = []

cartStartsToVelocities = {'>': ( 1,  0),
					      '<': (-1,  0),
					      '^': ( 1, -1),
					      'v': ( 1,  1)
}

crossingLocs = []
slashLocs = []
bslashLocs = []

lineIndex = 0
for l in lines:
	print("%s" % l, end='')

	# find all occurence of cart chars
	for (cartChar, startVel) in cartStartsToVelocities.items():
		cartXPositions = [pos for pos, char in enumerate(l) if char == cartChar]
		for cartXPos in cartXPositions:
			carts.append([(cartXPos, lineIndex), startVel])

	cartXPositions = [pos for pos, char in enumerate(l) if char == cartChar]
	for cartXPos in cartXPositions:
		carts.append([(cartXPos, lineIndex), startVel])

	# read +
	crossingPositions = [pos for pos, char in enumerate(l) if char == '+']
	for crossPos in crossingPositions:
		crossingLocs.append([(crossPos, lineIndex)])


	# read /
	slashPositions = [pos for pos, char in enumerate(l) if char == '/']
	for slashPos in slashPositions:
		slashLocs.append([(slashPos, lineIndex)])

	# read \
	bslashPositions = [pos for pos, char in enumerate(l) if char == '\\']
	for bslashPos in bslashPositions:
		bslashLocs.append([(bslashPos, lineIndex)])

	lineIndex += 1

print('\n====end')
print("carts = %s" % carts)
print("crossLocs = %s" % crossingLocs)
print("slashLocs = %s" % slashLocs)
print("bslashLocs = %s" % bslashLocs)



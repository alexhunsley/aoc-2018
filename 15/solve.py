# solve.py
#

from collections import Counter, defaultdict
from itertools import chain
import pprint
from copy import copy, deepcopy
from itertools import repeat
from functools import reduce
from types import SimpleNamespace
from enum import IntEnum

enableLog = True

def logPrint(str):
	if enableLog:
		print(str, end='')

# f = open("input.txt")
f = open("testShortestDistInput.txt")

mobs = []
mobChars = ['E', 'G']

lines = f.readlines()

mapSize = (len(lines[0].rstrip("\r\n")), len(lines))

for lineIndex, line in enumerate(lines):
	line = line.strip()

	plainLine = line
	for mobChar in mobChars:
		plainLine = plainLine.replace(mobChar, '.')
		mobPositions = [pos for pos, char in enumerate(line) if char == mobChar]
		print('mob pos', mobPositions)
		for m in mobPositions:
			m = SimpleNamespace(kind = mobChar, pos = [m, lineIndex])
			mobs.append(m)
	# print(plainLine)
				# c = SimpleNamespace(pos=[cartXPos, lineIndex], vel=startVel, behavIndex=CrossingBehaviour.TURNLEFT, processed=False, id=cartIndex)


def printMap():
	mobInfo = [ [m.pos, m.kind] for n in mobs ]
	
	for y in range (0, mapSize[1]):
		for x in range (0, mapSize[0]):
			mobKinds = [m.kind for m in mobs if m.pos == [x, y]]

			if mobKinds:
				print('%s' % mobKinds[0], end='')
			else:
				print(lines[y][x], end='')

		print('')

def printMapWithDists():
	mobInfo = [ [m.pos, m.kind] for n in mobs ]
	
	for y in range (0, mapSize[1]):
		for x in range (0, mapSize[0]):
			if (x, y) in shortestDistMap:
				print('%s' % repr(shortestDistMap[(x, y)]).ljust(3), end='')
			else:
				print('%s  ' % lines[y][x], end='')

		print('')

def sortedMobs():
	# left to right, top to bottom order (i.e. reading order)
	return sorted(mobs, key=lambda m: m.pos[0] + m.pos[1] * mapSize[0])

# while (any targets remain):
#  each unit turn:
#   in range?
#.    attack
#.  else
#.    any open squares NSEW of target?
#.      move there
#     else
#       end turn

printMap()
# print('mobs = ', mobs)

print('sroted mobs =', sortedMobs())

shortestDistMap = {}
# calcShortestDist([9, 4], [7, 7], 0)

neighbourCells = [[-1, 0], [1, 0], [0, -1], [0, 1]]

def calcShortestDist(a, distAccum):
	print('calc shortest dist: a = ', a, ' accum = ', distAccum)
	if (not a in shortestDistMap or shortestDistMap[a] > distAccum):
		shortestDistMap[a] = distAccum
	else:
		return

	for cell in neighbourCells:
		c = [a[0] + cell[0], a[1] + cell[1]]
		print('calc c=', c)
		if lines[ c[1] ][ c[0] ] == '.':
			calcShortestDist((c[0], c[1]), distAccum + 1)

calcShortestDist((8, 3), 0)

print('dists: ', shortestDistMap)

printMapWithDists()
# 	x = line[10:16].strip()
# 	y = line[17:24].strip()
	
# 	print("!%s,%s!" % (x, y))



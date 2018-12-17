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

f = open("input.txt")

map = []
mobs = []
mobChars = ['E', 'G']

lines = f.readlines()

mapSize = (len(lines[0].rstrip("\r\n")), len(lines))

for lineIndex, line in enumerate(f.readlines()):
	line = line.strip()

	plainLine = line
	for mobChar in mobChars:
		plainLine = plainLine.replace(mobChar, '.')
		mobPositions = [pos for pos, char in enumerate(line) if char == mobChar]

		for m in mobPositions:
			m = SimpleNamespace(kind = mobChar, pos = [m, lineIndex])
			mobs.append(m)
	print(plainLine)
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

print('mobs = ', mobs)
printMap()


# 	x = line[10:16].strip()
# 	y = line[17:24].strip()
	
# 	print("!%s,%s!" % (x, y))



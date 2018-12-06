# solve.py 6
#
import sys
from operator import methodcaller
from functools import reduce
from collections import Counter

f = open("input.txt")

# contents = f.readlines()

# f.close()

# # temp, just to keep stuff simpler

# print(contents)
# # contents = [[lineIndex] for lineIndex in range(0, 3)]
# # contents = [list(lineIndex) for lineIndex in range(0, len(contents))]
# # contents = [[lineIndex].append(contents[lineIndex]) for lineIndex in range(0, len(contents))]

# # print('new contents: ', contents)
# # sys.exit(1)

# # map in py3 returns an iterable!

# # contents = [[lineIndex, contents[lineIndex]] for lineIndex in range(0, len(contents))]
# # print('with line indexes: ', contents)

# # the inner map converts the list of coordinates from string pairs to int pairs
# # coords = list(map(lambda line: list(map(int, line.rstrip().replace(' ', '').split(','))), contents))
# coords = list(map(lambda lineIndex: list(map(int, contents[lineIndex].rstrip().replace(' ', '').split(','))), range(0, len(contents))))

coords = []

lineIndex = 0
for line in f.readlines():
	coordsAsList = list(map(int, line.rstrip().replace(' ', '').split(',')))
	coords.append(coordsAsList)
	lineIndex += 1

# coords = coords[0:2]
# coords = [(10,10), (11, 14), (12,12)]
# coords = [(10,10), (19, 18), (12,12)]

coords = [
	[1, 1],
	[1, 6],
	[8, 3],
	[3, 4],
	[5, 5],
	[8, 9]
]

print('coords: ', coords)
# print("it is", [item for item in coords])

minX = reduce(min, [item[0] for item in coords])
maxX = reduce(max, [item[0] for item in coords])
minY = reduce(min, [item[1] for item in coords])
maxY = reduce(max, [item[1] for item in coords])

print('bounds: ', minX, minY, maxX, maxY)

print
print

border = 1

for y in range(minY - border, maxY + 1 + border):
	for x in range(minX - border, maxX + 1 + border):
		# pass

		dists = [(abs(x - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]

		# print('x,y =', x, y)
		# print(' dists =', dists)

		distancesCounter = Counter(dists)

		# take away any distances that appear more than once
		# (either works!)
		uniqueDistances = [dist for dist in distancesCounter if distancesCounter[dist] == 1]
		# uniqueDistances = list(filter(lambda x: distancesCounter[x] == 1, distancesCounter))

		uniqueDistances.sort()

		# print('uniqueDistances = ', uniqueDistances)
		assert uniqueDistances

		indexOfClosestCoord = dists.index(uniqueDistances[0])
		# print('closest coord index= ', indexOfClosestCoord, ' from this array: ', dists)

		if (uniqueDistances[0] == 0):
			# print('*', end='')
			print(chr(ord('A') + indexOfClosestCoord), end='')
		else:
			print(indexOfClosestCoord, end='')
	print('')

# we can't discount the infinite area items yet - need to take them into account when calculating the distances.
# we remove them from consideration when considering the highest area region


# for x in range()
# methodcaller("int")
# print(stuff)


# minX = 9999
# maxX = -9999
# minY = 9999
# maxY = -9999

# for coord in coords:
# 	minX = min(coord[0], minX)
# 	minY = min(coord[1], minY)
# 	maxX = max(coord[0], maxX)
# 	maxY = max(coord[1], maxY)

# print('AB\n'.rstrip() + "X")

# print("it is", [item[0] for item in list(coords)])

# print(reduce((lambda x, y: x * y), [1, 2, 3, 4]))
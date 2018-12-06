# solve.py 6
#
import sys
from operator import methodcaller
from functools import reduce

f = open("input.txt")

contents = f.readlines()

f.close()

print(contents)
# temp, just to keep stuff simpler
contents = contents[0:2]
# contents = [[lineIndex] for lineIndex in range(0, 3)]
# contents = [list(lineIndex) for lineIndex in range(0, len(contents))]
# contents = [[lineIndex].append(contents[lineIndex]) for lineIndex in range(0, len(contents))]

# print('new contents: ', contents)
# sys.exit(1)

# map in py3 returns an iterable!

# the inner map converts the list of coordinates from string pairs to int pairs
coords = list(map(lambda line: list(map(int, line.rstrip().replace(' ', '').split(','))), contents))
print('coords: ', coords)
# print("it is", [item for item in coords])

minX = reduce(min, [item[0] for item in coords])
maxX = reduce(max, [item[0] for item in coords])
minY = reduce(min, [item[1] for item in coords])
maxY = reduce(max, [item[1] for item in coords])

print('bounds: ', minX, minY, maxX, maxY)

x = 86
y = 215

dists = [(abs(x - targetX) + abs(y - targetY)) for (targetX, targetY) in coords]
print('dists = ', dists)


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
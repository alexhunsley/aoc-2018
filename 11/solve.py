# solve.py
#

# Input: 9221

from collections import Counter, defaultdict
from itertools import chain
from pprint import pprint
from copy import copy, deepcopy
from itertools import repeat
from functools import reduce

enableLog = True

def logPrint(str):
	if enableLog:
		print(str, end='')

# serialNumber = 9221
serialNumber = 29

x = 33
y = 45

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

gridWidth = 30
gridHeight = 30

def getPowerLevel(x, y, serialNumber):
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
for y in range(1, gridHeight - 1):
	row = []
	for x in range(1, gridWidth - 1):
		row.append(getPowerLevel(x, y, serialNumber))
	cols.append(row)

print('done, data =%s', cols)

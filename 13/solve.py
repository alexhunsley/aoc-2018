# solve.py 13
#
# do carts always appear on straight sections in the input? I assume so.
# so on input can always replace v, ^ with | and <, > with -

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

lines = [x.strip() for x in f.readlines()]

carts = []

lineIndex = 0
for l in lines:
	print(l)
	# find all occurence of this char
	rightCartXPositions = [pos for pos, char in enumerate(l) if char == '>']
	for cartXPos in rightCartXPositions:
		carts.append([(cartXPos, lineIndex), (1, 0)])

	print("line %s, r carts = %s" % (l, carts))

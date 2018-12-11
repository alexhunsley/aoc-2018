# solve.py
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
		print(str, end='')

f = open("input.txt")

for line in f.readlines():
	x = line[10:16].strip()
	y = line[17:24].strip()
	
	print("!%s,%s!" % (x, y))



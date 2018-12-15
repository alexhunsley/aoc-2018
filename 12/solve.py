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

lines = []
with open("simpleInput.txt") as f:
	lines = f.readlines()

pattern = lines[0][15:]
print(pattern)

rules = {}
for l in lines[2:]:
	ruleLeft = l[:5]
	ruleRight = l[9]
	rules[ruleLeft] = ruleRight

print(rules)

for gen in range(0, 1):
	newPattern = ""
	for segmentRange in range(0, len(pattern) - 5):
		segment = pattern[segmentRange:segmentRange+5]
		if not segment in rules:
			newPattern += '.'
		else:
			print('seg: %s match: %s' % (segment, rules[segment]))
			newPattern += rules[segment]
	print('result pattern: %s' % newPattern)


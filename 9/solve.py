# AOC2018 day 9
#

# Input:
# 463 players; last marble is worth 71787 points

#
# puzzle notes:
# "last marble is worth 1618 points" - they just mean it is marble 1618.
# That marble is actually not worth anything, since it's not div by 23!

from collections import defaultdict
import sys
from functools import reduce

marbles = [0]
currentMarble = 0

numElves = 463
# numElves = 10

nextMarbleIndex = 1
nextElfToPlay = 0

elfScores = defaultdict(int)

def indexOfMarbleWithClockwiseOffset(position, offset):
	return (position + offset) % len(marbles)

def outputMarbles():
	str = ''
	for i in range(0, len(marbles)):
		if i == currentMarble:
			str += "( %s ) " % marbles[i]
		else:
			str += "  %s   " % marbles[i]

	print("[%d] %s" % (nextElfToPlay + 1, str))

outputMarbles()

# print(indexOfMarbleWithClockwiseOffset(0, 1))
# print(indexOfMarbleWithClockwiseOffset(0, 2))
# print(indexOfMarbleWithClockwiseOffset(0, 3))

# print('---------')
# print(indexOfMarbleWithClockwiseOffset(0, -1))
# print(indexOfMarbleWithClockwiseOffset(0, -2))
# print(indexOfMarbleWithClockwiseOffset(0, -3))
# print('---------')

for i in range(0, 71787 + 1):
	# print('i=', i)
	if nextMarbleIndex > 0 and (nextMarbleIndex % 23) == 0:
		print('-------------------------------------------------------------')
		print('--------------- RULE B!')
		pointsScored = nextMarbleIndex

		marbleIndexForRemoval = indexOfMarbleWithClockwiseOffset(currentMarble, -7)
		print('  marbleIndexForRemoval = ', marbleIndexForRemoval)

		# what if it's the last one though?
		pointsScored += marbles.pop(marbleIndexForRemoval)
		elfScores[nextElfToPlay] += pointsScored

		if len(marbles) == marbleIndexForRemoval:
			# special wrap-around case
			currentMarble = 0
		else:
			currentMarble = marbleIndexForRemoval


		print('23 FREAK! elf %d now has score %d (+%d)' % (nextElfToPlay, elfScores[nextElfToPlay], pointsScored))


		if elfScores[nextElfToPlay] == 8317:
			print('hit the high score! marbleIdx = %d, scores = %s' % (nextMarbleIndex, elfScores))
		# print(' an elf now has score', elfScores[nextElfToPlay])
	else:
		placeMarbleIndex = indexOfMarbleWithClockwiseOffset(currentMarble, 1)
		# print('marble %d, elf %d, want to place at index %d' % (nextMarbleIndex, nextElfToPlay, placeMarbleIndex))
		if (placeMarbleIndex == len(marbles) - 1):
			#append
			marbles.append(nextMarbleIndex)
			currentMarble = len(marbles) - 1
			# print('(did append)')
		else:
			marbles.insert(placeMarbleIndex + 1, nextMarbleIndex)
			currentMarble = placeMarbleIndex + 1
			# print('(did insert)')

	# print('MARBLES NOW:')
	# outputMarbles()

	nextMarbleIndex += 1
	nextElfToPlay = (nextElfToPlay + 1) % numElves

winningScore = reduce(max, [elfScores[item] for item in elfScores])
print(' Part 1: winning score is %d' % winningScore)


# the seasons tchaikovsky - dec

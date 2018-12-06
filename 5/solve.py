# solve.py 5
#

from __future__ import print_function

def lettersCollapse(letter1, letter2):
	return letter1.istitle() != letter2.istitle() and (letter1.lower() == letter2.lower())

# just for double checking there is no more collapsible stuff
def compactPolymerExitOnFirstCollapsePoint(poly):
	i = 0
	while i < len(poly) - 1:
		print('looping i=%d' % i)
		if lettersCollapse(poly[i], poly[i + 1]):
			print('found a collapse at i = %d' % i)
			return False
		i += 1
	print('found no collapse!')
	return True

def compactPolymer(poly):
	i = 0
	while i < len(poly) - 1:
		if lettersCollapse(poly[i], poly[i + 1]):
			newPoly = poly[0:i] + poly[i+2:]
			poly = newPoly
			if i > 0:
				i -= 1
		else:
			i += 1

		if len(poly) < 2:
			break
		if i == len(poly) - 1:
			break
	return poly


def testCompaction(input, output):
	assert compactPolymer(input) == output, "Given %s I expected %s, didn't get it" % (input, output)

def runTests():
	assert lettersCollapse('a', 'b') == False
	assert lettersCollapse('a', 'B') == False
	assert lettersCollapse('a', 'B') == False
	assert lettersCollapse('a', 'Z') == False
	assert lettersCollapse('a', 'a') == False
	assert lettersCollapse('a', 'A') == True
	assert lettersCollapse('B', 'b') == True

	testCompaction('', '')
	testCompaction('abc', 'abc')
	testCompaction('ABC', 'ABC')
	testCompaction('aA', '')
	testCompaction('abBA', '')
	testCompaction('abBcCcA', 'acA')
	testCompaction('abcdDCBA', '')



def solvePart1():
	f = open("input.txt")

	line = f.readline()

	resultPart1 = compactPolymer(line)

	# double check nothing more can be collapsed
	assert compactPolymerExitOnFirstCollapsePoint(resultPart1), "Found a collapsible part of result - not expected"
	
	print('PART 1: answer: chain length = %d' % len(resultPart1))


# runTests()
solvePart1()


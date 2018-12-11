# solve.py 8
#


from collections import Counter, defaultdict
from itertools import chain
from pprint import pprint
from copy import copy, deepcopy
from itertools import repeat
from functools import reduce

f = open("input.txt")
# f = open("exampleInput.txt")

input = f.read()

# ah! my node numbering is flawed!


# 0 children, 1 metadata = 10
# input = "0 1 10"

# 1 child, 2 metadatas = 10, 11
# input = "1 1 0 2 20 30 10"


# input = "2 1 0 2 20 31 0 4 1 2 3 3 1"
#        A---------------------------
#            B-------- C----------

input = "2 1 1 2 0 1 99 20 31 0 4 1 2 3 1 98"
#        A----------------------------------
#            B--------------- D-------------
#                C-----

# Ah! can ref child nodes in metadata multiple times! this work? yes.

# we want: ( ( ( (), 20, 30), ( (), 1, 2, 3, 4) ), 10 )

code = input.split(' ')

code = list(map(int, code))


opStack = []

metaDataTotal = 0

# set up initial node on the stack
numChildren = code[0]
numMetadata = code[1]

idx = 2

# node id, curr child being processed, num children, num metadata
opStack.append([0, 0, numChildren, numMetadata])
print('stack initially = ', opStack)

# map from child node ID to (parentNodeId, metadatas)
nodeRelations = {}

spaces = " " * 200

debugTree = ""

cnt = 0
while True:
	print('start loop, stack =', opStack)
	# cnt += 1
	# if cnt == 5:
	# 	break

	print('--------- start main loop, i = %d' % idx)
	if not opStack:
		print(' stack now empty! finished')
		break

	numItemsOnStack = len(opStack)
	spacer = spaces[0:numItemsOnStack * 2]

	(nodeId, currChild, numChildren, numMetadata) = opStack.pop()

	# debug tree
	if currChild == 0:
		debugTree += "%s >%s\n" % (spacer, nodeId)

	currChild += 1

	# put modified data back on stack (currChild has incremented)
	opStack.append((nodeId, currChild, numChildren, numMetadata))

	print(' stack not empty - doing children %d of %d' % (currChild, numChildren))

	# if no children left, node children finished processing - process metadata and continue
	if currChild == numChildren + 1:
		print('  .. reached end of (or no) children')
		metaData = code[idx : idx + numMetadata]
		print(' I saw metadata: ', metaData)

		debugTree += "%s <%s  %s\n" % (spacer, nodeId, metaData)

		metaDataTotal += reduce(lambda x, y: x+y, metaData)

		idx += numMetadata
		print(' nodeID: %s processed metadata %s, meta total: %d, stack idx now = %d ' % (nodeId, metaData, metaDataTotal, idx))
		opStack.pop()

		# if >0 items on stack, we have a parent node, identify it
		parentNodeId = -1
		if len(opStack) > 0:
			parentNodeId = opStack[-1][0]

		# relationValueData = [parentNodeId]

		nodeRelations[nodeId] = [parentNodeId] + metaData

		print('      PARENT NODE: ', parentNodeId)

		continue

	print(' processing CHILD ', currChild)

	numChildren = code[idx]
	numMetadata = code[idx + 1]
	idx += 2

	# opStack.append([nodeId + currChild, 0, numChildren, numMetadata])
	opStack.append([nodeId + currChild, 0, numChildren, numMetadata])

	# if numChildren == 0:
	# 	print('no children, reading the metadata')
	# 	# read metadata
	# 	metaData = code[i + 2 : i + 2 + numMetadata]
	# 	metaDataTotal += reduce(lambda x, y: x+y, metaData)

	# 	# todo add the metadata to total
	# else:
	# 	print('got %d children, processing them' % numChildren)


	# we store currChild, numChildren, metadata on the stack
	# opStack.append([0, numChildren, numMetadata])

	# break

print(opStack)
print(' final metadata total = ', metaDataTotal)

print()




def valueForNode(nodeId):
	print('=== ENTER value for node ', nodeId)
	# nodes pointing to this as parent should
	# be in correct order if sorted by nodeId

	# TODO - we don't need the full dict I think, just the id
	childNodes = {k: v for k, v in nodeRelations.items() if nodeId == v[0]}
	print('found child nodes ', childNodes)

	metadata = nodeRelations[nodeId][1:]

	if len(childNodes) == 0:
		return reduce(lambda x, y: x+y, metadata)

	# sum up the values of children referred to by metadata (where present)
	childNodeIdsSorted = list(childNodes.keys())
	childNodeIdsSorted.sort()

	total = 0
	childNodeIdsThatExist = [nodeId for nodeId in metadata if nodeId <= len(childNodes)]
	for nodeId in childNodeIdsThatExist:
		print('   ... calling sub childforNode... on id =', nodeId)
		total += valueForNode(nodeId)

	print('calc total = ', total)
	print('childNodeIdsThatExist=', childNodeIdsThatExist)
	print('child nodes of %s are %s' % (nodeId, childNodes))
	print('child nodes sorted: ', childNodeIdsSorted)

	return total

print('FINAL VALUE = ', valueForNode(0))
print('relations: ', nodeRelations)

print()

with open("tree.txt", "w") as treefile:
    treefile.write(debugTree)


# part2 - 93 is wrong

# for line in f.readlines():
# 	x = line[10:16].strip()
# 	y = line[17:24].strip()
	
# 	print("!%s,%s!" % (x, y))


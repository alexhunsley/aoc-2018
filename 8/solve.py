# solve.py 8
#

# 
# Exercise in masochism: I deliberately avoided recursion in the parsing.
# Stack based parsing is a PITA, ugh :(


from functools import reduce

f = open("input.txt")
# f = open("exampleInput.txt")

input = f.read()

# enable one of input defs below to see some simple examples

# 0 children, 1 metadata = 10
# input = "0 1 10"

# 1 child, 2 metadatas = 10, 11
# input = "1 1 0 2 20 30 10"


# input = "2 1 0 2 20 31 0 4 1 2 3 3 1"
#        A---------------------------
#            B-------- C----------

# input = "2 1 1 2 0 1 99 20 31 0 4 1 2 3 1 98"
#        A----------------------------------
#            B--------------- D-------------
#                C-----

code = input.split(' ')
code = list(map(int, code))

opStack = []

metaDataTotal = 0

# set up initial node on the stack
numChildren = code[0]
numMetadata = code[1]

# index into the input numbers
idx = 2

# node id, curr child being processed, num children, num metadata
opStack.append([0, 0, numChildren, numMetadata])

# map from child node ID to (parentNodeId, metadatas)
nodeRelations = {}

spaces = " " * 200

debugTree = ""

cnt = 0

nodeIdCounter = 0

while True:
	if not opStack:
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

	# if no children left, node children finished processing - process metadata and continue
	if currChild == numChildren + 1:
		metaData = code[idx : idx + numMetadata]

		debugTree += "%s <%s  %s\n" % (spacer, nodeId, metaData)

		metaDataTotal += reduce(lambda x, y: x+y, metaData)

		idx += numMetadata
		opStack.pop()

		# if >0 items on stack, we have a parent node, identify it
		parentNodeId = -1
		if len(opStack) > 0:
			parentNodeId = opStack[-1][0]

		nodeRelations[nodeId] = [parentNodeId] + metaData
		continue

	numChildren = code[idx]
	numMetadata = code[idx + 1]
	idx += 2

	nodeIdCounter += 1

	opStack.append([nodeIdCounter, 0, numChildren, numMetadata])


def valueForNode(nodeId):
	# nodes pointing to this as parent should
	# be in correct order if sorted by nodeId

	# TODO - we don't need the full dict I think, just the id
	childNodes = {k: v for k, v in nodeRelations.items() if nodeId == v[0]}

	metadata = nodeRelations[nodeId][1:]

	if len(childNodes) == 0:
		return reduce(lambda x, y: x+y, metadata)

	# sum up the values of children referred to by metadata (where present)
	childNodeIdsSorted = list(childNodes.keys())
	childNodeIdsSorted.sort()

	total = 0
	childNodeIdsThatExist = [nodeId for nodeId in metadata if nodeId <= len(childNodes)]
	for nodeId in childNodeIdsThatExist:
		nthChildKey = list(childNodes.keys())[nodeId - 1]
		total += valueForNode(nthChildKey)

	return total

with open("tree.txt", "w") as treefile:
    treefile.write(debugTree)

print(' Part 1: metadata total = ', metaDataTotal)
print(' Part 2: node(0) value: %s' % valueForNode(0))



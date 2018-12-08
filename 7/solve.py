# AOC2018 part 7
#
# Sleigh assembly:
# plan:
#   store a dict that maps a step to the step(s) that it depends on.
#   'solve' the items that have no dependencies. Then remove their
#   mentions as dependies for anything else (honouring the alphabetical order).

from collections import Counter, defaultdict
from itertools import chain
import pprint
from copy import copy, deepcopy

f = open("input.txt")

deps = defaultdict(set)

# deps[2] = set()
# print(deps[2])
# deps[2].add('3')
# print(deps[2])
# print(deps.items())

taskOrder = ""

for line in f.readlines():
	dependency = line[5]
	dependee = line[36]

	deps[dependee].add(dependency)

print(' have read deps=', deps)
# ensure all tasks with no dependencies are in the default dict

mostRecentTaskWithLastDependencyRemoved = ''

while deps:

	allDependencies = set()
	allDependees = set()

	for k, v in deps.items():
		print('working on k,v = ', k, v)
		allDependees = allDependees.union(k)
		allDependencies = allDependencies.union(v)

	# print(allDependencies)
	# print(allDependees)
	# sys.exit(1)

	executableTasksSet = allDependencies - allDependees
	executableTasks = list(executableTasksSet)
	executableTasks.sort()

	assert executableTasks, "No tasks!"
	# taskOrder += 
	print(' we can do: ', executableTasks)

	# note: only do the first task! not all! then
	# we need to recalc what next.
	taskOrder += executableTasks[0]

	print(' now have tasks order =', taskOrder)

	deps2 = deepcopy(deps)

	# remove task from all deps now it's done
	for k, v in deps.items():
		if executableTasks[0] in v:
			print('found %s in deps for %s (all deps = %s)' % (executableTasks[0], k, v))
			deps2[k].remove(executableTasks[0])
			print('   (after removal, we have: %s)' % deps2[k])
			if not deps2[k]:
				print(' deleting empty set! OMG!!!')
				mostRecentTaskWithLastDependencyRemoved = k
				del deps2[k]

	deps = deps2
# solve!

	# doableTasks = [k for k in deps if len(deps[k]) == 0]
	# print('doable tasks: ', doableTasks)
	
	print('============================================ startig again!')

print(deps)

taskOrder += mostRecentTaskWithLastDependencyRemoved
print(taskOrder)

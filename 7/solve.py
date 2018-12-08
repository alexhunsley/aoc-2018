# AOC2018 part 7
#
# Sleigh assembly:
# plan:
#   Store a dict that maps a step to the step(s) that it depends on.
#   'solve' the items that have no dependencies. Then remove their
#   mentions as dependencies for anything else (honouring the alphabetical order).

from collections import Counter, defaultdict
from itertools import chain
import pprint
from copy import copy, deepcopy

def solvePart1():
	f = open("input.txt")

	deps = defaultdict(set)

	taskOrder = ""

	for line in f.readlines():
		dependency = line[5]
		dependee = line[36]

		deps[dependee].add(dependency)

	mostRecentTaskWithLastDependencyRemoved = ''

	while deps:
		allDependencies = set()
		allDependees = set()

		for k, v in deps.items():
			allDependees = allDependees.union(k)
			allDependencies = allDependencies.union(v)

		executableTasksSet = allDependencies - allDependees
		executableTasks = list(executableTasksSet)
		executableTasks.sort()

		assert executableTasks, "No tasks! We expect to have some!"

		# note: only do the first task! not all! then
		# we need to recalc what to do next.
		taskOrder += executableTasks[0]

		depsCopy = deepcopy(deps)

		# remove task from all deps now it's done
		for k, v in deps.items():
			if executableTasks[0] in v:
				depsCopy[k].remove(executableTasks[0])
				if not depsCopy[k]:
					del depsCopy[k]
					mostRecentTaskWithLastDependencyRemoved = k

		deps = depsCopy

	taskOrder += mostRecentTaskWithLastDependencyRemoved
	return taskOrder

def solvePart2(taskOrder):
	print("part 2 todo")

taskOrder = solvePart1()
print('Part 1: ', taskOrder)

solvePart2(taskOrder)

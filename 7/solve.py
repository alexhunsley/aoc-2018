# AOC2018 part 7
#
# Sleigh assembly:
# Part 1 plan:
#   Store a dict that maps a step to the step(s) that it depends on.
#   while (tasksRemaining):
#      'solve' first item (alphabetically) that is executable (i.e. has no dependencies)
#      Then remove its mentions as a dependency for anything else 
#   (Hint: Items that have no dependencies appear in the dict value collections
#   but are not anywhere as a dict key.)
#
# Part 2 plan:
#   we maintain 'worker' details and the current time (seconds).
#   while (tasksRemaining):
#      schedule as many as possible of all task now executable (in alphabetical order).
#      For the scheduled task(s) T that will next finish:
#        mark each task as done
#
#
#
from collections import Counter, defaultdict
from itertools import chain
import pprint
from copy import copy, deepcopy

# we have five workers (you + four elves).
numWorkers = 5

WORKER_DATA_INDEX_TASK_ID = 0
WORKER_DATA_INDEX_TIME_STARTED = 1
WORKER_DATA_INDEX_TASK_DURATION = 2

# for each worker we store current task (or '.' for idle),
# time task started (since second 0), and task duration
workerData = [['.', -1, -1]] * numWorkers

# seonds since workers started making the sleigh
secondsElapsed = 0

tasksExecutable = set()

def solvePart1():	

	# f = open("input.txt")
	f = open("sampleInput.txt")

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

taskOrder = solvePart1()
print('Part 1: ', taskOrder)


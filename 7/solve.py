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
#   while (tasks still to start or tasks currently executing):
#      schedule as many as possible of all task now executable (in alphabetical order).
#      For the scheduled task(s) T that will next finish:
#        mark each task as done
#

from collections import Counter, defaultdict
from itertools import chain
import pprint
from copy import copy, deepcopy
from itertools import repeat
from functools import reduce

numWorkers = 5
taskTimeExcessSeconds = 60

WORKER_DATA_INDEX_TASK_ID = 0
WORKER_DATA_INDEX_TASK_FINISH_TIME = 1

# for each worker we store current task id (or '.' for idle) and task completion time 
workerData = [['.', -1] for i in range(0, numWorkers)]

tasksExecutable = set()

def calcTaskDuration(taskId):
	return ord(taskId) - ord('A') + 1 + taskTimeExcessSeconds

def solvePart1():	
	global tasksExecutable
	
	# seonds since workers started making the sleigh
	currentTimeSeconds = 0

	f = open("input.txt")

	deps = defaultdict(set)

	taskOrder = ""

	allDependencies = set()
	allDependees = set()
	
	for line in f.readlines():
		dependency = line[5]
		allDependencies.add(dependency)

		dependee = line[36]
		allDependees.add(dependee)

		deps[dependee].add(dependency)

	# explicitly add all tasks with no dependency to the deps dict - 
	# otherwise, they don't appear as a key
	tasksWithNoDependency = allDependencies - allDependees

	for d in tasksWithNoDependency:
		deps[d] = set()

	mostRecentTaskWithLastDependencyRemoved = ''

	while True:
		# our finishing condition
		idleWorkers = [worker for worker in workerData if worker[WORKER_DATA_INDEX_TASK_ID] == '.']
		if len(idleWorkers) == numWorkers and not deps:
			break

		newlyExecutableTasksSet = set(filter(lambda k: len(deps[k]) == 0, deps))

		tasksExecutable = tasksExecutable.union(newlyExecutableTasksSet)
		tasksExecutableList = list(tasksExecutable)

		if tasksExecutableList:
			tasksExecutableList.sort()

			# schedule as many tasks as we can - limited by tasks available for scheduling,
			# and by amount of workers currently idle
			for worker in idleWorkers:
				taskId = tasksExecutableList.pop(0)
				worker[WORKER_DATA_INDEX_TASK_ID] = taskId 
				taskDuration = calcTaskDuration(taskId)
				worker[WORKER_DATA_INDEX_TASK_FINISH_TIME] = currentTimeSeconds + taskDuration

				tasksExecutable.remove(taskId)
				del deps[taskId]

				if not tasksExecutableList:
					break

		# when is the nearest second time that one or more tasks complete?
		activeWorkers = [worker for worker in workerData if worker[WORKER_DATA_INDEX_TASK_ID] != '.']
		nearestTimeATasksWillComplete = reduce(min, [worker[WORKER_DATA_INDEX_TASK_FINISH_TIME] for worker in activeWorkers])

		workersCompleting = [worker for worker in workerData if worker[WORKER_DATA_INDEX_TASK_FINISH_TIME] == nearestTimeATasksWillComplete]
		# mark them all as complete

		workersCompleting.sort(key=lambda worker: worker[WORKER_DATA_INDEX_TASK_ID], reverse=False)

		for workerDone in workersCompleting:
			# taskOrder += tasksExecutableList[0]
			taskId = workerDone[WORKER_DATA_INDEX_TASK_ID]
			taskOrder += taskId
				
			depsCopy = deepcopy(deps)

			# remove task from all deps now it's done
			for k, v in deps.items():
				if taskId in v:
					depsCopy[k].remove(taskId)

			deps = depsCopy
			
			# make worker idle again
			workerDone[WORKER_DATA_INDEX_TASK_ID] = '.'
			# not stricly necessary, but good principle
			workerDone[WORKER_DATA_INDEX_TASK_FINISH_TIME] = -1

		currentTimeSeconds = nearestTimeATasksWillComplete
		
	print(' Part 2: finish time = %d' % currentTimeSeconds)
	return taskOrder

taskOrder = solvePart1()
print(' Part 1: ', taskOrder)


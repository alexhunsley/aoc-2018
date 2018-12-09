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
from itertools import repeat
from functools import reduce

# we have five workers (you + four elves).
# numWorkers = 5
numWorkers = 2

WORKER_DATA_INDEX_TASK_ID = 0
WORKER_DATA_INDEX_TASK_FINISH_TIME = 1

# 0 for the example, 60 for actual input data
taskTimeExcessSeconds = 0

# for each worker we store current task (or '.' for idle),
# time task started (since second 0), and task duration
# workerData = list(repeat(['.', -1, -1], numWorkers)) 
workerData = [['.', -1] for i in range(0, numWorkers)]

# print(workerData)
# workerData[0][0] = 999
# print(workerData)
# sys.exit(1)


tasksExecutable = set()

def calcTaskDuration(taskId):
	return ord(taskId) - ord('A') + 1 + taskTimeExcessSeconds

def solvePart1():	
	global tasksExecutable
	
	# seonds since workers started making the sleigh
	currentTimeSeconds = 0

	# f = open("input.txt")
	# f = open("sampleInput.txt")
	f = open("mySimpleInput.txt")

	deps = defaultdict(set)

	taskOrder = ""

	for line in f.readlines():
		dependency = line[5]
		dependee = line[36]

		deps[dependee].add(dependency)

	mostRecentTaskWithLastDependencyRemoved = ''

	loops = 0

	while deps:
		print('--------------------------------------------------------')
		print('start loop, workers =', workerData)
		allDependencies = set()
		allDependees = set()

		for k, v in deps.items():
			allDependees = allDependees.union(k)
			allDependencies = allDependencies.union(v)

		newlyExecutableTasksSet = allDependencies - allDependees

		print('currently executable tasks: %s' % tasksExecutable)
		print('newly executable tasks: %s' % newlyExecutableTasksSet)
		tasksExecutable = tasksExecutable.union(newlyExecutableTasksSet)
		print('hence, all tasks now executable = %s' % tasksExecutable)

		tasksExecutableList = list(tasksExecutable)
		tasksExecutableList.sort()

		assert tasksExecutableList, "No task(s) startable! We expect to have at least one!"

		# schedule as many tasks as we can - limited by tasks available for scheduling,
		# and by amount of workers currently idle
		idleWorkers = [worker for worker in workerData if worker[WORKER_DATA_INDEX_TASK_ID] == '.']

		print('idle workers = ', idleWorkers)
		for worker in idleWorkers:
			taskId = tasksExecutableList.pop(0)
			worker[WORKER_DATA_INDEX_TASK_ID] = taskId 
			taskDuration = calcTaskDuration(taskId)
			worker[WORKER_DATA_INDEX_TASK_FINISH_TIME] = currentTimeSeconds + taskDuration

			# you popped the task from the sorted list, but not the original set!
			# do that.
			tasksExecutable.remove(taskId)

			print('made a new worker: ', worker)
			if not tasksExecutableList:
				print(' (no tasks left in exec list, so exiting scheduler)')
				break

		print('after scheduling all tasks I could, all workers = ', workerData)

		# when is the nearest second time that one or more tasks complete?
		activeWorkers = [worker for worker in workerData if worker[WORKER_DATA_INDEX_TASK_ID] != '.']
		print('activeWorkers = ', activeWorkers)
		nearestTimeATasksWillComplete = reduce(min, [worker[WORKER_DATA_INDEX_TASK_FINISH_TIME] for worker in activeWorkers])
		print('nearestTimeATasksWillComplete: ', nearestTimeATasksWillComplete)

		workersCompleting = [worker for worker in workerData if worker[WORKER_DATA_INDEX_TASK_FINISH_TIME] == nearestTimeATasksWillComplete]
		# mark them all as complete

		workersCompleting.sort(key=lambda worker: worker[WORKER_DATA_INDEX_TASK_ID], reverse=False)
		print('  so workers completing then: ', workersCompleting)

		for workerDone in workersCompleting:
			# taskOrder += tasksExecutableList[0]
			taskId = workerDone[WORKER_DATA_INDEX_TASK_ID]
			taskOrder += taskId
				
			depsCopy = deepcopy(deps)

			# remove task from all deps now it's done
			for k, v in deps.items():
				if taskId in v:
					depsCopy[k].remove(taskId)
					if not depsCopy[k]:
						del depsCopy[k]
						mostRecentTaskWithLastDependencyRemoved = k

			deps = depsCopy
			
			# make worker idle again
			workerDone[WORKER_DATA_INDEX_TASK_ID] = '.'
			# not stricly necessary, but good principle
			workerDone[WORKER_DATA_INDEX_TASK_FINISH_TIME] = -1

		currentTimeSeconds = nearestTimeATasksWillComplete
		print('==== after processing all due workers, we have time = %d, workers = %s' % (currentTimeSeconds, workerData))
		
		# TEMP
		# loops += 1
		# if (loops == 5):
		# 	break

	# take into accoutn the last thing to complete
	taskOrder += mostRecentTaskWithLastDependencyRemoved
	currentTimeSeconds += calcTaskDuration(mostRecentTaskWithLastDependencyRemoved)

	print(' final reckoning: time = %d' % currentTimeSeconds)
	return taskOrder


taskOrder = solvePart1()
print('Part 1: ', taskOrder)


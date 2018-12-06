# advent of code, day 4
#


import sys
import operator

f = open("input.txt")

lines = f.readlines()

lines.sort()

asleepTime = -1
guardId = ""

guardAsleepTotalMins = {}
guardMinCounts = {}

# nasty fly-by-night recording of data for part 2
sleepiestMinuteSleepCount = 0
sleepiestMinute = -1
sleepiestMinuteHasGuardId = -1

def registerAsleepTime(guardId, minsDuration):
	if not guardId in guardAsleepTotalMins:
		guardAsleepTotalMins[guardId] = minsDuration
	else:
		guardAsleepTotalMins[guardId] = guardAsleepTotalMins[guardId] + minsDuration

def incrementMinutesWhileAsleep(guardId, asleepTime, wakeUpTime):
	global sleepiestMinuteSleepCount
	global sleepiestMinuteHasGuardId
	global sleepiestMinute

	if not guardId in guardMinCounts:
		guardMinCounts[guardId] = {}

	for minute in range(asleepTime, wakeUpTime):
		if not minute in guardMinCounts[guardId]:
			guardMinCounts[guardId][minute] = 1
		else:
			guardMinCounts[guardId][minute] += 1

		if (guardMinCounts[guardId][minute] > sleepiestMinuteSleepCount):
			sleepiestMinuteSleepCount = guardMinCounts[guardId][minute]
			sleepiestMinute = minute
			sleepiestMinuteHasGuardId = guardId

def registerStartStopSleep(guardId, asleepTime, wakeUpTime):
	durationAsleep = wakeUpTime - asleepTime
	registerAsleepTime(guardId, durationAsleep)
	incrementMinutesWhileAsleep(guardId, asleepTime, wakeUpTime)


for line in lines:
	if "Guard" in line:
		guardId = line.split(' ')[3]
		#print guardId
	elif "falls asleep" in line:
		asleepTime = int(line.split(' ')[1][3:5])
	elif "wakes up" in line:
		wakeUpTime = int(line.split(' ')[1][3:5])
		registerStartStopSleep(guardId, asleepTime, wakeUpTime)
	else:
		print("Aborting, unexpected line: %s", line)
		sys.exit(1)

guardAsleepTotalMinsSorted = sorted(guardAsleepTotalMins.items(), key=operator.itemgetter(1), reverse=True)
guardAsleepLongest = guardAsleepTotalMinsSorted[0]

(sleepiestGuardId, sleepiestGuardMinsSlept) = guardAsleepLongest

############### part 1

####################################################################
# find most popular minute this guard was sleeping

guardMinCountsSorted = sorted(guardMinCounts[sleepiestGuardId].items(), key=operator.itemgetter(1), reverse=True)
sleepiestMinuteForSleepiestGuard = guardMinCountsSorted[0][0]

submitAnswer1 = int(sleepiestGuardId[1:]) * int(sleepiestMinuteForSleepiestGuard)

print(' PART 1: ANSWER TO SUBMIT: ', submitAnswer1)

############### part 2

submitAnswer2 = int(sleepiestMinuteHasGuardId[1:]) * int(sleepiestMinute)

print(' PART 2: ANSWER TO SUBMIT: ', submitAnswer2)


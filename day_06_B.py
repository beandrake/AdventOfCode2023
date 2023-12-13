# https://adventofcode.com/2023/day/6#part2

# --- Day 6: Wait For It ---
# 
# The ferry quickly brings you across Island Island. After asking around, you discover that there is indeed normally a large pile of sand somewhere near here, but you don't see anything besides lots of water and the small island where the ferry has docked.
# 
# As you try to figure out what to do next, you notice a poster on a wall near the ferry dock. "Boat races! Open to the public! Grand prize is an all-expenses-paid trip to Desert Island!" That must be where the sand comes from! Best of all, the boat races are starting in just a few minutes.
# 
# You manage to sign up as a competitor in the boat races just in time. The organizer explains that it's not really a traditional race - instead, you will get a fixed amount of time during which your boat has to travel as far as it can, and you win if your boat goes the farthest.
# 
# As part of signing up, you get a sheet of paper (your puzzle input) that lists the time allowed for each race and also the best distance ever recorded in that race. To guarantee you win the grand prize, you need to make sure you go farther in each race than the current record holder.
# 
# The organizer brings you over to the area where the boat races are held. The boats are much smaller than you expected - they're actually toy boats, each with a big button on top. Holding down the button charges the boat, and releasing the button allows the boat to move. Boats move faster if their button was held longer, but time spent holding the button counts against the total race time. You can only hold the button at the start of the race, and boats don't move until the button is released.
# 
# For example:
# 
# Time:      7  15   30
# Distance:  9  40  200
# 
# This document describes three races:
# 
#     The first race lasts 7 milliseconds. The record distance in this race is 9 millimeters.
#     The second race lasts 15 milliseconds. The record distance in this race is 40 millimeters.
#     The third race lasts 30 milliseconds. The record distance in this race is 200 millimeters.
# 
# Your toy boat has a starting speed of zero millimeters per millisecond. For each whole millisecond you spend at the beginning of the race holding down the button, the boat's speed increases by one millimeter per millisecond.
# 
# So, because the first race lasts 7 milliseconds, you only have a few options:
# 
#     Don't hold the button at all (that is, hold it for 0 milliseconds) at the start of the race. The boat won't move; it will have traveled 0 millimeters by the end of the race.
#     Hold the button for 1 millisecond at the start of the race. Then, the boat will travel at a speed of 1 millimeter per millisecond for 6 milliseconds, reaching a total distance traveled of 6 millimeters.
#     Hold the button for 2 milliseconds, giving the boat a speed of 2 millimeters per millisecond. It will then get 5 milliseconds to move, reaching a total distance of 10 millimeters.
#     Hold the button for 3 milliseconds. After its remaining 4 milliseconds of travel time, the boat will have gone 12 millimeters.
#     Hold the button for 4 milliseconds. After its remaining 3 milliseconds of travel time, the boat will have gone 12 millimeters.
#     Hold the button for 5 milliseconds, causing the boat to travel a total of 10 millimeters.
#     Hold the button for 6 milliseconds, causing the boat to travel a total of 6 millimeters.
#     Hold the button for 7 milliseconds. That's the entire duration of the race. You never let go of the button. The boat can't move until you let go of the button. Please make sure you let go of the button so the boat gets to move. 0 millimeters.
# 
# Since the current record for this race is 9 millimeters, there are actually 4 different ways you could win: you could hold the button for 2, 3, 4, or 5 milliseconds at the start of the race.
# 
# In the second race, you could hold the button for at least 4 milliseconds and at most 11 milliseconds and beat the record, a total of 8 different ways to win.
# 
# In the third race, you could hold the button for at least 11 milliseconds and no more than 19 milliseconds and still beat the record, a total of 9 ways you could win.
# 
# To see how much margin of error you have, determine the number of ways you can beat the record in each race; in this example, if you multiply these values together, you get 288 (4 * 8 * 9).
# 
# Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers together?

# --- Part Two ---
# 
# As the race is about to start, you realize the piece of paper with race times and record distances you got earlier actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.
# 
# So, the example from before:
# 
# Time:      7  15   30
# Distance:  9  40  200
# 
# ...now instead means this:
# 
# Time:      71530
# Distance:  940200
# 
# Now, you have to figure out how many ways there are to win this single race. In this example, the race lasts for 71530 milliseconds and the record distance you need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the record, a total of 71503 ways!
# 
# How many ways can you beat the record in this one much longer race?
import math

INPUT_FILE = r'day_06_input.txt'
#INPUT_FILE = r'day_06_miniTest.txt'


with open(INPUT_FILE, 'r') as dataRows:
	
	timeLine = dataRows.readline()
	label, timeData = timeLine.split(':')
	timeLimits = timeData.split()
	#print(f"Time limits:       {timeLimits}")
	timeLimitAsString = ''.join(timeLimits)
	timeLimit = int(timeLimitAsString)
	print(f"Time limit:        {timeLimit} ms")

	distanceLine = dataRows.readline()
	label, distanceData = distanceLine.split(':')
	raceDistanceRecords = distanceData.split()	
	#print(f"Distance records:  {raceDistanceRecords}")
	distanceRecordAsString = ''.join(raceDistanceRecords)
	distanceRecord = int(distanceRecordAsString)
	print(f"Distance record:   {distanceRecord} mm")

	print()	
	# NOTE: Well well well, speak of the devil: performance has become an issue!
	#		In the previous code, I had suggested that this situation would call for a binary search.  
	# 		But I realized there's a better option: just solve the equations!
	
	# Okay, it's time to do some math
	# We know this from the instructions:
	# 	distanceCovered = chargeTime * moveTime
	# 	timeLimit = chargeTime + moveTime
	# Now let's see if we can use this to solve for the chargeTime and moveTime of the distanceRecord!

	# timeLimit = chargeTime + moveTime
	# timeLimit - chargeTime = moveTime

	# distanceRecord = chargeTime * moveTime
	# distanceRecord = chargeTime * (timeLimit - chargeTime)
	# distanceRecord = chargeTime*timeLimit - chargeTime*chargeTime
	# chargeTime*chargeTime + distanceRecord = chargeTime*timeLimit
	# chargeTime*chargeTime - chargeTime*timeLimit + distanceRecord = 0
	# chargeTime**2 - timeLimit*chargeTime + distanceRecord = 0
	
	# Quadratic Formula Time!
	# This takes an equation with the format of:
	#	ax**2 + bx + c = 0
	# And let's us solve for x via:
	# 	x = (-b ± math.sqrt(b**2 - 4ac))/2a 	
	# a = 1
	# b = -timeLimit
	# c = distanceRecord
	# x = chargeTime

	# We can simplify this part a bit to make our equation less messy:
	# 	b**2 - 4ac
	# 	(-timeLimit)**2 - 4*1*distanceRecord
	# 	timeLimit**2 - 4*distanceRecord
	
	# Thus we arrive at our equation:
	# 	chargeTime = (timeLimit ± math.sqrt(timeLimit**2 - 4*distanceRecord))/2	

	# We know that maxChargeTime will be the one with the + because the result of the square root will be positive
	maxChargeTime = (timeLimit + math.sqrt(timeLimit**2 - 4*distanceRecord))/2

	# Despite the ±, we only need to run the above equation once with the + version;
	#  because maxChargeTime = maxMoveTime, meaning:
	# 	minChargeTime = timeLimit - maxChargeTime	
	minChargeTime = timeLimit - maxChargeTime
	
	distance = round(minChargeTime * maxChargeTime)
		
	# now let's demonstrate to ourselves that this was correct
	print(f"The distance record would need a movement or charge time of {minChargeTime} ms")
	print(f"which would leave a remaining time of {maxChargeTime} ms for the other.")
	print(f"Resulting in a distance of {distance} mm.")
	print()
	# So, how do we beat that distance?
	#	The greater the difference between two positive numbers, the lower the value of their product will be when multiplied.
	#	Since raising our min value also lowers our max value (and vice versa) - which brings them closer together - we know
	#	that we'll beat the record as long as our charge time is between minChargeTime and maxChargeTime (exclusive).
	
	if maxChargeTime == math.floor(maxChargeTime):
		maxChargeTimeToBeatRecord = math.floor(maxChargeTime) - 1
	else:
		maxChargeTimeToBeatRecord = math.floor(maxChargeTime)

	minChargeTimeToBeatRecord = timeLimit - maxChargeTimeToBeatRecord

	print(f"To beat the record, our charge time will need to be between:")
	print(f"   {minChargeTimeToBeatRecord} and {maxChargeTimeToBeatRecord} ms (inclusive)")

	# remember, our ways to win must use integer values
	waysToWin = maxChargeTimeToBeatRecord - minChargeTimeToBeatRecord + 1

	print()
	print(f"Ways to win race:   {waysToWin}")
	input()
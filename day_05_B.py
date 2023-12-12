# https://adventofcode.com/2023/day/5#part2

# --- Part Two ---
# 
# Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.
# 
# The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:
# 
# seeds: 79 14 55 13
# 
# This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.
# 
# Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.
# 
# In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.
# 
# Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?


INPUT_FILE = r'day_05_input.txt'
#INPUT_FILE = r'day_05_miniTest.txt'

NUM_WIDTH = 12	# numbert of characters set aside to display the numerical values we're working with, so they visually align and can be compared more easily

class NumberChain:
	"""
	A NumberChain is an object that represents a range of consecutive numbers, from a starting value until an ending value (inclusive).
	When updated, a NumberChain sets a flag so that it cannot be updated again until the flag is manually reset.
	"""
	def __init__(self, firstNumber, lastNumber, canBeUpdated=True):
		self.firstNumber = firstNumber
		self.lastNumber = lastNumber
		self.canBeUpdated = canBeUpdated

	def getValues(self):
		return self.firstNumber, self.lastNumber
	
	def updateValues(self, firstNumber, lastNumber):
		if not self.canBeUpdated:
			return False
		
		self.firstNumber = firstNumber
		self.lastNumber = lastNumber
		self.canBeUpdated = False
		return True

	def allowUpdate(self):
		self.canBeUpdated = True

	def __str__(self):
		return f"{self.firstNumber}-{self.lastNumber}"
	
	def __repr__(self):
		return self.__str__()


with open(INPUT_FILE, 'r') as dataRows:
	
	# 0 seed --> 1 soil --> 2 fertilizer --> 3 water --> 4 light --> 5 temp --> 6 humidity --> 7 location
	processingStage = 0
	
	# STAGE: 0 SEED - this initializes the seeds
	firstLine = dataRows.readline()
	# Example:
	# 	seeds: 79 14 55 13

	stageName, data = firstLine.split(':')
	print(f"Stage: {stageName}")
	print()

	valueList = data.split()
	seedList = []
	# every pair of values is the START and then LENGTH of a consecutive range of seeds we have
	pairInProgress = False
	for value in valueList:
		if not pairInProgress:
			seedStart = int(value)
		else:
			chainLength = int(value)
			end = seedStart + chainLength - 1
			seedList.append( NumberChain(seedStart, end) )
		
		pairInProgress = not pairInProgress

	if pairInProgress:
		raise ValueError("Seed input requires an even number of numeric values.")

	print(f"Seeds: {seedList}")
	
	# STAGE: 1 thru 7 - these transition seeds into soil, soil into fertilizer, etc
	for line in dataRows:
		
		if ':' in line:
			# A colon means that this line is a header, which indicates a new stage is beginning.
			processingStage += 1
			
			# set state so that Seeds that were updated in the previous stage can now be updated again during this new stage
			for seed in seedList:
				seed.allowUpdate()
			print(line)
		
		else:
			# No colon means this line either contains transition data or blank space
			numberList = line.split()
			
			if len(numberList) < 1:
				# Sometimes there are blank lines; nothing to process so just move on.
				continue
			
			# We have legitimate values to get, so parse them to ints
			# Example:
			# 	52 50 48
			destinationStart, sourceStart, chainLength = [int(numericString) for numericString in numberList]
			sourceEnd = sourceStart + chainLength - 1
			destinationEnd = destinationStart + chainLength - 1
			adjustmentAmount = destinationStart - sourceStart
			
			print(f"source range:         {sourceStart:>{NUM_WIDTH}} {sourceEnd:>{NUM_WIDTH}}")
			print(f"destination range:    {destinationStart:>{NUM_WIDTH}} {destinationEnd:>{NUM_WIDTH}}")
			print(f"adjustment value:     {adjustmentAmount:>{NUM_WIDTH}}")

			if chainLength < 1:
				raise ValueError("Honestly why would you do this.")
			
			# check chains of seeds to see if and how they may need adjustments
			for seed in seedList:
				if not seed.canBeUpdated:
					continue

				currentSeedStart, currentSeedEnd = seed.getValues()

				if sourceEnd < currentSeedStart or currentSeedEnd < sourceStart:
					# no numbers in the update range
					continue

				# When the values in a NumberChain are updated, this can result in several possible outcomes:
				# - Every number in the range is updated:
				#		Simply updates the range values and revokes update permissions.
				# - There is a dividing line; numbers on one side need to be updated, but numbers on the other don't:
				# 		Essentially splits this object into two objects, one which represents the unaltered half, the other which represents the altered half with revoked update permissions.
				# - A subsection in the middle needs to be updated, but numbers to the right and left are unchanged:
				# 		Essentially splits this object into three objects, one which is changed and no longer has update permissions, and two on each side that are unaltered.

				print()
				# NOTE: when a new item is appended to the end of a list during a for each loop, those new items WILL be traversed as part of that loop.					
				if sourceStart <= currentSeedStart and currentSeedEnd <= sourceEnd:
					# all numbers need updating
					updatedStart = currentSeedStart + adjustmentAmount
					updatedEnd = currentSeedEnd + adjustmentAmount
					seed.updateValues(updatedStart, updatedEnd)
					print(f"  *   Updated seeds   {currentSeedStart:>{NUM_WIDTH}} {currentSeedEnd:>{NUM_WIDTH}}") 
					print(f"                 to   {updatedStart:>{NUM_WIDTH}} {updatedEnd:>{NUM_WIDTH}}")

				elif sourceStart <= currentSeedStart and currentSeedStart <= sourceEnd:
					# some numbers on the left need updating					
					print(f"  *  SPLIT!   seeds   {currentSeedStart:>{NUM_WIDTH}} {currentSeedEnd:>{NUM_WIDTH}}") 
					
					# Update numbers on the left
					updatedStart = currentSeedStart + adjustmentAmount
					updatedEnd = sourceEnd + adjustmentAmount
					wasUpdated = seed.updateValues(updatedStart, updatedEnd)
					print(f"    - Updated seeds   {currentSeedStart:>{NUM_WIDTH}} {sourceEnd:>{NUM_WIDTH}}") 
					print(f"                 to   {updatedStart:>{NUM_WIDTH}} {updatedEnd:>{NUM_WIDTH}}")

					# Create a new object for the unchanged numbers on the right
					splitStart = sourceEnd + 1
					splitEnd = currentSeedEnd
					seedList.append( NumberChain(splitStart, splitEnd) )
					print(f"    - Static  seeds   {splitStart:>{NUM_WIDTH}} {splitEnd:>{NUM_WIDTH}}") 
					
				elif sourceStart <= currentSeedEnd and currentSeedEnd <= sourceEnd:
					# some numbers on the right need updating
					print(f"  *  SPLIT!   seeds   {currentSeedStart:>{NUM_WIDTH}} {currentSeedEnd:>{NUM_WIDTH}}") 

					# Create a new object for the unchanged numbers on the left
					splitStart = currentSeedStart
					splitEnd = sourceStart - 1
					seedList.append( NumberChain(splitStart, splitEnd) )
					print(f"    - Static  seeds   {splitStart:>{NUM_WIDTH}} {splitEnd:>{NUM_WIDTH}}") 

					# Update numbers on the right
					updatedStart = sourceStart + adjustmentAmount
					updatedEnd = currentSeedEnd + adjustmentAmount
					wasUpdated = seed.updateValues(updatedStart, updatedEnd)
					print(f"    - Updated seeds   {sourceStart:>{NUM_WIDTH}} {currentSeedEnd:>{NUM_WIDTH}}") 
					print(f"                 to   {updatedStart:>{NUM_WIDTH}} {updatedEnd:>{NUM_WIDTH}}")

				elif currentSeedStart < sourceStart and sourceEnd < currentSeedEnd :
					# some seeds in the middle need updating
					print(f"  *  SPLIT!   seeds   {currentSeedStart:>{NUM_WIDTH}} {currentSeedEnd:>{NUM_WIDTH}}") 
					
					# Create a new object for the unchanged numbers on the left
					splitStart = currentSeedStart
					splitEnd = sourceStart - 1
					seedList.append( NumberChain(splitStart, splitEnd) )
					print(f"    - Static  seeds   {splitStart:>{NUM_WIDTH}} {splitEnd:>{NUM_WIDTH}}") 

					# Update numbers in the middle
					updatedStart = sourceStart + adjustmentAmount
					updatedEnd = sourceEnd + adjustmentAmount
					wasUpdated = seed.updateValues(updatedStart, updatedEnd)
					print(f"    - Updated seeds   {sourceStart:>{NUM_WIDTH}} {sourceEnd:>{NUM_WIDTH}}") 
					print(f"                 to   {updatedStart:>{NUM_WIDTH}} {updatedEnd:>{NUM_WIDTH}}")

					# Create a new object for the unchanged numbers on the right
					splitStart = sourceEnd + 1
					splitEnd = currentSeedEnd
					seedList.append( NumberChain(splitStart, splitEnd) )
					print(f"    - Static  seeds   {splitStart:>{NUM_WIDTH}} {splitEnd:>{NUM_WIDTH}}") 
					
			print()		

	print(f"Final values:")
	print(seedList)
	
	lowestValue, trash = seedList[0].getValues()
	for seed in seedList:
		targetValue, trash = seed.getValues()
		if targetValue < lowestValue:
			lowestValue = targetValue

	print(f"The lowest value is {lowestValue}")
	input()
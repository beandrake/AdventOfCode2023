# https://adventofcode.com/2023/day/3#part2

# --- Part Two ---
# 
# The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.
# 
# You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.
# 
# Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.
# 
# The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.
# 
# This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.
# 
# Consider the same engine schematic again:
# 
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# 
# In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
# 
# What is the sum of all of the gear ratios in your engine schematic?


INPUT_FILE = r'day_03_input.txt'

def getNumberAt(index, line):
	"""
	Given the index of a digit and the line of text the digit is from, return the value of the integer containing that digit.
	"""
	if not line[index].isnumeric():
		raise ValueError(f"The character at index {index} is not a digit as expected in the following line:\n{line}")

	# Let's find the left-most digit's index
	indexOfLeftMostDigit = index
	while True:
		if indexOfLeftMostDigit-1 < 0   or   not line[indexOfLeftMostDigit-1].isnumeric():
			break
		indexOfLeftMostDigit -= 1

	# Let's find the right-most digit's index
	indexOfRightMostDigit = index
	while True:
		if indexOfRightMostDigit+1 == len(line)   or   not line[indexOfRightMostDigit+1].isnumeric():
			break
		indexOfRightMostDigit += 1

	number = line[indexOfLeftMostDigit:indexOfRightMostDigit+1]
	return int(number)
	

def findGears(aboveLine, currentLine, belowLine):
	"""
	Given 3 lines of text, returns a list of gears found on the currentLine.  In the provided lines, a gear is an asterisk that is adjacent (includes diagonals) to exactly two numbers.
	In the returned list, each gear is represented by a list containing the numbers it is adjacent to.
	"""
	print(aboveLine)
	print(currentLine)
	print(belowLine)

	gears = []
	index = 0
	while index < len(currentLine):

		if currentLine[index] == '*':
			# first, let's check how many numbers are adjacent			
			center = index
			left = center-1 if center-1 >= 0 else 0
			right = center+1 if center+1 < len(currentLine) else center
			
			numbersFound = []			
			# check to the left and right on current line
			if currentLine[left].isnumeric():
				numbersFound.append( getNumberAt(left, currentLine) )

			if currentLine[right].isnumeric():
				numbersFound.append( getNumberAt(right, currentLine) )

			# check line above, then check line below
			for otherLine in [aboveLine, belowLine]:
				if center < len(otherLine) and otherLine[center].isnumeric():
					# this means there is exactly one number there, because if the spaces on the left or right of it were numeric they would be part of this same number
					numbersFound.append( getNumberAt(center, otherLine) )
				else:
					# since the center space isn't a number, the amount of numbers will be the number of digits found on the left and right of it
					if left < len(otherLine) and otherLine[left].isnumeric():
						numbersFound.append( getNumberAt(left, otherLine) )
					if left != right and right < len(otherLine) and otherLine[right].isnumeric():
						numbersFound.append( getNumberAt(right, otherLine) )

			print(numbersFound)
			# remember, it's not a gear unless it is adjacent to EXACTLY two numbers
			if len(numbersFound) == 2:
				print("The above is a gear!")
				gears.append(numbersFound)

		index += 1
	
	print(f"Gears found on middle line: {len(gears)}")
	return gears
			

def extractGearRatio(newGears):
	"""
	Given a list of gears (each represented as a list of two integers) returns the sum of the ratios the gears, where a ratio is the product its two integers.
	"""
	totalRatio = 0
	for gear in newGears:
		ratio = gear[0] * gear[1]
		print(f"Ratio: {ratio}")
		totalRatio += ratio
	return totalRatio


with open(INPUT_FILE) as dataRows:
	gearSum = 0

	# start out with some fake empty lines 
	midLine = '.'
	bottomLine = '.'
	for line in dataRows:

		# cycle lines upwards
		topLine = midLine
		midLine = bottomLine
		bottomLine = line.strip()

		# check the middle line for parts (ie - numbers near symbols)
		newGears = findGears(topLine, midLine, bottomLine)
		gearSum += extractGearRatio(newGears)
		print(f"Running total: {gearSum}\n")

	# bottomLine is a valid line and hasn't been checked yet, so let's check it now
	newGears = findGears(midLine, bottomLine, '.')
	gearSum += extractGearRatio(newGears)
	print(f"Running total: {gearSum}\n")

	print(f"Final total:   {gearSum}")
	input()
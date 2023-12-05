# https://adventofcode.com/2023/day/3

# --- Day 3: Gear Ratios ---
# 
# You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.
# 
# It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.
# 
# "Aaah!"
# 
# You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.
# 
# The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.
# 
# The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)
# 
# Here is an example engine schematic:
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
# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
# 
# Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?


INPUT_FILE = r'day_03_input.txt'


def isEngineSymbol(character):
	"""
	Returns true if the character is a symbol other than a period.
	"""
	# if the character isn't alphanumeric and isn't white space, let's consider it a symbol.
	return character != '.' and not character.isalnum() and not character.isspace()



def findParts(aboveLine, currentLine, belowLine):
	"""
	Given 3 lines of text, returns a list of all numeric values from the currentLine that are adjacent or diagonal to at least one non-period symbol.
	"""
	print(aboveLine)
	print(currentLine)
	print(belowLine)

	parts = []
	index = 0
	while index < len(currentLine):
		length = 1

		if currentLine[index].isnumeric():
			# found a number, let's determine how long it is
			while index+length < len(currentLine) and currentLine[index+length].isnumeric():
				length += 1

			# now that we know how long the number is, let's scan the spaces adjacent and diagonal to its digits for non-period symbols
			symbolFound = False			
			sensorMin = index-1 if index-1 >= 0 else 0
			sensorMax = index+length if index+length < len(currentLine) else index+length-1

			# check to the left and right on current line
			if isEngineSymbol(currentLine[sensorMin]) or isEngineSymbol(currentLine[sensorMax]):
				symbolFound = True

			# check above and below lines
			sensorIndex = sensorMin
			while not symbolFound and sensorIndex <= sensorMax:
				if (   sensorIndex < len(aboveLine) and isEngineSymbol(aboveLine[sensorIndex])
					or sensorIndex < len(belowLine) and isEngineSymbol(belowLine[sensorIndex]) ):
					symbolFound = True
				sensorIndex += 1

			# if we found a symbol in the search zone, add this number to the part list
			if symbolFound:
				partNumber = currentLine[index:index+length]
				parts.append( int(partNumber) )

		# incrementing by length will take us to the next space that we haven't already checked
		index += length
	
	print(f"Parts found on middle line: {parts}")
	return parts
			

with open(INPUT_FILE) as dataRows:
	partSum = 0

	# start out with some fake empty lines 
	midLine = '.'
	bottomLine = '.'
	for line in dataRows:

		# cycle lines upwards
		topLine = midLine
		midLine = bottomLine
		bottomLine = line.strip()

		# check the middle line for parts (ie - numbers near symbols)
		newParts = findParts(topLine, midLine, bottomLine)
		partSum += sum(newParts)
		print(f"Running total: {partSum}\n")

	# bottomLine is a valid line and hasn't been checked yet, so let's check it now
	newParts = findParts(midLine, bottomLine, '.')
	partSum += sum(newParts)
	print(f"Running total: {partSum}\n")

	print(f"Final total:   {partSum}")
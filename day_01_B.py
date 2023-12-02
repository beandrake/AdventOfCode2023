# https://adventofcode.com/2023/day/1#part2

# --- Part Two ---
# 
# Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".
# 
# Equipped with this new information, you now need to find the real first and last digit on each line. For example:
# 
# two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen
# 
# In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
# 
# What is the sum of all of the calibration values?


INPUT_FILE = r'day_01_input.txt'


numberDictNormal = {	'one'   :1,
						'two'   :2,
						'three' :3,
						'four'  :4,
						'five'  :5,
						'six'   :6,
						'seven' :7,
						'eight' :8,
						'nine'  :9  }

numberDictReversed = {	'one'[::-1]   :1,
						'two'[::-1]   :2,
						'three'[::-1] :3,
						'four'[::-1]  :4,
						'five'[::-1]  :5,
						'six'[::-1]   :6,
						'seven'[::-1] :7,
						'eight'[::-1] :8,
						'nine'[::-1]  :9  }

def getDigitFromText(text, numberDict):	
	"""
	Given a line of text, find the numerical value of the left-most word representing a number, which must be found in numberDict.
	If no number is found, raises a ValueError.

	:param line:       The line of text to search for a number in.
	:param numberDict: A user-provided dictionary whose keys are textual representations of digits, with values that are the corresponding integer.	
	"""
	numberList = numberDict.keys()

	for number in numberList:
		numLength = len(number)
		if len(text) < numLength:
			continue
		
		if text[0:numLength] == number:
			return numberDict.get(number)
	
	raise ValueError(f'The text "{text}" did not represent one of the registered numbers.')
	

def findFirstDigit(line, numberDict):
	"""
	Given a line of text, find the numerical value of the left-most number it contains, whether in the form of a numeral or a word representing a number that is found in numberDict.
	If no number is found, raises a ValueError.

	:param line:       The line of text to search for a number in.
	:param numberDict: A user-provided dictionary whose keys are textual representations of digits, with values that are the corresponding integer.	
	"""
	digitFound = False
	for index in range( len(line) ):
		
		# first see if this character is an actual numeral
		character = line[index]
		try:
			digit = int(character)
			digitFound = True
			break
		except ValueError:
			pass

		# not a numeral, so let's see if it spells a word that represents a number
		restOfLine = line[index:]
		try:
			digit = getDigitFromText(restOfLine, numberDict)
			digitFound = True
			break
		except ValueError:
			pass

	# Design decision: in the unexpected circumstances that a line contains no digits, what to do?  That would probably be an error, so let's raise it.
	if not digitFound:
		raise ValueError(f'The calibration text "{line}" was expected to contain at least one numeral.')

	return digit


if __name__ == '__main__':
	with open(INPUT_FILE) as calibrationData:
		sum = 0
		for rawLine in calibrationData:
			line = rawLine.strip()
			print(line)
			
			leftDigit = findFirstDigit(line, numberDictNormal)
			rightDigit = findFirstDigit(line[::-1], numberDictReversed)

			lineValue = leftDigit*10 + rightDigit
			sum += lineValue
			print(f"{lineValue} --> running total: {sum}", end='\n\n')

		print(f"Sum of all calibration values: {sum}")
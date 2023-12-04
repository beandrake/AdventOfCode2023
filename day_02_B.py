# https://adventofcode.com/2023/day/2#part2

# --- Part Two ---
# 
# The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure why the water stopped; however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!
# 
# As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?
# 
# Again consider the example games from earlier:
# 
# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
# 
#     In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
#     Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
#     Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
#     Game 4 required at least 14 red, 3 green, and 15 blue cubes.
#     Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
# 
# The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.
# 
# For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?


INPUT_FILE = r'day_02_input.txt'


def minCubes(gameData):
	"""
	Given an unparsed string containing the data for one game, determines and returns the minimum amount of red, green, and blue cubes needed to play that game, respectively.
	"""
	# gameData format example:
	#	1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
	maxRed = 0
	maxGreen = 0
	maxBlue = 0
	
	roundList = gameData.split('; ')
	for roundData in roundList:
		# roundData format example:
		#	1 green, 3 red, 6 blue
		gemList = roundData.split(', ')

		for gemData in gemList:
			# gemData format example:
			#	15 blue
			amount, color = gemData.split()
			amount = int(amount)
			#print(f"amount & color:   {amount} {color}")

			match color:
				case 'red':
					if amount > maxRed:
						maxRed = amount
				case 'green':
					if amount > maxGreen:
						maxGreen = amount
				case 'blue':
					if amount > maxBlue:
						maxBlue = amount
				case _:
					raise ValueError(f"Gem color {color} unrecognized or improperly formatted.")

	print(f"Red needed:    {maxRed}")
	print(f"Green needed:  {maxGreen}")
	print(f"Blue needed:   {maxBlue}")
	return maxRed, maxGreen, maxBlue


with open(INPUT_FILE) as dataRows:
	sum = 0
	for line in dataRows:
		print(line, end='')

		# Line format example:
		#	 Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
		header, gameData = line.split(sep=': ')		
		gameID = header.split()[1]
		print(f"GameID:   {gameID}")

		red, green, blue = minCubes(gameData)
		power = red * green * blue
		print(f"POWER:         {power}")

		sum += power
		print(f"Running total: {sum}\n")

	print(f"Final total:   {sum}")
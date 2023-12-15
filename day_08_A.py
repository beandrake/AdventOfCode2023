# https://adventofcode.com/2023/day/7#part2

# --- Day 8: Haunted Wasteland ---
# 
# You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.
# 
# One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.
# 
# It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!
# 
# After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.
# 
# This format defines each node of the network individually. For example:
# 
# RL
# 
# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)
# 
# Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.
# 
# Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:
# 
# LLR
# 
# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)
# 
# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?


INPUT_FILE = r'day_08_input.txt'
#INPUT_FILE = r'day_08_miniTest.txt'

STARTING_NODE = 'AAA'
DESTINATION_NODE = 'ZZZ'
NODE_LENGTH = 3

# we'll be using these as indicies 2-item lists representing forks in the road
LEFT = 0
RIGHT = 1

class Directions:
	"""
	Given a string of characters that terminates in a newline, this object will track your index in that string and loop to the beginning once it reaches the end.
	"""
	def __init__(self, directionString):
		
		# parse L's and R's into their corresponding numerical values, since those are the indices we'll be using later
		self.directionList = []
		for character in directionString:
			if character == 'L':
				self.directionList.append(LEFT)
			elif character == 'R':
				self.directionList.append(RIGHT)

		self.currentIndex = len(self.directionList)

	def getNext(self):
		"""
		Updates state to the next direction and returns it.
		"""
		self.currentIndex += 1

		if self.currentIndex >= len(self.directionList):
			self.currentIndex = 0

		return self.directionList[self.currentIndex]

	def __str__(self):
		stringVersion = ""
		for number in self.directionList:
			stringVersion += str(number)
		return stringVersion
	
	def __repr__(self):
		return self.__str__()


with open(INPUT_FILE, 'r') as dataRows:

	# read first line, which contains a series of L's and R's that represent our directional path
	print()
	print("Reading direction data...")
	print()
	directionString = dataRows.readline()
	print(f"Raw data: \n{directionString}")
	directions = Directions(directionString)
	print(f"Converted to numerical data: \n{directions}")

	# read blank line and throw it in the trash
	dataRows.readline()

	# read the rest of the file, which contains the data that will build our map of nodes
	print()
	print("Reading map data...")
	print()
	myMap = {}
	for line in dataRows:
		# Example line:
		#	BBB = (AAA, ZZZ)
		print(line)
		
		node = line[0:0+NODE_LENGTH]
		left = line[7:7+NODE_LENGTH]
		right = line[12:12+NODE_LENGTH]		
		print(f"Node:    {node}")
		print(f"Left:    {left}")
		print(f"Right:   {right}")
		print()
	
		fork = [left, right]
		nodeData = {node: fork}
		myMap.update(nodeData)
		

	# Follow our directions to traverse the map
	print("Let's start our journey!")
	print()
	currentNode = STARTING_NODE
	steps = 0
	while currentNode != DESTINATION_NODE:
		print(f"You are currently at {currentNode}.")
		
		steps += 1
		
		# which fork in the path should we take?
		currentFork = myMap.get(currentNode)
		print(f"You see a fork leading to {currentFork[LEFT]} and {currentFork[RIGHT]}.")
		print(currentFork)
		directionToTake = directions.getNext()
		print(directionToTake)
		print()

		currentNode = currentFork[directionToTake]	

	print(f"You have arrived at {DESTINATION_NODE}!")
	print(f"Steps taken to arrive at destination: { steps }")
	input()
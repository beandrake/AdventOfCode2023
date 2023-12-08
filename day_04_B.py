# https://adventofcode.com/2023/day/4#part2

# --- Part Two ---
# 
# Just as you're about to report your findings to the Elf, one of you realizes that the rules have actually been printed on the back of every card this whole time.
# 
# There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.
# 
# Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.
# 
# Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to win any more cards. (Cards will never make you copy a card past the end of the table.)
# 
# This time, the above example goes differently:
# 
# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
# 
#     Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.
#     Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
#     Your copy of card 2 also wins one copy each of cards 3 and 4.
#     Your four instances of card 3 (one original and three copies) have two matching numbers, so you win four copies each of cards 4 and 5.
#     Your eight instances of card 4 (one original and seven copies) have one matching number, so you win eight copies of card 5.
#     Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
#     Your one instance of card 6 (one original) has no matching numbers and wins no more cards.
# 
# Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6. In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!
# 
# Process all of the original and copied scratchcards until no more scratchcards are won. Including the original set of scratchcards, how many total scratchcards do you end up with?


INPUT_FILE = r'day_04_input.txt'


class AmountList:
	"""
	A class that represents a list where no index will ever be considered out of range.
	If you use this interface to interact with the underlying list and the index does not yet exist in the list, it will be created.
	"""
	
	def __init__(self, defaultAmount=0):
		"""
		:param defaultAmount:	the default value that will be assigned to indices that do not yet exist when created.
		"""
		self.listOfAmounts = []
		self.defaultAmount = defaultAmount

	def _ensureListReachesIndex(self, index):
		while index >= len(self.listOfAmounts):
			self.listOfAmounts.append(self.defaultAmount)
	
	def getAmount(self, index):
		self._ensureListReachesIndex(index)
		return self.listOfAmounts[index]
	
	def setAmount(self, index, amount):
		self._ensureListReachesIndex(index)
		self.listOfAmounts[index] = amount
	
	def addAmount(self, index, amount):
		self._ensureListReachesIndex(index)
		self.listOfAmounts[index] += amount

	def getLength(self):
		return len(self.listOfAmounts)
	
	def getTotalSum(self):
		return sum(self.listOfAmounts)


with open(INPUT_FILE, 'r') as dataRows:

	cardAmountList = AmountList(defaultAmount=1)
	currentCardIndex = 0
	for line in dataRows:
		# Example line:
		#	Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1

		# first get rid of everything before the colon
		header, numberData = line.split(sep=':')
		# split what's left into winning numbers on left, owned numbers on right
		winningData, ownedNumberData = numberData.split(sep='|')
		winningNumbers = winningData.split()
		ownedNumbers = ownedNumberData.split()

		# string comparison is slower than integer comparison so let's convert these strings to ints
		winningNumbers = [int(num) for num in winningNumbers]
		ownedNumbers = [int(num) for num in ownedNumbers]
		
		# sort both lists of numbers so that we can match with an n alrogithm instead of n-squared (granted, the sorts themselves will be somewhere between n log n and n, as they use Timsort)
		winningNumbers.sort()
		ownedNumbers.sort()
		currentCardCopies = cardAmountList.getAmount(currentCardIndex)
		print(f"Card Index:  {currentCardIndex}")
		print(f"Card Copies: {currentCardCopies}")
		print(f"Winning:     {winningNumbers}")
		print(f"Owned:       {ownedNumbers}")
		
		matches = 0
		windex = 0
		oindex = 0
		while oindex < len(ownedNumbers) and windex < len(winningNumbers):
			if ownedNumbers[oindex] == winningNumbers[windex]:
				# match found!  only increment owned in case it's possible to own multiple of the same number
				matches += 1
				oindex += 1
			elif ownedNumbers[oindex] < winningNumbers[windex]:
				oindex += 1
			else:
				windex += 1
		print(f"Matches:     {matches}")

		# Now that we know how many matches there are, we can generate the rewards.  Quoted from the official instructions:
		# 	"you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15."

		# And in the above scenario, if we have n copies of card 10, then that means we would win n copies of cards 11, 12, 13, 14, and 15.
		nextCardIndex = currentCardIndex + 1
		lastCardReceivingCopies = currentCardIndex + matches
		for indexToPutCopies in range(nextCardIndex, lastCardReceivingCopies+1):
			cardAmountList.addAmount(indexToPutCopies, currentCardCopies)

		if matches > 0:
			print(f"Added {currentCardCopies} copies of cards each card between {nextCardIndex} and {lastCardReceivingCopies}, inclusive.")

		print()
		currentCardIndex += 1

	print(f"{cardAmountList.listOfAmounts}\n")	
	print(f"Length of list: {cardAmountList.getLength()}")
	print(f"Total cards possessed:   {cardAmountList.getTotalSum()}")
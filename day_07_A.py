# https://adventofcode.com/2023/day/7

# --- Day 7: Camel Cards ---
# 
# Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.
# 
# "Did you bring the parts?"
# 
# You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.
# 
# "Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.
# 
# "The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.
# 
# After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.
# 
# You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.
# 
# Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.
# 
# In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.
# 
# Every hand is exactly one type. From strongest to weakest, they are:
# 
#     Five of a kind, where all five cards have the same label: AAAAA
#     Four of a kind, where four cards have the same label and one card has a different label: AA8AA
#     Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
#     Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
#     Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
#     One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
#     High card, where all cards' labels are distinct: 23456
# 
# Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.
# 
# If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.
# 
# So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).
# 
# To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:
# 
# 32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483
# 
# This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.
# 
# So, the first step is to put the hands in order of strength:
# 
#     32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
#     KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
#     T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
# 
# Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.
# 
# Find the rank of every hand in your set. What are the total winnings?
import functools

INPUT_FILE = r'day_07_input.txt'
#INPUT_FILE = r'day_07_miniTest.txt'

HAND_SCORE = 0
BET_AMOUNT = 1
		
CARD_VALUES = {
	'A':14,
	'K':13,
	'Q':12,
	'J':11,
	'T':10,
	'9':9,
	'8':8,
	'7':7,
	'6':6,
	'5':5,
	'4':4,
	'3':3,
	'2':2,
	'1':1	
}

with open(INPUT_FILE, 'r') as dataRows:

	handList = []
	for line in dataRows:

		hand, betAmount = line.split()
		
		# Since all we need to do is rank hands relative to other hands, our goal is to sort these hands.
		# To make sorting cheaper, we're going to generate a single value with which we can rank hands: handScore.
		# Hand score is an 11-digit number in the format of AbbCCddEEff:
		#	A - represents the value of the hand type
		#	bb - represents the value of card 1
		#	CC - represents the value of card 2
		#	dd - represents the value of card 3
		#	EE - represents the value of card 4
		#	ff - represents the value of card 5

		# Determine hand type		
		# 	To determine which Type of hand we have, we don't care about what the actual cards are;
		# 	we only care about how many-of-a-kind we have of different cards.
		# 	For example, it doesn't matter what values the cards in the hand 2A2A2, it matters that we have 3 of a card and 2 of another card.
		cardTypesFound = []
		
		# sort hand so identical cards are grouped together
		orderedHand = sorted(hand)
				
		cardIndex = 0
		while cardIndex < len(orderedHand):
			character = orderedHand[cardIndex]
			chainLength = 1
			# peek to the right to see if there are more of this card
			while (
				cardIndex + chainLength < len(orderedHand)
			    and orderedHand[cardIndex + chainLength] == character
				  ):
				# found another card like this one, increment and keep checking
				chainLength += 1
			# record the number of the same card that we found
			cardTypesFound.append(chainLength)

			# progress to the next kind of card
			cardIndex += chainLength

		# sort chains so the longest chains are first
		cardTypesFound.sort(reverse=True)
		print(f"Chains:  {cardTypesFound}")

		# At last, we are actually prepared to determine the hand type
		if cardTypesFound[0] == 5:
			# Five-of-a-Kind
			typeValue = 7
		elif cardTypesFound[0] == 4:
			# Four-of-a-Kind
			typeValue = 6
		elif cardTypesFound[0] == 3:
			if cardTypesFound[1] == 2:
				# Full House
				typeValue = 5
			else:		
				# Three-of-a-Kind
				typeValue = 4
		elif cardTypesFound[0] == 2:
			if cardTypesFound[1] == 2:
				# Two Pair
				typeValue = 3
			else:		
				# One Pair
				typeValue = 2
		else:
			# High Card
			typeValue = 1

		# place typeValue in the highest digit of our 11-digit score
		handScore = typeValue * 10**10

		# Determine value of cards
		# 	We'll make a 10-digit number, and each set of 2 digits in it will be the value of the card in that spot.
		# 	For example, the cards in Q12TA have values of 12, 01, 02, 10, and 14 respectively, so the hand value is 1201021014.
		#	Remember: order matters!		
		multiplier = 100**4
		for card in hand:
			value = CARD_VALUES.get(card)
			handScore += value * multiplier
			multiplier //= 100
		print(f"Hand:  {hand:>11}")
		print(f"Score: {handScore:>11}")
		print()
		
		# Record handScore and betAmount in list
		handData = [handScore, int(betAmount)]
		handList.append(handData)

	# Sort hands in order from weakest to strongest
	#	sorting lists prioritizes lower indices, meaning the sort will be based on handScore
	handList.sort()
	print(handList)
	print()

	# Tally the winnings, incrementing the multiplier for each next bet
	multiplier = 0
	totalWinnings = 0
	for hand in handList:
		multiplier += 1
		winnings = hand[BET_AMOUNT] * multiplier
		totalWinnings += winnings
		
	print(f"Total winnings: { totalWinnings }")
	input()
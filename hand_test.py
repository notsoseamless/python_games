# Testing template for the get_value method for Hands


import random

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (card_size[0] * (0.5 + RANKS.index(self.rank)), card_size[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, card_size, [pos[0] + card_size[0] / 2, pos[1] + card_size[1] / 2], card_size)


#####################################################
# Student should insert code for Hand class here
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        result = []
        result.append('Hand contains ')
        if self.hand:
            for card in self.hand:
                result.append(card.get_suit() + card.get_rank() + ' ')
        return string_list_join(result)

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        ''' count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust '''
        values_lst = []
        total_value = 0
        # create a list of the values from the ranks
        for card in self.hand:
            values_lst.append(VALUES.get(card.get_rank()))
        # sort the rank list as we evaluate any Aces last
        sorted_values_lst = sorted(values_lst, reverse=True)
        # traverse the sorted values, process Aces (at the end) 
        for value in sorted_values_lst:
            if (value == 1) and ((total_value + 10) < 22):
                # Can make Ace ten without busting...
                total_value += 10
            else:
                # hand is too high so make Ace value one
                total_value += value
        return total_value


#RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
#VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


   
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards

       
# define global helpers
def string_list_join(string_list):
   ''' Helper borrowed from Practice Exercises for week 5a '''
   ans = ""
   for i in range(len(string_list)):
       ans += string_list[i]
   return ans     



    
###################################################
# Test code

c1 = Card("S", "A")
c2 = Card("C", "2")
c3 = Card("D", "T")
c4 = Card("S", "K")
c5 = Card("C", "7")
c6 = Card("D", "A")

test_hand = Hand()
print test_hand
print test_hand.get_value()

test_hand.add_card(c2)
print test_hand
print test_hand.get_value()

test_hand.add_card(c5)
print test_hand
print test_hand.get_value()

test_hand.add_card(c3)
print test_hand
print test_hand.get_value()

test_hand.add_card(c4)
print test_hand
print test_hand.get_value()



test_hand = Hand()
print test_hand
print test_hand.get_value()

test_hand.add_card(c1)
print test_hand
print test_hand.get_value()

test_hand.add_card(c6)
print test_hand
print test_hand.get_value()

test_hand.add_card(c4)
print test_hand
print test_hand.get_value()

test_hand.add_card(c5)
print test_hand
print test_hand.get_value()

test_hand.add_card(c3)
print test_hand
print test_hand.get_value()



###################################################
# Output to console
# note that the string representation of a hand may vary
# based on your implementation of the __str__ method

#Hand contains 
#0
#Hand contains C2 
#2
#Hand contains C2 C7 
#9
#Hand contains C2 C7 DT 
#19
#Hand contains C2 C7 DT SK 
#29
#Hand contains 
#0
#Hand contains SA 
#11
#Hand contains SA DA 
#12
#Hand contains SA DA SK 
#12
#Hand contains SA DA SK C7 
#19
#Hand contains SA DA SK C7 DT 
#29


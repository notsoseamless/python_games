



class Mem():
    ''' globals container '''
    # define globals for cards
    number_of_cards = 16 # must be even
    SUITS = ('C', 'S', 'H', 'D')
    RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
    

    






class Deck():
    ''' represents a deck of cards '''
    def __init__(self):
        pass
        # create the deck of cards by joining two decks of equal size
        card_value_list = [Mem.RANKS[rank] for rank in range(0, Mem.number_of_cards // 2)] 

        self.deck = []
        for card_value in card_value_list:
            self.deck.append(Card('C', card_value, [0,0]  ))
        print self.deck

        #cards_1 = [Card rank  for rank in range(0, Mem.number_of_cards // 2) ]
        #cards_1 = range(1, (NUM_OF_CARDS // 2) + 1)
        #cards_2 = range(1, (NUM_OF_CARDS // 2) + 1)
        #DECK = cards_1 + cards_2
        # shuffle the deck
        #random.shuffle(DECK)
        # list to set them all face down
        #EXPOSED = [False] * NUM_OF_CARDS
        # figure out where they all go
        #calc_card_positions()






class Card():

    ''' The Card class, represents a playing card '''
    def __init__(self, suit, rank, position):
        ''' init method '''
        if (suit in Mem.SUITS) and (rank in Mem.RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
        self.exposed = False   # False = face down
        self.position = position

    def __str__(self):
        ''' string method '''
        return self.suit + self.rank

    def get_suit(self):
        ''' returns the suit of a card '''
        return self.suit

    def get_rank(self):
        ''' returns the value of a card '''
        return self.rank

    def set_exposed(self, exposed):
        self.exposed = exposed;

    def draw(self):
        ''' card draw method '''
        if self.exposed:
            # draw face up
            pass
        else:
            # draw face down
            pass



if __name__ == '__main__':
    deck = Deck()






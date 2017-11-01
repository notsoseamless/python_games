# Mini-project #6 - Blackjack

import simplegui
import random

DEBUG = True # Set this to print stuff to the console

FRAME_SIZE = (600, 600)


# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
IN_PLAY = False # game state variable
OUTCOME = ""
CHOICE = ""
SCORE = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


class Card:
    ''' The Card class, represents a playing card '''
    def __init__(self, suit, rank):
        ''' init method '''
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        ''' string method '''
        return self.suit + self.rank

    def get_suit(self):
        ''' returns the suit of a card '''
        return self.suit

    def get_rank(self):
        ''' returns the value of a card '''
        return self.rank

    def draw(self, canvas, pos):
        ''' card draw method '''
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), \
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, \
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], \
                          CARD_SIZE)

    def draw_card_back(self, canvas, pos):
        ''' any self respecting card should know about having two sides
            so this method draws card face down, only the dealer hand 
            calls this method '''
        card_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0] * (SUITS.index(self.suit) % 2), \
                    CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, \
                          [pos[0] + CARD_BACK_CENTER[0], \
                           pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)         



class Hand:
    ''' The Hand class, represents a hand of cards '''
    def __init__(self):
        ''' init method '''
        self.hand = []
        self.next_card_offset = 100

    def __str__(self):
        ''' string method '''
        result = [card.get_suit() + card.get_rank() + ' '  for card in self.hand]
        return 'Hand contains ' + string_list_join(result)

    def add_card(self, card):
        ''' add a card to the hand '''
        self.hand.append(card)

    def get_value(self):
        ''' count aces as 1, if the hand has an ace, then add 11 to hand
            value if it doesn't bust '''
        total_value = 0
        # create a list of the values from the ranks in the hand
        values_lst = [VALUES.get(card.get_rank()) for card in self.hand]        
        # reverse sort the values list because we evaluate any Aces last
        sorted_values_lst = sorted(values_lst, reverse=True)
        # traverse the reverse sorted values
        for value in sorted_values_lst:
            if (value == 1) and ((total_value + 11) < 22):
                # OK we have an Ace and can make Ace as eleven without busting...
                total_value += 11
            else:
                # Non Ace or Hand value is too high to value Ace as eleven 
                # so use card default value in VALUES
                total_value += value
        return total_value    
   
    def draw(self, canvas, pos):
        ''' draw method '''
        card_pos = list(pos)
        # traverse the hand, calling the card draw method
        for card in self.hand:
            card.draw(canvas, card_pos)
            card_pos[0] += (self.calc_offset())
            
    def calc_offset(self):
        ''' private helper method prevents cards extending beyond canvas,
            switches from spaced to overlapping cards '''
        num = len(self.hand)
        if num < 5:
            return 100
        else:
            return 100 / (num * 0.25)
 


class DealerHand(Hand):
    ''' inherits from Hand and knows about a hole card '''
    def __init__(self):
        Hand.__init__(self)
           
    def draw(self, canvas, pos, in_play):
        ''' overrides Hand draw method '''
        # traverse the hand, calling the card draw method
        first_card = True
        for card in self.hand:
            if first_card and in_play:
                card.draw_card_back(canvas, pos)
                first_card = False
            else:
                card.draw(canvas, pos)
            # move position to next card
            pos[0] += (self.calc_offset())
         


class Deck:
    ''' The Deck class, represents a deck of cards '''
    def __init__(self):
        ''' init method, initialise a decck of cards '''
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        ''' shuffle the deck '''
        random.shuffle(self.deck)

    def deal_card(self):
        ''' deal out a card '''
        return self.deck.pop()

    def __str__(self):
        ''' string method '''
        result = [card.get_suit() + card.get_rank() + ' '   for card in self.deck]
        return 'Deck contains ' + string_list_join(result)



# define global helpers
def string_list_join(string_list):
    ''' Helper borrowed from week 5a Practice Exercises '''
    ans = ""
    for i in range(len(string_list)):
        ans += string_list[i]
    return ans



# event handlers for buttons
def deal():
    ''' shuffles the deck and deals the two cards to both the dealer and the player '''
    global OUTCOME, CHOICE, IN_PLAY, deck, player_hand, dealer_hand, SCORE

    # create a deck of cards
    deck = Deck()
    deck.shuffle()

    # create new player and dealer hands
    player_hand = Hand()
    dealer_hand = DealerHand()

    # add two cards to each hand
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    OUTCOME = ''
    # Implement rule that if the "Deal" button is clicked during the
    # middle of a round then the player loses the round
    if IN_PLAY:
        OUTCOME = 'You lose, illegal deal'
        SCORE -= 1

    IN_PLAY = True
    CHOICE = 'Hit or Stand?'
    print_debug_info()
 


def hit():
    ''' hit button handler
        If the value of the hand is less than or equal to 21, clicking this
        button adds an extra card to player's hand '''
    global IN_PLAY, SCORE, player_hand, OUTCOME, CHOICE
    
    OUTCOME = ''
    # if the hand is in play, hit the player
    if IN_PLAY and player_hand.get_value() < 21:
        player_hand.add_card(deck.deal_card())
        # if busted, assign a message to OUTCOME, update IN_PLAY and score
        if player_hand.get_value() > 21:
            IN_PLAY = False
            SCORE -= 1
            OUTCOME = 'You have busted'
            CHOICE = 'New deal?'
    print_debug_info()
                


def stand():
    ''' stand button handler '''
    global SCORE, OUTCOME, CHOICE, IN_PLAY, DEBUG  

    OUTCOME = ''
    
    if IN_PLAY:
        # we stay in here now until the end of the round
        player_value = player_hand.get_value()
        if player_value > 21:
            # player has busted, remind the player that they have busted.
            OUTCOME = 'You have busted'
        else:
            # if hand is in play, repeatedly hit dealer until his hand has
            # value 17 or more
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
                print_debug_info()
            dealer_value = dealer_hand.get_value()
            # assign a message to OUTCOME, update IN_PLAY and score
            if dealer_value > 21:
                OUTCOME = 'Dealer busted'
                SCORE += 1
            elif dealer_value >= player_value:
                OUTCOME = 'Dealer wins'
                SCORE -= 1
            else:
                OUTCOME = 'Player wins'
                SCORE += 1
    CHOICE = 'New deal?'
    IN_PLAY = False
    print_debug_info()



def draw(canvas):
    ''' draw handler '''
    draw_text(canvas)
    draw_cards(canvas)
    
    

def draw_text(canvas):
    ''' helper for draw handler to take care of text '''
    font_face = 'sans-serif'
    title_font_size = 50
    title_font_colour = 'Blue'
    info_font_size = 30
    info_font_colour = 'Black'
    if SCORE >= 0:
        score_text_colour = info_font_colour
    else:
        score_text_colour = 'Maroon'
    canvas.draw_text('Blackjack', (60, 100), title_font_size, title_font_colour, font_face)
    canvas.draw_text('Score ' + str(SCORE), (400, 100), info_font_size, score_text_colour, font_face)
    canvas.draw_text('Dealer', (50, 200), info_font_size, info_font_colour, font_face)
    canvas.draw_text(OUTCOME, (200, 200), info_font_size, info_font_colour, font_face)
    canvas.draw_text('Player', (50, 400), info_font_size, info_font_colour, font_face)
    canvas.draw_text(CHOICE, (200, 400), info_font_size, info_font_colour, font_face)    


    
def draw_cards(canvas):
    ''' helper for draw handler to take care of cards '''   
    dealer_pos = [50, 225]
    player_pos = [50, 425]    
    # draw dealer's cards
    dealer_hand.draw(canvas, dealer_pos, IN_PLAY)    
    # draw player's cards
    player_hand.draw(canvas, player_pos)   

    
def print_debug_info():
    ''' helper prints info to console '''
    if DEBUG:
        print
        print 'dealer hand: ' + str(dealer_hand) + ' value = ' + str(dealer_hand.get_value())
        print 'player hand: ' + str(player_hand) + ' value = ' + str(player_hand.get_value())
        print 'OUTCOME ' + OUTCOME
        print 'score ' + str(SCORE)
        print 'CHOICE ' + CHOICE
        print 'in play: ' + str(IN_PLAY)
    else:
        print 'Set DEBUG to True for console messages'
       
    
 
# initialization frame
frame = simplegui.create_frame("Blackjack", FRAME_SIZE[0], FRAME_SIZE[1])
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()





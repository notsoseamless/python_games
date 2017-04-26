''' 
    implementation of card game - Memory
    this version ports pygame
'''

# import modules
import os
import pygame
import random

# pygame specific locals/constants
from pygame.locals import *

# some resource related warnings
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')




#globals
NUM_OF_CARDS = 16        # specifies card number
CARD_SIZE = [50, 100]    # cards are logically 50x100 pixels in size
DECK = []                # stores card values
EXPOSED = [0, 0]         # boolean list of turned/unturned cards
CARD_POSITIONS = []      # list of lists of card position mappings
TURNS = 0                # the try counter
GAME_STATE = 0           # state machine persistance
CLICKED_CARD = [0, 0]    # state machine persistance



# initializations
pygame.init()



# a bit similar to CodeSkulptor frame creation -- we'll call the window the canvas
canvas = pygame.display.set_mode((630, 300))
pygame.display.set_caption("My_Project")

# Pygame Wrapper functions -- resource loading sanity checks
# Taken from the "Monkey tutorial" and updated for 3.3 by me
#
# load Image:
# A colorkey is used in graphics to represent a color of the image
# that is transparent (r, g, b). -1 = top left pixel colour is used.
def load_image(name, colorkey=None):
    fullname = os.path.join('data\images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey is not None:
        image = image.convert()
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image, image.get_rect()



# Load Sound
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data\sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', name)
        raise SystemExit(message)
    return sound
    

# need to create fonts and colour objects in PyGame
#fontObj = pygame.font.Font('ARBERKLEY.ttf', 32)
#fontObj2 = pygame.font.Font('ARBERKLEY.ttf', 24)
fontObj3 = pygame.font.Font(pygame.font.match_font('timesnewroman'), 32)


def new_game():
    ''' helper function to initialize globals '''
    global DECK, EXPOSED, GAME_STATE, TURNS
    GAME_STATE = 0
    TURNS = 0
    # create the deck of cards by joining two decks of equal size
    cards_1 = range(1, (NUM_OF_CARDS // 2) + 1)
    cards_2 = range(1, (NUM_OF_CARDS // 2) + 1)
    DECK = cards_1 + cards_2
    # shuffle the deck
    random.shuffle(DECK)
    # list to set them all face down
    EXPOSED = [False] * NUM_OF_CARDS
    # figure out where they all go
    calc_card_positions()




def calc_card_offsets():
    ''' helper calculates the offsets of the cards '''
    offsets = []
    # make sure rows x cols = NUM_OF_CARDS !!!!
    rows = 2
    cols = 8
    pos = [0, 0]       # point mappings of card polygons
    offset = [50, 50]  # amount grid of cards are from left upper corner
    shift = [60, 110]  # sets spacing between cards
    # generate a list of lists of offsets
    for row in range(rows):
        for col in range(cols):
            pos[0] = col * shift[0] + offset[0]
            pos[1] = row * shift[1] + offset[1]
            offsets.append(list(pos))
    return offsets




def calc_card_positions():
    ''' helper calculates the positions of the cards using pre-calculated offsets '''
    # get the offets
    offset = calc_card_offsets()
    # generate a list of lists of card positions unsing the offsets
    for card in range(NUM_OF_CARDS):
        CARD_POSITIONS.append(list([[offset[card][0], offset[card][1]],
                                    [offset[card][0] + CARD_SIZE[0], offset[card][1]],
                                    [offset[card][0] + CARD_SIZE[0], offset[card][1] + CARD_SIZE[1]],
                                    [offset[card][0], offset[card][1] + CARD_SIZE[1]]]))




# define event handlers
def mouseclick(pos):
    ''' game state logic, here is the state machine '''
    global GAME_STATE, TURNS
    # find where we clicked, returns > zero if clicked on a card...
    card = mouse_is_on_a_card(pos)
    # game state machine, but better to check these super states first
    if False in EXPOSED and card > 0 and not EXPOSED[card - 1]:
        # ok, not all cards are exposed and mouse was clicked on a card
        # and the clicked card was not already exposed
        # messy but need to card minus one to match list addressing...
        if GAME_STATE == 0:
            # no cards exposed, store card
            CLICKED_CARD[0] = card - 1
            # turn the card
            EXPOSED[CLICKED_CARD[0]] = True
            # update state
            GAME_STATE = 1
        elif GAME_STATE == 1:
            # one card exposed, store new card
            CLICKED_CARD[1] = card - 1
            # turn the card
            EXPOSED[CLICKED_CARD[1]] = True
            # increment the counter
            TURNS += 1
            # update state
            GAME_STATE = 2
        else: # GAME_STATE == 2
            # two cards exposed, compare values stored in DECK[]
            if DECK[CLICKED_CARD[0]] != DECK[CLICKED_CARD[1]]:
                # unlucky, turn back the last two cards
                EXPOSED[CLICKED_CARD[0]] = False
                EXPOSED[CLICKED_CARD[1]] = False
            # store first card again
            CLICKED_CARD[0] = card - 1
            # turn the card
            EXPOSED[CLICKED_CARD[0]] = True
            # update state
            GAME_STATE = 1




def mouse_is_on_a_card(pos):
    ''' helper to find if pos is within one of the cards,
        returns zero if not on a card, or a card number from 1 to 16 '''
    for card in range(NUM_OF_CARDS):
        if (pos[0] > CARD_POSITIONS[card][0][0] and
            pos[0] < CARD_POSITIONS[card][1][0] and
            pos[1] < CARD_POSITIONS[card][2][1] and
            pos[1] < CARD_POSITIONS[card][3][1]):
            # found a card so return with card num + 1
            return card + 1
    # not on a card so return zero
    return 0




def draw_handler(canvas):
    ''' the draw handler '''
    gold_color = pygame.Color(255, 215, 0)
    white_color = pygame.Color(255, 255, 255)
    black_color = pygame.Color(0, 0, 0)

    # clear canvas -- fill canvas with uniform colour, then draw everything below.
    # this removes everything previously drawn and refreshes 
    canvas.fill((0, 0, 0))

    # add the text that shows the number of turns
    label1_text = "Turns =" + str(TURNS)
    label1 = fontObj3.render(label1_text, 1, white_color)
    canvas.blit(label1, (10, 10))

    # add the cards to the screen
    for card in range(NUM_OF_CARDS):
        if EXPOSED[card]:
            # exposed card so display outline and value
            pygame.draw.polygon(canvas, white_color, CARD_POSITIONS[card])
            # add the card value
            label2_txt = str(DECK[card])
            label2 = fontObj3.render(label2_txt, 1, black_color)
            canvas.blit(label2, calc_text_posn(card))
        else:
            # card is face down, don't show value
            pygame.draw.polygon(canvas, gold_color, CARD_POSITIONS[card])

    # update the display
    pygame.display.update()




def calc_text_posn(card):
    ''' Helper derives the text position from the card position so we can place
        the value in the middle of the card when the card is exposed.
        Assumes that card is the card number integer
        Uses global CARD_POSITIONS '''
    posn = [0, 0]
    posn[0] = CARD_POSITIONS[card][0][0] + CARD_SIZE[0] // 3
    posn[1] = CARD_POSITIONS[card][0][1] + CARD_SIZE[1] // 2
    return posn



# call this function to start everything
# could be thought of as the implemntation of the CodeSkulptor frame .start() method.
def main():
    # initialize loop until quit variable
    running = True
    
    # create our FPS timer clock
    clock = pygame.time.Clock()    

    # get things rolling
    new_game()

#---------------------------Frame is now Running-----------------------------------------
    
    # doing the infinte loop until quit -- the game is running
    while running:
        
        # event queue iteration
        for event in pygame.event.get():
            
            # window GUI ('x' the window)
            if event.type == pygame.QUIT:
                running = False

            # input - key and mouse event handlers
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # just respond to right mouse clicks
                if pygame.mouse.get_pressed()[0]:
                    mouseclick(pygame.mouse.get_pos())
                    #mc_handler(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                pass
                #kd_handler(event.key)

            # timers
            #elif event.type == timer_example:
                #t_example()      
                
        # the call to the draw har
        draw_handler(canvas)
        
        # FPS limit to 60 -- essentially, setting the draw handler timing
        # it micro pauses so while loop only runs 60 times a second max.
        clock.tick(60)
        
#-----------------------------Frame Stops------------------------------------------

    # quit game -- we're now allowed to hit the quit call
    pygame.quit ()


if __name__ == "__main__":
    main()



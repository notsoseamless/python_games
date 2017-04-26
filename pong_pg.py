''' 

    pygame port of CodeSkulptor pong
    
    Notsoseamless  - September 2015

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


# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = WIDTH / 20
PAD_WIDTH = 8
PAD_HEIGHT = 100 / 2
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
LK_UP = 119
LK_DOWN = 115
RK_UP = 273
RK_DOWN = 274


# initializations
pygame.init()


# a bit similar to CodeSkulptor frame creation -- we'll call the window the canvas
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

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

gold_color = pygame.Color(255, 215, 0)
white_color = pygame.Color(255, 255, 255)


def spawn_ball(direction):
    ''' spawns the ball in the middle of the table and assigns the ball a velocity '''
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # initialize ball_pos and ball_vel for new ball in middle of table
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # randomize the velocity, assuming that the draw handler runs about 60 times each second
    # then the suggested (120,240) and (60,180) becomes (2,4) and (1,2)
    ball_vel = [random.randrange(2,4), -random.randrange(1,3)]
    
    # if direction is RIGHT, the ball's velocity is upper right, else upper left
    if not direction :
        ball_vel[0] *= -1.0


# define event handlers
def new_game() :
    ''' event handler for new game ''' 
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # initialise the variables
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    
    # randomise start direction and spawn the ball
    spawn_ball(random.choice([LEFT, RIGHT]) )




count = 0
draw_colour = white_color
def draw_handler(canvas):
    ''' canvas draw handler '''

    # clear canvas -- fill canvas with uniform colour, then draw everything below.
    # this removes everything previously drawn and refreshes 
    canvas.fill((0, 0, 0))

    text_draw = fontObj3.render("CodeSkulptor Port", True, draw_colour)
    text_draw2 = fontObj3.render("Tutorial", True, draw_colour)

    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global ball_vel
    # draw mid line and gutter    pygame.draw.lines(canvas, white_color, False, [(WIDTH / 2, 0), (WIDTH / 2, HEIGHT)], 1) # mid line
    pygame.draw.lines(canvas, white_color, False, [(WIDTH / 2, 0),(WIDTH / 2, HEIGHT)], 1) # mid line
    pygame.draw.lines(canvas, white_color, False, [(PAD_WIDTH, 0), (PAD_WIDTH, HEIGHT)], 1) # left gutter
    pygame.draw.lines(canvas, white_color, False, [(WIDTH - PAD_WIDTH, 0),(WIDTH - PAD_WIDTH, HEIGHT)], 1) # right gutter

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if (ball_pos[1] <= 0 + BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS) :
        # ball has hit either the top or bottom of the screen, implement a bounce 
        # by reversing the vertical velocity
        ball_vel[1] *= -1    

    # draw ball
    pygame.draw.circle(canvas, white_color, [int(ball_pos[0]), int(ball_pos[1])], BALL_RADIUS, 0)
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = calculate_paddel_position(paddle1_pos, paddle1_vel)
    paddle2_pos = calculate_paddel_position(paddle2_pos, paddle2_vel)       

    # draw paddles
    pygame.draw.lines(canvas, white_color, False, [(HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), (HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT)], PAD_WIDTH)
    pygame.draw.lines(canvas, white_color, False, [(WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)], PAD_WIDTH)

    # determine whether paddle and ball collide
    if ball_pos[0] <= 0 + PAD_WIDTH + BALL_RADIUS :
        if (ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT) and (ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT) :
            # hit paddle1 so bounce back and increase velosity by 10%
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else :
            # player two scores
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS :
        if (ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT) and (ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT) :
            # hit paddle2 so bounce back and increase velosity by 10%
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else :
            # player one scores
            score1 += 1
            spawn_ball(LEFT)   

    # render text
    label1 = fontObj3.render(str(score1), 1, (255,255,0))
    canvas.blit(label1, ((WIDTH / 2) - 60, 60))
    
    label2 = fontObj3.render(str(score2), 1, (255,255,0))
    canvas.blit(label2, ((WIDTH / 2) + 60, 60))

    # update the display
    pygame.display.update()
 			
 			


def calculate_paddel_position(pos, vel) :
    ''' draw helper to calculate paddle's vertical position and keep paddle on the screen '''    
    if (vel > 0) and (pos < (HEIGHT - HALF_PAD_HEIGHT)) :
        if (pos + vel) <= (HEIGHT - HALF_PAD_HEIGHT) :
            # enough space to move down
            pos += vel
        else :
            # not enough so move to end
            pos = HEIGHT - HALF_PAD_HEIGHT
    elif (vel < 0) and (pos > HALF_PAD_HEIGHT) :
        if pos + vel >= HALF_PAD_HEIGHT :
            # enough space to move up
            pos += vel
        else :
            # not enough so move to end
            pos = HALF_PAD_HEIGHT
    return pos
        



def keydown(key):
    ''' handler for keydown events '''
    global paddle1_vel, paddle2_vel
    velocity = 7    
    if key == LK_UP:
        paddle1_vel = -velocity
    elif key == LK_DOWN:
        paddle1_vel = velocity
    elif key == RK_UP:
        paddle2_vel = -velocity
    elif key == RK_DOWN:
        paddle2_vel = velocity
   


   
def keyup(key):
    ''' handler for keyup events '''
    global paddle1_vel, paddle2_vel
    if key == LK_UP:
        paddle1_vel = 0
    elif key == LK_DOWN:
        paddle1_vel = 0
    elif key == RK_UP:
        paddle2_vel = 0
    elif key == RK_DOWN:
        paddle2_vel = 0
 



# call this function to start everything
# could be thought of as the implemntation of the CodeSkulptor frame .start() method.
def main():
    # initialize loop until quit variable
    running = True
    
    new_game()

    # create our FPS timer clock
    clock = pygame.time.Clock()    
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
                # just respond to left mouse clicks
                #if pygame.mouse.get_pressed()[0]:
                    #mc_handler(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                keydown(event.key)
            elif event.type == pygame.KEYUP:
                keyup(event.key)

            # timers
            #elif event.type == timer_example:
                #t_example()      
                
        # the call to the draw handler 
        draw_handler(canvas)
        
        # FPS limit to 60 -- essentially, setting the draw handler timing
        # it micro pauses so while loop only runs 60 times a second max.
        clock.tick(60)
        
#-----------------------------Frame Stops------------------------------------------

    # quit game -- we're now allowed to hit the quit call
    pygame.quit ()


if __name__ == "__main__":
    main()



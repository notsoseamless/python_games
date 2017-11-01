''' 
    pygame port of CodeSkulptor pong
    updated for ball bouncing in 2-d space
    
    Notsoseamless  - October 2015

'''

# import modules
import os
import pygame
import math
import random


# pygame specific locals/constants
from pygame.locals import *


# some resource related warnings
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 300
HEIGHT = 200 
BALL_RADIUS = WIDTH / 40
LEFT = False
RIGHT = True
# key pad definitions
LK_UP = 119
LK_DOWN = 115
RK_UP = 273
RK_DOWN = 274
QUIT = 113
#ball object storage
BALL_GROUP = set([])


# initializations
pygame.init()


# a bit similar to CodeSkulptor frame creation -- we'll call the window the canvas
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-D Balls")

# Pygame Wrapper functions -- resource loading sanity checks
# Taken from the "onkey tutorial" and updated for 3.3 by me
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


def spawn_ball():
    ''' spawns the ball in the middle of the table and assigns the ball velocity and direction '''

    # initialize ball_pos and ball_vel for new ball in middle of table
    pos = [WIDTH / 2, HEIGHT / 2]

    # randomize the velocity, assuming that the draw handler runs about 60 times each second
    # then the suggested (120,240) and (60,180) becomes (2,4) and (1,2)
    #vel = [random.randrange(2,4), - random.randrange(1,3)]
    vel = [0, 0]

    angle = get_random_float(0, 2 * math.pi)

    BALL_GROUP.add(Ball(pos, BALL_RADIUS, vel, angle)) 


# define event handlers
def new_game() :
    ''' event handler for new game ''' 
    spawn_ball()


class Ball:
    ''' basic ball class '''
    def __init__(self, pos, radius, vel, angle):
        ''' init methos '''
        self._radius = radius
        self._pos = [pos[0], pos[1]]
        self._vel = [vel[0], vel[1]]
        self._angle = angle
	    # velocity update
        self._forward_vector = angle_to_vector(self._angle)
        # apply forward vectro to velocity
        self._vel[0] += self._forward_vector[0]
        self._vel[1] += self._forward_vector[1]

    def draw(self, canvas):
        ''' draw ball on canvas '''
        pygame.draw.circle(canvas, white_color, [int(self._pos[0]), int(self._pos[1])], self._radius, 1)

    def update(self):
        ''' updates state of ball '''
        # position update
        self._pos[0] += self._vel[0]
        self._pos[1] += self._vel[1]
        # keep on canvas
        if (self._pos[1] <= 0 + self._radius) or (self._pos[1] >= HEIGHT - self._radius) :
            # implement a bounce by reversing the vertical velocity
            self._vel[1] *= -1 
        if self._pos[0] <= 0 + BALL_RADIUS:
            self._vel[0] *= -1
            self._vel[1] *= 1
        elif self._pos[0] >= WIDTH - BALL_RADIUS:
            self._vel[0] *= -1
            self._vel[1] *= 1
 
    def set_vel(self, vel):
        ''' setter to update velocity '''
        self._vel = [vel[0], vel[1]]

    def collide(self, other):
        ''' takes another argument as an argument and returns True if there
            is a collision '''
        return False # override for now...
        # don't count colliding with self
        collide_state = False
        if self._pos != other.get_position():
            if(dist(self._pos, other.get_position()) - (self._radius + other.get_radius())) < 0:
                collide_state = True
                # stop the ball
                self._vel[0] = 0
                self._vel[1] = 0 
        return collide_state

    def bounce(self):
        ''' bounce the ball '''
        print 'Speed was ', self._vel[0], ' ', self._vel[1],
        # reverse for now...
        
        self._vel[0] *= -1
        self._vel[1] *= -1

        print 'now',  self._vel[0], ' ', self._vel[1]

    def get_position(self):
        '''' getter returns position '''
        return self._pos 

    def get_radius(self):
        '''' getter returns radius '''
        return self._radius

    


def draw_handler(canvas):
    ''' canvas draw handler '''

    # clear canvas -- fill canvas with uniform colour, then draw everything below.
    # this removes everything previously drawn and refreshes 
    canvas.fill((0, 0, 0))

    draw_colour = white_color
    text_draw = fontObj3.render("CodeSkulptor Port", True, draw_colour)

    for ball in set(BALL_GROUP):
        ball.update()
        ball.draw(canvas)

        # handle collisions
        group_group_collide(BALL_GROUP, BALL_GROUP)

    # update the display
    pygame.display.update()
 


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
    elif key == QUIT:
        pygame.quit ()



 
def keyup(key):
    ''' handler for keyup events '''
    spawn_ball()
    global paddle1_vel, paddle2_vel
    if key == LK_UP:
        paddle1_vel = 0
    elif key == LK_DOWN:
        paddle1_vel = 0
    elif key == RK_UP:
        paddle2_vel = 0
    elif key == RK_DOWN:
        paddle2_vel = 0



# helper functions
def angle_to_vector(ang):
    ''' helper converts angle to vector '''
    return [math.cos(ang), math.sin(ang)]



def dist(p, q):
    ''' helper calculates distance between args '''
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)



def wrap(pos, vect, max_val):
    ''' helper implements canvas wrapping '''
    if pos[vect] < 0:
        pos[vect] = max_val
    elif pos[vect] > max_val:
        pos[vect] = 0


def get_random_float(min_val, max_val):
    ''' helper returns a random float between two float values '''
    random_width = max_val - min_val
    return random.random() * random_width + min_val


def group_collide(set_group, other_object):
    ''' Helper takes a set group and a sprite other_object and checks for collisions
        between other_object and elements of the group. If there is a collision, the
        colliding object bounce off each other '''
    global explosion_group
    collision = False
    for element in set(set_group):
        if element.collide(other_object):
            # collision!, remove element from the group
            #explosion_group.add(Sprite(element.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))

            # bounce balls off each other
            element.bounce()
            other_object.bounce()
            #set_group.discard(element)
            collision = True
    return collision



def group_group_collide(group_1, group_2):
    ''' takes two groups of objects as input and iterates through the elements of a copy of
        the first group then calls group_collide with each of these elements on the second
        group.
        Returns the number of elements in the first group that collide with the second group
        as well as deleting these elements in the first group '''
    collisions = 0
    for element in set(group_1):
        if group_collide(group_2, element):
            collisions += 1
    return collisions



# call this function to start everything
# could be thought of as the implemntation of the CodeSkulptor frame .start() method.
def main():
    # initialize loop until quit variable
    running = True

    new_game()

    # create our FPS timer clock
    clock = pygame.time.Clock()
    # Frame is now Running

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
    tear_down()
    pygame.quit ()


def tear_down():
    ''' try and close down nicely '''
    for ball in BALL_GROUP:
        ball.remove()





if __name__ == "__main__":
    main()






''' Rice Rocks '''

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
SCORE = 0
LIVES = 0
TIME = 0.5
MAX_ROCKS = 12
STARTED = False
SHIP_ROCK_MIN_SPACE = 30
GAME_DURATION = 0



class ImageInfo:
    ''' general object info class '''
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated



# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

#thruster sound fixed by Charles Stevenson
#ship_thrust_sound = simplegui.load_sound("https://www.dropbox.com/s/296i7mjk64iibmv/ship_thrust_sound_2.mp3?dl=1")



# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]



def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)



def wrap(pos, vect, max_val):
    ''' helper implements canvas wrapping '''
    if pos[vect] < 0:
        pos[vect] = max_val
    elif pos[vect] > max_val:
        pos[vect] = 0



def get_random_float(min_val, max_val):
    ''' helper returns a random float between two float values '''
    range_width = max_val - min_val
    return random.random() * range_width + min_val



# Ship class
class Ship:
    ''' represents a ship object '''

    def __init__(self, pos, vel, angle, image, info):
        ''' init funtion '''
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_size = info.get_size()
        self.image_center = info.get_center()
        self.image_thruster_center = list(self.image_center)
        self.image_thruster_center[0] += self.image_size[0]
        self.radius = info.get_radius()
        self.forward_vector = [0, 0]
        self.rotation = 0.1

    def draw(self, canvas):
        ''' draw ship on canvas '''
        if self.thrust:
            canvas.draw_image(self.image, self.image_thruster_center, self.image_size, \
                          self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, \
                          self.pos, self.image_size, self.angle)

    def update(self):
        ''' update state of ship '''
        # velocity update
        self.angle += self.angle_vel
        self.forward_vector = angle_to_vector(self.angle)
        # position update
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # apply friction
        friction = 0.05
        self.vel[0] *= (1 - friction)
        self.vel[1] *= (1 - friction)
        self.set_sound()
        if self.thrust:
            # apply forward vector to velocity
            self.vel[0] += self.forward_vector[0]
            self.vel[1] += self.forward_vector[1]
        # keep ship on canvas
        wrap(self.pos, 0, WIDTH)
        wrap(self.pos, 1, HEIGHT)

    def set_vel(self, vel):
        ''' setter method to update velocity '''
        self.vel = [vel[0], vel[1]]

    def set_increment_rotation(self):
        self.angle_vel += self.rotation

    def set_decrement_rotation(self):
        self.angle_vel -= self.rotation

    def set_thrusters(self, thrust):
        ''' control the thrusters '''
        self.thrust = thrust

    def set_sound(self):
        ''' private helper sets off a sound '''
        if self.thrust:
            ship_thrust_sound.play()
            ship_thrust_sound.set_volume(1)
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()

    def set_shoot(self):
        ''' method fires a missile '''
        global missile_group
        # set the missile attributes
        launch_vel = 5
        # add missile velicity to ship velocity
        missile_vel = [self.vel[0] + launch_vel, self.vel[1] + launch_vel]
        # offset launch position to front of ship
        missile_pos = [(self.pos[0] + self.forward_vector[0] * self.radius), (self.pos[1] + self.forward_vector[1] * self.radius)]
        # launch!
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius



class Sprite:
    ''' Sprite class '''

    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 1
        if sound:
            sound.rewind()
            sound.play()
        # apply forward vector to velocity
        self.forward_vector = angle_to_vector(self.angle)
        self.vel[0] *= self.forward_vector[0]
        self.vel[1] *= self.forward_vector[1]

    def draw(self, canvas):
        if self.animated:
            image_loc = (self.image_center[0] + self.image_size[0] * self.age, \
                         self.image_center[1])
            canvas.draw_image(self.image, image_loc, self.image_size, \
                              self.pos, self.image_size, self.angle)
            self.age += 1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, \
                              self.pos, self.image_size, self.angle)

    def update(self):
        ''' update state of sprite '''
        # velocity update
        self.angle += self.angle_vel
        # position update
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # keep rock on canvas
        wrap(self.pos, 0, WIDTH)
        wrap(self.pos, 1, HEIGHT)
        # see if sprite is too old...
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False

    def collide(self, other):
        ''' takes an other_object as an argument and returns True if there
            is a collision or False otherwise '''
        if (dist(self.pos, other.get_position()) - (self.radius + other.get_radius())) < 0:
            return True
        else:
            return False

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius



def draw(canvas):
    global STARTED, LIVES, SCORE, rock_group, missile_group, my_ship
    # set up background animations
    background_animation(canvas)
    if STARTED:
        # draw the ship
        my_ship.draw(canvas)
        # update ship and sprites
        my_ship.update()
        process_sprite_group(canvas, rock_group)
        process_sprite_group(canvas, missile_group)
        process_sprite_group(canvas, explosion_group)
        if group_collide(rock_group, my_ship):
            LIVES -= 1
            if LIVES < 1:
                STARTED = False
        SCORE += group_group_collide(missile_group, rock_group)
        soundtrack.play()
        soundtrack.set_volume(1)
    else:
        # stop the ship
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        my_ship.set_thrusters(False)
        # clear all rocks off the screen
        clear_sprite_group(rock_group)
        clear_sprite_group(missile_group)
        clear_sprite_group(explosion_group)
        # draw splash screen
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())
        soundtrack.pause()
        soundtrack.rewind()
    # set up text on the screen
    update_screen_text(canvas)



def background_animation(canvas):
    ''' draw helper animates the background '''
    global TIME
    TIME += 1
    wtime = (TIME / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))



def update_screen_text(canvas, font_size=25, font_colour='White', font_face='sans-serif'):
    ''' draw helper draws screen text '''      
    canvas.draw_text('Lives', (80, 50), font_size, font_colour, font_face)
    canvas.draw_text(str(LIVES), (80, 80), font_size, font_colour, font_face)
    canvas.draw_text('Score', (620, 50), font_size, font_colour, font_face)
    canvas.draw_text(str(SCORE), (620, 80), font_size, font_colour, font_face)



def process_sprite_group(canvas, sprite_group):
    ''' Helper takes a set and a canvas and calls the update and draw methods for
        each sprite in the group.  '''
    for sp in set(sprite_group):
        if sp.update():
            # remove old sprite
            sprite_group.remove(sp)
        else:
            # redraw the updated sprite
            sp.draw(canvas)



def clear_sprite_group(sprite_group):
    ''' helper clears all sprites in sprite_group '''
    for sp in set(sprite_group):
        sprite_group.discard(sp)



def group_collide(set_group, other_object):
    ''' Helper takes a set group and a sprite other_object and checks for collisions
        between other_object and elements of the group. If there is a collision, the
        colliding object should be removed from the group '''
    global explosion_group
    collision = False
    for element in set(set_group):
        if element.collide(other_object):
            # collision!, remove element from the group
            explosion_group.add(Sprite(element.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            set_group.discard(element)
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



def rock_spawner():
    ''' timer handler that spawns rocks '''
    global GAME_DURATION, rock_group
    GAME_DURATION += 1
    min_vel = 1.0
    max_vel = 2.0 + (GAME_DURATION / 5)
    if STARTED:
        # set rock attributes
        angle = get_random_float(0, 2 * math.pi)
        max_rotation = 0.2
        rotation = get_random_float(-max_rotation, max_rotation)
        pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]

        velocity = [random.randrange(min_vel, max_vel), random.randrange(min_vel, max_vel)]
        # get distance from ship
        ship_distance = dist(pos, my_ship.get_position()) - (asteroid_info.get_radius() + my_ship.get_radius())
        # launch a rock
        if (len(rock_group) < MAX_ROCKS) and (ship_distance > SHIP_ROCK_MIN_SPACE):
            rock_group.add(Sprite(pos, velocity, angle, rotation, asteroid_image, asteroid_info))



# key handlers
def keydown(key):
    ''' key down handler '''
    if key == simplegui.KEY_MAP['left']:
        my_ship.set_decrement_rotation()
    if key == simplegui.KEY_MAP['right']:
        my_ship.set_increment_rotation()
    if key == simplegui.KEY_MAP['up']:
        my_ship.set_thrusters(True)
    if key == simplegui.KEY_MAP['space']:
        my_ship.set_shoot()



def keyup(key):
    ''' key up handler '''
    if key == simplegui.KEY_MAP['left']:
        my_ship.set_increment_rotation()
    if key == simplegui.KEY_MAP['right']:
        my_ship.set_decrement_rotation()
    if key == simplegui.KEY_MAP['up']:
        my_ship.set_thrusters(False)



def click(pos):
    ''' mouseclick handlers that reset UI and conditions whether splash image is drawn '''
    global STARTED, LIVES, SCORE
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not STARTED) and inwidth and inheight:
        STARTED = True
        SCORE = 0
        LIVES = 3



# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)


# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])



# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)


timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()




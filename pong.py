# Implementation of classic arcade game Pong (Known as Ping-Pong in the UK)

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True




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
    
    # ransomise start direction and spawn the ball
    spawn_ball(random.choice([LEFT, RIGHT]) )




def draw(canvas):
    ''' handler to draw canvas '''
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global ball_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White") # mid line
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White") # left gutter
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White") # right gutter
                
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if (ball_pos[1] <= 0 + BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS) :
        # ball has hit either the top or bottom of the screen, implement a bounce 
        # by reversing the vertical velocity
        ball_vel[1] *= -1    
          
    # draw ball
    canvas.draw_circle([ball_pos[0], ball_pos[1]], BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = calculate_paddel_position(paddle1_pos, paddle1_vel)
    paddle2_pos = calculate_paddel_position(paddle2_pos, paddle2_vel)       
        
    # draw paddles
    canvas.draw_line([0 + HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [0 + HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")

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
   
        
    # draw score
    canvas.draw_text(str(score1), ((WIDTH / 2) - 60, 60), 50, "White")
    canvas.draw_text(str(score2), ((WIDTH / 2) + 60, 60), 50, "White")

    

    
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
    if key == simplegui.KEY_MAP['w'] :
        paddle1_vel = -velocity
    elif key == simplegui.KEY_MAP['s'] :
        paddle1_vel = velocity
    elif key == simplegui.KEY_MAP['up'] :
        paddle2_vel = -velocity
    elif key == simplegui.KEY_MAP['down'] :
        paddle2_vel = velocity
   


   
def keyup(key):
    ''' handler for keyup events '''
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w'] :
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s'] :
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up'] :
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down'] :
        paddle2_vel = 0
 



def restart_button_handler() :
    ''' handler for restart button '''
    new_game()

    



# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', restart_button_handler, 100)




# start frame
new_game()
frame.start()





''' 
Stopwatch: The Game 
A game to test your reflexes
'''

import simplegui


# define global variables
timer_op = 0
button_size = 50
frame_width = 300
frame_height = 200
timer_rate = 100 # for time set to 0.1 of a second
stopwatch_is_running = False
try_count = 0
sucess_count = 0


# helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    ''' assumes argument t is time in 1/10 seconds
    returns a string of the form A:BC.D 
    where A, C and D are digits in the range 0-9 
    and B is in the range 0-5 '''
       
    # calculate minutes A
    A =  t // 600     # 60 seconds per minute x 10
    
    # calculate tens of seconds (0-5) B
    B = ((t % 600) // 10) // 10
    
    # calculate units of seconds (0-9) C
    C = ((t % 600) // 10) % 10
    
    # calculate remaining tenths_of_seconds     
    D = (t % 600) % 10
    
    # return in form of "0:00.0"
    return str(A) + ':' + str(B) + str(C) + '.' + str(D)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button() :
    ''' Start button event handler '''
    global stopwatch_is_running
    stopwatch_is_running = True
    timer.start()
    

def stop_button() :
    ''' Stop button event handler '''
    global stopwatch_is_running, try_count, sucess_count
    timer.stop()
    if stopwatch_is_running :
        # we are in a game
        try_count += 1
        if timer_op % 10 == 0 :
            sucess_count += 1
    stopwatch_is_running = False
    

def reset_button() :
    ''' Reset button event handler '''
    global timer_op, try_count, sucess_count
    timer.stop()    
    # reset globals
    timer_op = 0
    stopwatch_is_running = False
    try_count = 0
    sucess_count = 0


def timer_handler():
    ''' 0.1 second timer event handler '''
    global timer_op, canvas
    timer_op += 1
        

def draw_handler(canvas) :
    ''' draw handler '''
    # output the time counter
    # position text in center of screen
    text_size = 50
    text_face = "sans-serif"
    time_str = str(format(timer_op))
    text_width = frame.get_canvas_textwidth(time_str, text_size, text_face)
    text_colour = 'Red'
    x_pos = (frame_width / 2) - (text_width / 2)
    y_pos = (frame_height / 2)
    canvas.draw_text(time_str, (x_pos, y_pos), text_size, text_colour, text_face)

    # output the results of player's reflexes
    x = sucess_count
    y = try_count
    result_str = str(sucess_count) + '/' + str(try_count)
    # draw in upper right of screen
    canvas.draw_text(result_str, (frame_width - 45, 30), 20, text_colour, text_face)

    
# create frame
frame = simplegui.create_frame("Stopwatch The Game", frame_width, frame_height)


# register event handlers
timer = simplegui.create_timer(timer_rate, timer_handler)
frame.set_canvas_background('White')
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start_button, button_size)
frame.add_button("Stop", stop_button, button_size)
frame.add_button("Reset", reset_button, button_size)


# start frame
frame.start()





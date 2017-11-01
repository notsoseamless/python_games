''' template for "Guess the number" mini-project ='''

import simplegui
import random
import math


# globals
secret_number = 0
num_of_guesses = 0




def new_game():
    ''' helper function to start and restart the game '''
    global secret_number, num_of_guesses
    
    # NOTE: could have saved code here by calling range100() but
    # I think professors wanted us to keep the handlers seperate.
    
    low = 0
    high = 100

    # initialize global variables used in your code here
    secret_number = random.randrange(low, high)
    num_of_guesses = compute_num_of_guesses(low, high)
    print '\n' * 2
    print 'New game. Range is from ' + str(low) + ' to ' + str(high)
    print 'Number of remaining guesses is ' + str(num_of_guesses)


    
def compute_num_of_guesses(low, high):
    ''' compute range using the given formula: 2 ** n >= high - low + 1 '''    
    range = high - low + 1    
    # use base 2 log
    return int(math.ceil(math.log(range, 2)))


def range100():
    ''' button handler that changes the range to [0,100) and starts a new game '''
    
    global secret_number, num_of_guesses

    low = 0
    high = 100

    # initialize global variables used in your code here
    secret_number = random.randrange(low, high)
    num_of_guesses = compute_num_of_guesses(low, high)
    print '\n' * 2
    print 'New game. Range is from ' + str(low) + ' to ' + str(high)
    print 'Number of remaining guesses is ' + str(num_of_guesses)

    
    

def range1000():
    ''' button handler that changes the range to [0,1000) and starts a new game '''
    
    global secret_number, num_of_guesses

    low = 0
    high = 1000

    # initialize global variables used in your code here
    secret_number = random.randrange(low, high)
    num_of_guesses = compute_num_of_guesses(low, high)
    print '\n' * 2
    print 'New game. Range is from ' + str(low) + ' to ' + str(high)
    print 'Number of remaining guesses is ' + str(num_of_guesses)

    
    
    
def input_guess(guess):
    ''' input event handler '''
    
    global secret_number, num_of_guesses
    
    # print out the guess
    print
    print 'Guess was ' + guess
    
    num_of_guesses -= 1
    print 'Number of remaining guesses is ' + str(num_of_guesses)
  
    # converts it to an integer
    int_guess = int(guess) 
    
    if num_of_guesses >= 0 :
        if int_guess > secret_number:
             print 'Lower'
        elif int_guess < secret_number:
            print 'Higher'
        else:
            print 'Correct'
            new_game()
    else:
        print 'You ran out of guesses. The number was ' + str(secret_number)
        new_game()
    



# create the frame
frame = simplegui.create_frame("Guess the number", 200, 200)




# register event handlers for control elements and start frame
frame.add_input("guess:", input_guess, 100)
frame.add_button("Range: 0 - 100", range100)
frame.add_button("Range: 0 - 1000", range1000)




# call new_game 
new_game()


# always remember to check your completed program against the grading rubric


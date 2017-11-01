# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings

''' Rock-paper-scissors-lizard-Spock '''


import random




def name_to_number(name):
    ''' convert name to number using if/elif/else '''
    result = 0
    if name == 'rock':
        result = 0
    elif name == 'Spock':
        result = 1
    elif name == 'paper':
        result = 2
    elif name == 'lizard':
        result = 3
    elif name == 'scissors':
        result == 4
    else:
        result = -1
        print 'ERROR: number out of range'
        exit(1)
    return result




def number_to_name(number):
    ''' convert number to a name using if/elif/else '''
    result = ''
    if number == 0:
        result = 'rock'
    elif number == 1:
        result = 'Spock'
    elif number == 2:
        result = 'paper'
    elif number == 3:
        result = 'lizard'
    elif number == 4:
        result = 'scissors'
    else:
        result = 'UNKNOWN'
        print 'ERROR: name not known'
        exit(1)
    return result


    

def rpsls(player_choice): 
    # print a blank line to separate consecutive games
    print

    # print out the message for the player's choice
    print 'Player chooses ' + player_choice

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 4)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    
    # print out the message for computer's choice
    print 'Computer chooses ' + comp_choice

    # compute difference of comp_number and player_number modulo five
    difference = (comp_number - player_number) % 5

    # use if/elif/else to determine winner, print winner message
    if (difference == 1) or (difference == 2):
        print 'Computer wins!'
    elif  (difference == 3) or (difference == 4):
        print 'Player wins!'
    else:
        print 'Player and computer tie!'

    


def main():
    ''' test code '''
    rpsls("rock")
    rpsls("Spock")
    rpsls("paper")
    rpsls("lizard")
    rpsls("scissors")




if __name__ == "__main__":
    main()




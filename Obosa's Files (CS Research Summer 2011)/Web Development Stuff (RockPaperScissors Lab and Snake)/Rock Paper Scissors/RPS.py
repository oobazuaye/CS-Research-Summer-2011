import random
def RPS(mychoice):
    #mychoice = input("What do you pick? 'Rock', 'Paper', or 'Scissors'? \n")
    choices = ['Rock', 'Paper', 'Scissors']
    compchoice = random.choice(choices)
    outcome = (mychoice, compchoice)
    #print 'You chose',mychoice,'.'
    #print 'The computer chooses', compchoice,'.'
    if mychoice == compchoice:
     #   print 'You tie.'
        outcome = (mychoice, compchoice, 'you tie.')
        return outcome
    elif outcome == ('Rock', 'Scissors') or \
    outcome == ('Scissors', 'Paper') or \
    outcome == ('Paper', 'Rock'):
      #  print 'You win!'
        outcome = (mychoice, compchoice, 'you win!')
        return outcome
    else:
       # print 'You lose!'
        outcome = (mychoice, compchoice, 'you lose!')
        return outcome
    

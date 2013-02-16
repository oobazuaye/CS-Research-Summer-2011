import time
from turtle import *
import csgrid; from csgrid import *
from random import *
screen = Screen()

def evolve2d(board, i, j):
    """Takes a board and two numbers 'i' and 'j' as input, which represent a row and column in the board.
        Changes the colors of spaces on the grid surrounding the square at board[i][j]
        according to the rules of Lights Out. Uses evolve1d if the board is just 1 list."""
    if type(board[0]) == int: #If the board is just 1 list...
        board = evolve1d(board, j)
    else:
        if i != 0 and j != 0 and i != len(board)-1 and j != len(board[0])-1: #Not on a border
            board[i][j-1] = 1 - board[i][j-1] #Left Cell
            board[i][j+1] = 1 - board[i][j+1] #Right Cell
            board[i-1][j] = 1 - board[i-1][j] #Top Cell
            board[i+1][j] = 1 - board[i+1][j] #Bottom Cell
            board[i][j] = 1 - board[i][j] #Same Cell
        if i == 0 and j != 0 and j != len(board[0])-1: #Top row
            board[i][j] = 1 - board[i][j] #Same Cell
            board[i][j-1] = 1 - board[i][j-1] #Left Cell
            board[i][j+1] = 1 - board[i][j+1] #Right Cell
            board[i+1][j] = 1 - board[i+1][j] #Bottom Cell
        if i == 0 and j == 0: #Top left corner
            board[i][j] = 1 - board[i][j] #Same Cell
            board[i][j+1] = 1 - board[i][j+1] #Right Cell
            board[i+1][j] = 1 - board[i+1][j] #Bottom Cell
        if i == 0 and j == len(board[0])-1: #top right corner
            board[i][j] = 1 - board[i][j] #Same Cell
            board[i][j-1] = 1 - board[i][j-1] #Left Cell
            board[i+1][j] = 1 - board[i+1][j] #Bottom Cell
        if i != 0 and j == 0 and i != len(board)-1: #left column
            board[i][j] = 1 - board[i][j] #Same Cell
            board[i-1][j] = 1 - board[i-1][j] #Top Cell
            board[i][j+1] = 1 - board[i][j+1] #Right Cell
            board[i+1][j] = 1 - board[i+1][j] #Bottom Cell
        if j == 0 and i == len(board)-1: #bottom left corner
            board[i-1][j] = 1 - board[i-1][j] #Top Cell
            board[i][j] = 1 - board[i][j] #Same Cell
            board[i][j+1] = 1 - board[i][j+1] #Right Cell
        if i != 0 and i != len(board)-1 and j == len(board[0])-1: #right column
            board[i][j-1] = 1 - board[i][j-1] #Left Cell
            board[i][j] = 1 - board[i][j] #Same Cell
            board[i-1][j] = 1 - board[i-1][j] #Top Cell
            board[i+1][j] = 1 - board[i+1][j] #Bottom Cell
        if i == len(board)-1 and j == len(board[0])-1: #bottom right corner
            board[i][j] = 1 - board[i][j] #Same Cell
            board[i-1][j] = 1 - board[i-1][j] #Top Cell
            board[i][j-1] = 1 - board[i][j-1] #Left Cell
        if i == len(board)-1 and j != 0 and j != len(board[0])-1: #bottom row
            board[i][j-1] = 1 - board[i][j-1] #Left Cell
            board[i][j] = 1 - board[i][j] #Same Cell
            board[i-1][j] = 1 - board[i-1][j] #Top Cell
            board[i][j+1] = 1 - board[i][j+1] #Right Cell
    return board

def evolve1d(L,x):
    """ evolve1d takes in a list of integers, L,
          and returns a new list of integers
          considered to be the "next generation"
    """
    N = len(L)  # N now holds the size of the list L
    return [setNewElement(L, i, x) for i in range(N)]

def setNewElement(L, i, x):
    """ setNewElement returns the NEW list's ith element
          input L: any list of integers
          input i: the index of the new element to return
          input x: an extra, optional input for future use
    """
    if abs(i-x)<=1:  # if it's the user's chosen column,
        return 1-L[i]            # toggle the one clicked
    else:                        # otherwise,
        return L[i]
    
def newBoard(sidelength):
    """Returns a board of size sidelength x sidelength with 0's and 1's in random positions"""
    board = []
    row = []
    for num in range(sidelength):
        for bum in range(sidelength):
            row.append(choice([0,1])) #creates a row of zeroes and ones
        board.append(row) #adds the row of zeros to the new blank board
        row = []
    return board

def lightsMouseHandler(x,y):
    """ This function is called with each mouse click.

        Its inputs are the pixel location of the
        next mouse click: (x,y)
        
        It computes the column and row(within the list)
        where the click occurred with getPos.

        Then, this function calls the next board via evolve2d
    """
    global board
    row = getPos(x,y)[0]
    col = getPos(x,y)[1]
    board = evolve2d(board, row, col)
    show(board)
    if allZeroes(board) or allOnes(board): #If the game is over...
        running = False
        print "\nYou've won!!"
        screen.ontimer(bye, t=3000) #closes the window after 3 seconds
        return
    
def allOnes(L):
    """Checks if the board is all ones"""
    if type(board[0]) == int: #If the board is only 1 list...
        return L == [1]*len(L)
    else: #If the board is a grid...
        counter = 0
        for List in L:
            if List == [1]*len(List): counter+=1
        return counter == len(L)
    
def allZeroes(L):
    """Checks if the board is all zeroes"""
    if type(board[0]) == int: #If the board is only 1 list...
        return L == [0]*len(L)
    else: #If the board is a grid...
        counter = 0
        for List in L:
            if List == [0]*len(List): counter+=1
        return counter == len(L)

def showgood():
    """Used for the random square-choosing version
        of Lights Out. Picks a random square, and changes
        the board."""
    global board
    row = choice(range(len(board)))
    col = choice(range(len(board)))
    board = evolve2d(board, row, col)
    show(board)

running = True
def showgood2():
    """Runs the random square-choosing version of the game.
        Allows for pausing with "p", resuming with "Enter"/"Return",
        and ends the game when the board is all of one color."""
    global board
    global running
    screen.onkey(gamepause, "p")
    screen.onkey(gameresume, "Return")
    screen.listen()
    if running:
        if allZeroes(board) or allOnes(board): #If the game is over...
            running = False
            print "You've won!!"
            screen.ontimer(bye, t=3000) #Closes the screen after 3 seconds
            return
        else:
            showgood()
            screen.ontimer(showgood2, 1000)

def gamepause():
    """Pauses the game."""
    global running
    running = False

def gameresume():
    """Resumes a paused game."""
    global running
    running = True
    showgood2()

# here is where your starting conditions go...
# when it runs, it will be ready to play
global listlen #This global variable represents the length of each row and column of the board
listlen = 6
global board #This global variable represents the board itself
board = newBoard(listlen) #This starts out the board as a random board using newBoard.
#You can replace this line with board = [some list that you would like the board to be]
#For example, you could use board = [ 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 ]
# to make a board that is a single list with only 1 spot lit.

screen.listen()
screen.onscreenclick(lightsMouseHandler) #Allows the board to be played by screen click
screen.onkey(showgood2, "Return") #Starts the random version of the game by pressing Return/Enter
screen.onkey(bye, "Escape") #Closes the game by pressing escape
print "Welcome to the game of 'Lights Out'!!\n"
print "Click a square to change the color of it and \nits horizontal and vertical neighbors.\n"
print "You win when all the squares are of the same color.\n"
print "You can start a version where the computer \npicks a random square every second \nby pressing 'Return'/'Enter'.\n"
print "You can pause this random version by pressing 'p', \nand resume it by pressing 'Return'/'Enter'.\n"
print "The game can be closed at any time by \npressing the 'Escape' key.\n"
print "Have fun!! :D"
show(board)
done()


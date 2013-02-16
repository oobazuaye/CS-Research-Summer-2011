import time
from turtle import *
import csgrid; from csgrid import *
from random import *
screen = Screen()

def evolve2d(board, i, j):
    """Takes a board and two numbers 'i' and 'j' as input, which represent a row and column in the board.
        Returns the number of '1's in the 8 surrounding cells of the cell at row 'i' and column 'j'"""
    if i != 0 and j != 0 and i != len(board)-1 and j != len(board[0])-1: #Not on a border
        board[i][j-1] = 1 - board[i][j-1] #Left Cell
        board[i][j+1] = 1 - board[i][j+1] #Right Cell
        board[i-1][j] = 1 - board[i-1][j] #Top Cell
        board[i+1][j] = 1 - board[i+1][j] #Bottom Cell
        board[i][j] = 1 - board[i][j] #Same Cell
    if i == 0 and j != 0 and j != len(board[0])-1: #Top row
        board[i][j] = 1 - board[i][j]
        board[i][j-1] = 1 - board[i][j-1]
        board[i][j+1] = 1 - board[i][j+1]
        board[i+1][j] = 1 - board[i+1][j]
    if i == 0 and j == 0: #Top left corner
        board[i][j] = 1 - board[i][j]
        board[i][j+1] = 1 - board[i][j+1]
        board[i+1][j] = 1 - board[i+1][j]
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

def newBoard(sidelength):
    """Returns a board with the given number of rows and columns with 0's in all of the positions"""
    board = []
    row = []
    for num in range(sidelength):
        for bum in range(sidelength):
            row.append(choice([0,1])) #creates a row of zeroes and ones
        board.append(row) #adds the row of zeros to the new blank board
        row = []
    return board
def mouseHandler(x,y):
    """ This function is called with each mouse click.

        Its inputs are the pixel location of the
        next mouse click: (x,y)
        
        It computes the column (within the list)
        where the click occurred with getCol.

        The overall list is shared between turtle graphics
        and the other parts of your program as a global
        variable named currentL. In general, global variables
        make software more complex, but sometimes they are
        necessary.

        Then, this function calls the next generation via
        runGraphicsGen( L, col ) - note that the col is available!
    """
    global board
    row = getPos(x,y)[0]
    col = getPos(x,y)[1]
    board = evolve2d(board, row, col)
    show(board)
#n=0
def showgood():
    #global n
    global board
    global listlen
    row = getPos(x,y)[0]
    col = getPos(x,y)[1]
    #n = n+1
    board = evolve2d(board, row, col)
    show(board)
    
#def allOnes(L): return L == [1]*len(L)
#def allZeroes(L): return L == [0]*len(L)

running = True
def showgood2():
    global board
    global running
    screen.onkey(lifepause, "p")
    screen.onkey(liferesume, "r")
    screen.listen()
    if running:
        showgood()
        screen.ontimer(showgood2, 1000)

def lifepause():
    global running
    running = False

def liferesume():
    global running
    running = True
    showgood2()
# here is where your starting conditions go...
# when it runs, it will be ready to play
# however, you'll need to change the setNewElement function, above
# in order to play according to the "Lights out" rules...
global listlen
listlen = 6
global board
board = newBoard(listlen)
#columnsUsed = runGenerations(startingList)
#print columnsUsed
screen.listen()
#for num in range(columnsUsed[0]):
#    ontimer(showgood, t = 100*num)
screen.onscreenclick(mouseHandler)
screen.onkey(showgood2, "Return")
screen.onkey(bye, "Escape")
show(board)
#startingList = [ 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 ]
#show( startingList )

done()  # your system may need this line uncommented...

'''
while not allZeroes(L):
    col = choice(range(listlen))
    L = csgrid.currentL
    runGraphicsGen(L, col)
''' 


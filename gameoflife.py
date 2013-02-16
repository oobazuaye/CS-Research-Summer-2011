import time
from turtle import *
import csgrid; from csgrid import *
from random import *
screen = Screen()

#A sample board you can try.
board1 = [ [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]]

#Another sample board you can try. 
board2 = [
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0]]

def blankBoard(rows, cols):
    """Creates a board with the given number of
        rows and columns with 0's in all positions."""
    board = []
    row = []
    for num in range(rows):
        for bum in range(cols):
            if num == 0 or num == rows-1 or bum == 0 or bum == cols-1:
                row.append(2)
            else: row.append(0) #creates a row of zeros
        board.append(row) #adds the row of zeros to the new blank board
        row = []
    return board

def neighbors(board, i, j):
    """Takes a board and two numbers 'i' and 'j' as input, which represent a row and column in the board.
        Returns the number of '1's in the 8 surrounding cells of the cell at row 'i' and column 'j'"""
    counter = 0
    if board[i][j-1] == 1: counter +=1 #If the cell to the left of the current place is a 1, add 1 to the number of neighbors counted.
    if board[i][j+1] == 1: counter +=1 #If the cell to the right of the current place is a 1, add 1 to the number of neighbors counted.
    for num in board[i-1][j-1:j+2]: 
        if num ==1: counter +=1 #For each cell above the current place that is a 1, add 1 to the number of neighbors counted.
    for num in board[i+1][j-1:j+2]:
        if num ==1: counter +=1 #For each cell below the current place that is a 1, add 1 to the number of neighbors counted.
    return counter

def nextBoard( board ):
    """Takes a 'board' as input, constructs a new blank board using
    'blankBoard', uses the Life rules to populate that board to correspond
    to the next generation, and then returns the new board."""
    newBoard = blankBoard(len(board), len(board[0]))
    for num in range(len(board)):
        for bum in range(len(board[0])):
            if board[num][bum] == 1: #If the current cell being inspected is a 1 (a live cell)...
                neighborhood = neighbors(board, num, bum) #Count the number of live neighbors this cell has.
                if neighborhood < 2 or neighborhood > 3: #If the number of live neighbors is below two or is above three...
                    newBoard[num][bum] = 0 #The cell dies.
                else:
                    newBoard[num][bum] = 1 #Otherwise, the cell survives.
            if board[num][bum] == 0:
                if num != 0 and bum != 0 and num != len(board)-1 and bum != len(board[0])-1: #If the cell is empty and is not on the border...
                    neighborhood = neighbors(board, num, bum) #Count the number of neighbors this cell has.
                    if neighborhood == 3: #If the number of live neighbors this cell has is exactly equal to three...
                        newBoard[num][bum] = 1 #This empty cell comes to life.
    return newBoard

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
    """Makes the next life generation appear"""
    global board
    board = nextBoard(board)
    show(board)

running = True
def showgood2():
    """Sets the board to keep moving through generations of life.
        Allows for pausing with "p", resuming with "Enter"/"Return",
        and automatically pauses the game if the board stops changing
        or becomes blank."""
    global board
    global running
    screen.onkey(gamepause, "p")
    screen.onkey(gameresume, "Return")
    screen.listen()
    if running:
        if board == nextBoard(board) == nextBoard(nextBoard(board)) or allZeroes(board):
            running = False
        else:
            showgood()
            screen.ontimer(showgood2, t=0)
            #The t value above sets how many milliseconds there are
            # between each generation of life. Set it low (e.g. 0 seconds, or 500
            # for half a second, etc.) for fast movement, or
            # set it high (e.g. 1000 for 1 second, 3000 for 3 seconds, etc.)
            # for fast slower movement.

def gamepause():
    """Pauses the game"""
    global running
    running = False

def gameresume():
    """Resumes a paused game."""
    global running
    running = True
    showgood2()
    
def blank():
    """Makes the board blank (resets the board)"""
    global board
    board = blankBoard(rows, cols)
    show(board)

print "Welcome to the game of 'Life'!!\n"
print "Click on a blank square to bring it to life,\nor on a live square to kill it.\n"
print "By pressing 'Return'/'Enter', the simulation begins.\n"
print "The rules of the game are as follows:\n"
print "\n1. A cell that has fewer than\ntwo live neighbors dies (because of loneliness)."
print "\n2. A cell that has more than \nthree live neighbors dies (because of over-crowding)."
print "\n3. A cell that is dead and has\nexactly three live neighbors comes to life."
print "\n4. All other cells maintain their state.\n"
print "\nThe game automatically pauses\nif the board stops changing or becomes blank.\n"
print "You can pause the game by 'p', \nand resume it by pressing 'Return'/'Enter'.\n"
print "You can reset the board (make all squares blank)\nby pressing the 'Space' key.\n"
print "You can change the speed of the simulation\nby going to the function 'showgood2()',"
print "and changing the numerical value given\nto the variable t at the end of the function.\n"
print "The game can be closed at any time\nby pressing the 'Escape' key.\n"
print "Have fun!! :D"

print "\n\n\n What size would you like your board to be?"
print "(The two rows and columns on the ends will be borders)\n"
rows = input("Rows: ") #number of rows on the board. The two on the ends will be borders.
cols = input("Columns: ") #number of columns on the board. The two on the ends will be borders.
print "\n"

#Replace the 5 lines above with
# rows = number of rows you want
# cols = number of columns you want
#if you don't want to use input at the start.

# here is where your starting conditions go...
# when it runs, it will be ready to play.
#You can change the size of the board, but a size of 
global board
board = blankBoard(rows, cols) #Starts the board with a blank board.
#If you would like to use one of the sample boards, simply replace the line
# with board = board2, board = board1, etc.

screen.listen()
onscreenclick(lifeMouseHandler)
screen.onkey(showgood2, "Return")
screen.onkey(bye, "Escape")
screen.onkey(blank, "space")


show(board)
done()  

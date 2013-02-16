# hw3pr1.py - Lab problem: "Lights On!"
#
# Name:



# Most of your Lab 3 code will go here:














# Note: the code below is for the optional
#       graphics part of this lab.
# Feel free to ignore - at least til then.
#
# Mac OS X users likely need to uncomment
# the done() line at the very bottom here.

import time
from turtle import *
import csgrid; from csgrid import *
from random import *
screen = Screen()


'''
def runGenerations1(L):
    """ runGenerations keeps running the evolve function...
    """
    #print L                 # display the list, L
    #time.sleep(0.5)         # pause a bit
    if allZeroes(L): return 0
    else:
        col = choice(range(listlen))
        newL = evolve(L,col)        # evolve L into newL
        return 1 + runGenerations(newL)    # recur
'''
def runGenerations(L):
    columnsUsed = []
    print L
    while allZeroes(L) == False:
        col = choice(range(listlen))
        columnsUsed.append(col)
        L = evolve(L, col)
    return [len(columnsUsed), columnsUsed]
    
def runGraphicsGen(L,col):
    """ L is the list last displayed
        evolve L first
    """
    print "col is", col
    L = evolve(L,col)
    show(L)             # display
    if allZeroes(L):
        print "Hooray!"
        return
       # time.sleep(2)
       # bye()
      #  return
    
    # We finish here!
    
    # When the mouse is clicked,
    # this will be called again!

    # L is "remembered" by show (in a "global"
    # variable) and is later passed in by the
    # graphics system. Global variables are
    # best avoided, but sometimes are required.

def evolve(L,x):
    """ evolve takes in a list of integers, L,
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
        return L[i]              # return the original


'''
# set the mouse handler...
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
    col = getCol(x,y)
    L = csgrid.currentL  # get from the graphics module
    if not allZeroes(L):
        col = choice(range(listlen))
        runGraphicsGen(L, col)
        mouseHandler
   #runGraphicsGen(L,col)

def looper():
    col = choice(range(listlen))
    L = csgrid.currentL  # get from the graphics module
    print L
    runGraphicsGen(L, col)

def keyHandler():
    col = choice(range(listlen))
    L = csgrid.currentL
    runGraphicsGen(L, col)

def looper():
    col = columnsUsed[1][num]
    L = csgrid.currentL
    runGraphicsGen(L, col)
#    time.sleep(2)
#    looper()

    if not allZeroes(L):
        screen.ontimer(runGraphicsGen(L, col), 250)
        looper()
    else:
        bye()

'''
board = []
def newBoard(sidelength):
    """Returns a board with the given number of rows and columns with 0's in all of the positions"""
    global board
    row = []
    for num in range(sidelength):
        for bum in range(sidelength):
            row.append(choice([0,1])) #creates a row of zeros
        board.append(row) #adds the row of zeros to the new blank board
        row = []
    return board

n=0
def showgood():
    global n
    square = choice(choice(board))
    n = n+1
    L = csgrid.currentL
    runGraphicsGen(board, square)
    
def allOnes(L): return L == [1]*len(L)
def allZeroes(L): return L == [0]*len(L)

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
listlen = 6
global board
board = newBoard(listlen)
#columnsUsed = runGenerations(startingList)
#print columnsUsed
screen.listen()
#for num in range(columnsUsed[0]):
#    ontimer(showgood, t = 100*num)
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


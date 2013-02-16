# hw3pr1.py - Lab problem: "Lights On!"
#
# Name:



# Most of your Lab 3 code will go here:


import time           # provides time.sleep(0.5)
from random import *  # provides choice([0,1]), etc.
import sys            # larger recursive stack
sys.setrecursionlimit(100000) # 100,000 deep - in theory


def runGenerations(L):
    """ runGenerations keeps running the evolve function...
    """
    print L                 # display the list, L
    time.sleep(0.5)         # pause a bit
    if allOnes(L): return 0
    else:
        newL = evolve(L)        # evolve L into newL
        return 1 + runGenerations(newL)    # recur

def allOnes(L):
    if L == []: return True
    else:
        if L[0] == 1: return allOnes(L[1:])
        else: return False
        

def evolve(L):
    """ evolve takes in a list of integers, L,
          and returns a new list of integers
          considered to be the "next generation"
    """
    N = len(L)  # N now holds the size of the list L
    x = choice(range(N))#input("Enter an index to change: ")  # Get numeric input from user
    return [setNewElement(L, i, x) for i in range(N)]


def setNewElement(L, i, x):
    """ setNewElement returns the NEW list's ith element
          input L: any list of integers
          input i: the index of the new element to return
          input x: an extra, optional input for future use
    """
    if i == x:  # if it's the user's chosen column,
        return 1 - L[i]
    if i == x-1:
        return 1 - L[i]
    if i == x+1:
        return 1 - L[i]
    else:                        # otherwise,
        return L[i]              # return the original


def randBL(N):
    newlist = []
    for num in range(N):
        newlist.append(choice([0,1]))
    return newlist





# Note: the code below is for the optional
#       graphics part of this lab.
# Feel free to ignore - at least til then.
#
# Mac OS X users likely need to uncomment
# the done() line at the very bottom here.


from turtle import *
import csgrid; from csgrid import *
from random import *

def runGraphicsGen(L,col):
    """ L is the list last displayed
        evolve L first
    """
    print "col is", col
    L = evolve(L,col)
    show(L)             # display
    if allOnes(L):
        print "Hooray!"
        return
    
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
    runGraphicsGen(L,col)

def allOnes(L): return L == [1]*len(L)

onscreenclick(mouseHandler)

# here is where your starting conditions go...
# when it runs, it will be ready to play
# however, you'll need to change the setNewElement function, above
# in order to play according to the "Lights out" rules...

startingList = [ 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 ]
show( startingList )

done()  # your system may need this line uncommented...







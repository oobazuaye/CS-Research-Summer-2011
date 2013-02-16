from turtle import *
import time

forward(10) # forces a redraw

s = Screen()  # get the graphics object from turtle

#print s

c = s.getcanvas()  # get the canvas on which the turtle is drawn

test_line = c.create_line(10,0, 100, 100)  # create a line named test_line

# set some parameters of test_line -- a bit roundabout (through c)
c.itemconfigure( test_line, # the item
                 fill='red', # the parameters...
                 width=3 )

print "Done with line creation"

forward(0)  # forces a redraw - may not be the most efficient way...
time.sleep(.5)

c.coords( test_line, 10,0, -125,125 )

forward(0)
time.sleep(.5)

c.delete( test_line )


forward(0) # force a redraw
time.sleep(.5)

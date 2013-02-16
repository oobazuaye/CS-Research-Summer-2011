from turtle import *
from math import *
import math

def axis_draw(min_x, max_x, min_y, max_y):
    '''Draws the x and y axes on screen based on the given
    minimum and maximum x and y values, and returns
    the x position of the y axis and the
    y position of the x axis '''
    
    screen = Screen()
    end =  - window_width() / 2.0 #Left edge of the screen
    top = window_height() / 2.0 # Top of the screen
    real_width = window_width() #Real window width
    real_height = window_height() #Real window height
    wide = max_x - min_x #Inputted x axis width
    height = max_y - min_y #Inputted y axis height
    x_step = ((wide) / 2.) / 100. # How far apart each data point will be graphed on the screen
    number_of_x_values = int((wide) / x_step) #Number of x values that will be taken
    
    speed("fastest") #Speed at which the axes will be drawn
    hideturtle() #Hides the turtle cursor so that drawing is faster
    width(3) #Pixel thickness of the axes
    
    #The next two variables are:
    # - The x position of the y axis
    # - The y position of the x axis
    y_axis = end + (((0 - min_x) / (1. * wide)) * real_width)
    x_axis = -top + (((0 - min_y) / (1. * height)) * real_height)
    
    penup()
    setpos(end, x_axis) #Starting position for drawing the x axis (Far left)
    pendown()
    setpos(-end, x_axis) #Move to the far right (completed x axis)
    penup()
    setpos(y_axis, top) #Move to the top of the y axis
    pendown()
    setpos(y_axis, -top) #Move to the bottom (completed y axis)
    penup()
    setpos(end, x_axis) #Starting position for drawing the x axis interval markers
    pendown()
    
    x_interval = -end / wide #relative distance between each x interval tick
    y_interval = top / height #relative distance between each y interval tick
    
    for num in range(int(wide+1)):
   #for each interval tick...
        seth(90) #aim upward
        color('blue')
        forward(10) 
        backward(20) 
        forward(10)
        #draw a blue 20 pixel-long tick (10 on each side of axis)
        color('black')
        if round(xcor(), 1) != -round(end, 1):
       #if not at the end of the axis:
            setpos(xcor() + 2*x_interval, x_axis)
            #move one relative interval distance to the right
            
    penup()
    setpos(y_axis, top) #Starting position for drawing the y axis interval markers
    pendown()
    
    for num in range(int(height+1)):
   #for each interval tick...
        seth(0) #aim to the right
        color('blue')
        forward(10)
        backward(20)
        forward(10)
        #draw a blue 20 pixel-long tick (10 on each side of axis)
        color('black')
        if round(ycor(), 1) != -round(top, 1):
       #if not at the end of the graph:
            setpos(y_axis, ycor() - 2*y_interval)
           #move one relative interval distance downward

    print #make a new line between the prompts used in grapher
    return x_axis, y_axis

    
def grapher():
    '''Graphs stuff in turtle!
        Asks for boundaries of the axes,
        asks for function to be graphed,
        and asks if integral rectangles should be
        drawn under the graph.'''
    
    print "Welcome to Grapher! \n"
    print "Feel free to type any requested text inputs \n\
with or without quotes.\n"
    print "Make sure your function is simply a function of x \n\
(e.g. 4*x, sin(x), x**2, etc.) \n"
    print "For a list of functions, exit by typing 'quit', \n\
and then type help(math). \n"
    print "After the graph has been drawn, \n\
you may close the window \n\
by clicking inside the graph window, \n\
or by any regular window-closing method. \n"

    #Dictionary of x and y axis boundaries:
    #default values are -10 to 10.
    values = {"minimum value of the x axis": -10,
              "maximum value of the x axis": 10,
              "minimum value of the y axis": -10,
              "maximum value of the y axis": 10}
    ok = 'ok' #If the user types ok or 'ok', it will be the same

    
    #Gets x and y axis boundary data from the user
    for key in values.keys():
   #for each boundary value...
        while True:
            #keep looping until we get good data!
            try: newvalue = eval(raw_input("Please enter an integer for the " + key + ", \n\
type 'quit' to exit, or type 'ok' to use the default values of \n\
-10 (minimum x and minimum y) and 10 (maximum x and maximum y): \n"))
                #ask the user for an integer input
            except: #if the input is not a proper input, tell the user, and try again.
                print "\nThat is not a valid number. \n"
            else:
                if type(newvalue) != int and \
                   newvalue != ok and newvalue != 'quit' and \
                   newvalue != quit:
                #if the input was not a valid input we can use...
                    print "\nThat is not a valid number. \n"
                else: break #otherwise, get out of the loop.
            
        if newvalue == ok: #If the input was 'ok' or ok
            values = {"minimum value of the x axis": -10,
                      "maximum value of the x axis": 10,
                      "minimum value of the y axis": -10,
                      "maximum value of the y axis": 10}
                        #use the default values
            break #get out of the "each boundary value input" loop
        if newvalue == quit or newvalue == 'quit':
       #If the input was quit or 'quit':
            bye() #close the turtle window
            return #end the program
        values[key] = newvalue #Otherwise, save the inputted data in the dictionary
        
    #Takes the dictionary values and assigns them to variables
    min_x = values["minimum value of the x axis"]
    max_x = values["maximum value of the x axis"]
    min_y = values["minimum value of the y axis"]
    max_y = values["maximum value of the y axis"]

    print "\n Now drawing the axes...\n\
(See the Python Turtle Graphics Window) \n"
    x_axis, y_axis = axis_draw(min_x, max_x, min_y, max_y) #Draws the axes,
    #and returns the positions of the x and y axes
    
    screen = Screen()
    real_width = window_width() #Real window width
    real_height = window_height() #Real window height
    wide = max_x - min_x #Inputted x axis width
    height = max_y - min_y #Inputted y axis height
    x_step = ((wide) / 2.) / 100. # How far apart each x data point will be 
    number_of_x_values = int((wide) / x_step) #Number of x values that will be taken
    
    x = min_x #starting point of the x values
    xs = [x] #initializing the list of x values
    
    for num in range(number_of_x_values):
   #for each x value...
        x = round(x + x_step, 3) #the new x will be one step away from the previous x
        xs.append(x) #adds the new x to the list of x values
    while True:
        #Keep looping until we get a usable function!
        try:
            function = raw_input("Please input your function: ") #asks for the function
            eval(function) #Tries the function to see if it makes sense
        except: print "\nThat is not a valid function.\n" #If it's not a good function, tell the user
        else: break
    ys = [] #initialize the y values
    for x in xs:
   #for each x value...
        try:
            #try to run the function on it and add the result to the ys
            ys.append(eval(function))
        #If any of the following possible errors occur,
        #add the string "no value" to the list, which will
        #be processed later as place that will be skipped
        #on the graph.
        except ValueError:
            ys.append("no value")
        except ZeroDivisionError:
            ys.append("no value")
        except OverflowError:
            ys.append("no value")
    
    
    #makes the screen relative x values
    real_xs = [y_axis + ((x / (1. * wide)) * real_width) for x in xs]

    #makes the screen-relative y values
    real_ys = []
    for y in ys:
        if y == "no value":
        #if the y value doesn't exist
            real_ys.append(y)
            #make the real_y value also not exist
        else:
            real_y = x_axis + ((y / (1. * height)) * real_height) #convert the value
            if abs(real_y) > 1e+7: #if it is too big for the screen...
                real_ys.append("no value") #add "no value" instead
            else: real_ys.append(real_y)

    color("red") #Color of the function
    width(2) #Pixel thickness of the function
    print #make a new line for the next user input
    #Asks if the user would like integral rectangles to be drawn
    try: riemannDraw = eval(raw_input("Type 'True' if you would also like \n\
the integral rectangles to be drawn, or type 'False'\n\
(or anything that's not 'True') otherwise: ")) #Asks if the user wants to draw the integral rectangles
    except: riemannDraw = False #If the user inputs something non-True, then we won't draw it
    if riemannDraw == True or riemannDraw == 'True':
    #If the user inputted True..
        size = raw_input("\nWhat size should the rectangles be? \n\
Type 'small', 'medium', or 'large': ") #Ask for the size of the rectangles
    print "\n Now drawing the function...\n\
(See the Python Turtle Graphics Window) \n"
    penup()
    if real_ys[0] != "no value":
        setpos(real_xs[0], real_ys[0]) #Moves to the start position of the graph
    pendown()
    for num in range(len(real_ys)):
   #for each x/y value index...
        if real_ys[num] == "no value": #if the value doesn't exist
            penup() #don't draw it on the screen
        else:
            setpos(real_xs[num], real_ys[num]) #move the turtle to that position
            pendown()
    if riemannDraw == True or riemannDraw == 'True':
   #if the user says that he or she wants the rectangles to be drawn..
        riemann(real_xs, real_ys, x_axis, y_axis, size) #Draw 'em!
        
    #This line makes the screen big enough to display the axes:
    screen.setup(width=1000, height=700, startx=0, starty=0)

    #This line adds scroll bars to allow the user to see
    #to the end of the function (in case of large y values):
    screen.screensize(real_xs[-1], 2 * max([num for num in real_ys if num != "no value"]))

    print "\nGraphing completed!!\n"
    print "You may close your graph, and run\n\
grapher() in Python Shell to graph another function."
    
    screen.exitonclick() #closes the window if the screen is clicked on

    
def right_hand(x1, x2, y2, x_axis):
    '''Draws the right-hand rectangle approximation'''
    penup()
    setpos(x2, x_axis)
    pendown()
    fill(True) #turns fill on for drawing the rectangles
    setpos(x2, y2)
    setpos(x1, y2)
    setpos(x1, x_axis)


def left_hand(x1, y1, x2, x_axis):
    '''Draws the left-hand rectangle approximation'''
    penup()
    setpos(x1, x_axis)
    pendown()
    fill(True) #turns fill on for drawing the rectangles
    setpos(x1, y1)
    setpos(x2, y1)
    setpos(x2, x_axis)


def riemann(x_values, y_values, x_axis, y_axis, size):
    '''Draws the integral rectangles based on
        the given x and y values, the size of rectangles
        the user asks for, and the location
        of the x and y axes on the screen.'''
    color('orange') #color of the rectangles' edges
    fillcolor('green') #fill color
    width(1) #Pixel thickness of the rectangles' edges

    large = "large"
    medium = "medium"
    small = "small"
    size = eval(size)
    if size == "large":
        full = 2
    if size == "medium":
        full = 1
    if size == "small":
        full = 0

    #the variable "full" is the number of x values
    #wide that the rectangles will be.

    #the variable "counter" will be used to count when
    #that many x values have been iterated across.
    counter = full
    start = (x_values[0], y_values[0])
    for num in range(len(x_values)):
        if start[1] == "no value":
            counter = 0
            start = (x_values[num], y_values[num])
   #for each x/y value index...
        elif counter == full:
       #if a rectangle width has been passed through:
            if y_values[num] > x_axis and start[1] > x_axis:
           #if the function is positive if this region:
                if y_values[num] < start[1]:
               #If the current y value is less than the y-value 1 rectangle width ago
                    right_hand(start[0], x_values[num], y_values[num], x_axis)
                   #draw with the right hand approximation
                    counter = 0 #start the rectangle width counter over
                    start = (x_values[num], y_values[num])
                   #set the current position as the previous position for when
                   #the next rectangle width has been made
                else:
                    left_hand(start[0], start[1], x_values[num], x_axis)
                   #draw with the right hand approximation
                    counter = 0
                    start = (x_values[num], y_values[num])
            if y_values[num] < x_axis and start[1] < x_axis:
           #if the function is negative if this region:
                if y_values[num] > start[1]:
               #If the current y value is greater than the y-value 1 rectangle width ago
                    right_hand(start[0], x_values[num], y_values[num], x_axis)
                    #draw with the right hand approximation
                    counter = 0 #start the rectangle width counter over
                    start = (x_values[num], y_values[num])
                   #set the current position as the previous position for when
                   #the next rectangle width has been made
                else:
                    left_hand(start[0], start[1], x_values[num], x_axis)
                   #draw with the right hand approximation
                    counter = 0
                    start = (x_values[num], y_values[num])
            else:
           #If the function at this point is not the same sign as the function
           #1 rectangle width ago, or both are on the axis:
                counter = 0 #Start the counter over (skip the rectangle),
                #so that the rectangle does not cross the axis
                start = (x_values[num], y_values[num])
            fill(False) #Turn off fill, now that a rectangle has been drawn
        else: counter+=1 #If a rectangle width has not been made, add one to the counter.

        
#grapher()
#uncomment above line to start up grapher() upon running this turtleGrapher module

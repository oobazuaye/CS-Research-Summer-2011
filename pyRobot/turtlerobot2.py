from turtle import *
screen = Screen()
canvas = screen.getcanvas()
screen.register_shape("C:/Users/Obosa/Desktop/awesome.gif")

shape("turtle") #Sets the shape of the robot to be a turtle
turnAngle = 15 #The angle that the robot rotates clockwise or counterclockwise
stepDistance = 1 #How many pixels the robot moves with each step
threshold = 10 #How many pixels the robot needs to be from an object to "hit" it
running1 = False #Moving Forward
running2 = False #Moving Backward
running3 = False #Turning Clockwise or Counterclockwise
running4 = False #Moving Autonomously
#x = position()[0]
#y = position()[1]
height = window_height() - 30
width = window_width() - 30
x_origin = -width/2
y_origin = height/2
goal = (-x_origin, 0) #initializes the position of the goal

#map0: A rectangular border at the edges of the screen
map0 = [((x_origin, y_origin), (-x_origin, y_origin)),
          ((-x_origin, y_origin), (-x_origin, -y_origin)),
          ((-x_origin, -y_origin), (x_origin, -y_origin)),
          ((x_origin, -y_origin), (x_origin, y_origin))]

#map1: Same as map0, but with a square obstacle in the upper left
#       and a rectangular obstacle in the lower right
map1 = [((x_origin, y_origin), (-x_origin, y_origin)),
        ((-x_origin, y_origin), (-x_origin, -y_origin)),
        ((-x_origin, -y_origin), (x_origin, -y_origin)),
        ((x_origin, -y_origin), (x_origin, y_origin)),
        ((x_origin/2, y_origin/2), (x_origin/2 + 100, y_origin/2)),
        ((x_origin/2 + 100, y_origin/2), (x_origin/2 + 100, y_origin/2 - 100)),
        ((x_origin/2 + 100, y_origin/2 - 100), (x_origin/2, y_origin/2 - 100)),
        ((x_origin/2, y_origin/2 - 100), (x_origin/2, y_origin/2)),
        ((-x_origin/3.5, -y_origin/5), (-x_origin/3.5 + 150, -y_origin/5)),
        ((-x_origin/3.5 + 150, -y_origin/5), (-x_origin/3.5 + 150, -y_origin/5 - 50)),
        ((-x_origin/3.5 + 150, -y_origin/5 - 50), (-x_origin/3.5, -y_origin/5 - 50)),
        ((-x_origin/3.5, -y_origin/5 - 50), (-x_origin/3.5, -y_origin/5))]
'''
map1 = [((x_origin, y_origin), (-x_origin, y_origin)),
        ((-x_origin, y_origin), (-x_origin, -y_origin)),
        ((-x_origin, -y_origin), (x_origin, -y_origin)),
        ((x_origin, -y_origin), (x_origin, y_origin)),
        ((-200, 200), (-100, 200)),
        ((-100, 200), (-100, 100)),
        ((-100, 100), (-200, 100)),
        ((-200, 100), (-200, 200)),
        ((150, -150), (300, -150)),
        ((300, -150), (300, -200)),
        ((300, -200), (150, -200)),
        ((150, -200), (150, -150))]
'''

#map2: A rectangular border with a gap at the bottom for exit,
#      and a line obstacle near the middle
map2 = [((x_origin/2, y_origin), (-x_origin/2, y_origin)),
        ((-x_origin/2, y_origin), (-x_origin/2, -y_origin)),
        ((-x_origin/2, -y_origin), (0, -y_origin)),
        ((x_origin/2, -y_origin), (x_origin/2, y_origin)),
        ((x_origin/2, -y_origin/5), (0, -y_origin/5))]

our_map = map2 #Set our map!
ray = canvas.create_line(0, 0, 0, 0) #Initializes the ray
canvas.itemconfigure(ray, fill='red', width=3) #Sets how the ray looks

'''
speed("fastest")
penup()
hideturtle()
setpos(x_origin, y_origin)
pendown()
seth(0)
forward(width)
right(90)
forward(height)
right(90)
forward(width)
right(90)
forward(height)
penup()
home()
pendown()
showturtle()
hideturtle()
speed("fastest")
forward(ray)
setpos(x, y)
showturtle()
'''

def forwards():
    '''Moves the turtle forward until it hits a wall, reaches
        the goal, is set to move backward, or is otherwise commanded
        to halt.'''
    global running1
    global running2
    global goal
    running1 = True #Set forward movement to on
    running2 = False #Set backward movement to off
    while running1:
        forward(stepDistance) #Move the robot forward one step
        x = position()[0]
        y = position()[1]
        closechecker() #Checks if the robot has hit a wall
        good_rayer(x, y) #Project the ray 
        if x - threshold <= goal[0] <= x + threshold and \
           y - threshold <= goal[1] <= y + threshold:
       #If the robot has come within the collision threshold of the goal...
            stoprunning()
            print "You've reached the goal!!"
            break
        '''
        if x_origin + threshold >= x >= x_origin or \
           -x_origin >= x >= -x_origin - threshold or \
           y_origin - threshold <= y <= y_origin or \
           -y_origin <= y <= -y_origin + threshold:
            stoprunning()
            print "You've hit a wall!!"
            break
        '''
        
def backwards():
    '''Moves the turtle backward until it hits a wall, reaches
        the goal, is set to move forward, or is otherwise commanded
        to halt.'''
    global running1
    global running2
    global goal
    running1 = False #Set forward movement to off
    running2 = True #Set backward movement to on
    while running2:
        backward(stepDistance) #Move the robot backward one step
        x = position()[0]
        y = position()[1]
        closechecker() #Checks if the robot has hit a wall
        good_rayer(x, y) #Project the ray
        if x - threshold <= goal[0] <= x + threshold and \
           y - threshold <= goal[1] <= y + threshold:
       #If the robot has come within the collision threshold of the goal...
            stoprunning()
            print "You've reached the goal!!"
            break
        '''
        if x_origin + threshold >= x >= x_origin or \
           -x_origin >= x >= -x_origin - threshold or \
           y_origin - threshold <= y <= y_origin or \
           -y_origin <= y <= -y_origin + threshold:
            stoprunning()
            print "You've hit a wall!!"
            break
        '''

def counterclockwise():
    global running3
    running3 = True #Sets the robot to be turning
    '''Moves the robot counterclockwise by a predetermined angle.'''
    #speed("slowest")
    left(turnAngle)
    #lame_rayer()
    
def clockwise():
    global running3
    running3 = True #Sets the robot to be turning
    '''Moves the robot clockwise by a predetermined angle.'''
    #speed("slowest")
    right(turnAngle)
    #lame_rayer()
    
def closewindow():
    '''Stops everything from running, and cleanly closes the window.'''
    stoprunning()
    ontimer(bye, 100)

def lame_rayer():
    #This is lame. So we'll use good_rayer.
    '''Draws a ray from the robot to the
    closest point on the closest wall
    for a split second.'''
    showturtle()
    x = position()[0]
    y = position()[1]
    closest_wall = closechecker()
    print "The closest wall is", round(closest_wall[0], 2), "away."
    speed("fastest")
    good_stamp = stamp()
    hideturtle()
    setpos(closest_wall[1])
    setpos(x, y)
    showturtle()
    for num in range(6): undo()
    clearstamp(good_stamp)
    pendown()

def good_rayer(x, y):
    '''Projects a ray from the robot
    to the closest point on the closest wall'''
    global ray
    closest_wall = closechecker()
    close_x = closest_wall[1][0]
    close_y = closest_wall[1][1]
    canvas.coords(ray, x, -y, close_x, -close_y)
    # Changes the ray line to extend from the old
    # position to the new coordinates
    
"""
def restart():
    '''Resets the environment.'''
    global goal
    reset()
    shape("turtle")
    color("green")
    turnAngle = 15
    stepDistance = 1
    threshold = 10
    stoprunning()
    height = window_height() - 30
    width = window_width() - 30
    x_origin = -width/2
    y_origin = height/2
    goal = (-x_origin, 0)
    speed("fastest")
    penup()
    hideturtle()
    setpos(x_origin, y_origin)
    pendown()
    seth(0)
    color("blue")
    forward(width)
    right(90)
    forward(height)
    right(90)
    forward(width)
    right(90)
    forward(height)
    penup()
    color("green")
    home()
    pendown()
    showturtle()
"""

def restart():
    '''Resets the environment'''
    stoprunning() #Stops all movement
    reset() #Clears everything on the screen
    color("blue")
    hideturtle()
    speed("fastest")
    penup()
    for line_segment in our_map:
   #Draws the map on the screen
        start = line_segment[0]
        end = line_segment[1]
        setpos(start)
        pendown()
        setpos(end)
        penup()
    home() #Moves the turtle to the center
    showturtle()
    pendown()
    color("green")

def edgechecker(line_segment):
    '''Returns the point on the given line segment
    that is closest to the robot'''
    start = line_segment[0]
    end = line_segment[1]
    x = position()[0]
    y = position()[1]
    
    if start[0] == end[0]:
   #if the line is vertical...
        if start[1] < end[1]:
       #if the line's start point is below the end point...
            if y > end[1] or y < start[1]:
           #if the robot is past the start or end point...
                if distance(end) < distance(start):
               #if the robot is closer to the end point than the start point...
                    close_point = end
                else:
               #if the robot is closer to the start point than the end point...
                    close_point = start
            else:
           #if the robot is between the start point and the end point...
                close_point = (start[0], y)
        else:
       #if the line's end point is below the start point...
            if y < end[1] or y > start[1]:
           #if the robot is past the start or end point...
                if distance(end) < distance(start):
               #if the robot is closer to the end point than the start point...
                    close_point = end
                else:
               #if the robot is closer to the start point than the end point...
                    close_point = start
            else:
           #if the robot is between the start point and the end point...
                close_point = (start[0], y)
        
    if start[1] == end[1]:
   #if the line is horizontal...
        if start[0] < end[0]:
       #if the line's start point is to the left of the end point...
            if x > end[0] or x < start[0]:
           #if the robot is past the start or end point...
                if distance(end) < distance(start):
               #if the robot is closer to the end point than the start point...
                    close_point = end
                else:
               #if the robot is closer to the start point than the end point...
                    close_point = start
            else:
           #if the robot is between the start point and the end point...
                close_point = (x, start[1])
        else:
       #if the line's start point is to the right of the end point...
            if x < end[0] or x > start[0]:
            #if the robot is past the start or end point...
                if distance(end) < distance(start):
               #if the robot is closer to the end point than the start point...
                    close_point = end
                else:
               #if the robot is closer to the start point than the end point...
                    close_point = start
            else:
           #if the robot is between the start point and the end point...
                close_point = (x, start[1])
                
    return close_point
            
def closechecker():
    '''Returns the closest point on the wall closest to the turtle,
    and checks if the turtle has made contact with a wall.'''
    closest_distance = 1e308 #Sets the closest distance to be infintely far away
    closest_point = (1e308, 1e308) #Sets the closest point to be...really far away
    for line_segment in our_map:
   #For each line in the map...
        close_point = edgechecker(line_segment) #Find the closest point
        close_distance = distance(close_point)
        if close_distance < closest_distance: #Finds the closest point in the map
            closest_distance = close_distance
            closest_point = close_point
    closest_wall = [closest_distance, closest_point]
    if closest_distance <= threshold:
   #If the closest point is within our collision threshold...
            stoprunning()
            print "You've hit a wall!!"
    return closest_wall
    
def stoprunning():
    '''Sets all of the robots movement booleans
    to false, effectively halting the robot's movement.'''
    global running1 #Forward movement
    global running2 #Backward movement
    global running3 #Rotational movement
    global running4 #Autonomous movement
    running1 = False
    running2 = False
    running3 = False
    running4 = False
    print "You are currently at", position()
    
def autonomous():
    '''Runs the robot autonomously.
    (For now, it just moves the robot on
    the straightest path toward the goal)'''
    global goal
    global running3
    global running4
    stoprunning() #Stops the robot's manual movement
    running4 = True #Sets the robot to be in autonomous mode
    while running4:
   #While still in autonomous mode...
        seth(towards(goal)) #Set the robot to face the goal
        forward(stepDistance) #Move it forward one step
        x = position()[0]
        y = position()[1]
        good_rayer(x, y)
        if running1 or running2 or running3:
       #If the user moves the robot manually...
            running4 = False #Switch off autonomous mode
            if running3:
           #If the user turns the robot clockwise or counterclockwise...
                forwards() #Continue the robot moving forward
            break
        closechecker() #Check if the robot has hit any walls
        if x - threshold <= goal[0] <= x + threshold and \
           y - threshold <= goal[1] <= y + threshold:
       #If the robot has come within the collision threshold of the goal...
            stoprunning() #Stop the robot.
            print "You've reached the goal!!"
            break
        '''
        if x_origin + threshold >= x >= x_origin or \
           -x_origin >= x >= -x_origin - threshold or \
           y_origin - threshold <= y <= y_origin or \
           -y_origin <= y <= -y_origin + threshold:
            stoprunning()
            print "You've hit a wall!!"
            break
        '''
        
def mouseHandler(mouse_x, mouse_y):
    '''Sets the goal to be at the location
    of the mouse click'''
    global goal
    clearstamps()
    oldpos = position()
    me = stamp()
    hideturtle()
    #shape("circle")
    shape("C:/Users/Obosa/Desktop/awesome.gif")
    goal = (mouse_x, mouse_y) #Sets the new goal to be at the mouse click
    penup()
    speed("fastest")
    showturtle()
    setpos(mouse_x, mouse_y)
    color("red")
    stamp()
    hideturtle()
    shape("turtle")
    color("green")
    setpos(oldpos[0], oldpos[1])
    showturtle()
    clearstamp(me)
    pendown()
    #(((goal[0] - oldpos[0])**2 + (goal[1] - oldpos[1])**2)**0.5), 2
    dist = round(distance(goal), 2) #Calculates the distance to the new goal
    print "The goal is now at", goal,". \n You are at", oldpos, \
          ", a distance of", dist,"away."

restart()
screen.onkey(forwards, "w")
screen.onkey(backwards, "s")
screen.onkey(counterclockwise, "a")
screen.onkey(clockwise, "d")
screen.onkey(stoprunning, "e")
screen.onkey(closewindow, "q")
screen.onkey(autonomous, "f")
screen.onkey(restart, "r")
screen.onkey(lame_rayer, "2")
screen.onclick(mouseHandler)
screen.listen()

done()

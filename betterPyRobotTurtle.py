from turtle import *
from math import * 
from intersections import *
from Tkinter import *
import random
screen = Screen()
canvas = screen.getcanvas()
import time

turnAngle = 15 #The angle that the robot rotates clockwise or counterclockwise
stepDistance = 1 #How many pixels the robot moves with each step
threshold = 10 #How many pixels the robot needs to be from an object to "hit" it
trail = True #Trail on or off
flashing = True #Turn flashing on or off
map_lines = []
state_list = ['KBD', 'GO_TIL_BUMP', 'AUTO', 'STOP', 'GO'] #States that can be used
state = 'STOP' #Starting state

range_angles = [0, 45, 90, 135, 180, 225, 270, 315] #Angles of the range sensors

#list containing the range sensors:
ray_list = [canvas.create_line(0, 0, 0, 0) for angle in range_angles]
color_list = [] #List containing colors of the range angles

updates = {} #Dictionary containing the robot's information
height = window_height() - 30
width = window_width() - 30
x_origin = -width/2
y_origin = height/2

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

#map2: A rectangular border with a gap at the bottom for exit,
#      and a line obstacle near the middle
map2 = [((x_origin/2, y_origin), (-x_origin/2, y_origin)),
        ((-x_origin/2, y_origin), (-x_origin/2, -y_origin)),
        ((-x_origin/2, -y_origin), (0, -y_origin)),
        ((x_origin/2, -y_origin), (x_origin/2, y_origin)),
        ((x_origin/2, -y_origin/5), (0, -y_origin/5))]

goal = (-x_origin - 50, 0) #initializes the position of the goal
picnum = 1
pic = PhotoImage(file = "alien.gif")
goaldot = canvas.create_image(goal[0], -goal[1], image = pic)
our_map = map2 #Set our map!

def stateChange(newState):
    '''Changes the current state to the inputted state'''
    global state
    state = newState

def changePic():
    '''Changes the goal's image'''
    global pic
    global picnum
    global goaldot
    canvas.delete(goaldot)
    if picnum == 1:
        pic = PhotoImage(file = "awesome.gif")
        picnum = 2
    elif picnum == 2:
        pic = PhotoImage(file = "panda.gif")
        picnum = 3
    elif picnum == 3:
        pic = PhotoImage(file = "firefox.gif")
        picnum = 4
    else:
        pic = PhotoImage(file = "alien.gif")
        picnum = 1
    goaldot = canvas.create_image(goal[0], -goal[1], image = pic)

def changeRange(angle_list):
    '''Changes the range sensor angles to the angles
        given in the inputted angle_list'''
    global range_angles
    if type(angle_list) == list:
        range_angles = angle_list
    else: print 'Please provide a list as input.'

def changeMap():
    '''Changes the current map'''
    global our_map
    if our_map == map0:
        our_map = map1
        print "Current map is map1"
    elif our_map == map1:
        our_map = map2
        print "Current map is map2"
    else:
        our_map = map0
        print "Current map is map0"
    restart()

def KBD_state():
    '''Sets the state to "KBD"'''
    stateChange('KBD')
    
def go(dist, ang):
    '''Sets the stepDistance and turnAngle global variables'''
    global stepDistance
    global turnAngle
    stepDistance = dist
    turnAngle = ang

def Up():
    '''Moves the turtle forward'''
    global state
    state = 'KBD'
    update()
    while state == 'KBD':
        setVel(50, 0)

def Left():
    '''Rotates the turtle counterclockwise'''
    global state
    state = 'KBD'
    update()
    setVel(0, 100)
    update()

def Right():
    '''Rotates the turtle clockwise'''
    global state
    state = 'KBD'
    update()
    setVel(0, -100)
    update()

def Down():
    '''Moves the turtle backward'''
    global state
    state = 'KBD'
    update()
    while state == 'KBD':
        setVel(-50, 0)

def setVel(trans_vel, ang_vel):
    '''Takes velocities as input, and uses change in time
        to calculate the distance that should be traveled'''
    update()
    go(trans_vel * updates["time change"], ang_vel * updates["time change"])
    update()

def angler():
    '''Prints the angles of incidence between the
        rangefinder rays and the walls'''
    incidence_angles = []
    for angle in range_angles:
   #for each rangefinder ray...
        intersection = best_rayer(angle,
                    ray_list[range_angles.index(angle)])
       #Find the intersection between it and the wall it hits
        angleVertex = intersection[0]
        if intersection[1] == 0:
            incident = "nonexistent; this ray does not hit a wall"
        else:
            pointA = intersection[1][0]
            pointB = position()
            if distancer(pointA, angleVertex) <= 1:
                incident = 45
            else:
                #Use math to find the angle of incidence!
                incident = lawOfCosines(pointA, pointB, angleVertex)
            if incident > 90: incident = 180 - incident
        if type(incident) == float: incident = round(incident, 2)
        incidence_angles.append(incident)
    return incidence_angles

def distancer(point1, point2):
    '''Returns the absolute distance between two points'''
    return hypot(point2[0] - point1[0], point2[1] - point1[1])

def lawOfCosines(pointA, pointB, angleVertex):
    '''Finds the angle in front of the angleVertex point'''
    a = distancer(angleVertex, pointA)
    b = distancer(pointB, angleVertex)
    c = distancer(pointA, pointB)
    return degrees(acos(-(c**2 - a**2 - b**2) / (2 * a * b)))

def printAnglerData():
    '''Prints the angles of incidence calculated by the angler'''
    incidence_angles = angler()
    print "Your heading is", heading()
    for angle in range(len(incidence_angles)):
        print "The angle of incidence for ray #", angle, \
        "is", incidence_angles[angle]

def update():
    '''Stores all of the information concerning the turtle,
        and moves it correspondingly.'''
    global updates
    global goal
    #updates["rays"] = ray_list
    #forward(stepDistance)
    #right(turnAngle)
    multi_rayer()
    closechecker()
    goalchecker()
    updates["ray angles"] = range_angles
    updates["position"] = position()
    updates["heading"] = heading()
    updates["goal"] = goal
    updates["closest wall"] = closechecker()
    updates["intersecting angles"] = angler()
    updates["intersecting points"] = \
    [best_rayer(range_angles[index], ray_list[index])[0] for index \
     in range(len(range_angles))]
    updates["time change"] = abs(time.time() - updates["current time"])
    updates["current time"] = time.time()
    previousState = updates["state"]
    updates["state"] = state
    setpos(xcor() + stepDistance*cos(radians(heading())),
           ycor() + stepDistance*sin(radians(heading())))
    setheading(heading() + turnAngle)
    #for a, b in updates.iteritems(): print a,":", b, "\n"
    if previousState != updates["state"]:
        print "The current state is now:", updates["state"]
    return updates

def updatePrinter():
    '''Prints all the information in the update dictionary'''
    for a, b in updates.iteritems(): print a,":", b, "\n"
    
def best_rayer(angle, ray):
    '''Projects a rangefinder ray from the robot to the wall
        that it hits'''
    best_intersect = (10000, 10000)
    pt1 = position()
    pt2 = (xcor() + 10000*cos(radians(angle + heading())),
           ycor() + 10000*sin(radians(angle + heading())))
    goodline = 0
    for line in our_map:
        ptA = line[0]
        ptB = line[1]
        intersect = intersectLines(pt1, pt2, ptA, ptB)
        point = (intersect[0], intersect[1])
        if intersect != (0, 0, 0, 0, 0) and \
           in_line3(point, pt1, pt2) and \
           in_line3(point, ptA, ptB):
            if distance(point) < distance(best_intersect):
                best_intersect = point
                goodline = line
    if best_intersect == (10000, 10000):
        canvas.coords(ray, xcor(), -ycor(), pt2[0], -pt2[1])
    else:
        canvas.coords(ray, xcor(), -ycor(), best_intersect[0], -best_intersect[1])
    return (best_intersect, goodline)

def multi_rayer():
    '''Projects multiple rays, stored in ray_list, using
        best_rayer'''
    global flashing
    global color_list
    color_list = []
    for index in range(len(range_angles)):
        angle = range_angles[index]
        ray = ray_list[index]
        if flashing == True:
            color_choice = random_color()
            while color_choice in color_list:
                color_choice = random_color()
            color_list.append(color_choice)
            canvas.itemconfigure(ray_list[index], fill = color_choice, width = 3)
        best_rayer(angle, ray)    


def autonomous():
    '''Runs the robot autonomously.
    (For now, it just moves the robot on
    the straightest path toward the goal)'''
    global goal
    global state
    if state == 'AUTO':
        return
    state = 'AUTO'
    update()
    setVel(100, 0)
    while state == 'AUTO':
   #While still in autonomous mode...
        seth(towards(goal)) #Set the robot to face the goal
        update()

def mouseHandler(mouse_x, mouse_y):
    '''Sets the goal to be at the location
    of the mouse click'''
    global goal
    global trail
    global goaldot
    clearstamps()
    goal = (mouse_x, mouse_y) #Sets the new goal to be at the mouse click
    canvas.delete(goaldot)
    goaldot = canvas.create_image(goal[0], -goal[1], image = pic)
    dist = round(distance(goal), 2) #Calculates the distance to the new goal
    print "The goal is now at", goal,". \n You are at", position(), \
          ", a distance of", dist,"away."

def stoprunning():
    '''Sets all of the robots movement booleans
    to false, effectively halting the robot's movement.'''
    global state
    state = 'STOP'
    go(0, 0)
    
def restart():
    '''Resets the environment'''
    global goal
    global goaldot
    global trail
    global color_list
    global updates
    global map_lines
    stoprunning() #Stops all movement
    reset() #Clears everything on the screen
    shape("turtle") #Sets the shape of the robot to be a turtle
    color("green") #Sets the color of the robot to be green
    speed("fastest") #Sets the turtle's movements to be instantaneous
    canvas.delete(goaldot) #Delete the goal from the screen
    
    #Delete the map:
    for index in range(len(map_lines)): canvas.delete(map_lines[index])
    
    #Delete the range-finder rays from the screen:
    for index in range(len(ray_list)): canvas.delete(ray_list[index])
    
    goal = (-x_origin - 50, 0) #initializes the position of the goal
    goaldot = canvas.create_image(goal[0], -goal[1], image = pic) #Draw the goal
    color_list = [] #empties the color list
    for index in range(len(ray_list)): #Draws the range angles
        ray_list[index] = canvas.create_line(0, 0, 0, 0)
        color_choice = random_color()
        while color_choice in color_list:
            color_choice = random_color()
        color_list.append(color_choice)
    for line_segment in our_map:
   #Draws the map on the screen
        start = line_segment[0]
        end = line_segment[1]
        x1 = start[0]
        y1 = start[1]
        x2 = end[0]
        y2 = end[1]
        map_lines.append(canvas.create_line(x1, -y1, x2, -y2, fill = 'blue'))
    updates["ray angles"] = range_angles
    updates["goal"] = "None"
    updates["position"] = (0.00,0.00)
    updates["closest wall"] = closechecker()
    updates["intersecting angles"] = "None"
    updates["intersecting points"] = "None"
    updates["current time"] = time.time()
    updates["time change"] = 0
    updates["state"] = state
    trail = True

def edgechecker(line_segment):
    '''Returns the point on the given line segment
    that is closest to the robot'''
    start = line_segment[0]
    end = line_segment[1]
    x = xcor()
    y = ycor()
    
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
    global goal
    closest_distance = 1e308 #Sets the closest distance to be infintely far away
    closest_point = (1e308, 1e308) #Sets the closest point to be...really far away
    for line_segment in our_map:
   #For each line in the map...
        close_point = edgechecker(line_segment) #Find the closest point
        close_distance = distance(close_point)
        if close_distance < closest_distance: #Finds the closest point in the map
            closest_distance = close_distance
            closest_point = close_point
    closest_wall = closest_point
    closest_distance = distance(closest_wall)
    if closest_distance <= threshold:
   #If the closest point is within our collision threshold...
            stoprunning()
            print "You've hit a wall!!"
    return closest_wall

def goalchecker():
    '''Checks if the robot has reached the goal'''
    if xcor() - threshold - 5 <= goal[0] <= xcor() + threshold + 5 and \
           ycor() - threshold - 5 <= goal[1] <= ycor() + threshold + 5:
        stoprunning()
        print "You've reached the goal!!!"
        
def closewindow():
    '''Stops everything from running, and cleanly closes the window.'''
    stoprunning()
    ontimer(bye, 500)
    
def flash_toggle():
    '''Toggles the flashing rangefinder rays on or off'''
    global flashing
    if flashing == True:
        print "Flashing off."
        flashing = False
    else:
        print "Flashing on."
        flashing = True


def random_color():
    '''Picks a random color'''
    colors = []
    for num in range(3):
   #For the 3 RGB values...
        colors.append(random.choice(range(256)))
        #...pick a random number between 0 and 256
    rgb = (colors[0], colors[1], colors[2])
    return random.choice(['#%02x%02x%02x' % rgb, '#%02x%02x%02x' % rgb,
                          '#%02x%02x%02x' % rgb, '#%02x%02x%02x' % rgb,
                          '#%02x%02x%02x' % rgb, 'red',
                          'orange', 'yellow', 'green',
                          'blue', 'violet', 'pink',
                          'black', 'brown', 'gray'])

def trail_toggle():
    '''Toggles the robot's trail on or off'''
    global trail
    if trail == True:
        print "Trail off."
        penup()
        trail = False
    else:
        print "Trail on."
        pendown()
        trail = True

restart()
screen.onkey(stoprunning, "1")
screen.onkey(closewindow, "2")
screen.onkey(autonomous, "3")
screen.onkey(restart, "4")
screen.onkey(trail_toggle, "5")
screen.onkey(flash_toggle, "6")
screen.onkey(changePic, "7")
screen.onkey(changeMap, "8")
screen.onkey(Up, "Up")
screen.onkey(Down, "Down")
screen.onkey(Left, "Left")
screen.onkey(Right, "Right")
screen.onkey(KBD_state, ' a ')
screen.onkey(KBD_state, ' b ')
screen.onkey(KBD_state, ' c ')
screen.onkey(KBD_state, ' d ')
screen.onkey(KBD_state, ' e ')
screen.onkey(KBD_state, ' f ')
screen.onkey(KBD_state, ' g ')
screen.onkey(KBD_state, ' h ')
screen.onkey(KBD_state, ' i ')
screen.onkey(KBD_state, ' j ')
screen.onkey(KBD_state, ' k ')
screen.onkey(KBD_state, ' l ')
screen.onkey(KBD_state, ' m ')
screen.onkey(KBD_state, ' n ')
screen.onkey(KBD_state, ' o ')
screen.onkey(KBD_state, ' p ')
screen.onkey(KBD_state, ' q ')
screen.onkey(KBD_state, ' r ')
screen.onkey(KBD_state, ' s ')
screen.onkey(KBD_state, ' t ')
screen.onkey(KBD_state, ' u ')
screen.onkey(KBD_state, ' v ')
screen.onkey(KBD_state, ' w ')
screen.onkey(KBD_state, ' x ')
screen.onkey(KBD_state, ' y ')
screen.onkey(KBD_state, ' z ')
screen.onkey(KBD_state, ' A ')
screen.onkey(KBD_state, ' B ')
screen.onkey(KBD_state, ' C ')
screen.onkey(KBD_state, ' D ')
screen.onkey(KBD_state, ' E ')
screen.onkey(KBD_state, ' F ')
screen.onkey(KBD_state, ' G ')
screen.onkey(KBD_state, ' H ')
screen.onkey(KBD_state, ' I ')
screen.onkey(KBD_state, ' J ')
screen.onkey(KBD_state, ' K ')
screen.onkey(KBD_state, ' L ')
screen.onkey(KBD_state, ' M ')
screen.onkey(KBD_state, ' N ')
screen.onkey(KBD_state, ' O ')
screen.onkey(KBD_state, ' P ')
screen.onkey(KBD_state, ' Q ')
screen.onkey(KBD_state, ' R ')
screen.onkey(KBD_state, ' S ')
screen.onkey(KBD_state, ' T ')
screen.onkey(KBD_state, ' U ')
screen.onkey(KBD_state, ' V ')
screen.onkey(KBD_state, ' W ')
screen.onkey(KBD_state, ' X ')
screen.onkey(KBD_state, ' Y ')
screen.onkey(KBD_state, ' Z ')
screen.onclick(mouseHandler)

screen.listen()

print "Welcome to pyRobot! \n"
print "Click on a point on-screen to place the goal for the robot. \n"
print "Press 'Up Arrow' to make the turtle move forward. \n"
print "Press 'Down Arrow' to make the turtle move backward. \n"
print "Press 'Left Arrow' to make the turtle turn counterclockwise. \n"
print "Press 'Right Arrow' to make the turtle turn clockwise. \n"
print "Press '1' to make the turtle stop moving. \n"
print "Press '2' to quit and close the window. \n"
print "Press '3' to set the turtle running autonomously. \n"
print "Press '4' to reset the turtle and the objects on screen. \n"
print "Press '5' to toggle trailing lines on or off. \n"
print "Press '6' to toggle flashing rays on or off. \n"
print "Press '7' to change the image used as the goal. \n"
print "Press '8' to change the current map. \n"
print "Good luck!"

#done()
#if you want to run the pyRobot from here rather than from another
#module that imports this file, then uncomment the
#'done()" line 3 lines above.

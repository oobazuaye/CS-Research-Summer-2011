from betterPyRobotTurtle import * #Imports the pyRobot module

#Name(s):



#Welcome to pyRobot, intrepid CS 5 student(s)!


##########################
######## CONTROLS ########
##########################
#Press F5 to run the module.
#Click on a point on-screen to place the goal for the robot.
#Press 'Up Arrow' to make the turtle move forward.
#Press 'Down Arrow' to make the turtle move backward.
#Press 'Left Arrow' to make the turtle turn counterclockwise.
#Press 'Right Arrow' to make the turtle turn clockwise.
#Press '1' to make the turtle stop moving.
#Press '2' to quit and close the window.
#Press '3' to set the turtle running autonomously.
#Press '4' to reset the turtle and the objects on screen.
#Press '5' to toggle trailing lines on or off.
#Press '6' to toggle flashing rays on or off.
#Press '7' to change the image used as the goal.
#Press '8' to change the current map.
#Press '9' to run the basic 'curve-and-bounce' state machine
#Press '0' to run the basic 'move-near-wall-and-print-data' state machine
#Good luck!


##########################
######### STATES #########
##########################

#The current states available are:
#   'KBD', 'GO_TIL_BUMP', 'AUTO', 'STOP', and 'GO'

###### 'KBD' is Keyboard/manual control.
#   Activated by pressing any letter or
#   direction/arrow key on the keyboard.

###### 'GO_TIL_BUMP' is the curve-and-bounce state machine.
#   Activated by the function runner(), seen below.
#   runner() is currently called by pressing the number '9',
#   but this can be changed at the bottom of the file.

###### 'AUTO' is the autonomous state machine
# that moves the robot directly toward the goal.
#   Activated by the function autonomous().
#   autonomous() is called by pressing the number '3'.

###### 'STOP' is the state in which the robot is halted in place.
#   Activated by the function stoprunning().
#   stoprunning() is called by pressing the number '1'.

###### 'GO' is the state machine in which the robot moves forward,
# and upon reaching a certain distance from a wall,
# it prints out all of its current data.
#   Activated by the function goto(), seen below.
#   goto() is currently called by pressing the number '0',
#   but this can be changed at the bottom of the file.

#Feel free to create your own states and state machine functions.


###########################
######## FUNCTIONS ########
########    AND    ########
######## VARIABLES ########
###########################

#### setVel(translational_velocity, angular velocity) ####

#Sets the velocity of the robot.
#Positive numbers move the robot forward (translational) 
# and rotate it counterclockwise (angular).
#Negative numbers move the robot backward (translational)
# and rotate it clockwise (angular).
#Using zero halts the robot (translational)
# and makes it move in a straight line (angular).
#Using a translational velocity that is too high (say, > 150)
# may cause the robot to pass through walls.


#### updates = update() ####

#Updates the robot's information dictionary, position, and range sensors.
#Information available in this dictionary, named 'updates', include:
# updates["ray angles"] == List of the angles of the range sensors
# updates["position"] == The robot's current coordinates, as an ordered pair
# updates["heading"] ==
#    The angle of the robot's current direction/heading, as a floating-point number
# updates["goal"] == The goal's current coordinates, as an ordered pair
# updates["closest wall"] ==
#    The coordinates of the closest point on the closest wall, as an ordered pair
# updates["intersecting angles"] ==
#   List of the angles of incidence between the range sensors
#   and the walls they come in contact with.
# updates["intersecting points"] ==
#   Points of intersection between each range sensor and the walls they hit
# updates["time change"] == time transpired between the last call to update()
# updates["current time"] = current time
# updates["state"] = current state


#### stateChange(newState) ####

#Changes the current state to newState.
#Using "state = newState" in your functions will not work.


#### seth(angle) or setheading(angle) ####

#sets the heading (direction) of the robot to angle.
#0 (or any multiple of 360) is right.
#90, -270 or any equivalent angle is up.
#180 (or any multiple of 180) is left.
#270, -90, or any equivalent angle is down.


#### distance(point) ####
#calculates the distance from the robot to the inputted point


#### distancer(point1, point2) ####
#calculates the distance from point1 to point2


#### updatePrinter() ####
#Prints all the information in the update dictionary


#### printAnglerData() ####
#Prints all of the angles of incidence of the range sensors


#### restart() ####
#Resets the environment (you probably won't need to use this
#in your code...)


#### towards(point) ####
#Finds the angle between the robot and the given point.
# (Useful for directing the robot toward the goal, when
# used in conjunction with setheading(angle)...that is,
# you can use setheading(towards(updates['goal'])).)


#### threshold ####
#the variable 'threshold' represents how far away the robot must be
# from an object to be considered in contact with it.
# It is set to 10. That is, the robot must be
# at least 10 pixels away from a wall or object to be considered in contact.
# You cannot change the threshold.


#### changeRange(list_of_angles) ####
# takes a list of angles as input,
# and changes the range sensor angles
# to be the ones provided in the list.


### TO run for a certain amount of time:
# set updates['current time'] + time (in seconds) for which
# you would like to run as an arbitrary variable.
#use a while loop: while updates['current time'] <= arbitrary variable
# for example:
#runtime = updates['current time'] + 3.5
#while updates['current time'] <= runtime:
#   updates = update()
#   setVel(35, 35)

########################
### edit code below: ###
########################

def runner():
    '''Makes the robot move forward while slowly rotating,
        and upon reaching a certain distance from a wall,
        it turns around 180 degrees and continues moving
        (bouncing around in arcs)'''
    stateChange('GO_TIL_BUMP')
    updates = update()
    while updates["state"] == 'GO_TIL_BUMP':
        updates = update()
        setVel(100, 45)
        if distance(updates["closest wall"]) <= threshold + 10:
            seth(heading() + 180)

def goto():
    '''Slowly moves the turtle forward, and upon
        reaching a certain distance from a wall,
        it prints out all of its current data.'''
    stateChange('GO')
    updates = update()
    while updates["state"] == 'GO':
        updates = update()
        setVel(30, 0)
        if distance(updates["closest wall"]) <= threshold + 20:
            print "I'm done!"
            updatePrinter()
            stoprunning()
            update()


screen.onkey(runner, "9")
screen.onkey(goto, "0")
#screen.onkey(yourfunctionname, "space")
#uncomment the above line, and replace "yourfunctionname" with
#the name of your function to assign the Spacebar to run your
#pyRobot state machine.
#Feel free to use the above syntax to assign other functions
#to keys. However, keep in mind:
#    The function must take no input.
#    The function should use a key not already already assigned.
#    Thus, no keyboard letters, and no numbers 0 through 9.
#    However, symbols, the function keys (f1, f2, etc.),
#    "Escape", and "Return" are okay.

done() #Keep this line in at the end of the file!
#It sets everything running.

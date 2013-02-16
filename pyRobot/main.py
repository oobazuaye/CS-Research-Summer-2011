#
# main.py
#

import RobotCanvas
import Tkinter
import time
import threading
import random
import Queue
import math
import sys
from roombaSim import *
from turtle import *
screen = Screen()
    



def statePrint( robotTask ):
    """ a small function to print the state to which
        we are transitioning...
        input: robotTask, the state number, used as
            an index into a list of state names
    """
    # You'll need to update this list, as you add states!
    stateName = [ "STOP", "KBD", "TURN", "GO", "WANDER", "GOFOR" ]
    print "State is", stateName[robotTask]
    
        
class Robot(ThreadedClient):
    """
    A class defining the graphical display and the behavior of
    a Roomba-like robot (except that it has a range sensor!)
    """
    def f():
        self.setVels(FV,0,noise)
        #screen.ontimer(f, t=500)

    def b():
        self.setVels(-FV,0,noise)
        #screen.ontimer(b, t=500)
        
    def e():
        robotTask = STOP
        print position()

    def q():
        global running1
        global running2
        running1 = False
        running2 = False
        bye()
        
    def l():
        self.setVels(FV,RV,noise)

    def r():
        self.setVels(FV,-RV,noise)
        def __init__(self, mapname):
            """
            This constructor delegates a couple graphics-specific things
            to the ThreadedClient class
            """
            self.mapname = mapname
            ThreadedClient.__init__(self, mapname)
            
        
    def simulator(self):
        """
        This function gets called by the graphics.
        The while loop is, in essence, the life of the robot.
        Each time through the loop, you will want to 
           * read the sensors
           * decide on what action to take (if any)
           * execute the current action
        Then, it all begins again!
        """
        # pause for a second to let the graphics initialize
        time.sleep(1)

        # these constants are the robot's translational
        # and rotational velocities...
        FORWARD_VELOCITY = 50.0   # about 50.0 cm/sec is the max
        FV = FORWARD_VELOCITY     
        ROTATIONAL_VELOCITY = 45.0    # about 45.0 deg/sec
        RV = ROTATIONAL_VELOCITY
        
        # these constants represent different tasks
        # the robot might be currently performing
        STOP = 0
        KBD = 1
        TURN = 2
        GO = 3
        WANDER = 4
        GOFOR = 5

        # important values
        robotTask = KBD      # this is the robot's current state
        noise = 0.0          # the noise in the velocities 
        RADIUS = 16          # the roomba's radius in cm
        
        # Note on the "noisy roomba" ...
        # see at the bottom of the file
        segList = self.getMap()
        counter = 0
        for s in segList:
            print 'segment #', counter, 'is (', s.x1, ',', s.y1, ') - (', s.x2, ',', s.y2, ')'
            counter += 1
        # although printing the above list is just for show, keep in mind that
        # the variable segList is now accessible and holds a list of all of
        # the obstacles in the world (each a segment)

        print """\n\nHold down 'g' and click to set a goal (a green dot).
You may need to move the window a bit first!
In order to start autonomous mode, hit 's'
"""
        
        rangeHeading = 0.0   # where to point our range finder
        
        oldgoal = (0,0)      # the old goal
        goal = (0,0)         # the current goal
        
        while True:          # run until you hit 'Q' in the window 
                             # or control-c at the command prompt

            #
            # Reading our sensors
            #
            
            # x is the x coordinate of the robot
            # y is the y coordinate of the robot
            # thd is the robot's heading, theta, in degrees
            # bump is a list of two bump sensor readings: left and right
            [x,y,thd], bump = self.getData()
            #
            # get the range to the walls at a particular heading
            d = self.getRange(rangeHeading)   # in degrees
            #
            # thr is the robot's heading, theta, in radians
            thr = math.radians(thd)       # nice of python to have this function
            #
            # get any keypresses and goal locations (mouse clicks)
            #
            kbd, goal = self.getWindowEvents()  # at start, kbd == '' and goal == (0,0)
            if goal != oldgoal: 
                # a new goal has been clicked - let's confirm this on the screen             
                print 'New goal at x =', goal[0], 'and y =', goal[1]
                self.showGoal( goal )           # displays the goal in green
                oldgoal = goal                  # reset the old goal
          
            # have we gotten to the goal - check if we're not stopped and not keyboarding
            if robotTask != STOP and robotTask != KBD:
                [realx, realy, realthr] = self.getRealPose()
                distToGoal = math.sqrt( (realx-goal[0])**2 + (realy-goal[1])**2 )
                if distToGoal < RADIUS:
                    print 'At goal!'
                    self.setVels(0,0,noise)
                    robotTask = KBD


                
            
            #
            # Planning what to do next
            #


            
            # This stops if a bump is encountered
            if bump[0] == True or bump[1] == True:
                print 'BUMP!',
                print '  [Left bump sensor:',  bump[0], ']  ',
                print '  [Right bump sensor:', bump[1], ']  '
                robotTask = STOP
                statePrint( robotTask )
                
                
            # This checks for proximity to a wall...
            if d < 2*RADIUS and robotTask == GO:
                # if we're within 2 robot radii:
                print "Near a wall!"
                self.setVels(0,RV,noise)  # set a turning velocity
                pause_stop = time.time() + 2.0    # 2 seconds from now
                nextRobotTask = GO        # return to GO state afterwards
                robotTask = GOFOR         # this is out timing-based state
                statePrint( robotTask )   # let the user know...
                

                
            #          
            # Taking action: Setting velocities
            #
            
            if robotTask == GOFOR:
                if time.time() > pause_stop:
                    robotTask = nextRobotTask
                    statePrint( robotTask )
                
            if robotTask == GO:
                self.setVels(50,0,noise)
                    
            if robotTask == STOP:  
                self.setVels(0,0)   # stop!
                robotTask = KBD     # go to KBD state
                
            # In state KBD keypresses can
            # override or set our actions
            if robotTask == KBD:
                if   kbd == 'r': 
                    rangeHeading += 5
                    if rangeHeading > 180: rangeHeading -= 360
                elif kbd == 'R':
                    rangeHeading -= 5
                    if rangeHeading < -180: rangeHeading += 360
                elif kbd == 'i': self.setVels(FV,0,noise)
                elif kbd == 'k': self.setVels(-FV,0,noise)
                elif kbd == 'j': self.setVels(FV,RV,noise)
                elif kbd == 'l': self.setVels(FV,-RV,noise)
                elif kbd == 's':
                    robotTask = GO
                    statePrint( robotTask )
                elif kbd == ' ': 
                    robotTask = KBD
                    self.setVels(0,0,noise)   
                
            # special cases to allow us to quit entirely ('Q' or 'q')
            # or to stop (' ') and resume keyboard control
            if kbd == 'Q' or kbd == 'q': break    # 'Q' or 'q' quits

            # space (' ') stops and sets keyboard control
            if kbd == ' ':
                self.setVels( 0.0, 0.0, noise )
                robotTask = KBD
            

            # We sleep to let the graphics catch up...
            # Don't sleep elsewhere (it makes the program
            # unresponsive, since the kbd is not being
            # checked!) Instead, use the PAUSE state.
            time.sleep(0.025) # 1/40 of a second
               
            
        # if the while loop ends, we shutdown the gui, too. 
        self.gui.shutdown()
        time.sleep(1)
        sys.exit()
    
            

    
if __name__ == '__main__':
        
    # you might try one of these maps:
    MAPS = [ 'map0.txt',  # 0
             'map1.txt',  # 1
             'map2rooms.txt',   # 2
             'mapColors.txt',   # 3
             'mapMaze.txt',     # 4
             'mapHallways.txt', # 5
             'mapLibraComplex.txt' ]  # 6
             
    R = Robot(MAPS[1])
    R.run()

# Note on using the "noisy roomba" ...
#
        # you can control the noise added to the velocities by passing in
        # a third parameter to setVels. This third parameter is interpreted
        # as a percentage of the actual velocity. (Since any % of 0 is 0, the
        # robot will stop when commanded to stop, regardless of the noise size.)
        #
        # You will have access only to the noisy odometric readings (x, y, thr),
        # but you'll get to see both the noisy readings (blue) and the real
        # robot position (red). The sensor data comes from the real robot, as it
        # must, since the real robot is the one interacting with the world.
        # 
        # Keep in mind that the objective is still to get the _real_ robot
        # to the goal. In order to check this, there is a self.getRealPose
        # method for seeing if you're close enough to the goal. (See code.)
        # You're welcome to use self.getRealPose elsewhere, but then the task
        # reduces to the non-noise case... .
        #
        # So, how can this be done? The key is to use the environment!
        # The following call gets the segments (of class Seg) in the map
        # each has two endpoints named (x1,y1) and (x2,y2). See the code
        # for this.
    

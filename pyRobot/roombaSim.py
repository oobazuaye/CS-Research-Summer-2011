
import random
import time
import math

GLOBAL_DELTA = 10.0   # 1/2 the distance between the wheels

class RoombaOdometricPosition:

    def __init__(self, x_in=0., y_in=0., thr_in=0.):
        self.x = x_in
        self.y = y_in
        self.thr = thr_in # radians from 0 to 2pi - change to thr sometime...
        self.DELTA = GLOBAL_DELTA

    def __str__(self):
        return 'x,y,thd:' + str(self.x) + ' ' + str(self.y) + ' ' + str(math.degrees(self.thr))

    def set(self,x_in,y_in,thr_in):
        self.x = x_in
        self.y = y_in
        self.thr = thr_in

    def reset(self):
        self.set(0.,0.,0.)
        
    def vals(self):
        return self.x, self.y, self.thr

    def diffDriveKinUpdate(self, left_cm, right_cm):
        """This method takes in
        left_cm  = the number of cm the left wheel has turned
        right_cm = the number of cm the right wheel has turned
        (forward is positive, reverse is negative)
        and it changes the calling object to reflect this motion
        """
        #
        # debugging
        #
        #print 'in Kin, l,r are', left_cm, right_cm

        # let's leave if there is nothing to do...
        if left_cm == 0 and right_cm == 0:
            return

        # compute the radius of curvature (ROC)
        #
        # this assumes that the robot has been traveling with constant
        # radius of curvature, which should be mostly satisfied
        # as long as we update the position every time that the velocity
        # is changed
        #
        # ROC = DELTA * (R + L) / (R - L), where DELTA is 1/2 distance between the wheels
        ROCdenominator = right_cm - left_cm
        ROCnumerator = right_cm + left_cm

        # if the denominator's value is too small relative to the numerator, the robot is 
        # essentially traveling in a straight line - the following ratio of 10000:1 means
        # that we will consider anything within 0.005 of a degree a straight line - 
        # likely undetectable, given all of the other sources of odometric error

        if ROCdenominator == 0 or math.fabs(ROCnumerator/float(ROCdenominator)) > 10000.0:
            # theta does not change
            self.x += math.cos(self.thr)*left_cm # left_cm ~= right_cm
            self.y += math.sin(self.thr)*left_cm

        else:  # left_cm ~= right_cm
            #global gvel_left_cmpersec, gvel_right_cmpersec, gtime
            #print 'gvel:l,r,time are', gvel_left_cmpersec, gvel_right_cmpersec, gtime
            #print 'gpos before is', self.x, self.y, self.theta*180.0/math.pi
            #print 'right_cm, left_cm are', right_cm, left_cm
            #print 'ROCden, ROCnum are', ROCdenominator, ROCnumerator
            #
            # otherwise, we have to figure out the ROC and the angle turned
            # the angle, theta, is computed based on the wheel that turned further
            #
            # that wheel rotated around a radius of (DELTA + fabs(ROC))
            #
            # theta = max(fabs(L),fabs(R)) / (DELTA + fabs(ROC)) 
            #
            # DELTA has to be in the same units as w1 and w0...
            ROC = self.DELTA * float(ROCnumerator) / float(ROCdenominator)
            #print 'ROC is', ROC
            d_thr = max(math.fabs(right_cm),math.fabs(left_cm)) / (self.DELTA + math.fabs(ROC))
            # but theta's sign is not necessarily correct...
            #
            # we will use a positive value to indicate counterclockwise rotation (left)
            # with respect to the robot's "forward-facing" pose
            #
            # the opposite (negative) rotation occurs when the left wheel has
            # traveled further
            #
            if left_cm > right_cm:
                d_thr = -d_thr

            # new conversion
            #print 'theta is', theta*180.0/math.pi;

            # first, we compute the canonical distance traveled
            # assume the robot is facing the positive x direction
            # and that positive y is to the left and the robot
            # is at (0,0)
            #
            # hooray for ASCII art!
            #
            #                ^ +x (aligned with self.theta)
            #                |
            # L=left_cm  ^   |   ^  right_cm=R
            #            |   |   |
            #     +y <---W1--+--W0--- -y (perp to self.theta)
            #                |
            #                |       DELTA = 1/2 distance from W1 to W0
            #                | -x
            #
            # The wheels W1 and W0 give rise to positive differences
            # when they are headed forward along the positive x axis
            #
            # then the center of the circle along which it's traveling
            # is at (0,ROC)
            # 
            # and the resulting position after the arc is
            # (0,ROC) + (ROC*sin(theta),-ROC*cos(theta))
            #
            # kinematics error #2: used absolute value below...
            deltax = 0.0 + ROC*math.sin(d_thr)
            deltay = ROC - ROC*math.cos(d_thr)
            #print 'local deltax and deltay are', deltax, deltay

            # now, we need to convert this local-coordinate deltax and deltay
            # into the global frame - 
            # deltax is the change along self.theta
            # deltay is the change perpendicular to self.theta, along self.theta + pi/2
            #
            x_from_deltax = math.cos(self.thr) * deltax
            # are you joking me!! the value on the right below was deltay - ouch!
            y_from_deltax = math.sin(self.thr) * deltax
            x_from_deltay = math.cos(self.thr + math.pi/2.0) * deltay
            y_from_deltay = math.sin(self.thr + math.pi/2.0) * deltay

            #print 'global deltax and deltay are', (x_from_deltax + x_from_deltay), (y_from_deltax + y_from_deltay)

            # adjust position
            self.x += (x_from_deltax + x_from_deltay)
            self.y += (y_from_deltax + y_from_deltay)
            self.thr += d_thr

            # make sure we're less or equal to 2pi
            while self.thr > math.pi*2.:
                self.thr -= math.pi*2.
            # make sure we're greater than or equal to 0
            while self.thr < 0:
                self.thr += math.pi*2.

            #print for debugging...
            #print 'l,r,ROC,thd are', left_cm, right_cm, ROC, self.theta*180.0/3.14159
            #print 'gpos after is', self.x, self.y, self.theta*180.0/math.pi, '\n'
            #print 'current pos is'
            #self.pr();
            
import sensorSimulator

class roombaSim:
    def __init__(self, PORT, mapfile=None):
        self.gvel_left_cmpersec = 0.0
        self.gvel_right_cmpersec = 0.0
        self.gpos = RoombaOdometricPosition()  # real, global pose
        
        # get rid of calls to getPose... all in getUpdatedPose
        self.odpos = RoombaOdometricPosition() # odometric pose
        self.odvel_left_cmpersec = 0.0
        self.odvel_right_cmpersec = 0.0
        self.odvel_left_cmpersec_old = 0.0
        self.odvel_right_cmpersec_old = 0.0
        
        self.lastUpdatedTime = time.time()
        
        if mapfile != None:
            self.simmap = sensorSimulator.Map(mapfile)
        else:
            self.simmap = None
        
        global GLOBAL_DELTA
        self.DELTA = GLOBAL_DELTA 
        
    def getPose(self):
        newtime = time.time()
        deltaTimeSeconds = newtime - self.lastUpdatedTime
        self.lastUpdatedTime = newtime
        left_wheel_cm = self.gvel_left_cmpersec * deltaTimeSeconds
        right_wheel_cm = self.gvel_right_cmpersec * deltaTimeSeconds
        # next, update the current odometer based on those motions
        self.gpos.diffDriveKinUpdate(left_wheel_cm, right_wheel_cm)
        #delta_trans = 10
        #delta_degrees = 30
        #dx = random.uniform( -delta_trans, delta_trans )
        #dy = random.uniform( -delta_trans, delta_trans )
        #dthr = random.uniform( -math.radians(delta_degrees),
        #                        math.radians(delta_degrees) )
        #print 'time:', newtime, 'pose', self.gpos
        return self.gpos.x, self.gpos.y, self.gpos.thr
        
    def getRange( self, offsetThd ):
        # forward is offsetThd of 0.0
        # we'll see about left and right...
        x, y, thr = self.gpos.vals()
        current_thd = math.degrees(thr)
        range_thd = current_thd+offsetThd
        # self.simmap is a Map
        distance = self.simmap.findRangeDeg(x,y,range_thd)
        return distance
        
    def getUpdatedPose(self):
        newtime = time.time()
        deltaTimeSeconds = newtime - self.lastUpdatedTime
        self.lastUpdatedTime = newtime
        left_wheel_cm = self.gvel_left_cmpersec * deltaTimeSeconds
        right_wheel_cm = self.gvel_right_cmpersec * deltaTimeSeconds
        #oldgpos = self.gpos.vals()
        # next, update the current odometer based on those motions
        self.gpos.diffDriveKinUpdate(left_wheel_cm, right_wheel_cm)
        
        collisions = self.simmap.findroombacollisions(*self.gpos.vals())
        if len(collisions) > 0:
            # undo the last pose change...
            # we don't change the odpos either (no encoder changes; fair enough)
            self.gpos.diffDriveKinUpdate(-left_wheel_cm, -right_wheel_cm)
            if collisions[0] < -0.1:
                self.SENSORS = [False, True]  #right
            elif collisions[0] > 0.1:
                self.SENSORS = [True, False]  #left
            else:
                self.SENSORS = [True, True]   #front
        else: #len(collisions) == 0 
            # we _do_ change the odometric pose
            left_wheel_cm = self.odvel_left_cmpersec * deltaTimeSeconds
            right_wheel_cm = self.odvel_right_cmpersec * deltaTimeSeconds
            self.odpos.diffDriveKinUpdate(left_wheel_cm, right_wheel_cm)
            self.SENSORS = [False, False]
           

        #print 'time:', newtime, 'pose', self.gpos
        #return [self.gpos.x, self.gpos.y, self.gpos.thr], self.SENSORS
        return [self.gpos.x, self.gpos.y, self.gpos.thr], [self.odpos.x, self.odpos.y, self.odpos.thr], self.SENSORS

    
    def setVels(self, cmpersec, degpersec, noise_perc=0.0):
        # need to invert the kinematics to get the wheel rotations
        # in cm per second
        
        # the translational component is easy
        left_trans_cm_sec = cmpersec
        right_trans_cm_sec = cmpersec
        
        # the rotational component is not too bad 
        # note that if the translational component is 0, this
        # allows for a maximum of about 60 degrees per second...
        
        # ok, I think this does not combine rotation and translation
        # in the most natural way
        DELTA = self.DELTA
        left_rot_cm_sec = - self.DELTA * (degpersec * math.pi / 180.0 )
        right_rot_cm_sec = self.DELTA * (degpersec * math.pi / 180.0 )
        
        #print 'cm, deg', cmpersec, ',', degpersec
        #print 'left,right trans', left_trans_cm_sec, ',', right_trans_cm_sec
        
        # instead, we should add a constant that makes the smaller of
        # these equal to zero - that way the slower wheel will travel
        # the desired translational amount, and the rotation will
        # be taken up by the faster wheel...
        
        # since they're of opposite sign, this will work
        #adjust = max(left_rot_cm_sec, right_rot_cm_sec)
        #left_rot_cm_sec += adjust
        #right_rot_cm_sec += adjust
        
        # add them up
        left_cm_sec = left_trans_cm_sec + left_rot_cm_sec
        right_cm_sec = right_trans_cm_sec + right_rot_cm_sec
        #print 'left,right total', left_cm_sec, ',', right_cm_sec
        
        # see if they've changed - if not, return
        if left_cm_sec == self.odvel_left_cmpersec_old and right_cm_sec == self.odvel_right_cmpersec_old:
            return
        # otherwise, reset the old ones...
        else:
            self.odvel_left_cmpersec_old = left_cm_sec
            self.odvel_right_cmpersec_old = right_cm_sec
        
        # "send off to robot"
        self.getUpdatedPose()  # update odometry
        self.odvel_right_cmpersec = right_cm_sec
        self.odvel_left_cmpersec = left_cm_sec
        
        # plus the random components for the REAL velocities!!
        self.gvel_right_cmpersec = right_cm_sec*(1.0 + random.uniform(-noise_perc, noise_perc))
        self.gvel_left_cmpersec = left_cm_sec*(1.0 + random.uniform(-noise_perc, noise_perc))
        
    def getData(self):
        return self.getUpdatedPose()
        
        
        
import RobotCanvas
import Tkinter
import time
import threading
import random
import Queue
import math
import sys

class GuiPart:
    def __init__(self, master, queue, mapname):
        self.queue = queue
        self.master = master
        #
        self.rf = RobotCanvas.RobotFrame(master)
        # right now, maps have to be added before robots
        self.mapname = mapname
        self.rf.canv.loadMap(self.mapname)
        
        # the robot
        self.odrobot = RobotCanvas.MovableCircle( self.rf.canv, colorstr='blue' )
        self.simrobot = RobotCanvas.MovableCircle( self.rf.canv, colorstr='red' )
        
    def shutdown(self):
        self.rf.quit()
        self.master.destroy()
        sys.exit(0)

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        self.rf.canv.redrawRemote()

        while self.queue.qsize():
            try:
                list = self.queue.get(0)
                #execute function with 0 or more parameters
                list[0](*list[1:])
            except Queue.Empty:
                pass

        self.master.after(20, self.processIncoming) # 50 hz

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, mapname):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        # the map
        self.mapname = mapname
        
        # basic windows
        self.root = Tkinter.Tk()
        self.root.withdraw()
        self.master = Tkinter.Toplevel(master=self.root)
        
        # Create the queue
        self.queue = Queue.Queue()
        # Set up the GUI part
        self.gui = GuiPart(self.master, self.queue, self.mapname)
        self.canv = self.gui.rf.canv  # for easy reference
        
        # the simulated robot, r and the map it is in...
        self.r = roombaSim(0,self.mapname)
        self.rangeLine = RobotCanvas.MovableLine(self.canv, 
            [(-10000,-10000),(-10000,-10000)], colorstr='red', width=1)
        self.goalPoint = RobotCanvas.MovablePoint(self.canv, cx = -10000,
             cy = -10000, pixelradius=5, colorstr='green')

        # see if this helps with getting the graphics set up
        time.sleep(1)
        
        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.sim = threading.Thread(target=self.simulator)
        self.sim.setDaemon(1)
        self.sim.start()
        
        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.gui.processIncoming()
        
    def run(self):
        """ starts handling under events to the window """
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print 'Control-c caught from GUI. Quitting...'
            sys.exit(0)
        
    def getWindowEvents(self):
        return self.canv.lastKeyDown, self.canv.lastMouseClick
        
    def getRealPose(self):
        return [self.r.gpos.x, self.r.gpos.y, math.degrees(self.r.gpos.thr)]
        
    def getData(self):
        #try:
            [x,y,thr], [odx,ody,odthr], bump = self.r.getData()
            self.queue.put([self.gui.simrobot.setGlobalPose, x, y, thr])
            self.queue.put([self.gui.odrobot.setGlobalPose, odx, ody, odthr])
            #self.gui.simrobot.setGlobalPose(x, y, thr)
        #except Exception, e:
            # print e
            # print 'Exception in getData'
            # x = 0
            # y = 0
            # thr = 0.0
            # bump = [False,False]

            odthd = math.degrees(odthr)
            return [odx,ody,odthd], bump
        
    def setVels(self, cmpersec, degpersec, noise=0.0):
        if cmpersec >  50.0: cmpersec =  50.0
        if cmpersec < -50.0: cmpersec = -50.0
        if degpersec >  75.0: degpersec =  75.0
        if degpersec < -75.0: degpersec = -75.0
        self.r.setVels(cmpersec, degpersec, noise)
        
    def getMap(self):
        return self.r.simmap.items
        
    def getRange(self, degrees):
        #try:
            d = self.r.getRange(degrees)
            odx, ody, odthr = self.r.odpos.vals()
            self.queue.put([self.rangeLine.setGlobalPose,odx,ody,odthr+math.radians(degrees)])
            self.queue.put([self.rangeLine.changeCoords,[(0,0),(d,0)]])
            #self.rangeLine.setGlobalPose(x,y,thr+math.radians(degrees))
            #self.rangeLine.changeCoords([(0,0),(d,0)]) 
        #except Exception, e:
            # print e
            # print 'Exception in getRange'
            # d = 0
            return d
        
    def showGoal(self, goal):
        self.goalPoint.setGlobalPose(goal[0], goal[1], 0.0)
                
    def simulator(self):
        """ placeholder for the Robot's simulator method """
        print 'In ThreadedClient\'s simulator method'
        
        
        

"""
A Tkinter.Canvas derived class with some
helpful things for drawing and updating...
"""

import random
from Tkinter import *
import math

class Affine2dTrans:
    """ let's create our own 2d affine class """

    def __init__(self):
        """ the components currently supported """ 
        self.scalex = 1.0  # units of  pixels per worldunit (cm)
        self.scaley = 1.0  # units of  pixels per worldunit (cm)
        self.cx = 0.0      # worldunits (cm)
        self.cy = 0.0      # worldunits (cm)
        self.px = 0.0      # pixels
        self.py = 0.0      # pixels
        self.thr = 0.0     # radians, though the interface is always degrees
        self.sinthr = math.sin(0.0)   # why compute this more than once?
        self.costhr = math.cos(0.0)   # why not say it more than once?

    def transform(self, (x,y)):
        return self.transformWorldToPixel((x,y))
        
    def __repr__(self):
        s = '\n'
        s += '\nscalex  '+ str(self.scalex)
        s += '\nscaley  '+ str(self.scaley)
        s += '\ncx      '+ str(self.cx)
        s += '\ncy      '+ str(self.cy)
        s += '\npx      '+ str(self.px)
        s += '\npy      '+ str(self.py)
        s += '\nthr     '+ str(self.thr)
        s += '\nthd     '+ str(math.degrees(self.thr))
        s += '\nsinthr  '+ str(self.sinthr)
        s += '\ncosthr  '+ str(self.costhr)
        s += '\n'
        return s

    def transformWorldToPixel(self, (worldx, worldy)):
        """ outpus pixel coordinates for the input world coords """
        # first, compute the offset from the world's center of rotation
        offx = worldx - self.cx
        offy = worldy - self.cy
        # next, rotate the resulting vector by theta
        rx = self.costhr * offx - self.sinthr * offy
        ry = self.sinthr * offx + self.costhr * offy
        # next, scale the result
        rx = rx * self.scalex
        ry = ry * self.scaley
        # finally, add the pixel offset
        return ( self.px + rx, self.py + ry )

    def transformPixelToWorld(self, (pixelx, pixely)):
        """ outputs world coordinates for the input pixel coords """
        # first subtract the pixel offset
        rx = pixelx - float(self.px)
        ry = pixely - float(self.py)
        # unscale the result
        rx = rx / self.scalex
        ry = ry / self.scaley
        # unrotate the vector by theta
        offx =  self.costhr * rx + self.sinthr * ry
        offy = -self.sinthr * rx + self.costhr * ry
        # add the world offset to get world coords
        return (offx + self.cx, offy + self.cy)

    def transform_scale(self, length, thd):
        """ returns the new length equivalent in pixels to  the input
            length along the thd direction (in degrees) - if x and y
            are not equal, thd will make a difference... 

            length sould be positive - a positive result will be
            returned in any case

            thd is in global world terms, not relative to the
            stored thr within this transformation """
        # first, compute the offset from the world's center of rotation
        thr = thd * 180.0 / math.pi
        offx = length * math.cos(thr)
        offy = length * math.sin(thr)
        # next, scale the result
        rx = offx * self.scalex
        ry = offy * self.scaley
        # finally, compute the magnitude
        return ( math.sqrt( rx * rx + ry * ry ) )
        
    def deltaWorldRotationCenter(self, deltaworldx, deltaworldy):
        """ moves the world rotation center by the amounts
            provided in the inputs deltaworldx and deltaworldy
        """
        self.cx += deltaworldx
        self.cy += deltaworldy

    def setWorldRotationCenter(self, worldcenterx, worldcentery):
        """ puts the input world point onto the input pixel point
            and make that point the center of any rotation specified """
        # I don't know if rotation should be preserved through this call...
        self.cx = worldcenterx
        self.cy = worldcentery

    def setPixelRotationCenter(self, pixelx, pixely):
        """ puts the input world point onto the input pixel point
            and make that point the center of any rotation specified 
        """
        # I don't know if rotation should be preserved through this call...
        self.px = pixelx
        self.py = pixely

    def setScales(self, scale_x, scale_y):
        """ allows for axis flipping and nonuniform (!) scaling, though
            why you'd want that is beyond me... each of scale_x and 
            scale_y are expressed in pixels per world unit (cm) "
        """
        if scale_x == 0.0 or scale_y == 0.0:
            print "Warning - you don't want a finite world length mapping to 0 pixels!"
        self.scalex = scale_x
        self.scaley = scale_y
    
    def setScalesAbsVal(self, scale_x, scale_y):
        """ this will preserve the signs of self.scalex and self.scaley,
            setting their absolute values to scale_x and scale_y, respectively
        """
        if scale_x == 0.0 or scale_y == 0.0:
            print "Warning - you don't want a finite world length mapping to 0 pixels!"
        if self.scalex > 0: self.scalex = abs(scale_x)
        else:               self.scalex = -abs(scale_x)
        if self.scaley > 0: self.scaley = abs(scale_y)
        else:               self.scaley = -abs(scale_y)

    def multiplyScales(self, mult_x, mult_y):
        """ change the x and y scales by multiplying by the inputs 
            scalex and scaley are in units of pixels per world unit (cm)
        """
        if mult_x == 0.0 or mult_y == 0.0:
            print "Warning - you don't want a finite world length mapping to 0 pixels!"
        self.scalex *= mult_x
        self.scaley *= mult_y

    def setRotationAngle(self, thd):
        """ set the number of degrees which the world coordinates
            are rotated (around the rotation center) before mapping to pixels """
        self.thr = thd * math.pi / 180.0
        self.costhr = math.cos(self.thr)
        self.sinthr = math.sin(self.thr)

    def deltaRotationAngle(self, thd):
        """ changes the number of degrees which the world coordinates
            are rotated (around the rotation center) before mapping to pixels """
        self.thr = self.thr + (thd * math.pi / 180.0)
        self.costhr = math.cos(self.thr)
        self.sinthr = math.sin(self.thr)



class Movable:
    """ Movable is a wrapper around Tkinter.Canvas objects
        it holds their _global_ coordinates, converting to
        pixel coordinates as necessary (saving time, perhaps...)

        It can be subclassed to allow for all sorts of
        composite objects to be treated as one, with their
        own, object-local coordinate system
    """

    def __init__(self, canvas, cx=0.0, cy=0.0, thr=0.0, colorstr='black'):
        """ set up a local coordinate system """
        self.canvas = canvas
        # self.tag = 'notag'  # don't seem to be using this...
        self.cx = cx
        self.cy = cy
        self.thr = thr
        self.colorstr = colorstr
        self.sinthr = math.sin(self.thr)
        self.costhr = math.cos(self.thr)
        self.localCoords = []
        self.updateGlobalCoords() # sets self.globalCoords
        self.canvas.addMovable(self) # adds self object to the canvas's list

    def localToGlobalCoords(self, (x,y)):
        """ transforms one point from object-local to global
            coordinates

            self.cx and self.cy are the global location of the 
            center of the object-local coordinate system, and it's
            facing self.thr
        """
        return ( (x*self.costhr - y*self.sinthr + self.cx, 
                  x*self.sinthr + y*self.costhr + self.cy) )

    def updateGlobalCoords(self):
        """ create global coordinates if the object-local coordinates
            are centered at (cx,cy) facing thr
            input L: should be a list of tuples

            could be overridden
        """
        self.globalCoords = [ self.localToGlobalCoords(T) for T in self.localCoords ]
        #print 'cx,cy,thd are', self.cx, self.cy, math.degrees(self.thr)
        #print 'globalCoords are', self.globalCoords

    def deltaGlobalPose( self, dx, dy, dthr ):
        """ change the global pose of this object """
        self.setGlobalPose( self.cx+dx, self.cy+dy, self.thr+dthr )

    def setGlobalPose( self, cx, cy, thr ):
        """ set the absolute global pose of this object """
        self.cx = cx
        self.cy = cy
        self.thr = thr
        self.sinthr = math.sin(self.thr)
        self.costhr = math.cos(self.thr)
        self.updateGlobalCoords()
        self.updatePixelCoords()

    def setColor( self, r, g, b ):
        """ this writes the appropriate color string """
        self.colorstr = "#%02x%02x%02x" % (r,g,b)
        self.canvas.itemconfigure( self.itemid, fill=colorstr )

    def setColorstr( self, colorstr ):
        """ this takes a color name """
        self.colorstr = colorstr
        self.canvas.itemconfigure( self.itemid, fill=colorstr )

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
            should be overridden
        """
        print 'in Movable\'s updatePixelCoords'

    def createObjects( self ):
        """ computes pixel coordinates and then creates the canvas objects
            should be overridden
        """
        print 'in Movable\'s createObjects'
        
    def delete( self ):
        """ deletes the items from the canvas
        """
        # should be the list of items!
        # some have more than 1!
        self.canvas.delete( self.itemid )

        
        
       
class MovablePixelLengthLine(Movable):
    
    def __init__(self, canvas, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black', width=2, pixellength=8, arrow=None):
        """ the MovablePixelLengthLine constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        self.width = width
        self.pixellength = pixellength
        self.arrow = arrow
        self.localCoords = [ (0.0,0.0),    # these are object-local coordinates
                             (1.0,0.0) ]   # except the length is wrong...
        self.updateGlobalCoords()        # now in world coords, (cx,cy)
        self.createObjects()             # using self.pixellength
        
    def changeAnchor( self, cx, cy, thr=None ):
        """ changeAnchor moves the starting point of the line, cx, and cy,
            both in world coordinates. thr is optional and will reorient the
            line from its anchor for its designated pixel length
        """
        # can't use   if not thr  below because thr might be 0.0 !!
        if thr == None:
            thr = self.thr
        self.setGlobalPose( cx, cy, thr )
        #print 'global pose set to', cx, cy, math.degrees(thr), 'in changeAnchor'
        self.updatePixelCoords()
        
    def computeEndVertex( self, p ):
        """ returns a tuple with the pixel coordinates of the end vertex
            if the initial vertex has pixel coordinates of p[0][0], p[0][1]
            and the end vertex is currently p[1][0], p[1][1] (the wrong length)
        """
        #print 'p is', p
        length = math.sqrt( (p[1][0] - p[0][0])**2 + (p[1][1] - p[0][1])**2 )
        ratio = self.pixellength / float(length)
        #print 'l and ratio are', length, ratio
        endx = p[0][0] + (p[1][0]-p[0][0])*ratio
        endy = p[0][1] + (p[1][1]-p[0][1])*ratio
        #print 'endx,y are', endx, endy
        return endx, endy
        

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # p has the pixel coords of the anchor (starting vertex)
        p = map( self.canvas.tfm.transform, self.globalCoords )
        # now we need to find the other endpoint by scaling p[1] and p[2]
        # so that the length of their sum is self.;pixellength
        endx, endy = self.computeEndVertex(p)
        self.canvas.coords( self.itemid, p[0][0], p[0][1], 
                                         endx, endy )

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        endx, endy = self.computeEndVertex(p)
        self.itemid = self.canvas.create_line(p[0][0], p[0][1], 
                                              endx,    endy,
                                              fill=self.colorstr,
                                              width=self.width) 
        if self.arrow:
            self.canvas.itemconfigure( self.itemid, arrow='last',
                                                    capstyle='round' )
        
        
        
        
class MovablePoint(Movable):

    def __init__(self, canvas, cx=0.0, cy=0.0, 
                       colorstr='black', pixelradius=2):
        """ the MovablePoint constructor """
        Movable.__init__(self, canvas, cx, cy, 0.0, colorstr)
        self.pixelradius = int(pixelradius)
        self.localCoords = [ (0,0) ]
        self.updateGlobalCoords()
        self.createObjects()

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        p = map( self.canvas.tfm.transform, self.globalCoords )
        r = self.pixelradius
        self.canvas.coords( self.itemid, p[0][0]-r, p[0][1]-r, 
                                         p[0][0]+r, p[0][1]+r )

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        r = self.pixelradius
        self.itemid = self.canvas.create_oval(p[0][0]-r, p[0][1]-r, 
                                              p[0][0]+r, p[0][1]+r,
                                              fill=self.colorstr, 
                                              outline='')
        
        
        
        
class MovableCircle(Movable):

    def __init__(self, canvas, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black', radius=10.0):
        """ the MovableCircle constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        self.radius = radius
        self.localCoords = [ (0.0,0.0), (self.radius,0.0) ]
        self.updateGlobalCoords()
        self.createObjects()

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        p = map( self.canvas.tfm.transform, self.globalCoords )
        r = self.canvas.tfm.transform_scale( self.radius, 0.0 )
        self.canvas.coords( self.itemid, p[0][0]-r, p[0][1]-r, 
                                         p[0][0]+r, p[0][1]+r )
        self.canvas.coords( self.itemid2, p[0][0],p[0][1],
                                          p[1][0],p[1][1])

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        r = self.canvas.tfm.transform_scale( self.radius, 0.0 )
        self.itemid = self.canvas.create_oval(p[0][0]-r, p[0][1]-r, 
                                              p[0][0]+r, p[0][1]+r,
                                              fill=self.colorstr, 
                                              outline='black')
        self.itemid2 = self.canvas.create_line(p[0][0],p[0][1],
                                               p[1][0],p[1][1],
                                               fill='white',width=2)
                                               


class MovableLine(Movable):

    def __init__(self, canvas, endpoints, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black', width=2):
        """ the MovableLine constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        self.width = width
        self.localCoords = endpoints[:]  # should be two 2-tuples
        self.updateGlobalCoords()
        self.createObjects()
        
    def changeCoords( self, newcoords ):
        """ should be called updateWorldCoords!
        """
        # remember this "localCoords" is object-local (NOT pixel)
        self.localCoords = newcoords[:]  # better be the right format!
        self.updateGlobalCoords()
        self.updatePixelCoords()

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        p = map( self.canvas.tfm.transform, self.globalCoords )
        self.canvas.coords( self.itemid, p[0][0], p[0][1], 
                                         p[1][0], p[1][1] )

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        self.itemid = self.canvas.create_line(p[0][0], p[0][1], 
                                              p[1][0], p[1][1],
                                              fill=self.colorstr,
                                              width=self.width) 


class MovableRect(Movable):

    def __init__(self, canvas, tlbr_endpoints, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black'):
        """ the MovableRect constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        [ (tlx,tly), (brx,bry) ] = tlbr_endpoints
        # need to use a polygon so we can rotate...
        self.localCoords = [ (tlx,tly), (tlx,bry), (brx,bry), (brx,tly) ]
        self.updateGlobalCoords()
        self.createObjects()

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        p = map( self.canvas.tfm.transform, self.globalCoords )
        self.canvas.coords( self.itemid, p[0][0], p[0][1], 
                                         p[1][0], p[1][1],
                                         p[2][0], p[2][1],
                                         p[3][0], p[3][1] )

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        self.itemid = self.canvas.create_polygon(p[0][0], p[0][1], 
                                                 p[1][0], p[1][1],
                                                 p[2][0], p[2][1],
                                                 p[3][0], p[3][1],
                                                 fill=self.colorstr,
                                                 outline="black") 
class MovablePoly(Movable):

    def __init__(self, canvas, path_endpoints, cx=0.0, cy=0.0, thr=0.0, 
                       colorstr='black'):
        """ the MovablePoly constructor """
        Movable.__init__(self, canvas, cx, cy, thr, colorstr)
        self.localCoords = path_endpoints[:]
        self.colorstr = colorstr
        self.updateGlobalCoords()
        self.createObjects()
        
    def mappend(self,f,pointlist):
        """ just like mappend in CS 60
        """
        if len(pointlist) == 0: return []
        fp = f(pointlist[0])
        return [fp[0],fp[1]] + self.mappend(f,pointlist[1:])
        

    def updatePixelCoords( self ):
        """ redraws the object it represents on the canvas
        """
        # we could just delete and then call draw...
        # perhaps (?) it's faster to change the coordinates...
        # so we'll give it a try
        #px,py = self.canvas.tfm.transform( self.globalCoords[0] )
        #radius = self.canvas.tfm.transform_scale(self.radius,0.0)
        #self.canvas.coords( self.itemid, px-radius, py-radius,
        #p = map( self.canvas.tfm.transform, self.globalCoords 
        p = self.mappend( self.canvas.tfm.transform, self.globalCoords )
        #print 'p is', p
        # seems to want integral pixel values... fair enough
        p = map(int,p)
        #print 'now p is', p
        # it seems that the following call wants p in a flattened list
        # instead of a list of pairs
        self.canvas.coords( self.itemid, tuple(p) )
        # HERE for poly

    def createObjects( self ):
        """ computes pixel coordinates and then creates the
            canvas objects
        """
        # find pixel coordinates and create the canvas objects
        p = map( self.canvas.tfm.transform, self.globalCoords )
        self.itemid = self.canvas.create_polygon(p,
                                                 fill=self.colorstr,
                                                 outline=self.colorstr)
                          # it's good to have the outline be the same color
                          # to minimize gaps...


class ErdosCanvas(Canvas):
    """ This is a dervied class from canvas with support for
        a global transformation (tfm) and multiple objects
    """

    def __init__(self,master,height=400,width=400):
        """ a canvas to show a robot running around and a map
            a key facility is a general transformation allowing
            a user to specify everything in global coordinates
            and leave all of the translation to pixel coordinates
            to the computer (good!)
        """
        Canvas.__init__(self,master)
        # basic data members 
        self.master = master
        self.height = height   # window height
        self.width  = width    # window width
        self.scrollWidth = width
        self.scrollHeight = height  # this we'll work on later...

        # here is the transformation...
        self.tfm = Affine2dTrans()
        self.tfm.setWorldRotationCenter(0,0) # maps the world point 0,0 to 
        self.tfm.setPixelRotationCenter(self.width/2,self.height/2) # the center of the window

        # things in the world...
        self.movables = []   # for possibly moving objects with local coords

        # dictionary for keys pressed
        self.keysdown = {}

        self.configure(bg='white', width=self.width, height=self.height)
        self.bind("<Configure>", self.configcallback)

        # this will bring the focus to the main canvas...
        self.focus_set()
        self.bind("<KeyPress>", self.keypresscallback)
        self.bind("<KeyRelease>", self.keyreleasecallback)
        self.configure(highlightthickness=0)

        # handle all of the button events...
        self.bind("<Button-1>", self.b1_down)
        self.bind("<B1-Motion>", self.b1_move)
        self.bind("<ButtonRelease-1>", self.b1_up)

        self.bind("<Button-2>", self.click_b2_down)
        self.bind("<B2-Motion>", self.click_b2_move)
        self.bind("<ButtonRelease-2>", self.click_b2_up)

        self.bind("<Button-3>", self.click_b3_down)
        self.bind("<B3-Motion>", self.click_b3_move)
        self.bind("<ButtonRelease-3>", self.click_b3_up)

        # this data member flags the need to redraw for the graphics thread
        self.needToRedraw = False
        self.lastKeyDown = ''        # tracks the last key pressed, while pressed
        self.lastMouseClick = (0,0)  # tracks the last mouse click with 'g' pressed
        # the above data member will be used as the goal for the robot!

	# end of the __init__ constructor

    def reconfig(self):
        """ check h and w... """
        h = int(self.cget('height'))
        w = int(self.cget('width'))
        #print 'h,w are', h, w
        self.width = w
        self.height = h
        self.tfm.setPixelRotationCenter(self.width/2,self.height/2) 
        self.redraw()

    def configcallback(self, event):
        """ configcallback handles resizing, etc. """
        #print "***** config! *****"
        #print "dir is", dir(event)
        #print 'char, delta, height, keycode are', event.char, event.delta, event.height, event.keycode
        #print 'keysym, keysym_num, num, send_event', event.keysym, event.keysym_num, event.num, event.send_event
        #print 'serial, state, time, type', event.serial, event.state, event.time, event.type
        #print 'widget, width, x, x_root, y, y_root', event.widget, event.width, event.x, event.x_root, event.y, event.y_root
        #print "***** ******* *****"
        self.height = event.height 
        self.width = event.width
        # print 'h,w are', self.height, self.width
        # so that the world rotation center maps to the center of the window...
        self.tfm.setPixelRotationCenter(self.width/2,self.height/2) 
        self.startx = self.width/2    # for GUI events that change tfm
        self.starty = self.height/2
        self.redraw()
    
    def keypresscallback(self, event):
        """ handling keypresses """
        c = event.char
        #print 'keysym is', event.keysym
        #print 'c is', 
        self.lastKeyDown = c  # set the last key down

        # add an entry to our keysdown dictionary
        self.keysdown[event.keysym] = 1

        if c == '?':
            # way to ask about things on the fly!
            #print 'dir is', dir(tkv.canvas)
            #print 'help is', help(tkv.canvas.create_polygon)
            print 'This is the help system... add help to it as you see fit!'
        # char is the empty string for special (non-char) keys
        #print 'keysym is', event.keysym # things like 'Shift_R' for right shift key, etc.

    def keyreleasecallback(self, event):
        """ handling keyreleases """
        k = event.keysym
        self.lastKeyDown = '' # clear the last key down -- don't use multiple keys
        #print "key RELEASE of", k
        if self.keysdown.has_key(event.keysym):
            self.keysdown[event.keysym] = 0

    def loadMap(self, filename):
        """ loadMap reads in a file of obstacles and places them
            on this (self) canvas
        """
        # first clear the old stuff, if any
        # but keep the robots...
        #for (key,item) in self.world.iteritems():
        #    self.delete(item.itemid)  # deletes from the canvas
        #self.world = {}
        self.delete('all') # ... this will also delete any robots...
        self.movables = []

        # open the file
        # should do some sanilty checking here...
        mapfile = open(filename, 'r')
    
        prevx = 0
        prevy = 0

        max_x_found = -1000000.0
        max_y_found = -1000000.0
        min_x_found =  1000000.0
        min_y_found =  1000000.0
        
        for line in mapfile:
            line = line[0:line.find('#')]  # strip comment
            # strip whitespace and replace tabs with spaces
            line = line.strip().replace('\t',' ')  
            # get just the space-delimited tokens
            linedata = [x for x in line.split(' ') if x != '']

            # print "linedata is", linedata
            # if empty, continue
            if len(linedata) == 0: continue
        
            # check the type field
            if linedata[0] == 'LINE':
                if linedata[1] == 'PREV':
                    # create linked segment
                    x1 = prevx
                    y1 = prevy
                    x2 = float(linedata[2])
                    y2 = float(linedata[3])
                    # colors
                    r = float(linedata[4])
                    g = float(linedata[5])
                    b = float(linedata[6])

                else:
                    # create new segment
                    x1 = float(linedata[1])
                    y1 = float(linedata[2])
                    x2 = float(linedata[3])
                    y2 = float(linedata[4])
                    # colors
                    r = float(linedata[5])
                    g = float(linedata[6])
                    b = float(linedata[7])

                # add this wall line...
                tmpname = MovableLine(self,
                                      endpoints=[(x1,y1),(x2,y2)], 
                                      colorstr=("#%02x%02x%02x" % (r, g, b)) ) 

                prevx = x2
                prevy = y2
                if x1 < min_x_found:  min_x_found = x1
                if y1 < min_y_found:  min_y_found = y1
                if x1 > max_x_found:  max_x_found = x1
                if y1 > max_y_found:  max_y_found = y1
                if x2 < min_x_found:  min_x_found = x2
                if y2 < min_y_found:  min_y_found = y2
                if x2 > max_x_found:  max_x_found = x2
                if y2 > max_y_found:  max_y_found = y2

        self.snugSquareFitNoRotation( min_x_found, max_x_found, min_y_found, max_y_found )

        mapfile.close()
        
    def snugSquareFitNoRotation(self, x_min, x_max, y_min, y_max):
        """ this will set self.tfm so that the input rectangle
            is aligned with the window
            this will not change the rotation
            (but does not handle rotation yet)
        """
        yMultiplier = 0.85*self.height/math.fabs(y_max-y_min)
        xMultiplier = 0.85*self.width/math.fabs(x_max-x_min)
        #print 'y,x mults are', yMultiplier, xMultiplier
        scaleMultiplier = min(yMultiplier,xMultiplier)
        # mapdelta = max( (y_max-y_min), (x_max-x_min) )
        # scaleMultiplier = 0.85*min(self.height,self.width)/mapdelta
        # self.tfm.multiplyScales(scaleMultiplier, scaleMultiplier)
        #
        # this preserves the signs of the scales...
        self.tfm.setScalesAbsVal(scaleMultiplier, scaleMultiplier)

        # and set the center appropriate to the map...
        wx = (x_max + x_min)/2.0
        wy = (y_max + y_min)/2.0
        self.tfm.setWorldRotationCenter(wx, wy)
        self.redraw()  # have to redraw whenever self.tfm changes...

    def b1_down(self, event):
        if self.keysdown.has_key("Shift_L") and self.keysdown["Shift_L"] == 1:
            # print "b1 down with shift"
            self.click_b3_down(event)
        # c for camera/rotation
        # t for translation
        # should have r for rotation...
        elif (self.keysdown.has_key("c") and self.keysdown["c"] == 1) or \
             (self.keysdown.has_key("t") and self.keysdown["t"] == 1):
            self.startx = event.x
            self.starty = event.y
        # nonuniform scaling
        # c for camera/rotation
        # t for translation
        elif (self.keysdown.has_key("y") and self.keysdown["y"] == 1) or \
             (self.keysdown.has_key("x") and self.keysdown["x"] == 1):
            self.startx, self.starty = event.x, event.y
            self.b1_move(event)
            

    def b1_move(self,event):
        if self.keysdown.has_key("Shift_L") and self.keysdown["Shift_L"] == 1:
            # print "b1 move with shift"
            self.click_b3_move(event)

        elif (self.keysdown.has_key("c") and self.keysdown["c"] == 1) or \
             (self.keysdown.has_key("t") and self.keysdown["t"] == 1):
            self.endx = event.x
            self.endy = event.y
            # create a line in pixel space...
            self.delete('temporary_line')
            self.create_line(self.startx,self.starty,self.endx,self.endy,
                                         tag='temporary_line', fill='purple')
                                         
        elif (self.keysdown.has_key("y") and self.keysdown["y"] == 1) or \
             (self.keysdown.has_key("x") and self.keysdown["x"] == 1):
            self.delete('circle')
            x, y = self.width/2.0, self.height/2.0
            radius = self.length((x,y),(event.x,event.y)) 
            self.create_oval(x - radius, y - radius, x + radius, y + radius, 
                             tag="circle", outline="purple")
            # create a line in pixel space...
            self.delete('temporary_line')
            if (self.keysdown.has_key("y") and self.keysdown["y"] == 1):
                self.create_line(x,y-radius,  # from the center
                                 x,y+radius, # for our y extent
                                 tag='temporary_line', fill='purple',
                                 width=3)
            else:
                self.create_line(x-radius,y,  # from the center
                                 x+radius,y, # for our y extent
                                 tag='temporary_line', fill='purple',
                                 width=3)


    def b1_up(self,event):
        #print "up event at pixel coordinate", event.x, event.y
        #print "up event.keysym is", event.keysym
        
        if self.keysdown.has_key("Shift_L") and self.keysdown["Shift_L"] == 1:
            self.click_b3_up(event)
            
        elif self.keysdown.has_key("Control_L") and self.keysdown["Control_L"] == 1:
            (wx,wy) = self.tfm.transformPixelToWorld((event.x, event.y))
            self.tfm.setWorldRotationCenter(wx, wy)
            self.redraw()
            
        elif self.keysdown.has_key("t") and self.keysdown["t"] == 1:
            #print 'Translating...'
            self.endx = event.x
            self.endy = event.y
            # delete old line
            self.delete('temporary_line')
            sx, sy = self.tfm.transformPixelToWorld( (self.startx,self.starty) )
            #print "starting coordinates are (wx,wy) = ", (sx, sy)
            ex, ey = self.tfm.transformPixelToWorld( (self.endx,self.endy) )
            #print "ending coordinates are (ex,ey) = ", (ex, ey)
            self.tfm.deltaWorldRotationCenter( (sx-ex), (sy-ey) )
            self.redraw() # need to redraw after tfm changes!
            
        elif (self.keysdown.has_key("y") and self.keysdown["y"] == 1) or \
             (self.keysdown.has_key("x") and self.keysdown["x"] == 1):
            self.delete('circle')
            self.delete('temporary_line')
            x, y = self.width/2.0, self.height/2.0
            radius_stop = self.length((x,y),(event.x,event.y)) 
            radius_start = self.length((x,y),(self.startx, self.starty))
            if radius_start == 0.0: scaleMultiplier = 10.0
            else: scaleMultiplier = radius_stop/radius_start
            if (self.keysdown.has_key("y") and self.keysdown["y"] == 1) :
                self.tfm.multiplyScales(1.0, scaleMultiplier)
            else:
                self.tfm.multiplyScales(scaleMultiplier,1.0)
            self.redraw()
            
        elif self.keysdown.has_key("c") and self.keysdown["c"] == 1:
            self.endx = event.x
            self.endy = event.y
            # delete old line
            self.delete('temporary_line')
            wx, wy = self.tfm.transformPixelToWorld( (self.startx,self.starty) )
            # print "world coordinates are (wx,wy) = ", (wx, wy)
            # compute the theta in world space!
            ex, ey = self.tfm.transformPixelToWorld( (self.endx,self.endy) )
            thr = math.atan2( ey-wy, ex-wx)
            thd = (180.0/math.pi) * thr
            # create a camera!
            # self.addMovable...
            self.redraw()
            
        elif self.keysdown.has_key("p") and self.keysdown["p"] == 1:  
            # if 'p' is pressed, we print the coordinates
            #print "\npixel coordinates are (px,py) = ", event.x, event.y
            #print 'event.x and event.y are', event.x, event.y
            #print self.tfm
            #print 'event is', event
            #print 'event.x_root is', event.x_root
            #print 'event.y_root is', event.y_root
            #print 'event.delta is', event.delta
            #print dir(event)
            wx, wy = self.tfm.transformPixelToWorld( (event.x,event.y) )
            print "Click at world coordinates of (wx,wy) = ", wx, wy
            
        elif self.keysdown.has_key("g") and self.keysdown["g"] == 1:  
            # if 'g' is pressed, we set the "last goal clicked" variable
            #print "\npixel coordinates are (px,py) = ", event.x, event.y
            #print 'event.x and event.y are', event.x, event.y
            wx, wy = self.tfm.transformPixelToWorld( (event.x,event.y) )
            #print self.tfm
            #print "Goal clicked at world coordinates of (wx,wy) = ", wx, wy
            self.lastMouseClick = (wx,wy)

    def click_b2_down(self, event):
        pass

    def click_b2_move(self, event):
        pass

    def click_b2_up(self, event):
        pass

    def length(self, (x1, y1), (x2, y2)):
        return math.sqrt( (x1-x2)**2 + (y1-y2)**2 )

    def click_b3_down(self, event):
        self.startx, self.starty = event.x, event.y
        self.click_b3_move(event)

    def click_b3_move(self, event):
        self.delete('circle')
        x, y = self.width/2.0, self.height/2.0
        radius = self.length((x,y),(event.x,event.y)) 
        self.create_oval(x - radius, y - radius, x + radius, y + radius, tag="circle", outline="purple")

    def click_b3_up(self, event):
        """ scaling... """
        self.delete('circle')
        x, y = self.width/2.0, self.height/2.0
        radius_stop = self.length((x,y),(event.x,event.y)) 
        radius_start = self.length((x,y),(self.startx,self.starty))
        if radius_start == 0.0: scaleMultiplier = 10.0
        else: scaleMultiplier = radius_stop/radius_start
        self.tfm.multiplyScales(scaleMultiplier, scaleMultiplier)
        self.redraw()

    def redraw(self):
        """ this goes through the dictionary and recomputes the
            pixel coordinates
        """
        self.needToRedraw = True

    def redrawRemote(self):
        """ this goes through the dictionary and recomputes the
            pixel coordinates
        """
        if (self.needToRedraw):
            for item in self.movables:
                item.updatePixelCoords()
	    self.needToRedraw = False

    def addMovable(self, m):
        # check m's name or itemid - if already there, replace
        # self.movables[m.tag] = m
        # self.movables[m.itemid] = m
        # self.redraw()
        self.movables.append(m)
        
        
class RobotFrame(Frame):
    """ There was a split here to handle scroll bars, but
        then I decided against scroll bars.
        Yet the two classes (CS5Frame and CS5Win) remain...
    """
		
    def __init__(self,root):
        """ RobotFrame constructor """
        self.tkroot = root
        Frame.__init__(self,self.tkroot)
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(sticky=N+S+E+W)
        self.canv = ErdosCanvas( self )
        self.canv.grid( row=0, column=0, sticky=N+S+E+W )
        self.canv.tfm.setScales(1,-1)
        self.canv.tfm.setWorldRotationCenter(0,0)

    def _destroy(self):
        self.tkroot.destroy()
		


# I just like to have this for pasting into the console...
# import RobotCanvas ; reload(RobotCanvas) ; from RobotCanvas import *




# sensorSimulator.py

import math

# line segment class
class Seg:

    def __init__(self, x1, y1, x2, y2, r=42, g=42, b=42):
        """ we use a two-point representation """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.r = r
        self.g = g
        self.b = b

    def length(self):
        """ returns the Euclidean length """
        return math.sqrt( (self.x1 - self.x2)**2
                         +(self.y1 - self.y2)**2 )

    def setColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return "x1,y1,x2,y2,r,g,b: %f %f %f %f %d %d %d" % (self.x1,self.y1,self.x2,self.y2,self.r,self.g,self.b)

    def closestPoint(self, xp, yp):
        """ this returns (cx,cy,d): the point along self that 
            is closest to the point (px,py), along with the distance

            it's for finding intersections with circles...
        """
        # Ok, how do we do this?
        # look toward the point from each Seg endpoint
        # if the angle of _either one_ is not acute,
        # then the endpoint in question _is_ the closest
        # point (I don't see how they can _both_ be obtuse (?))
        #
        # this is equivalent to checking the sign of the dot product
        # with the unit vector along the Seg in each direction...
        #
        # dot1 = (xp-self.x1, yp-self.y1) * (self.x2-self.x1, self.y2-self.y1)
        #
        dx = self.x2-self.x1
        dy = self.y2-self.y1
        dot1 = (xp-self.x1)*dx + (yp-self.y1)*dy

        #print 'dot1 is', dot1

        if dot1 <= 0.0:
            # then x1,y1 is the closest point
            return (self.x1, self.y1, math.sqrt( (xp-self.x1)**2 + (yp-self.y1)**2 ) )
        
        # need to reverse the sign of dx and dy for the other direction
        dot2 = (xp-self.x2)*(-dx) + (yp-self.y2)*(-dy)
        #print 'dot2 is', dot2
        if dot2 <= 0.0:
            # then x2,y2 is the closest point
            return (self.x2, self.y2, math.sqrt( (xp-self.x2)**2 + (yp-self.y2)**2 ) )

        # so, the closest point is within the segment
        # I think taking the larger provides better accuracy (?)
        # but we'll just use dot1 for now...
        segLengthSq = float(dx*dx + dy*dy)

        #print 'dx,dy are', dx, dy
        #print 'segLengthSq is', segLengthSq

        # don't need to use trig functions, because it's already all there...
        cx = self.x1 + (dot1 * dx)/segLengthSq
        cy = self.y1 + (dot1 * dy)/segLengthSq
        d = math.sqrt( (cx-xp)**2 + (cy-yp)**2 )

        return (cx,cy,d)



    def intersectLine(self, x, y, dx, dy):
        """ this returns the intersection of the input line and self
        
            the line contains (x, y) + s(dx, dy) for all scalars s
            
            returns a tuple: (xi, yi, valid, r, s), where
            (xi, yi) is the intersection
            r is the scalar multiple along the "self" segment
            s is the scalar multiple along the input line
                valid == 0 if there are 0 or inf. intersections (invalid)
                valid == 1 if it has a unique intersection ON the segment    """

        ANGLE_TOLERANCE = 0.000001
        DET_TOLERANCE = 0.00000001

        # what do we do here?
        # we use a '1' to designate the segment's data
        #
        # I don't know if this really costs us any time... I doubt it...
        # but it could be removed, if it does
        x1 = self.x1
        y1 = self.y1
        dx1 = self.x2 - self.x1
        dy1 = self.y2 - self.y1

        # now the 'self' segment is (x1, y1) + r(dx1, dy1) (analogous to the line)
        #
        # we need to find the (typically unique) values of r and s
        # that will satisfy
        #
        # (x1, y1) + r(dx1, dy1) = (x, y) + s(dx, dy)
        #
        # which is the same as
        #
        #    [ dx1  -dx ][ r ] = [ x-x1 ]
        #    [ dy1  -dy ][ s ] = [ y-y1 ]
        #
        # whose solution is
        #
        #    [ r ] = _1_  [  -dy   dx ] [ x-x1 ]
        #    [ s ] = DET  [ -dy1  dx1 ] [ y-y1 ]
        #
        # where DET = (-dx1 * dy + dy1 * dx)
        #
        # if DET is too small, they're parallel
        # same as atan2(dy,dx) being the same as atan2(dy1,dx1)
        # if DET and the distance between them are both too small, they're coincident
        # ang  = math.atan2( dy, dx) + 0.42 % math.pi   # let the tricky cases be somewhere
        # ang1 = math.atan2(dy1,dx1) + 0.42 % math.pi   # other than 0.0 = 180.0
        # if math.fabs(ang - ang1) < ANGLE_TOLERANCE: return (0,0,0,0,0)
        #
        # even faster if we just check DET, but more sensitive to very short segments
        #
        DET = (-dx1 * dy + dy1 * dx)

        if math.fabs(DET) < DET_TOLERANCE: return (0,0,0,0,0)

        # now, the determinant should be OK
        DETinv = 1.0/DET

        # find the scalar amount along the "self" segment
        r = DETinv * (-dy  * (x-x1) +  dx * (y-y1))

        # return if we're off the segment
        #
        # we allow small deviations because it's more important 
        # not to escape out of rooms than to be 100% accurate
        if r < 0-DET_TOLERANCE or r > 1+DET_TOLERANCE: return (0,0,0,0,0)

        # find the scalar amount along the input line
        s = DETinv * (-dy1 * (x-x1) + dx1 * (y-y1))

        # return the average of both points (better numerically)
        # return ( (x1+r*dx1 + x+s*dx)/2.0 , (y1+r*dy1 + y+s*dy)/2.0 , 1, r, s )  

        # return the point along the segment (faster)
        return ( x1+r*dx1, y1+r*dy1, 1, r, s )

        
class Map:
    """ just a list of static items for now... """

    def __init__(self, filename):
        """ hi from Map's constructor """
 
        # here is the map of items
        self.items = []

        # here are the endpoints and other point features
        # a dictionary from world coordinates to a list of segments
        self.pointFeatures = {}

        # load in the file
        if filename != None:
            mapfile = open(filename, 'r')
        else:
            return # empty list, I guess...
    
        prevx = 0
        prevy = 0
        
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

                # create segment
                s = Seg(x1,y1,x2,y2)

                # record the first endpoint
                if not self.pointFeatures.has_key( (x1,y1) ):
                    self.pointFeatures[ (x1,y1) ] = [ s ]
                else:
                    self.pointFeatures[ (x1,y1) ].append(s)

                # same for the second endpoint
                if not self.pointFeatures.has_key( (x2,y2) ):
                    self.pointFeatures[ (x2,y2) ] = [ s ]
                else:
                    self.pointFeatures[ (x2,y2) ].append(s)

                # add segment to list of map items
                self.items.append(s)
                s.setColor(r,g,b)
                prevx = x2
                prevy = y2

            #print "map is now", self

        mapfile.close()

    def __str__(self):
        s = "\n"
        for item in self.items:
            s = s + str(item) + "\n"
        s = s + "\n" + str(self.pointFeatures)
        return s

    def numHits( self, x, y, thr ):
        # let's guess a point off the map
        xoff = -42424242.42
        yoff = -42424242.42
        # let's see how many intersections there are from
        # (x,y) to (xoff,yoff)
        xi, yi, count, d, item = self.rayTraceCount(x,y,xoff-x,yoff-y)
        return count


    def getExactImageFeatures(self, cx, cy, thd, f=1.0):
        """ returns a list of all features (and their world coords)
            that are visible in front of the image plane
        """
        # run through all of the point features
        # cast a ray FROM the point feature to the center (cx,cy)
        # see if it hits anything in the world before reaching the center
        # if so, it's blocked; if not blocked and on the same side as thd, it's visible
        # then project and add to image feature list

        imagefeatures = {}   # dictionary for all of the image features with
                             # imx as the key and global world coords as the value
                             # this value, in turn, can be used from self.pointFeatures
                             # to obtain the attached segments, if desired

        # the direction the camera is pointing
        costh = math.cos( thd * math.pi/180.0 )
        sinth = math.sin( thd * math.pi/180.0 )

        # for each world feature in the map
        for (wx,wy) in self.pointFeatures:
            # print "handling wx,wy=", wx, wy
            # is it on the correct side of the camera?
            # that is, does the vector have a positive dot product with
            # the camera direction?
            dx = wx-cx
            dy = wy-cy
            distanceAlongTheta = dx*costh + dy*sinth 
            # print "  distanceAlongTheta is", distanceAlongTheta
            if distanceAlongTheta <= 0.0:  continue

            # so it's on the correct side of the camera
            # now, we'll cast the ray (wx,wy) + s(dx,dy) through the world
            # to see what it hits... (note we have to point back to the optical center)
            xi, yi, valid, d, item = self.rayTrace(wx,wy,-dx,-dy)
            # print "rayTrace results are", self.rayTrace(wx,wy,-dx,-dy)
            if valid > 0 and d < math.sqrt(dx*dx + dy*dy): continue   # hit something too close!

            # ok, it did not hit anything between it and the camera
            # so, this feature is visible - now we project it
            # we already know the feature's distance along the optical axis = distanceAlongTheta
            # what is the signed distance perpendicular to the optical axis?
            #
            # I think cos(thd+90) = -sin(thd) and sin(thd+90) = cos(thd)
            # note that this yields an image coordinate system with origin
            # along the optical axis (OK) and positive to the left (so-so)
            distancePerpTheta = -sinth*dx + costh*dy
            # print "  distancePerpTheta is", distancePerpTheta

            # projecting to the single imx coordinate is then easy
            imx = f * distancePerpTheta / float(distanceAlongTheta)
            # print "  imx is", imx

            # load it into our dictionary
            imagefeatures[imx] = (wx,wy)

        # should this just set self.imagefeatures?
        return imagefeatures

    def getExactImage(self, cx, cy, thd, f=1.0):
        """ returns a list of segments (Seg) with y=0 (1d)
            to represent the image

            right now, the image endpoints are hardcoded to +-1000
        """
        # get the image features
        feats = self.getExactImageFeatures(cx, cy, thd, f)
        # we should sort them by their imx coordinate...
        # to do this, we will get all of the keys
        # sorted is not in 2.3
        sortedfeats = feats.keys()[:]
        sortedfeats.sort()
        #print 'sortedfeats is', sortedfeats
        # truncate (if needed) and add our endpoints
        LEFT_ENDPOINT = -1000.0
        RIGHT_ENDPOINT = 1000.0
        sortedfeats = [x for x in sortedfeats if x > -1000.0 and x < 1000.0]
        sortedfeats[:0] = [LEFT_ENDPOINT]
        sortedfeats[len(sortedfeats):] = [RIGHT_ENDPOINT]
        #print "sortedfeats is", sortedfeats
        # find half of the smallest gap between the features
        smallestgap = 0.5 * min( map( lambda x,y: y-x, sortedfeats[:-1], sortedfeats[1:] ) )
        # make sure it's at least small!
        smallestgap = min( smallestgap, 0.01 )
        #print "smallestgap is", smallestgap
        # now, sample the colors in between the features
        # project out through each feature with an offset of smallestgap
        raycastpoints = [x-smallestgap for x in sortedfeats[1:-1]]  # not endpoints
        # add one spot to the right of the last point
        raycastpoints.append(sortedfeats[-2]+smallestgap) # -2 because we don't want 1000.0
        #print "raycastpoints is", raycastpoints
        # cast these rays and get the resulting colors, then
        # combine those colors into a list of segments and return them
        # here is the return variable
        segments = []
        # first, the pixel-independent parts
        thr = thd*math.pi/180.0
        costhr = math.cos(thr)
        sinthr = math.sin(thr)
        imx = cx+f*costhr
        imy = cy+f*sinthr
        # print "imx,imy are", imx,imy
        # now, the pixel-dependent parts...
        # index into sortedfeats (remember that sortedfeats contains the real pixel locations)
        index = 1
        for raycastpoint in raycastpoints:
            # compute world-coordinate dx and dy offsets from cx and cy from the image coordinate
            # it should be the center of the image plus a bit along the image plane...
            dx = imx + raycastpoint*(-sinthr)   # cos(thd+90) = -sin(thd)
            dy = imy + raycastpoint*(costhr)    # sin(thd+90) = cos(thd)
            # print "dx,dy are", dx,dy
            result = self.rayTrace(cx,cy,dx-cx,dy-cy)
            xi, yi, valid, distance, item = result
            # ycoordinates are all 0
            segments.append( Seg(sortedfeats[index-1],0,sortedfeats[index],0,
                                 item.r, item.g, item.b) )   # use the color of the segment hit
            index = index + 1

        # print to check things
        #for s in segments:
            #print "segment:",s

        return segments



    def getSampledImage(self, x, y, thd, firstthd=-90, lastthd=90, numpix=180, f=1.0):
        """ returns a list of (r,g,b) color tuples

            seen from optical center x, y
            facing global direction thd (degrees)
            with focal length f
            with first pixel at an offset angle of "firstthd" degrees
            with last pixel at an offset angle of "lastthd" degrees
            with numpix pixels total, evenly (linearly) spaced

        """
        # here's the list of pixels that will be returned
        pixels = []
        # this is the color for a pixel if no objects are seen along a ray
        bkg_r = 42
        bkg_g = 42
        bkg_b = 42

        # we need to have at least one pixel!
        if numpix < 1:  numpix = 1

        # we need a positive focal length!
        if f == 0.0:  f = 1.0
        
        # "real" vision with a flat retina...
        # we need to loop over the pixels
        firstthr = (thd + firstthd) * math.pi/180.0
        p1x = x + f*math.cos(firstthr)
        p1y = y + f*math.sin(firstthr)
        lastthr = (thd + lastthd) * math.pi/180.0
        p2x = x + f*math.cos(lastthr)
        p2y = y + f*math.sin(lastthr)

        if numpix == 1:
            dx = 0
            dy = 0
        else:
            dx = (p2x - p1x)/float(numpix-1) # step size for x
            dy = (p2y - p1y)/float(numpix-1) # step size for y

        # loop over the pixels
        for i in range(numpix):
            px = p1x + i*dx
            py = p1y + i*dy
            # now we use this offset to define the ray to trace
            x,y,v,d,item = m.rayTrace(x,y,px-x,py-y)
            if v == 0:
                pixels.append( (bkg_r,bkg_g,bkg_b) )
            else:
                pixels.append( (item.r,item.g,item.b) )

    def findER1collisions(self, cx, cy, thr):
        """ this should check to see if any of the er1's segments
            intersect any of the world's segments
            it should return the point(s) of intersection
            it should set the velocity to zero etc.
        """
        # return the list of collisions
        collisions = []
        # consider each segment of the robot
        # choose one endpoint and ray trace in the world
        # see if the nearest intersection hits the segment itself
        # if so, add it to the "collisions" locations
        # listofvertices should be shared with findER1ranges, except no duplicates here
        # and, in particular, they should only be transformed once!
        # we really should have an ER1 object around!
        costhr = math.cos(thr)
        sinthr = math.sin(thr)
        # precompute the robot's side lengths, rounding down
        distances = [ 15, 20, 15, 11.18, 11.18 ]
        listofvertices = [(-5,-10),(-5,10),(10,10),(15,0),(10,-10)]
        transformedList = [ self.adjustPose( x, costhr, sinthr, cx, cy ) for x in listofvertices ]
        (x,y) = transformedList[-1]  # last one
        index = 0
        for (newx,newy) in transformedList:
            rayTraceResults = self.rayTrace(x,y,newx-x,newy-y)
            #print 'for side #', index, 'results are', rayTraceResults
            if distances[index] > rayTraceResults[3]: # we hit!
                #print "We hit!"
                collisions.append( (rayTraceResults[0], rayTraceResults[1]) )

            index = index + 1
            x, y = newx, newy   # slide down to the next side
        # if it does crash, it should set velocity to zero
        # and set some stall variable to true or 1
        return collisions

    def angleOffset(self, refangler, angler):
        """ doesn't use self, just finds the angle from
            which angler is offset from refangler, between
            -pi and pi
        """
        while angler < refangler-math.pi: angler += 2*math.pi
        while angler > refangler+math.pi: angler -= 2*math.pi
        return angler - refangler

    def findroombacollisions(self, rx, ry, thr, radius=16.5):
        """ this should check to see if the roomba at (rx,ry,thr)
            intersects any of the world's segments

            it should return the point(s) of intersection
            or perhaps whether the left, right, both, or no
            bump sensors are triggered (none if it's backing up...)

            the radius is in cm (16.5 cm for the roomba)
        """
        # return the list of collision _angles_, relative to
        # the robot's canonical coordinate system (forward == 0.0)
        collisions = []
        # find the distance from the center to each segment in the world
        #
        for s in self.items:  # for each segment in the map
            cx, cy, d = s.closestPoint( rx, ry )   # find the closest point
            if d <= radius:   # we hit!
                gthr = math.atan2(cy-ry,cx-rx)
                collisions.append( self.angleOffset( thr, gthr ) )

        return collisions


    def findER1ranges(self, cx, cy, thr):
        """ returns range sensor values given the robot's pose """
        # well, we really need some kind of sensor
        # object etc., but for now, we'll assume there
        # are five range sensors - one on each vertex
        # here they are (from Visualizer):
        # listofvertices = [(-5,-10),(-5,10),(10,10),(10,10),(15,0),(10,-10),(10,-10)]
        # directions in degrees = [ -90, 90,   90,     0,      0,      0,      -90 ]
        costhr = math.cos(thr)
        sinthr = math.sin(thr)
        R = []
        # number 0
        R.append( self.findRangeRadTuple( 
                    self.adjustPose( (-5,-10), costhr, sinthr, cx, cy ), 
                    thr - math.pi/2.0 ) )
        # number 1
        R.append( self.findRangeRadTuple( 
                    self.adjustPose( (-5,10), costhr, sinthr, cx, cy ), 
                    thr + math.pi/2.0 ) )
        # number 2
        R.append( self.findRangeRadTuple( 
                    self.adjustPose( (10,10), costhr, sinthr, cx, cy ), 
                    thr + math.pi/2.0 ) )
        # number 3
        R.append( self.findRangeRadTuple( 
                    self.adjustPose( (10,10), costhr, sinthr, cx, cy ), 
                    thr + 0.0 ) )
        # number 4
        R.append( self.findRangeRadTuple( 
                    self.adjustPose( (15,0), costhr, sinthr, cx, cy ), 
                    thr + 0.0 ) )
        # number 5
        R.append( self.findRangeRadTuple( 
                    self.adjustPose( (10,-10), costhr, sinthr, cx, cy ), 
                    thr + 0.0 ) )
        # number 6
        R.append( self.findRangeRadTuple( 
                    self.adjustPose( (10,-10), costhr, sinthr, cx, cy ), 
                    thr - math.pi/2.0 ) )
        return R



    def adjustPose(self, (x,y), costhr, sinthr, cx, cy):
        return ( (x*costhr - y*sinthr + cx, 
                  x*sinthr + y*costhr + cy) )

    def findRangeRadTuple(self, tuple, thr):
        x,y = tuple
        rayTraceResults = self.rayTrace(x,y,math.cos(thr),math.sin(thr))
        return rayTraceResults[3]

    def findRangeRad(self, x, y, thr):
        rayTraceResults = self.rayTrace(x,y,math.cos(thr),math.sin(thr))
        return rayTraceResults[3]

    def findRangeDeg(self, x, y, thd):
        thr = math.radians(thd)
        rayTraceResults = self.rayTrace(x,y,math.cos(thr),math.sin(thr))
        return rayTraceResults[3]


    def rayTrace(self, x, y, dx, dy):
        """ cast a ray out along (x,y)+s(dx,dy) with s>0 
            and return the closest item it hits, if any 

            returns
            (xi, yi, valid, distance, item)  """

        MIN_SCALAR = 0.0000001

        minsqrdist = 1.0e9
        closestItem = None
        closestxi = 0.0
        closestyi = 0.0
        finalvalid = 1         # we will set to 0 if no intersecting item is found

        for item in self.items:
            # assume everything is a Seg right now
            # print "  checking", item
            xi, yi, valid, r, s = item.intersectLine(x,y,dx,dy)
        # we use a small positive tolerance here so that
        # we can cast rays from an environmental surface without
        # simply returning that surface...
            if valid > 0 and s > MIN_SCALAR:
                sqrdist = (x-xi)**2 + (y-yi)**2
                if sqrdist < minsqrdist:
                    minsqrdist = sqrdist
                    closestItem = item
                    closestxi = xi
                    closestyi = yi

        if closestItem is None:
            finalvalid = 0

        return (closestxi, closestyi, finalvalid, math.sqrt(minsqrdist), closestItem)


    def rayTraceCount(self, x, y, dx, dy):
        """ cast a ray out along (x,y)+s(dx,dy) with s>0 
            and return the closest item it hits, if any 

            returns
            (xi, yi, valid, distance, item)  """

        MIN_SCALAR = 0.0000001

        minsqrdist = 1.0e9
        closestItem = None
        closestxi = 0.0
        closestyi = 0.0
        finalcount = 0  # = number of segments it hits...

        for item in self.items:
            # assume everything is a Seg right now
            # print "  checking", item
            xi, yi, valid, r, s = item.intersectLine(x,y,dx,dy)
        # we use a small positive tolerance here so that
        # we can cast rays from an environmental surface without
        # simply returning that surface...
            if valid > 0 and s > MIN_SCALAR:
                finalcount += 1
                sqrdist = (x-xi)**2 + (y-yi)**2
                if sqrdist < minsqrdist:
                    minsqrdist = sqrdist
                    closestItem = item
                    closestxi = xi
                    closestyi = yi

        return (closestxi, closestyi, finalcount, math.sqrt(minsqrdist), closestItem)
        
        



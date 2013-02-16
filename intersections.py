#
# intersections.py
#
# Python for finding line intersections
#   intended to be easily adaptable for line-segment intersections
#

import math

def intersectLines( pt1, pt2, ptA, ptB ): 
    """ this returns the intersection of Line(pt1,pt2) and Line(ptA,ptB)
        
        returns a tuple: (xi, yi, valid, r, s), where
        (xi, yi) is the intersection
        r is the scalar multiple such that (xi,yi) = pt1 + r*(pt2-pt1)
        s is the scalar multiple such that (xi,yi) = pt1 + s*(ptB-ptA)
            valid == 0 if there are 0 or inf. intersections (invalid)
            valid == 1 if it has a unique intersection ON the segment    """

    DET_TOLERANCE = 0.00000001

    # the first line is pt1 + r*(pt2-pt1)
    # in component form:
    x1, y1 = pt1;   x2, y2 = pt2
    dx1 = x2 - x1;  dy1 = y2 - y1

    # the second line is ptA + s*(ptB-ptA)
    x, y = ptA;   xB, yB = ptB;
    dx = xB - x;  dy = yB - y;

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
    #
    DET = (-dx1 * dy + dy1 * dx)

    if math.fabs(DET) < DET_TOLERANCE: return (0,0,0,0,0)

    # now, the determinant should be OK
    DETinv = 1.0/DET

    # find the scalar amount along the "self" segment
    r = DETinv * (-dy  * (x-x1) +  dx * (y-y1))

    # find the scalar amount along the input line
    s = DETinv * (-dy1 * (x-x1) + dx1 * (y-y1))

    # return the average of the two descriptions
    xi = (x1 + r*dx1 + x + s*dx)/2.0
    yi = (y1 + r*dy1 + y + s*dy)/2.0
    return ( xi, yi, 1, r, s )

def in_line(point, line_segment):
    start = line_segment[0]
    end = line_segment[1]
    x = point[0]
    y = point[1]
    
    if start[0] == end[0]:
   #if the line is vertical...
        if start[1] < end[1]:
       #if the line's start point is below the end point...
            if y <= end[1] and y >= start[1]:
           #if the robot is between the start and end point...
                if start[0] - 1 < x < start[0] + 1 or \
                    end[0] - 1 < x < end[0] + 1:
                    return True
                else: return False
            else: return False
            
        else:
       #if the line's end point is below the start point...
            if y >= end[1] and y <= start[1]:
           #if the robot is between the start and end point...
                if start[0] - 1 < x < start[0] + 1 or \
                    end[0] - 1 < x < end[0] + 1:
                    return True
                else: return False
            else: return False
    
    if start[1] == end[1]:
   #if the line is horizontal...
        if start[0] < end[0]:
       #if the line's start point is to the left of the end point...
            if x <= end[0] and x >= start[0]:
           #if the robot is between the start and end point...
                if start[1] - 1 < y < start[1] + 1 or \
                    end[1] - 1 < y < end[1] + 1:
                    return True
                else: return False
            else: return False
            
        else:
       #if the line's start point is to the right of the end point...
            if x >= end[0] and x <= start[0]:
           #if the robot is between the start and end point...
                if start[1] - 1 < y < start[1] + 1 or \
                    end[1] - 1 < y < end[1] + 1:
                    return True
                else: return False
            else: return False

def in_line2(point, start, end):
    x = point[0]
    y = point[1]
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]
    if x1 <= x2:
    #if the start is to the left of the end
        if y1 <= y2:
        #if the start is below the end
            if x1 <= x <= x2 and y1 <= y <= y2:
                return True
            else: return False
        if y1 >= y2:
        #if the start is above the end
            if x1 <= x <= x2 and y1 >= y >= y2:
                return True
            else: return False
    if x1 >= x2:
    #if the start is to the right of the end
        if y1 <= y2:
        #if the start is below the end
            if x1 >= x >= x2 and y1 <= y <= y2:
                return True
            else: return False
        if y1 >= y2:
        #if the start is above the end
            if x1 >= x >= x2 and y1 >= y >= y2:
                return True
            else: return False

def in_line3(point, start, end):
    x = point[0]
    y = point[1]
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]
    
    if x1 <= x2:
   #if the start is to the left of the end...
        if x1 - 1 <= x <= x2 + 1:
       #if the point is in the domain of the line segment...
            if y1 - 1 <= y <= y2 + 1 or y1 + 1 >= y >= y2 - 1:
           #if the point is in the range of the line segment
               return True
            else: return False
        else: return False
        
    if x1 >= x2:
   #if the start is to the right of the end...
        if x1 + 1 >= x >= x2 - 1:
       #if the point is in the domain of the line segment...
            if y1 - 1 <= y <= y2 + 1 or y1 + 1 >= y >= y2 - 1:
           #if the point is in the range of the line segment                
               return True
            else: return False
        else: return False
            
    
def testIntersection( pt1, pt2, ptA, ptB ):
    """ prints out a test for checking by hand... """
    print "Line segment #1 runs from", pt1, "to", pt2
    print "Line segment #2 runs from", ptA, "to", ptB

    result = intersectLines( pt1, pt2, ptA, ptB )
    print "    Intersection result =", result
    print


if __name__ == "__main__":

  pt1 = (10,10)
  pt2 = (20,20)

  pt3 = (10,20)
  pt4 = (20,10)

  pt5 = (40,20)

  testIntersection( pt1, pt2, pt3, pt4 )
  testIntersection( pt1, pt3, pt2, pt4 )
  testIntersection( pt1, pt2, pt4, pt5 )

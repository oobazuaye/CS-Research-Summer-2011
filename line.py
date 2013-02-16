import sys

def line():
    print "Enter point 1"
    x1=input("Enter x:")
    y1=input("Enter y:")
    print "Enter point 2"
    x2=input("Enter x:")
    y2=input("Enter y:")
    dx=x2-x1
    dy=y2-y1
    m=dy/dx    #slope
    print "The equation of the line is- y-%s=%s(x-%s)"%(y1,m,x1)

def line2(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    if x2 - x1 == 0:
        return ["vertical", x1]
    slope = 1. * (y2 - y1) / (x2 - x1)
    intercept = slope * -x1 + y1
    sys.stdout.write('The line is: ')
    sys.stdout.write("Y = ")
    sys.stdout.write(slope)
    sys.stdout.write("X + ")
    sys.stdout.write(intercept)
    return [slope, intercept]

def in_line(point, line_segment):
    start = line_segment[0]
    end = line_segment[1]
    x = point[0]
    y = point[1]
    if point == start or point == end:
   #if the point is the start or end point
        return True
    
    if start[0] == end[0]:
   #if the line is vertical...
        return close_point == (start[0], y)
        
    if start[1] == end[1]:
   #if the line is horizontal...
        return point == (x, start[1])
                
            
    

def equation_solver(equation1, equation2):
    slope1 = equation1[0]
    intercept1 = equation1[1]
    slope2 = equation2[0]
    intercept2 = equation2[1]
    intercept_diff = intercept1 - intercept2
    slope_diff = slope2 - slope1
    if slope_diff == 0:
        print "These lines do not intersect."
        return 0
    x = intercept_diff / slope_diff
    y = slope1 * x + intercept1
    return [x, y]

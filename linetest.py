import turtle
from math import *
screen = turtle.Screen()

thr = 45
turtle.setpos(turtle.xcor() + 50*cos(radians(thr)),
              turtle.ycor() + 50*sin(radians(thr)))

turtle.exitonclick()

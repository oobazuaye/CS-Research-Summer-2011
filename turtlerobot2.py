from turtle import *
screen = Screen()

turnAngle = 15
stepDistance = 1
running1 = True
running2 = True
def f():
    global running1
    global running2
    running1 = True
    running2 = False
    #if running1 == True:
    while running1:
        forward(stepDistance)
        #screen.ontimer(f, t=500)

def b():
    global running1
    global running2
    running1 = False
    running2 = True
    while running2:
        backward(stepDistance)
        #screen.ontimer(b, t=500)

def e():
    global running1
    global running2
    running1 = False
    running2 = False
    print position()

def q():
    global running1
    global running2
    running1 = False
    running2 = False
    bye()
    
def l():
    left(turnAngle)

def r():
    right(turnAngle)
    

screen.onkey(f, "w")
screen.onkey(b, "s")
screen.onkey(l, "a")
screen.onkey(r, "d")
screen.onkey(e, "e")
screen.onkey(q, "q")
screen.listen()
done()

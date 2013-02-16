# robot_lab.py

from arduinoController import *

the_port = getPort(4) # number is diff. for each machine
# check controlpanel/system/devices/COM for yours...
# and you need to subtract one!
#close(the_port) on Windows, it seems you need to close
# BEFORE re-loading the file... run close() !
ser = init(the_port)


wait(2) # 2 second wait
# setup a servo motor on digital pin 12
attachServo( 1, 13 )

import time

def close():
    ser.close()

# your code goes here:
def LED_test():
    setLED( True )  
    time.sleep(0.5)
    setLED( False )

def blinkn(n):
    for num in range(n):
        blink()
        wait(1)

def allon():
    for num in range(2,13):
        output(num, 1)

def alloff():
    for num in range(2,13):
        output(num, 0)

def outputAll( L ):
    lightPosition = 2
    for light in L:
        output(lightPosition, light)
        lightPosition+=1

def vegasLights(n):
    L = [0,1,0,1,0,1,0,1,0, 1, 0]
    for num in range(n):
        L = [1 - num for num in L]
        outputAll(L)
        wait(1)

def hypnotize():
    speed = 0.75
    for num in range(15):
        for num in range(2,13):
            output(num, 1)
            wait(speed)
            output(num, 0)
            output(num+1, 1)
        L = range(2, 13)
        L.reverse()
        speed = speed*.75
        for num in L:
            output(num, 1)
            wait(speed)
            output(num, 0)
            output(num-1, 1)
        speed = speed*.75
    
def lights(analog_reading):
    alloff()
    startnum = 0
    if analog_reading <= 0:
        alloff()
    if analog_reading > 1000:
        allon()
    else:
        LEDnum = analog_reading / 100
        if LEDnum == 0: output(2, 1)
        else: outputAll([ 1 for num in range(LEDnum)])

def lightMeter(n):
    if n == 0: return
    else:
        analog_reading = getADports()[0]
        print "The analog reading is: ", analog_reading
        lights(analog_reading)
        wait(2)
        alloff()
        lightMeter(n-1)

def lightMotor():
    analog_reading = getADports()[0]
    speed = analog_reading / 100
    if speed == 0:
        return
    else:
        servoOn(1, speed, True)
        wait(2)
        lightMotor()
    

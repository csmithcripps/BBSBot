import board
import time
import busio
import displayio
import digitalio
import terminalio
from adafruit_display_text import label
from digitalio import DigitalInOut, Direction, Pull
import pulseio
#import adafruit_hcsr04
import adafruit_lis3dh
#sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.ECHO, echo_pin=board.TRIGGER)
import bbsRobot

rb = bbsRobot.bbsRobot()

#i2c.try_lock()

#speaker =  pulseio.PWMOut(board.SPEAKER, frequency=5000, duty_cycle= 2 ** 15)


board.DISPLAY.brightness = 0
rb.displayBBS()
while True:
    rb.Wait_For_Button()
    rb.Motors_Turn(50)        
    rb.displayBBS("ROBOT_TURN:\nRIGHT AT HALF SPEED")

    rb.Wait_For_Button()
    rb.Motors_Turn(-50)
    rb.displayBBS("ROBOT_TURN:\nLEFT AT HALF SPEED")

    

    rb.Wait_For_Button()
    rb.Motors_Turn(0)
    rb.displayBBS()
        

    #i2c.unlock()
    #continue
#for x in range(150, 170):
#    for y in range(100, 110):
#        bitmap[x, y] = 1

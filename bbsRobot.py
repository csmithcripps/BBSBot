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

class bbsRobot:
    def __init__(self):
        #Set up Switch and block until pressed
        self.sw1 = digitalio.DigitalInOut(board.SWITCH1)
        self.sw1.direction = digitalio.Direction.INPUT
        #sw.pull = digitalio.Pull.UP
        #Initialise I2C
        self.i2c=  busio.I2C(board.SCL, board.SDA)

        #Initialise accellerometer interrupt
        self.int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)  # Set this to the correct pin for the interrupt!

        #Init Radio
        self.radio = digitalio.DigitalInOut(board.RADIO)
        self.radio.direction = Direction.OUTPUT
        self.radio.value = True # false is at mode

        #Init Serial Communication (To Computer?)
        self.uart = busio.UART(board.TX, board.RX)

        #Connect Accelerometer via I2C
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(self.i2c, int1=self.int1)

        #Init Motors
        self.m1a =  pulseio.PWMOut(board.M1B, frequency=1000, duty_cycle= 0x0)
        #m1a = DigitalInOut(board.M1A)
        #m1a.direction = Direction.OUTPUT
        #m1a.value = True

        #m1b = pulseio.PWMOut(board.M1B, frequency=5000, duty_cycle=0xffff)
        self.m1b = DigitalInOut(board.M1A)
        self.m1b.direction = Direction.OUTPUT
        self.m1b.value = False


        self.m2a = pulseio.PWMOut(board.M2A, frequency=1000, duty_cycle=0x0) #
        #m2a = DigitalInOut(board.M2A)
        #m2a.direction = Direction.OUTPUT
        #m2a.value = True
        #m2b = pulseio.PWMOut(board.M2B, frequency=25000, duty_cycle=0) #
        self.m2b =DigitalInOut(board.M2B)
        self.m2b.direction = Direction.OUTPUT
        self.m2b.value = False
        
        self.display = board.DISPLAY
        self.display_y0 = 11

        self.bitmap_file = open("/BBS.bmp", "rb")

    '''
    Motors_Forward
    Moves the robot forward at a given speed as a percentage of a given duty cycle.
    Defaults to full speed
    @params:
        speed:          Speed as a percentage defaults to 100
        duty_cycle:     Duty Cycle for motors defaults to 0xffff --> FULL SPEED

    '''
    def Motors_Forward(self, speed=100, duty_cycle=0xffff):        
        self.m1a.duty_cycle = (speed/100)*duty_cycle
        self.m2a.duty_cycle = (speed/100)*duty_cycle
    
    
    
    '''
    Motors_Stop
    Sets the motor duty cycles to 0, stopping the motors
    NOTE: No breacking occures

    '''
    def Motors_Stop(self):       
        self.m1a.duty_cycle = 0
        self.m2a.duty_cycle = 0

    '''
    Motors_Turn
    Makes the robot turn, with a turn rate between 100 and -100, where positive is a right turn
    and negative is a left turn. 
    NOTE:   Is not capable of turning on the spot as it's max is turning about one wheel as an anchor.
            Stops if no turnRate is given
            Defaults to stopped
    @params:
        turnRate:       Speed of turn / Sharpness of turn
        speed:          Speed as a percentage defaults to 100
        duty_cycle:     Duty Cycle for motors defaults to 0xffff --> FULL SPEED

    '''
    def Motors_Turn(self, turnRate=0, speed=100, duty_cycle=0xffff):               
        if(turnRate > 0):
            lm = (speed/100)*duty_cycle
            rm = ((100 - turnRate)/100)*(speed/100)*duty_cycle
        elif(turnRate<0):
            turnRate = abs(turnRate)
            lm = ((100 - turnRate)/100)*(speed/100)*duty_cycle
            rm = (speed/100)*duty_cycle
        else:
            lm = 0
            rm = 0

        self.m1a.duty_cycle = int(lm)
        self.m2a.duty_cycle = int(rm)
        
        
    '''
    Wait_For_Button
    Blocks code until button press

    '''
    def Wait_For_Button(self):
        while self.sw1.value == True:
            pass
        time.sleep(1)

    '''
    displayText
    Displays text on screen
    Default display of "BBS"
    @params
        text:       Text to display
        x:          x position of text
                        default: 0
        y:          y position of text relative to top of screen
                        default: 0
        color:      text colout
                        default: White (0xFFFFFF)
        font:       text font
                        default: terminalio.FONT

    '''
    def displayText(self, text="BBS", x=0, y=0, color=0xFFFFFF, font=terminalio.FONT):       
        text_area = label.Label(font, text=text, color=color)
        text_area.height = 100
        # Set the location
        text_area.x = x
        text_area.y = self.display_y0 + y
        # Show it
        self.display.show(text_area)

    '''
    displayBBS
    Displays BBS logo and text on screen
    Default text  "BBS:\nBUILDING BLOCK STUDIO"
    @params
        text:       Text to display
        x:          x position of text
                        default: 0
        y:          y position of text relative to top of screen
                        default: 0
        color:      text colout
                        default: White (0xFFFFFF)
        font:       text font
                        default: terminalio.FONT

    '''
    def displayBBS(self, text="BBS:\nBUILDING BLOCK STUDIO", x=0, y=60, color=0xFFFFFF, font=terminalio.FONT):
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(self.bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group

        # Set text, font, and color      
        text_area = label.Label(font, text=text, color=color)
        text_area.height = 2
        # Set the location
        text_area.x = x
        text_area.y = self.display_y0 + y

        group.append(text_area)
        group.append(tile_grid)

        self.display.show(group)
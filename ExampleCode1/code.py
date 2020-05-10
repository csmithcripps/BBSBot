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


#Set up Switch and block until pressed
sw = digitalio.DigitalInOut(board.SWITCH1)
sw.direction = digitalio.Direction.INPUT
#sw.pull = digitalio.Pull.UP
while sw.value == True:
    pass

#Initialise I2C
i2c=  busio.I2C(board.SCL, board.SDA)

#Initialise accellerometer interrupt
int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)  # Set this to the correct pin for the interrupt!

#Init Radio
radio = digitalio.DigitalInOut(board.RADIO)
radio.direction = Direction.OUTPUT
radio.value = True # false is at mode

#Init Serial Communication (To Computer?)
uart = busio.UART(board.TX, board.RX)

#Connect Accelerometer via I2C
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

#i2c.try_lock()

#speaker =  pulseio.PWMOut(board.SPEAKER, frequency=5000, duty_cycle= 2 ** 15)


m1a =  pulseio.PWMOut(board.M1B, frequency=1000, duty_cycle= 0xffff)
#m1a = DigitalInOut(board.M1A)
#m1a.direction = Direction.OUTPUT
#m1a.value = True

#m1b = pulseio.PWMOut(board.M1B, frequency=5000, duty_cycle=0xffff)
m1b = DigitalInOut(board.M1A)
m1b.direction = Direction.OUTPUT
m1b.value = False


m2a = pulseio.PWMOut(board.M2A, frequency=1000, duty_cycle=0xffff) #
#m2a = DigitalInOut(board.M2A)
#m2a.direction = Direction.OUTPUT
#m2a.value = True
#m2b = pulseio.PWMOut(board.M2B, frequency=25000, duty_cycle=0) #
m2b =DigitalInOut(board.M2B)
m2b.direction = Direction.OUTPUT
m2b.value = False

display = board.DISPLAY

board.DISPLAY.brightness = 1

with open("/BBS.bmp", "rb") as bitmap_file:

    # Setup the file as the bitmap data source
    bitmap = displayio.OnDiskBitmap(bitmap_file)

    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

    # Create a Group to hold the TileGrid
    group = displayio.Group()

    # Add the TileGrid to the Group
    group.append(tile_grid)

    # Add the Group to the Display
    display.show(group)

    time.sleep(1)

    # Set text, font, and color
    text = "         "
    font = terminalio.FONT

    color = 0x00FFFF

    # Create the test label
    text_area = label.Label(font, text=text, color=color)
    text_area.height = 100


    # Set the location
    text_area.x = 20
    text_area.y = 80

    # Show it
    display.show(text_area)

    # Draw even more pixels
    #display.auto_brightness = False
    #display.auto_refresh = True
    lis3dh.set_tap(2, 90)
    while True:
        try:

            #uart.write(b'AT+BAUD\r\n')
            data = uart.read(32)
            print(data)
            #print(i2c.scan())
            #print((sonar.distance,))
            #text_area.text = str(sonar.distance)
            #display.show(text_area)
            #time.sleep(0.4)
            #x, y, z = lis3dh.acceleration
            #print(x, y, z)

            if lis3dh.tapped:
                print("Tapped!")
                m1a.duty_cycle = 0
                m2a.duty_cycle = 0
                time.sleep(3)
                m1a.duty_cycle = 0xffff
                m2a.duty_cycle = 0xffff
        except RuntimeError:
            continue
        
        # display.show(text_area)
        time.sleep(0.1)

    #i2c.unlock()
    #continue
#for x in range(150, 170):
#    for y in range(100, 110):
#        bitmap[x, y] = 1

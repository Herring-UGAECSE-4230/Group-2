#imports for file
import time
import RPi.GPIO as GPIO
from datetime import datetime

# Defining GPIO mode and input/output
GPIO.setmode(GPIO.BCM)

# X-Values (Horizontal) Mapping
GPIO.setup(18, GPIO.OUT) # Yellow Wire X1
GPIO.setup(23, GPIO.OUT) # Orange Wire X2
GPIO.setup(24, GPIO.OUT) # Brown Wire X3
GPIO.setup(25, GPIO.OUT) # Red Wire X4

xPins = [18,23,24,25]

# Y-Values (Vertical) Mapping
GPIO.setup(12, GPIO.IN) # Black Wire Y1
GPIO.setup(16, GPIO.IN) # White Wire Y2
GPIO.setup(20, GPIO.IN) # Gray Wire Y3
GPIO.setup(21, GPIO.IN) # Blue Wire Y4

yPins = [12,16,20,21]
# Clock Setup
Clk1 = 22
Clk2 = 27
Clk3 = 17
Clk4 = 4

# Seven Segment Setup
E = 26
D = 19
C = 13
DP = 6
G = 5
F = 11
A = 10
B = 9

LED = 8
GPIO.setup([Clk1,Clk2,Clk3,Clk4], GPIO.OUT) # Clocks


GPIO.setup([E,D,C,DP,G,F,A,B,LED], GPIO.OUT) # E

count = 0
enable = True
global position
position = 1
last1 = []
last2 = []
last3 = []
last4 = []


#decided to rework our ssd code for clock to simplfy some of the logic
seven_segment_map = {
    '0': [1, 1, 1, 1, 1, 1, 0],
    '1': [0, 1, 1, 0, 0, 0, 0],
    '2': [1, 1, 0, 1, 1, 0, 1],
    '3': [1, 1, 1, 1, 0, 0, 1],
    '4': [0, 1, 1, 0, 0, 1, 1],
    '5': [1, 0, 1, 1, 0, 1, 1],
    '6': [1, 0, 1, 1, 1, 1, 1],
    '7': [1, 1, 1, 0, 0, 0, 0],
    '8': [1, 1, 1, 1, 1, 1, 1],
    '9': [1, 1, 1, 0, 0, 1, 1],
    'A': [1, 1, 1, 0, 1, 1, 1],
    'B': [0, 0, 1, 1, 1, 1, 1],
    'C': [1, 0, 0, 1, 1, 1, 0],
    'D': [0, 1, 1, 1, 1, 0, 1],
}


#waits for user input on keypad and flashes the seven seg
def flash(Clk):
    GPIO.output(Clk, GPIO.LOW)
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.HIGH)
    GPIO.output(Clk, GPIO.HIGH)
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
    GPIO.output(Clk, GPIO.HIGH)
# Resets SSD Display
def resetGPIO(Clk):
    GPIO.output(Clk, GPIO.HIGH)
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
    GPIO.output(Clk, GPIO.LOW)
    
def loadLast(Clk, *last):
    GPIO.output(*last, GPIO.HIGH)
    GPIO.output(Clk, GPIO.HIGH)
    GPIO.output(*last, GPIO.LOW)
    GPIO.output(Clk, GPIO.LOW)
        
# Conditional implementation of keypad changed to look up table to make it easier for logic
def read_keypad():

    #Look up table for Keypad
    key_map_lut = [
        "1", "2", "3", "A",
        "4", "5", "6", "B",
        "7", "8", "9", "C",
        "*", "0", "#", "D"
    ]

    #just learned enumerate from a classmate this is game changing
    for row, rowPins in enumerate(xPins):
        GPIO.output(rowPins, GPIO.HIGH)
        #I am about to only use enumerate forever no more i++ so long loser (-_-)7
        for col, colPins in enumerate(yPins):
            #checks if high
            if GPIO.input(colPins):
                #time sleep for a little debounce
                time.sleep(0.1)  
                if GPIO.input(colPins):
                    GPIO.output(rowPins, GPIO.LOW)
                    #returns the corresponding map
                    return key_map_lut[row * 4 + col]
        GPIO.output(rowPins, GPIO.LOW)

        GPIO.output(row, GPIO.LOW)

def loadDisplay(value):
    print(WIP)

while True:
    if(GPIO.input(yPins)):
       value = read_keypad()
       loadDisplay(value)
    else:
        flash()
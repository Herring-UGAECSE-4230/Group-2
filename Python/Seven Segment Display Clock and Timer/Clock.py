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
position = 1
last = []



#decided to rework our ssd code for clock to simplfy some of the logic
#is a table that contains the each seg and the corresponding value of gpio output to display
seven_segment_map = {
    '0': [(A,1), (B,1), (C,1), (D,1), (E,1), (F,1), (G,0)],
    '1': [(A,0), (B,1), (C,1), (D,0), (E,0), (F,0), (G,0)],
    '2': [(A,1), (B,1), (C,0), (D,1), (E,1), (F,0), (G,1)],
    '3': [(A,1), (B,1), (C,1), (D,1), (E,0), (F,0), (G,1)],
    '4': [(A,0), (B,1), (C,1), (D,0), (E,0), (F,1), (G,1)],
    '5': [(A,1), (B,0), (C,1), (D,1), (E,0), (F,1), (G,1)],
    '6': [(A,1), (B,0), (C,1), (D,1), (E,1), (F,1), (G,1)],
    '7': [(A,1), (B,1), (C,1), (D,0), (E,0), (F,0), (G,0)],
    '8': [(A,1), (B,1), (C,1), (D,1), (E,1), (F,1), (G,1)],
    '9': [(A,1), (B,1), (C,1), (D,0), (E,0), (F,1), (G,1)],
    'A': [(A,1), (B,1), (C,1), (D,0), (E,1), (F,1), (G,1)],
    'B': [(A,0), (B,0), (C,1), (D,1), (E,1), (F,1), (G,1)],
    'C': [(A,1), (B,0), (C,0), (D,1), (E,1), (F,1), (G,0)],
    'D': [(A,0), (B,1), (C,1), (D,1), (E,1), (F,0), (G,1)],
}


#waits for user input on keypad and flashes the seven seg
def flash(Clk):
    GPIO.output(Clk, GPIO.LOW)
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.HIGH)
    GPIO.output(Clk, GPIO.HIGH)
    time.sleep(.2)              #slows it down so we can see it flash
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
    GPIO.output(Clk, GPIO.HIGH)
# Resets SSD Display
def resetGPIO(Clk):
    GPIO.output(Clk, GPIO.HIGH)
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
    GPIO.output(Clk, GPIO.LOW)
    
def loadLast():
    loadDisplay(Clk1,last[0])
    loadDisplay(Clk1,last[1])
    loadDisplay(Clk1,last[2])
    loadDisplay(Clk1,last[3])
    print("loads last")
# Conditional implementation of keypad changed to look up table to make it easier for logic
def read_keypad():

    #Look up table for Keypad
    key_lut = [
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
                    #returns the corresponding values based on the map
                    return key_lut[row * 4 + col]
        GPIO.output(rowPins, GPIO.LOW)

        GPIO.output(row, GPIO.LOW)

def loadDisplay(Clk, value):

    position = position + 1 
    print("loading" + value + "into seven seg " + position)
    outputs = seven_segment_map[value]
    for pin, state in outputs:
        GPIO.output(Clk, GPIO.LOW)
        GPIO.output(pin, state)
        GPIO.output(Clk, GPIO.HIGH)
   



while True:
    GPIO.output([Clk1,Clk2,Clk3,Clk4], GPIO.LOW)
    if(GPIO.input(yPins)):
       value = read_keypad()
       if value == '#':
            if(count % 2 == 0):
                enable = False
            else:
                enable = True
                loadLast()
       else:
        if position == 1:
            loadDisplay(Clk1, value)
            last[0] = value
        elif position == 2:
            loadDisplay(Clk2, value)
            last[1] = value
        elif position == 3:
            loadDisplay(Clk3, value)
            last[2] = value
        elif position == 4:   
            loadDisplay(Clk4, value)
            last[3] = value
    else:
        if position == 1:
            flash(Clk1)
        elif position == 2:
            flash(Clk2)
        elif position == 3:
            flash(Clk3)
        elif position == 4:
            flash(Clk4)
        else:
            time.sleep(60)
            last[3] = last[3] + 1
            if last[3] == 10:
                last[2] = last [2] + 1
                last[3] = 0
                if last [2] == 6:
                    last [1] = last[1] + 1
                    last [2] = 0
                    if last [0] == 1 and last [1] == 2:
                        last [0] = 0
                        last [1] = 1
                    elif last [1] == 10:
                        last [0] = last [0] + 1
                        last [1] = 0
            loadLast()
    time.sleep(.1)
# Imports for file
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
last = [0,0,0,0]
escape = 0
global now
now = time.time()


# Maps the segments on the SSD to the corresponding keypad values
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
    'X': [(A,0), (B,0), (C,0), (D,0), (E,0), (F,0), (G,0)],
}

# Waits for user input on keypad and flashes the SSD
def flash(Clk):
    global now
    print ("flashing")
    if(now + 0.12 > time.time()):
        GPIO.output(Clk, GPIO.LOW)
        GPIO.output([A,B,C,D,E,F,G,DP], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
    else:

        GPIO.output(Clk, GPIO.LOW)
        GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
        GPIO.output(Clk, GPIO.HIGH)
        now = time.time()

# Resets SSD Display
def resetGPIO(Clk):
    GPIO.output(Clk, GPIO.HIGH)
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
    GPIO.output(Clk, GPIO.LOW)
    
def loadLast():
    loadDisplay(Clk1,str(last[0]))
    loadDisplay(Clk2,str(last[1]))
    loadDisplay(Clk3,str(last[2]))
    loadDisplay(Clk4,str(last[3]))
    print("loads last")

# Conditional implementation of keypad changed to look up table to make it easier for logic
def read_keypad():
    # Look up table for Keypad
    key_lut = [
        "1", "2", "3", "A",
        "4", "5", "6", "B",
        "7", "8", "9", "C",
        "*", "0", "#", "D"
    ]
    
    for row, rowPins in enumerate(xPins):
        GPIO.output(rowPins, GPIO.HIGH)
        for col, colPins in enumerate(yPins):
            # Checks if high
            if GPIO.input(colPins):
                time.sleep(0.1)
                if GPIO.input(colPins):
                    GPIO.output(rowPins, GPIO.LOW)
                    return key_lut[row * 4 + col]
        GPIO.output(rowPins, GPIO.LOW)
        

def loadDisplay(Clk, value):
    global position
    position = position + 1 
    print("loading")
    outputs = seven_segment_map[value]
    for pin, state in outputs:
        GPIO.output(Clk, GPIO.LOW)
        GPIO.output(pin, state)
        GPIO.output(DP, GPIO.LOW)
        GPIO.output(Clk, GPIO.HIGH)
        
def startMode():
    loadDisplay(Clk1, 'X')
    loadDisplay(Clk2, 'X')
    loadDisplay(Clk3, 'X')
    loadDisplay(Clk4, 'X')

def autoClock():
    PM = False
    GPIO.output([Clk1, Clk2, Clk3, Clk4], GPIO.LOW)
    now = datetime.now()
     
    # Retrieves the hour and subtracts 12 to remain in 12-hour format 
    hour = now.hour
    if hour > 12:
        hour -= 12
        PM = True
    else:
        PM = False

    # Retrieves the minute
    minute = now.minute

    # Format hour and minute to 2-digit string
    hour = '{0:02d}'.format(hour)
    minute = '{0:02d}'.format(minute)

    # Returns the hour and the minute as 2 digit strings
    return hour, minute
  
while True:
    escape = 0
    GPIO.output([Clk1,Clk2,Clk3,Clk4], GPIO.LOW)
    value = read_keypad()
    print(value)
    if(value):
        print("reading")

        # This runs the automatic clock
        if value == 'A':
            while True:
                hourDigit, minuteDigit = autoClock()
                # Separates the two digit strings into a single digit
                hourDigit.split()
                minuteDigit.split()
                # Loads corresponding displays with single digits
                loadDisplay(Clk1, hourDigit[0])
                loadDisplay(Clk2, hourDigit[1])
                loadDisplay(Clk3, minuteDigit[0])
                loadDisplay(Clk4, minuteDigit[1])
                value = read_keypad()
                if value == 'B':
                    break
        
        elif value == 'B':
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
            now = time.time()
            switch = now + 60
            while(time.time() < switch):
                # This turns the clock on and off
                value = read_keypad()
                if value == '#':
                    if(count % 2 == 0):
                        enable = False
                        startMode()
                        count = count + 1
                        time.sleep(0.05)
                    else:
                        enable = True
                        loadLast()
                        count = count + 1
                        time.sleep(0.05)
                        continue
                
                elif(value == 'B'):
                    escape = escape + 1
                    if(escape == 3):
                        startMode()
                        escape = 0
                        position = 1
                    break
                    
            last[3] = int(last[3]) + 1
            if int(last[3]) == 10:
                last[2] = int(last [2]) + 1
                last[3] = 0
                if int(last [2]) == 6:
                    last [1] = int(last[1]) + 1
                    last [2] = 0
                    if int(last [0]) == 1 and int(last [1]) == 3:
                        last [0] = 0
                        last [1] = 1
                    elif int(last [1]) == 10:
                        last [0] = int(last [0]) + 1
                        last [1] = 0
            loadLast()
    time.sleep(0.1)

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

# Set up pins and clocks as list
GPIO.setup([Clk1,Clk2,Clk3,Clk4], GPIO.OUT) # Clocks
GPIO.setup([E,D,C,DP,G,F,A,B,LED], GPIO.OUT) # E

# Initialize variables
count = 0
enable = True
global position
position = 1
last = [0,0,0,0]
global now
now = time.time()
global interrupt
interrupt = False
global countb
countb = 0

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

# Sets the seven segment display to "0000"
def startMode():
    global position
    loadDisplay(Clk1, '0')
    loadDisplay(Clk2, '0')
    loadDisplay(Clk3, '0')
    loadDisplay(Clk4, '0')
    position = 1

# Turns the seven segment display off
def disable():
    global position
    position = 1
    loadDisplay(Clk1, 'X')
    loadDisplay(Clk2, 'X')
    loadDisplay(Clk3, 'X')
    loadDisplay(Clk4, 'X')
    position = 1
    
# Waits for user input on keypad and flashes the SSD
def flash(Clk):
    global now
    print ("flashing")
    if(now + 0.2 > time.time()):
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

# Loads the last stored keypad value to the corresponding SSD    
def loadLast():
    global position
    position = 1
    loadDisplay(Clk1,str(last[0]))
    loadDisplay(Clk2,str(last[1]))
    loadDisplay(Clk3,str(last[2]))
    loadDisplay(Clk4,str(last[3]))
    print("loads last")
    position = 1
    print(position)

# Tmplementation of keypad as a lookup table
def read_keypad():
    # Look up table for keypad
    key_lut = [
        "1", "2", "3", "A",
        "4", "5", "6", "B",
        "7", "8", "9", "C",
        "*", "0", "#", "D"
    ]
    # Enumerate allows the cycling of all keys on the keypad
    for row, rowPins in enumerate(xPins):
        GPIO.output(rowPins, GPIO.HIGH) # Row pins are used as output pins
        for col, colPins in enumerate(yPins):
            # Checks if high
            if GPIO.input(colPins):
                time.sleep(0.1)
                if GPIO.input(colPins): # Column pins are used as input pins
                    GPIO.output(rowPins, GPIO.LOW)
                    return key_lut[row * 4 + col]
        GPIO.output(rowPins, GPIO.LOW)

# This method loads a provided value from the keypad onto a seven segment display        
def loadDisplay(Clk, value):
    global position # Position is used to determine which display a value will load to
    print(position)
    position = position + 1 # Increment position to cycle through all four seven segments
    print("loading")
    outputs = seven_segment_map[value] # Uses earlier SSD display mapping
    for pin, state in outputs:
        GPIO.output(Clk, GPIO.LOW)
        GPIO.output(pin, state)
        GPIO.output(DP, GPIO.LOW)
        GPIO.output(Clk, GPIO.HIGH)

# Increments the position of the display and checks the status of previous values
def increment():
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

# Sets up the automatic clock for use in runAutoClock() method
def autoClock():
    GPIO.output([Clk1, Clk2, Clk3, Clk4], GPIO.LOW)
    now = datetime.now()
    
    # Retrieves the hour and subtracts 12 to remain in 12-hour format 
    hour = now.hour
    if hour > 12:
        hour = hour - 12
        useDot() # Dot is used to show PM
        
    if hour == 0:
        hour = hour + 12
        useDot() # Dot is used to show PM

    # Retrieves the minute
    minute = now.minute
    
    # Format hour and minute to 2-digit string
    hour = '{0:02d}'.format(hour)
    minute = '{0:02d}'.format(minute)

    # Returns the hour and the minute as 2 digit strings
    return hour, minute

# Autoclock method that is called when "A" is pressed   
def runAutoClock():
    global interrupt # Establishes interrupt to break the loop when certain criteria is met
    interrupt = False # Setting interrupt to false allows the loop to continuously run
    hourDigit, minuteDigit = autoClock() # Takes values from autoClock and to use them in this method
    # Separates the two digit strings into a single digit
    hourDigit.split() 
    minuteDigit.split()
    # Loads corresponding displays with single digits
    loadDisplay(Clk1, hourDigit[0])
    last[0] = hourDigit[0]
    loadDisplay(Clk2, hourDigit[1])
    last[1] = hourDigit[1]
    loadDisplay(Clk3, minuteDigit[0])
    last[2] = minuteDigit[0]
    loadDisplay(Clk4, minuteDigit[1])
    last[3] = minuteDigit[1]
    value = read_keypad()
    while(not interrupt):
        manualTimer() # After setting the initial value for autoclock the manual timer system is used
        if(interrupt):
            break
        increment() # Increments display position

# Main timer loop    
def manualTimer():
    global countb # Counts the number of times "B" is pressed
    global count # Counts the number of times "#" is pressed
    global position
    global interrupt
    interrupt = False
    count = 0
    now = time.time() # Stores the current time
    switch = now + 60 # Stores sixty seconds in the future from the current time
    while(time.time() < switch and not interrupt): # Runs loop until interrupt
        # This turns the clock on and off
        value = read_keypad() # Reads the keypad to detect presses for "B" or "#"
        if value == 'B':
            countb = countb + 1 # Increments countb when "B" is pressed
            print("b")
            if countb == 3: # If "B" is pressed three times return to "0000" on SSDs and interrupt to break loop
                count = 0
                countb = 0
                position = 1
                startMode()
                value = 'C' # Stores value "C" to avoid the detection of four "B" presses (debounce)
                print("broke")
                interrupt = True
                break
        if value == '#':
            if(count % 2 == 0):
                position = 1
                print("off")
                
                disable() # Turns the display off if the "#" is pressed
                count = count + 1 # Increments count to keep track of display state (on or off)
                
            else:
                print("on")
               
                loadLast() # Loads the last displayed values onto the screen when turned back on
                count = count + 1
               
# Reloads the last position of the first two SSDs for overflow detection
def reLoad():
    global position
    position = 1
    print("reload")
    loadDisplay(Clk1,str(last[0]))
    loadDisplay(Clk2,str(last[1]))

# Runs the manual clock when "B" is pressed on start screen   
def runManualClock():
    global interrupt
    interrupt = False # Allows loop to continously run until broken
    while(not interrupt):
        time.sleep(.1) # Debounce
        manValue = read_keypad() # Reads the keypad and stores it as the manual clock value
        if(manValue):
            if position == 1 and (manValue == '0' or manValue == '1' or manValue == '2'): # Overflow checking logic for first SSD
                loadDisplay(Clk1, manValue)
                last[0] = int(manValue)
                GPIO.output(LED, GPIO.LOW)
            elif position == 2 and (manValue == '0' or manValue == '1' or manValue == '2' or manValue == '3' or manValue == '4' or manValue == '5' or manValue == '6' or manValue ==  '7' or manValue == '8' or manValue == '9'): # Overflow checking logic for second SSD
                loadDisplay(Clk2, manValue)
                last[1] = int(manValue)
                GPIO.output(LED, GPIO.LOW)
                if last[0] == 2: # Used for PM
                    if last[1] == 0:
                        last[0] = 0
                        last[1] = 8
                        reLoad()
                        useDot()
                    elif last[1] == 1: # Used for PM
                        last[0] = 0
                        last[1] = 9
                        reLoad()
                        useDot()
                    elif last[1] == 2: # Used for PM
                        last[0] = 1
                        last[1] = 0
                        reLoad()
                        useDot()
                    elif last[1] == 3: # Used for PM
                        last[0] = 1
                        last[1] = 1
                        reLoad()
                        useDot()
                    elif last[1] == 4: # Used for PM
                        last[0] = 1
                        last[1] = 2
                        reLoad()
                        useDot()
                elif last[0] == 1: # Used for PM
                    if last[1] == 2:
                        last[0] = 1
                        last[1] = 2
                        reLoad()
                        useDot()
                    elif last[1] == 3: # Used for PM
                        last[0] = 0
                        last[1] = 1
                        reLoad()
                        useDot()
                    elif last[1] == 4: # Used for PM
                        last[0] = 0
                        last[1] = 2
                        useDot()
                    elif last[1] == 5: # Used for PM
                        last[0] = 0
                        last[1] = 3
                        reLoad()
                        useDot()
                    elif last[1] == 6: # Used for PM
                        last[0] = 0
                        last[1] = 4
                        reLoad()
                        useDot()
                    elif last[1] == 7: # Used for PM
                        last[0] = 0
                        last[1] = 5
                        useDot()
                    elif last[1] == 8: # Used for PM
                        last[0] = 0
                        last[1] = 6
                        reLoad()
                        useDot()
                    elif last[1] == 9: # Used for PM
                        last[0] = 0
                        last[1] = 7
                        reLoad()
                        useDot()
            elif position == 3 and (manValue == '0' or manValue == '1' or manValue == '2' or manValue == '3' or manValue == '4' or manValue == '5'): # Overflow logic for third SSD
                loadDisplay(Clk3, manValue)
                last[2] = int(manValue)
                GPIO.output(LED, GPIO.LOW)
            elif position == 4 and (manValue == '0' or manValue == '1' or manValue == '2' or manValue == '3' or manValue == '4' or manValue == '5' or manValue == '6' or manValue ==  '7' or manValue == '8' or manValue ==  '9'): # Overflow logic for fourth SSD   
                loadDisplay(Clk4, manValue)
                last[3] = int(manValue)
                GPIO.output(LED, GPIO.LOW)
            else:
                GPIO.output(LED, GPIO.HIGH)
        else: # Begins flashing the SSDs based on above logic
            if position == 1:
                flash(Clk1)
            elif position == 2:
                flash(Clk2)
            elif position == 3:
                flash(Clk3)
            elif position == 4:
                flash(Clk4)
            else:
                while(not interrupt):
                    manualTimer()
                    if(interrupt):
                        break
                    increment()

# Uses the dot if value is PM in manual or automatic mode
def useDot():
    GPIO.output(Clk2, GPIO.LOW)
    GPIO.output(DP, GPIO.HIGH)
    GPIO.output(Clk2, GPIO.HIGH)
    GPIO.output(DP, GPIO.LOW)
    GPIO.output(Clk2, GPIO.LOW)
    
# Sets the displays to "0000" on program run   
startMode()

# Main loop
while True:
    value = read_keypad() # Reads keypad continuously
    print(value)
    if(value):
        print("reading")
        # This runs the automatic clock
        if value == 'A':
            runAutoClock()
        # This runs the manual clock    
        elif value == 'B':
            runManualClock()

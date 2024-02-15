#imports for file
import time
import RPi.GPIO as GPIO

#Definig GPIO mode and input/output
GPIO.setmode(GPIO.BCM)

# X-Values (Horizontal) Mapping
GPIO.setup(18, GPIO.OUT) #Yellow Wire X1
GPIO.setup(23, GPIO.OUT) #Orange Wire X2
GPIO.setup(24, GPIO.OUT) #Brown Wire X3
GPIO.setup(25, GPIO.OUT) #Red Wire X4

#  Y-Values (Vertical) Mapping
GPIO.setup(12, GPIO.IN) #Black Wire Y1
GPIO.setup(16, GPIO.IN) #White Wire Y2
GPIO.setup(20, GPIO.IN) #Gray Wire Y3
GPIO.setup(21, GPIO.IN) #Blue Wire Y4

#GPIO SETUP
Clk = 26
E = 19
D =13
C =6
DP = 5
G = 22
F = 27
A =17
B = 4
GPIO.setup(Clk, GPIO.OUT) #Clock 
GPIO.setup(E, GPIO.OUT) #E
GPIO.setup(D, GPIO.OUT) #D
GPIO.setup(C, GPIO.OUT) #C
GPIO.setup(DP, GPIO.OUT) #DP
GPIO.setup(G, GPIO.OUT) #G
GPIO.setup(F, GPIO.OUT) #F
GPIO.setup(A, GPIO.OUT) #A
GPIO.setup(B, GPIO.OUT) #B

enable = True

# Resets SSD Display
def resetGPIO():
    GPIO.output(Clk, GPIO.HIGH)
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
    GPIO.output(Clk, GPIO.LOW)
    
# Conditional implementation of keypad
def readKeypad(rowNum, char):
    
    curVal = 0
    GPIO.output(rowNum, GPIO.HIGH)
    if GPIO.input(12) == 1:
        curVal = char[0]
        time.sleep(0.2)
        return curVal
        
    if GPIO.input(16) == 1:
        curVal = char[1]
        time.sleep(0.2)
        return curVal
        
    if GPIO.input(20) == 1:
        curVal = char[2]
        time.sleep(0.2)
        return curVal
        
    if GPIO.input(21) ==1:
        curVal = char[3]
        time.sleep(0.2)
        return curVal

    GPIO.output(rowNum, GPIO.LOW)

while True:
    GPIO.output(Clk, GPIO.LOW)
    
    row1 = readKeypad(18,[1,2,3,'A'])
    if row1 == 1 and enable:
        resetGPIO()
        GPIO.output([B,C], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row1 == 2 and enable:
        resetGPIO()
        GPIO.output([A,B,G,E,D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row1 == 3 and enable:
        resetGPIO()
        GPIO.output([A,B,C,G,D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row1 == 'A' and enable:
        resetGPIO()
        GPIO.output([F, A, E, B, C, G], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
        
    row2 = readKeypad(23,[4,5,6,'B'])
    if row2 == 4 and enable:
        resetGPIO()
        GPIO.output([F, G, B, C], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row2 == 5 and enable:
        resetGPIO()
        GPIO.output([A, F, G, C, D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row2 == 6 and enable:
        resetGPIO()
        GPIO.output([A,F,G,C,D,E], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row2 == 'B' and enable:
        resetGPIO()
        GPIO.output([F,E,D,C,G], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)

    row3 = readKeypad(24,[7,8,9,'C'])
    if row3 == 7 and enable:
        resetGPIO()
        GPIO.output([A,B,C], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row3 == 8 and enable:
        resetGPIO()
        GPIO.output([A,B,C,D,E,F,G], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row3 == 9 and enable:
        resetGPIO()
        GPIO.output([A,B,C,F,G], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row3 == 'C' and enable:
        resetGPIO()
        GPIO.output([A,F,E,D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)

    row4 = readKeypad(25,['*',0,'#','D'])
    if row4 == '*' and enable:
        resetGPIO()
        GPIO.output([DP], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row4 == 0 and enable:
        resetGPIO()
        GPIO.output([A,B,F,C,E,D], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    elif row4 == '#':
        resetGPIO()
        print("useless")
        if(enable):
                GPIO.output(Clk, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(Clk, GPIO.LOW)
                enable = False
                time.sleep(.1)
                print(enable)
        else: = True
                GPIO.output(Clk, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(Clk, GPIO.LOW)
                print(enable)
    elif row4 == 'D' and enable:
        resetGPIO()
        GPIO.output([B,G,E,D,C], GPIO.HIGH)
        GPIO.output(Clk, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(Clk, GPIO.LOW)
    
    GPIO.output(Clk, GPIO.LOW)

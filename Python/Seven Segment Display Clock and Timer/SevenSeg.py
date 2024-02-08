#imports for file
import time
import RPi.GPIO as GPIO
from Keypad import readKeypad


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

def resetGPIO():
    GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)

while True:
    row1 = readKeypad(18,[1,2,3,'A'])
    time.sleep(.01)
    if row1 == 1:
        resetGPIO()
        GPIO.output([B,C], GPIO.HIGH)
    elif row1 == 2:
        resetGPIO()
        GPIO.output([A,B,G,E,D], GPIO.HIGH)
    elif row1 == 3:
        resetGPIO()
        GPIO.output([A,B,C,G,D], GPIO.HIGH)
    else:
        resetGPIO()
        GPIO.output([F, A, E, B, C, G], GPIO.HIGH)
        
    row2 = readKeypad(23,[4,5,6,'B'])
    time.sleep(.01)
    if row2 == 4:
        resetGPIO()
        GPIO.output([F, G, B, C], GPIO.HIGH)
    elif row2 == 5:
        resetGPIO()
        GPIO.output([A, F, G, C, D], GPIO.HIGH)
    elif row2 == 6:
        resetGPIO()
        GPIO.output([A,F,G,C,D,E], GPIO.HIGH)
    else:
        resetGPIO()
        GPIO.output([F,E,D,C,G], GPIO.HIGH)

    row3 = readKeypad(24,[7,8,9,'C'])
    time.sleep(.01)
    if row3 == 7:
        resetGPIO()
        GPIO.output([A,B,C], GPIO.HIGH)
    elif row3 == 8:
        resetGPIO()
        GPIO.output([A,B,C,D,E,F,G], GPIO.HIGH)
    elif row3 == 9:
        resetGPIO()
        GPIO.output([A,B,C,F,G], GPIO.HIGH)
    else:
        resetGPIO()
        GPIO.output([A,F,E,D], GPIO.HIGH)

    row4 = readKeypad(25,['*',0,'#','D'])
    time.sleep(.01)
    if row4 == '*':
        resetGPIO()
        GPIO.output([A,B,C,D,E,F,G,DP], GPIO.LOW)
    elif row4 == 0:
        resetGPIO()
        GPIO.output([A,B,F,C,E,D], GPIO.HIGH)
    elif row4 == '#':
        resetGPIO()
        print("useless")
    else:
        resetGPIO()
        GPIO.output([B,G,E,D,C], GPIO.HIGH)
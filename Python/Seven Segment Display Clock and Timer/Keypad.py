#Imports
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

# Conditional implementation of keypad
def readKeypad(rowNum, char):
    curVal = 0
    GPIO.output(rowNum, GPIO.HIGH)
    if GPIO.input(12) == 1:
        curVal = char[0]
        return curVal
        time.sleep(0.1)
    if GPIO.input(16) == 1:
        curVal = char[1]
        return curVal
        time.sleep(0.1)
    if GPIO.input(20) == 1:
        curVal = char[2]
        return curVal
        time.sleep(0.1)
    if GPIO.input(21) ==1:
        curVal = char[3]
        return curVal
        time.sleep(0.1)
    GPIO.output(rowNum, GPIO.LOW)
    

while True:
    readKeypad(18,[1,2,3,'A'])
    time.sleep(.01)
    readKeypad(23,[4,5,6,'B'])
    time.sleep(.01)
    readKeypad(24,[7,8,9,'C'])
    time.sleep(.01)
    readKeypad(25,['*',0,'#','D'])
    time.sleep(.01)

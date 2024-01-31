#Imports
import time
import RPi.GPIO as GPIO

#Definig GPIO mode and input/output
GPIO.setmode(GPIO.BCM)


GPIO.setup(18, GPIO.OUT) #Yellow Wire X1
GPIO.setup(23, GPIO.OUT) #Orange Wire X2
GPIO.setup(24, GPIO.OUT) #Brown Wire X3
GPIO.setup(25, GPIO.OUT) #Red Wire X4
GPIO.setup(12, GPIO.IN) #Black Wire Y1
GPIO.setup(16, GPIO.IN) #White Wire Y2
GPIO.setup(20, GPIO.IN) #Gray Wire Y3
GPIO.setup(21, GPIO.IN) #Blue Wire Y4


#Defining the keymap for the keypad


#conditional implementation of keypad I thought it would be easiest this way
def readKeypad(rowNum, char):
    GPIO.output(rowNum, GPIO.HIGH)
    if GPIO.input(12) == 1:
        curVal = char[0]
    if GPIO.input(16) == 1:
        curVal = char[1]
    if GPIO.input(20) == 1:
        curVal = char[2]
    if GPIO.input(21) ==1:
        curVal = char[3]
    GPIO.output(rowNum, GPIO.LOW)
    return curVal

while True:
    readKeypad(18,[1,2,3,'A'])
    readKeypad(23,[1,2,3,'A'])
    readKeypad(24,[1,2,3,'A'])
    readKeypad(25,[1,2,3,'A'])

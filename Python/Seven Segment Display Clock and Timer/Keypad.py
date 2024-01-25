#Imports
import time
import RPi.GPIO as GPIO

#Definig GPIO mode and input/output
GPIO.setmode(GPIO.BCM)


GPIO.setup(18, GPIO.IN) #Yellow Wire X1
GPIO.setup(23, GPIO.IN) #Orange Wire X2
GPIO.setup(24, GPIO.IN) #Brown Wire X3
GPIO.setup(25, GPIO.IN) #Red Wire X4
GPIO.setup(12, GPIO.IN) #Black Wire Y1
GPIO.setup(16, GPIO.IN) #White Wire Y2
GPIO.setup(20, GPIO.IN) #Gray Wire Y3
GPIO.setup(21, GPIO.IN) #Blue Wire Y4


#Defining the keymap for the keypad



def readKeypad(rowNum,char):

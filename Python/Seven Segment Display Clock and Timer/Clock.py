#imports for file
import time
import RPi.GPIO as GPIO
from datetime import datetime
GPIO.setmode(GPIO.BCM)


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

GPIO.setup(Clk1, GPIO.OUT) # Clock 1
GPIO.setup(Clk2, GPIO.OUT) # Clock 2
GPIO.setup(Clk3, GPIO.OUT) # Clock 3
GPIO.setup(Clk4, GPIO.OUT) # Clock 4

GPIO.setup(E, GPIO.OUT) # E
GPIO.setup(D, GPIO.OUT) # D
GPIO.setup(C, GPIO.OUT) # C
GPIO.setup(DP, GPIO.OUT) # DP
GPIO.setup(G, GPIO.OUT) # G
GPIO.setup(F, GPIO.OUT) # F
GPIO.setup(A, GPIO.OUT) # A
GPIO.setup(B, GPIO.OUT) # B
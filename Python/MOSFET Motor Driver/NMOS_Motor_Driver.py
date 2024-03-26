import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Variables
print("Enter Frequency: ")
freq = int(input())
print("Enter Duty Cycle")
duty = int(input())

# Pin Setup
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18,freq)

while True:
	pwm.ChangeFrequency(freq)
	pwm.start(duty)

pwm.stop()

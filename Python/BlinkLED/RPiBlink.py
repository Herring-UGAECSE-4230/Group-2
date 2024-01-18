# Import libraries and dependencies
import RPi.GPIO as GPIO
from time import sleep

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pin setup
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)

# Main square wave loop
while True:
	GPIO.output(17, GPIO.HIGH)
	sleep(.05)
	GPIO.output(17, GPIO.LOW)
	sleep(.05)

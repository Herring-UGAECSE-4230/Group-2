# Import libraries and dependencies
import RPi.GPIO as GPIO
from time import sleep

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pin setup
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)

# Main square wave loop
while True:
	GPIO.output(25, GPIO.HIGH)
	sleep(0.1)
	GPIO.output(25, GPIO.LOW)
	sleep(0.1)

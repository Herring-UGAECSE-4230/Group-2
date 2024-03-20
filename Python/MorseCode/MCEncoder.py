import RPi.GPIO as GPIO
import time
from time import sleep, perf_counter
import simpleaudio as sa
import numpy as np

# Pin configuration
LED_PIN = 26
SPEAKER_PIN = 18

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)

# Morse code mapping
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..', ' ': ' ', 'ATTENTION': '-.-.-', 'OVER': '-.-', 'OUT': '.-.-.',
    '1': '.----', '0':'-----', '9': '----.-'
}

# Function to output Morse code
def output_morse(morse_code, unit_length):
    # Initialize PWM for the speakers
    speaker_pwm = GPIO.PWM(SPEAKER_PIN, 50000) # Frequency 1000 Hz
    
    dot_duration = unit_length / 1000  # Convert to seconds
    dash_duration = 3 * dot_duration

    for char in morse_code:
        start_time = perf_counter()
        if char == '.':
            GPIO.output(LED_PIN, True)
            speaker_pwm.start(50)  # 50% Duty cycle
            time.sleep(dot_duration)
            GPIO.output(LED_PIN, False)
            speaker_pwm.stop()
        elif char == '-':
            GPIO.output(LED_PIN, True)
            speaker_pwm.start(50)  # 50% Duty cycle
            time.sleep(dash_duration)
            GPIO.output(LED_PIN, False)
            speaker_pwm.stop()
        else:
            sleep(dot_duration)  # Off period between dots/dashes, words, and letters
        end_time = perf_counter()
        print(f"Duration: {end_time - start_time} seconds")  # Print the duration for verification

def main():
	output_morse("...", 100)
 
while True:
	 main()

import RPi.GPIO as GPIO
import time
from datetime import datetime

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO Setup
GPIO.setup(23, GPIO.IN)
GPIO.setup(25, GPIO.OUT)

# Morse code mapping
MORSE_CODE_DICT = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 
    'y': '-.--', 'z': '--..', ' ': ' ', 'attention': '-.-.-', 'over': '-.-',
    'out': '.-.-.', '1': '.----', '0':'-----', '9': '----.-'
}

MORSE_TO_LETTERS = {
    '.-':'a', '-...':'b', '-.-.':'c', '-..':'d', '.':'e', '..-.':'f', 
    '--.':'g', '....':'h', '..':'i', '.---':'j', '-.-':'k', '.-..':'l', 
    '--':'m', '-.':'n', '---':'o', '.--.':'p', '--.-':'q', '.-.':'r', 
    '...':'s' , '-':'t', '..-':'u', '...-':'v', '.--':'w', '-..-':'x', 
    '-.--':'y', '--..':'z', ' ': ' ', '-.-.-':'attention',  '-.-':'over',
    '.-.-.':'out', '.----':'1', '-----':'0', '----.-':'9'
}


global dot_length, morse, decoded, word, calibrated
dot_length = 0
morse = ""
word = ""
decoded = ""
calibrated = False

#Attention
def calibrate():
    global calibrated,dot_length
    count = 0
    print ("Attention")
    print("tap: -.-.-")
    while(not calibrated):
        print("not in contact")
        if(GPIO.input(23)==1):
            time.sleep(0.05)
            
            #only increments the count after it is released
 
            if(count == 0):
                dash_start = float(time.time())
            elif(count == 1):
                dot_start = float(time.time())
            elif(count == 2):
                dash_start = float(time.time())
            elif(count == 3):
                dot_start = float(time.time())
            
            elif(count == 4):
                dash_start = float(time.time())

            #won't loop again until release  
            while(GPIO.input(23)==1):
                print("in contact")
            #increment count
            time.sleep(0.01)
            count = count + 1
        elif(GPIO.input(23) == 0):
            if(count == 1):
                first_dash = float(time.time()) - dash_start
            elif(count == 2):
                first_dot = float(time.time())- dot_start
            elif(count == 3):
                second_dash = float(time.time()) - dash_start
            elif(count == 4):
                second_dot = float(time.time()) - dot_start
            elif (count ==  5):
                third_dash = float(time.time())-dash_start
                calibrated = True

    
    dot_length = (first_dot+second_dot)/2  + ((first_dash + second_dash + third_dash)/9)/2
    print(dot_length)
   
    # trying to calibrate the most accurate dot using all data possible
    


            



    
calibrate()
print("calibrated")
while(True):
    if(GPIO.input(23) == 1): # If a signal is detected we go into "on" mode
        on = float(time.time())
        while(GPIO.input(23) == 1): # While the tapper is held down, a timer is running
           GPIO.output(25, 1)
           print("timing")
        GPIO.output(25, 0)

        onLength = float(time.time()) - on # Timer for "on" state of tapper
        
        if(onLength < dot_length*2): # If on length is less than 2 times unit length -> .
            morse = morse +"."
            print(onLength)
            print(morse)
        else: # If on length is more than 2 times unit length -> -
            morse = morse + "-"
            print(morse)
            
    elif(GPIO.input(23) == 0): # If a signal is not detected we go into "off mode"
        off = float(time.time())
        while(GPIO.input(23) == 0): 
            GPIO.output(25, 0)
        
        offLength = float(time.time()) - off # Timer for "off" state of tapper
        
        # Conditionals to determine what is displaying
        if(offLength < dot_length*2): # If off time is less than 2 times unit length -> Morse code
            print("Morse Code")
            time.sleep(0.01)
            
        elif(dot_length*5 > offLength > dot_length*2): # If off time is between 2 times unit length and 5 times unit length -> Space between character
            # Space between characters
            print("Space between CHARACTER")
            time.sleep(0.01)
            
            if(morse in MORSE_TO_LETTERS):
                character = MORSE_TO_LETTERS[morse]
                word = word + character
                morse = ""
                print(word)
                
        elif(offLength > dot_length*5): # If off time is greater than 5 times the unit length -> Space between word
            # Space between words
            print("Space between WORD")
            time.sleep(0.01)
            if(morse in MORSE_TO_LETTERS):
                word = MORSE_TO_LETTERS[morse]
                morse = ""
                decoded = word + " "
                print(decoded)
                if (word == "out"):
                    break
                else:
                    word = ""

outputfile = open("output.txt", "a")
outputfile.write(decoded)
outputfile.close()
                


        

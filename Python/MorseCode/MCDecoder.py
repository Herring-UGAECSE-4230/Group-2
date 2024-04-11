import RPi.GPIO as GPIO
import time
from datetime import datetime
import io

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO Setup
GPIO.setup(23, GPIO.IN)
GPIO.setup(25, GPIO.OUT)

# English to morse code mapping
MORSE_CODE_DICT = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 
    'y': '-.--', 'z': '--..', ' ': ' ', 'attention': '-.-.-', 'over': '-.-',
    'out': '.-.-.', '1': '.----', '0':'-----', '9': '----.-', "sos": "...---...", "?":"?"
}

# Morse code to English mapping
MORSE_TO_LETTERS = {
    '.-':'a', '-...':'b', '-.-.':'c', '-..':'d', '.':'e', '..-.':'f', 
    '--.':'g', '....':'h', '..':'i', '.---':'j', '-.-':'k', '.-..':'l', 
    '--':'m', '-.':'n', '---':'o', '.--.':'p', '--.-':'q', '.-.':'r', 
    '...':'s' , '-':'t', '..-':'u', '...-':'v', '.--':'w', '-..-':'x', 
    '-.--':'y', '--..':'z', ' ': ' ', '-.-.-':'attention',  '-.-':'over',
    '.-.-.':'out', '.----':'1', '-----':'0', '----.-':'9', "...---...": "sos", "?":"?"
}

# Globalizing and declaring variables
global dot_length, morse, word, calibrated, spaceTrue
dot_length = 0
morse = ""
word = ""
calibrated = False
spaceWord = False
spaceChar = False
threshold = 0.01

# Encoding method from MC Encoder
def encode():
    global morseOnly
    global word
    outputfile = open("output.txt", "w")
    mc = ""
    mc = str(mc)
    print(word)
    word_array = word.split("\n")
    print(word_array)
    
    for x in word_array:
        
        if(x == "attention"):
            mc += "-.-.-"
        elif(x  == "over"):
            mc += "-.-"
        elif(x  == "out"):
            mc += ".-.-."
        else:
            for char in x:
                print(char)
                mc += str(MORSE_CODE_DICT[char]) + " "
        mc += ("| " +  x + "\n")
    mc = mc[0:len(mc)-4]
    print(mc)
    outputfile.write(mc)
    outputfile.close()
    
# Calibrating based on code word attention    
def calibrate():
    global calibrated,dot_length,word 
    count = 0
    print("Tap: -.-.-")
    while(not calibrated):
        if(GPIO.input(23)==1):
            time.sleep(0.05)
            
            # Only increments the count after it is released
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

            # Won't loop again until release  
            while(GPIO.input(23)==1):
                pass
            # Increment count
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

    word = word + "attention" + "\n"
    dot_length = (first_dash + second_dash + third_dash)/9
    print("The unit dot length is: ")
    print(dot_length)
    # Trying to calibrate the most accurate dot using all data possible

calibrate()
print("Calibrated")
while(True):
    spaceChar = False
    spaceWord = False
    if(GPIO.input(23) == 1): # If a signal is detected we go into "on" mode
        on = float(time.time())
        while(GPIO.input(23) == 1): # While the tapper is held down, a timer is running
           GPIO.output(25, 1)

        GPIO.output(25, 0)

        onLength = float(time.time()) - on # Timer for "on" state of tapper
        
        if(onLength < dot_length*2 and onLength > threshold): # If on length is less than 2 times unit length -> .
            morse = morse +"."
            print(onLength)
            print(morse)
        elif(onLength > dot_length*2): # If on length is more than 2 times unit length -> -
            morse = morse + "-"
            print(morse)
            
        spaceWord = True
        spaceChar = True
            
    elif(GPIO.input(23) == 0): # If a signal is not detected we go into "off mode"
        off = float(time.time())
        while(GPIO.input(23) == 0): 
            GPIO.output(25, 0)
        
        offLength = float(time.time()) - off # Timer for "off" state of tapper
        
        # Conditionals to determine what is displaying
        if(offLength < dot_length*2): # If off time is less than 2 times unit length -> Morse code
            time.sleep(0.01)
            
            
        elif((dot_length*6 > offLength) and (offLength>dot_length*2)): # If off time is less than 5 times unit length and greater than 2 times unit length -> Space between characters
            time.sleep(0.01)
            
            if(morse in MORSE_TO_LETTERS):
                character = MORSE_TO_LETTERS[morse]
                word = word + character
                morse = ""
                print(word)
                if (character == "out"):
                    break
            elif(len(morse) > 0):
                word = word + "?"
                morse = ""
            spaceChar = False
                
            
        elif(offLength > dot_length*6):
            # Space between words
            time.sleep(0.01)
            spaceWord = False
            if(morse in MORSE_TO_LETTERS):
                character = MORSE_TO_LETTERS[morse]
                word = word + character + "\n"
                morse = ""
                print(word)
                if (character == "out"):
                    encode()
                    break
                    
            elif(len(morse) > 0):
                word = word + "?"
                morse = ""
            spaceChar = False


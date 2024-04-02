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
    global calibrated
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
                time.sleep(0.01)
            elif(count == 1):
                dot_start = float(time.time())
                time.sleep(0.01)
            elif(count == 2):
                dash_start = float(time.time())
                time.sleep(0.01)
            elif(count == 3):
                dot_start = float(time.time())
                time.sleep(0.01)
            
            elif(count == 4):
                dash_start = float(time.time())
                time.sleep(0.01)

            #won't loop again until release  
            while(GPIO.input(23)==1):
                print("in contact")
            #increment count
            count = count + 1
        elif(GPIO.input(23) == 0):
            time.sleep(0.05)
            if(count == 1):
                first_dash = float(time.time()) - dash_start
                time.sleep(0.01)
            elif(count == 2):
                first_dot = float(time.time())- dot_start
                time.sleep(0.01)
            elif(count == 3):
                second_dash = float(time.time()) - dash_start
                time.sleep(0.01)
            elif(count == 4):
                second_dot = float(time.time()) - dot_start
                time.sleep(0.01)
            elif (count ==  5):
                third_dash = float(time.time())-dash_start
                time.sleep(0.01)
                calibrated = True

    
    dash_length = (first_dash + second_dash + third_dash)/3
    dot_length = (first_dot+second_dot)/2  + (dash_length/3)/2
    print(dot_length)
    # trying to calibrate the most accurate dot using all data possible
    


            



    
calibrate()
print("calibrated")
while(True):
    if(GPIO.input(23) == 1):
        on = float(time.time())
        
        while(GPIO.input(23) == 1):
           GPIO.output(25, 1)
           print("timing")
        GPIO.output(25, 0)

        onLength = float(time.time()) - on
        if(onLength<dot_length+dot_length*0.5):
            morse = morse +"."
            print(morse)
        else:
            morse = morse + "-"
            print(morse)
    elif(GPIO.input == 0):
        off = float(time.time())
        while(GPIO.input(23) == 0):
            print("timing")
        offLength = float(time.time()) - off
        if(dot_length/2<offLength<dot_length+dot_length*0.5):
            #space between characters
            print("space between character")

        elif(offLength>dot_length+dot_length*0.5):
            #space between words
            if(morse in MORSE_TO_LETTERS ):
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
                


        

import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
# GPIO Setup
GPIO.setup(18, GPIO.IN)
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


global dot_length, morse, decoded, word
dot_length = 0
morse = ""
word = ""
decoded = ""

#attention
def calibrate():
    calibrated = False
    count = 0
    print ("Attention")
    print("tap: -.-.-")
    while(not calibrated):
        if(GPIO.input(18)==1):
            if(count == 0):
                dash_start = time.now()
                count = count + 1
            elif(count == 1):
                first_dash = time.now() - dash_start
                count = count + 1
            elif(count == 2):
                dot_start = time.now()
                count = count + 1
            elif(count == 3):
                first_dot = time.now()- dot_start
                count = count + 1
            elif(count == 4):
                dash_start = time.now()
                count = count + 1
            elif(count == 5):
                second_dash = time.now() - dash_start
                count = count + 1
            elif(count == 6):
                dot_start = time.now()
                count = count + 1
            elif(count == 7):
                second_dot = time.now() - dot_start
                count = count + 1
            elif(count == 8):
                dash_start = time.now()
                count = count + 1
            elif(count == 9):
                third_dash = time.now()-dash_start
                count = count + 1
                calibrated = True
    
    dash_length = (first_dash + second_dash + third_dash)/3
    dot_length = (first_dot+second_dot)/2 
    # trying to calibrate the most accurate dot using all data possible
    dot_length = (dot_length + (dash_length/3)/2)


            



    


while(True):
    if(GPIO.input(18) == 1):
        start = time.now()
        GPIO.output(25, 1)
        while(GPIO.input(18) == 1):
            print("wait")
        GPIO.output(25, 0)
        length = time.now() - start
        if(length<dot_length+dot_length*0.5):
            morse = morse +"."
        else:
            morse = morse + "-"
    elif(GPIO.input == 0):
        start = time.now()
        while(GPIO.input(18) == 0):
            print("wait")
        length = time.now() - start
        if(dot_length/2<length<dot_length+dot_length*0.5):
            #space between characters
            print("space between character")

        elif(length>dot_length+dot_length*0.5):
            #space between words
            if(morse in MORSE_TO_LETTERS ):
                word = MORSE_TO_LETTERS[morse]
                morse = ""
                decoded = word + " "
                if (word == "out"):
                    break
                else:
                    word = ""

outputfile = open("output.txt", "a")
outputfile.write(decoded)
outputfile.close()
                


        

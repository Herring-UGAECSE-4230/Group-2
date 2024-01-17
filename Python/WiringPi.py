#Imported wiring pi library
import wiringpi

#Setting up GPIO using wiringpi
wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(17)

#second paramter is frequency
wiringpi.softToneWrite(17, 10)


while True:
    #empty while loop
    print(" ")
wiringpi.softToneWrite(17, 0)

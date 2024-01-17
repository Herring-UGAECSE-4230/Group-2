#Imported wiring pi library
import wiringPi

#Setting up GPIO using wiringpi
wiringpi.wiringPiSetupGpio(17)
wiringpi.sodtToneCreate(17)

#second paramter is frequency
wiringpi.softToneWrite(17, 100)


while True:
    #empty while loop


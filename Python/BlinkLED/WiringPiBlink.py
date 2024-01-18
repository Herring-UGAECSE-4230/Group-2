# Imported wiring pi library
import wiringpi

# Setting up GPIO using wiringpi
wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(17)

# Second paramter is frequency
wiringpi.softToneWrite(17, 100000)

# Empty while loop
while True:
    print(" ")
wiringpi.softToneWrite(17, 0)

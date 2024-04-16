import RPi.GPIO as GPIO
import time
from datetime import datetime
import math
# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setting duty cycle
duty = 18
freq = 500
# Defining RPM
global RPM
RPM = 0
DesiredRPM = 850
# Setting GPIO pins
clk =22
dt = 27
sw = 17
ir = 23
previousFreq = 0
# Setting PWM and pin setup
GPIO.setup(18, GPIO.OUT)
motor = GPIO.PWM(18, freq)
GPIO.setup([clk,dt,sw,ir], GPIO.IN)

# Allowing for dt and clk to have an internal pull up
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Tracks amount of switch press used to turn off and on the PWM later in code
pressCount = 0

# Setup and initialize variables
start = time.time()


# Debounce method
def debounce(input):
 global start, previousFreq
    
  # Calculate difference in time between start and current time
 now = time.time()
 difference = abs(now - start)
    
  # Shows change from last signal to help filter random noise
 change = abs(input - previousFreq)
    
  # Essentially creates a threshold to filter out some noise we encountered
 if (abs(change) > 0.2):
      

   # Print("Turns per second: ", tps)
    # Update tps based on change of freqeuncy and difference in time
    # Update previous values 
    start = now
    previousFreq = input
    
 
 
    
def countSpins():
    global RPM
    irCounter = 0
    
    start = float(time.time())
    blocked = False

    while(irCounter < 4):
      end = time.time()
      if((end - start) > 0.1):
        RPM = 0
        return
      if(GPIO.input(ir) == 1 and (not blocked)):
        irCounter += 1
        blocked = True
      elif(GPIO.input(ir) == 0):
        blocked = False
    
    done = float(time.time()) - start

    RPM = 16*3.14/done
        
    
# Defining last state
lastClkState = GPIO.input(clk)
lastswState = GPIO.input(sw)


# Main loop to monitor encoder
while True:

    
  print("Desired RPM: ", DesiredRPM, " RPM: ", RPM)
  print("Duty: ", duty)
  direction = "None"
  # Monitors GPIO states
  clkState = GPIO.input(clk)
  dtState = GPIO.input(dt)
  swState = GPIO.input(sw)
  debounce(clkState)
  # Conditionals to monitor the states of clk dt and sw 
  if (swState != lastswState):
    if swState == False:
      print("Press")
      
      if(pressCount % 2 == 0):
        motor.start(duty)
      else:
        motor.stop()

      pressCount += 1
      time.sleep(0.15)
  if (clkState != lastClkState):
    if (dtState != clkState):
      if(DesiredRPM<2525):
        DesiredRPM += 25
        duty = math.exp((DesiredRPM + 2165.539) / 1022.3302)
        motor.start(duty)
        countSpins()
        print("Desired RPM: ", DesiredRPM, " RPM: ", RPM)
        print("Duty: ", duty)
      
    else:
      if(duty > 18):
        DesiredRPM -= 25
        duty = duty = math.exp((DesiredRPM + 2165.539) / 1022.3302)
        motor.start(duty)
        countSpins()
        print("Desired RPM: ", DesiredRPM, " RPM: ", RPM)
        print("Duty: ", duty)
    lastClkState=clkState
    

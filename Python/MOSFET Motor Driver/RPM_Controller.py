import RPi.GPIO as GPIO
import time
from datetime import datetime

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setting frequency and duty cycle
freq = 0
duty = 50

# Defining RPM
global RPM
RPM = 0

# Setting GPIO pins
clk =22
dt = 27
sw = 17
ir = 23

# Setting PWM and pin setup
pwm = GPIO.PWM(18,freq)
GPIO.setup([clk,dt,sw,ir], GPIO.IN)

# Allowing for dt and clk to have an internal pull up
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Tracks amount of switch press used to turn off and on the pwm later in code
pressCount = 0

# Debounce method
def debounce(input):
 global start, previousFreq, tps
    
  # Calculate difference in time between start and current time
 now = time.time()
 difference = abs(now - start)
    
  # Shows change from last signal to help filter random noise
 change = abs(input - previousFreq)
    
  # Essentially creates a threshold to filter out some noise we encountered
 if (abs(change) > 0.2):
      
    tps = change / difference
   # Print("Turns per second: ", tps)
    # Update tps based on change of freqeuncy and difference in time
    # Update previous values 
    start = now
    previousFreq = input
    
   # Sleep for time based debounce
 time.sleep(0.01)
    
def countSpins():
    global RPM
    irCounter = 0
    start = float(time.time())
    blocked = False

    while(irCounter < 3):
      if(GPIO.input(ir) == 1 and (not blocked)):
        irCounter += 1
        blocked = True
      elif(GPIO.input(ir) == 0):
        blocked = False
    
    done = float(time.time()) - start

    RPM = 20/done
        
    
# Defining last state
lastClkState = GPIO.input(clk)
lastswState = GPIO.input(sw)


# Main loop to monitor encoder
while True:
  
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
        pwm.start(duty)
      else:
        pwm.stop()

      pressCount += 1
      time.sleep(0.15)
  if (clkState != lastClkState):
    if (dtState != clkState):
      freq += 25
      pwm.ChangeFrequency(freq)
      direction = "Clockwise"
      countSpins()
      print("Desired Freq: ", freq, " RPM: ", RPM)
    else:
      if(freq > 1):
        freq -= 25
        pwm.ChangeFrequency(freq)
        direction = "CounterClockwise"
        countSpins()
        print("Desired Freq: ", freq, " RPM: ", RPM)
    lastClkState=clkState

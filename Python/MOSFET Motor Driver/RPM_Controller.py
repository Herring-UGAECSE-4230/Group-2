import RPi.GPIO as GPIO
import time
from datetime import datetime
import math

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setting duty cycle and frequency
duty = 18
freq = 500

# Initializing and defining RPM
global RPM
RPM = 0
DesiredRPM = 850

# Setting up GPIO pins and debounce variable
clk =22 # Clock pin
dt = 27 # Data pin
sw = 17 # Switch pin
ir = 23 # IR Sensor pin
previousFreq = 0 # Debounce variable
inputPin = 24 # PWM detector pin

# Setting PWM and pins to outputs and inputs
GPIO.setup(18, GPIO.OUT)
GPIO.setup(inputPin, GPIO.IN)
motor = GPIO.PWM(18, freq) # PWM for motor control
GPIO.setup([clk,dt,sw,ir], GPIO.IN)

# Allowing for dt and clk to have an internal pull up
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Tracks amount of switch press used to turn off and on the PWM later in code
pressCount = 0
on = False

# Setup and initialize variables for debounce
start = time.time()

# Debounce method
def debounce(input):
 global start, previousFreq
    
  # Calculate difference in time between start and current time
 now = time.time()
 difference = abs(now - start)
    
  # Shows change from last signal to help filter random noise
 change = abs(input - previousFreq)
    
  # Creates a threshold to filter out noise we encountered
 if (abs(change) > 0.2):
    # Update previous values 
    start = now 
    previousFreq = input

# Method to count the the amount of fan blades that pass in front of IR sensor
def countSpins():
    global RPM
    irCounter = 0 # Counter for fan blades
    start = float(time.time()) # Timer to calculate RPM
    blocked = False # Determines whether or not the IR sensor is blocked by fan blade

    # Loops if there has not been sufficient fan interrupts to calculate RPM
    while(irCounter < 4): 
      end = time.time() # Starts second timer to compare to start timer
      
      if((end - start) > 0.1): # If fan no longer is receiving input
        RPM = 0
        return
      
      if(GPIO.input(ir) == 1 and (not blocked)): 
        irCounter += 1 # Increments the irCounter if a rising edge is detected
        blocked = True # Notifies method that the fan is blocking the IR sensor
      
      elif(GPIO.input(ir) == 0): 
        blocked = False # If fan blade is not detected then blocked becomes false
    
    done = float(time.time()) - start # Calculates the total time taken for a full rotation of the fan

    RPM = 16*3.14/done # Converts rising edges per second to rising edges per minute
    # Also turns a linear speed into an angular speed by C = 2*pi*r (circumference)
    

# Defining last state for switch and clock pin and sets a timer to determine state of optocoupler
lastClkState = GPIO.input(clk)
lastswState = GPIO.input(sw)
optoTime = time.time()

# Main loop to monitor encoder
while True:
  if(GPIO.input(inputPin)):
    optoTime = time.time() # Starts the optocoupler timer
  
  if(time.time() > optoTime + 1 and pressCount > 0): # If no signal at optocoupler input for at least a second then no RPM
    RPM = 0
  
  print("Desired RPM: ", DesiredRPM, " RPM: ", RPM)
  print("Duty: ", duty)
  direction = "None" # Unused directional variable for rotary encoder
  # Monitors GPIO states for clock, switch, and data pins
  clkState = GPIO.input(clk)
  dtState = GPIO.input(dt)
  swState = GPIO.input(sw)
  debounce(clkState) # Debounces based on the clock state
  
  # Conditionals to monitor the states of clk dt and sw 
  if (swState != lastswState):
    if swState == False: # Detects a button press
      print("Press")
      on = True # Determines whether system is on or off based on rotary encoder press state
      countSpins()
      if(pressCount % 2 == 0):
        motor.start(duty) # Start the motor if system is on
        
      else:
        motor.stop() # Stop the motor if system is off
        on = False 
      pressCount += 1 # Accumulates the amount of button pressed for later use
      time.sleep(0.2) # Part of debouncing
  
  if (clkState != lastClkState):
    if (dtState != clkState):
      if(DesiredRPM < 2525 and on): # If the desired RPM is within the upper threshold
        DesiredRPM += 25 # Increment by 25 RPM for one turn of rotary encoder
        duty = math.exp((DesiredRPM + 2165.539) / 1022.3302) # Exponential function determined from excel transfer function
        motor.start(duty) # Start the motor
        countSpins() # Use IR sensor to count the spins
        print("Desired RPM: ", DesiredRPM, " RPM: ", RPM)
        print("Duty: ", duty)
      
    else:
      if(duty > 18 and on): # If the desired RPM is within the lower threshold
        DesiredRPM -= 25 # Decrement 25 RPM for one turn of rotary encoder
        duty = math.exp((DesiredRPM + 2165.539) / 1022.3302) # Exponential function determined from excel transfer function
        motor.start(duty) # Start the motor
        countSpins() # Use IR sensor to count the spins
        print("Desired RPM: ", DesiredRPM, " RPM: ", RPM)
        print("Duty: ", duty)
    
    lastClkState=clkState # Reset clock state
    

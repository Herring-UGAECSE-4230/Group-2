import RPi.GPIO as GPIO
import time

#GPIO Setup
GPIO.setmode(GPIO.BCM)
clk =22
dt = 27
sw = 17
GPIO.setup([clk,dt,sw], GPIO.IN)

#Allowing for dt and clk to have an internal pull up
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#start time to track turns per second
start = time.time()


#deobounce method
def debounce():
  time.sleep(.01)
    

#defining last state and intializing the counter
counter=0
lastClkState=GPIO.input(clk)
lastswState=GPIO.input(sw)


#main loop to monitor encoder
while True:
  debounce()
  direction = "none"
  #monitors gpio states
  clkState=GPIO.input(clk)
  dtState=GPIO.input(dt)
  swState=GPIO.input(sw)
  #the condionals to monitor the states of clk dt and sw 
  if swState!=lastswState:
    if swState == False:
      print("Press")
      time.sleep(0.1)
      debounce()
  if clkState!=lastClkState:
    if dtState!=clkState:
      counter+=1
      direction = "Clockwise"
    else:
      counter-=1
      direction = "CounterClockwise"
    lastClkState=clkState
  
  later = time.time()+1
  turns = counter / (time.time()-start)
  print("Direction: ", direction,"Counter: ", counter, "Turns per second", turns)
  
  

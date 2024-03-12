import RPi.GPIO as GPIO
import time
clk =12
dt = 27
sw = 22
GPIO.setup([clk,dt,sw], GPIO.IN)


GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)


def debounce():
  time.sleep(.01)
    

counter=0
lastClkState=GPIO.input(clk)
while True:
  clkState=GPIO.input(clk)
  dtState=GPIO.input(dt)
  if clkState!=lastClkState:
    if dtState!=clkState:
      counter+=1
      direction = "Clockwise"
    else:
      counter-=1
      direction = "CounterClockwise"
  lastClkState=clkState
  print(direction)
  print(counter)
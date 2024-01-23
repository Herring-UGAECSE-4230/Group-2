# Importing pigpio
import pigpio

# Selecting pi and setting frequency/duty cycle
pi = pigpio.pi()
pi.set_PWM_frequency(17, 500)
pi.set_PWM_dutycycle(17, 114.75)

# Empty the loop
while True:
    print(" ")
pi.set_PWM_dutycycle(17,0)

# Need to enable Daemon thread using "sudo pigpiod" in terminal
# To stop running use "sudo kill (insert PID here)"

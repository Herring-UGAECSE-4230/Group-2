#importing pigpio
import Pigpio

#selecting pi and setting frequency/duty cycle
pi = pigpio.pi()
pi.set_PWM_frequency(17, 100)
pi.set_PWM_dutycycle(17, 100)

while True:
    #empty loop\

pi.set_PWM_dutycycle(17,0)
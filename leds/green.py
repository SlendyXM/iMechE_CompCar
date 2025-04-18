import RPi.GPIO as io
import time

def LED_Green(power):
    pwm_pin = 42
    io.setup(pwm_pin, io.OUT)
    if power == True:
        io.output(pwm_pin, io.HIGH)
    else:
        io.output(pwm_pin, io.LOW)
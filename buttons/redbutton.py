import RPi.GPIO as io
import time

def single_target():
    pwm_pin = 44
    io.setup(pwm_pin, io.OUT, pull_up_down=io.PUD_UP)
    
    while True:
        if io.input(pwm_pin) == io.LOW:
            return True
        else:
            return False
        time.sleep(0.01)
import RPi.GPIO as io
import time

def cease_all_functions():
    pwm_pin = 45
    io.setup(pwm_pin, io.OUT, pull_up_down=io.PUD_UP)
    
    while True:
        if io.input(pwm_pin) == io.LOW:
            return True
        else:
            return False
        time.sleep(0.01)

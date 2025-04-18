import RPi.GPIO as io

def sound(power):
    pwm_pin = 43
    io.setup(pwm_pin, io.OUT)
    if power == True:
        io.output(pwm_pin, io.HIGH)
    else:
        io.output(pwm_pin, io.LOW)
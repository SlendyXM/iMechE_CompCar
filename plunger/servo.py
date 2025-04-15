import RPi.GPIO as io

class Servo():
    def __init__(self,pwm=8):
        self.pwm_pin = pwm
        io.setup(self.pwm_pin,io.OUT)
        if not hasattr(Servo, 'pwm'):
            Servo.pwm = io.PWM(self.pwm_pin, 50)
            Servo.pwm.start(0)

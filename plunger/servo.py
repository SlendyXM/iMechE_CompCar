import RPi.GPIO as io

class Servo():
    def __init__(self,pwm=8,vcc=10,grd=12):
        self.pwm_pin = pwm
        self.vcc = vcc
        self.grd = grd
        io.setup(self.pwm_pin,io.OUT)
        io.setup(self.vcc,io.OUT)
        io.setup(self.grd,io.OUT)
        io.output(self.vcc, io.HIGH)
        io.output(self.grd, io.LOW)
        if not hasattr(Servo, 'pwm'):
            Servo.pwm = io.PWM(self.pwm_pin, 50)
            Servo.pwm.start(7)
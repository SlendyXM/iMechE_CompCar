import RPi.GPIO as io

class Plunger():
    def __init__(self,pwm=8,in1=10,in2=12):
        self.pwm = pwm
        self.in1 = in1
        self.in2 = in2
        io.setup(self.pwm,io.OUT)
        io.setup(self.in1,io.OUT)
        io.setup(self.in2,io.OUT)
        self.pwm = io.PWM(self.pwm,1000)
        self.pwm.start(0)
import RPi.GPIO as io

class MotorD():
    def __init__(self,pwm=36,in1=38,in2=40):
        self.pwm = pwm
        self.in1 = in1
        self.in2 = in2
        io.setup(self.pwm,io.OUT)
        io.setup(self.in1,io.OUT)
        io.setup(self.in2,io.OUT)
        self.pwm = io.PWM(self.pwm,1000)
        self.pwm.start(0)
    
    def forward(self):
        io.output(self.in1, False)
        io.output(self.in2, True)

    def backward(self):
        io.output(self.in1, True)
        io.output(self.in2, False)

    def stop(self):
        io.output(self.in1, True)
        io.output(self.in2, True)

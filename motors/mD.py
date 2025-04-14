import RPi.GPIO as io

class MotorD():
    def __init__(self,pwm=36,in1=38,in2=40):
        self.pwm_pin = pwm
        self.in1 = in1
        self.in2 = in2
        io.setup(self.pwm_pin, io.OUT)
        io.setup(self.in1,io.OUT)
        io.setup(self.in2,io.OUT)
        if not hasattr(MotorD, 'pwm'):
            MotorD.pwm = io.PWM(self.pwm_pin, 1000)
            MotorD.pwm.start(0)
    
    def forward(self):
        io.output(self.in1, True)
        io.output(self.in2, False)

    def backward(self):
        io.output(self.in1, False)
        io.output(self.in2, True)

    def stop(self):
        io.output(self.in1, True)
        io.output(self.in2, True)

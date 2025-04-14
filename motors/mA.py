import RPi.GPIO as io

class MotorA():
    def __init__(self,pwm=11,in1=13,in2=15):
        self.pwm_pin = pwm
        self.in1 = in1
        self.in2 = in2
        io.setup(self.pwm_pin,io.OUT)
        io.setup(self.in1,io.OUT)
        io.setup(self.in2,io.OUT)
        if not hasattr(MotorA, 'pwm'):
            MotorA.pwm = io.PWM(self.pwm_pin, 1000)
            MotorA.pwm.start(0)
    
    def forward(self):
        io.output(self.in1, False)
        io.output(self.in2, True)

    def backward(self):
        io.output(self.in1, True)
        io.output(self.in2, False)

    def stop(self):
        io.output(self.in1, True)
        io.output(self.in2, True)

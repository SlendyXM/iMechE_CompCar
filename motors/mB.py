import RPi.GPIO as io

class MotorB():
    def __init__(self,pwm=19,in1=21,in2=23):
        self.pwm_pin = pwm
        self.in1 = in1
        self.in2 = in2
        io.setup(self.pwm_pin,io.OUT)
        io.setup(self.in1,io.OUT)
        io.setup(self.in2,io.OUT)
        if not hasattr(MotorB, 'pwm'):
            MotorB.pwm = io.PWM(self.pwm_pin, 1000)
            MotorB.pwm.start(0)
    
    def forward(self):
        io.output(self.in1, True)
        io.output(self.in2, False)

    def backward(self):
        io.output(self.in1, False)
        io.output(self.in2, True)

    def stop(self):
        io.output(self.in1, True)
        io.output(self.in2, True)
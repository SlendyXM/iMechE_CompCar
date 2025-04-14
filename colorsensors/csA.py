import RPi.GPIO as io
import time

class Color_SensorA():
    def __init__(self,s0=31,s1=29,s2=35,s3=33,out=37,oe=32):
        self.s0 = s0
        self.s1 = s1        
        self.s2 = s2        
        self.s3 = s3        
        self.oe = oe        # Output Enable
        self.out = out      # Output
        io.setup(self.s0, io.OUT)
        io.setup(self.s1, io.OUT)
        io.setup(self.s2, io.OUT)
        io.setup(self.s3, io.OUT)
        io.setup(self.oe, io.OUT)
        io.setup(self.out, io.IN, pull_up_down=io.PUD_UP)
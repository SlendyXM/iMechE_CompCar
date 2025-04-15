import RPi.GPIO as io
from colorsensors.csA import Color_SensorA
from colorsensors.csB import Color_SensorB
from colorsensors.csC import Color_SensorC

def red():
    io.output(Color_SensorA.s2, io.LOW)
    io.output(Color_SensorA.s3, io.LOW)
    io.output(Color_SensorB.s2, io.LOW)
    io.output(Color_SensorB.s3, io.LOW)
    io.output(Color_SensorC.s2, io.LOW)
    io.output(Color_SensorC.s3, io.LOW)

def blue():
    io.output(Color_SensorA.s2, io.HIGH)
    io.output(Color_SensorA.s3, io.HIGH)
    io.output(Color_SensorB.s2, io.HIGH)
    io.output(Color_SensorB.s3, io.HIGH)
    io.output(Color_SensorC.s2, io.HIGH)
    io.output(Color_SensorC.s3, io.HIGH)

def green():
    io.output(Color_SensorA.s2, io.LOW)
    io.output(Color_SensorA.s3, io.HIGH)
    io.output(Color_SensorB.s2, io.LOW)
    io.output(Color_SensorB.s3, io.HIGH)
    io.output(Color_SensorC.s2, io.LOW)
    io.output(Color_SensorC.s3, io.HIGH)
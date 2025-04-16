import RPi.GPIO as io
from colorsensors.csA import Color_SensorA
#from colorsensors.csB import Color_SensorB
#from colorsensors.csC import Color_SensorC

colorsensorA = Color_SensorA()
#colorsensorB = Color_SensorB()
#colorsensorC = Color_SensorC()

def red():
    io.output(colorsensorA.s2, io.LOW)
    io.output(colorsensorA.s3, io.LOW)
    #io.output(colorsensorB.s2, io.LOW)
    #io.output(colorsensorB.s3, io.LOW)
    #io.output(colorsensorC.s2, io.LOW)
    #io.output(colorsensorC.s3, io.LOW)

def green():
    io.output(colorsensorA.s2, io.HIGH)
    io.output(colorsensorA.s3, io.HIGH)
    #io.output(colorsensorB.s2, io.HIGH)
    #io.output(colorsensorB.s3, io.HIGH)
    #io.output(colorsensorC.s2, io.HIGH)
    #io.output(colorsensorC.s3, io.HIGH)

def blue():
    io.output(colorsensorA.s2, io.LOW)
    io.output(colorsensorA.s3, io.HIGH)
    #io.output(colorsensorB.s2, io.LOW)
    #io.output(colorsensorB.s3, io.HIGH)
    #io.output(colorsensorC.s2, io.LOW)
    #io.output(colorsensorC.s3, io.HIGH)
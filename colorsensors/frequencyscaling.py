import RPi.GPIO as io
from colorsensors.csA import Color_SensorA
from colorsensors.csB import Color_SensorB
from colorsensors.csC import Color_SensorC

colorsensorA = Color_SensorA()
colorsensorB = Color_SensorB()
colorsensorC = Color_SensorC()

def frequency_scaling_0percent():
    io.output(colorsensorA.s0, io.LOW)
    io.output(colorsensorA.s1, io.LOW)
    io.output(colorsensorB.s0, io.LOW)
    io.output(colorsensorB.s1, io.LOW)
    io.output(colorsensorC.s0, io.LOW)
    io.output(colorsensorC.s1, io.LOW)

def frequency_scaling_2percent():
    io.output(colorsensorA.s0, io.LOW)
    io.output(colorsensorA.s1, io.HIGH)
    io.output(colorsensorB.s0, io.LOW)
    io.output(colorsensorB.s1, io.HIGH)
    io.output(colorsensorC.s0, io.LOW)
    io.output(colorsensorC.s1, io.HIGH)

def frequency_scaling_20percent():
    io.output(colorsensorA.s0, io.HIGH)
    io.output(colorsensorA.s1, io.LOW)
    io.output(colorsensorB.s0, io.HIGH)
    io.output(colorsensorB.s1, io.LOW)
    io.output(colorsensorC.s0, io.HIGH)
    io.output(colorsensorC.s1, io.LOW)

def frequency_scaling_100percent():
    io.output(colorsensorA.s0, io.HIGH)
    io.output(colorsensorA.s1, io.HIGH)
    io.output(colorsensorB.s0, io.HIGH)
    io.output(colorsensorB.s1, io.HIGH)
    io.output(colorsensorC.s0, io.HIGH)
    io.output(colorsensorC.s1, io.HIGH)
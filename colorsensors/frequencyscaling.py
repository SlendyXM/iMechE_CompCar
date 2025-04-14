import RPi.GPIO as io
from csA import Color_SensorA
from csB import Color_SensorB
from csC import Color_SensorC

def frequency_scaling_0percent():
    io.output(Color_SensorA.s0, io.LOW)
    io.output(Color_SensorA.s1, io.LOW)
    io.output(Color_SensorB.s0, io.LOW)
    io.output(Color_SensorB.s1, io.LOW)
    io.output(Color_SensorC.s0, io.LOW)
    io.output(Color_SensorC.s1, io.LOW)

def frequency_scaling_2percent():
    io.output(Color_SensorA.s0, io.LOW)
    io.output(Color_SensorA.s1, io.HIGH)
    io.output(Color_SensorB.s0, io.LOW)
    io.output(Color_SensorB.s1, io.HIGH)
    io.output(Color_SensorC.s0, io.LOW)
    io.output(Color_SensorC.s1, io.HIGH)

def frequency_scaling_20percent():
    io.output(Color_SensorA.s0, io.HIGH)
    io.output(Color_SensorA.s1, io.LOW)
    io.output(Color_SensorB.s0, io.HIGH)
    io.output(Color_SensorB.s1, io.LOW)
    io.output(Color_SensorC.s0, io.HIGH)
    io.output(Color_SensorC.s1, io.LOW)

def frequency_scaling_100percent():
    io.output(Color_SensorA.s0, io.HIGH)
    io.output(Color_SensorA.s1, io.HIGH)
    io.output(Color_SensorB.s0, io.HIGH)
    io.output(Color_SensorB.s1, io.HIGH)
    io.output(Color_SensorC.s0, io.HIGH)
    io.output(Color_SensorC.s1, io.HIGH)
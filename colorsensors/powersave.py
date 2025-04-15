import RPi.GPIO as io
from colorsensors.csA import Color_SensorA
from colorsensors.csB import Color_SensorB
from colorsensors.csC import Color_SensorC

def enterpowersave():
    io.setup(Color_SensorA.oe, io.HIGH)
    io.setup(Color_SensorB.oe, io.HIGH)
    io.setup(Color_SensorC.oe, io.HIGH)

def exitpowersave():
    io.setup(Color_SensorA.oe, io.LOW)
    io.setup(Color_SensorB.oe, io.LOW)
    io.setup(Color_SensorC.oe, io.LOW)
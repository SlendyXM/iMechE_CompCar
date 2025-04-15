import RPi.GPIO as io
from colorsensors.csA import Color_SensorA
#from colorsensors.csB import Color_SensorB
#from colorsensors.csC import Color_SensorC

colorsensorA = Color_SensorA()
#colorsensorB = Color_SensorB()
#colorsensorC = Color_SensorC()

def enterpowersave():
    io.setup(colorsensorA.oe, io.HIGH)
    #io.setup(colorsensorB.oe, io.HIGH)
    #io.setup(colorsensorC.oe, io.HIGH)

def exitpowersave():
    io.setup(colorsensorA.oe, io.LOW)
    #io.setup(colorsensorB.oe, io.LOW)
    #io.setup(colorsensorC.oe, io.LOW)
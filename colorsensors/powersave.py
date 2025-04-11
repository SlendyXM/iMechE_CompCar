import RPi.GPIO as io
from cspin import color_sensor_pin
from csB import Color_SensorB
from csC import Color_SensorC

def enterpowersave():
    io.setup(color_sensor_pin.oe, io.HIGH)
    io.setup(Color_SensorB.oe, io.HIGH)
    io.setup(Color_SensorC.oe, io.HIGH)

def exitpowersave():
    io.setup(color_sensor_pin.oe, io.LOW)
    io.setup(Color_SensorB.oe, io.LOW)
    io.setup(Color_SensorC.oe, io.LOW)
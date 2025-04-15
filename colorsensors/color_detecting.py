import RPi.GPIO as io
import time
from colorsensors.csA import Color_SensorA
from colorsensors.csB import Color_SensorB
from colorsensors.csC import Color_SensorC
from colorsensors.colorfilter import red, blue, green

cycle = 10

def color_detecting():
    while True:
        red()
        time.sleep(0.1)
        start = time.time()
        for impulse_count in range(cycle):
            io.wait_for_edge(Color_SensorA.out, io.FALLING)
        duration = time.time() - start
        red_value = cycle / duration
        print(f"R:{red_value}")

        blue()
        time.sleep(0.1)
        start = time.time()
        for impulse_count in range(cycle):
            io.wait_for_edge(Color_SensorA.out, io.FALLING)
        duration = time.time() - start
        blue_value = cycle / duration
        print(f"B:{blue_value}")

        green()
        time.sleep(0.1)
        start = time.time()
        for impulse_count in range(cycle):
            io.wait_for_edge(Color_SensorA.out, io.FALLING)
        duration = time.time() - start
        green_value = cycle / duration
        print(f"G:{green_value}")

        time.sleep(0.2)
import RPi.GPIO as io
import time
from colorsensors.csA import Color_SensorA
#from colorsensors.csB import Color_SensorB
#from colorsensors.csC import Color_SensorC
from colorsensors.colorfilter import red, blue, green

colorsensorA = Color_SensorA()
#colorsensorB = Color_SensorB()
#colorsensorC = Color_SensorC()

cycle = 10

def color_detecting():
    temp = 1
    while (1):
        red()
        time.sleep(0.05)
        start = time.time()
        for impulse_count in range(cycle):
            io.wait_for_edge(colorsensorA.out, io.FALLING)
        duration = time.time() - start
        red_value = cycle / duration

        blue()
        time.sleep(0.05)
        start = time.time()
        for impulse_count in range(cycle):
            io.wait_for_edge(colorsensorA.out, io.FALLING)
        duration = time.time() - start
        blue_value = cycle / duration

        green()
        time.sleep(0.05)
        start = time.time()
        for impulse_count in range(cycle):
            io.wait_for_edge(colorsensorA.out, io.FALLING)
        duration = time.time() - start
        green_value = cycle / duration
        
        print(f"R:{red_value: .2f} G:{green_value: .2f} B:{blue_value: .2f}")

        if red_value >= 300 and green_value >= 300 and blue_value >= 300:
            temp += 1
            print("white")
            if temp > 4:
                print("white")
                temp = 1
        elif red_value <= 300 and green_value <= 300 and blue_value <= 300:
            temp += 1
            print("black")
            if temp > 4:
                print("black")
                temp = 1
        elif red_value < blue_value and green_value < blue_value and blue_value >= 300:
            temp += 1
            print("blue")
            if temp > 4:
                print("blue")
                temp = 1
        elif red_value >= 300 and green_value < red_value and blue_value < red_value:
            temp += 1
            print("red")
            if temp > 4:
                print("red")
                temp = 1
        else:
            temp += 1
            print("wood")
            if temp > 4:
                print("wood")
                temp = 1

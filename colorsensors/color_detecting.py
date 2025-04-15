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
    while True:
        io.output(colorsensorA.s2, io.LOW)
        io.output(colorsensorA.s3, io.LOW)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(cycle):
            io.wait_for_edge(colorsensorA.out, io.FALLING)
        duration = time.time() - start
        red_value = cycle / duration
        #print(f"R:{red_value}")

        blue()
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(cycle):
            io.wait_for_edge(colorsensorA.out, io.FALLING)
        duration = time.time() - start
        blue_value = cycle / duration
        #print(f"B:{blue_value}")

        green()
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(cycle):
            io.wait_for_edge(colorsensorA.out, io.FALLING)
        duration = time.time() - start
        green_value = cycle / duration
        #print(f"G:{green_value}")
        
        print(f"R:{red_value} G:{green_value} B:{blue_value}")

        '''if green_value < 7000 and blue_value < 7000 and red_value > 12000:
            print("red")
            temp = 1
        elif red_value < 12000 and blue_value < 12000 and green_value > 12000:
            print("green")
            temp = 1
        elif green_value <7000 and red_value < 7000 and blue_value > 12000:
            print("blue")
            temp = 1
        elif red_value > 10000 and green_value > 10000 and blue_value > 10000 and temp==1:
            print("place the object.....")
            temp = 0
        else:
            print("No matching condition for the current values.")'''

import RPi.GPIO as io
import time
from colorsensors.csA import Color_SensorA
#from colorsensors.csB import Color_SensorB
#from colorsensors.csC import Color_SensorC
#from colorsensors.csD import Color_SensorD
from colorsensors.colorfilter import red, blue, green

colorsensorA = Color_SensorA()
#colorsensorB = Color_SensorB()
#colorsensorC = Color_SensorC()
#colorsensorD = Color_SensorD()

cycle = 10

def detect_color(sensor, sensor_name):
    red()
    time.sleep(0.05)
    start = time.time()
    for impulse_count in range(cycle):
        io.wait_for_edge(sensor.out, io.FALLING)
    duration = time.time() - start
    red_value = cycle / duration

    blue()
    time.sleep(0.05)
    start = time.time()
    for impulse_count in range(cycle):
        io.wait_for_edge(sensor.out, io.FALLING)
    duration = time.time() - start
    blue_value = cycle / duration

    green()
    time.sleep(0.05)
    start = time.time()
    for impulse_count in range(cycle):
        io.wait_for_edge(sensor.out, io.FALLING)
    duration = time.time() - start
    green_value = cycle / duration

    print(f"{sensor_name} - R:{red_value:.2f} G:{green_value:.2f} B:{blue_value:.2f}")

    if red_value >= 300 and green_value >= 300 and blue_value >= 300:
        print(f"{sensor_name} - white")
        return "white"
    elif red_value <= 300 and green_value <= 300 and blue_value <= 300:
        print(f"{sensor_name} - black")
        return "black"
    elif red_value < blue_value and green_value < blue_value and blue_value >= 300:
        print(f"{sensor_name} - blue")
        return "blue"
    elif red_value >= 300 and green_value < red_value and blue_value < red_value:
        print(f"{sensor_name} - red")
        return "red"
    else:
        print(f"{sensor_name} - wood")
        return "wood"

def color_detecting():
    while True:
        # Detect color for Sensor A
        color_a = detect_color(colorsensorA, "Color Sensor A")
        print(f"Detected by Color Sensor A: {color_a}")

        '''# Detect color for Sensor B
        color_b = detect_color(colorsensorB, "Color Sensor B")
        print(f"Detected by Color Sensor B: {color_b}")

        # Detect color for Sensor C
        color_c = detect_color(colorsensorC, "Color Sensor C")
        print(f"Detected by Color Sensor C: {color_c}")

        # Detect color for Sensor D
        color_d = detect_color(colorsensorD, "Color Sensor D")
        print(f"Detected by Color Sensor D: {color_d}")'''

        # Check the specified conditions
        if color_a == "red": # and color_b == "blue" and color_c == "blue" and color_d == "black":
            print("Condition met: Sensor A is red, Sensor B and C are blue, Sensor D is black.")
            return True  # Break the loop and return True

        # If conditions are not met, output False
        print("Condition not met. Returning False.")
        return False




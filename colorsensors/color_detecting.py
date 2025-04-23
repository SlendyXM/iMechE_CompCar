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
    """Detect the color using the specified sensor with polling."""
    try:
        # Activate red filter and measure frequency
        red()
        time.sleep(0.05)
        start = time.time()
        red_value = measure_frequency(sensor.out, "red", sensor_name)

        # Activate blue filter and measure frequency
        blue()
        time.sleep(0.05)
        blue_value = measure_frequency(sensor.out, "blue", sensor_name)

        # Activate green filter and measure frequency
        green()
        time.sleep(0.05)
        green_value = measure_frequency(sensor.out, "green", sensor_name)

        # Print the detected values
        print(f"{sensor_name} - R:{red_value:.2f} G:{green_value:.2f} B:{blue_value:.2f}")

        # Determine the color based on the measured values
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
    except RuntimeError as e:
        print(f"Error detecting color for {sensor_name}: {e}")
        return None


def measure_frequency(pin, color, sensor_name):
    """Measure the frequency of falling edges on the specified GPIO pin."""
    impulse_count = 0
    timeout = 1  # Timeout in seconds
    start_time = time.time()
    previous_state = io.input(pin)

    while time.time() - start_time < timeout:
        current_state = io.input(pin)
        if previous_state == io.HIGH and current_state == io.LOW:
            impulse_count += 1
        previous_state = current_state

    if impulse_count == 0:
        print(f"{sensor_name} - No impulses detected for {color} filter.")
    return impulse_count / timeout  # Frequency in Hz


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




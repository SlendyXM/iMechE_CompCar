import RPi.GPIO as io
import time
'''io.setmode(io.BOARD)
io.setup(3, io.OUT)
io.output(3, io.HIGH)'''
from colorsensors.csA import Color_SensorA
from colorsensors.frequencyscaling import frequency_scaling_20percent
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
        if red_value >= 100 and green_value >= 100 and blue_value >= 100:
            print(f"{sensor_name} - white")
            return "white"
        elif red_value <= 35 and green_value <= 35 and blue_value <= 35:
            print(f"{sensor_name} - black")
            return "black"
        elif red_value >= 60 and green_value >= 60 and blue_value >= 60:
            print(f"{sensor_name} - wood")
            return "wood"
        elif red_value < blue_value and green_value < blue_value and blue_value >= 60:
            print(f"{sensor_name} - blue")
            return "blue"
        elif red_value >= 60 and green_value < red_value and blue_value < red_value:
            print(f"{sensor_name} - red")
            return "red"
        else:
            print(f"{sensor_name} - wood")
            return "wood"
    except RuntimeError as e:
        print(f"Error detecting color for {sensor_name}: {e}")
        return None


def measure_frequency(pin, color, sensor_name, timeout = 0.01): # Timeout = 0.01s
    """Measure the frequency of falling edges on the specified GPIO pin."""
    impulse_count = 0
    start_time = time.time()
    previous_state = io.input(pin)

    while time.time() - start_time < timeout:
        current_state = io.input(pin)
        if previous_state == io.HIGH and current_state == io.LOW:
            impulse_count += 0.1
        previous_state = current_state
        time.sleep(0.0001)  # Small delay to avoid busy-waiting

    if impulse_count == 0:
        print(f"{sensor_name} - No impulses detected for {color} filter.")
    return impulse_count / timeout  # Frequency in Hz

'''
import threading

def measure_frequency(pin, color, sensor_name, timeout=0.03):
    """Measure the frequency of falling edges on the specified GPIO pin using event detection."""
    impulse_count = 0

    def edge_callback(channel):
        nonlocal impulse_count
        impulse_count += 1

    # Set up event detection for falling edges
    io.add_event_detect(pin, io.FALLING, callback=edge_callback)

    # Wait for the specified timeout
    time.sleep(timeout)

    # Remove event detection to clean up
    io.remove_event_detect(pin)

    if impulse_count == 0:
        print(f"{sensor_name} - No impulses detected for {color} filter.")
    return impulse_count / timeout  # Frequency in Hz




def measure_frequency_parallel(sensor, color, sensor_name, result_dict):
    """Measure frequency for a specific color filter in a separate thread."""
    result_dict[color] = measure_frequency(sensor.out, color, sensor_name)

def detect_color_parallel(sensor, sensor_name):
    """Detect the color using the specified sensor with parallel polling."""
    try:
        # Activate filters and measure frequencies in parallel
        result_dict = {}
        threads = []

        # Red filter
        red()
        red_thread = threading.Thread(target=measure_frequency_parallel, args=(sensor, "red", sensor_name, result_dict))
        threads.append(red_thread)
        red_thread.start()

        # Blue filter
        blue()
        blue_thread = threading.Thread(target=measure_frequency_parallel, args=(sensor, "blue", sensor_name, result_dict))
        threads.append(blue_thread)
        blue_thread.start()

        # Green filter
        green()
        green_thread = threading.Thread(target=measure_frequency_parallel, args=(sensor, "green", sensor_name, result_dict))
        threads.append(green_thread)
        green_thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Retrieve measured values
        red_value = result_dict.get("red", 0)
        blue_value = result_dict.get("blue", 0)
        green_value = result_dict.get("green", 0)

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
        return None'''

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

if __name__ == "__main__":
    frequency_scaling_20percent()
    while True:
        color_detecting()
    io.cleanup([3, 29, 31, 33 ,35, 37 ,32])



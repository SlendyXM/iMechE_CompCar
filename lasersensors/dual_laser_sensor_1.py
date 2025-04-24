import serial
from serial import Serial
import re
import time


def setup_serial(port, baudrate=115200, timeout=1):
    """Initialize serial connection with error handling."""
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        ser.flushInput()  # Clear input buffer
        ser.flushOutput()  # Clear output buffer
        print(f"Connected to {port} at {baudrate} baud")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None


def parse_sensor_data(line, sensor_state):
    """Parse a single line of sensor data and update validity state."""
    line = line.strip()
    distance_match = re.search(r'd:\s*(\d+)\s*mm', line, re.IGNORECASE)
    state_match = re.search(r'State:(\d+)', line, re.IGNORECASE)
    distance = None

    # Update validity state if state information is present
    if state_match:
        if state_match.group(1) == '0' and "Range Valid" in line:
            sensor_state['is_valid'] = True
        else:
            sensor_state['is_valid'] = False

    # Extract distance if present
    if distance_match:
        distance = int(distance_match.group(1))

    return distance, sensor_state['is_valid']


def read_sensor_data(ser, sensor_state, sensor_id):
    """Read and process data from a sensor."""
    try:
        raw_data_1 = ser.readline()  # First line
        raw_data_2 = ser.readline()  # Second line

        if raw_data_1 and raw_data_2:
            try:
                line_1 = raw_data_1.decode('utf-8', errors='replace')
                line_2 = raw_data_2.decode('utf-8', errors='replace')
                combined_line = f"{line_1.strip()} {line_2.strip()}"
                distance, is_valid = parse_sensor_data(combined_line, sensor_state)
                return distance, is_valid
            except UnicodeDecodeError:
                return None, False
        else:
            return None, sensor_state['is_valid']
    except serial.SerialException:
        return None, False


def compare_distances(distance1, distance2, offset):
    """Compare distances from two sensors and return rotation command."""
    if distance1 is None or distance2 is None:
        return "No rotation: Missing distance data"

    difference = (distance1 - distance2)/distance1

    if difference > 0.2:
        print(f'Distance 1:{distance1} -- Distance 2: {distance2} -- Offset{difference}')
        return "Anticlockwise"
        
    elif difference < -0.2:
        print(f'Distance 1:{distance1} -- Distance 2: {distance2} -- Offset{difference}')
        return "Clockwise"
    else:
        print(f'Distance 1:{distance1} -- Distance 2: {distance2} -- Offset{difference}')
        return "Parallel"


def process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state, offset=-43):
    """Process data from both sensors and return the rotation command."""
    # Read and process data from sensor 1
    distance1, is_valid1 = read_sensor_data(sensor1, sensor1_state, "ACM0")

    # Read and process data from sensor 2
    distance2, is_valid2 = read_sensor_data(sensor2, sensor2_state, "ACM1")

    # Check for stop condition
    if distance1 is not None and distance2 is not None:
        if distance1 <= 55 or distance2 <= 55:
            return "stop"

    # Compare distances and return rotation command
    rotation_command = compare_distances(distance1, distance2, offset)
    return rotation_command


if __name__ == "__main__":
    # Initialize both sensors
    sensor1 = setup_serial('/dev/ttyACM0')
    sensor2 = setup_serial('/dev/ttyACM1')
    offset = -43  # Constant error

    # Check if both sensors are initialized
    if not sensor1 or not sensor2:
        print("Failed to initialize one or both serial connections")
        if sensor1:
            sensor1.close()
        if sensor2:
            sensor2.close()
        exit()

    # Initialize state tracking for each sensor
    sensor1_state = {'is_valid': False, 'id': 'ACM0'}
    sensor2_state = {'is_valid': False, 'id': 'ACM1'}

    time.sleep(1.5)  # Wait for sensors to stabilize

    try:
        while True:
            # Process laser data and get the rotation command
            command = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state, offset)
            print(f"Action: {command}")

            # Exit loop if stop condition is met
            if command == "stop":
                break

            time.sleep(0.01)  # Minimal delay to reduce CPU load
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        # Close both serial ports
        if sensor1:
            sensor1.close()
            print("Sensor ACM0 serial port closed")
        if sensor2:
            sensor2.close()
            print("Sensor ACM1 serial port closed")

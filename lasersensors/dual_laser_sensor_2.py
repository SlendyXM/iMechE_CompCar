import serial
from serial import Serial
import re
import time

def setup_serial(port, baudrate=115200, timeout=0.05):
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

    if state_match:
        if state_match.group(1) == '0' and "Range Valid" in line:
            sensor_state['is_valid'] = True
        else:
            sensor_state['is_valid'] = False

    if distance_match:
        distance = int(distance_match.group(1))

    return distance, sensor_state['is_valid']

def read_sensor_data(ser, sensor_state):
    """Read and process data from a sensor."""
    try:
        raw_data_1 = ser.readline()
        raw_data_2 = ser.readline()

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

def compare_distances(distance1, distance2):
    """Compare distances from two sensors using zone-based logic."""
    if distance1 is None or distance2 is None:
        return "No rotation: Missing distance data", 0

    offset = distance2 - distance1
    avg_distance = (distance1 + distance2) / 2

    if avg_distance < 200:
        if offset < 30:
            command = "Anticlockwise"
        elif offset > 40:
            command = "Clockwise"
        else:
            command = "Parallel"

    elif avg_distance < 500:
        if offset < 40:
            command = "Anticlockwise"
        elif offset > 50:
            command = "Clockwise"
        else:
            command = "Parallel"

    elif avg_distance < 1000:
        if offset < 45:
            command = "Anticlockwise"
        elif offset > 60:
            command = "Clockwise"
        else:
            command = "Parallel"

    elif avg_distance < 1600:
        if offset < 50:
            command = "Anticlockwise"
        elif offset > 70:
            command = "Clockwise"
        else:
            command = "Parallel"

    elif avg_distance < 2600:
        if offset < 60:
            command = "Anticlockwise"
        elif offset > 80:
            command = "Clockwise"
        else:
            command = "Parallel"

    else:
        command = "Parallel"  # Ignore high-distance noise

    print(f"Distance1: {distance1} -- Distance2: {distance2} -- Offset: {offset} -- AvgDist: {avg_distance:.1f} => Action: {command}")
    return command,avg_distance

def process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state):
    """Process data from both sensors and return the rotation command."""
    distance1, is_valid1 = read_sensor_data(sensor1, sensor1_state)
    distance2, is_valid2 = read_sensor_data(sensor2, sensor2_state)

    if distance1 is not None and distance2 is not None:
        if distance1 <= 55 or distance2 <= 95:
            return "stop",distance1

    rotation_command, average_distance = compare_distances(distance1, distance2)
    return rotation_command, average_distance

if __name__ == "__main__":
    sensor1 = setup_serial('/dev/ttyACM0')
    sensor2 = setup_serial('/dev/ttyACM1')

    if not sensor1 or not sensor2:
        print("Failed to initialize one or both serial connections")
        if sensor1:
            sensor1.close()
        if sensor2:
            sensor2.close()
        exit()

    sensor1_state = {'is_valid': False, 'id': 'ACM0'}
    sensor2_state = {'is_valid': False, 'id': 'ACM1'}

    time.sleep(1.5)  # Allow sensors to stabilize

    try:
        while True:
            command, average = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
            if average == 0:
                continue
            print(f"Action: {command} average {average}")

            if command == "stop":
                break

            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        if sensor1:
            sensor1.close()
            print("Sensor ACM0 serial port closed")
        if sensor2:
            sensor2.close()
            print("Sensor ACM1 serial port closed")

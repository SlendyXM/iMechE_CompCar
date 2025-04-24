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
    # Make regex more robust: case-insensitive, flexible spacing
    distance_match = re.search(r'd:\s*(\d+)\s*mm', line, re.IGNORECASE)
    state_match = re.search(r'State:(\d+)', line, re.IGNORECASE)
    distance = None
    
    # Update validity state if state information is present
    if state_match:
        if state_match.group(1) == '0' and "Range Valid" in line:
            sensor_state['is_valid'] = True
            print(f"Updated {sensor_state['id']} validity: Valid")
        else:
            sensor_state['is_valid'] = False
            print(f"Updated {sensor_state['id']} validity: Invalid")
    
    # Extract distance if present
    if distance_match:
        distance = int(distance_match.group(1))
        print(f"Parsed {sensor_state['id']} distance: {distance} mm")
    else:
        print(f"No distance match in {sensor_state['id']} line: '{line}'")
    
    return distance, sensor_state['is_valid']

def read_sensor1_data(ser, sensor_state):
    """Read and process data from sensor 1 (ACM0)."""
    try:
        # Read one line at a time
        raw_data_1 = ser.readline()  # First line
        raw_data_2 = ser.readline()  # Second line

        if raw_data_1 and raw_data_2:
            print(f"Sensor ACM0 Raw data (line 1): {raw_data_1}")  # Debug: Print first raw line
            print(f"Sensor ACM0 Raw data (line 2): {raw_data_2}")  # Debug: Print second raw line

            try:
                # Decode both lines
                line_1 = raw_data_1.decode('utf-8', errors='replace')
                line_2 = raw_data_2.decode('utf-8', errors='replace')
                print(f"Sensor ACM0 Decoded (line 1): {line_1}")  # Debug: Print first decoded line
                print(f"Sensor ACM0 Decoded (line 2): {line_2}")  # Debug: Print second decoded line

                # Combine the two lines for parsing
                combined_line = f"{line_1.strip()} {line_2.strip()}"
                print(f"Sensor ACM0 Combined: {combined_line}")  # Debug: Print combined line

                distance, is_valid = parse_sensor_data(combined_line, sensor_state)
                return distance, is_valid
            except UnicodeDecodeError as e:
                print(f"Sensor ACM0 Decode error: {e}")
                return None, False
        else:
            print(f"Sensor ACM0: No data in buffer")
            return None, sensor_state['is_valid']
    except serial.SerialException as e:
        print(f"Sensor ACM0 Error reading serial data: {e}")
        return None, False

def read_sensor2_data(ser, sensor_state):
    """Read and process data from sensor 2 (ACM1)."""
    try:
        # Read one line at a time
        raw_data_1 = ser.readline()  # First line
        raw_data_2 = ser.readline()  # Second line

        if raw_data_1 and raw_data_2:
            print(f"Sensor ACM1 Raw data (line 1): {raw_data_1}")  # Debug: Print first raw line
            print(f"Sensor ACM1 Raw data (line 2): {raw_data_2}")  # Debug: Print second raw line

            try:
                # Decode both lines
                line_1 = raw_data_1.decode('utf-8', errors='replace')
                line_2 = raw_data_2.decode('utf-8', errors='replace')
                print(f"Sensor ACM1 Decoded (line 1): {line_1}")  # Debug: Print first decoded line
                print(f"Sensor ACM1 Decoded (line 2): {line_2}")  # Debug: Print second decoded line

                # Combine the two lines for parsing
                combined_line = f"{line_1.strip()} {line_2.strip()}"
                print(f"Sensor ACM1 Combined: {combined_line}")  # Debug: Print combined line

                distance, is_valid = parse_sensor_data(combined_line, sensor_state)
                return distance, is_valid
            except UnicodeDecodeError as e:
                print(f"Sensor ACM1 Decode error: {e}")
                return None, False
        else:
            print(f"Sensor ACM1: No data in buffer")
            return None, sensor_state['is_valid']
    except serial.SerialException as e:
        print(f"Sensor ACM1 Error reading serial data: {e}")
        return None, False
        
def compare_distances(distance1, distance2,offset):
    """Compare distances from ACM0 and ACM1 and return rotation command."""
    if distance1 is None or distance2 is None:
        return "No rotation: Missing distance data"
    
    difference = distance1 - distance2 + offset
    print(f"Distance difference (ACM0 - ACM1): {difference} mm")
    print(f"Offset ratio with distance 1 : {difference/distance1}")
    print(f"Offset ratio with distance 2 :{difference/distance2}")
    print(f"Offset ratio with average distance : {2*difference/(distance1+distance2)}")
    
    if difference > 5:
        return "Anticlockwise"
    elif difference < -5:
        return "Clockwise"
    else:
        return "Parallel"

def read_laser():
    # Initialize both sensors
    sensor1 = setup_serial('/dev/ttyACM0')
    sensor2 = setup_serial('/dev/ttyACM1')

    offset=90    #constant error

    # Check if both sensors are initialized
    if not sensor1 or not sensor2:
        print("Failed to initialize one or both serial connections")
        if sensor1:
            sensor1.close()
        if sensor2:
            sensor2.close()
        return
    
    # Initialize state tracking for each sensor
    sensor1_state = {'is_valid': False, 'id': 'ACM0'}
    sensor2_state = {'is_valid': False, 'id': 'ACM1'}
    
    time.sleep(0.1)  # Wait for sensors to stabilize
    
    try:
        while True:
            # Read and process data from sensor 1
            distance1, is_valid1 = read_sensor1_data(sensor1, sensor1_state)
            if distance1 is not None:
                status1 = "Valid" if is_valid1 else "Invalid"
                print(f"Sensor ACM0: Distance: {distance1} mm, Range: {status1}")
            else:
                print("Sensor ACM0: No distance data received")
            
            # Small delay to avoid overwhelming serial ports
            time.sleep(0.01)
            
            # Read and process data from sensor 2
            distance2, is_valid2 = read_sensor2_data(sensor2, sensor2_state)
            if distance2 is not None:
                status2 = "Valid" if is_valid2 else "Invalid"
                print(f"Sensor ACM1: Distance: {distance2} mm, Range: {status2}")
            else:
                print("Sensor ACM1: No distance data received")
            if distance1 and distance2 is not None:
                if distance1<=55 or distance2<=55:
                    return("stop")
            if distance1<=55 or distance2<=55:
                return("stop")
            # Compare distances and print rotation command
            rotation_command = compare_distances(distance1, distance2,offset)
            print(f"Action: {rotation_command}")
            if rotation_command is not None:
                return(rotation_command)
            else:
                return(None)
            print("-" * 40)  # Separator for clarity
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

if __name__ == "__main__":
    read_laser()

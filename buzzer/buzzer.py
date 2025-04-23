import serial
import time
from typing import List, Tuple, Optional

<<<<<<< HEAD
class PiDeviceController:
    def __init__(self, serial_port='/dev/ttyACM0', baudrate=115200, timeout=1):
        """
        Initialize the device controller for Raspberry Pi
        :param serial_port: Default is '/dev/ttyACM0'
        :param baudrate: Communication baud rate
        :param timeout: Serial timeout in seconds
        """
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        
        # Raspberry Pi specific serial setup
        self._enable_serial()
    def _enable_serial(self):
            """Enable serial interface on Raspberry Pi"""
            try:
                with open('/boot/cmdline.txt', 'r') as f:
                    cmdline = f.read().strip()
                if 'console=serial0' in cmdline:
                    print("Warning: Serial console is enabled in /boot/cmdline.txt")
                    print("Disable it by removing 'console=serial0,115200' and run: sudo raspi-config -> Interface Options -> Serial -> No")
            except Exception as e:
                print(f"Warning checking cmdline.txt: {e}")
    def connect(self):
        """Establish connection to the device"""
        try:
            self.ser = serial.Serial(
                port=self.serial_port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            print(f"Connected to {self.serial_port} at {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to {self.serial_port}: {e}")
            print("Possible solutions:")
            print("1. Ensure serial interface is enabled (sudo raspi-config)")
            print("2. Try /dev/ttyAMA0 for older Pi")
            print("3. Verify baud rate matches device")
            print("4. Ensure no other process uses the serial port")
            return False
    
    def disconnect(self):
        """Close the serial connection"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Connection closed")
    def send_command(self, command_bytes: bytes) -> bool:
        """Send a command to the device"""
        if not self.ser or not self.ser.is_open:
            print("Not connected to device")
            return False
        try:
            self.ser.write(command_bytes)
            print(f"Sent command: {self._format_hex(command_bytes)}")
            return True
        except serial.SerialException as e:
            print(f"Error sending command: {e}")
            return False
    
    def _format_hex(self, data: bytes) -> str:
        """Format bytes as hex string for display"""
        return ' '.join(f'0x{byte:02X}' for byte in data)
    
    def gpio_single_pin_config(self, pin_configs: List[Tuple[int, int, int]]) -> bool:
        """
        Configure single GPIO pins (Command 0x01)
        :param pin_configs: List of tuples (pin_num, pin_type, init_level)
        :return: True if command sent successfully
        """
        if len(pin_configs) > 16:
            print("Maximum 16 pin configurations allowed")
            return False
        command = bytearray([0x01])
        for pin_num, pin_type, init_level in pin_configs:
            if not (1 <= pin_num <= 16):
                print(f"Invalid pin number {pin_num}. Must be 1-16")
                return False
            if not (1 <= pin_type <= 5):
                print(f"Invalid pin type {pin_type}. Must be 1-5")
                return False
            if init_level not in (0, 1):
                print(f"Invalid init level {init_level}. Must be 0 or 1")
                return False
            command.extend([pin_num, pin_type, init_level])
        return self.send_command(command)
    
    def gpio_single_pin_set(self, pin_num: int, level: int) -> bool:
        """
        Set single GPIO pin level (Command 0x02)
        :param pin_num: Pin number to set (1-16)
        :param level: 0 (low) or 1 (high)
        :return: True if command sent successfully
        """
        if not (1 <= pin_num <= 16):
            print("Pin number must be between 1 and 16")
            return False
        if level not in (0, 1):
            print("Level must be 0 or 1")
            return False
        command = bytearray([0x02, pin_num, level])
        return self.send_command(command)
def main():
    print("Raspberry Pi Buzzer and LED Controller")
    print("--------------------------------------")
    
    # Default serial port and baud rate
    default_port = '/dev/ttyACM0'
    baudrate = 115200
    
    # Initialize controller
    controller = PiDeviceController(serial_port=default_port, baudrate=baudrate)
    
    if not controller.connect():
        print("Exiting due to connection failure")
        return
    
    try:
        # Configure pins: pin 1 (buzzer) and pin 2 (LED) as outputs (pin_type=1) with initial level low (0)
        pin_configs = [
            (1, 1, 0),  # Buzzer: pin 1, output, initially low
            (2, 1, 0)   # LED: pin 2, output, initially low
        ]
        if not controller.gpio_single_pin_config(pin_configs):
            print("Failed to configure pins")
            controller.disconnect()
            return
        
        print("Buzzer and LED configured. Starting toggle sequence...")
        print("Press Ctrl+C to stop")
        
        # Toggle buzzer and LED alternately
        while True:
            # Turn buzzer ON, LED OFF
            controller.gpio_single_pin_set(1, 1)  # Buzzer ON
            controller.gpio_single_pin_set(2, 0)  # LED OFF
            print("Buzzer ON, LED OFF")
            time.sleep(1)  # Wait 1 second
            
            # Turn buzzer OFF, LED ON
            controller.gpio_single_pin_set(1, 0)  # Buzzer OFF
            controller.gpio_single_pin_set(2, 1)  # LED ON
            print("Buzzer OFF, LED ON")
            time.sleep(1)  # Wait 1 second
    
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        # Turn off both buzzer and LED before exiting
        controller.gpio_single_pin_set(1, 0)
        controller.gpio_single_pin_set(2, 0)
        print("Buzzer and LED turned OFF")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        controller.disconnect()

if __name__ == "__main__":
    main()
=======
io.setmode(io.BOARD)
io.setup(3, io.OUT)  # STBY
io.setup(12, io.OUT)
io.setup(16, io.OUT)
io.output(3, io.HIGH)  # enable board


while True:
    io.output(12, io.HIGH)
    io.output(16, io.LOW)
    io.output(12, io.LOW)
    io.output(16, io.HIGH)
    
>>>>>>> 05c4280175885e6a75e4cdd84f40adc3bde340a7

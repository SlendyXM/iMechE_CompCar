import serial
import time
import struct
import RPi.GPIO as GPIO
from typing import List, Tuple, Optional

class PiDeviceController:
    def _init_(self, serial_port='/dev/ttyACM0', baudrate=115200, timeout=1):
        """
        Initialize the device controller for Raspberry Pi
        :param serial_port: Default is '/dev/ttyS0' for Pi 3/4, '/dev/ttyAMA0' for older Pi
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
            # Disable console over serial (may require sudo)
            with open('/boot/cmdline.txt', 'r') as f:
                cmdline = f.read().strip()
            
            if 'console=serial0' in cmdline:
                print("Warning: Serial console is enabled in /boot/cmdline.txt")
                print("For reliable communication, you should disable it by removing 'console=serial0,115200'")
                print("Then run: sudo raspi-config -> Interface Options -> Serial -> No")
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
            print("1. Make sure the serial interface is enabled (sudo raspi-config)")
            print("2. Check if you're using the correct port (try /dev/ttyAMA0 for older Pi)")
            print("3. Verify your baud rate matches the device")
            print("4. Ensure no other process is using the serial port")
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
        if 41<=pin_num<=56:
            pin_num=pin_num-40        
        elif not (1 <= pin_num <= 16):
            print("Pin number must be between 1 and 16")
            return False
        if level not in (0, 1):
            print("Level must be 0 or 1")
            return False
            
        command = bytearray([0x02, pin_num, level])
        return self.send_command(command)
    
    def gpio_bulk_set(self, pin_levels: List[int]) -> bool:
        """
        Set multiple GPIO pins at once (Command 0x03)
        :param pin_levels: List of pin numbers to set high (others will be low)
        :return: True if command sent successfully
        """
        # Create a 16-bit mask (for pins 1-16)
        mask = 0
        for pin in pin_levels:
            if 1 <= pin <= 16:
                mask |= 1 << (pin - 1)
            else:
                print(f"Ignoring invalid pin number {pin}")
        
        # Split into 2 bytes (little-endian)
        byte1 = mask & 0xFF
        byte2 = (mask >> 8) & 0xFF
        command = bytearray([0x03, byte1, byte2])
        
        return self.send_command(command)
    
    def gpio_status_read(self) -> bool:
        """Read GPIO status (Command 0x11)"""
        return self.send_command(bytearray([0x11]))
    
    def pwm_group_config(self, group_num: int, resolution: int, period: int, 
                        active_level: int, idle_level: int) -> bool:
        """
        Configure PWM group (Command 0x21)
        :param group_num: PWM group number (1-3)
        :param resolution: PWM resolution (0-65535)
        :param period: PWM period count (32-bit value)
        :param active_level: 4-bit value for active levels of pins in group
        :param idle_level: 4-bit value for idle levels of pins in group
        :return: True if command sent successfully
        """
        if not (1 <= group_num <= 3):
            print("Group number must be 1, 2, or 3")
            return False
        if not (0 <= resolution <= 65535):
            print("Resolution must be between 0 and 65535")
            return False
        if not (0 <= active_level <= 0b1111):
            print("Active level must be a 4-bit value (0-15)")
            return False
        if not (0 <= idle_level <= 0b1111):
            print("Idle level must be a 4-bit value (0-15)")
            return False
        
        # Combine active and idle levels
        px_level = ((active_level & 0x0F) << 4) | (idle_level & 0x0F)
        
        command = bytearray([0x21, group_num])
        command.extend(resolution.to_bytes(2, 'little'))
        command.extend(period.to_bytes(4, 'little'))
        command.append(px_level)
        
        return self.send_command(command)
    
    def pwm_duty_cycle_set(self, group_num: int, duty_cycles: List[int]) -> bool:
        """
        Set PWM duty cycles (Command 0x22)
        :param group_num: PWM group number (1-3)
        :param duty_cycles: List of 4 duty cycle counts (32-bit values each)
        :return: True if command sent successfully
        """
        if not (1 <= group_num <= 3):
            print("Group number must be 1, 2, or 3")
            return False
        if len(duty_cycles) != 4:
            print("Exactly 4 duty cycles required")
            return False
        
        command = bytearray([0x22, group_num])
        for duty in duty_cycles:
            command.extend(duty.to_bytes(4, 'little'))
        
        return self.send_command(command)
    
    def pwm_group_control(self, group_num: int, state: int) -> bool:
        """
        Control PWM group output (Command 0x23)
        :param group_num: PWM group number (1-3)
        :param state: 0 (stop) or 1 (start)
        :return: True if command sent successfully
        """
        if not (1 <= group_num <= 3):
            print("Group number must be 1, 2, or 3")
            return False
        if state not in (0, 1):
            print("State must be 0 or 1")
            return False
            
        command = bytearray([0x23, group_num, state])
        return self.send_command(command)
    
    def pwm_status_read(self) -> bool:
        """Read PWM status (Command 0x24)"""
        return self.send_command(bytearray([0x24]))
    
    def device_info_read(self) -> bool:
        """Read device information (Command 0x41)"""
        return self.send_command(bytearray([0x41]))
    
    def save_config(self) -> bool:
        """Save all configurations (Command 0x42)"""
        return self.send_command(bytearray([0x42]))
    
    def unlock_programming(self) -> bool:
        """Unlock programming mode (Command 0xAA)"""
        confirm = input("WARNING: This will unlock programming mode. Continue? (y/n): ")
        if confirm.lower() == 'y':
            return self.send_command(bytearray([0xAA]))
        return False

def execute_device_command(port: Optional[str] = None, 
                         baudrate: Optional[int] = None, 
                         command_index: int = 0,
                         input_array: Optional[list] = None) -> bool:
    """
    Execute a device command with given parameters
    
    Args:
        port: Serial port (default: '/dev/ttyACM0')
        baudrate: Baud rate (default: 115200)
        command_index: Index of command to execute (1-11)
        input_array: Input parameters specific to each command
        
    Returns:
        bool: True if command was executed successfully, False otherwise
    """
    # Set defaults if None
    if port is None:
        port = '/dev/ttyACM0'
    if baudrate is None:
        baudrate = 115200
    if input_array is None:
        input_array = []
    
    # Create controller instance
    controller = PiDeviceController(serial_port=port, baudrate=baudrate)
    
    if not controller.connect():
        return False
    
    try:
        result = False
        
        if command_index == 1:
            # GPIO Single Pin Configuration
            if len(input_array) % 3 != 0:
                print("Invalid input array for GPIO config - needs tuples of (pin_num, pin_type, init_level)")
                return False
                
            pin_configs = []
            for i in range(0, len(input_array), 3):
                pin_configs.append((input_array[i], input_array[i+1], input_array[i+2]))
            result = controller.gpio_single_pin_config(pin_configs)
            
        elif command_index == 2:
            # GPIO Single Pin Set
            if len(input_array) != 2:
                print("Need exactly 2 parameters: pin_num and level")
                return False
            result = controller.gpio_single_pin_set(input_array[0], input_array[1])
            
        elif command_index == 3:
            # GPIO Bulk Set
            result = controller.gpio_bulk_set(input_array)
            
        elif command_index == 4:
            # GPIO Status Read
            result = controller.gpio_status_read()
            
        elif command_index == 5:
            # PWM Group Configuration
            if len(input_array) != 5:
                print("Need exactly 5 parameters: group_num, resolution, period, active_level, idle_level")
                return False
            result = controller.pwm_group_config(*input_array)
            
        elif command_index == 6:
            # PWM Duty Cycle Set
            if len(input_array) != 5:
                print("Need exactly 5 parameters: group_num followed by 4 duty cycles")
                return False
            result = controller.pwm_duty_cycle_set(input_array[0], input_array[1:5])
            
        elif command_index == 7:
            # PWM Group Control
            if len(input_array) != 2:
                print("Need exactly 2 parameters: group_num and state")
                return False
            result = controller.pwm_group_control(*input_array)
            
        elif command_index == 8:
            # PWM Status Read
            result = controller.pwm_status_read()
            
        elif command_index == 9:
            # Device Info Read
            result = controller.device_info_read()
            
        elif command_index == 10:
            # Save Configuration
            result = controller.save_config()
            
        elif command_index == 11:
            # Unlock Programming
            result = controller.unlock_programming()
            
        else:
            print("Invalid command index (must be 1-11)")
            return False
        
        return result
        
    except Exception as e:
        print(f"Error executing command: {e}")
        return False
    finally:
        controller.disconnect()

def main():
    print("Raspberry Pi GPIO/PWM Device Controller")
    print("--------------------------------------")
    
    # Default to /dev/ttyS0 (Pi 3/4) or /dev/ttyACM0 (older Pi)
    default_port = '/dev/ttyACM0'
    try:
        # Simple check to see which port might be available
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read()
            if 'Raspberry Pi 1' in model or 'Raspberry Pi Zero' in model:
                default_port = '/dev/ttyAMA0'
    except:
        pass
    
    port = input(f"Enter serial port [{default_port}]: ") or default_port
    baudrate = int(input("Enter baud rate [115200]: ") or 115200)
    
    try:
        while True:
            print("\nAvailable Commands:")
            print(" 1. GPIO Single Pin Configuration")
            print(" 2. GPIO Single Pin Set")
            print(" 3. GPIO Bulk Set")
            print(" 4. GPIO Status Read")
            print(" 5. PWM Group Configuration")
            print(" 6. PWM Duty Cycle Set")
            print(" 7. PWM Group Control")
            print(" 8. PWM Status Read")
            print(" 9. Device Info Read")
            print("10. Save Configuration")
            print("11. Unlock Programming")
            print(" 0. Exit")
            
            choice = input("Enter command number: ").strip()
            
            if choice == '0':
                break
            
            command_index = int(choice)
            input_array = []
            
            if command_index == 1:
                # GPIO Single Pin Configuration
                pin_configs = []
                while True:
                    try:
                        pin_num = int(input("Enter pin number (1-16, 0 to finish): "))
                        if pin_num == 0:
                            break
                        pin_type = int(input("Enter pin type (1-5): "))
                        init_level = int(input("Enter initial level (0-1): "))
                        pin_configs.extend([pin_num, pin_type, init_level])
                    except ValueError:
                        print("Invalid input. Please enter numbers only.")
                
                if pin_configs:
                    execute_device_command(port=port, baudrate=baudrate, 
                                          command_index=command_index, 
                                          input_array=pin_configs)
            
            elif command_index == 2:
                # GPIO Single Pin Set
                try:
                    pin_num = int(input("Enter pin number (1-16): "))
                    level = int(input("Enter level (0-1): "))
                    execute_device_command(port=port, baudrate=baudrate, 
                                         command_index=command_index, 
                                         input_array=[pin_num, level])
                except ValueError:
                    print("Invalid input. Please enter numbers only.")
            
            elif command_index == 3:
                # GPIO Bulk Set
                try:
                    pins = input("Enter pin numbers to set high (e.g., '1 3 5'): ")
                    pin_list = [int(p) for p in pins.split() if p.isdigit()]
                    execute_device_command(port=port, baudrate=baudrate, 
                                         command_index=command_index, 
                                         input_array=pin_list)
                except ValueError:
                    print("Invalid input. Please enter numbers only.")
            
            elif command_index == 4:
                # GPIO Status Read
                execute_device_command(port=port, baudrate=baudrate, 
                                     command_index=command_index)
            
            elif command_index == 5:
                # PWM Group Configuration
                try:
                    group_num = int(input("Enter group number (1-3): "))
                    resolution = int(input("Enter resolution (0-65535): "))
                    period = int(input("Enter period count: "))
                    active_level = int(input("Enter active level (0-15): "))
                    idle_level = int(input("Enter idle level (0-15): "))
                    execute_device_command(port=port, baudrate=baudrate, 
                                         command_index=command_index, 
                                         input_array=[group_num, resolution, period, 
                                                     active_level, idle_level])
                except ValueError:
                    print("Invalid input. Please enter numbers only.")
            
            elif command_index == 6:
                # PWM Duty Cycle Set
                try:
                    group_num = int(input("Enter group number (1-3): "))
                    duty_cycles = []
                    for i in range(1, 5):
                        duty = int(input(f"Enter duty cycle count for pin {i}: "))
                        duty_cycles.append(duty)
                    execute_device_command(port=port, baudrate=baudrate, 
                                         command_index=command_index, 
                                         input_array=[group_num] + duty_cycles)
                except ValueError:
                    print("Invalid input. Please enter numbers only.")
            
            elif command_index == 7:
                # PWM Group Control
                try:
                    group_num = int(input("Enter group number (1-3): "))
                    state = int(input("Enter state (0=stop, 1=start): "))
                    execute_device_command(port=port, baudrate=baudrate, 
                                         command_index=command_index, 
                                         input_array=[group_num, state])
                except ValueError:
                    print("Invalid input. Please enter numbers only.")
            
            elif command_index == 8:
                # PWM Status Read
                execute_device_command(port=port, baudrate=baudrate, 
                                     command_index=command_index)
            
            elif command_index == 9:
                # Device Info Read
                execute_device_command(port=port, baudrate=baudrate, 
                                     command_index=command_index)
            
            elif command_index == 10:
                # Save Configuration
                execute_device_command(port=port, baudrate=baudrate, 
                                     command_index=command_index)
            
            elif command_index == 11:
                # Unlock Programming
                execute_device_command(port=port, baudrate=baudrate, 
                                     command_index=command_index)
            
            else:
                print("Invalid choice. Please try again.")
            
            # Small delay between commands
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")

if __name__ == "__main__":
    main()

# # Example usage:
# if _name_ == "_main_":
#     # Example 1: Set single GPIO pin
#     # execute_device_command(command_index=2, input_array=[5, 1])  # Set pin 5 to high
    
#     # Example 2: Configure PWM group
#     # execute_device_command(command_index=5, input_array=[1, 1000, 20000, 0b1010, 0b0101])
    
#     # Example 3: Bulk set GPIO pins
#     # execute_device_command(command_index=3, input_array=[1, 3, 5])
    
#     # Original main function can still be used for interactive mode
#     # main()





















# import serial
# import time
# import struct
# import RPi.GPIO as GPIO
# from typing import List, Tuple

# class PiDeviceController:
#     def init(self, serial_port='/dev/ttyACM0', baudrate=115200, timeout=1):
#         """
#         Initialize the device controller for Raspberry Pi
#         :param serial_port: Default is '/dev/ttyS0' for Pi 3/4, '/dev/ttyAMA0' for older Pi
#         :param baudrate: Communication baud rate
#         :param timeout: Serial timeout in seconds
#         """
#         self.serial_port = serial_port
#         self.baudrate = baudrate
#         self.timeout = timeout
#         self.ser = None
        
#         # Raspberry Pi specific serial setup
#         self._enable_serial()
        
#     def _enable_serial(self):
#         """Enable serial interface on Raspberry Pi"""
#         try:
#             # Disable console over serial (may require sudo)
#             with open('/boot/cmdline.txt', 'r') as f:
#                 cmdline = f.read().strip()
            
#             if 'console=serial0' in cmdline:
#                 print("Warning: Serial console is enabled in /boot/cmdline.txt")
#                 print("For reliable communication, you should disable it by removing 'console=serial0,115200'")
#                 print("Then run: sudo raspi-config -> Interface Options -> Serial -> No")
#         except Exception as e:
#             print(f"Warning checking cmdline.txt: {e}")

#     def connect(self):
#         """Establish connection to the device"""
#         try:
#             self.ser = serial.Serial(
#                 port=self.serial_port,
#                 baudrate=self.baudrate,
#                 timeout=self.timeout,
#                 bytesize=serial.EIGHTBITS,
#                 parity=serial.PARITY_NONE,
#                 stopbits=serial.STOPBITS_ONE
#             )
#             print(f"Connected to {self.serial_port} at {self.baudrate} baud")
#             return True
#         except serial.SerialException as e:
#             print(f"Failed to connect to {self.serial_port}: {e}")
#             print("Possible solutions:")
#             print("1. Make sure the serial interface is enabled (sudo raspi-config)")
#             print("2. Check if you're using the correct port (try /dev/ttyAMA0 for older Pi)")
#             print("3. Verify your baud rate matches the device")
#             print("4. Ensure no other process is using the serial port")
#             return False
    
#     def disconnect(self):
#         """Close the serial connection"""
#         if self.ser and self.ser.is_open:
#             self.ser.close()
#             print("Connection closed")
    
#     def send_command(self, command_bytes: bytes) -> bool:
#         """Send a command to the device"""
#         if not self.ser or not self.ser.is_open:
#             print("Not connected to device")
#             return False
        
#         try:
#             self.ser.write(command_bytes)
#             print(f"Sent command: {self._format_hex(command_bytes)}")
#             return True
#         except serial.SerialException as e:
#             print(f"Error sending command: {e}")
#             return False
    
#     def _format_hex(self, data: bytes) -> str:
#         """Format bytes as hex string for display"""
#         return ' '.join(f'0x{byte:02X}' for byte in data)
    
#     def gpio_single_pin_config(self, pin_configs: List[Tuple[int, int, int]]) -> bool:
#         """
#         Configure single GPIO pins (Command 0x01)
#         :param pin_configs: List of tuples (pin_num, pin_type, init_level)
#         :return: True if command sent successfully
#         """
#         if len(pin_configs) > 16:
#             print("Maximum 16 pin configurations allowed")
#             return False
        
#         command = bytearray([0x01])
#         for pin_num, pin_type, init_level in pin_configs:
#             if not (1 <= pin_num <= 16):
#                 print(f"Invalid pin number {pin_num}. Must be 1-16")
#                 return False
#             if not (1 <= pin_type <= 5):
#                 print(f"Invalid pin type {pin_type}. Must be 1-5")
#                 return False
#             if init_level not in (0, 1):
#                 print(f"Invalid init level {init_level}. Must be 0 or 1")
#                 return False
#             command.extend([pin_num, pin_type, init_level])
        
#         return self.send_command(command)
    
#     def gpio_single_pin_set(self, pin_num: int, level: int) -> bool:
#         """
#         Set single GPIO pin level (Command 0x02)
#         :param pin_num: Pin number to set (1-16)
#         :param level: 0 (low) or 1 (high)
#         :return: True if command sent successfully
#         """
#         if not (1 <= pin_num <= 16):
#             print("Pin number must be between 1 and 16")
#             return False
#         if level not in (0, 1):
#             print("Level must be 0 or 1")
#             return False
            
#         command = bytearray([0x02, pin_num, level])
#         return self.send_command(command)
    
#     def gpio_bulk_set(self, pin_levels: List[int]) -> bool:
#         """
#         Set multiple GPIO pins at once (Command 0x03)
#         :param pin_levels: List of pin numbers to set high (others will be low)
#         :return: True if command sent successfully
#         """
#         # Create a 16-bit mask (for pins 1-16)
#         mask = 0
#         for pin in pin_levels:
#             if 1 <= pin <= 16:
#                 mask |= 1 << (pin - 1)
#             else:
#                 print(f"Ignoring invalid pin number {pin}")
        
#         # Split into 2 bytes (little-endian)
#         byte1 = mask & 0xFF
#         byte2 = (mask >> 8) & 0xFF
#         command = bytearray([0x03, byte1, byte2])
        
#         return self.send_command(command)
    
#     def gpio_status_read(self) -> bool:
#         """Read GPIO status (Command 0x11)"""
#         return self.send_command(bytearray([0x11]))
    
#     def pwm_group_config(self, group_num: int, resolution: int, period: int, 
#                         active_level: int, idle_level: int) -> bool:
#         """
#         Configure PWM group (Command 0x21)
#         :param group_num: PWM group number (1-3)
#         :param resolution: PWM resolution (0-65535)
#         :param period: PWM period count (32-bit value)
#         :param active_level: 4-bit value for active levels of pins in group
#         :param idle_level: 4-bit value for idle levels of pins in group
#         :return: True if command sent successfully
#         """
#         if not (1 <= group_num <= 3):
#             print("Group number must be 1, 2, or 3")
#             return False
#         if not (0 <= resolution <= 65535):
#             print("Resolution must be between 0 and 65535")
#             return False
#         if not (0 <= active_level <= 0b1111):
#             print("Active level must be a 4-bit value (0-15)")
#             return False
#         if not (0 <= idle_level <= 0b1111):
#             print("Idle level must be a 4-bit value (0-15)")
#             return False
        
#         # Combine active and idle levels
#         px_level = ((active_level & 0x0F) << 4) | (idle_level & 0x0F)
        
#         command = bytearray([0x21, group_num])
#         command.extend(resolution.to_bytes(2, 'little'))
#         command.extend(period.to_bytes(4, 'little'))
#         command.append(px_level)
        
#         return self.send_command(command)
    
#     def pwm_duty_cycle_set(self, group_num: int, duty_cycles: List[int]) -> bool:
#         """
#         Set PWM duty cycles (Command 0x22)
#         :param group_num: PWM group number (1-3)
#         :param duty_cycles: List of 4 duty cycle counts (32-bit values each)
#         :return: True if command sent successfully
#         """
#         if not (1 <= group_num <= 3):
#             print("Group number must be 1, 2, or 3")
#             return False
#         if len(duty_cycles) != 4:
#             print("Exactly 4 duty cycles required")
#             return False
        
#         command = bytearray([0x22, group_num])
#         for duty in duty_cycles:
#             command.extend(duty.to_bytes(4, 'little'))
        
#         return self.send_command(command)
    
#     def pwm_group_control(self, group_num: int, state: int) -> bool:
#         """
#         Control PWM group output (Command 0x23)
#         :param group_num: PWM group number (1-3)
#         :param state: 0 (stop) or 1 (start)
#         :return: True if command sent successfully
#         """
#         if not (1 <= group_num <= 3):
#             print("Group number must be 1, 2, or 3")
#             return False
#         if state not in (0, 1):
#             print("State must be 0 or 1")
#             return False
            
#         command = bytearray([0x23, group_num, state])
#         return self.send_command(command)
    
#     def pwm_status_read(self) -> bool:
#         """Read PWM status (Command 0x24)"""
#         return self.send_command(bytearray([0x24]))
    
#     def device_info_read(self) -> bool:
#         """Read device information (Command 0x41)"""
#         return self.send_command(bytearray([0x41]))
    
#     def save_config(self) -> bool:
#         """Save all configurations (Command 0x42)"""
#         return self.send_command(bytearray([0x42]))
    
#     def unlock_programming(self) -> bool:
#         """Unlock programming mode (Command 0xAA)"""
#         confirm = input("WARNING: This will unlock programming mode. Continue? (y/n): ")
#         if confirm.lower() == 'y':
#             return self.send_command(bytearray([0xAA]))
#         return False

# def main():
#     print("Raspberry Pi GPIO/PWM Device Controller")
#     print("--------------------------------------")
    
#     # Default to /dev/ttyS0 (Pi 3/4) or /dev/ttyACM0 (older Pi)
#     default_port = '/dev/ttyACM0'
#     try:
#         # Simple check to see which port might be available
#         with open('/proc/device-tree/model', 'r') as f:
#             model = f.read()
#             if 'Raspberry Pi 1' in model or 'Raspberry Pi Zero' in model:
#                 default_port = '/dev/ttyAMA0'
#     except:
#         pass
    
#     port = input(f"Enter serial port [{default_port}]: ") or default_port
#     baudrate = int(input("Enter baud rate [115200]: ") or 115200)
    
#     controller = PiDeviceController(serial_port=port, baudrate=baudrate)
    
#     if not controller.connect():
#         return
    
#     try:
#         while True:
#             print("\nAvailable Commands:")
#             print(" 1. GPIO Single Pin Configuration")
#             print(" 2. GPIO Single Pin Set")
#             print(" 3. GPIO Bulk Set")
#             print(" 4. GPIO Status Read")
#             print(" 5. PWM Group Configuration")
#             print(" 6. PWM Duty Cycle Set")
#             print(" 7. PWM Group Control")
#             print(" 8. PWM Status Read")
#             print(" 9. Device Info Read")
#             print("10. Save Configuration")
#             print("11. Unlock Programming")
#             print(" 0. Exit")
            
#             choice = input("Enter command number: ").strip()
            
#             if choice == '0':
#                 break
#             elif choice == '1':
#                 # GPIO Single Pin Configuration
#                 pin_configs = []
#                 while True:
#                     try:
#                         pin_num = int(input("Enter pin number (1-16, 0 to finish): "))
#                         if pin_num == 0:
#                             break
#                         pin_type = int(input("Enter pin type (1-5): "))
#                         init_level = int(input("Enter initial level (0-1): "))
#                         pin_configs.append((pin_num, pin_type, init_level))
#                     except ValueError:
#                         print("Invalid input. Please enter numbers only.")
                
#                 if pin_configs:
#                     controller.gpio_single_pin_config(pin_configs)
            
#             elif choice == '2':
#                 # GPIO Single Pin Set
#                 try:
#                     pin_num = int(input("Enter pin number (1-16): "))
#                     level = int(input("Enter level (0-1): "))
#                     controller.gpio_single_pin_set(pin_num, level)
#                 except ValueError:
#                     print("Invalid input. Please enter numbers only.")
            
#             elif choice == '3':
#                 # GPIO Bulk Set
#                 try:
#                     pins = input("Enter pin numbers to set high (e.g., '1 3 5'): ")
#                     pin_list = [int(p) for p in pins.split() if p.isdigit()]
#                     controller.gpio_bulk_set(pin_list)
#                 except ValueError:
#                     print("Invalid input. Please enter numbers only.")
            
#             elif choice == '4':
#                 # GPIO Status Read
#                 controller.gpio_status_read()
            
#             elif choice == '5':
#                 # PWM Group Configuration
#                 try:
#                     group_num = int(input("Enter group number (1-3): "))
#                     resolution = int(input("Enter resolution (0-65535): "))
#                     period = int(input("Enter period count: "))
#                     active_level = int(input("Enter active level (0-15): "))
#                     idle_level = int(input("Enter idle level (0-15): "))
#                     controller.pwm_group_config(group_num, resolution, period, active_level, idle_level)
#                 except ValueError:
#                     print("Invalid input. Please enter numbers only.")
            
#             elif choice == '6':
#                 # PWM Duty Cycle Set
#                 try:
#                     group_num = int(input("Enter group number (1-3): "))
#                     duty_cycles = []
#                     for i in range(1, 5):
#                         duty = int(input(f"Enter duty cycle count for pin {i}: "))
#                         duty_cycles.append(duty)
#                     controller.pwm_duty_cycle_set(group_num, duty_cycles)
#                 except ValueError:
#                     print("Invalid input. Please enter numbers only.")
            
#             elif choice == '7':
#                 # PWM Group Control
#                 try:
#                     group_num = int(input("Enter group number (1-3): "))
#                     state = int(input("Enter state (0=stop, 1=start): "))
#                     controller.pwm_group_control(group_num, state)
#                 except ValueError:
#                     print("Invalid input. Please enter numbers only.")
            
#             elif choice == '8':
#                 # PWM Status Read
#                 controller.pwm_status_read()
            
#             elif choice == '9':
#                 # Device Info Read
#                 controller.device_info_read()
            
#             elif choice == '10':
#                 # Save Configuration
#                 controller.save_config()
            
#             elif choice == '11':
#                 # Unlock Programming
#                 controller.unlock_programming()
            
#             else:
#                 print("Invalid choice. Please try again.")
            
#             # Small delay between commands
#             time.sleep(0.1)
    
#     except KeyboardInterrupt:
#         print("\nProgram interrupted by user")
#     finally:
#         controller.disconnect()

# if _name_ == "_main_":
#     main()
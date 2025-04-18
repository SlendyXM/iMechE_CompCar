from extension_gpio_board import execute_device_command
#     # execute_device_command(command_index=2, input_array=[5, 1])  # Set pin 5 to high
    
def LED_Green(power):
    pwm_pin = 42
    if power == True:
        execute_device_command(command_index=2, input_array=[pwm_pin, 1])
    else:
        execute_device_command(command_index=2, input_array=[pwm_pin, 0])

if __name__ == "__main__":
    LED_Green(True)
    LED_Green(False)
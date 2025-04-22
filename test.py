import RPi.GPIO as io
import time

# Initializing the GPIO pins
io.setmode(io.BOARD)
io.setup(3,io.OUT)		# STBY
io.output(3,io.HIGH)	# enable board
import gpio_board_extension.extension_gpio_board

execute = gpio_board_extension.extension_gpio_board.execute_device_command


# Importing Motor Movements and Rotations
from motors.movements.stop import stop

from motors.movements.forward import move_forward
from motors.movements.backward import move_backward
from motors.movements.left import move_left
from motors.movements.right import move_right

from motors.rotations.clockwise import rotate_clockwise
from motors.rotations.anticlockwise import rotate_anticlockwise

from motors.changedirection.forwardlateralleft import forward_lateral_anticlockwise
from motors.changedirection.forwardlateralright import forward_lateral_clockwise
from motors.changedirection.backwardlateralleft import backward_lateral_clockwise
from motors.changedirection.backwardlateralright import backward_lateral_anticlockwise

# Importing Plunger
from plunger.rotation_servo import servo_control

# Importing Color Sensor
from colorsensors.frequencyscaling import frequency_scaling_0percent, frequency_scaling_2percent, frequency_scaling_20percent, frequency_scaling_100percent
from colorsensors.powersave import enterpowersave, exitpowersave
from colorsensors.color_detecting import color_detecting

# Importing LED Lights
from leds.green import LED_Green
from leds.red import LED_Red

# Importing Laser Sensor
from lasersensors.lsl import Laser_Sensor_left
from lasersensors.lsr import Laser_Sensor_right

# Importing the button
from buttons.redbutton import single_target
from buttons.bluebutton import multiple_target
from buttons.blackbutton import cease_all_functions

# Importing the buzzer
from buzzer.buzzer import sound

# Importing the camera
from camera.MiddleCalibration import middle_calibration

# Localize all pins
stby_pin						= [3]
motor_a_pins					= [11, 13, 15]
motor_b_pins					= [19, 21, 23]
motor_c_pins					= [22, 24, 26]
motor_d_pins					= [36, 38, 40]
plunger_pin						= [8]
color_sensor_a_pins				= [29, 31, 32, 33, 35, 37]
color_sensor_b_pins				= []
color_sensor_c_pins				= []
color_sensor_d_pins				= []
laser_sensor_left_pin			= []
laser_sensor_right_pin			= []
red_button_pin					= [44]
blue_button_pin					= []
black_button_pin				= [45]
red_LED_pin						= [41]
green_LED_pin					= [42]
buzzer_pin						= [43]

# Combine all pins into a single list
all_pins = (
	stby_pin + 
	motor_a_pins + motor_b_pins + motor_c_pins + motor_d_pins + 
	plunger_pin + 
	color_sensor_a_pins + color_sensor_b_pins + color_sensor_c_pins + color_sensor_d_pins + 
	laser_sensor_left_pin + laser_sensor_right_pin + 
	red_button_pin + blue_button_pin + black_button_pin + 
	red_LED_pin + green_LED_pin + 
	buzzer_pin
)

# Main Function
def main():
	try:
		# Motor Functions all tested
		'''move_forward(10,5)
		stop(0,1)
		move_backward(10,5)
		stop(0,1)
		move_left(10,5)
		stop(0,1)
		move_right(10,5)
		stop(0,1)
		rotate_clockwise(10,5)
		stop(0,1)
		rotate_anticlockwise(10,5)
		stop(0,1)
		forward_lateral_clockwise(10,1)
		forward_lateral_anticlockwise(10,1)
		backward_lateral_clockwise(10,1)
		backward_lateral_anticlockwise(10,1)
		stop(0,1)'''
		# Plunger Functions all tested
		'''servo_control()'''
		# Color Sensors all tested
		exitpowersave()
		frequency_scaling_2percent()
		while True:
			result = color_detecting()
			if result:
				print("Color detecting condition met. Exiting loop.")
				enterpowersave()
				break
			else:
				print("Color detecting condition not met. Continuing...")
	finally:
		io.cleanup(all_pins)
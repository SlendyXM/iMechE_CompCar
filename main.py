import RPi.GPIO as io
import time

# Initializing the GPIO pins
io.setmode(io.BOARD)
io.setup(3,io.OUT)		# STBY
io.output(3,io.HIGH)	# enable board

# Importing Motor Movements and Rotations
from camera import MiddleCalibration
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
red_button_pin					= []
blue_button_pin					= []
black_button_pin				= []
red_LED_pin						= []
green_LED_pin					= []
buzzer_pin						= []

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
		'''exitpowersave()
		frequency_scaling_2percent()
		while True:
			result = color_detecting()
			if result:
				print("Color detecting condition met. Exiting loop.")
				enterpowersave()
				break
			else:
				print("Color detecting condition not met. Continuing...")'''
		# Actual Main Loop
		while True:
			# Green, Red LED and buzzer is off until button is pressed
			LED_Red(False)
			sound(False)

			# Check if the button is pressed

			# If black button is pushed, all functions will cease
			if cease_all_functions() == True:
				io.cleanup(all_pins)
				print("Ceasing all functions.")
				break	# Break main loop and terminate the program

			# If red button is pushed, single target mode will be activated
			if single_target() == True:

				# Turn on the green LED
				LED_Green(True)
				while LED_Green(True) == True:

					# Move forward at 30% speed until wall is detected
					move_forward(30)

					yellow_position, cam_distance = middle_calibration()

					# Detect yellow object
					while yellow_position:
						print(f"Yellow Position: {yellow_position}, Distance: {cam_distance:.2f} cm")
						if yellow_position == "Left":
							print("Adjusting to the left...")
							rotate_anticlockwise(10)
						elif yellow_position == "Right":
							print("Adjusting to the right...")
							rotate_clockwise(10)
						elif yellow_position == "Centered":
							print("Yellow object centered. Proceeding...")
							break

					# Detect wall
					if cam_distance <= 5:

						# Turn on red LED and sound the buzzer
						LED_Red(True)
						sound(True)

						# Stop the car 
						stop(0,15)

						# Turn off red LED and turn off the buzzer
						LED_Red(False)
						sound(False)

					# Check if original target is reached
					reach_original_target = False
					while not reach_original_target:

						# Turning on the TCS3200 color sensors
						exitpowersave()

						# Set the frequency scaling to 2%
						frequency_scaling_2percent()

						# Move backward at 30% speed until reach back to the original position
						move_backward(30)

						# Color detection method for the original target
						result = color_detecting()
						if result:
							print("Detected the original target. Exiting loop.")

							# Turn off the TCS3200 color sensors
							enterpowersave()

							# Stop the car
							stop(0, 1)

							# Break loop
							reach_original_target = True

						else:
							print("Not yet detected the original target. Continuing...")
	finally:
		# Cleanup
		LED_Green(False)
		io.cleanup(all_pins)
			
if __name__ == "__main__":
	main()




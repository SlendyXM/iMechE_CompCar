import RPi.GPIO as io
import time
import cv2

# Initializing the GPIO pins
io.setmode(io.BOARD)
io.setup(3,io.OUT)		# STBY
io.output(3,io.HIGH)	# enable board

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
'''
# Importing LED Lights
from led.green import LED_Green
from led.red import LED_Red

g = LED_Green()
r = LED_Red()

# Importing Laser Sensor
from lasersensors.ls import Laser_Sensor

ls = Laser_Sensor()

# Importing the button
from button.b import Button

b = Button()'''

# Localize all pins
stby_pin = [3]
motor_a_pins = [11, 13, 15]
motor_b_pins = [19, 21, 23]
motor_c_pins = [22, 24, 26]
motor_d_pins = [36, 38, 40]
plunger_pin = [8]
color_sensor_a_pins = [29, 31, 32, 33, 35, 37]

# Combine all pins into a single list
all_pins = stby_pin + motor_a_pins + motor_b_pins + motor_c_pins + motor_d_pins + plunger_pin + color_sensor_a_pins

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
		
	finally:
		# Cleanup
		io.cleanup(all_pins)

if __name__ == "__main__":
	main()




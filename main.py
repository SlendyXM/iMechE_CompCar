import RPi.GPIO as io
import time
import cv2
from plunger.rotation_servo import servo_control

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
from colorsensors.csA import Color_SensorA
from colorsensors.csB import Color_SensorB
from colorsensors.csC import Color_SensorC

csA = Color_SensorA()
csB = Color_SensorB()
csC = Color_SensorC()

from colorsensors.frequencyscaling import frequency_scaling_0percent, frequency_scaling_2percent, frequency_scaling_20percent, frequency_scaling_100percent
from colorsensors.powersave import enterpowersave, exitpowersave
from colorsensors.color_detecting import color_detecting

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

b = Button()

# Main Function
def main():
	try:
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
		servo_control()
		'''initial_speed = 50
		initial_duration = 1
		while True:
			exitpowersave()
			color_detecting()'''







	finally:
		io.cleanup([3, 11, 13, 15, 19, 21, 23, 22, 24, 26, 36, 38, 40, 8, 10, 12])

if __name__ == "__main__":
	main()




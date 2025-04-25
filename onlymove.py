import RPi.GPIO as io
import time
#from picamera2 import Picamera2


# Initializing the GPIO pins
io.setmode(io.BOARD)
io.setup(3, io.OUT)  # STBY
io.output(3, io.HIGH)  # enable board

# Importing Motor Movements
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


# Importing Buzzer
#from buzzer.buzzer import buzzer
#buzzer = buzzer()

# Importing the camera

# Localize all pins
stby_pin                        = [3]
motor_a_pins                    = [11, 13, 15]
motor_b_pins                    = [19, 21, 23]
motor_c_pins                    = [22, 24, 26]
motor_d_pins                    = [36, 38, 40]
color_sensor_a_pins				= [29, 31, 32, 33, 35, 37]
color_sensor_b_pins             = []
color_sensor_c_pins             = []
color_sensor_d_pins             = []
buzzer_pins                     = [12, 16]

all_pins = stby_pin + motor_a_pins + motor_b_pins + motor_c_pins + motor_d_pins + color_sensor_a_pins + buzzer_pins

move_forward(100)
time.sleep(20)
stop(0,1)
io.cleanup(all_pins)

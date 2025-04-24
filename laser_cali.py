
import RPi.GPIO as io
import time
import cv2
from picamera2 import Picamera2


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
from motors.movements.stop import stop
# # Importing the camera
# from camera.MiddleCalibrationPiCam import middle_calibration

# from camera.TargetCalibation_0424 import process_frame



# Importing the laser sensor
from lasersensors.dual_laser_sensor import read_laser

# Localize all pins
stby_pin = [3]
motor_a_pins = [11, 13, 15]
motor_b_pins = [19, 21, 23]
motor_c_pins = [22, 24, 26]
motor_d_pins = [36, 38, 40]

# Combine all pins into a single list
all_pins = stby_pin + motor_a_pins + motor_b_pins + motor_c_pins + motor_d_pins
def lasercali():
    confirm_coe=0
    while True:
        result=read_laser()
        print(f'result:{result}')
        print(f"{confirm_coe}")
        if result=="Anticlockwise":
            confirm_coe=0
            rotate_anticlockwise(10)
            time.sleep(0.1)
            stop(0,0.01)
        elif result=="Clockwise":
            confirm_coe=0
            rotate_clockwise(10)
            time.sleep(0.1)
            stop(0,0.01)
        elif result=="Parallel":
            stop(0,0.01)
            confirm_coe+=1
            print(f"{confirm_coe}")
            if confirm_coe>=10:
                break
    else:
        print("Happy")

if __name__ == "__main__":
    try:
        lasercali()
    finally:
        io.cleanup(all_pins)

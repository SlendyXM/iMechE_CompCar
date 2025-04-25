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

# Importing the camera
from camera.MiddleCalibrationPiCam import middle_calibration

from camera.TargetCalibation_0424 import process_frame

from motors.movements.stop import stop

# Localize all pins
stby_pin = [7]
motor_a_pins = [11, 13, 15]
motor_b_pins = [19, 21, 23]
motor_c_pins = [22, 24, 26]
motor_d_pins = [36, 38, 40]

# Combine all pins into a single list
all_pins = stby_pin + motor_a_pins + motor_b_pins + motor_c_pins + motor_d_pins

# Main Function
def main():
    
    print("Initializing camera...")
    camera = cv2.VideoCapture(1, cv2.CAP_V4L2)

    # Set camera properties
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_EXPOSURE, -0.3)
    print("Current Exposure:", camera.get(cv2.CAP_PROP_EXPOSURE))

    center_point = (325, 360)  # Default center point
    successful=0
    try:
        while True:
            frame, mask, x_cmd, y_cmd = process_frame(camera, center_point)

            # Display the frame and mask
            if frame is not None:
                cv2.imshow("Smart Circle Tracking", frame)
            if mask is not None:
                cv2.imshow("Color Mask", mask)

            # Print movement commands
            if x_cmd and y_cmd:
                if x_cmd == "CENTER":
                    if y_cmd=="CENTER":
                          stop(0,0.05)
                          successful+=1
                          if successful>=10:
                              break
                    elif y_cmd=="GO STRAIGHT":
                        successful=0
                        move_backward(10)
                        time.sleep(0.02)
                        stop(0,0.01)
                    elif y_cmd=="GO BACK":
                        successful=0
                        move_forward(5) #forward means backward because different orientation
                        time.sleep(0.02)
                        stop(0,0.01)
                        

                elif x_cmd=="GO LEFT":
                   successful=0
                   move_left(10)
                   time.sleep(0.02)
                   stop(0,0.01)
                elif x_cmd== "GO RIGHT":
                    successful=0
                    move_right(10)
                    time.sleep(0.02)
                    stop(0,0.01)
                    
                print(f"X Command: {x_cmd}, Y Command: {y_cmd}")

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()
        io.cleanup(all_pins)

if __name__ == "__main__":
    main()

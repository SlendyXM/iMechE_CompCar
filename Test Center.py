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

# Importing Color Sensor
from colorsensors.frequencyscaling import frequency_scaling_2percent
from colorsensors.powersave import enterpowersave, exitpowersave
from colorsensors.color_detecting import color_detecting

# Importing the camera
from camera.MiddleCalibrationPiCam import middle_calibration

from motors.movements.stop import stop

# Localize all pins
stby_pin                        = [3]
motor_a_pins                    = [11, 13, 15]
motor_b_pins                    = [19, 21, 23]
motor_c_pins                    = [22, 24, 26]
motor_d_pins                    = [36, 38, 40]
color_sensor_a_pins				= [29, 31, 32, 33, 35, 37]

# Combine all pins into a single list
all_pins = stby_pin + motor_a_pins + motor_b_pins + motor_c_pins + motor_d_pins + color_sensor_a_pins

# Main Function
def main():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    #if not video_capture.isOpened():
        #print("Error: Could not open camera")
        #return

    try:
        #while True:
            move_forward(10)
            vt_position=""
            while not vt_position:
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)
                print([vt_position, cam_distance])
                move_forward(10)
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break
                
				
            #if frame is not None and mask is not None:
                #cv2.imshow("Camera Feed", frame)
                #cv2.imshow("Mask", mask)
            # Detect yellow object
            i=0
            while True:
                # Detect wall
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)
                print([i,vt_position, cam_distance])
                #cv2.imshow("Camera Feed", frame)
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                
                #cv2.imshow("Mask", mask)
                if cam_distance <= 20:
                    stop(0, 1)
                    break
                # Move forward at 30% speed until wall is detected
                move_forward(30)

                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    move_right(3)
                elif vt_position == "Right":
                    print("Adjusting to the right...")
                    move_left(3)
                elif vt_position == "Centered":
                    print("Yellow object centered. Proceeding...")
                #time.sleep(0.2)
                i+=1
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break
			
                
            
            reach_original_target = False
            exitpowersave()
            frequency_scaling_2percent()

            while not reach_original_target:

                # Detect wall
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)
                print([i,vt_position, cam_distance])
                #cv2.imshow("Camera Feed", frame)
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

	            # Move backward at 30% speed until reach back to the original position
                move_backward(30)
                time.sleep(2)
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    move_right(3)
                elif vt_position == "Right":
                    print("Adjusting to the right...")
                    move_left(3)
                elif vt_position == "Centered":
                    print("Yellow object centered. Proceeding...")
                #time.sleep(0.2)
                i+=1
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break

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
        io.cleanup(all_pins)

if __name__ == "__main__":
    main()

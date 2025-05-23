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
from motors.movements.forwardleft import forwardleft
from motors.movements.forwardright import forwardright
from motors.movements.backwardleft import backwardleft
from motors.movements.backwardright import backwardright

from motors.rotations.clockwise import rotate_clockwise
from motors.rotations.anticlockwise import rotate_anticlockwise

from motors.changedirection.forwardlateralleft import forward_lateral_anticlockwise
from motors.changedirection.forwardlateralright import forward_lateral_clockwise
from motors.changedirection.backwardlateralleft import backward_lateral_clockwise
from motors.changedirection.backwardlateralright import backward_lateral_anticlockwise

# Importing Color Sensor
from colorsensors.powersave import enterpowersave, exitpowersave
from colorsensors.color_detecting import color_detecting

# Importing Buzzer
from buzzer.buzzer import buzzer
buzzer = buzzer()

# Importing Servo
from plunger.rotation_servo import servo_control

# Importing the camera
from camera.MiddleCalibrationPiCam import middle_calibration
from camera.MiddleCalibrationPiCam_Green import middle_calibration_green
from camera.TargetCalibation_0424 import process_frame

from gpio_board_extension.extension_gpio_board import execute_device_command


from lasersensors.dual_laser_sensor_1 import setup_serial, process_laser_data

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
servo_motor_pin                 = [8]

# Combine all pins into a single list
all_pins = (stby_pin + 
            motor_a_pins + motor_b_pins + motor_c_pins + motor_d_pins + 
            color_sensor_a_pins + color_sensor_b_pins + color_sensor_c_pins + color_sensor_d_pins + 
            buzzer_pins +
            servo_motor_pin)

# Initialize sensors
sensor1 = setup_serial('/dev/ttyACM0')
sensor2 = setup_serial('/dev/ttyACM1')
offset = -43  # Constant error

# Initialize sensor states
sensor1_state = {'is_valid': False, 'id': 'ACM0'}
sensor2_state = {'is_valid': False, 'id': 'ACM1'}

Extension_GPIO_Port = "/dev/ttyACM2"

# Main Function
def main():
    #LED_Green()
    #execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [41, 1])
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    print("Initializing camera...")
    camera = cv2.VideoCapture(1, cv2.CAP_V4L2)

    # Set camera properties
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_EXPOSURE, -0.3)
    print("Current Exposure:", camera.get(cv2.CAP_PROP_EXPOSURE))

    center_point = (337, 365)  # Default center point
    successful=0
    buzzer.sound(False)
    execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=12)
    start_time = time.time()
    time.sleep(5)
    try:
        #while True
            Temp,initial_distance=process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
            
            move_forward(10)
            vt_position=""
            average_distance=1800
            while average_distance>1500:
                frame = picam2.capture_array()
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)

                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)
                print([vt_position, cam_distance])
                move_forward(10)
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break              
				
            if frame is not None and mask is not None:
                cv2.imshow("Camera Feed", frame)
                cv2.imshow("Mask", mask)
            # Detect yellow object
            i=0
            #while True:
                # Detect wall
            
            while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                if i ==0:
                    First_Rotate_command=Rotate_command
                i+=1
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.07)
                    stop(0,0.01)
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.07)
                    stop(0,0.01)
                
            while True:
                
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)

                print([i,vt_position, cam_distance])
                
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Move forward at 30% speed until wall is detected
                #move_forward(30)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break    
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    move_right(10)
                    time.sleep(0.07)
                    stop(0, 0.01)
                    Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                    if Rotate_command == "stop":
                        
                        stop(0,0.01)                  
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 1])
                        buzzer.sound(True)
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 0])
                        break 
                elif vt_position == "Right":
                    print("Adjusting to the right...")
                    move_left(10)
                    time.sleep(0.07)
                    stop(0, 0.01)
                    Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                    if Rotate_command == "stop":
                        
                        stop(0,0.01)                  
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 1])
                        buzzer.sound(True)
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 0])
                        break 
                elif vt_position == "Centered":
                    stop(0,0.01)
                    print("Yellow object centered. Proceeding...")
                    Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                    print(Rotate_command)
                    move_forward(10)
                    time.sleep(0.07)
                    if Rotate_command == "stop":
                        
                        stop(0,0.01)                  
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 1])
                        buzzer.sound(True)
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 0])
                        break 
                    move_forward(5)
                    time.sleep(0.07)
                        
                elif vt_position =="":
                    move_backward(5)
                    time.sleep(0.05)
                    '''if First_Rotate_command=="Anticlockwise":
                        rotate_anticlockwise(5)
                        time.sleep(0.07)
                        stop(0,0.01)
                    #elif First_Rotate_command=="Clockwise":
                        # rotate_clockwise(5)
                        # time.sleep(0.07)
                        # stop(0,0.01)
                    # else:
                        # rotate_clockwise(5)
                        # time.sleep(0.07)
                        #stop(0,0.01)'''
                   
                    
                    
                
            


                

                    #time.sleep(0.01)
                #time.sleep(0.2)
                i+=1
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break
                
            buzzer.sound(False)
            reach_original_target = False
            exitpowersave()
            print(initial_distance)

            # Move backward at 30% speed until reach back to the original position
            move_backward(10)
            
            time.sleep(2)
            stop(0,0.4)
            i=0
            servo_control()
            while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    i+=1
                    if i>=10:
                        break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
            
            i=0
            while True:
                
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)

                print([i,vt_position, cam_distance])
                
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Move forward at 30% speed until wall is detected
                #move_forward(30)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break    
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    i=0
                    move_right(10)
                    time.sleep(0.07)
                    stop(0,0.01)
                elif vt_position == "Right":
                    i=0
                    print("Adjusting to the right...")
                    move_left(10)
                    time.sleep(0.07)
                    stop(0,0.01)
                elif vt_position == "Centered":
                    i+=1
                    print("Yellow object centered. Proceeding...")
                    if i >10:
                        break
            
            while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    i+=1
                    if i>=10:
                        break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
            
            
            move_left(10)
            time.sleep(0.14)
            stop(0,0.01)



            Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)

            while average_distance < (initial_distance-200):
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                move_backward(10)
                print(average_distance)
                print(f"initial {initial_distance}")
            
            stop(0,1)
            
            
                       
            '''Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)

            while average_distance<1500:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                move_backward(50)
                print(average_distance)
                print(f"initial {initial_distance}")
            
            stop(0,1)'''
            
            i=0
            while True:
                
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration_green(frame)

                print([i,vt_position, cam_distance])
                
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Move forward at 30% speed until wall is detected
                #move_forward(30)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break    
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    i=0
                    rotate_anticlockwise(5)
                    time.sleep(0.02)
                    stop(0,0.01)
                elif vt_position == "Right":
                    i=0
                    print("Adjusting to the right...")
                    rotate_clockwise(5)
                    time.sleep(0.02)
                    stop(0,0.01)
                elif vt_position == "Centered":
                    i+=1
                    print("Yellow object centered. Proceeding...")
                    if i >10:
                        break
            
            
            '''while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    i+=1
                    if i>=10:
                        break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
            
                        
            i=0
            while True:
                
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)

                print([i,vt_position, cam_distance])
                
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Move forward at 30% speed until wall is detected
                #move_forward(30)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break    
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    i=0
                    move_right(10)
                    time.sleep(0.07)
                    stop(0,0.01)
                elif vt_position == "Right":
                    i=0
                    print("Adjusting to the right...")
                    move_left(10)
                    time.sleep(0.07)
                    stop(0,0.01)
                elif vt_position == "Centered":
                    i+=1
                    print("Yellow object centered. Proceeding...")
                    if i >10:
                        break
            

            
            while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    i+=1
                    if i>=10:
                        break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0'''
            
            
            
            while not reach_original_target:

                '''# Detect wall
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)
                print([i,vt_position, cam_distance])
                #cv2.imshow("Camera Feed", frame)
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

	            # Move backward at 30% speed until reach back to the original position
                move_backward(5)
                # print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                # if vt_position == "Left":
                    # print("Adjusting to the left...")
                    # backwardleft(10)
                # elif vt_position == "Right":
                    # print("Adjusting to the right...")
                    # backwardright(10)
                # elif vt_position == "Centered":
                    # print("Yellow object centered. Proceeding...")
                # if Rotate_command == "Parallel":
                    # print("Parallel")
                    # move_backward(10)
                # elif Rotate_command == "Anticlockwise":
                    # backward_lateral_anticlockwise(10)
                    # time.sleep (0.01)
                # elif Rotate_command == "Clockwise":
                    # backward_lateral_clockwise(10)
                    # time.sleep(0.01)
                i+=1
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break'''

	            # Color detection method for the original target
                result = color_detecting()
                if result:
                    print("Detected the original target. Exiting loop.")

	                # Turn off the TCS3200 color sensors
                    enterpowersave()

	                # Stop the car
                    stop(0, 1)
                    servo_control()

	                # Break loop
                    reach_original_target = True
                else:
                    print("Not yet detected the original target. Continuing...")

            
            # Visual center
            while True:
                frame, mask, x_cmd, y_cmd = process_frame(camera, center_point)

                # Display the frame and mask
                if frame is not None:
                    cv2.imshow("Smart Circle Tracking", frame)
                if mask is not None:
                    cv2.imshow("Color Mask", mask)
                
                if x_cmd == None:
                    break
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
            
            
            
            i=0
            

            
            while True:
                
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration_green(frame)

                print([i,vt_position, cam_distance])
                
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Move forward at 30% speed until wall is detected
                #move_forward(30)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break    
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    i=0
                    rotate_anticlockwise(5)
                    time.sleep(0.02)
                    stop(0,0.01)
                elif vt_position == "Right":
                    i=0
                    print("Adjusting to the right...")
                    rotate_clockwise(5)
                    time.sleep(0.02)
                    stop(0,0.01)
                elif vt_position == "Centered":
                    i+=1
                    print("Yellow object centered. Proceeding...")
                    if i >10:
                        break
            Temp,initial_distance=process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
            
            move_forward(10)
            vt_position=""
            average_distance=1800
            while average_distance>700:
                frame = picam2.capture_array()
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)

                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)
                print([vt_position, cam_distance])
                move_forward(10)
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break              
				
            if frame is not None and mask is not None:
                cv2.imshow("Camera Feed", frame)
                cv2.imshow("Mask", mask)
            # Detect yellow object
            i=0
            #while True:
                # Detect wall
            
            while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                if i ==0:
                    First_Rotate_command=Rotate_command
                i+=1
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.07)
                    stop(0,0.01)
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.07)
                    stop(0,0.01)
                
            while True:
                
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)

                print([i,vt_position, cam_distance])
                
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Move forward at 30% speed until wall is detected
                #move_forward(30)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break    
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    move_right(10)
                    time.sleep(0.07)
                    stop(0, 0.01)
                    Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                    if Rotate_command == "stop":
                        
                        stop(0,0.01)                  
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 1])
                        buzzer.sound(True)
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 0])
                        break 
                elif vt_position == "Right":
                    print("Adjusting to the right...")
                    move_left(10)
                    time.sleep(0.07)
                    stop(0, 0.01)
                    Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                    if Rotate_command == "stop":
                        
                        stop(0,0.01)                  
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 1])
                        buzzer.sound(True)
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 0])
                        break 
                elif vt_position == "Centered":
                    stop(0,0.01)
                    print("Yellow object centered. Proceeding...")
                    Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                    print(Rotate_command)
                    move_forward(10)
                    time.sleep(0.07)
                    if Rotate_command == "stop":
                        
                        stop(0,0.01)                  
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 1])
                        buzzer.sound(True)
                        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [42, 0])
                        break 
                    move_forward(5)
                    time.sleep(0.07)
                        
                elif vt_position =="":
                    move_backward(5)
                    time.sleep(0.05)
                    '''if First_Rotate_command=="Anticlockwise":
                        rotate_anticlockwise(5)
                        time.sleep(0.07)
                        stop(0,0.01)
                    #elif First_Rotate_command=="Clockwise":
                        # rotate_clockwise(5)
                        # time.sleep(0.07)
                        # stop(0,0.01)
                    # else:
                        # rotate_clockwise(5)
                        # time.sleep(0.07)
                        #stop(0,0.01)'''
                   
                    
            move_backward(10)
            
            time.sleep(2)
            stop(0,0.4)
            i=0
            servo_control()
            while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    i+=1
                    if i>=10:
                        break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
            
            i=0
            while True:
                
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)

                print([i,vt_position, cam_distance])
                
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Move forward at 30% speed until wall is detected
                #move_forward(30)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break    
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    i=0
                    move_right(10)
                    time.sleep(0.07)
                    stop(0,0.01)
                elif vt_position == "Right":
                    i=0
                    print("Adjusting to the right...")
                    move_left(10)
                    time.sleep(0.07)
                    stop(0,0.01)
                elif vt_position == "Centered":
                    i+=1
                    print("Yellow object centered. Proceeding...")
                    if i >10:
                        break
            
            while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    i+=1
                    if i>=10:
                        break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
            
            
            move_left(10)
            time.sleep(0.14)
            stop(0,0.01)



            Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)

            while average_distance < 500:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                move_backward(10)
                print(average_distance)
                print(f"initial {initial_distance}")
            
            stop(0,1)
            
            
                       
            '''Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)

            while average_distance<1500:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                move_backward(50)
                print(average_distance)
                print(f"initial {initial_distance}")
            
            stop(0,1)'''
            
            i=0
            while True:
                
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration_green(frame)

                print([i,vt_position, cam_distance])
                
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Move forward at 30% speed until wall is detected
                #move_forward(30)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break    
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    i=0
                    rotate_anticlockwise(5)
                    time.sleep(0.02)
                    stop(0,0.01)
                elif vt_position == "Right":
                    i=0
                    print("Adjusting to the right...")
                    rotate_clockwise(5)
                    time.sleep(0.02)
                    stop(0,0.01)
                elif vt_position == "Centered":
                    i+=1
                    print("Yellow object centered. Proceeding...")
                    if i >10:
                        break
            
            
            '''while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    i+=1
                    if i>=10:
                        break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
            
                        
            i=0
            while True:
                
                frame = picam2.capture_array()
                vt_position, cam_distance, processed_frame, mask = middle_calibration(frame)

                print([i,vt_position, cam_distance])
                
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Move forward at 30% speed until wall is detected
                #move_forward(30)
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break    
                print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                if vt_position == "Left":
                    print("Adjusting to the left...")
                    i=0
                    move_right(10)
                    time.sleep(0.07)
                    stop(0,0.01)
                elif vt_position == "Right":
                    i=0
                    print("Adjusting to the right...")
                    move_left(10)
                    time.sleep(0.07)
                    stop(0,0.01)
                elif vt_position == "Centered":
                    i+=1
                    print("Yellow object centered. Proceeding...")
                    if i >10:
                        break
            

            
            while True:
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                print(f"Rotate Action: {Rotate_command} and {average_distance}")

                if not sensor1 or not sensor2:
                    print("Failed to initialize sensors")
                    break
                
                if Rotate_command == "Parallel":
                    print("Parallel")
                    i+=1
                    if i>=10:
                        break
                    
                elif Rotate_command == "Anticlockwise":
                    rotate_anticlockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0
                    #time.sleep (0.01)
                elif Rotate_command == "Clockwise":
                    rotate_clockwise(5)
                    time.sleep(0.03)
                    stop(0,0.01)
                    i=0'''
            
            
            
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
                move_backward(5)
                # print(f" {i} Yellow Position: {vt_position}, Distance: {cam_distance:.2f} cm")
                # if vt_position == "Left":
                    # print("Adjusting to the left...")
                    # backwardleft(10)
                # elif vt_position == "Right":
                    # print("Adjusting to the right...")
                    # backwardright(10)
                # elif vt_position == "Centered":
                    # print("Yellow object centered. Proceeding...")
                # if Rotate_command == "Parallel":
                    # print("Parallel")
                    # move_backward(10)
                # elif Rotate_command == "Anticlockwise":
                    # backward_lateral_anticlockwise(10)
                    # time.sleep (0.01)
                # elif Rotate_command == "Clockwise":
                    # backward_lateral_clockwise(10)
                    # time.sleep(0.01)
                i+=1
                if cv2.waitKey(1) & 0xFF == 27:
                    stop(0,1)
                    break

	            # Color detection method for the original target
                result = color_detecting()
                Rotate_command,average_distance = process_laser_data(sensor1, sensor2, sensor1_state, sensor2_state)
                if average_distance> initial_distance-900:
                    break
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

            
            # Visual center
            while True:
                frame, mask, x_cmd, y_cmd = process_frame(camera, center_point)

                # Display the frame and mask
                if frame is not None:
                    cv2.imshow("Smart Circle Tracking", frame)
                if mask is not None:
                    cv2.imshow("Color Mask", mask)
                
                if x_cmd == None:
                    break
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
                    
            


    except KeyboardInterrupt:
        pass
    
    finally:
        # Cleanup
        io.cleanup(all_pins)
        sensor1.close()
        sensor2.close()
        camera.release()
        cv2.destroyAllWindows()
        execute_device_command(port= Extension_GPIO_Port,baudrate= 115200, command_index=2, input_array= [41, 0])

if __name__ == "__main__":
    main()

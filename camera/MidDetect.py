import socket
import cv2
import numpy as np

# ---------------------- TCP Connection Setup ----------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("raspberrypi.local", 5005))  # Replace with Pi's IP or hostname

# Calibration constants for distance calculation
KNOWN_DISTANCE = 50.0  # Distance to object in cm during calibration
KNOWN_WIDTH =   4.9     # Width of object in cm during calibration

# Initialize focal length (calculated based on calibration images)
FOCAL_LENGTH = 1473.67  # Replace with your calculated focal length

# Tolerance for determining object position
tolerance = 20
#chassis State
ch_state = 0 # 0: middle, 1:go left, 2:go right
try:
    while True:
        # ---------------------- Step 1: Receive Frame ----------------------
        raw_size = client_socket.recv(4)
        if len(raw_size) < 4:
            break
        frame_size = int.from_bytes(raw_size, 'big')

        encoded_frame = b""
        while len(encoded_frame) < frame_size:
            packet = client_socket.recv(frame_size - len(encoded_frame))
            if not packet:
                break
            encoded_frame += packet

        if len(encoded_frame) < frame_size:
            break

        frame_array = np.frombuffer(encoded_frame, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        if frame is None:
            continue

        # ---------------------- Step 2: Yellow Object Detection ----------------------
        height, width, _ = frame.shape
        frame_center_x, frame_center_y = width // 2, height // 2

        roi_left = int(0.15 * width)
        roi_right = int(0.85 * width)
        roi_top = 0
        roi_bottom = height

        cv2.rectangle(frame, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)
        roi = frame[roi_top:roi_bottom, roi_left:roi_right]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        mask = cv2.inRange(hsv_roi, lower_yellow, upper_yellow)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        yellow_position = ""
        distance_to_yellow = None

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            if area > 50:
                x, y, w, h = cv2.boundingRect(largest_contour)
                label_center_x = x + w // 2
                label_center_y = y + h // 2
                absolute_label_center_x = roi_left + label_center_x

                # Distance Calculation
                distance_to_yellow = (KNOWN_WIDTH * FOCAL_LENGTH) / w  # Using detected width

                if abs(absolute_label_center_x - frame_center_x) <= tolerance:
                    yellow_position = "Centered"
                elif absolute_label_center_x < frame_center_x - tolerance:
                    yellow_position = "Left"
                elif absolute_label_center_x > frame_center_x + tolerance:
                    yellow_position = "Right"

                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.circle(roi, (label_center_x, label_center_y), 3, (0, 0, 255), -1)
                cv2.putText(frame, f"Yellow is: {yellow_position}", (roi_left, roi_top + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, f"Distance: {distance_to_yellow:.2f} cm", (roi_left, roi_top + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            else:
                cv2.putText(frame, "Yellow detected but too small", (roi_left, roi_top + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "No Yellow detected", (roi_left, roi_top + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # ---------------------- Step 3: Display Results ----------------------
        cv2.imshow("Camera Feed", frame)
        cv2.imshow("Yellow Mask ROI", mask)
        if yellow_position == "Left":
            ch_state = 2
        elif yellow_position == "Right":
            ch_state = 1
        else:
            ch_state = 0
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    client_socket.close()
    cv2.destroyAllWindows()
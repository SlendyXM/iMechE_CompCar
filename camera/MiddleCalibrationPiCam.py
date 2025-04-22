from picamera2 import Picamera2
import cv2
import numpy as np

def middle_calibration(frame, tolerance=20):
    # Calibration constants for distance calculation
    KNOWN_DISTANCE = 50.0  # Distance to object in cm during calibration
    KNOWN_WIDTH = 4.9  # Width of object in cm during calibration
    FOCAL_LENGTH = 1473.67  # Replace with your calculated focal length
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, -1)
    # ---------------------- Step 2: Blue Object Detection ----------------------
    height, width, _ = frame.shape
    frame_center_x = width // 2

    roi_left = int(0.15 * width)
    roi_right = int(0.85 * width)
    roi_top = 0
    roi_bottom = height

    roi = frame[roi_top:roi_bottom, roi_left:roi_right]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define HSV range for blue
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv_roi, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blue_position = ""
    distance_to_blue = 100000000

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        if area > 50:  # Filter small contours
            x, y, w, h = cv2.boundingRect(largest_contour)
            label_center_x = x + w // 2
            absolute_label_center_x = roi_left + label_center_x

            # Distance Calculation
            distance_to_blue = (KNOWN_WIDTH * FOCAL_LENGTH) / w

            if abs(absolute_label_center_x - frame_center_x) <= tolerance:
                blue_position = "Centered"
            elif absolute_label_center_x < frame_center_x - tolerance:
                blue_position = "Left"
            elif absolute_label_center_x > frame_center_x + tolerance:
                blue_position = "Right"

            cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f"Blue is: {blue_position}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(frame, f"Distance: {distance_to_blue:.2f} cm", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Return position, distance, frame, and mask for debugging
    return blue_position, distance_to_blue, frame, mask


if __name__ == "__main__":
    # Parameter to select camera type: 1 for Pi Camera, 0 for USB Camera
    pi_or_usbcam = 1  # Change this to 0 for USB Camera

    if pi_or_usbcam == 1:
        # Initialize the Pi Camera using picamera2
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(main={"size": (640, 480)})
        picam2.configure(config)
        picam2.start()

        try:
            while True:
                # Capture a frame from the Pi Camera
                frame = picam2.capture_array()


                # Call the middle_calibration function
                position, distance, processed_frame, mask = middle_calibration(frame)

                # Display the frame and mask for debugging
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Exit on 'Esc' key
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        finally:
            # Release the camera and close all windows
            picam2.stop()
            cv2.destroyAllWindows()

    elif pi_or_usbcam == 0:
        # Initialize the USB Camera
        video_capture = cv2.VideoCapture(1, cv2.CAP_V4L2)

        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set lower resolution
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not video_capture.isOpened():
            print("Error: Could not open camera")
            exit()

        try:
            while True:
                # Capture a frame from the USB camera
                ret, frame = video_capture.read()
                if not ret:
                    print("Failed to grab frame")
                    break

                # Call the middle_calibration function
                position, distance, processed_frame, mask = middle_calibration(frame)

                # Display the frame and mask for debugging
                if processed_frame is not None and mask is not None:
                    cv2.imshow("Camera Feed", processed_frame)
                    cv2.imshow("Mask", mask)

                # Exit on 'Esc' key
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        finally:
            # Release the camera and close all windows
            video_capture.release()
            cv2.destroyAllWindows()

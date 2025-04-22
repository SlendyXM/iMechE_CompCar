from camera.MiddleCalibrationTesting import middle_calibration
import cv2

def main():
    # Initialize the camera
    video_capture = cv2.VideoCapture(1, cv2.CAP_V4L2)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set lower resolution
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not video_capture.isOpened():
        print("Error: Could not open camera")
        return

    try:
        while True:
            # Capture position, distance, frame, and mask
            position, distance, frame, mask = middle_calibration(video_capture)

            # Display the frame and mask for debugging
            if frame is not None and mask is not None:
                cv2.imshow("Camera Feed", frame)
                cv2.imshow("Mask", mask)

            # Check if a blue object is detected
            if position:
                print(f"Detected Position: {position}, Distance: {distance:.2f} cm")

                # Stop if the object is too close
                if distance is not None and distance <= 5:
                    print("Object too close. Stopping...")
                    break

                # Adjust direction based on the object's position
                if position == "Left":
                    print("Adjusting to the left...")
                elif position == "Right":
                    print("Adjusting to the right...")
                elif position == "Centered":
                    print("Object centered. Moving forward...")
            else:
                print("No object detected. Moving forward...")

            # Exit on 'Esc' key
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        # Release the camera and close all windows
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

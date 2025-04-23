import cv2
import numpy as np

# Define color ranges in HSV
COLOR_RANGES = {
    'yellow': {
        'lower': np.array([18, 70, 140]),  # Adjusted lower bound
        'upper': np.array([32, 255, 255]),  # Adjusted upper bound
        'color': (0, 255, 255)  # Yellow in BGR
    },
    'red': {
        'lower': np.array([0, 150, 50]),
        'upper': np.array([10, 255, 255]),
        'color': (0, 0, 255)  # Red in BGR
    },
    'blue': {
        'lower': np.array([90, 50, 50]),
        'upper': np.array([130, 255, 255]),
        'color': (255, 0, 0)  # Blue in BGR
    }
}


def detect_sphere(frame, color_name):
    """Detect a sphere of specified color"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_data = COLOR_RANGES[color_name]

    mask = cv2.inRange(hsv, color_data['lower'], color_data['upper'])
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        if len(largest_contour) >= 5:
            # Fit an ellipse to the contour
            ellipse = cv2.fitEllipse(largest_contour)
            center = (int(ellipse[0][0]), int(ellipse[0][1]))
            axes = (int(ellipse[1][0] / 2), int(ellipse[1][1] / 2))  # Semi-major and semi-minor axes
            angle = ellipse[2]  # Rotation angle of the ellipse

            # Only consider valid ellipses with a minimum size
            if axes[0] > 10 and axes[1] > 10:  # Adjust the threshold as needed
                return {
                    'center': center,
                    'axes': axes,
                    'angle': angle,
                    'color': color_name,
                    'color_bgr': color_data['color']
                }
    return None




def get_movement_commands(center, frame_width, frame_height, tolerance=20):
    """Determine movement commands based on centroid position"""
    center_x, center_y = 325, 360
    #center_x, center_y = frame_width // 2, frame_height // 2
    x, y = center

    # X-axis movement
    if abs(x - center_x) <= tolerance:
        x_cmd = "CENTER"
    elif x < center_x - tolerance:
        x_cmd = "GO LEFT"
    else:
        x_cmd = "GO RIGHT"

    # Y-axis movement
    if abs(y - center_y) <= tolerance:
        y_cmd = "CENTER"
    elif y < center_y - tolerance:
        y_cmd = "GO STRAIGHT"
    else:
        y_cmd = "GO BACK"

    return x_cmd, y_cmd


def main(camera):
    while True:
        ret, frame = camera.read()

        if not ret:
            break

        height, width = frame.shape[:2]
        center_x, center_y = 325, 560

        # Draw center lines and crosshair
        cv2.line(frame, (center_x, 0), (center_x, height), (255, 255, 255), 1)
        cv2.line(frame, (0, center_y), (width, center_y), (255, 255, 255), 1)
        cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)

        # Try detecting partial circles in order of priority
        detected = None
        mask = None  # Initialize mask
        for color in ['yellow', 'red']:  # Red is now the highest priority
            detected = detect_partial_circle(frame, color)
            if detected:
                # Generate the mask for the detected color
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                color_data = COLOR_RANGES[color]
                mask = cv2.inRange(hsv, color_data['lower'], color_data['upper'])
                break

        if detected:
            # Draw the detected circle
            circle_center = detected['center']
            radius = detected['radius']
            diameter = 2 * radius

            # Filter out circles with diameter < 200
            if diameter < 200:
                print(f"Circle filtered out - Diameter: {diameter:.2f} px")
            else:
                cv2.circle(frame, circle_center, radius, detected['color_bgr'], 3)
                cv2.circle(frame, circle_center, 5, detected['color_bgr'], -1)

                # Calculate the size of the circle
                area = np.pi * (radius ** 2)

                # Display circle info
                cv2.putText(frame, detected['color'].upper(),
                            (circle_center[0] + 15, circle_center[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            detected['color_bgr'], 2)

                cv2.putText(frame, f"({circle_center[0]},{circle_center[1]})",
                            (circle_center[0] + 15, circle_center[1] + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            detected['color_bgr'], 1)

                # Display the size of the circle
                cv2.putText(frame, f"Diameter: {diameter:.2f} px", (10, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(frame, f"Area: {area:.2f} px^2", (10, 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                # Print the size of the circle to the console
                print(f"Detected Circle - Color: {detected['color']}, Center: {circle_center}, Radius: {radius}, Diameter: {diameter:.2f}, Area: {area:.2f}")

                # Get movement commands
                x_cmd, y_cmd = get_movement_commands(circle_center, width, height)

                # Display movement commands
                cv2.putText(frame, f"X: {x_cmd}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Y: {y_cmd}", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Display detection info
                cv2.putText(frame, f"Detected: {detected['color']}", (10, 110),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            cv2.putText(frame, "No circle detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Display instructions
        cv2.putText(frame, "Detection priority: Red -> Yellow -> Blue", (10, height - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Display the mask (rotate it by 180 degrees if it exists)
        if mask is not None:
            cv2.imshow("Color Mask", mask)

        # Display the original frame
        cv2.imshow('Smart Circle Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()







def detect_partial_circle(frame, color_name):
    """Detect a partial circle of specified color"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_data = COLOR_RANGES[color_name]

    mask = cv2.inRange(hsv, color_data['lower'], color_data['upper'])
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        if len(largest_contour) >= 5:
            # Fit a minimum enclosing circle to the contour
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            center = (int(x), int(y))
            radius = int(radius)

            # Only consider valid circles with a minimum radius
            if radius > 10:  # Adjust the threshold as needed
                return {
                    'center': center,
                    'radius': radius,
                    'color': color_name,
                    'color_bgr': color_data['color']
                }
    return None



if __name__ == '__main__':
    print("Happy")
    camera = cv2.VideoCapture(1,cv2.CAP_V4L2)
    print("Sad")
    #camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set resolution width
    #.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set resolution height

    # Reduce exposure time
    # Note: The value for exposure depends on the camera. Experiment with different values.
    # A negative value (e.g., -4) may be required for some cameras to enable manual exposure.
    camera.set(cv2.CAP_PROP_EXPOSURE, -0.3)
    print("Current Exposure:", camera.get(cv2.CAP_PROP_EXPOSURE))

    print("Angry")
    main(camera)






# def main(camera):

#     while True:
#         ret, frame = camera.read()
#         if not ret:
#             break

#         height, width = frame.shape[:2]
#         #center_x, center_y = width // 2, height // 2
#         center_x, center_y = 320,400

#         # Draw center lines and crosshair
#         cv2.line(frame, (center_x, 0), (center_x, height), (255, 255, 255), 1)
#         cv2.line(frame, (0, center_y), (width, center_y), (255, 255, 255), 1)
#         cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)

#         # Try detecting spheres in order of priority
#         detected = None
#         for color in ['red','yellow', 'blue']:
#             detected = detect_sphere(frame, color)
#             if detected:
#                 break

#         if detected:
#             # Draw the detected ellipse
#             ellipse_center = detected['center']
#             axes = detected['axes']
#             angle = detected['angle']
#             cv2.ellipse(frame, (ellipse_center, (axes[0] * 2, axes[1] * 2), angle), detected['color_bgr'], 3)
#             cv2.circle(frame, ellipse_center, 5, detected['color_bgr'], -1)

#             # Display sphere info
#             cv2.putText(frame, detected['color'].upper(),
#                         (ellipse_center[0] + 15, ellipse_center[1]),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7,
#                         detected['color_bgr'], 2)

#             cv2.putText(frame, f"({ellipse_center[0]},{ellipse_center[1]})",
#                         (ellipse_center[0] + 15, ellipse_center[1] + 25),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5,
#                         detected['color_bgr'], 1)

#             # Get movement commands
#             x_cmd, y_cmd = get_movement_commands(ellipse_center, width, height)

#             # Display movement commands
#             cv2.putText(frame, f"X: {x_cmd}", (10, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
#             cv2.putText(frame, f"Y: {y_cmd}", (10, 70),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

#             # Display detection info
#             cv2.putText(frame, f"Detected: {detected['color']}", (10, 110),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#         else:
#             cv2.putText(frame, "No sphere detected", (10, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

#         # Display instructions
#         cv2.putText(frame, "Detection priority: Yellow -> Red -> Blue", (10,  height - 40),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#         cv2.imshow('Smart Sphere Tracking', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     camera.release()
#     cv2.destroyAllWindows()

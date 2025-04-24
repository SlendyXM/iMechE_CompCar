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
                    'color_bgr': color_data['color'],
                    'mask': mask
                }
    return {'mask': mask}


def get_movement_commands(center, center_point, tolerance=20):
    """Determine movement commands based on centroid position"""
    center_x, center_y = center_point
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


def process_frame(camera, center_point):
    """Process a single frame from the camera and return movement commands"""
    ret, frame = camera.read()
    if not ret:
        return None, None, None, None  # Return None if no frame is captured

    height, width = frame.shape[:2]
    detected = None
    mask = None

    # Draw center lines and crosshair
    center_x, center_y = center_point
    cv2.line(frame, (center_x, 0), (center_x, height), (255, 255, 255), 1)
    cv2.line(frame, (0, center_y), (width, center_y), (255, 255, 255), 1)
    cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)

    # Try detecting partial circles in order of priority
    for color in ['yellow', 'red']:  # Red is now the highest priority
        detected = detect_partial_circle(frame, color)
        if detected and 'center' in detected:
            mask = detected['mask']
            break

    if detected and 'center' in detected:
        circle_center = detected['center']
        radius = detected['radius']
        diameter = 2 * radius

        # Filter out circles with diameter < 200
        if diameter < 200:
            print(f"Circle filtered out - Diameter: {diameter:.2f} px")
            return frame, mask, None, None

        # Draw the detected circle
        cv2.circle(frame, circle_center, radius, detected['color_bgr'], 3)
        cv2.circle(frame, circle_center, 5, detected['color_bgr'], -1)

        # Get movement commands
        x_cmd, y_cmd = get_movement_commands(circle_center, center_point)

        # Print the detected circle info
        print(f"Detected Circle - Color: {detected['color']}, Center: {circle_center}, "
              f"Radius: {radius}, Diameter: {diameter:.2f}")

        return frame, mask, x_cmd, y_cmd

    # If no circle is detected
    print("No circle detected")
    return frame, mask, None, None


if __name__ == "__main__":
    print("Initializing camera...")
    camera = cv2.VideoCapture(1, cv2.CAP_V4L2)

    # Set camera properties
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_EXPOSURE, -0.3)
    print("Current Exposure:", camera.get(cv2.CAP_PROP_EXPOSURE))

    center_point = (325, 360)  # Default center point

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
                print(f"X Command: {x_cmd}, Y Command: {y_cmd}")

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()

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
                    'color_bgr': color_data['color'],
                    'mask': mask
                }
    return {'mask': mask}


def get_movement_commands(center, center_point, tolerance=20):
    """Determine movement commands based on centroid position"""
    center_x, center_y = center_point
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


def process_frame(camera, center_point):
    """Process a single frame from the camera and return movement commands"""
    ret, frame = camera.read()
    if not ret:
        return None, None, None, None  # Return None if no frame is captured

    height, width = frame.shape[:2]
    detected = None
    mask = None

    # Draw center lines and crosshair
    center_x, center_y = center_point
    cv2.line(frame, (center_x, 0), (center_x, height), (255, 255, 255), 1)
    cv2.line(frame, (0, center_y), (width, center_y), (255, 255, 255), 1)
    cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)

    # Try detecting partial circles in order of priority
    for color in ['yellow', 'red']:  # Red is now the highest priority
        detected = detect_partial_circle(frame, color)
        if detected and 'center' in detected:
            mask = detected['mask']
            break

    if detected and 'center' in detected:
        circle_center = detected['center']
        radius = detected['radius']
        diameter = 2 * radius

        # Filter out circles with diameter < 200
        if diameter < 200:
            print(f"Circle filtered out - Diameter: {diameter:.2f} px")
            return frame, mask, None, None

        # Draw the detected circle
        cv2.circle(frame, circle_center, radius, detected['color_bgr'], 3)
        cv2.circle(frame, circle_center, 5, detected['color_bgr'], -1)

        # Get movement commands
        x_cmd, y_cmd = get_movement_commands(circle_center, center_point)

        # Print the detected circle info
        print(f"Detected Circle - Color: {detected['color']}, Center: {circle_center}, "
              f"Radius: {radius}, Diameter: {diameter:.2f}")

        return frame, mask, x_cmd, y_cmd

    # If no circle is detected
    print("No circle detected")
    return frame, mask, None, None


if __name__ == "__main__":
    print("Initializing camera...")
    camera = cv2.VideoCapture(1, cv2.CAP_V4L2)

    # Set camera properties
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_EXPOSURE, -0.3)
    print("Current Exposure:", camera.get(cv2.CAP_PROP_EXPOSURE))

    center_point = (325, 360)  # Default center point

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
                print(f"X Command: {x_cmd}, Y Command: {y_cmd}")

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


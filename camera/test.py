import socket
import cv2
from picamera2 import Picamera2

# Initialize the camera
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(video_config)
picam2.start()

# Set up TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 5005))  # Bind to port 5005
server_socket.listen(1)  # Listen for a single connection
print("Waiting for a connection...")

# Accept connection from the client
conn, addr = server_socket.accept()
print(f"Connected to {addr}")

try:
    while True:
        frame = picam2.capture_array()

        # Encode frame as JPEG
        _, encoded_frame = cv2.imencode('.jpg', frame)

        # Send the size of the frame first (fixed length)
        frame_size = len(encoded_frame.tobytes())
        conn.sendall(frame_size.to_bytes(4, 'big'))

        # Send the encoded frame
        conn.sendall(encoded_frame.tobytes())

finally:
    picam2.stop()
    conn.close()
    server_socket.close()

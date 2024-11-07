import cv2
from ultralytics import YOLO
import cv2
import subprocess
import numpy as np
import time
from time import sleep
from motor_control import (
    initialize_thrusters,
    start_heave,
    start_stern_thrusters,
    start_bow_thrusters,
    stop_bow_thrusters,
    slow_down_heave_thruster,
    slow_down_stern_thrusters,
)

# Load the YOLO model (adjust the path as needed for your environment)
model = YOLO("epoch_100.pt")

# Command to capture an image with libcamera on Raspberry Pi
capture_command = [
    "libcamera-jpeg",
    "-o", "-",        # Output to standard output
    "--width", "640", # Set desired resolution
    "--height", "480",
    "--nopreview"     # Disable preview to speed up the capture
]

# Initialize thrusters before starting the loop
initialize_thrusters()

frame_center_x = 640 // 2  # X-coordinate of the frame's center (assuming 640x480 resolution)

while True:
    # Capture the image using libcamera-jpeg
    result = subprocess.run(capture_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Error capturing image:", result.stderr.decode())
        break

    # Convert the captured JPEG bytes to a numpy array
    image_array = np.frombuffer(result.stdout, np.uint8)
    # Decode JPEG to OpenCV BGR format
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Start time for inference
    _time_start = time.time()
    
    # Perform inference with YOLOv8
    results = model.predict(image, show=True)

    # Print the inference time
    print("Inference time:", time.time() - _time_start)

    # Check if there are any detections
    if len(results[0].boxes) == 0:
        print("No object detected, moving forward")
        start_stern_thrusters()  # Move forward using stern thrusters
        sleep(1)
        slow_down_stern_thrusters()
    else:
        # Loop through the detections
        for result in results:
            boxes = result.boxes  # Extract detected bounding boxes
            
            for box in boxes:
                # Get the coordinates of the bounding box
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # Find the center of the bounding box
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # Draw the center point on the image
                cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)

                # Optionally draw the bounding box for the gate
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

                # Print the coordinates of the center
                print(f"Center of the gate: ({center_x}, {center_y})")
                
                # Decision-making logic based on object position
                if center_x < frame_center_x - 50:  # Object is on the left side of the frame
                    print("Object on the left, turning right")
                    start_bow_thrusters()
                    sleep(1)
                    stop_bow_thrusters()
                elif center_x > frame_center_x + 50:  # Object is on the right side of the frame
                    print("Object on the right, turning left")
                    start_bow_thrusters()
                    sleep(1)
                    stop_bow_thrusters()
                else:
                    print("Object centered, moving forward")
                    start_stern_thrusters()
                    sleep(1)
                    slow_down_stern_thrusters()

    # Display the image with the detection and center point
    cv2.imshow("Gate Detection", image)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()

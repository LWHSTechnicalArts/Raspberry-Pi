import os
os.environ["OPENCV_IO_ENABLE_JASPER"] = "1"  # Suppress libpng ICC profile warnings
from gpiozero import LED
from picamera2 import Picamera2
import cv2
import numpy as np
import time

# Initialize the LED
red_led = LED(21)

# Start with LED off
red_led.off()
led_on = False

# Initialize the camera
print("[INFO] Waiting for camera to warm up...")
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()
time.sleep(2.0)

# Define dummy HSV range values
color_lower = np.array([0, 0, 0])
color_upper = np.array([255, 255, 255])

# Create a window for trackbars
cv2.namedWindow("Trackbars")

# Trackbar callback function
def nothing(x):
    pass

# Create trackbars for HSV range
cv2.createTrackbar("H Lower", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("H Upper", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("S Lower", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("S Upper", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("V Lower", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("V Upper", "Trackbars", 255, 255, nothing)

print("[INFO] Starting video stream...")
try:
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Rotate and correct colors
        #frame = cv2.rotate(frame, cv2.ROTATE_180)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize the frame for smaller display
        frame = cv2.resize(frame, (320, 240))

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Get the current positions of trackbars
        h_lower = cv2.getTrackbarPos("H Lower", "Trackbars")
        h_upper = cv2.getTrackbarPos("H Upper", "Trackbars")
        s_lower = cv2.getTrackbarPos("S Lower", "Trackbars")
        s_upper = cv2.getTrackbarPos("S Upper", "Trackbars")
        v_lower = cv2.getTrackbarPos("V Lower", "Trackbars")
        v_upper = cv2.getTrackbarPos("V Upper", "Trackbars")

        # Update the HSV range
        color_lower = np.array([h_lower, s_lower, v_lower], dtype=np.uint8)
        color_upper = np.array([h_upper, s_upper, v_upper], dtype=np.uint8)

        # Create the mask
        mask = cv2.inRange(hsv, color_lower, color_upper)

        # Resize the mask for smaller display
        mask = cv2.resize(mask, (320, 240))

        # Convert mask to BGR for side-by-side display
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # Concatenate the original frame and mask horizontally
        side_by_side = np.hstack((frame, mask_bgr))

        # Display the side-by-side output
        cv2.imshow("Frame and Mask", side_by_side)

        # Break the loop with the ESC key
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    print("\n[INFO] Exiting program and cleaning up...")
    red_led.off()
    cv2.destroyAllWindows()
    picam2.stop()



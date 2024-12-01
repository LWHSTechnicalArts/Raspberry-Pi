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

# Define the lower and upper boundaries of the object
color_lower = np.array([53, 119, 62])  # Adjusted values
color_upper = np.array([150, 255, 235])  # Adjusted values

print("[INFO] Starting video stream...")
try:
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Rotate and correct colors
        #frame = cv2.rotate(frame, cv2.ROTATE_180)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to HSV and create mask
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, color_lower, color_upper)

        # Erode and dilate the mask to clean up noise
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Process contours
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # Find the largest contour and compute the minimum enclosing circle
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            if radius > 10:
                # Draw the circle and centroid on the frame
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                if not led_on:
                    red_led.on()
                    led_on = True
        elif led_on:
            red_led.off()
            led_on = False

        # Convert mask to BGR for side-by-side display
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # Concatenate the original frame and mask horizontally
        side_by_side = np.hstack((frame, mask_bgr))

        # Resize the side-by-side output for a smaller preview
        side_by_side_small = cv2.resize(side_by_side, (640, 240))  # Adjust resolution here

        # Display the smaller side-by-side output
        cv2.imshow("Frame and Mask", side_by_side_small)

        # Break the loop with the ESC key
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    print("\n[INFO] Exiting program and cleaning up...")
    red_led.off()
    cv2.destroyAllWindows()
    picam2.stop()

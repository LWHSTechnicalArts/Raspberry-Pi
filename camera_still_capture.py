from picamera2 import Picamera2, Preview
from libcamera import Transform
import os
import time

# Define the Desktop path
desktop_path = os.path.expanduser("~/Desktop/")

# Initialize the camera
picam2 = Picamera2()

# Configure the preview
picam2.start_preview(Preview.QTGL, x=100, y=100, width=800, height=600, transform=Transform(hflip=1))

# Start the camera
picam2.start()
print("Preview started. Showing for 5 seconds...")

# Show preview for 5 seconds
time.sleep(5)

# Capture the image
image_path = os.path.join(desktop_path, "captured_image.jpg")
print(f"Capturing image and saving to {image_path}...")
picam2.capture_file(image_path)

# Stop the camera
picam2.stop()
print("Preview closed and image saved.")

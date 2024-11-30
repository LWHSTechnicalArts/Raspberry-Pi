import os
from datetime import datetime
from picamera2 import Picamera2
import time

# Initialize the camera
picam2 = Picamera2()

# Configure the camera for still capture
picam2.configure(picam2.create_still_configuration())

# Start the camera
picam2.start()
print("Camera warming up...")
time.sleep(2)  # Allow the camera to adjust

# Generate a timestamp for folder and filename
now = datetime.now()
tstamp = "{0:%Y}-{0:%m}-{0:%d}_{0:%H}_{0:%M}_{0:%S}".format(now)

# Create a directory on the Desktop with the timestamp
desktop_path = os.path.expanduser("~/Desktop/")
directory_path = os.path.join(desktop_path, tstamp)
os.mkdir(directory_path)  # Create the directory
os.chdir(directory_path)  # Change to the directory

# Capture the image with a date-stamped filename
image_filename = f"image_{tstamp}.jpg"
picam2.capture_file(image_filename)
print(f"Image captured and saved as: {image_filename}")

# Stop the camera
picam2.stop()

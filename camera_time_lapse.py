from picamera2 import Picamera2
from datetime import datetime
import os
import time

# Initialize the camera
picam2 = Picamera2()

# Configure the camera for still capture
picam2.configure(picam2.create_still_configuration())

# Start the camera
picam2.start()
print("Camera warming up...")
time.sleep(2)  # Allow the camera to adjust

# Generate a date-stamped folder
now = datetime.now()
tstamp = now.strftime("%Y-%m-%d_%H-%M-%S")
desktop_path = os.path.expanduser("~/Desktop/")
folder_path = os.path.join(desktop_path, tstamp)
os.makedirs(folder_path)  # Create the folder

# Capture 10 images and save them in the date-stamped folder
for i in range(10):
    filename = f"image{i:04d}.jpg"
    file_path = os.path.join(folder_path, filename)
    print(f"Capturing {file_path}...")
    picam2.capture_file(file_path)

print(f"All images captured and saved in folder: {folder_path}")

# Stop the camera
picam2.stop()

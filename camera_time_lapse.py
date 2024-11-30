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

# Capture 10 images in a loop
for i in range(10):
    filename = f"image{i:04d}.jpg"
    print(f"Capturing {filename}...")
    picam2.capture_file(filename)

print("All images captured.")

# Stop the camera
picam2.stop()

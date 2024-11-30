from picamera2 import Picamera2
import time
import os

# Define the Desktop path
desktop_path = os.path.expanduser("~/Desktop/")

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start()

print("Camera preview started. Check the output window.")
time.sleep(5)  # Preview for 5 seconds

# Save the image to the Desktop
image_path = os.path.join(desktop_path, "test_image.jpg")
print("Capturing an image...")
picam2.capture_file(image_path)
print(f"Image saved as '{image_path}'")

picam2.stop()

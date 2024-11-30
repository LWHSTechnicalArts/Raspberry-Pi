from picamera2 import Picamera2, Preview
from libcamera import Transform

# Initialize the camera
picam2 = Picamera2()

# Start the preview with specific options
picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600, transform=Transform(hflip=1))

# Start the camera
picam2.start()

print("Preview running... Press Ctrl+C to exit.")

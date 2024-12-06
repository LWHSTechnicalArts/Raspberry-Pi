import cv2
from picamera2 import Picamera2
import numpy as np

# Initialize the camera
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

# Load Haar cascade using the full path
cascade_path = "/home/lick/opencv_haarcascades/haarcascade_frontalface_default.xml"
cascade_path = "/home/lick/opencv_haarcascades/haarcascade_frontalcatface.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

# OpenCV window setup
cv2.namedWindow("Face Detection", cv2.WINDOW_AUTOSIZE)

print("Starting face detection. Press 'q' to exit.")
try:
    while True:
        # Capture frame from the Pi Camera
        frame = picam2.capture_array()
        
        # Convert BGR to RGB for correct color display
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Draw rectangles around detected faces on the RGB frame
        for (x, y, w, h) in faces:
            cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Display the result
        cv2.imshow("Face Detection", rgb_frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Cleanup
    picam2.stop()
    cv2.destroyAllWindows()
    print("Face detection stopped.")

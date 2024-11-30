import cv2
from picamera2 import Picamera2

# Load the Haar Cascade for eye detection
cascade_path = "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
eye_cascade = cv2.CascadeClassifier(cascade_path)

# Initialize the Pi Camera
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

# OpenCV window setup
cv2.namedWindow("Eye Detection", cv2.WINDOW_AUTOSIZE)

print("Starting eye detection. Press 'q' to exit.")
try:
    while True:
        # Capture frame from the Pi Camera
        frame = picam2.capture_array()

        # Convert BGR to RGB for correct color display
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to grayscale for eye detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangles around the eyes
        for (x, y, w, h) in eyes:
            cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

        # Display the resulting frame
        cv2.imshow("Eye Detection", rgb_frame)

        # Break the loop with the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # When everything done, release the camera and close windows
    picam2.stop()
    cv2.destroyAllWindows()
    print("Eye detection stopped.")

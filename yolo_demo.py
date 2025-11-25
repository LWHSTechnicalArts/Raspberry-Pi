rom ultralytics import YOLO
from picamera2 import Picamera2
import cv2

# Load ONNX model
print("Loading ONNX model...")
model = YOLO('yolo11n.onnx', task='detect')

# Setup camera
print("Starting camera...")
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

print("Camera ready! Press 'q' to quit")

while True:
    # Capture frame
    frame = picam2.capture_array()
    
    # Convert RGB to BGR for OpenCV
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Run ONNX inference (faster!)
    results = model(frame, verbose=False)
    annotated_frame = results[0].plot()
    
    # Display
    cv2.imshow('YOLOv11 ONNX', annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()

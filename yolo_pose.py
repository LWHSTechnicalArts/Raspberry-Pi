import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# Use ONNX model
model = YOLO("yolo11n-pose.onnx", task='pose')

# Lower camera resolution
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640,640)}))
picam2.start()

print("Camera ready! Press 'q' to quit")

frame_count = 0
last_annotated = None

while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Process every other frame
    if frame_count % 2 == 0:
        # Lower resolution, higher confidence threshold
        results = model(frame, imgsz=320, conf=0.5, verbose=False)
        last_annotated = results[0].plot()
        
        fps = 1000 / results[0].speed['inference']
        cv2.putText(last_annotated, f'FPS: {fps:.1f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Always display (smooth video)
    if last_annotated is not None:
        cv2.imshow('Pose Detection', last_annotated)
    else:
        cv2.imshow('Pose Detection', frame)
    
    frame_count += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()

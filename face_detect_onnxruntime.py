import cv2
from picamera2 import Picamera2
import onnxruntime as ort
import numpy as np

# Load the model
session = ort.InferenceSession("version-RFB-320.onnx")

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

def detect_faces(frame, session, threshold=0.7, nms_threshold=0.4):
    h, w = frame.shape[:2]
    
    # Ensure we have 3 channels
    if len(frame.shape) == 3 and frame.shape[2] == 4:
        frame = frame[:, :, :3]
    
    # Prepare image for model
    img = cv2.resize(frame, (320, 240))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = (img - 127.0) / 128.0
    img = np.transpose(img, [2, 0, 1])
    img = np.expand_dims(img, axis=0).astype(np.float32)
    
    # Run inference
    confidences, boxes = session.run(None, {session.get_inputs()[0].name: img})
    
    # Collect all valid detections
    detection_boxes = []
    detection_scores = []
    
    for i in range(confidences.shape[1]):
        confidence = confidences[0, i, 1]
        
        if confidence > threshold:
            box = boxes[0, i]
            x1 = int(box[0] * w)
            y1 = int(box[1] * h)
            x2 = int(box[2] * w)
            y2 = int(box[3] * h)
            
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            if x2 > x1 and y2 > y1:
                detection_boxes.append([x1, y1, x2, y2])
                detection_scores.append(float(confidence))
    
    # Apply Non-Maximum Suppression to remove overlapping boxes
    if len(detection_boxes) > 0:
        indices = cv2.dnn.NMSBoxes(
            detection_boxes, 
            detection_scores, 
            threshold, 
            nms_threshold
        )
        
        faces = []
        for i in indices:
            x1, y1, x2, y2 = detection_boxes[i]
            faces.append((x1, y1, x2, y2, detection_scores[i]))
        
        return faces
    
    return []

print("Starting face detection. Press 'q' to exit.")

try:
    while True:
        frame = picam2.capture_array()
        
        # Ensure 3 channels
        if len(frame.shape) == 3 and frame.shape[2] == 4:
            frame = frame[:, :, :3]
        
        # Convert RGB to BGR for OpenCV display
        display_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Detect faces
        faces = detect_faces(frame, session)
        
        # Draw rectangles
        for (x1, y1, x2, y2, conf) in faces:
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(display_frame, f'{conf:.2f}', (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("Face Detection", display_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
finally:
    picam2.stop()
    cv2.destroyAllWindows()
    print("Face detection stopped.")

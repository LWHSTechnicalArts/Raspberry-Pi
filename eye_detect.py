import cv2

# Load the Haar Cascade for eye detection
eye_cascade = cv2.CascadeClassifier('/home/pi/Documents/opencv/data/haarcascades/haarcascade_eye.xml')

# Capture video from webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect eyes
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Draw rectangles around the eyes
    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
    
    # Display the resulting frame
    cv2.imshow('Eye Detection', frame)
    
    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()

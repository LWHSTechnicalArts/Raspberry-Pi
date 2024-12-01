import cv2
import numpy as np

# Read the picture - The 1 means we want the image in BGR
img = cv2.imread('object.jpg', 1)

if img is None:
    print("Error: Could not load image.")
    exit()

# Resize image to 20% in each axis
img = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)

# Convert BGR image to an HSV image
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define lower and upper ranges for the mask
lower_range = np.array([167, 100, 100], dtype=np.uint8)
upper_range = np.array([187, 255, 255], dtype=np.uint8)

# Create a mask for the image
mask = cv2.inRange(hsv, lower_range, upper_range)

# Convert the mask to BGR for side-by-side display
mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

# Concatenate the original image and mask horizontally
side_by_side = np.hstack((img, mask_bgr))

# Display the side-by-side image
cv2.imshow('Original and Mask Side-by-Side', side_by_side)

# Wait for user to press [ESC] key
while True:
    k = cv2.waitKey(0)
    if k == 27:  # ASCII code for ESC key
        break

cv2.destroyAllWindows()

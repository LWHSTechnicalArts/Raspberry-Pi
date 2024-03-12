#pan and tilt example using adafruit_servo bonnet
#download the data set you need at https://github.com/opencv/opencv/tree/master/data/haarcascades

import RPi.GPIO as GPIO          
from time import sleep

from adafruit_servokit import ServoKit

from picamera.array import PiRGBArray
from picamera import PiCamera
import time 
import cv2

kit = ServoKit(channels=16)

face_cascade = cv2.CascadeClassifier('/home/pi/Documents/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

Px,Ix,Dx=-1/160,0,0
Py,Iy,Dy=-0.2/120,0,0
 
#initialize some other required vaqriables
integral_x,integral_y=0,0
differential_x,differential_y=0,0
prev_x,prev_y=0,0

width,height=320,240
camera = PiCamera()
camera.resolution = (width,height)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(width,height))
time.sleep(1)

offset_x = 0
offset_y = 0

#motor start position
kit.servo[0].angle = 90  #pan
kit.servo[1].angle = 30  #tilt

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    frame=cv2.flip(image,1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    #detect face coordinates x,y,w,h
    faces=face_cascade.detectMultiScale(gray,1.3,5) # face_cascade loaded earlier.
    c=0
    for(x,y,w,h) in faces:
        c+=1
        if(c>1):  # we just take care of the first face detected.
            break

        #center of face
        face_centre_x=x+w/2
        face_centre_y=y+h/2
 
        #calculate pixels to move 
        error_x=160-face_centre_x  # X-coordinate of Centre of frame is 160
        error_y=120-face_centre_y # Y-coordinate of Centre of frame is 120
 
        integral_x=integral_x+error_x
        integral_y=integral_y+error_y
 
        differential_x= prev_x- error_x
        differential_y= prev_y- error_y
 
        prev_x=error_x
        prev_y=error_y
        
        valx=Px*error_x +Dx*differential_x + Ix*integral_x
        valy=Py*error_y +Dy*differential_y + Iy*integral_y
        
        valx=round(valx,2)
        valy=round(valy,2)
        
        print('pixelerrorx=',error_x,'valx=',valx)
        print('pixelerrory=',error_y,'valy=',valy)
        
        move=5
        tolerance=10
        
        if (error_x > tolerance):
            offset_x+=move
        elif (error_x < -tolerance):
            offset_x-=move
        
        if (error_y > tolerance):
            offset_y+=move
        elif (error_y < -tolerance):
            offset_y-=move
        
        #watch out for movement limitations
        if (offset_y + 30) < 0: offset_y+=move  
        if (offset_x + 90) < 0: offset_x+=move
        if (offset_y + 30) > 180: offset_y-=move
        if (offset_x + 90) > 180: offset_x-=move
        
        kit.servo[0].angle = 90 + offset_x  #pan
        kit.servo[1].angle = 30 + offset_y  #tilt

        if(c==1):
            frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),6)
 
    cv2.imshow('frame',frame) #display image
    
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == 27:    #press esc key to quit
        break
 
cv2.destroyAllWindows() 

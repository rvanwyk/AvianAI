#!/usr/bin/python3
import cv2
import numpy as np
from picamera2 import Picamera2, MappedArray
import time

# Grab images as numpy arrays and leave everything else to OpenCV.

cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

tmpAvg = 0
alpha = 0.95
frame_count = 0
fps = 30
frame_size = (640, 480)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None

while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # tmpAvg = tmpAvg*alpha + (1-alpha)*np.average(im) 

    newAvg = np.average(im) 
    print(newAvg)

    if abs(newAvg - tmpAvg) > 10:
        print("Motion detected!")
        if out is not None:
            out.release()
        
        out = cv2.VideoWriter('motion_detected_%d.mp4' % frame_count, fourcc, fps, frame_size)
    
    if out is not None:
        out.write(im)
        frame_count += 1
    
    tmpAvg = newAvg

    cv2.imshow("Camera", im)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()



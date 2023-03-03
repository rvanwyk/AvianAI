#!/usr/bin/python3
import cv2
import numpy as np
from picamera2 import Picamera2, MappedArray
import time
import os

# Create directory to save images if it doesn't already exist
if not os.path.exists("motion_images"):
    os.mkdir("motion_images")

# Grab images as numpy arrays and leave everything else to OpenCV.

cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

tmpAvg = 0
alpha = 0.95
frame_count = 0
frame_size = (640, 480)

while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    newAvg = np.average(im) 
    print(newAvg)

    if abs(newAvg - tmpAvg) > 5:
        print("Motion detected!")
        filename = os.path.join("motion_images", f"motion_detected_{frame_count}.jpg")
        cv2.imwrite(filename, im)
        frame_count += 1

    tmpAvg = newAvg

    cv2.imshow("Camera", im)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()


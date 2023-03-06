#!/usr/bin/python3
import cv2
import numpy as np
from picamera2 import Picamera2, MappedArray
import time
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Initialize Google Cloud Storage client
client = storage.Client()


# Get the bucket object
bucket_name = 'avian_motion'
bucket = client.bucket(bucket_name)


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


while True:
    im = picam2.capture_array()


    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # tmpAvg = tmpAvg*alpha + (1-alpha)*np.average(im) 


    newAvg = np.average(im) 
    print(newAvg)


    if abs(newAvg - tmpAvg) > 10:
        print("Motion detected!")
        
        # Save the image to a file
        filename = 'motion_detected_%d.jpg' % time.time()
        cv2.imwrite(filename, im)
        
        # Upload the image file to the bucket
        blob = bucket.blob('motion_images/%s' % filename)
        blob.upload_from_filename(filename)
        
        frame_count += 1
    
    tmpAvg = newAvg


    cv2.imshow("Camera", im)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


picam2.stop()
cv2.destroyAllWindows()

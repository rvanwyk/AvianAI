#!/usr/bin/python3
import cv2
import numpy as np
from picamera2 import Picamera2, MappedArray, Preview
import time
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Initialize Google Cloud Storage client
client = storage.Client()


# Get the bucket object
bucket_name = "avian_motion"
bucket = client.bucket(bucket_name)


# Grab images as numpy arrays and leave everything else to OpenCV.


cv2.startWindowThread()


picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
picam2.configure(
    picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (1080, 760)})
)
picam2.start()


tmpAvg = np.average(picam2.capture_array())
alpha = 0.95
frame_count = 0
fps = 30
frame_size = (1080, 760)

LOCK = False
vid = 0
fourcc = cv2.VideoWriter_fourcc(*"XVID")
video_writer = cv2.VideoWriter("output.avi", fourcc, 20.0, (1080, 760))
a = open("test.txt", "w")

img_arr = np.array([])
tmp_arr = np.array([])

buffer = []
RECORD = False

for i in range(10):
    im = picam2.capture_array()
    im = im[:, :, 0:3]
    buffer.append(im)
iter = 0
while True:
    im = picam2.capture_array()
    im = im[:, :, 0:3]
    buffer.append(im)
    buffer.pop(0)

    tmpAvg = tmpAvg * alpha + (1 - alpha) * np.average(im)

    newAvg = np.average(im)
    print(newAvg)
    
    if abs(newAvg - tmpAvg) > 5:
        print("********************* MOTION *********************")
        RECORD = True
        for i in buffer:
            video_writer.write(i)
        buffer = []
    if RECORD and iter < 100:
        video_writer.write(im)
        iter = iter + 1
        
    if iter >= 100:
        RECORD = False
        iter = 0
        # filename = 'motion_detected_%d.jpg' % time.time()
        # blob = bucket.blob('motion_videos/%s' % filename)
        blob = bucket.blob("output.avi")
        blob.upload_from_filename("motion_videos/output.avi")
        print("********************* COMPLETE *********************")
    tmpAvg = newAvg





import cv2
import numpy as np

img=[]
for i in range(0,5):
    img.append(cv2.imread(str(i)+'.png'))

height,width,layers=img[1].shape

video=cv2.VideoWriter('video.avi',-1,1,(width,height))

for j in range(0,5):
  video.write(img[j])

cv2.destroyAllWindows()
video.release()
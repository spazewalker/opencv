#!/usr/bin/env python3

import cv2
import random
import numpy as np

low = (90,100,150)
upp = (180,255,255)

err_shape = 5
precision = 3
P_def = 88*2 #cm #Diameter of ball in image
d_def = 20 #cm #Distance of ball for callibration
l_def = 5 #cm #Actual Diameter of ball
f = P_def * d_def / l_def
font_color = (255,255,255)

def calculate_dist(frame,rect,radius):
    #calculate P'
    #configure F L P AND D
    #distance = f*L/P'
    P = 2 * radius #diameter of ball in image
    distance = f * l_def / P
    distance = (int)(10**precision * distance)
    distance = 'distance: ' +str((float)(distance/10**precision)) + " cm"
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame,distance,((int)(rect[0]-150),(int)(rect[1]-rect[3]/2)),font,0.75,font_color)
    return frame




source_window = 'source'
cv2.namedWindow(source_window)

camera = cv2.VideoCapture(0)

grabbed = True

sum_time_count=0
n=0
color = (random.randint(0,256), random.randint(0,256), random.randint(0,256))
while grabbed:

    e1 = cv2.getTickCount()
    (grabbed, frame) = camera.read()

    src_gray = cv2.blur(frame, (7,7))
    src_gray = cv2.cvtColor(src_gray, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(src_gray,low,upp)
    mask = cv2.dilate(mask,(3,3),iterations=2)
    cnts = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    hull_list = []
    for i in range(len(cnts)):
        hull = cv2.convexHull(cnts[i])
        hull_list.append(hull)

    x,y,w,h = 0,0,0,0
    for i in range(len(cnts)):
        area = cv2.contourArea(hull_list[i])
        x,y,w,h = cv2.boundingRect(hull_list[i])
        r_eq = np.sqrt(area/np.pi)
        req = (w+h)/4
        if abs(req-r_eq)<err_shape and abs(w/2 - r_eq) < err_shape and abs(h/2 - r_eq) < err_shape:
            (x,y),radius = cv2.minEnclosingCircle(hull_list[i])
            center = (int(x),int(y))
            radius = int(radius)
            if radius>20:
                frame = cv2.circle(frame,center,radius,color,2)
                frame = calculate_dist(frame,(x,y,w,h),radius)
    # cv2.imshow('mask',mask)
    # frame = calculate_dist(frame,(x,y,w,h))
    
    cv2.imshow(source_window,frame)



    e2 = cv2.getTickCount()
    t=(e2-e1)/cv2.getTickFrequency()
    sum_time_count += t
    n=n+1
    print("frame time: ",t," avg time: ",sum_time_count/n," total frames: ",n," python ")
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        grabbed = False

camera.release()
cv2.destroyAllWindows()
#!/usr/bin/env python3

import cv2
import numpy as np

low = (151,40,0)
upp = (255,255,135)
err_shape = 5


# def draw(val):
#     hlow = cv2.getTrackbarPos('hlow','image')
#     slow = cv2.getTrackbarPos('slow','image')
#     vlow = cv2.getTrackbarPos('vlow','image')
#     hupp = cv2.getTrackbarPos('hupp','image')
#     supp = cv2.getTrackbarPos('supp','image')
#     vupp = cv2.getTrackbarPos('vupp','image')
#     low = (hlow,slow,vlow)
#     upp = (hupp,supp,vupp)
#     mask = cv2.inRange(image,low,upp)
#     mask = cv2.dilate(mask,(3,3),iterations=2)
#     cv2.imshow('mask',mask)



image = cv2.imread('test.jpg')
# cv2.namedWindow('image')
# cv2.createTrackbar('hlow','image',0,255,draw)
# cv2.createTrackbar('slow','image',0,255,draw)
# cv2.createTrackbar('vlow','image',0,255,draw)
# cv2.createTrackbar('hupp','image',0,255,draw)
# cv2.createTrackbar('supp','image',0,255,draw)
# cv2.createTrackbar('vupp','image',0,255,draw)


mask = cv2.inRange(image,low,upp)
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
        cv2.drawContours(image,hull_list[i],i,(255,0,0),thickness=2)
        center = (int(x),int(y))
        radius = int(radius)
        print(radius)
        if radius>20:
            image = cv2.circle(image,center,radius,(255,0,0),2)
            cv2.imshow('mask',mask)
            cv2.imshow('image',image)


cv2.waitKey()
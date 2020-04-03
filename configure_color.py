import cv2 as cv
import numpy as np

px_hsv = []

min_h = 10
min_s = 10
min_v = 10
max_h = 10
max_s = 10
max_v = 10

def nothing(_):
    pass

def mouse(event,x,y,flags,param):
    global px_hsv, min_h, min_s, min_v, max_h, max_s, max_v
    if event == cv.EVENT_MOUSEMOVE:
        px = frame[x,y]
        px_array = np.uint8([[px]])
        px_hsv = cv.cvtColor(px_array,cv.COLOR_BGR2HSV)
    elif event == cv.EVENT_LBUTTONDBLCLK:
        px = frame[x,y]
        px_array = np.uint8([[px]])
        px_hsv = cv.cvtColor(px_array,cv.COLOR_BGR2HSV)

        min_h = (px_hsv[0][0][0]-20 if px_hsv[0][0][0]-20 > 0 else 0)
        min_s = (px_hsv[0][0][1]-40 if px_hsv[0][0][1]-20 > 0 else 0)
        min_v = (px_hsv[0][0][2]-40 if px_hsv[0][0][2]-20 > 0 else 0)
        max_h = (px_hsv[0][0][0]+20 if px_hsv[0][0][0]+20 < 180 else 180)
        max_s = (px_hsv[0][0][1]+20 if px_hsv[0][0][1]+20 < 255 else 255)
        max_v = (px_hsv[0][0][2]+40 if px_hsv[0][0][2]+20 < 255 else 255)

cap = cv.VideoCapture(0)

cv.namedWindow('video')
cv.setMouseCallback("video",mouse)

while True:
    _, frame = cap.read()

    src_gray = cv.blur(frame, (7,7))
    src_gray = cv.cvtColor(src_gray, cv.COLOR_BGR2HSV)
    
    

    cv.createTrackbar("H1", "video", min_h, 180, nothing)
    cv.createTrackbar("S1", "video", min_s, 255, nothing)
    cv.createTrackbar("V1", "video", min_v, 255, nothing)
    cv.createTrackbar("H2", "video", max_h, 180, nothing)
    cv.createTrackbar("S2", "video", max_s, 255, nothing)
    cv.createTrackbar("V2", "video", max_v, 255, nothing)

    h1 = cv.getTrackbarPos('H1', 'video')
    s1 = cv.getTrackbarPos('S1', 'video')
    v1 = cv.getTrackbarPos('V1', 'video')
    h2 = cv.getTrackbarPos('H2', 'video')
    s2 = cv.getTrackbarPos('S2', 'video')
    v2 = cv.getTrackbarPos('V2', 'video')

    lower = np.array([h1,s1,v1])
    upper = np.array([h2,s2,v2])

    mask = cv.inRange(src_gray,lower,upper)
    mask = cv.dilate(mask,(3,3),iterations=2)

    pixel_hsv = " ".join(str(values) for values in px_hsv)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(frame, "px HSV: "+pixel_hsv, (10, 260),
               font, 1, (255, 255, 255), 1, cv.LINE_AA)

    cv.imshow('video',frame)
    cv.imshow('mask',mask)

    key = cv.waitKey(5) & 0xFF
    if key == 27:
        break
cv.destroyAllWindows()
import numpy as np
import cv2

greenLower = (80, 100, 20)
greenUpper = (100, 255, 255)


camera = cv2.VideoCapture(0)

grabbed = True

sum_time_count=0
n=0

while grabbed:

    e1 = cv2.getTickCount()
    (grabbed, frame) = camera.read()

    mask = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(mask, greenLower, greenUpper)
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)


    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

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
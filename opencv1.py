import numpy as np
import cv2

greenLower = (80, 100, 20)
greenUpper = (100, 255, 255)

camera = cv2.VideoCapture(0)

grabbed = True

while grabbed:
    (grabbed, frame) = camera.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, (3,3), iterations=2)
    mask = cv2.dilate(mask, (3,3), iterations=2)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cv2.drawContours(frame,cnts,-1,(255,255,0),2)

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        grabbed = False

camera.release()
cv2.destroyAllWindows()
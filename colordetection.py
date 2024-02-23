import cv2
import numpy as np
import time
import math

cn = "http://192.168.0.3:4747/video"
cap = cv2.VideoCapture(cn)

def empty(a):
    pass

# if needed
cv2.namedWindow('para')
cv2.resizeWindow('para', 640, 240)
cv2.createTrackbar('t1', 'para', 48, 255, empty)
cv2.createTrackbar('t2', 'para', 30, 255, empty)

def detect_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hg = np.array([90, 255, 255])
    lg = np.array([50, 100, 100])
    hr = np.array([4, 255, 255])
    lr = np.array([1, 100, 100])

    mask_green = cv2.inRange(hsv, lg, hg)
    mask_red = cv2.inRange(hsv, lr, hr)

    return mask_green, mask_red

# Define and implement the detect_objects function if needed

while True:
    start = time.time()
    ret, frame = cap.read()
    end = time.time()
    #fps = math.ceil(1 / (end - start))

    ic = frame.copy()

    mask_green, mask_red = detect_color(frame)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_green:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(ic, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(ic, 'Green', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(ic, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(ic, 'Red', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display FPS on the frame
    #cv2.putText(ic, 'FPS: ' + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Frame', ic)

    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

cap.release()
cv2.destroyAllWindows()


# -*- coding: utf-8 -*-
"""visionsport.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13NPEN0oLkkBT-BKigbuxuAYwiyHlyUn1
"""

import pandas as pd
import cv2 as cv
import numpy as np

vidcap = cv.VideoCapture(0)     #acces to camera
while True:
  ret,frame = vidcap.read()
  cv.imshow('frame',frame)
  if cv.waitKey(1) & 0xFF == ord('q'):
    break
vidcap.release()
cv.destroyAllWindows()

vidcap = cv.VideoCapture(0)                             # open
while True:

    ret,frame = vidcap.read()                           #read
    if not ret:
        break
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)             #convert to gray
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)          #gray to blur with intensity 17,17

    cv.imshow('blurFrame',blurFrame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
vidcap.release()
cv.destroyAllWindows()

vidcap = cv.VideoCapture(0)
prevCircle = None

# Define a function to calculate squared distance
dist = lambda x1, y1, x2, y2: (x1 - x2) ** 2 + (y1 - y2) ** 2

while True:
    ret, frame = vidcap.read()
    if not ret:
        break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)

    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=35, minRadius=60, maxRadius=300)            #circle parameter
                                                         #clrcle, mindistcentre ,sensitivitydetection, accuracycircledetection,
    if circles is not None:
        circles = np.uint16(np.around(circles))

        chosen = None
        for circle in circles[0,:]:
            if chosen is None:
                chosen = circle
            elif prevCircle is not None:
                dist_chosen = dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1])
                dist_circle = dist(circle[0], circle[1], prevCircle[0], prevCircle[1])

                if dist_circle <= dist_chosen:
                    chosen = circle

        cv.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)                   #making circle around object
        cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)
        prevCircle = chosen

    cv.imshow("circles", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vidcap.release()
cv.destroyAllWindows()

#trying to capture movment of ball in video

vid_path = r"C:\Users\vishal\Downloads\videocrick.mp4"
vidcap = cv.VideoCapture(vid_path)
if not vidcap.isOpened():
    print("Error: Could not open video.")
else:
    while True:
        ret, frame = vidcap.read()

        if ret:
            cv.imshow('Video', frame)

            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    vidcap.release()
    cv.destroyAllWindows()

vid_path = r"C:\Users\vishal\Downloads\videocrick.mp4"
vidcap = cv.VideoCapture(vid_path)

if not vidcap.isOpened():
    print("Error: Could not open video.")
else:
    def detect_small_objects(frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)


        lower_color = np.array([0, 0, 120])
        upper_color = np.array([180, 50, 255])
        mask = cv.inRange(hsv, lower_color, upper_color)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        min_area = 20
        max_area = 100
        for contour in contours:
            area = cv.contourArea(contour)
            if min_area < area < max_area:

                M = cv.moments(contour)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    radius = int(np.sqrt(area / np.pi))

                    cv.circle(frame, (cx, cy), radius, (0, 255, 0), 2)

        return frame

    while vidcap.isOpened():
        ret, frame = vidcap.read()
        if not ret:
            break

        processed_frame = detect_small_objects(frame)

        cv.imshow('Small Object Detection', processed_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    vidcap.release()
    cv.destroyAllWindows()


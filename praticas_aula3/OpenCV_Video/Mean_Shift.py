#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
# "numpy",
# "opencv-python",
# "matplotlib",
# ]
# ///


import cv2
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt


cap = cv2.VideoCapture(0)
ret, frame = cap.read()
# Setup initial location of window
# Using more reasonable defaults (centering a small window)
height, width = frame.shape[:2]
c, r, w, h = width//2 - 30, height//2 - 30, 60, 60
track_window = (c, r, w, h)
# Set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
# Mask out low light and very low saturation points
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
# Setup the termination criteria, either 10 iteration or move by at least 1 pt
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)



while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    # Apply MeanShift to get the new location
    ret_iter, track_window = cv2.meanShift(dst, track_window, term_crit)
    # Draw it on image
    x, y, w, h = track_window
    img2 = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('MeanShift Tracking', img2)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # ESC
        break
cap.release()
cv2.destroyAllWindows()
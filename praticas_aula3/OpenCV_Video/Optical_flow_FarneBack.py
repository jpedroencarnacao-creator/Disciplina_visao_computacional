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


def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (128, 128, 128), -1)
    return vis


#########################MAIN####################################
cam = cv2.VideoCapture(0)
# Check if camera opened successfully
if (cam.isOpened() == False):
    print("Unable to read camera feed")
    exit(1) # exit with problem; exit (0) - exit ok
ret, prev = cam.read()
prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    prevgray = gray

    cv2.imshow('flow', draw_flow(gray, flow))
    
    ch = cv2.waitKey(5)
    if ch == 27:
        break
cv2.destroyAllWindows()
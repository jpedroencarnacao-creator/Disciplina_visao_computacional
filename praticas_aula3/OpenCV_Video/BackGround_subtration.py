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
# Check if camera opened successfully
if not cap.isOpened():
    print("Unable to read camera feed")
    exit(1)
# Create Background Subtractor object
fgbg = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=200, detectShadows=False)
print("Starting Background Subtraction. Press 'ESC' to exit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Apply background subtraction to get foreground mask
    fgmask = fgbg.apply(frame)
    # Convert mask to 3 channels so it can be stacked with the color frame
    fgmask_rgb = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
    # Horizontally stack original frame and mask
    res = np.hstack((frame, fgmask_rgb))
    cv2.imshow('Background Subtraction (Left: Original, Right: Mask)', res)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # ESC
        break

cap.release()
cv2.destroyAllWindows()



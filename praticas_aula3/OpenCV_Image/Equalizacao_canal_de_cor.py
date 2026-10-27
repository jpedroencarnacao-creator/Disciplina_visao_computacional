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

pasta = Path(r"C:\Users\jpedr\Documents\Visao_computacional\Imagens_OpenCV\Imagens")
img1_path = pasta / "exemplo.JPG"

img = cv2.imread(str(img1_path))
# Convert to HSV
imhsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# Perform histogram equalization only on the V channel
imhsv[:,:,2] = cv2.equalizeHist(imhsv[:,:,2])
# Convert back to BGR format
imEq = cv2.cvtColor(imhsv, cv2.COLOR_HSV2BGR)
cv2.namedWindow("imeq", cv2.WINDOW_NORMAL)
cv2.resizeWindow("imeq", 800, 600) 
cv2.imshow("imeq",imEq)
cv2.waitKey()

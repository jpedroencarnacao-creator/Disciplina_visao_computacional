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
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv2.namedWindow("dst", cv2.WINDOW_NORMAL)
cv2.resizeWindow("dst", 800, 600) 
cv2.imshow('dst',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
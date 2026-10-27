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
Z = img.reshape((-1,3))#Mx3 size (M is number of pixels in image), 3 = R,G,B
# convert to np.float32
Z = np.float32(Z)
# define criteria, number of clusters(K) and apply kmeans()
# iteration termination criteria. When this criteria is satisfied, algorithm iteration stops.
#Actually, it should be a tuple of 3 parameters.
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 8 # images show k={2,4,8}
ret,label,center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))
cv2.namedWindow("Segmentation", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Segmentation", 800, 600) 
cv2.imshow('Segmentation',res2)
cv2.waitKey(0)
cv2.destroyAllWindows() 
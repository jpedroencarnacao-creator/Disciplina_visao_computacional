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
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#calculating the histogram
hist = cv2.calcHist(imgray,[0],None,[256],[0,256])
#Ploting the histogram
plt.hist(imgray.ravel(),256,[0,256]);
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
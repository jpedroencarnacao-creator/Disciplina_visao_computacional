#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
# "numpy",
# "opencv-contrib-python",
# "matplotlib",
# ]
# ///

import cv2
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt

pasta = Path(r"C:\Users\jpedr\Documents\Visao_computacional\Imagens_OpenCV\Imagens")
img1_path = pasta / "exemplo.JPG"


# Read image
img = cv2.imread(str(img1_path))
# Initialize Saliency detector (Spectral Residual)
# Requires opencv-contrib-python
saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
# Compute Saliency Map
success, saliencyMap = saliency.computeSaliency(img)
if success:
    # Normalize to 0-255 range and convert to uint8 for visualization
    saliencyMap = (saliencyMap * 255).astype("uint8")
    # Apply a colormap (Jet is common for heatmaps)
    saliencyMapColor = cv2.applyColorMap(saliencyMap, cv2.COLORMAP_JET)
    # Display results
    cv2.namedWindow("Saliency Map (Gray)", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Saliency Map (Gray)", 800, 600) 
    cv2.imshow("Saliency Map (Gray)", saliencyMap)
    res = np.hstack((img, saliencyMapColor))
    cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Result", 800, 600) 
    cv2.imshow("Result", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: Failed to compute saliency map.")
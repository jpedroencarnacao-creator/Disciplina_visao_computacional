#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
# "numpy",
# "opencv-python",
# ]
# ///

import cv2
import numpy as np
from pathlib import Path

pasta = Path(r"C:\Users\jpedr\Documents\Visao_computacional\Imagens_OpenCV\Imagens")
img1_path = pasta / "exemplo.JPG"


Max_edge = 100;
Min_edge = 50;
apertureSize = 7;
img = cv2.imread(str(img1_path),cv2.IMREAD_GRAYSCALE)
height, width = img.shape[:2]
edges = cv2.Canny(img,Min_edge,Max_edge, apertureSize)

#canny -> location , Min detection Value , Max detection Value , apertureSize , L2gradient
# Baixar os valores de Max e Min (ex: 50, 100) dá mais bordas e mais detalhe, mas também mais ruído.
# Subir os valores (ex: 150, 300) deixa só as bordas mais marcadas
# apertureSize ->tamanho do filtro Sobel usado no gradiente (3, 5 ou 7). Maior apanha bordas mais suaves.
# L2gradient -> calcula o gradiente de forma mais precisa, um pouco mais lento.

cv2.namedWindow("Orig", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Orig", 800, 600) 
cv2.imshow('Orig',img)

cv2.namedWindow("Edges", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Edges", 800, 600) 
cv2.imshow('Edges',edges)
cv2.waitKey(0)
#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
# "numpy",
# "opencv-python",
# ]
# ///

import cv2
from pathlib import Path
import numpy as np

pasta = Path(r"C:\Users\JP\Documents\Visao_computacional\Imagens_OpenCV\Aula_2")
img1_path = pasta / "Imagem_modelo.jpg"

img = cv2.imread(str(img1_path),cv2.IMREAD_GRAYSCALE)


height, width = img.shape[:2]
thresh = 127
maxval = 255

ret,thresh1 = cv2.threshold(img,thresh,maxval,cv2.THRESH_BINARY)

#src	-> img	                ->imagem de entrada, em cinzento
#thresh	-> 127	                ->o limiar: o valor que separa os dois grupos
#maxval	-> 255	                ->o valor atribuído aos píxeis "acima" (nos tipos BINARY)
#type	-> cv2.THRESH_BINARY	->a regra a aplicar (há 5 tipos, ver abaixo)

#       outras regras que se pode aplicar: cv2.THRESH_BINARY; cv2.THRESH_BINARY_INV; cv2.THRESH_TRUNC; cv2.THRESH_TOZERO; cv2.THRESH_TOZERO_INV
#
# THRESH_BINARY -> os píxeis acima do limiar ficam brancos; os restantes ficam pretos
#   dst(x,y) = maxval     se src(x,y) > thresh
#              0          caso contrário
#
# THRESH_BINARY_INV -> o inverso do anterior; os píxeis acima do limiar ficam pretos e os restantes brancos.
#   dst(x,y) = 0          se src(x,y) > thresh
#              maxval     caso contrário
#
# THRESH_TRUNC -> os píxeis acima do limiar são reduzidos ao valor do limiar; os restantes ficam iguais.
#   dst(x,y) = thresh     se src(x,y) > thresh
#              src(x,y)   caso contrário
#
# THRESH_TOZERO -> os píxeis acima do limiar mantêm o valor original; os restantes ficam pretos.
#   dst(x,y) = src(x,y)   se src(x,y) > thresh
#              0          caso contrário
#
# THRESH_TOZERO_INV -> os píxeis acima do limiar ficam pretos; os restantes mantêm o valor original.
#   dst(x,y) = 0          se src(x,y) > thresh
#              src(x,y)   caso contrário


cv2.namedWindow("threshold", cv2.WINDOW_NORMAL)
cv2.resizeWindow("threshold", 800, 600) 
cv2.imshow("threshold", thresh1)
cv2.waitKey(0)
cv2.destroyAllWindows()
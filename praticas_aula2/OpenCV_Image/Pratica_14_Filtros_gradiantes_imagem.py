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

imgaux = cv2.imread(str(img1_path),cv2.IMREAD_GRAYSCALE)
#Deteção de arestas (contornos) numa imagem
height, width = imgaux.shape[:2]
cv2.namedWindow("Orig", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Orig", 800, 600) 
cv2.imshow('Orig',imgaux)


#gradient computation in x and in y

# Os argumentos do Sobel são:

# Argumento	    Valor	            Significado
# src	        imgaux	         imagem de entrada
# ddepth	   cv2.CV_64F	tipo da saída: decimais de 64 bits
# dx	        1 ou 0	        ordem da derivada em x
# dy	        0 ou 1	        ordem da derivada em y
# ksize	           5        tamanho do kernel (1, 3, 5 ou 7)


sobelx = cv2.Sobel(imgaux,cv2.CV_64F,1,0,ksize=5)# 1,0 = dx     #função que permite calcular a primeira derivada, a taxa de variação da intensidade
sobely = cv2.Sobel(imgaux,cv2.CV_64F,0,1,ksize=5)# 0,1 = dy
#gradient module and normalization for visualization
module = cv2.sqrt(sobelx**2 + sobely**2)        # -> Combina as duas direções numa só medida, a magnitude: magnitude = √(gx² + gy²)
module = cv2.normalize(module, None, 0, 1, cv2.NORM_MINMAX)
#laplacian computation
laplacian = cv2.Laplacian(imgaux,cv2.CV_64F)    #função que permite calcular a segunda derivada, a variação da variação

cv2.namedWindow("SobelX", cv2.WINDOW_NORMAL)
cv2.resizeWindow("SobelX", 800, 600) 
cv2.imshow('SobelX',sobelx)

cv2.namedWindow("SobelY", cv2.WINDOW_NORMAL)
cv2.resizeWindow("SobelY", 800, 600) 
cv2.imshow('SobelY',sobely)

cv2.namedWindow("Module", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Module", 800, 600) 
cv2.imshow('Module',module)

cv2.namedWindow("Laplacian", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Laplacian", 800, 600) 
cv2.imshow('Laplacian',laplacian)
cv2.waitKey(0)
cv2.destroyAllWindows()

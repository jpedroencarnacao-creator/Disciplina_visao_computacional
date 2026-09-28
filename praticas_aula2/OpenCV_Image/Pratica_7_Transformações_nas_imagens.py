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
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np


pasta = Path(r"C:\Users\JP\Documents\Visao_computacional\Imagens_OpenCV\Aula_2")
img_path = pasta / "Imagem_modelo.jpg"

img = cv2.imread(str(img_path))


# Redimensionamento da imagem (Scaling) -> cv2.resize()
""" 


dst = cv2.resize( src, dsize[, dst[, fx[, fy[,
interpolation]]]] )
Parameters
•src - input image
•dst - output resized image
•dsize - output image size
•fx - fator escalar ao longo do eixo horizontal
•fy - fator escalar ao longo do eixo vertical; 
ou dsize ou ambos fx e fy devem ser diferentes de zero.

•interpolation - método de interpolação ( Bilinear /Bicubic etc )
O metodo Bilinear:
Usa os 4 píxeis vizinhos mais próximos (um quadrado 2×2), onde faz uma média desses pixeis; 
quanto mais perto está o vizinho, mais o valor dele conta.
A transição entre os vizinhos é linear (em linha reta).
É um processo rápido e dá um bons resultados, contudo as imagens ficam um pouco desfocadas, sobretudo quando se aumenta muito a imagem.

O metodo Bicubic:
Usa 16 píxeis vizinhos (um quadrado 4×4).
Usa uma curva (polinómio cúbico) em vez de uma reta, o que dá transições mais suaves, gerando imagens  mais nítidas e as bordas bem mais definidas.
Contudo é mais lento, pois tem 4× mais pixeis vizinhos para calcular.

Scaling: Metodos de interpolação preferiveis para scaling
cv2.INTER_AREA for shrinking and
cv2.INTER_CUBIC (slow) &
cv2.INTER_LINEAR for zooming.
By default, interpolation method used is
cv2.INTER_LINEAR for all resizing purposes.

"""

res1 = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
#OR

height, width = img.shape[:2]
#rows,cols,channels = img2.shape
res2 = cv2.resize(img,(2*width,2*height), interpolation = cv2.INTER_CUBIC)

res3 = cv2.resize(img,(int(width/5),3*height), interpolation = cv2.INTER_AREA)

cv2.namedWindow("Orig_Img", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Orig_Img", 800, 600) 
cv2.imshow('Orig_Img',img)

cv2.namedWindow("Res1", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Res1", 800, 600) 
cv2.imshow('Res1',res1)

cv2.namedWindow("Res2", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Res2", 800, 600) 
cv2.imshow('Res2',res2)

cv2.namedWindow("Res3", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Res3", 800, 600) 
cv2.imshow('Res3',res3)
cv2.waitKey(0)
cv2.destroyAllWindows()


# translação da imagem (Translation) -> cv2.warpAffine()

rows,cols = img.shape[:2] #rows,cols,channels = img2.shape
M = np.float32([[1,0,500],[0,1,250]])
dst = cv2.warpAffine(img,M,(cols,rows))

cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.resizeWindow("img", 800, 600) 
cv2.imshow('img',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()


# rotação da imagem (Rotation) -> cv2.getRotationMatrix2D() + cv2.warpAffine()

rows,cols = img.shape[:2]
#cv2.getRotationMatrix2D(center, angle, scale)
#Example #1
Mrot2 = cv2.getRotationMatrix2D((0,0),45,0.5)
dst2 = cv2.warpAffine(img,Mrot2,(cols,rows))
#Example #2
Mrot = cv2.getRotationMatrix2D((cols/2,rows/2),45,0.5)
dst = cv2.warpAffine(img,Mrot,(cols,rows))

cv2.namedWindow("Dst", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Dst", 800, 600) 
cv2.imshow('Dst',dst)

cv2.namedWindow("Dst2", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Dst2", 800, 600) 
cv2.imshow('Dst2',dst2)
cv2.waitKey(0)
cv2.destroyAllWindows()

#transformada da perspectiva (Perspective Transform) -> cv2.getPerspectiveTransform() + cv2.warpPerspective()

rows,cols,ch = img.shape
print("rows = ",rows)
print("cols = ",cols)
pts1 = np.float32([[0,0],[cols,0],[0,rows],[cols,rows]])  #posições dos 4 pontos da imagem original
#         [superior esquerdo, superior direito, inferior esquerdo, inferior direito]

pts2 = np.float32([[556, 1256],[2048 , 1000],[834, 2294],[1947, 3500]])    #posições dos 4 pontos da imagem transformada
M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M,(cols,rows))

cv2.namedWindow("Ori", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Ori", 800, 600) 
cv2.imshow('Ori',img)

cv2.namedWindow("Tansf", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Tansf", 800, 600) 
cv2.imshow('Tansf',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
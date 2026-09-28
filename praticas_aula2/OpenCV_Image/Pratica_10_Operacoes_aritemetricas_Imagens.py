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
img2_path = pasta / "Imagem_modelo2.jpg"

img1 = cv2.imread(str(img1_path))
img2 = cv2.imread(str(img2_path))


#   Operação "ADD" soma de duas imagens 

# Fórmula (slide 55): dst = alpha * img1 + beta * img2 + gamma
#   alpha -> peso da img1 (Lenna)
#   beta  -> peso da img2 (rapariga), aqui beta = 1 - alpha
#   gamma -> valor somado a todos os píxeis (brilho extra), aqui 0
#   O resultado é limitado a 0-255 (saturação)

alpha = 0.45
dst = cv2.addWeighted(img1, alpha, img2, (1 - alpha), 0)

cv2.namedWindow("dst", cv2.WINDOW_NORMAL)
cv2.resizeWindow("dst", 800, 600) 
cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()


#   Operação "Bitwise" - ADD (AND) - AND bit a bit entre duas imagens

pasta = Path(r"C:\Users\JP\Documents\Visao_computacional\Imagens_OpenCV\Aula_2")
img3_path = pasta / "Imagem_modelo3.jpg"
img4_path = pasta / "Imagem_modelo4.jpg"

img3 = cv2.imread(str(img3_path))
img4 = cv2.imread(str(img4_path))

# cv2.bitwise_and is applied over the
# image inputs with applied parameters
dest_and = cv2.bitwise_and(img3, img4, mask = None)
# the window showing output image
# with the Bitwise AND operation
# on the input images
cv2.namedWindow("Bitwise And", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Bitwise And", 800, 600) 
cv2.imshow('Bitwise And', dest_and)
# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()




#   Operação "Bitwise" - or (OR) - OR bit a bit entre duas imagens


# cv2.bitwise_or is applied over the
# image inputs with applied parameters
dest_or = cv2.bitwise_or(img3, img4, mask = None)
# the window showing output image
# with the Bitwise OR operation
# on the input images
cv2.namedWindow("Bitwise OR", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Bitwise OR", 800, 600) 
cv2.imshow('Bitwise OR', dest_or)
# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
 cv2.destroyAllWindows() 


#   Operação "Bitwise" - or (XOR) - OR bit a bit entre duas imagens

 # cv2.bitwise_xor is applied over the
# image inputs with applied parameters
dest_xor = cv2.bitwise_xor(img3, img4, mask = None)
# the window showing output image
# with the Bitwise XOR operation
# on the input images
cv2.namedWindow("Bitwise XOR", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Bitwise XOR", 800, 600)
cv2.imshow('Bitwise XOR', dest_xor)
# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
 cv2.destroyAllWindows() 


#   Operação "Bitwise" - or (NOT) - OR bit a bit entre duas imagens

 # cv2.bitwise_not is applied over the
# image input with applied parameters
dest_not1 = cv2.bitwise_not(img4, mask = None)
# the windows showing output image
# with the Bitwise NOT operation
cv2.namedWindow("Bitwise NOT on image 1", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Bitwise NOT on image 1", 800, 600)
cv2.imshow('Bitwise NOT on image 1', dest_not1)
# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
 cv2.destroyAllWindows() 
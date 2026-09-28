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

#Em processamento de imagem, um kernel é uma pequena matriz de números (normalmente 3×3 ou 5×5) 
#  que se passa por cima da imagem, píxel a píxel, para calcular uma imagem nova. Os valores do kernel definem o efeito: 
# desfocar, 
# realçar contornos, 
# detetar arestas, 
# etc. 
# Também se chama máscara ou filtro.

#como criar um kernel 5x5 com todos os valores iguais a 1/25 (para desfocar a imagem)
#ddepth=-1, the output image will have the same depth as the source
#CV_8U; CV_16U/CV_16S; CV_32F; CV_64F

# ------------------------------------------------------------------
# Linha 1: criar o kernel
# ------------------------------------------------------------------
# np.ones((5,5), np.float32) cria uma matriz 5x5 com o valor 1 em todas
# as posições. O np.float32 define o tipo dos números: decimais de 32
# bits. O filter2D espera um kernel com números decimais, e o float32 é
# o tipo normal para isso.
# /25 divide cada elemento por 25. Cada posição passa a valer
# 1/25 = 0,04.
#
# O resultado é:
#   0.04  0.04  0.04  0.04  0.04
#   0.04  0.04  0.04  0.04  0.04
#   0.04  0.04  0.04  0.04  0.04
#   0.04  0.04  0.04  0.04  0.04
#   0.04  0.04  0.04  0.04  0.04
#
# Porquê dividir por 25: multiplicar 25 píxeis por 0,04 e somar é o
# mesmo que somá-los e dividir por 25, ou seja, calcular a média. Como
# os 25 pesos somam exatamente 1, o brilho geral da imagem mantém-se.
# Sem a divisão, cada píxel passaria a ser a soma dos 25 vizinhos,
# quase sempre acima de 255, e a imagem ficaria praticamente toda branca.
kernel = np.ones((5,5),np.float32)/25

# ------------------------------------------------------------------
# Linhas 2-3: os comentários sobre o ddepth
# ------------------------------------------------------------------
# A profundidade (depth) é o tipo de dados de cada píxel, ou seja, que
# valores pode guardar. Os tipos listados no comentário são:
#
#   Nome OpenCV | Tipo NumPy | Valores possíveis
#   ------------+------------+------------------------------------------
#   CV_8U       | uint8      | inteiros de 0 a 255 (tipo normal das imagens)
#   CV_16U      | uint16     | inteiros de 0 a 65 535
#   CV_16S      | int16      | inteiros de -32 768 a 32 767 (aceita negativos)
#   CV_32F      | float32    | decimais, positivos e negativos
#   CV_64F      | float64    | decimais com mais precisão
#
# O -1 significa "o mesmo tipo da imagem de entrada". Como a imagem lida
# com imread é uint8 (CV_8U), a saída também é uint8.
#ddepth=-1, the output image will have the same depth as the source
#CV_8U; CV_16U/CV_16S; CV_32F; CV_64F

# ------------------------------------------------------------------
# Linha 4: aplicar o filtro
# ------------------------------------------------------------------
# Os argumentos são:
#   img    -> a imagem de entrada.
#   -1     -> a profundidade da saída (o ddepth dos comentários).
#   kernel -> a matriz criada na primeira linha.
#
# O filter2D passa o kernel por cima de cada píxel, multiplica os 25
# valores por 0,04, soma-os e escreve o resultado em dst. O resultado é
# a imagem desfocada. É exatamente o mesmo que cv2.blur(img, (5, 5)) do
# slide 61; o slide 60 mostra a versão "manual", em que se define o kernel
dst = cv2.filter2D(img,-1,kernel) # -> imagem desfocada

cv2.namedWindow("Orig", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Orig", 800, 600) 
cv2.imshow('Orig',img)

cv2.namedWindow("Res", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Res", 800, 600) 
cv2.imshow('Res',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()



average = cv2.blur(img,(5,5)) # average: NxM mask
gauss = cv2.GaussianBlur(img,(5,5), 2,0) #gaussian: NxM Masc , sigma
median = cv2.medianBlur(img,5) #Medium - specke noise
bilateral = cv2.bilateralFilter(img,9,75,75) #preserves the edges

cv2.namedWindow("Orig", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Orig", 800, 600) 
cv2.imshow('Orig',img)      # -> imagem original

cv2.namedWindow("average", cv2.WINDOW_NORMAL)
cv2.resizeWindow("average", 800, 600) 
cv2.imshow('average',average)   # -> imagem desfocada com média

cv2.namedWindow("gauss", cv2.WINDOW_NORMAL)
cv2.resizeWindow("gauss", 800, 600) 
cv2.imshow('gauss',gauss)       # -> imagem desfocada com gaussiano

cv2.namedWindow("median", cv2.WINDOW_NORMAL)
cv2.resizeWindow("median", 800, 600) 
cv2.imshow('median',median)     # -> imagem desfocada com mediana

cv2.namedWindow("bilateral", cv2.WINDOW_NORMAL)
cv2.resizeWindow("bilateral", 800, 600) 
cv2.imshow('bilateral',bilateral)       # -> imagem desfocada com filtro bilateral (preserva as bordas)
cv2.waitKey(0)
cv2.destroyAllWindows()
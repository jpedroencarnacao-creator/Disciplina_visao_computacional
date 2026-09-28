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

row = 100
col = 100
# alterar a cor do pixel da imagem nas coordenadas (x,y) para verde
for row in range(100, 500):     #aqui iremos alterar a cor de todos os pixeis dentro do espçao de linhaa: [100 -> 500] e coluna: [50 -> 150] para verde
    for col in range(50, 150):
        img[row, col] = [0, 255, 0]  # BGR -> Verde

cv2.namedWindow("teste", cv2.WINDOW_NORMAL)
cv2.resizeWindow("teste", 800, 600)     # redefini a largura e altura, para ser mais facil visualizar a imagem 
cv2.imshow("teste", img)
cv2.waitKey()
cv2.destroyAllWindows()

#ROI -> Region of Interest é selecionar uma região da imagem para trabalhar.
img = cv2.imread(str(img_path),0)   

# segundo argumento do imread diz como ler a imagem.
# 0  -> grayscale   igual a utilizar cv2.IMREAD_GRAYSCALE
# 1  -> color       igual a utilizar cv2.IMREAD_COLOR
# -1 -> unchanged

cv2.namedWindow("ImgOri", cv2.WINDOW_NORMAL) # tenho que continuar a utilizar a criação de janela, 
                                            #pois a minha iamgem é muito grande e não cabe na janela do computador, 
                                            # então tenho que criar uma janela redimensionável
cv2.resizeWindow("ImgOri", 800, 600)     # largura, altura
cv2.imshow('ImgOri',img)
cv2.waitKey()


#old line, column
#RoI = img[50:150, 100:150]
#img[100:200, 400:450] = RoI
# line, column
RoI = img[1000:2000, 500:1300]        # 1000 linhas x 800 colunas
img[2800:3800, 1800:2600] = RoI       # 1000 linhas x 800 colunas


cv2.namedWindow("ImagRoI", cv2.WINDOW_NORMAL)
cv2.resizeWindow("ImagRoI", 800, 600)     # largura, altura
cv2.imshow('ImagRoI',img)
cv2.waitKey()
while (True):
    if cv2.waitKey(1) & 0xFF == 27: #clicar na tecla ESC para sair do programa
        break
cv2.destroyAllWindows()
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

#conversão de cores (BGR) para b&w e de (BGR) para HSV

#HSV (Hue, Saturation, Value) é um metodo de descrever cores:
# H -> Hue (matiz) - representa a cor em si, medida em graus de 0 a 360. Por exemplo, vermelho é 0°, verde é 120° e azul é 240°. (mas no caso do opne cv, só vai de 0 a 179)
# S -> Saturation (saturação) - representa a intensidade da cor, variando de 0 a 100% (0 a 255 no OpenCV). 
# V -> Value (valor) - representa o brilho da cor, variando de 0 a 100% (0 a 255 no OpenCV).

""" 
Serve sobretudo para encontrar objetos pela cor. 
No metodo BGR, o mesmo ponto vermelho tem números muito diferentes na parte iluminada e na parte à sombra, porque os 3 canais mudam todos. 
No HSV, o H quase não muda com a luz: o que muda é o V. Por isso é muito mais fácil separar os objetos apenas pelas cores.
"""

pasta = Path(r"C:\Users\JP\Documents\Visao_computacional\Imagens_OpenCV\Aula_2")
img_path = pasta / "Imagem_modelo.jpg"

img = cv2.imread(str(img_path))  #leitura da imagem a cores, no seguinte path (quando não tem o segundo argumento, a imagem é lida a cores)
                                  # a preto e branco utilizar: cv2.IMREAD_GRAYSCALE
                                  # a cores utilizar: cv2.IMREAD_COLOR

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # converção de cor -> b&w

lin = 100
col = 100

#impressão do pixel da imagem nas coordenadas (x,y) a b&w
px_gray = img_gray[lin, col]
print ('Gray ', px_gray)        #apenas uma versão mais geral da leitura de um pixel na imagem (que foi utilizado no exercicio anterior)


#-----------------------------------------------------
#impressão do pixel da imagem nas coordenadas (x,y) a cores
px = img[lin, col]
print ('BGR ',px)

#-----------------------------------------------------
# leitura apenas do canal de cor azul da imagem nas coordenadas (x,y)
px_blue = img[lin, col, 0] # canal Azul
print ('Blue ',px_blue)

# leitura apenas do canal de cor Verde da imagem nas coordenadas (x,y)
px_green = img[lin, col, 1] # canal Verde
print ('Green ',px_green)

# leitura apenas do canal de cor Vermelho da imagem nas coordenadas (x,y)
px_red = img[lin, col, 2] # canal Vermelho
print ('Red ',px_red)
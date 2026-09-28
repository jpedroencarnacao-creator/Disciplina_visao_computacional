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

testImage = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)  #leitura da imagem a cores, no seguinte path 
                                                    # a preto e branco utilizar: cv2.IMREAD_GRAYSCALE
                                                    # a cores utilizar: cv2.IMREAD_COLOR
print(testImage)

#exemplo do resultado da imagem a b&w 
"""
[[127 129 127 ...  60  62  62]
 [125 129 129 ...  65  64  63]
 [128 130 131 ...  64  64  63]
 ...
 [125 125 127 ... 155 156 157]
 [125 126 127 ... 157 157 158]
 [126 127 127 ... 158 158 158]]

"""
#exemplo do resultado da imagem a cores
"""
[[[148 129 114]
  [150 131 116]
  [146 129 116]
  ...
  [ 79  61  50]
  [ 80  64  52]
  [ 81  64  51]]

 [[146 127 112]
  [150 131 116]
  [148 131 118]
  ...
  [ 84  66  55]
  [ 82  66  54]
  [ 82  65  52]]

 [[149 130 115]
  [149 132 119]
  [150 133 120]
  ...
  [ 83  65  54]
  [ 82  65  56]
  [ 82  64  53]]

 ...

 [[ 77 131 131]
  [ 75 132 131]
  [ 77 134 133]
  ...
  [134 163 148]
  [135 163 150]
  [136 164 151]]

 [[ 77 132 129]
  [ 76 133 132]
  [ 77 134 133]
  ...
  [134 164 151]
  [136 164 151]
  [137 164 154]]

 [[ 78 133 130]
  [ 77 134 131]
  [ 77 134 133]
  ...
  [135 165 152]
  [137 165 152]
  [137 164 154]]]
"""

print("Data type = {}\n".format(testImage.dtype))   #Data type = uint8  [unsigned integer de 8 bits] -> ideifica o tamanho de cada pixel, neste caso 8bits =[0,255] grey rate 
print("Object type = {}\n".format(type(testImage))) #Object type = <class 'numpy.ndarray'>  -> identifica o tipo de variavel/sting
print("Image Dimensions = {}\n".format(testImage.shape))  #comando para visualizar a resuolução da imagem, Image Dimensions = (4288, 2848)
print(testImage[0,0]) # (line, column) # o resultado é o valorde preto entre 0 e 255, no pixel de posição [0,0] neste caso com valor 127



print("teste 1")
testImage[0,2] = 0      #substituição do valor do pixel na posição [0,2] para 0 (preto)
testImage[2,0] = 255    #substituição do valor do pixel na posição [2,0] para 255 (branco)
print(testImage) # (y,x )

cv2.namedWindow("image", cv2.WINDOW_NORMAL) #criação de uma janela 
cv2.imshow("image", testImage)              #gerada a imagem na janela criada
cv2.waitKey(0)                              #comando de espera por uma tecla qualquer
cv2.destroyAllWindows()                     #comando para destruir a janela criada

"""teste 1
[[127 129   0 ...  60  62  62]
 [125 129 129 ...  65  64  63]
 [255 130 131 ...  64  64  63]
 ...
 [125 125 127 ... 155 156 157]
 [125 126 127 ... 157 157 158]
 [126 127 127 ... 158 158 158]]"""

print("teste 2")
testRoI = testImage[0:2, 0:4]       
print(testRoI) # (y,x )             #impressão de apenas um excerto da imagem, 
testImage[0:2, 0:4] = 0             #susbtituição do excerto da imagem por preto (0)
print(testImage) # (y,x )


cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.imshow("image", testImage)
cv2.waitKey(0)
cv2.destroyAllWindows() 

"""teste 2
[[127 129   0 129]
 [125 129 129 129]]     ->  Excerto "testRoI"

[[  0   0   0 ...  60  62  62]
 [  0   0   0 ...  65  64  63]
 [255 130 131 ...  64  64  63]
 ...
 [125 125 127 ... 155 156 157]
 [125 126 127 ... 157 157 158]
 [126 127 127 ... 158 158 158]]"""
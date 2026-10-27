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
img1_path = pasta / "OpenCV_logo.png"


img = cv2.imread(str(img1_path),cv2.IMREAD_GRAYSCALE)
img = cv2.medianBlur(img,5) #é feito um media blur, para desfocar um pouco a imagem, para terira ruidos e inrregularidades (janela 5x5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)


# circles = cv2.HoughCircles(image, method, dp, minDist, param1=..., param2=..., minRadius=..., maxRadius=...)

#method = Algoritmo de detecção -> cv2.HOUGH_GRADIENT (clássico) ou cv2.HOUGH_GRADIENT_ALT (mais preciso, ver abaixo)
#dp = Resolução do acumulador em relação à imagem. 1 = a mesma resolução, 2 = metade -> 1 é mais preciso. 1.5 ou 2 é mais rápido e tolera melhor círculos imperfeitos (os votos ficam mais concentrados)
#minDist = 	Distância mínima entre centros de círculos detetados -> Pequeno demais dá duplicados (o teu primeiro problema). Grande demais perde círculos próximos. Comece pelo tamanho aproximado dos círculos
#param1 = Limiar máximo do Canny interno (o mínimo é automaticamente metade) -> Mais alto dá menos bordas (só as fortes). Mais baixo dá mais bordas e mais ruído
#param2 = Limiar de votos no acumulador: quantos votos um centro precisa para ser aceite -> O mais importante para afinar. Mais baixo deteta mais círculos (incluindo falsos). Mais alto deteta só círculos muito claros
#minRadius = Raio mínimo a procurar (px) -> Útil para ignorar círculos pequenos/ruído
#maxRadius = Raio máximo (px). 0 = sem limite. Negativo = só devolve centros, sem calcular o raio -> Restringir o intervalo melhora velocidade e precisão. Foi o que resolveu os furos vs. anéis

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,30,param1=40,param2=30,minRadius=0,maxRadius=0)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()

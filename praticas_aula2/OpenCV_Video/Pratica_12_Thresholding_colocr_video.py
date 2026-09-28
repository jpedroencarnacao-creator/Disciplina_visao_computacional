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

#cap = cv2.VideoCapture(0) #normalmente 0 é objeto para definir a camera default
ip_address = "192.168.1.81"
# IP (remote) camera
cap = cv2.VideoCapture(f"http://{ip_address}:4747/video")

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")
    exit (1) #exit with problem; exit (0) - exit ok

while(True):
    # Take each frame
    _, frame = cap.read() #neste caso estamos a ignorar o valor de retorno (ret)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([85,50,50])   #valor minimo do azul (H,S,V) -> H=85, S=50, V=50
    upper_blue = np.array([130,255,255])    #valor maximo do azul (H,S,V) -> H=130, S=255, V=255
    
    # é utilizado o HSV porque é mais fácil de definir a cor azul (ou qualquer outra cor) em HSV do que em BGR.
    # passei o valor minimo de 100 para 85, para permitir-me ver certos tons de azul, pois 85 pertence a ciano
    
    #Cor	H (0–179)
    #Vermelho	0–10 e 170–179
    #Laranja	10–25
    #Amarelo	25–35
    #Verde	35–85
    #Ciano	85–100
    #Azul	100–130
    #Roxo / magenta	130–170


    mask = cv2.inRange(hsv, lower_blue, upper_blue)     #função que verifica se os três canais estão dentro do intervalos definidos
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)      #função aritemétrica que aplica a máscara à imagem original (frame), permitindo assim ver realmente apenas a cor azul (ou seja, a cor que está dentro do intervalo definido)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:     #click on ESC to exit
        break
cv2.destroyAllWindows()
cap.close()

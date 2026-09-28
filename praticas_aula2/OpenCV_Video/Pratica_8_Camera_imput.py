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

#cap = cv2.VideoCapture(0) #normalmente 0 é objeto para definir a camera default
ip_address = "192.168.1.81"
# IP (remote) camera
cap = cv2.VideoCapture(f"http://{ip_address}:4747/video")

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")
    exit (1) #sai do programa caso não consiga detetar a camera

frame_width = int(cap.get(3))   #faz a leitura da largura do frame  da camera
frame_height = int(cap.get(4))  #faz a leitura da altura do frame  da camera
FPS = int(cap.get(5))           #faz a leitura do FPS da camera


print("Frame width: ", frame_width, flush=True)
print("Frame height: ", frame_height, flush=True)
print("FPS: ", FPS, flush=True)


while(cap.isOpened()):
    # Captura frame-a-frame
    ret, frame = cap.read()         # verfica se consegui receber com sucesso o novo frame (bool (True/False)) e
                                    #entrega-o para uma variavel + frame
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frameGray',gray)
    cv2.imshow('frameColor', frame)
    if cv2.waitKey(1) & 0xFF == 27: #ESC … time in milliseconds
        break

cap.release()
cv2.destroyAllWindows()



#   •CV_CAP_PROP_POS_MSEC (0) ->   Posição atual no ficheiro de vídeo, em milissegundos, ou instante (timestamp) da captura.
#   •CV_CAP_PROP_POS_FRAMES (1) ->   Índice (a começar em 0) do próximo frame a ser descodificado/capturado.
#   •CV_CAP_PROP_POS_AVI_RATIO (2) ->   Posição relativa no ficheiro de vídeo: 0 - início do filme, 1 - fim do filme.
#   •CV_CAP_PROP_FRAME_WIDTH (3) ->   Largura dos frames do vídeo.
#   •CV_CAP_PROP_FRAME_HEIGHT (4) ->   Altura dos frames do vídeo.
#   •CV_CAP_PROP_FPS (5) ->   Taxa de frames (imagens por segundo).
#   •CV_CAP_PROP_FOURCC (6) ->   Código de 4 caracteres do codec.
#   •CV_CAP_PROP_FRAME_COUNT (7) ->   Número total de frames do ficheiro de vídeo.
#   •CV_CAP_PROP_FORMAT (8) ->   Formato das imagens (objetos Mat) devolvidas pelo retrieve().
#   •CV_CAP_PROP_MODE (9) ->   Valor, específico do backend, que indica o modo de captura atual.
#   •CV_CAP_PROP_BRIGHTNESS (10) ->   Brilho da imagem (só para câmaras).
#   •CV_CAP_PROP_CONTRAST (11) ->   Contraste da imagem (só para câmaras).
#   •CV_CAP_PROP_SATURATION (12) ->   Saturação da imagem (só para câmaras).
#   •CV_CAP_PROP_HUE (13) ->   Matiz (tom de cor) da imagem (só para câmaras).
#   •CV_CAP_PROP_GAIN (14) ->   Ganho da imagem (só para câmaras).
#   •CV_CAP_PROP_EXPOSURE (15) ->   Exposição (só para câmaras).
#   •CV_CAP_PROP_CONVERT_RGB (16) ->   Indicador booleano (True/False) que diz se as imagens devem ser convertidas para RGB.
#   •CV_CAP_PROP_WHITE_BALANCE_U (17) ->   Valor U do balanço de brancos (nota: de momento só suportado pelo backend DC1394 v2.x)
#   •CV_CAP_PROP_WHITE_BALANCE_V (26) ->   Valor V do balanço de brancos (nota: de momento só suportado pelo backend DC1394 v2.x)
#   •CV_CAP_PROP_RECTIFICATION (18) ->   Indicador de retificação para câmaras estéreo (nota: de momento só suportado pelo backend DC1394 v2.x)
#   •CV_CAP_PROP_ISO_SPEED (30) ->   Sensibilidade ISO da câmara (nota: de momento só suportado pelo backend DC1394 v2.x)
#   •CV_CAP_PROP_BUFFERSIZE (38) ->   Número de frames guardados na memória interna (buffer) (nota: de momento só suportado pelo backend DC1394 v2.x)

#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "numpy",
#   "opencv-python",
# ]
# ///

import time
import cv2
import numpy as np

""" Necessidades no projeto
Câmara estática no teto, vídeo em direto, com uma grelha 5×5 sobreposta em todas as frames.

Deteção de movimento significativo por célula, que rejeite o ruído do sensor, os artefactos de compressão e as mudanças graduais de iluminação.

As células com movimento aparecem em negativo ao vivo; as restantes aparecem normais.

Contágio: a primeira célula com movimento é a semente. A partir daí, só se ativam células vizinhas de uma célula ativa (vizinhança de 8). O movimento noutras células é ignorado.

Reset: 10 s sem movimento em toda a imagem apagam tudo.

FPS visível, critério de movimento justificado, parâmetros ajustáveis (sensibilidade, área mínima, intervalo de reset) e feedback visual do estado.

Só métodos dados até agora. A apresentação dura 10 minutos, sem PowerPoint, com demonstração ao vivo.
"""

# A resolução do Frame é 640×480, por causa do DroidCam tem proporção 4:3
#   640×480 -> 4:3
#   640:430 -> 16:9

#---------------------------
#Parametros a utilizar

IP = "192.168.1.81"
CAMERA_SRC = f"http://{IP}:4747/video"
LARGURA = 640          # largura máxima de trabalho
GRID_N = 5             # grelha 5 x 5


#-------------------------
#Iniciação da camera

cap = cv2.VideoCapture(CAMERA_SRC)
if not cap.isOpened():
    print("Não foi possível ligar a", CAMERA_SRC)
    exit(1)

fps = 0.0
contador = 0
T_inicio = time.time()
dt_atualizacao_fps = 0.5
primeira_frame = True
mostrar_information = True




while(cap.isOpened()):
    # Captura frame-a-frame
    ret, frame = cap.read()         
    if not ret:
        print("Frame não Recebida!")
        break

    #Primeiro Passo é Redimensionar a imagem para manter a proporção correta (apenas um sistema de segurança)
    h, w = frame.shape[:2]
    if primeira_frame:
        print("Resolucao recebida:")
        print("Largura", w)
        print("Altura", h)


    if w > LARGURA: #Se a largura for maior que 640, é redimensionada para manter a largura de 640px
        frame = cv2.resize(frame, (LARGURA, int(h * LARGURA / w)), interpolation=cv2.INTER_AREA)

        h, w = frame.shape[:2]

    if primeira_frame:      #apenas para ter acerteza que está na resolução certa
        print("Resolucao de trabalho:")
        print("Largura", w)
        print("Altura", h)
        primeira_frame = False
    

    # 2. FPS (frames contadas em intervalos de 0,5 s)
    contador += 1
    decorrido = time.time() - T_inicio
    if decorrido >= dt_atualizacao_fps:
        fps = contador / decorrido
        contador = 0
        T_inicio = time.time()

    # 3. Cinzento (ainda não é usado; serve para verificar a conversão)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 4. Grelha 5 x 5
    saida = frame.copy() #a grelha será exposta numa copia do frame, para não interromper ou afetar a deteção de movimento
    ys = [round(i * h / GRID_N) for i in range(GRID_N + 1)]    
    xs = [round(j * w / GRID_N) for j in range(GRID_N + 1)]     #estas funções servem para determinar as coordenadas de cada divisão da imagem
                                                                # para gerar a grelha de 5x5 - se for preciso alterar o tamanho da grelha é só mudar GRID_N
                                                                #i	i × 480 / 5	ys
                                                                #0	0	0
                                                                #1	96	96
                                                                #2	192	192
                                                                #3	288	288
                                                                #4	384	384
                                                                #5	480	480

    for y in ys[1:-1]:      #as linhas serão geradas, menos no primeiro e no ultimo setor
        linha = np.array([[0, y], [w - 1, y]], np.int32)
        cv2.polylines(saida, [linha], False, (255, 255, 255), 1)
    for x in xs[1:-1]:
        linha = np.array([[x, 0], [x, h - 1]], np.int32)
        cv2.polylines(saida, [linha], False, (255, 255, 255), 1)



    # 5. Texto do FPS (contorno preto + texto branco, legível sobre qualquer fundo)
    if mostrar_information:
        texto = f"FPS: {fps:.1f}"
        cv2.putText(saida, texto, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3)
        cv2.putText(saida, texto, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    #Argumento	            Valor	            Significado
    #imagem	                saida	            onde escrever
    #texto	                texto	            o que escrever
    #posição	           (10, 25)	            canto inferior esquerdo do texto, em (x, y): 10 píxeis da esquerda, 25 do topo
    #fonte	          FONT_HERSHEY_SIMPLEX	    o tipo de letra
    #escala	                 0.6	            o tamanho do texto
    #cor	   (0, 0, 0) / (255, 255, 255)	    preto / branco, em BGR
    #espessura	            3 / 1	            grossura do traço, em píxeis

    # 6. Mostrar
    cv2.imshow("Contagion - etapa 1", saida)
    cv2.imshow("Cinzento", gray)

    # 7. Teclado
    key = cv2.waitKey(1) & 0xFF
    if key == 27:                        # ESC para sair
        break
    elif key == ord('1'):                # tecla 1: mostra/esconde o FPS
        mostrar_information = not mostrar_information



cap.release()
cv2.destroyAllWindows()
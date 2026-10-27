#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
# "numpy",
# "opencv-python",
# ]
# ///

import time
import cv2
import numpy as np
from pathlib import Path



# A resolução do Frame é 640×480, por causa do DroidCam tem proporção 4:3
#   640×480 -> 4:3
#   640:360 -> 16:9

#---------------------------
#Parametros a utilizar

IP = "192.168.1.81"
CAMERA_SRC = f"http://{IP}:4747/video"
LARGURA = 640          # largura máxima de trabalho

#-----------------
#Parametros para a gravação de vídeo (fase 8, como no Trabalho 1; VideoWriter)
PASTA = Path(r"C:\Users\jpedr\Documents\Visao_computacional\Imagens_OpenCV\Videos")
FICHEIRO = PASTA / "Trabalho_2.avi"    # cada execução do programa substitui o ficheiro anterior

#-----------------
#Parametros da janela (só muda o tamanho com que a imagem é MOSTRADA; o processamento continua em 640x480)
Janela_principal = "Trabalho 2 - Segmentacao e Tracking"
ESCALA_JANELA = 1.5    # 1.5 -> janela de 960x720 para uma imagem de 640x480

#-----------------
#Parametros da segmentação (K-means em HSV)
N_INICIAL = 5          # nº de regiões
N_MIN, N_MAX = 2, 20
PESO_BRILHO_INICIAL = 0.3   # peso do V no K-means (menor = sombras partem menos os objetos)
PESO_BRILHO_MIN, PESO_BRILHO_MAX, PASSO_PESO_BRILHO = 0.0, 1.0, 0.1
KMEANS_TENTATIVAS = 3
KMEANS_CRITERIO = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
MEDIAN_KSIZE = 5
ALFA_SEGMENTACAO = 0.6 # opacidade das cores das regiões

#-----------------
#Parametros da seleção
PASSO_CURSOR = 20      # px por toque na seta
MORPH_KSIZE = 5        # abertura / fecho
AREA_MIN_ALVO = 200    # px

#-----------------
#Parametros do tracking (histograma H-S + backprojection + meanShift)
H_BINS, S_BINS = 30, 32
MARGEM_FORA = 0.5           # zona à volta da seleção que não conta como "fora"
BLUR_HIST = 3
S_MIN_INICIAL, V_MIN_INICIAL = 90, 50   # cor fiável
PASSO_SV = 10
LIMIAR_PROB_INICIAL = 50    # probabilidade mínima para um píxel ser alvo
LIMIAR_PROB_MIN, LIMIAR_PROB_MAX, PASSO_LIMIAR_PROB = 10, 250, 10
MEANSHIFT_CRITERIO = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
MARGEM_MASCARA = 0.25       # a máscara é procurada numa zona 25% maior que a janela
BLUR_PROB = 7
JANELA_MIN = 20             # px
JANELA_ESCALA_MAX = 3.0     # máximo 3x o tamanho inicial
BLUR_PROCURA = 31           # procura na imagem toda
LIMIAR_PROCURA = 30
N_CANDIDATOS = 3

#-----------------
#Parametros da confiança e dos estados (TRACKING / OCCLUDED / LOST)
T_SIM_INICIAL = 0.5         # limiar de semelhança
T_SIM_MIN, T_SIM_MAX, PASSO_T_SIM = 0.1, 0.95, 0.05
MARGEM_RECUPERAR = 0.1      # histerese: para voltar é preciso T_SIM + 0.1
ALFA_AREA = 0.1             # atualização da área de referência
AREA_MIN_REL = 0.4          # área face à referência
AREA_MAX_REL = 2.5
AREA_RECUPERAR_REL = 0.10   # área face à inicial, para voltar
AREA_RECUPERAR_MAX = 5.0
PESO_INICIAL = 0.35         # peso mínimo do modelo original
ALFA_MODELO = 0.15          # aprendizagem do modelo
CONF_ATUALIZAR = 0.6        # confiança mínima para aprender
# Zona de movimento (Farneback)
FARNEBACK_ESCALA = 0.25         # corre a 160x120
FARNEBACK_LIMIAR = 1.0          # px por frame
FARNEBACK_DILATE = 5
PESO_MOVIMENTO_MAX = 0.4
FRACAO_MOV_CHEIA = 0.3
FRACAO_MOV_GLOBAL = 0.5     # acima disto a câmara mexeu-se
SALTO_RECUPERAR_MOV = 200   # px, candidato a mexer-se
VEL_RECUPERAR_MOV = 600     # px/s
MOV_MIN_LONGE = 0.08
FRAMES_CONFIRMAR = 3
SALTO_MAX = 40              # px
SALTO_RECUPERAR = 60        # px, candidato parado
VEL_RECUPERAR = 150         # px/s
AREA_MIN_INICIAL_REL = 0.10
T_OCC_INICIAL = 2.0         # s em OCCLUDED até LOST
T_OCC_MIN, T_OCC_MAX, PASSO_T_OCC = 0.5, 10.0, 0.5
FATOR_JANELA = 4.0          # largura da janela = 4 x desvio padrão

#-----------------
#Modos do programa
MODO_AO_VIVO = 0
MODO_SEGMENTACAO = 1
MODO_SELECAO = 2
MODO_TRACKING = 3
NOMES_MODOS = ["AO VIVO", "SEGMENTACAO", "SELECAO", "TRACKING"]

#Estados do tracking
EST_TRACKING = 0
EST_OCCLUDED = 1
EST_LOST = 2
NOMES_ESTADOS = ["TRACKING", "OCCLUDED", "LOST"]

#-----------------
#Cores (BGR)--> apenas é utilizado para colocar coisas á frente da janela
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (0, 255, 255)
VERMELHO = (0, 0, 255)
CORES_ESTADOS = [VERDE, AMARELO, VERMELHO]   # cor da janela e do texto em TRACKING / OCCLUDED / LOST

#-----------------
#Códigos das teclas especiais (devolvidos pelo cv2.waitKeyEx; as setas mudam conforme o sistema operativo)
#                 Windows    Linux
SETA_CIMA     = (2490368,   65362,)
SETA_BAIXO    = (2621440,   65364,)
SETA_ESQUERDA = (2424832,   65361,)
SETA_DIREITA  = (2555904,   65363,)
TECLA_ENTER = (13, 10)
TECLA_BACKSPACE = 8

TECLAS = """
---------------- Teclas ----------------
  ESC                    sair
  1                      mostrar/esconder o FPS e as informacoes
 AO VIVO
  S                      congelar o frame e segmentar
 SEGMENTACAO
  S                      congelar um frame mais recente (mantem o N e o peso)
  + / -  (setas cima/baixo)   mais / menos regioes (N)
  setas esquerda/direita      menos / mais peso do brilho (V)
  Enter                  aceitar a segmentacao
  Backspace              voltar ao video ao vivo
 SELECAO
  setas                  mover a cruz para cima do objeto
  A                      juntar ao alvo a mancha debaixo da cruz
  X                      tirar do alvo a mancha debaixo da cruz
  C                      limpar o alvo (comecar de novo)
  Enter                  confirmar o alvo (se nao juntou nada, usa a mancha debaixo da cruz)
  Backspace              voltar a segmentacao
 TRACKING
  setas esquerda/direita      menos / mais limiar de probabilidade (o que conta como alvo)
  setas cima/baixo            mais / menos limiar de semelhanca (T_SIM)
  O / P                  menos / mais tempo em OCCLUDED ate passar a LOST (T_OCC)
  F                      ligar/desligar a zona de movimento (optical flow de Farneback)
  U                      ligar/desligar a aprendizagem do modelo (aprende devagar as cores atuais do alvo)
  K / L                  menos / mais saturacao minima da cor fiavel
  N / M                  menos / mais brilho minimo da cor fiavel
  D                      janela do mapa: 1.a vez abre, 2.a vez junta os vetores do Farneback, 3.a vez fecha
  C                      apagar o caminho (o tracking continua)
  R                      reset: voltar ao video ao vivo
  (as teclas so funcionam com uma janela do programa selecionada)
  (o video da janela principal e gravado automaticamente em Imagens_OpenCV/Videos/Trabalho_2.avi)
-----------------------------------------
"""

fps = 0.0
n_medicoes_fps = 0       # a 1.ª medição não serve para a gravação
out = None               # VideoWriter
contador = 0 #contador de frames em x tempo
T_inicio = time.time()
dt_atualizacao_fps = 0.5
primeira_frame = True   #apenas variavel temporaria para o programa
mostrar_information = True  #variavel para permitir mostrar os valores no monitor



modo = MODO_AO_VIVO
frame_congelado = None   # frame da tecla S
N = N_INICIAL
peso_brilho = PESO_BRILHO_INICIAL
precisa_segmentar = False
etiquetas = None         # nº da região de cada píxel
CORES_REGIOES = np.random.default_rng(7).integers(40, 256, (N_MAX, 3), dtype=np.uint8)   # uma cor por região
vista_seg = None
tempo_seg = 0.0



cursor_x, cursor_y = 0, 0   # posição da cruz
mancha_bruta = None      # mancha antes da limpeza
mascara_sel = None       # mancha debaixo da cruz, limpa
vista_sel = None
precisa_selecao = False
mascara_alvo = None      # alvo confirmado
mascara_juntada = None   # alvo construído com A / X



hist_alvo = None         # modelo usado no tracking
hist_inicial = None      # modelo da seleção
hist_aprendido = None
resto_original = 1.0
janela = None            # (x, y, largura, altura)
area0 = 0                # área inicial
area_ref = 0             # área de referência
janela_max = None
tamanho_inicial = None   # (largura, altura) da janela no momento da seleção
centroide = None
area_alvo = 0
mascara_atual = None
prob = None              # mapa de probabilidade
limiar_prob = LIMIAR_PROB_INICIAL
s_min, v_min = S_MIN_INICIAL, V_MIN_INICIAL   # cor fiável
mostrar_prob = 0         # tecla D: 0, 1 ou 2
fluxo_mov = None
magnitude_mov = None
mov_candidato = None

estado = EST_TRACKING
t_inicio_oclusao = 0.0
conf0 = 1.0              # referência da confiança
confianca = 0.0
t_sim = T_SIM_INICIAL
t_occ = T_OCC_INICIAL
aprender = True          # tecla U
usar_movimento = True    # tecla F
cinz_ant = None          # frame anterior (Farneback)
zona_mov = None
w_mov = 0.0              # peso do movimento
melhor_cand = None
motivo_rejeicao = ""
n_confirmacoes = 0
cand_anterior = None        #candidato anterior
n_cand = 0

camada_caminho = None    # onde se desenha o caminho
centroide_ant = None
ultimo_visto = None      # último centroide conhecido





#---------------------------
#Funções
#---------------------------



def redimensionar(frame, largura_max):
    h, w = frame.shape[:2]
    if w > largura_max: #Se a largura for maior que 640, é redimensionada para manter a largura de 640px
        frame = cv2.resize(frame, (largura_max, int(h * largura_max / w)), interpolation=cv2.INTER_AREA)
    return frame




#--------------------------
#   Segmentação (fase 2)

def segmentar_kmeans(frame, N, peso_brilho):
   
    h, w = frame.shape[:2]

    suave = cv2.medianBlur(frame, MEDIAN_KSIZE)          # tira o ruído "sal e pimenta" antes de agrupar
    hsv = cv2.cvtColor(suave, cv2.COLOR_BGR2HSV)         # H = tom, S = saturação, V = brilho

    Z = hsv.reshape((-1, 3))                             # converter a matrix em 3 colunas (H, S, V), uma linha por pixel
    Z = np.float32(Z)                                    # o kmeans necessita de float32
    Z[:, 2] = Z[:, 2] * peso_brilho                      # o brilho (V) passa a contar menos do que o tom e a saturação

    _, rotulos, _ = cv2.kmeans(Z, N, None, KMEANS_CRITERIO, KMEANS_TENTATIVAS, cv2.KMEANS_PP_CENTERS) #executa a segmentação
    # rotulos: uma coluna com a região (0..N-1) de cada píxel (os centros não são precisos)

    etiquetas = rotulos.reshape(h, w).astype(np.uint8)   # volta à forma de imagem (matrix)
    etiquetas = cv2.medianBlur(etiquetas, MEDIAN_KSIZE)  # tira píxeis soltos de todas as regiões de uma vez
    return etiquetas


def vista_segmentacao(frame, etiquetas, N):

    seg = CORES_REGIOES[etiquetas]                                   # cada píxel com a cor da sua região
    vista = cv2.addWeighted(frame, 1 - ALFA_SEGMENTACAO, seg, ALFA_SEGMENTACAO, 0)   # vê-se a imagem real e as regiões

    # fronteiras: cada região com um tom de cinzento diferente e o Canny marca onde o tom muda
    passo = 255 // max(N - 1, 1)                                     # atribui a cada região um tom de cinza bem diferente
    tons = (etiquetas.astype(np.int32) * passo).astype(np.uint8)
    fronteiras = cv2.Canny(tons, 10, 20)                             # qualquer mudança de região dá um salto >= passo
    vista[fronteiras > 0] = BRANCO

    for i in range(N):                                               # número de cada região, sempre DENTRO da região
        ys, xs = np.nonzero(etiquetas == i)
        if len(xs) == 0:                                             # região sem píxeis (segurança)
            continue
        # o centro (média) de uma região com forma irregular pode cair fora dela (noutra região);
        # por isso escolhe-se o píxel DA região mais perto desse centro
        mx, my = xs.mean(), ys.mean()
        k = np.argmin((xs - mx) ** 2 + (ys - my) ** 2)
        pos = (int(xs[k]) - 6, int(ys[k]) + 6)
        cv2.putText(vista, str(i), pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, PRETO, 4, cv2.LINE_AA)       # contorno preto (lê-se sobre qualquer cor)
        cv2.putText(vista, str(i), pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, VERMELHO, 2, cv2.LINE_AA)    # número a vermelho por cima
    return vista




#--------------------------
#   Seleção (fase 3)

def reconstruir(mascara, x, y, passo=1):
    # fica só com a parte da máscara ligada ao ponto (x, y): cresce a partir do ponto, sempre cortada pela máscara
    mancha = np.zeros_like(mascara)
    if mascara[y, x] == 0:                                  # o ponto não está na máscara
        return mancha
    mancha[y, x] = 255                                      # semente: só o ponto
    kernel = np.ones((3, 3), np.uint8)
    while True:
        nova = cv2.bitwise_and(cv2.dilate(mancha, kernel, iterations=passo), mascara)   # cresce, mas nunca para fora da máscara
        if np.array_equal(nova, mancha):                              # deixou de crescer: a mancha está completa
            return mancha
        mancha = nova


def mancha_do_ponto(etiquetas, x, y):
    regiao = np.uint8(etiquetas == etiquetas[y, x]) * 255   # todos os píxeis da região do ponto (branco)
    regiao = erodir_e_dilatar(regiao)                       # corta as pontes finas ANTES de crescer
    return reconstruir(regiao, x, y)


def erodir_e_dilatar(mascara):
    
    kernel = np.ones((MORPH_KSIZE, MORPH_KSIZE), np.uint8)
    return cv2.dilate(cv2.erode(mascara, kernel), kernel)


def dilatar_e_erodir(mascara):
    
    kernel = np.ones((MORPH_KSIZE, MORPH_KSIZE), np.uint8)
    return cv2.erode(cv2.dilate(mascara, kernel), kernel)


def desenhar_contorno(img, mascara, cor, espessura=2):
    
    kernel = np.ones((espessura + 1, espessura + 1), np.uint8)
    borda = cv2.bitwise_and(cv2.dilate(mascara, kernel), cv2.bitwise_not(cv2.erode(mascara, kernel)))
    img[borda > 0] = cor


def desenhar_cruz(img, x, y, cor=VERMELHO, tamanho=12):
    
    cv2.line(img, (x - tamanho, y), (x + tamanho, y), PRETO, 4)   # contorno preto, para se ver sobre qualquer cor
    cv2.line(img, (x, y - tamanho), (x, y + tamanho), PRETO, 4)
    cv2.line(img, (x - tamanho, y), (x + tamanho, y), cor, 2)
    cv2.line(img, (x, y - tamanho), (x, y + tamanho), cor, 2)


def vista_selecao(frame, juntada, atual):
    
    cinzento = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)   # volta a ter 3 canais, para se poder pintar
    vista = (cinzento * 0.6).astype(np.uint8)        # o resto fica cinzento e mais escuro
    cores = cv2.bitwise_or(juntada, atual) > 0
    vista[cores] = frame[cores]                      # o alvo e a mancha atual ficam com as cores reais
    desenhar_contorno(vista, atual, AMARELO)
    desenhar_contorno(vista, juntada, VERDE)
    return vista




#--------------------------
#   Modelo do alvo e tracking (fase 4)

def mascara_cor_valida(hsv):
    
    return cv2.inRange(hsv, np.array((0, s_min, v_min)), np.array((180, 255, 255)))   # s_min e v_min ajustáveis


def retangulo_da_mascara(mascara):
    
    ys, xs = np.nonzero(mascara)    #devolve as coordenadas dos pontos alvo
    return (int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1))


def criar_modelo(frame, mascara):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    valida = mascara_cor_valida(hsv)
    dentro = cv2.bitwise_and(mascara, valida)                # píxeis do alvo com cor fiável
    
    if np.count_nonzero(dentro) == 0:                        # alvo todo cinzento/preto/branco: usa-se a máscara toda (o tracking vai ser fraco)
        dentro = mascara

    
    x, y, wm, hm = retangulo_da_mascara(mascara)    #calcula o tamanho do retangulo e a sua posi
    mx, my = int(wm * MARGEM_FORA), int(hm * MARGEM_FORA) #aumenta a margem do retangulo
    perto = np.zeros_like(mascara)  #cria uma matriz toda preta do tamanho da mascara alvo
    perto[max(y - my, 0):y + hm + my, max(x - mx, 0):x + wm + mx] = 255 #coloca o retangulo extendido nessa matrix
    #isto serve para tentar separar um bocado o objeto do exterior, para quando for feita a comparação ele não ter tanta probabilidade de apanhar pixeis do objeto
    fora = cv2.bitwise_and(cv2.bitwise_not(perto), valida)  #identificamos apenas o exterior 

    hist_dentro = cv2.calcHist([hsv], [0, 1], dentro, [H_BINS, S_BINS], [0, 180, 0, 256])   #calculo do histograma no objeto alvo
    hist_fora = cv2.calcHist([hsv], [0, 1], fora, [H_BINS, S_BINS], [0, 180, 0, 256])       #calculo do histograma no exterior em volta do objeto com margem de segurança

    # suaviza os dois histogramas (GaussianBlur): cada cor "empresta" valor às caixas vizinhas,
    # para que tonalidades um pouco diferentes do mesmo objeto (ex.: a parte à sombra) também sejam reconhecidas
    hist_dentro = cv2.GaussianBlur(hist_dentro, (BLUR_HIST, BLUR_HIST), 0)
    hist_fora = cv2.GaussianBlur(hist_fora, (BLUR_HIST, BLUR_HIST), 0)

    hist = hist_dentro / (hist_dentro + hist_fora + 1e-6)    # fração da cor que é do alvo (0 a 1); o 1e-6 evita dividir por 0
    #uma cor que só aparece no alvo fica perto de 1;
    #uma cor que só aparece no fundo fica perto de 0;
    #uma cor que aparece nos dois fica com um valor intermédio. Por exemplo, se 30% dos píxeis dessa cor são do alvo e 70% do fundo, vale cerca de 0,3
    hist = np.float32(hist)
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)       # a cor mais típica do alvo vale 255 (normalize):
                                                             # o mapa fica forte mesmo que nenhuma cor seja 100% exclusiva do alvo
    return hist


def backprojection(frame, hist):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    p = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1) #cria um mapa de comparação com um histograma, e quando for parecido ele poem a branco
    return cv2.bitwise_and(p, mascara_cor_valida(hsv))


def mascara_do_alvo(prob, janela, limiar):
    # zona de procura: a janela alargada 25% para cada lado (sem sair da imagem), para o alvo poder crescer
    h_img, w_img = prob.shape[:2]
    x, y, wj, hj = janela
    mx, my = int(wj * MARGEM_MASCARA), int(hj * MARGEM_MASCARA)
    x0, y0 = max(x - mx, 0), max(y - my, 0)
    x1, y1 = min(x + wj + mx, w_img), min(y + hj + my, h_img)
    m = np.zeros_like(prob)

    suave = cv2.GaussianBlur(prob[y0:y1, x0:x1], (BLUR_PROB, BLUR_PROB), 0)   # junta os píxeis acesos (tapa buracos do ruído)
    _, recorte = cv2.threshold(suave, limiar, 255, cv2.THRESH_BINARY)          # acima do limiar = alvo
    recorte = erodir_e_dilatar(recorte)                                        # abertura: tira pontinhos e ligações finas

    # um objeto é UMA mancha: fica só a ligada ao ponto mais aceso (os pontos soltos do fundo não contam)
    _, max_val, _, max_loc = cv2.minMaxLoc(suave, recorte)  #dá a localização e o valor ponto mais alto
     # o ponto mais aceso DENTRO da máscara
    if max_val > 0:
        recorte = reconstruir(recorte, max_loc[0], max_loc[1], passo=3)   # 3 píxeis por volta (mais rápido)

    m[y0:y1, x0:x1] = dilatar_e_erodir(recorte)              # fecho: tapa buracos dentro da mancha
    return m


def centroide_e_area(mascara):
    ys, xs = np.nonzero(mascara)
    if len(xs) == 0:
        return None, 0
    return (int(xs.mean()), int(ys.mean())), len(xs)


def ajustar_janela(janela, mascara, centroide, w_img, h_img, tamanho_max):
    if centroide is None:                       # sem alvo na janela: fica como estava
        return janela
    ys, xs = np.nonzero(mascara)
    wj = int(min(max(FATOR_JANELA * xs.std(), JANELA_MIN), w_img, tamanho_max[0]))
    hj = int(min(max(FATOR_JANELA * ys.std(), JANELA_MIN), h_img, tamanho_max[1]))
    x = min(max(centroide[0] - wj // 2, 0), w_img - wj)
    y = min(max(centroide[1] - hj // 2, 0), h_img - hj)
    return (x, y, wj, hj)


def candidatos_na_imagem(prob, tamanho):
    h_img, w_img = prob.shape[:2] # tamanho da imagem (480, 640)
    wj, hj = tamanho    # tamanho de cada janela (o inicial)
    suave = cv2.GaussianBlur(prob, (BLUR_PROCURA, BLUR_PROCURA), 0) #desfocamos a imagem para tentar separar ainda mais o monte
    janelas = []

    for _ in range(N_CANDIDATOS):   #repete 3 vezes
        _, max_val, _, max_loc = cv2.minMaxLoc(suave)   #Encontra o ponto mais alto do mapa desfocado
        if max_val < LIMIAR_PROCURA:            # não há mais nada parecido com o alvo na imagem
            break
        x = min(max(max_loc[0] - wj // 2, 0), w_img - wj)   #calcula a posição das janelas
        y = min(max(max_loc[1] - hj // 2, 0), h_img - hj)
        janelas.append((x, y, wj, hj))  #guarda a janela
        suave[y:y + hj, x:x + wj] = 0           # apaga o monte, para o próximo minMaxLoc encontrar o seguinte
    return janelas


def medir(prob, janela, limiar):
    m = mascara_do_alvo(prob, janela, limiar)   #desenha a fronteira do objeto
    c, area = centroide_e_area(m)   #calculo do centroide do objeto
    media = float(prob[m > 0].mean()) if area > 0 else 0.0  #probabilidade media dos pixeis do alvo que pertecem no modelo
    #esta media é a media atual do que está a ser visualizado e é constantemente calculado
    return m, c, area, media


def zona_de_movimento(frame, cinz_ant):
    cinz = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converter para cinzento
    cinz = cv2.resize(cinz, None, fx=FARNEBACK_ESCALA, fy=FARNEBACK_ESCALA, interpolation=cv2.INTER_AREA)
    if cinz_ant is None:
        return None, cinz, None, None
    fluxo = cv2.calcOpticalFlowFarneback(cinz_ant, cinz, None, 0.5, 3, 15, 3, 5, 1.2, 0) #deteção da zona de movimento
    magnitude, _ = cv2.cartToPolar(fluxo[..., 0], fluxo[..., 1])
    magnitude = magnitude / FARNEBACK_ESCALA
       # em píxeis da imagem de 640x480
    _, zona = cv2.threshold(magnitude, FARNEBACK_LIMIAR, 1, cv2.THRESH_BINARY) # acima do limiar -> movimento (1)
    zona = np.uint8(zona)         
    zona = cv2.dilate(zona, np.ones((FARNEBACK_DILATE, FARNEBACK_DILATE), np.uint8)) 
    #dilatar a zona de movimento, para permitir incluir o interior de um objeto liso
    h, w = frame.shape[:2]
    return cv2.resize(zona, (w, h), interpolation=cv2.INTER_NEAREST), cinz, fluxo, magnitude


def desenhar_vetores(img, fluxo, passo=16):
    h, w = img.shape[:2]
    for y in range(passo // 2, h, passo):
        for x in range(passo // 2, w, passo):
            fx, fy = fluxo[int(y * FARNEBACK_ESCALA), int(x * FARNEBACK_ESCALA)] / FARNEBACK_ESCALA     # em px por frame da imagem de 640x480
            cor = VERDE if np.hypot(fx, fy) > FARNEBACK_LIMIAR else (90, 90, 90)
            cv2.line(img, (x, y), (int(x + 10 * fx), int(y + 10 * fy)), cor, 1)
            cv2.circle(img, (x, y), 1, cor, -1)


def peso_movimento(zona, janela):
    if zona is None:                          # ainda não há zona de movimento (1.º frame)
        return 0.0
    if zona.mean() > FRACAO_MOV_GLOBAL:       # caso mais de metade da imagem mexa-se
        return 0.0

    x, y, wj, hj = janela
    if wj == 0 or hj == 0:                    # janela vazia
        return 0.0
    recorte = zona[y:y + hj, x:x + wj]        # a zona de movimento só dentro da janela
    fracao = recorte.mean()                   # fração dos píxeis da janela que se mexem (0 a 1)

    if fracao >= FRACAO_MOV_CHEIA:            # 30% ou mais a mexer-se: peso máximo
        return PESO_MOVIMENTO_MAX
    return PESO_MOVIMENTO_MAX * fracao / FRACAO_MOV_CHEIA   # menos do que isso: peso proporcional


def passo_tracking(frame, hist, janela, limiar, zona=None, w_mov=0.0):
    p = backprojection(frame, hist)
    if zona is not None and w_mov > 0:
        parado = zona == 0                                         # píxeis sem movimento
        p[parado] = (p[parado] * (1 - w_mov)).astype(np.uint8)     # faz os pixeis parados perder valor (ex.: 0,4 -> ficam com 60%)
    _, jan = cv2.meanShift(p, janela, MEANSHIFT_CRITERIO)   #move a janela para cima do objeto no mapa de probabilidade
    m, c, area, media = medir(p, jan, limiar)
    return p, jan, m, c, area, media


def passa_verificacoes(c, area, media, area_base, conf0, limiar_conf, area_min, area_max, centroide_ref=None, salto_max=SALTO_MAX):
   #verifica se tem centroide, se a A confiança (média atual ÷ referência) é alta o suficiente,
   #  se a área é comparada com uma área de referência (area do objeto em função do tempo) e se nunca passa mais do 10% na area inicial
    if c is None:
        return False
    if media / conf0 < limiar_conf:
        return False
    if not (area_min <= area / area_base <= area_max):
        return False
    if area < AREA_MIN_INICIAL_REL * area0:                # nunca abaixo de 15% da área inicial
        return False
    if centroide_ref is not None and np.hypot(c[0] - centroide_ref[0], c[1] - centroide_ref[1]) > salto_max:
        return False
    return True


def juntar_candidatos(prob, candidato_janela, tamanho):
    # candidatos para recuperar o alvo: o da janela congelada + os "montes" mais acesos da imagem toda
    candidatos = [candidato_janela]
    for jc in candidatos_na_imagem(prob, tamanho):  #devolve os candidatos para o objeto
        _, jc = cv2.meanShift(prob, jc, MEANSHIFT_CRITERIO)   # centra o candidato no objeto antes de o medir
        candidatos.append((jc,) + medir(prob, jc, limiar_prob)) #e feita a medição do cadidato detro da janela
        #O append junta um elemento ao fim de uma lista
    return candidatos


def escolher_candidato(candidatos, zona_mov, ultimo_visto, tempo_perdido):
    # devolve (o 1.º candidato que passa em tudo ou None, porque é que o último foi recusado, movimento medido)
    motivo = ""
    mov_medido = None

    for cand in candidatos:
        jc, mc, cc, ac, mdc = cand  #janela (jc), máscara (mc), centroide (cc), área (ac), média (mdc)
        if cc is None:                                         # sem alvo nesta janela
            continue

        # 1. parece-se com o alvo? (limiares mais exigentes do que para ficar: histerese)
        if not passa_verificacoes(cc, ac, mdc, area0, conf0, t_sim + MARGEM_RECUPERAR, AREA_RECUPERAR_REL, AREA_RECUPERAR_MAX):
            motivo = motivo or "conf/area"
            continue

        # 2. está a uma distância possível do sítio onde se perdeu?
        if ultimo_visto is None:            # nunca houve um último sítio
            dist = 0.0
        else:
           dx = cc[0] - ultimo_visto[0]    # diferença em x
           dy = cc[1] - ultimo_visto[1]    # diferença em y
           dist = np.sqrt(dx**2 + dy**2)     # distância em linha reta (Pitágoras)

        if usar_movimento:  #se o movimento do farneback estiver ativo
            mov = float(zona_mov[mc > 0].mean()) if zona_mov is not None else 0.0   # fração dos píxeis do candidato a mexer-se
            mov_medido = mov

            if mov >= MOV_MIN_LONGE:                           # a mexer-se: pode estar longe o objeto
                limite = SALTO_RECUPERAR_MOV + VEL_RECUPERAR_MOV * tempo_perdido

                if dist > limite:
                    motivo = f"longe demais a mexer-se ({dist:.0f} > {limite:.0f} px)"
                    continue
            elif dist > SALTO_RECUPERAR:                       # parado: só perto
                motivo = f"parado longe ({dist:.0f} > {SALTO_RECUPERAR} px, mov {mov:.2f})"
                continue
        else:                                                  # se o movimento não esitver ativo movimento: a distância permitida cresce com o tempo
            limite = SALTO_RECUPERAR + VEL_RECUPERAR * tempo_perdido
            if dist > limite:
                motivo = f"longe demais ({dist:.0f} > {limite:.0f} px)"
                continue

        return cand, motivo, mov_medido
    return None, motivo, mov_medido




#--------------------------
#   Caminho do centroide (fase 5)

def atualizar_caminho(camada, centroide, centroide_ant, ultimo_visto):
    if centroide is None:
        return ultimo_visto
    if centroide_ant is not None:
        cv2.line(camada, centroide_ant, centroide, VERDE, 2)
    elif ultimo_visto is not None:
        cv2.line(camada, ultimo_visto, centroide, AMARELO, 2)
    return centroide




#--------------------------
#   Dezenhos das informações na janela

def escrever(img, texto, pos, cor=BRANCO, escala=0.6):
    cv2.putText(img, texto, pos, cv2.FONT_HERSHEY_SIMPLEX, escala, cor, 1, cv2.LINE_AA)


def desenhar_texto(img, texto, n_linha, cor=BRANCO):
    pos = (10, 25 + 22 * n_linha)
    escrever(img, texto, pos, cor)


def desenhar_texto_direita(img, texto, n_linha, cor=BRANCO):
    h, w = img.shape[:2]
    (largura, _), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 3)   # largura do texto em píxeis
    pos = (w - largura - 10, 25 + 22 * n_linha)    # 10 píxeis de margem à direita
    escrever(img, texto, pos, cor)



#-----------------
# Fim das funções
#-----------------















#-------------------------
#Iniciação da camera

cap = cv2.VideoCapture(0) #leitura da camera vindo do protatil
#cap = cv2.VideoCapture(CAMERA_SRC)  #captura de video (DroidCam por IP)


if not cap.isOpened(): #pequena verificação se a camera ligou
    print("Não foi possível ligar à câmara")
    exit(1)

print(TECLAS)   # mensagem inicial com as teclas disponíveis




# (no Windows o WINDOW_KEEPRATIO é ignorado: se a janela for esticada com o rato, a imagem deforma)
cv2.namedWindow(Janela_principal, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO) 

T_inicio = time.time()  # a medição do FPS começa aqui, depois de a câmara estar ligada (e não no início do programa)

while(cap.isOpened()):


    ret, frame = cap.read() #captura o frame e verifica se o recebeu
    if not ret:
        print("Frame não Recebida!")
        break

    # 1. Redimensionar
    h_cam, w_cam = frame.shape[:2]              # verificação da resolução original da imagem
    frame = redimensionar(frame, LARGURA)   #executa o redimensionar para passar o frame para um multiplo de 680
    h, w = frame.shape[:2]                      # resolução do frame pos redimensionamento

    if primeira_frame:      # só na 1.ª frame: confirmar a resolução e dar o tamanho inicial à janela
        print(f"Resolucao recebida: {w_cam}x{h_cam}  ->  resolucao de trabalho: {w}x{h}")
        cv2.resizeWindow(Janela_principal, int(w * ESCALA_JANELA), int(h * ESCALA_JANELA))   # depois pode ser mudado com o rato
        primeira_frame = False



    # 2. FPS (frames contadas em intervalos de 0,5 s)
    contador += 1
    Delta_T = time.time() - T_inicio
    if Delta_T >= dt_atualizacao_fps:   # a cada 0,5s calcula quantos frames ocorreram em função desse tempo
        fps = contador / Delta_T
        contador = 0
        T_inicio = time.time()
        n_medicoes_fps += 1



    # 3. Segmentação: só corre quando é pedida (tecla S ou mudança do N), nunca em todos os frames
    if precisa_segmentar:
        t0 = time.time()
        etiquetas = segmentar_kmeans(frame_congelado, N, peso_brilho)
        vista_seg = vista_segmentacao(frame_congelado, etiquetas, N)
        tempo_seg = time.time() - t0
        precisa_segmentar = False



    # 4. Seleção: recalcula a mancha só quando a cruz sai da mancha atual (mexer a cruz dentro da mesma mancha não muda nada)
    if precisa_selecao:
        if mancha_bruta is None or mancha_bruta[cursor_y, cursor_x] == 0:
            mancha_bruta = mancha_do_ponto(etiquetas, cursor_x, cursor_y)
            mascara_sel = dilatar_e_erodir(mancha_bruta)     # a abertura já foi feita dentro do mancha_do_ponto (antes de crescer)
        vista_sel = vista_selecao(frame_congelado, mascara_juntada, mascara_sel)
        precisa_selecao = False



    # 5. Tracking (fases 4 a 6): corre em todos os frames do modo TRACKING
    if modo == MODO_TRACKING:
        agora = time.time()
        zona_mov, cinz_ant, fluxo_mov, magnitude_mov = zona_de_movimento(frame, cinz_ant)   # deteção da zona de movimento com o Farneback
        
        
        if usar_movimento and zona_mov is not None: #existe movimento
            if estado == EST_TRACKING: #objeto em tracking atualmente
                jan_peso = janela          # janela é o retangulo fisico que identifica para o utilizador o objeto
                                           #atribuimos valor ao movimento dentro desta janela, caso esteja em track
            
            else: # perdido: o movimento da imagem toda
                jan_peso = (0, 0, w, h)    # o retângulo da imagem toda: (0, 0, 640, 480)
                
            w_mov = peso_movimento(zona_mov, jan_peso)


        else:   #não existe movimento
            w_mov = 0.0
        prob, jan_ms, m, c, area, media = passo_tracking(frame, hist_alvo, janela, limiar_prob, zona_mov, w_mov)
        aceite = False      # o frame começa sempre como não confiavel
        estado_antes = estado



        if estado == EST_TRACKING:      #apenas verifica se está em tracking
            # continua em tracking: limiares normais + salto face ao último centroide aceite
            if passa_verificacoes(c, area, media, area_ref, conf0, t_sim, AREA_MIN_REL, AREA_MAX_REL, ultimo_visto):
                aceite = True
            else:
                estado = EST_OCCLUDED            # falhou: a janela fica congelada na última posição boa e muda o titulo
                n_confirmacoes, cand_anterior = 0, None #candidato passa a não existir, e a confirmação fica a 0
                t_inicio_oclusao = agora
        
        else:
            # está em OCCLUDED ou LOST: 
            # tentar VOLTAR, com os limiares mais exigentes
            #  Candidatos: perto da janela congelada (meanShift) e na imagem toda.
            # 1. juntar candidatos
            
            candidatos = juntar_candidatos(prob, (jan_ms, m, c, area, media), tamanho_inicial)
            # entra o mapa de probabilidade, a janela, máscara, centroide, área e média e a janela normal inicial
            # para a janela do D: o melhor candidato e quantos a procura na imagem toda encontrou

            melhor_cand = max(((mdc / conf0, ac / area0) for (_, _, cc, ac, mdc) in candidatos if cc is not None), default=None)    #calcula aquele que tem melhor probabilidade de ser candidato - apenas informação
            n_cand = len(candidatos) - 1 #mostra o numero de candidatos

            # 2. escolher o primeiro candidato que passa em tudo
            bom, motivo_rejeicao, mov = escolher_candidato(candidatos, zona_mov, ultimo_visto, agora - t_inicio_oclusao)
            if melhor_cand is None:
                motivo_rejeicao = "nenhum candidato com alvo"
            if mov is not None:
                mov_candidato = mov #copia o valor do moviemnto do candidato

            # 3. confirmar: o candidato tem de aparecer FRAMES_CONFIRMAR em 3 frames seguidos no mesmo sítio
            if bom is None:
                n_confirmacoes, cand_anterior = 0, None
            else:
                centro_bom = bom[2]                              # centroide do candidato bom (x, y)
                #    está perto do candidato bom do frame anterior?
                if cand_anterior is None:
                    perto = False                                # é o primeiro: não há com que comparar
                else:
                   dx = centro_bom[0] - cand_anterior[0]
                   dy = centro_bom[1] - cand_anterior[1]
                   perto = np.hypot(dx, dy) <= SALTO_RECUPERAR  # até 60 px = o mesmo objeto

                # conta os frames seguidos no mesmo sítio
                if perto:
                    n_confirmacoes = n_confirmacoes + 1          # mais um frame no mesmo sítio
                else:
                   n_confirmacoes = 1                           # sítio novo: recomeça a contar

                cand_anterior = centro_bom                       # guarda para o próximo frame
                motivo_rejeicao = f"a confirmar {n_confirmacoes}/{FRAMES_CONFIRMAR}"   # para o ecrã

                if n_confirmacoes >= FRAMES_CONFIRMAR:
                    jan_ms, m, c, area, media = bom
                    estado = EST_TRACKING   #passa a tracking
                    aceite = True
                    n_confirmacoes, cand_anterior = 0, None

            # 4. demasiado tempo em OCCLUDED sem recuperar -> LOST
            if not aceite and estado == EST_OCCLUDED and agora - t_inicio_oclusao >= t_occ:
                estado = EST_LOST                                # demasiado tempo sem recuperar: perdido

        confianca = media / conf0
        area_alvo = area




        if aceite:  #o objeto foi aceite
            # 1. área de referência
            if estado_antes != EST_TRACKING:              # acabou de recuperar: a referência recomeça
                area_ref = area
            else:                                         # já estava a seguir: acompanha devagar (90% + 10%)
                area_ref = (1 - ALFA_AREA) * area_ref + ALFA_AREA * area

            # 2. janela e resultado deste frame
            janela = ajustar_janela(jan_ms, m, c, w, h, janela_max)
            mascara_atual, centroide = m, c

            # 3. aprender as cores atuais do alvo
            ja_seguia = estado_antes == EST_TRACKING        #condições apra permitir aprende
            confia = media / conf0 >= CONF_ATUALIZAR        # a confiança é ≥ 0,6
            mexe = w_mov > 0 or not usar_movimento        # com o movimento ligado, só aprende com o alvo a mexer-se

            if aprender and ja_seguia and confia and mexe:
                # só os píxeis do alvo que se mexem (um objeto parado encostado não entra)
                if w_mov > 0 and zona_mov is not None:  #se estiver a mexer-se ele só aprende com os pixeis que estiverem na mascara e a mexer-se
                    m_aprender = cv2.bitwise_and(m, zona_mov * 255) 
                else:   #se estiver parado aprende apenas com os pixeis da mascara
                    m_aprender = m

                if np.count_nonzero(m_aprender) >= AREA_MIN_ALVO:
                    hist_aprendido = (1 - ALFA_MODELO) * hist_aprendido + ALFA_MODELO * criar_modelo(frame, m_aprender)
                    #Cria um histograma com as cores deste frame e mistura-o no aprendido: 15% novo, 85% do que já tinha.

                    resto_original *= (1 - ALFA_MODELO)                       # só para o ecrã
                    hist_alvo = PESO_INICIAL * hist_inicial + (1 - PESO_INICIAL) * hist_aprendido   # o original nunca abaixo de 35%
                    cv2.normalize(hist_alvo, hist_alvo, 0, 255, cv2.NORM_MINMAX)
                    #A cor mais forte volta a valer 255, para o backprojection continuar na mesma escala
                    conf0 = (1 - ALFA_MODELO) * conf0 + ALFA_MODELO * max(media, 1.0)   # a referência acompanha o modelo
        else:
            mascara_atual, centroide = np.zeros((h, w), np.uint8), None       # nada é desenhado nem entra no caminho

        # 4. caminho
        ultimo_visto = atualizar_caminho(camada_caminho, centroide, centroide_ant, ultimo_visto)    #desenha o caminho
        centroide_ant = centroide


#------FIm do tracking



    # 6. Imagem de saída conforme o modo (os desenhos são feitos numa cópia, para não afetar o processamento)
    if modo == MODO_AO_VIVO:
        saida = frame.copy()

    elif modo == MODO_SEGMENTACAO:
        saida = vista_seg.copy()

    elif modo == MODO_SELECAO:
        saida = vista_sel.copy()
        desenhar_cruz(saida, cursor_x, cursor_y)
        
    else:
        saida = frame.copy()
        tem_caminho = camada_caminho.any(axis=2)                    # píxeis onde já foi desenhado caminho
        saida[tem_caminho] = camada_caminho[tem_caminho]            # o caminho por cima do vídeo (não se usa cv2.add porque o add
                                                                    # SOMA as cores: num fundo claro o verde e o amarelo ficavam quase brancos)
        desenhar_contorno(saida, mascara_atual, VERDE)              # a fronteira da região (pedida no enunciado; só em TRACKING)
        x, y, wj, hj = janela
        cv2.rectangle(saida, (x, y), (x + wj, y + hj), CORES_ESTADOS[estado], 2)   # a janela na cor do estado
        if centroide is not None:
            cv2.circle(saida, centroide, 5, VERMELHO, -1)           # o centroide
        # o ESTADO escrito junto da janela, na cor do estado (por cima; se não houver espaço, por baixo)
        texto_estado = NOMES_ESTADOS[estado]
        if estado == EST_OCCLUDED:
            texto_estado += f" ({time.time() - t_inicio_oclusao:.1f} s)"
        (tl, th), _ = cv2.getTextSize(texto_estado, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        ty = y - 8 if y - 8 - th >= 0 else min(y + hj + th + 8, h - 5)
        tx = min(max(x, 0), w - tl - 2)
        cv2.putText(saida, texto_estado, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.6, PRETO, 4, cv2.LINE_AA)   # contorno preto
        cv2.putText(saida, texto_estado, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.6, CORES_ESTADOS[estado], 2, cv2.LINE_AA)






    # 7. Texto do FPS e informações
    if mostrar_information:
        desenhar_texto(saida, f"FPS: {fps:.1f}", 0)
        if modo != MODO_TRACKING:                                    # no tracking, o estado aparece junto da janela (passo 6)
            desenhar_texto_direita(saida, NOMES_MODOS[modo], 0, AMARELO)

        if modo == MODO_AO_VIVO:
            escrever(saida, "S -> segmentar | ESC -> sair", (10, h - 15))
        elif modo == MODO_SEGMENTACAO:
            desenhar_texto(saida, f"Regioes N (+/-): {N}", 1)
            desenhar_texto(saida, f"Peso do brilho (setas esq/dir): {peso_brilho:.1f}", 2)
            desenhar_texto(saida, f"Segmentacao: {tempo_seg:.2f} s", 3)
            escrever(saida, "S -> frame novo | Enter -> aceitar | Backspace -> voltar ao vivo", (10, h - 15))
        elif modo == MODO_SELECAO:
            area_sel = int(np.count_nonzero(mascara_sel))
            area_junt = int(np.count_nonzero(mascara_juntada))
            desenhar_texto(saida, f"Regiao {etiquetas[cursor_y, cursor_x]} | mancha: {area_sel} px | alvo: {area_junt} px", 1)
            if max(area_sel, area_junt) < AREA_MIN_ALVO:   # nada com tamanho suficiente para ser o alvo
                desenhar_texto(saida, "Mancha demasiado pequena para ser o alvo", 2, VERMELHO)
            escrever(saida, "A -> juntar | X -> tirar | C -> limpar", (10, h - 40))
            escrever(saida, "Setas -> mover | Enter -> confirmar | Backspace -> voltar", (10, h - 15))
        elif modo == MODO_TRACKING:
            desenhar_texto(saida, f"Confianca: {confianca:.2f} | T_SIM (setas cima/baixo): {t_sim:.2f}", 1)
            desenhar_texto(saida, f"Area: {100 * area_alvo / max(area0, 1):.0f}% da inicial | {100 * area_alvo / max(area_ref, 1):.0f}% da referencia", 2)
            desenhar_texto(saida, f"Limiar prob. (setas esq/dir): {limiar_prob} | movimento (F): {'ON' if usar_movimento else 'OFF'} w={w_mov:.2f}", 3)
            desenhar_texto(saida, f"T_OCC (O/P): {t_occ:.1f} s | cor fiavel: S>={s_min} (K/L) V>={v_min} (N/M) | aprender (U): {'ON' if aprender else 'OFF'}", 4)
            if estado != EST_TRACKING:                              # porquê não recupera: o melhor candidato e o que precisava
                if melhor_cand is None:
                    desenhar_texto(saida, f"Candidatos: {n_cand} (nenhum com alvo)", 5, AMARELO)
                else:
                    desenhar_texto(saida, f"Melhor candidato: conf {melhor_cand[0]:.2f} (precisa {t_sim + MARGEM_RECUPERAR:.2f})"
                                          f" | area {100 * melhor_cand[1]:.0f}% (precisa {100 * AREA_RECUPERAR_REL:.0f}%)", 5, AMARELO)
            escrever(saida, "D -> mapa | C -> apagar caminho | R -> reset", (10, h - 15))





    # 8. Gravação do vídeo (grava a imagem principal tal como aparece no ecrã, em 640x480)
    if out is None and n_medicoes_fps >= 2:   # só cria o ficheiro com um FPS fiável (a 1.ª medição inclui o atraso da ligação à câmara)
        PASTA.mkdir(parents=True, exist_ok=True)                  # cria a pasta, se ainda não existir
        fourcc = cv2.VideoWriter_fourcc(*'XVID')                   # codec [alternativa: (*'MJPG')]
        out = cv2.VideoWriter(str(FICHEIRO), fourcc, fps, (w, h))  # FPS medido e (largura, altura) da imagem de saída
        if out.isOpened():
            print(f"A gravar em {FICHEIRO} a {fps:.1f} fps")
        else:
            print("Não foi possível criar o ficheiro de vídeo:", FICHEIRO)
    if out is not None and out.isOpened() and saida.shape[:2] == (h, w):
        out.write(saida)





    # 9. Mostrar
    cv2.imshow(Janela_principal, saida)
    if mostrar_prob and modo == MODO_TRACKING:
        # janela do D: o mapa (branco = cor parecida com a do alvo) + os valores para perceber porque segue ou perde o alvo
        vista_prob = cv2.cvtColor(prob, cv2.COLOR_GRAY2BGR)
        desenhar_texto(vista_prob, f"Estado: {NOMES_ESTADOS[estado]}", 0, CORES_ESTADOS[estado])
        desenhar_texto(vista_prob, f"Confianca: {confianca:.2f} (ficar {t_sim:.2f} | voltar {t_sim + MARGEM_RECUPERAR:.2f})", 1)
        desenhar_texto(vista_prob, f"Area: {100 * area_alvo / max(area0, 1):.0f}% inicial | {100 * area_alvo / max(area_ref, 1):.0f}% referencia", 2)
        desenhar_texto(vista_prob, f"Modelo original: {100 * (PESO_INICIAL + (1 - PESO_INICIAL) * resto_original):.0f}% (minimo {100 * PESO_INICIAL:.0f}%)"
                                   f" | aprender: {'ON' if aprender else 'OFF'}", 3)
        desenhar_texto(vista_prob, f"Movimento: {'ON' if usar_movimento else 'OFF'} w={w_mov:.2f}", 4)
        if estado != EST_TRACKING:
            if melhor_cand is None:
                desenhar_texto(vista_prob, f"Candidatos: {n_cand} (nenhum com alvo)", 5, AMARELO)
            else:
                desenhar_texto(vista_prob, f"Candidato: conf {melhor_cand[0]:.2f} (precisa {t_sim + MARGEM_RECUPERAR:.2f})", 5, AMARELO)
                desenhar_texto(vista_prob, f"           area {100 * melhor_cand[1]:.0f}% (precisa {100 * AREA_RECUPERAR_REL:.0f}%)", 6, AMARELO)
            if motivo_rejeicao:
                desenhar_texto(vista_prob, f"Recusado: {motivo_rejeicao}", 7, VERMELHO)
        if mostrar_prob == 2 and fluxo_mov is not None:     # 2.º toque no D: os vetores do Farneback e os valores do movimento
            vista_prob[zona_mov > 0] = (vista_prob[zona_mov > 0] * 0.5 + np.array((80, 0, 80)) * 0.5).astype(np.uint8)   # zona a roxo
            desenhar_vetores(vista_prob, fluxo_mov)
            hv = vista_prob.shape[0]
            escrever(vista_prob, f"Deslocamento (px por frame): max {magnitude_mov.max():.1f} | medio {magnitude_mov.mean():.2f}"
                                 f" | limiar {FARNEBACK_LIMIAR:.1f}", (10, hv - 65), AMARELO)
            escrever(vista_prob, f"Zona de movimento: {100 * zona_mov.mean():.0f}% da imagem (acima de {100 * FRACAO_MOV_GLOBAL:.0f}% = camara, ignorado)",
                     (10, hv - 42), AMARELO)
            txt_cand = f"{100 * mov_candidato:.0f}% (precisa {100 * MOV_MIN_LONGE:.0f}%)" if mov_candidato is not None else "-"
            escrever(vista_prob, f"Peso w = {w_mov:.2f} (max {PESO_MOVIMENTO_MAX:.2f}) | candidato longe a mexer-se: {txt_cand}",
                     (10, hv - 19), AMARELO)
        cv2.imshow("Probabilidade (backprojection)", vista_prob)





    # 10. Teclado
    key = cv2.waitKeyEx(1)      # waitKeyEx devolve o código completo da tecla (necessário para as setas)
    tecla = key & 0xFF          # para as teclas normais (letras, números, ESC) basta o primeiro byte

    if tecla == 27:                        # ESC para sair
        break
    elif tecla == ord('1'):                # tecla 1: mostra/esconde o FPS e as informações
        mostrar_information = not mostrar_information

    elif modo == MODO_AO_VIVO:
        if tecla in (ord('s'), ord('S')):  # S: congela o frame atual e segmenta-o
            frame_congelado = frame.copy()
            precisa_segmentar = True
            modo = MODO_SEGMENTACAO



    elif modo == MODO_SEGMENTACAO:
        if tecla in (ord('s'), ord('S')):                  # S outra vez: congela um frame MAIS RECENTE e segmenta-o (mantém o N e o peso)
            frame_congelado = frame.copy()
            precisa_segmentar = True

        elif tecla == ord('+') or key in SETA_CIMA:        # mais regiões (volta a segmentar o MESMO frame)
            N = min(N + 1, N_MAX)
            precisa_segmentar = True

        elif tecla == ord('-') or key in SETA_BAIXO:       # menos regiões
            N = max(N - 1, N_MIN)
            precisa_segmentar = True

        elif key in SETA_DIREITA:                          # o brilho passa a contar mais
            peso_brilho = min(round(peso_brilho + PASSO_PESO_BRILHO, 1), PESO_BRILHO_MAX)
            precisa_segmentar = True

        elif key in SETA_ESQUERDA:                         # o brilho passa a contar menos (sombras partem menos os objetos)
            peso_brilho = max(round(peso_brilho - PASSO_PESO_BRILHO, 1), PESO_BRILHO_MIN)
            precisa_segmentar = True

        elif tecla in TECLA_ENTER:                         # aceitar a segmentação -> escolher a região
            cursor_x, cursor_y = w // 2, h // 2            # a cruz começa no centro (é normalmente onde está o objeto)
            mancha_bruta = None                            # obriga a calcular a mancha (a segmentação pode ter mudado)
            mascara_juntada = np.zeros((h, w), np.uint8)   # o alvo começa vazio
            precisa_selecao = True
            modo = MODO_SELECAO

        elif tecla == TECLA_BACKSPACE:                     # voltar ao vivo (para tirar outro frame)
            modo = MODO_AO_VIVO



    elif modo == MODO_SELECAO:
        if key in SETA_CIMA:                               # mover a cruz (sem sair da imagem)
            cursor_y = max(cursor_y - PASSO_CURSOR, 0)
            precisa_selecao = True

        elif key in SETA_BAIXO:
            cursor_y = min(cursor_y + PASSO_CURSOR, h - 1)
            precisa_selecao = True

        elif key in SETA_ESQUERDA:
            cursor_x = max(cursor_x - PASSO_CURSOR, 0)
            precisa_selecao = True

        elif key in SETA_DIREITA:
            cursor_x = min(cursor_x + PASSO_CURSOR, w - 1)
            precisa_selecao = True

        elif tecla in (ord('a'), ord('A')):                # juntar ao alvo a mancha debaixo da cruz
            mascara_juntada = cv2.bitwise_or(mascara_juntada, mascara_sel)
            precisa_selecao = True

        elif tecla in (ord('x'), ord('X')):                # tirar do alvo a mancha debaixo da cruz
            mascara_juntada = cv2.bitwise_and(mascara_juntada, cv2.bitwise_not(mascara_sel))
            precisa_selecao = True

        elif tecla in (ord('c'), ord('C')):                # limpar o alvo
            mascara_juntada[:] = 0
            precisa_selecao = True

        elif tecla in TECLA_ENTER:                         # confirmar o alvo -> tracking
            if np.count_nonzero(mascara_juntada) > 0:      # alvo com varias manchas
                alvo = mascara_juntada
            else:                                          # alvo apenas com uma mancha (mancha original)
                alvo = mascara_sel

            if np.count_nonzero(alvo) >= AREA_MIN_ALVO:
                mascara_alvo = alvo.copy()  #copia do alvo
                hist_alvo = criar_modelo(frame_congelado, mascara_alvo)   # modelo de cor do alvo (fase 4)

                hist_inicial, hist_aprendido = hist_alvo.copy(), hist_alvo.copy()   # a parte fixa e a parte que aprende dos histogramas começam iguais
                resto_original = 1.0                                      # no início o modelo é 100% o original
                janela = retangulo_da_mascara(mascara_alvo)               # determina o retangulo que cobre os valores brancos da mascara_alvo
                tamanho_inicial = (max(janela[2], JANELA_MIN), max(janela[3], JANELA_MIN))   # guardado para a procura na imagem toda
                janela_max = (max(int(janela[2] * JANELA_ESCALA_MAX), JANELA_MIN), max(int(janela[3] * JANELA_ESCALA_MAX), JANELA_MIN))
                #define o tamanho maximo que a janela pode ter durante tracking, neste caso x3
                
                prob0 = backprojection(frame_congelado, hist_alvo)  #cria o mapa de probabilidade original
                m0, centroide, area0, _ = medir(prob0, janela, limiar_prob) #calcula a area inicial, o centroide, e a mascara alvo (junção do mapa com as cores)

                if area0 == 0:                                            # o alvo não tem cor fiável suficiente: usa a máscara escolhida
                    m0 = mascara_alvo
                    centroide, area0 = centroide_e_area(mascara_alvo)
                janela = ajustar_janela(janela, m0, centroide, w, h, janela_max)   # a janela com o tamanho que o tracking vai usar...
                _, _, _, conf0 = medir(prob0, janela, limiar_prob)                #confiança media medida inicialna seleção do objeto

                if conf0 < 1.0:                                           # a medição falhou: usa a probabilidade média dos píxeis escolhidos
                    conf0 = max(float(prob0[mascara_alvo > 0].mean()), 1.0)

                area_ref = area0                                          # a referência da área começa na área inicial
                estado = EST_TRACKING
                camada_caminho = np.zeros((h, w, 3), np.uint8)            # caminho novo, vazio (fase 5)
                centroide_ant = centroide                                 # o caminho começa no centroide do alvo escolhido
                ultimo_visto = centroide
                cinz_ant = None                                           # o Farneback recomeça (não compara com um frame antigo)
                modo = MODO_TRACKING


        elif tecla == TECLA_BACKSPACE:                     # voltar à segmentação
            modo = MODO_SEGMENTACAO

    elif modo == MODO_TRACKING:
        if key in SETA_DIREITA:                            # limiar mais alto: a máscara do alvo fica mais "exigente" (menor)
            limiar_prob = min(limiar_prob + PASSO_LIMIAR_PROB, LIMIAR_PROB_MAX)

        elif key in SETA_ESQUERDA:                         # limiar mais baixo: entram mais píxeis (pode apanhar fundo)
            limiar_prob = max(limiar_prob - PASSO_LIMIAR_PROB, LIMIAR_PROB_MIN)

        elif key in SETA_CIMA:                             # T_SIM mais alto: mais exigente (dá OCCLUDED mais depressa)
            t_sim = min(round(t_sim + PASSO_T_SIM, 2), T_SIM_MAX)

        elif key in SETA_BAIXO:                            # T_SIM mais baixo: mais tolerante (arrisca seguir a coisa errada)
            t_sim = max(round(t_sim - PASSO_T_SIM, 2), T_SIM_MIN)

        elif tecla in (ord('f'), ord('F')):                # liga/desliga a zona de movimento (Farneback)
            usar_movimento = not usar_movimento

        elif tecla in (ord('u'), ord('U')):                # liga/desliga a aprendizagem do modelo
            aprender = not aprender

        elif tecla in (ord('k'), ord('K')):                # saturação mínima da cor fiável: menos (aceita cores mais desbotadas)
            s_min = max(s_min - PASSO_SV, 0)

        elif tecla in (ord('l'), ord('L')):                # mais (só cores vivas: tira o preto/cinzento ligeiramente colorido)
            s_min = min(s_min + PASSO_SV, 250)

        elif tecla in (ord('n'), ord('N')):                # brilho mínimo da cor fiável: menos
            v_min = max(v_min - PASSO_SV, 0)

        elif tecla in (ord('m'), ord('M')):                # mais (tira as zonas escuras)
            v_min = min(v_min + PASSO_SV, 250)

        elif tecla in (ord('o'), ord('O')):                # menos tempo em OCCLUDED até LOST
            t_occ = max(t_occ - PASSO_T_OCC, T_OCC_MIN)

        elif tecla in (ord('p'), ord('P')):                # mais tempo em OCCLUDED até LOST
            t_occ = min(t_occ + PASSO_T_OCC, T_OCC_MAX)

        elif tecla in (ord('d'), ord('D')):                # D: fechada -> mapa -> mapa + vetores -> fechada
            mostrar_prob = (mostrar_prob + 1) % 3
            if mostrar_prob == 0:
                cv2.destroyWindow("Probabilidade (backprojection)")

        elif tecla in (ord('c'), ord('C')):                # apagar só o caminho (o tracking continua)
            camada_caminho[:] = 0
        elif tecla in (ord('r'), ord('R')):                # reset: volta ao vídeo ao vivo para escolher outro alvo (o caminho é apagado)
            mascara_alvo = None
            camada_caminho = None
            if mostrar_prob:
                cv2.destroyWindow("Probabilidade (backprojection)")
                mostrar_prob = 0
            modo = MODO_AO_VIVO



if out is not None:        # fecha o ficheiro de vídeo (sem isto o vídeo pode ficar corrompido)
    out.release()
    print("Gravação terminada:", FICHEIRO)
cap.release()
cv2.destroyAllWindows()

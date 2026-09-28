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
from pathlib import Path

""" Necessidades no projeto
Câmara estática no teto, vídeo em direto, com uma grelha 5x5 sobreposta em todas as frames.

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

#-----------------
#Parametros para a deteção de movimento
BLUR_KSIZE = 7         # tamanho do kernel do desfoque gaussiano (7×7). escolhido por tentativa, poderado o 7x7 e 5x5 pois eram os que fazim mais efeito
MEDIAN_KSIZE = 5       # tamanho da janela do filtro de mediana aplicado à máscara (5×5).  -> serve para limpar ruido nos pixeis de movimento, isto depois do threshold
Sensibilidade_Movimento = 25            # Valor de Sensibilidade [ajustável]: diferença mínima (0-255) para um píxel cinzento contar como movimento

#-----------------
#Parametros para a decisão por célula (etapa 3)
AREA_MINIMA = 0.01     # precentagem mínima da célula (0.02 = 2%) [ajustável]: permitie eliminar ruido dentro de cada celula
GLOBAL_CELLS = 15      # impede que varias celula disparem ao mesmo tempo

#-----------------
#Parametros para o contágio (etapa 5)
PERSIST_FRAMES = 3     # nº de frames seguidas com movimento para uma célula poder ser ativada 

#-----------------
#Parametros para o reset (etapa 6)
RESET_SEGUNDOS = 10.0  # [ajustável] tempo sem qualquer movimento na imagem até o contágio ser apagado

#-----------------
#Parametros para a gravação de vídeo
PASTA = Path(r"C:\Users\JP\Documents\Visao_computacional\Imagens_OpenCV\Videos")
FICHEIRO = PASTA / "Trabalho_1.avi"    # cada execução do programa substitui o ficheiro anterior

#-----------------
#Cores (BGR)--> apenas é utilizado para colocar coisas á frente da janela
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)      # píxeis com movimento na vista cinzento + deteção (tecla 2)
VERMELHO = (0, 0, 255)

#-----------------
#Códigos das setas do teclado (devolvidos pelo cv2.waitKeyEx; mudam conforme o sistema operativo)
#                 Windows    Linux 
SETA_CIMA     = (2490368,   65362,)
SETA_BAIXO    = (2621440,   65364,)
SETA_ESQUERDA = (2424832,   65361,)
SETA_DIREITA  = (2555904,   65363,)

TECLAS = """
---------------- Teclas ----------------
  ESC            sair
  1              mostrar/esconder FPS, celulas ativas, limiar e area minima
  2              janela da mascara: abrir -> cinzento + detecao -> fechar
  3              mostrar/esconder as percentagens em cada celula
  4              mostrar/esconder o aviso de mudanca global de luz
  C              reset manual do contagio (apaga todas as celulas ativas)
  R  /  T        intervalo de reset menor / maior (1 s)
  Seta baixo     mais sensivel   (limiar -5)
  Seta cima      menos sensivel  (limiar +5)
  Seta direita   area minima maior (+0.5%)
  Seta esquerda  area minima menor (-0.5%)
  (as teclas so funcionam com uma janela do programa selecionada)
  (o video da janela principal e gravado automaticamente)
-----------------------------------------
"""

fps = 0.0
contador = 0 #contador de frames em x tempo
T_inicio = time.time()
dt_atualizacao_fps = 0.5    
n_medicoes_fps = 0     #nº de medições de FPS já feitas (a primeira é descartada para a gravação)
primeira_frame = True   #apenas variavel temporaria para o programa
mostrar_information = True  #variavel para permitir mostrar os valores no monitor
modo_mascara = 0                #janela da mascara: 0 = fechada, 1 = mascara (preto/branco), 2 = cinzento + deteção a verde
mostrar_percentagens = False    #para ativar e desativar a percentagem de movimento escrita em cada célula
mostrar_aviso_global = False     #para ativar e desativar o aviso de mudança global de luz
limiar = Sensibilidade_Movimento
area_min = AREA_MINIMA
anterior = None        # frame anterior (já em cinzento e desfocada)

ativas = np.zeros((GRID_N, GRID_N), bool)    # matrix das células ativas (em negativo) - True/False por célula
persist = np.zeros((GRID_N, GRID_N), int)    # matrix das frames seguidas com movimento em cada célula
semente = None                               # (linha, coluna) da primeira célula ativada

intervalo_reset = RESET_SEGUNDOS             # intervalo de reset em uso (alterado pelas teclas R e T)
ultimo_movimento = time.time()               # instante do último movimento válido em qualquer célula

out = None             # objeto VideoWriter (criado logo que o FPS é medido pela primeira vez)





#---------------------------
#Funções

def redimensionar(frame, largura_max):
    """Reduz a frame para largura_max, mantendo a proporção de 16:9 ou 4:3. para ter-se uma resolução de 640x480 ou 640x430"""
    #Primeiro Passo é Redimensionar a imagem para manter a proporção correta (apenas um sistema de segurança)
    h, w = frame.shape[:2]
    if w > largura_max: #Se a largura for maior que 640, é redimensionada para manter a largura de 640px
        frame = cv2.resize(frame, (largura_max, int(h * largura_max / w)), interpolation=cv2.INTER_AREA)
    return frame


def preprocessar(frame, kernnel_size):     #convertemos o frame em b&w e depois desfocamos, para preparar para a deteção de movimento
    """BGR -> cinzento -> desfoque gaussiano (reduz o ruído do sensor e da compressão)."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gray, (kernnel_size, kernnel_size), 0) #O 0 é o sigma, que define a força do desfoque
    #o desfoque irá ajudar mais tarde a limitar a quantidade de pontos diferentes entre dois frames seguintes


def mascara_movimento(atual, anterior, limiar, ksize_mediana):
    """Máscara binária (0/255) dos píxeis que mudaram entre duas frames."""
    # Diferença com sinal: dst = 1 * atual + (-1) * anterior + 0
    # dtype=CV_32F faz a saída ser decimal com sinal, para não perder os negativos
    diff = cv2.addWeighted(atual, 1, anterior, -1, 0, dtype=cv2.CV_32F)
    diff_abs = np.abs(diff).astype(np.uint8) # Valor absoluto: apenas serve para retiar o sinal negativo dos valores

            # não utilizei o bitwise_xor pois gerava ruido (estas operações são boas para valores de extremo)
          
        
    _, mask = cv2.threshold(diff_abs, limiar, 255, cv2.THRESH_BINARY) # Limiar: acima de 'limiar' -> 255 (mudou), caso contrário -> 0
    
    return cv2.medianBlur(mask, ksize_mediana)# Mediana: elimina píxeis brancos isolados (ruído que passou o limiar)
                                            #pois queremos apenas  aglomerado de pontos brancos (movimento)


def limites_grelha(h, w, n):    # -> Coordenadas das fronteiras das células de uma grelha n x n.
    ys = [round(i * h / n) for i in range(n + 1)]
    xs = [round(j * w / n) for j in range(n + 1)]     #estas funções servem para determinar as coordenadas de cada divisão da imagem
                                                      # para gerar a grelha de 5x5 - se for preciso alterar o tamanho da grelha é só mudar GRID_N
                                                      #i	i × 480 / 5	ys
                                                      #0	0	0
                                                      #1	96	96
                                                      #2	192	192
                                                      #3	288	288
                                                      #4	384	384
                                                      #5	480	480
    return ys, xs


def fracao_por_celula(mask, ys, xs, n): #com esta função separamos a frame em realmente varias celula, é o principio para depois a grelha 5x5 funcionar corretamente
    frac = np.zeros((n, n)) #criação de uma matrix de 5x5 de zeros(neste caso)
    for i in range(n):          # i = linha da grelha
        for j in range(n):      # j = coluna da grelha
            celula = mask[ys[i]:ys[i + 1], xs[j]:xs[j + 1]]     # recorte a celula com as posições definidas em limites_grelha
            frac[i, j] = np.count_nonzero(celula) / celula.size  # preenxe a matrix de 5x5, com valor de precentagem dos píxeis brancos 
                                                                #essa precentagem é achada, contando a quantidade de pixeis brancos e depois divide pelo numero total de ponto por celula
    return frac


def decidir_movimento(frac, area_min, global_cells):    #Decide que células têm movimento validp 

    movimento = frac >= area_min                    # comparação com a percentagem minima de pontos brancos por celula
    mudanca_global = movimento.sum() >= global_cells  # demasiadas células ao mesmo tempo -> não é uma pessoa, é a luz/exposição
    if mudanca_global:
        movimento[:] = False                        # ignora a frame inteira: nenhuma célula conta como movimento
    return movimento, mudanca_global    #movimento é uma matrix 5x5 com as confirmações de movimentos


def celulas_elegiveis(ativas): # verifica se há pelo menos uma célula ativa na janela 3×3 à volta de cada celula inativa    
                                #devolver uma matriz 5×5 com True nas células que podem ser ativadas na próxima vez que tiverem movimento, e False nas restantes.

    n = ativas.shape[0] #apenas para ler o tamanho da grelha
    elegiveis = np.zeros_like(ativas)       # cria uma matrix n x n a zeros, contudo é utilizado este metodo, para ter as mesmas caracteristicas que a matrix ativas
    if not ativas.any():                    # ainda sem semente: todas as células são elegíveis
        elegiveis[:] = True     #poem as 25 celulas a true (que podem ser ativadas a qualquer segundo) apenas caso ainda não exista ainda uma semnete definida
        return elegiveis
    
    for i in range(n):
        for j in range(n):
            if not ativas[i, j]:     # caso uma célula já esteja ativa não precisa de ser elegível, por isso salta os 3 passos seguintes passa para a proxima celula
                #Calcula os limites da janela à volta da célula: uma linha acima até uma abaixo, e uma coluna à esquerda até uma à direita
                i0, i1 = max(i - 1, 0), min(i + 2, n)     # linhas vizinhas (sem sair da grelha)
                j0, j1 = max(j - 1, 0), min(j + 2, n)     # colunas vizinhas (sem sair da grelha) (é definido j+2 para incluir o limite e o valor a seguir a ele)
                                                          #pois a posição da celula, (a:b) o b não está incluido, é o mesmo que nos limites
                elegiveis[i, j] = ativas[i0:i1, j0:j1].any()   # analisa para ver se existe algum vizinho ativo na janela 3x3     
    return elegiveis


def atualizar_contagio(ativas, confirmadas, frac, elegiveis, semente):  #Recebe o estado atual e decide que células passam a estar ativas nesta frame. Os argumentos são
    if not ativas.any():    # Ainda não há semente: a célula confirmada com mais movimento torna-se a semente
        
        if confirmadas.any():
            idx = np.argmax(np.where(confirmadas, frac, -1))   # Compara as matrixes confirmadas e frac e sobrepõem uma a outra
            semente = divmod(int(idx), ativas.shape[0])       # converte a posição em (linha, coluna), pois o np.argmax, devolve a posição seguida, linha a linha
            ativas[semente] = True
            #este sistema cerve como filtro também pois ele precisa da confirmação que tem muito movimento 
            # e que esse movimento foi consistente, nos ultimos 3 frames
    else:
        # Caso já exista semente: só se ativam células com movimento confirmado E elegíveis (vizinhas de uma ativa)
        ativas |= confirmadas & elegiveis
        # O |= acrescenta células às que já estão ativas, sem apagar nenhuma
    return ativas, semente


def limpar_contagio(ativas, persist):
    """Apaga todas as células ativas e a persistência. Devolve a nova semente (None)."""
    ativas[:] = False       # nenhuma célula ativa: a grelha volta toda ao normal
    persist[:] = 0          # recomeça a contagem de frames seguidas em todas as células
    return None             # deixa de haver semente: o próximo movimento escolhe uma nova




#--------------------------
#   Dezenhos das informações na janela

def aplicar_negativo(saida, frame, celulas, ys, xs):
    """Nas células marcadas a True, substitui o conteúdo da saída pelo negativo da frame original (ao vivo)."""
    n = celulas.shape[0]
    for i in range(n):
        for j in range(n):
            if celulas[i, j]:
                y0, y1 = ys[i], ys[i + 1]
                x0, x1 = xs[j], xs[j + 1]
                saida[y0:y1, x0:x1] = cv2.bitwise_not(frame[y0:y1, x0:x1])   # negativo = 255 - valor (slide 56)
                # lê da frame original e escreve na saída: a deteção nunca vê a imagem invertida


def desenhar_grelha(img, ys, xs):
    """Desenha as linhas interiores da grelha (sem as bordas da imagem)."""
    h, w = img.shape[:2]
    for y in ys[1:-1]:      #as linhas serão geradas, menos no primeiro e no ultimo setor
        linha = np.array([[0, y], [w - 1, y]], np.int32)
        cv2.polylines(img, [linha], False, BRANCO, 1)
    for x in xs[1:-1]:
        linha = np.array([[x, 0], [x, h - 1]], np.int32)
        cv2.polylines(img, [linha], False, BRANCO, 1)


def escrever(img, texto, pos, cor=BRANCO, escala=0.6):
    """Escreve texto na posição pos (contorno preto + texto na cor pedida, legível sobre qualquer fundo)."""
    cv2.putText(img, texto, pos, cv2.FONT_HERSHEY_SIMPLEX, escala, PRETO, 3)
    cv2.putText(img, texto, pos, cv2.FONT_HERSHEY_SIMPLEX, escala, cor, 1)

    #Argumento	            Valor	            Significado
    #imagem	                img	                onde escrever
    #texto	                texto	            o que escrever
    #posição	           pos	                canto inferior esquerdo do texto, em (x, y): 10 píxeis da esquerda, 25 do topo (+22 por cada linha)
    #fonte	          FONT_HERSHEY_SIMPLEX	    o tipo de letra
    #escala	                 0.6	            o tamanho do texto
    #cor	   (0, 0, 0) / (255, 255, 255)	    preto / branco, em BGR
    #espessura	            3 / 1	            grossura do traço, em píxeis


def desenhar_texto(img, texto, n_linha, cor=BRANCO):
    """Escreve texto no canto superior esquerdo (contorno preto + texto branco, legível sobre qualquer fundo).
    n_linha = 0 é a primeira linha, 1 a segunda, etc."""
    pos = (10, 25 + 22 * n_linha)
    escrever(img, texto, pos, cor)


def desenhar_texto_direita(img, texto, n_linha, cor=BRANCO):
    """Escreve texto alinhado ao canto superior DIREITO (mesmas linhas que o desenhar_texto).
    n_linha = 0 é a primeira linha, 1 a segunda, etc."""
    h, w = img.shape[:2]
    (largura, _), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 3)   # largura do texto em píxeis
    pos = (w - largura - 10, 25 + 22 * n_linha)    # 10 píxeis de margem à direita
    escrever(img, texto, pos, cor)


def vista_deteccao(frame, mask):
    """Imagem em cinzento com os píxeis de movimento pintados a verde (vista 2 da janela da máscara)."""
    cinzento = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    vista = cv2.cvtColor(cinzento, cv2.COLOR_GRAY2BGR)   # volta a ter 3 canais, para se poder pintar a cores
    vista[mask > 0] = VERDE                              # onde a máscara é branca (movimento), o píxel fica verde
    return vista


def desenhar_percentagens(img, frac, ys, xs):
    """Escreve, no canto inferior esquerdo de cada célula, a percentagem de píxeis com movimento."""
    n = frac.shape[0]
    for i in range(n):
        for j in range(n):
            escrever(img, f"{frac[i, j] * 100:.1f}%", (xs[j] + 6, ys[i + 1] - 8), BRANCO, 0.4)




#-------------------------
#Iniciação da camera

cap = cv2.VideoCapture(CAMERA_SRC)  #captura de video
if not cap.isOpened():
    print("Não foi possível ligar a", CAMERA_SRC)
    exit(1)

print(TECLAS)   # mensagem inicial com as teclas disponíveis

T_inicio = time.time()  # a medição do FPS começa aqui, depois de a câmara estar ligada (e não no início do programa)

while(cap.isOpened()):
    # Captura frame-a-frame
    ret, frame = cap.read()
    if not ret:
        print("Frame não Recebida!")
        break

    # 1. Redimensionar (só reduz, mantém a proporção)
    if primeira_frame:
        h, w = frame.shape[:2]
        print("Resolucao recebida:")
        print("Largura", w)
        print("Altura", h)

    frame = redimensionar(frame, LARGURA)
    h, w = frame.shape[:2]
    ys, xs = limites_grelha(h, w, GRID_N)   # fronteiras das células (usadas na deteção por célula e no desenho da grelha)

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
        n_medicoes_fps += 1



    # 3. Deteção de movimento (diferença entre frames consecutivas)
    atual = preprocessar(frame, BLUR_KSIZE)
    if anterior is None:          # primeira frame: ainda não há com que comparar
        anterior = atual
        continue
    mask = mascara_movimento(atual, anterior, limiar, MEDIAN_KSIZE)
    anterior = atual              # a frame atual passa a ser a anterior da próxima volta

    # 4. Decisão por célula (área mínima + rejeição global)
    frac = fracao_por_celula(mask, ys, xs, GRID_N)
    movimento, mudanca_global = decidir_movimento(frac, area_min, GLOBAL_CELLS)



    # 5. Contágio (persistência + semente + vizinhos)
    if movimento.any():                                # qualquer movimento válido, em QUALQUER célula (elegível ou não)
        ultimo_movimento = time.time()                 # reinicia o cronómetro do reset
    persist = np.where(movimento, persist + 1, 0)      # soma 1 onde há movimento, volta a 0 onde não há (assim conseguimos verificar onde existe movimento constante)
    confirmadas = persist >= PERSIST_FRAMES            # movimento torna-se conformado (mas não ativo) com pelo menos PERSIST_FRAMES frames seguidas (3 neste caso)
    elegiveis = celulas_elegiveis(ativas)              # função para determinar e calculada com o estado ANTERIOR, as celulas que podem contagiar (o contágio avança 1 passo por frame)
    ativas, semente = atualizar_contagio(ativas, confirmadas, frac, elegiveis, semente) #ativa finalmente a celula mais indicada para o contagio


    # 6. Reset automático (sem movimento durante intervalo_reset segundos)
    restante = intervalo_reset - (time.time() - ultimo_movimento)   # segundos que faltam para o reset
    if ativas.any() and restante <= 0:                 # só faz sentido quando há células ativas
        semente = limpar_contagio(ativas, persist)

    # 7. Imagem de saída: negativo + grelha
    saida = frame.copy() #a grelha será exposta numa copia do frame, para não interromper ou afetar a deteção de movimento
    aplicar_negativo(saida, frame, ativas, ys, xs)     # células ATIVAS em negativo (antes da grelha, para não inverter as linhas)
    desenhar_grelha(saida, ys, xs)
    if mostrar_percentagens:
        desenhar_percentagens(saida, frac, ys, xs)

    # 8. Texto do FPS, das células ativas, da contagem do reset, do limiar e da área mínima
    if mostrar_information:
        desenhar_texto(saida, f"FPS: {fps:.1f}   Celulas ativas: {int(ativas.sum())}/{GRID_N * GRID_N}", 0)
        desenhar_texto(saida, f"Limiar (setas cima/baixo): {limiar}", 1)
        desenhar_texto(saida, f"Area minima (setas esq/dir): {area_min * 100:.1f}%", 2)
        # informação do reset no canto superior direito
        desenhar_texto_direita(saida, f"Reset (r/t): {intervalo_reset:.0f}s", 0)
        if ativas.any():                               # a contagem só aparece quando há algo para apagar
            desenhar_texto_direita(saida, f"Reset em: {max(restante, 0):.1f}s", 1)
        escrever(saida, "ESC -> Sair", (10, h - 30))   # canto inferior esquerdo (acima das percentagens da última linha)
    if mostrar_aviso_global and mudanca_global:     # aviso de mudança global de luz (tecla 4 liga/desliga)
        escrever(saida, "Mudanca global de luz: frame ignorada", (10, h // 2), VERMELHO)

    # 9. Gravação do vídeo (grava a imagem principal, tal como aparece no ecrã)
    if out is None and n_medicoes_fps >= 2:   # só cria o ficheiro com um FPS fiável (a 1.ª medição inclui o atraso da ligação à câmara)
        PASTA.mkdir(parents=True, exist_ok=True)                  # cria a pasta, se ainda não existir
        # Define o codec e cria o objeto VideoWriter [alternativa: (*'MJPG')]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(str(FICHEIRO), fourcc, fps, (w, h))   # FPS medido e (largura, altura) da imagem de saída
        if out.isOpened():
            print(f"A gravar em {FICHEIRO} a {fps:.1f} fps")
        else:
            print("Não foi possível criar o ficheiro de vídeo:", FICHEIRO)
    if out is not None and out.isOpened():
        out.write(saida)

    # 10. Mostrar
    cv2.imshow("Contagion - etapa 6", saida)
    if modo_mascara == 1:
        cv2.imshow("Mascara de movimento", mask)                       # só a máscara (preto/branco)
    elif modo_mascara == 2:
        cv2.imshow("Mascara de movimento", vista_deteccao(frame, mask))  # cinzento + movimento a verde

    # 11. Teclado
    key = cv2.waitKeyEx(1)      # waitKeyEx devolve o código completo da tecla (necessário para as setas)
    tecla = key & 0xFF          # para as teclas normais (letras, números, ESC) basta o primeiro byte

    if key in SETA_BAIXO:                  # seta baixo: mais sensível (limiar menor)
        limiar = max(limiar - 5, 5)
    elif key in SETA_CIMA:                 # seta cima: menos sensível (limiar maior)
        limiar = min(limiar + 5, 250)
    elif key in SETA_DIREITA:              # seta direita: área mínima maior (exige mais movimento dentro da célula)
        area_min = min(round(area_min + 0.005, 3), 0.5)
    elif key in SETA_ESQUERDA:             # seta esquerda: área mínima menor (aceita movimentos mais pequenos)
        area_min = max(round(area_min - 0.005, 3), 0.005)
    elif tecla == 27:                      # ESC para sair
        break
    elif tecla == ord('1'):                # tecla 1: mostra/esconde o FPS, o limiar e a área mínima
        mostrar_information = not mostrar_information
    elif tecla == ord('2'):                # tecla 2: fechada -> máscara -> cinzento + deteção -> fechada
        modo_mascara = (modo_mascara + 1) % 3
        if modo_mascara == 0:
            cv2.destroyWindow("Mascara de movimento")
    elif tecla == ord('3'):                # tecla 3: mostra/esconde as percentagens em cada célula
        mostrar_percentagens = not mostrar_percentagens
    elif tecla == ord('4'):                # tecla 4: mostra/esconde o aviso de mudança global de luz
        mostrar_aviso_global = not mostrar_aviso_global
    elif tecla in (ord('c'), ord('C')):    # tecla C: reset manual do contágio
        semente = limpar_contagio(ativas, persist)
        ultimo_movimento = time.time()
    elif tecla in (ord('r'), ord('R')):    # tecla R: intervalo de reset menor
        intervalo_reset = max(intervalo_reset - 1, 1)
    elif tecla in (ord('t'), ord('T')):    # tecla T: intervalo de reset maior
        intervalo_reset = min(intervalo_reset + 1, 60)



if out is not None:        # fecha o ficheiro de vídeo (sem isto o vídeo pode ficar corrompido)
    out.release()
    print("Gravação terminada:", FICHEIRO)
cap.release()
cv2.destroyAllWindows()
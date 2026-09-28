#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "numpy",
#   "opencv-python",
# ]
# ///


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
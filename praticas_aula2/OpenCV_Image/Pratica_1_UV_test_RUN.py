#!uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
# "numpy",
# "opencv-python",
# "matplotlib",
# ]
# ///

#teste inicial

import sys  
import cv2  #biblioteca de visão computacional
import numpy    #biblioteca de matemática, para trabalhar com matrizes, vetores e etc
import matplotlib   #biblioteca de graficos, parecido ao matlab
print("python: ", sys.version)      #comando para verificar a versão das bibliotecas, 
                                    #é o mesmo que escrever np cmd python --version
print("numpy: ", numpy.__version__)
print("matplotlib: ", matplotlib.__version__)
print("CV :", cv2.__version__)



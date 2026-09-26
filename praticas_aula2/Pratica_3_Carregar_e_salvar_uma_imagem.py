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
#Color
#img1 = cv2.imread('Lena.png',cv2.IMREAD_COLOR)

#Gray
#img2 = cv2.imread('Lena.png',cv2.IMREAD_GRAYSCALE)


# Load an color image in grayscale
#img = cv2.imread('D:\OneDrivePess\OneDrive\/2_CODE\Imgs4CV\imgs\lena.jpg',cv2.IMREAD_COLOR)

#cv2.imshow() #mostra a imagem numa janela
#cv2.waitKey() #espera por uma tecla, para sair do modo de espera 
#cv2.destroyAllWindows() 
#imag = cv2.imread('lena.jpg')


pasta = Path(r"C:\Users\JP\Documents\Visao_computacional\Imagens_OpenCV\Aula_2")
img_path = pasta / "Imagem_modelo.jpg"

img = cv2.imread(str(img_path), cv2.IMREAD_COLOR) #leitura da imagem a cores, no seguinte path 
                                                    # a preto e branco utilizar: cv2.IMREAD_GRAYSCALE
                                                    # a cores utilizar: cv2.IMREAD_COLOR
#imagem a cores vem em bgr em vez de rgb 
if img is None:
    print("Image not found:", img_path) #caso dei-a sai do programa
    exit()
#cv2.imshow('image1',img)

 # if you want to resize the window      
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # converte cor -> cinzento

# save an color image in grayscale
output_dir = pasta / "output"
#output_dir.mkdir(exist_ok=True)            # cria a pasta Aula_2\output se não existir
output_path = output_dir / "ImagemGravada.jpg"
saved = cv2.imwrite(str(output_path), img) #guardado a imagem a cores no path 

output_path = output_dir / "ImagemGravada_gray.jpg"
saved = cv2.imwrite(str(output_path), img_gray)    #guardado a imagem a b&w no path


if not saved or not output_path.exists():
    print('Failed to save image')
#print("Gravada em:", output_path if saved else "FALHOU")
else:
    print("Imagem gravada com sucesso!")
    print("Gravada em:", output_path)

    
cv2.waitKey(0)
cv2.destroyAllWindows()


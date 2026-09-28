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

PASTA = Path(r"C:\Users\JP\Documents\Visao_computacional\Imagens_OpenCV\Videos")
FICHEIRO = PASTA / "teste.avi"

#cap = cv2.VideoCapture(0)
# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Unable to read camera feed")
    exit (1) #exit with problem; exit (0) - exit ok
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# Define the codec and create VideoWriter object [(*'MJPG')]
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(str(FICHEIRO), fourcc, 20.0, (frame_width, frame_height))


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #flip the image from the camera
        frame = cv2.flip(frame,0)
        # write the flipped frame
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
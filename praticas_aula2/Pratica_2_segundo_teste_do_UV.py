#!uv run
# /// script
# requires-python = "==3.12.*"
# dependencies = [
# "mediapipe==0.10.20",
# "opencv-python>=4.10.0.84",
# ]
# ///
import cv2      #biblioteca de visão computacional
import mediapipe as mp      #biblioteca da Google com modelos de IA já treinados, 
                            #para permitir receber imagens do OpenCV e devolver coordenadas e informação
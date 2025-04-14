from playsound import playsound
import os

def speak(text):
    print("Roonie:", text)
    caminho = os.path.join(os.getcwd(), "voz.mp3")
    if os.path.exists(caminho):
        playsound(caminho)
    else:
        print("Arquivo voz.mp3 não encontrado.")

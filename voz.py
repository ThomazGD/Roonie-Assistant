from gtts import gTTS
import pygame
import time
import os

def speak(texto):
    try:
        tts = gTTS(texto, lang='pt')
        filename = "voz.mp3"
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # Espera o áudio acabar
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.quit()
        os.remove(filename)

    except Exception as e:
        print("Erro ao reproduzir áudio:", e)

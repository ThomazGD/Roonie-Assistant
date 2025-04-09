# Em desenvolvimento
import sounddevice as sd
import queue
import vosk
import json
import os

q = queue.Queue()

# Caminho do modelo VOSK (ajuste se estiver diferente)
model_path = os.path.join("resources", "vosk-model", "vosk-model-small-pt-0.3")
model = vosk.Model(model_path)

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen_and_recognize():
    print("🎧 Escutando... fale algo:")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    return text

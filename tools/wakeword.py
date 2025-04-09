import speech_recognition as sr

def listen_for_wakeword(wake_word="acorde roonie"):
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8  # pequena pausa entre as palavras
    with sr.Microphone() as source:
        print("Aguardando a palavra de ativação...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="pt-BR").lower()
        print("Você disse:", command)  # 👈 ajuda a saber o que foi captado
        if wake_word.lower() in command:
            return True
    except sr.UnknownValueError:
        print("Não entendi o que foi dito.")
    except sr.RequestError:
        print("Erro ao conectar com o serviço de reconhecimento.")
    return False

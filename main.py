import pyttsx3
import speech_recognition as sr
from tools.browser import search_google
from tools.apps import open_app
from tools.time_utils import get_time, get_date
from tools.notes import save_note, read_notes
from tools.wakeword import listen_for_wakeword
import time
import json
from datetime import datetime
import os

# Iniciar engine de voz
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Maria

def speak(text):
    print("Roonie:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escutando comando...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="pt-BR").lower()
        print("Você disse:", command)
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Erro ao conectar com o serviço.")
    return ""

def registrar_log(acao, conteudo, resultado="sucesso", arquivo='memory/log.json'):
    entrada = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "acao": acao,
        "conteudo": conteudo,
        "resultado": resultado
    }

    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(entrada)

    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

def handle_command(command):
    if "pesquisar" in command:
        speak("O que você quer que eu pesquise?")
        query = ""
        tentativas = 0

        while not query and tentativas < 2:
            query = listen()
            tentativas += 1

        if query:
            speak(f"Pesquisando por {query}")
            registrar_log("pesquisar", query)
            search_google(query)
        else:
            speak("Desculpe, não consegui entender o que você quer pesquisar.")
            registrar_log("pesquisar", "", "falha")

    elif "abrir" in command:
        while True:
            app_name = command.replace("abrir", "").strip()
            if not app_name:
                speak("Qual aplicativo você quer abrir?")
                app_name = listen()

            resposta = open_app(app_name)
            speak(resposta)
            registrar_log("abrir", app_name, "sucesso" if "Abrindo" in resposta else "falha")

            if "não foi possível encontrar" in resposta.lower():
                speak("Qual aplicativo você quer abrir?")
                command = listen()
                if not command:
                    speak("Não entendi o aplicativo.")
                    break
            else:
                break

    elif "horas" in command or "hora" in command:
        hora = get_time()
        speak(f"Agora são {hora}")
        registrar_log("hora", hora)

    elif "dia" in command or "data" in command:
        data = get_date()
        speak(f"Hoje é {data}")
        registrar_log("data", data)

    elif "anotar" in command:
        nota = command.replace("anotar", "").strip()
        resposta = save_note(nota)
        speak(resposta)
        registrar_log("anotar", nota)

    elif "ler anotações" in command:
        anotações = read_notes()
        speak("Suas anotações são:")
        print(anotações)
        speak(anotações)
        registrar_log("ler anotações", anotações)

    elif "encerrar" in command or "tchau roonie" in command:
        speak("Até logo! Encerrando o assistente.")
        registrar_log("encerrar", "Roonie desligado")
        exit()

    else:
        speak("Não entendi o comando.")
        registrar_log("comando desconhecido", command, "falha")

speak("Roonie está pronto. Diga 'Acorde' para ativar.")

# Aguarda uma vez só e permanece acordado depois
while True:
    if listen_for_wakeword("acorde"):
        speak("Estou ouvindo, diga o comando.")
        while True:
            comando = listen()
            if comando:
                handle_command(comando)
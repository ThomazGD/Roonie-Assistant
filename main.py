import pyttsx3
import speech_recognition as sr
from tools.browser import search_google, search_youtube
from tools.apps import open_app, fechar_app
from tools.time_utils import get_time, get_date
from tools.notes import save_note, read_notes
from tools.wakeword import listen_for_wakeword
import time
import json
from datetime import datetime
import os
import webbrowser  # para abrir URLs no navegador

# Iniciar engine de voz
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Maria

def speak(text):
    print("Roonie:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 2

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

def tocar_musica(query, plataforma="youtube"):
    if plataforma == "spotify":
        url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
    else:
        url = f"https://music.youtube.com/search?q={query.replace(' ', '+')}"

    webbrowser.open(url)
    return f"Tocando {query} no {plataforma.capitalize()}"

def handle_command(command):
    if "youtube" in command and "pesquisar" in command:
        speak("O que você quer que eu procure no YouTube?")
        query = ""
        tentativas = 0

        while not query and tentativas < 2:
            query = listen()
            tentativas += 1

        if query:
            speak(f"Pesquisando por {query} no YouTube.")
            registrar_log("pesquisar_youtube", query)
            search_youtube(query)
        else:
            speak("Desculpe, não consegui entender o que você quer pesquisar.")
            registrar_log("pesquisar_youtube", "", "falha")

    elif "pesquisar" in command:
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

    elif "tocar" in command or "toque" in command:
        plataforma = "youtube"
        if "spotify" in command:
            plataforma = "spotify"
        musica = command.replace("toque", "").replace("tocar", "").replace("no spotify", "").replace("no youtube", "").strip()

        if not musica:
            speak("Qual música você quer ouvir?")
            musica = listen()

        if musica:
            resposta = tocar_musica(musica, plataforma)
            speak(resposta)
            registrar_log("tocar_musica", f"{musica} - {plataforma}")
        else:
            speak("Desculpe, não entendi a música.")
            registrar_log("tocar_musica", "", "falha")

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

    elif "fechar" in command:
        app_name = command.replace("fechar", "").strip()
        if not app_name:
            speak("Qual aplicativo você deseja fechar?")
            app_name = listen()

        if app_name:
            resposta = fechar_app(app_name)
            speak(resposta)
            registrar_log("fechar", app_name, "sucesso" if "foi fechado" in resposta else "falha")
        else:
            speak("Não entendi o nome do aplicativo.")
            registrar_log("fechar", "", "falha")

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

speak("Roonie está pronto. Diga 'Bom Dia' para ativar.")

while True:
    if listen_for_wakeword("bom dia"):
        speak("Estou ouvindo, diga o comando.")
        while True:
            comando = listen()
            if comando:
                handle_command(comando)

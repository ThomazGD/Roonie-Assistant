import pyttsx3
import speech_recognition as sr
from tools.browser import search_google, search_youtube
from tools.apps import open_app, fechar_app
from tools.time_utils import get_time, get_date
from tools.notes import save_note, read_notes
from tools.wakeword import listen_for_wakeword
from tools.wiki_searcher import resumo_wikipedia
from tools.discord_sender import enviar_mensagem_discord
from tools.whatsapp_sender import enviar_mensagem_whatsapp
from tools.conversa_leve import conversa_leve
from voz import speak
import time
import json
from datetime import datetime
import os
import webbrowser 
from collections import defaultdict, Counter
from difflib import get_close_matches

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

def avaliar_comandos(arquivo='memory/log.json'):
    if not os.path.exists(arquivo):
        return {}

    with open(arquivo, 'r', encoding='utf-8') as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            return {}

    avaliacao = defaultdict(lambda: {"sucesso": 0, "falha": 0, "neutro": 0})

    for log in logs:
        chave = f"{log['acao']} {log['conteudo']}".strip().lower()
        resultado = log.get("resultado", "neutro").lower()
        if resultado in avaliacao[chave]:
            avaliacao[chave][resultado] += 1

    return dict(avaliacao)

def feedback_sucesso(acao, conteudo):
    speak("Isso funcionou como esperado?")
    resposta = listen()
    if "não" in resposta:
        registrar_log(acao, conteudo, "falha")
        speak("Obrigado pelo feedback, vou tentar melhorar.")
    elif "sim" in resposta:
        registrar_log(acao, conteudo, "sucesso")
        speak("Ótimo!")
    else:
        registrar_log(acao, conteudo, "neutro")
        speak("Entendido.")


def sugerir_correcao_comando(comando_usuario):
    if not os.path.exists('memory/log.json'):
        return None

    with open('memory/log.json', 'r', encoding='utf-8') as f:
        logs = json.load(f)

    comandos_sucesso = [log['conteudo'] for log in logs if log['resultado'] == 'sucesso']
    sugestoes = get_close_matches(comando_usuario, comandos_sucesso, n=1, cutoff=0.6)

    if sugestoes:
        return sugestoes[0]
    return None   

def tocar_musica(query, plataforma="youtube"):
    if plataforma == "spotify":
        url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
    else:
        url = f"https://music.youtube.com/search?q={query.replace(' ', '+')}"

    webbrowser.open(url)
    return f"Tocando {query} no {plataforma.capitalize()}"

def modo_pausa():
    speak("Roonie entrou em modo de descanso. Diga 'bom dia' para me chamar novamente.")
    while True:
        with sr.Microphone() as source:  # Desabilitar o "print" de escuta e não mostrar nada
            recognizer = sr.Recognizer()
            recognizer.pause_threshold = 2
            audio = recognizer.listen(source)
    
        try:
            comando = recognizer.recognize_google(audio, language="pt-BR").lower()
        except sr.UnknownValueError:
            comando = ""
        except sr.RequestError:
            comando = ""

        if "bom dia" in comando:  # Quando o 'bom dia' for detectado, ele sai do modo de pausa
            speak("Estou acordado. Como posso ajudar?")
            return  # Sai do modo de pausa e volta para o loop normal
        time.sleep(1)  # Um pequeno delay para não sobrecarregar a CPU

def listen_for_wakeword(palavra_chave):
    # Implementar escuta contínua para palavra-chave
    while True:
        comando = listen()
        if palavra_chave in comando:
            speak("Estou acordado. Como posso ajudar?")
            return True  # Retorna para sair do loop de escuta, apenas após "bom dia"
        time.sleep(1)
 #FUNCIONALIDADES

def handle_command(command):
    # Verifique se o comando está na lista de comandos conhecidos
    if any(frase in command for frase in ["me explica", "o que é", "quem foi", "quem é", "explique"]):
        termo = (
            command.replace("me explica", "")
                   .replace("o que é", "")
                   .replace("quem foi", "")
                   .replace("quem é", "")
                   .replace("explique", "")
                   .strip()
        )
        if termo:
            resposta = resumo_wikipedia(termo)
            speak(resposta)
            registrar_log("resumo_wikipedia", termo)
        else:
            speak("Desculpe, não entendi o que você quer que eu explique.")
            registrar_log("resumo_wikipedia", "", "falha")

    elif any(frase in command for frase in ["como você está", "vamos conversar", "me conte algo", "está tudo bem", "fala comigo"]):
        resposta = conversa_leve(command)
        speak(resposta)

    elif "youtube" in command and "pesquisar" in command:
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

    # Comando de correção apenas quando falha
    elif "fechar" in command:
        app_name = command.replace("fechar", "").strip()

        if not app_name:
            speak("Qual aplicativo você deseja fechar?")
            app_name = listen()

        if app_name:
            # Chamando a sugestão de correção **somente quando o comando não for claro ou não for encontrado**
            sugestao = sugerir_correcao_comando(app_name)
            if sugestao and sugestao != app_name:
                speak(f"Você quis dizer '{sugestao}'? Posso tentar fechar isso.")
                confirmacao = listen()
                if "sim" in confirmacao:
                    app_name = sugestao
                else:
                    speak("Ok, não vou executar.")
                    return

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

    elif "descansar" in command or "pausar" in command:
        modo_pausa()

    elif "encerrar" in command or "tchau roonie" in command:
        speak("Até logo! Encerrando o assistente.")
        registrar_log("encerrar", "Roonie desligado")
        exit()

    else:
        speak("Não entendi o comando.")
        registrar_log("comando desconhecido", command, "falha")

    return 


# Início do assistente
speak("Roonie está pronto. Diga 'Bom Dia' para ativar.")

while True:
    if listen_for_wakeword("bom dia"):
        speak("Estou ouvindo, diga o comando.")
        while True:
            comando = listen()
            if not comando:
                speak("Não entendi o que foi dito.")
                continue

            # Encerrar diretamente
            if "encerrar" in comando or "tchau roonie" in comando:
                speak("Até logo! Encerrando o assistente.")
                registrar_log("encerrar", "Roonie desligado")
                exit()
            # Comando de pausa
            elif "descansar" in comando or "pausar" in comando:
                modo_pausa()  # Ativa o modo de descanso e fica aguardando o 'bom dia' para voltar
                continue
            
            # Tratar fechamento de aplicativo com correção
            if "fechar" in comando:
                app_name = comando.replace("fechar", "").strip()
                while not app_name:
                    speak("Qual aplicativo você deseja fechar?")
                    app_name = listen()

                sugestao_app = sugerir_correcao_comando(app_name)
                if sugestao_app and sugestao_app != app_name:
                    speak(f"Você quis dizer '{sugestao_app}'? Posso tentar fechar isso.")
                    confirmacao = listen()
                    if "sim" in confirmacao:
                        app_name = sugestao_app
                    else:
                        speak("Ok, não vou executar.")
                        continue

                resposta = fechar_app(app_name)
                speak(resposta)
                registrar_log("fechar", app_name, "sucesso" if "foi fechado" in resposta else "falha")
            else:
                handle_command(comando)
                speak("Deseja fazer mais alguma coisa?")
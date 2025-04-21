import pyttsx3
import speech_recognition as sr
from tools.browser import search_platform
from tools.apps import open_app, fechar_app
from tools.time_utils import get_time, get_date
from tools.notes import save_note, read_notes
from tools.wakeword import listen_for_wakeword
from tools.wiki_searcher import resumo_wikipedia
from tools.discord_sender import enviar_mensagem_discord
from tools.whatsapp_sender import enviar_mensagem_whatsapp
from tools.conversa_leve import conversa_leve
from tools.knowledge_acquisition import estudar_assunto, estudar_pdfs
from voz import speak
import subprocess
import time
import json
from datetime import datetime
import os
import webbrowser 
from collections import defaultdict, Counter
from difflib import get_close_matches
from pathlib import Path
from datetime import datetime
import sys

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
def get_memory_path(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))  # Caminho da pasta onde está o script
    memory_folder = os.path.join(base_path, "memory")
    os.makedirs(memory_folder, exist_ok=True)  # Garante que a pasta exista
    return os.path.join(memory_folder, filename)

def registrar_log(acao, conteudo, resultado="sucesso"):
    arquivo = get_memory_path("log.json")

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

def carregar_aliases(arquivo='memory/alias.json'):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            aliases = json.load(f)
        return aliases
    except Exception as e:
        print(f"Erro ao carregar aliases: {e}")
        return {}
    
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
    speak("Roonie entrou em modo de descanso. Diga 'ativar' para me chamar novamente.")
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

        if "ativar" in comando:  # Quando o 'bom dia' for detectado, ele sai do modo de pausa
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

# Função para carregar o arquivo JSON de jogos
def carregar_jogos(arquivo='memory/todos_os_jogos.json'):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            jogos = json.load(f)  # Carrega o dicionário de jogos do arquivo JSON
        return jogos
    except Exception as e:
        print(f"Erro ao carregar jogos: {e}")
        return {}  # Retorna um dicionário vazio em caso de erro

def open_app(app_name, jogos):
    if app_name.lower() in jogos:
        jogo = jogos[app_name.lower()]
        caminho = jogo["caminho"]
        tipo = jogo["tipo"]

        try:
            if tipo == "url":
                if caminho.startswith("http"):
                    webbrowser.open(caminho)
                    return f"Abrindo {app_name} no navegador..."
                else:
                    os.startfile(caminho)  # Para com.epicgames.launcher:// e similares
                    return f"Abrindo {app_name} via protocolo..."

            elif tipo == "atalho":
                subprocess.Popen(caminho, shell=True)
                return f"Abrindo {app_name}..."

            elif tipo == "exe":
                subprocess.Popen(caminho)
                return f"Abrindo {app_name}..."

            else:
                return f"Tipo de caminho desconhecido para o jogo {app_name}."
        except Exception as e:
            return f"Erro ao tentar abrir {app_name}: {e}"
    else:
        return f"Não foi possível encontrar o jogo ou aplicativo: {app_name}"

def handle_command(command):
    if any(frase in command for frase in ["me explica", "o que é", "quem foi", "quem é", "explique"]):
        termo = command.replace("me explica", "").replace("o que é", "").replace("quem foi", "").replace("quem é", "").replace("explique", "").strip()
        if termo:
            resposta = resumo_wikipedia(termo)
            speak(resposta)
            registrar_log("resumo_wikipedia", termo)
        else:
            speak("Desculpe, não entendi o que você quer que eu explique.")
            registrar_log("resumo_wikipedia", "", "falha")

    elif "estude sobre" in command or "pesquise sobre" in command or "estudo sobre" in command:
        assunto = command.replace("estude sobre", "").replace("pesquise sobre", "").strip()
        if assunto:
            speak(f"Ok, vou estudar sobre {assunto}.")
            resultado = estudar_assunto(assunto)
            speak(resultado)
        else:
            speak("Qual assunto você quer que eu estude?")
    elif "o que você sabe sobre" in command:
        assunto = command.replace("o que você sabe sobre", "").strip().lower()
        try:
            with open('memory/knowledge.json', 'r', encoding='utf-8') as f:
                memoria = json.load(f)
            if assunto in memoria:
                resumo = memoria[assunto]
                resposta = resumo.get('wikipedia') or resumo.get('google') or resumo.get('duckduckgo')
                speak(resposta[:300] + "...")  # Limita para não falar demais
            else:
                speak("Ainda não estudei sobre esse assunto.")
        except:
            speak("Não encontrei minha base de conhecimento.")

    elif "estude os arquivos pdf" in command or "estudar arquivos" in command:
        speak("Ok, vou estudar os arquivos PDF agora.")
        resultado = estudar_pdfs()
        speak(resultado)
        
    elif "pesquisar" in command:
        plataformas_disponiveis = ["google", "youtube", "instagram", "tiktok", "twitch"]
        plataforma = "google"
        query = ""
        for plataforma_opcao in plataformas_disponiveis:
            if f"na {plataforma_opcao}" in command or f"no {plataforma_opcao}" in command:
                plataforma = plataforma_opcao
                query = command.split(f"{plataforma_opcao}")[-1].strip()
                break
        if not query:
            query = command.replace("pesquisar", "").strip()
        if query:
            speak(f"Pesquisando por {query} no {plataforma.capitalize()}")
            registrar_log(f"pesquisar_{plataforma}", query)
            search_platform(plataforma, query)
        else:
            speak("Desculpe, não consegui entender o que você quer pesquisar.")
            registrar_log(f"pesquisar_{plataforma}", "", "falha")

    elif "abrir" in command:
        jogos = carregar_jogos()
        while True:
            app_name = command.replace("abrir", "").strip()
            if not app_name:
                speak("Qual aplicativo você quer abrir?")
                app_name = listen()
            resposta = open_app(app_name, jogos)
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
        sys.exit()
    else:
        speak("Não entendi o comando.")
        registrar_log("comando desconhecido", command, "falha")
    return

# Início do assistente
speak("Roonie está pronto. Diga 'Ativar' Para Começar.")

while True:
    if listen_for_wakeword("ativar"):
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
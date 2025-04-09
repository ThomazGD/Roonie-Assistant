import os
import json
import subprocess

def open_app(nome_app, arquivo_games='games.json'):
    if not os.path.exists(arquivo_games):
        return "Arquivo de jogos não encontrado."

    with open(arquivo_games, 'r', encoding='utf-8') as f:
        jogos = json.load(f)

    nome_app = nome_app.lower().strip()

    # 1. Busca exata
    if nome_app in jogos:
        caminho = jogos[nome_app]
        subprocess.Popen(caminho, shell=True)
        return f"Abrindo {nome_app}"

    # 2. Busca parcial mais segura
    correspondencias = {nome: path for nome, path in jogos.items() if nome_app in nome}

    if len(correspondencias) == 1:
        nome_encontrado, caminho = next(iter(correspondencias.items()))
        subprocess.Popen(caminho, shell=True)
        return f"Abrindo {nome_encontrado}"

    elif len(correspondencias) > 1:
        opcoes = ', '.join(correspondencias.keys())
        return f"Encontrei várias opções para '{nome_app}': {opcoes}. Por favor, seja mais específico."

    return f"O sistema não encontrou o aplicativo '{nome_app}'."


def abrir_jogo(jogo):
    caminho = jogo["caminho"]
    try:
        if caminho.startswith("steam://") or caminho.startswith("epic://"):
            os.system(f'start "" "{caminho}"')  # Isso usa o interpretador de comandos do Windows
        elif caminho.endswith(".url") or caminho.startswith("http"):
            os.startfile(caminho)
        else:
            subprocess.Popen(caminho)
        return f"Abrindo {jogo['nome']}"
    except Exception as e:
        return f"Ocorreu um erro ao tentar abrir {jogo['nome']}: {str(e)}"

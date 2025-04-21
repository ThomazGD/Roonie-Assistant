import os
import json
import pythoncom
import configparser
from win32com.client import Dispatch

# Palavras que ajudam a identificar possíveis jogos (pode expandir)
PALAVRAS_CHAVE = ["jogo", "game", "launcher", "steam", "epic", "riot", "blizzard"]

def extrair_url_de_atalho(caminho_url):
    try:
        with open(caminho_url, 'r', encoding='utf-8') as f:
            for linha in f:
                if linha.strip().lower().startswith('url='):
                    return linha.strip()[4:]  # remove o "url="
    except Exception as e:
        print(f"Erro ao ler .url {caminho_url}: {e}")
    return None

def extrair_caminho_de_lnk(caminho_lnk):
    try:
        pythoncom.CoInitialize()
        shell = Dispatch('WScript.Shell')
        atalho = shell.CreateShortCut(caminho_lnk)
        return atalho.Targetpath
    except Exception as e:
        print(f"Erro ao ler .lnk {caminho_lnk}: {e}")
        return None

def contem_palavra_chave(nome):
    return any(palavra in nome.lower() for palavra in PALAVRAS_CHAVE)

def escanear_pasta(pasta, jogos, usar_filtro=False):
    destinos_adicionados = set()

    for root, dirs, files in os.walk(pasta):
        for file in files:
            caminho = os.path.join(root, file)
            nome = os.path.splitext(file)[0].lower()

            if usar_filtro and not contem_palavra_chave(nome):
                continue

            if file.endswith('.exe'):
                if caminho not in destinos_adicionados:
                    jogos[nome] = {"caminho": caminho, "tipo": "exe"}
                    destinos_adicionados.add(caminho)

            elif file.endswith('.lnk'):
                destino = extrair_caminho_de_lnk(caminho)
                if destino and destino not in destinos_adicionados:
                    jogos[nome] = {"caminho": destino, "tipo": "atalho"}
                    destinos_adicionados.add(destino)

            elif file.endswith('.url'):
                url = extrair_url_de_atalho(caminho)
                if url and url not in destinos_adicionados:
                    jogos[nome] = {"caminho": url, "tipo": "url"}
                    destinos_adicionados.add(url)

def escanear_todos_atalhos(arquivo_saida='memory/todos_os_jogos.json', usar_filtro=False):
    jogos = {}
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    print(f"Escaneando a área de trabalho ({desktop})...")
    escanear_pasta(desktop, jogos, usar_filtro)

    os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)  # Garante que a pasta memory exista
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(jogos, f, indent=4, ensure_ascii=False)

    print(f"{len(jogos)} jogos/atalhos salvos em {arquivo_saida}.")


if __name__ == '__main__':
    # Mude para True se quiser usar o filtro por palavras-chave
    escanear_todos_atalhos(usar_filtro=False)

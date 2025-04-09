import os
import json
import pythoncom
import configparser
from win32com.client import Dispatch

def extrair_caminho_de_lnk(caminho_lnk):
    try:
        pythoncom.CoInitialize()
        shell = Dispatch('WScript.Shell')
        atalho = shell.CreateShortCut(caminho_lnk)
        return atalho.Targetpath
    except Exception as e:
        print(f"Erro ao ler .lnk {caminho_lnk}: {e}")
        return None

def extrair_url_de_atalho(caminho_url):
    config = configparser.ConfigParser()
    try:
        config.read(caminho_url)
        return config['InternetShortcut']['URL']
    except Exception as e:
        print(f"Erro ao ler .url {caminho_url}: {e}")
        return None

def escanear_todos_atalhos(pasta='C:\\Users\\Thomaz\\Desktop', arquivo_saida='todos_os_jogos.json'):
    jogos = {}

    print(f"Escaneando {pasta}...")

    for item in os.listdir(pasta):
        caminho = os.path.join(pasta, item)
        nome = os.path.splitext(item)[0].lower()

        if item.endswith('.exe'):
            jogos[nome] = caminho

        elif item.endswith('.lnk'):
            destino = extrair_caminho_de_lnk(caminho)
            if destino:
                jogos[nome] = destino

        elif item.endswith('.url'):
            url = extrair_url_de_atalho(caminho)
            if url:
                jogos[nome] = url

    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(jogos, f, indent=4, ensure_ascii=False)

    print(f"{len(jogos)} jogos/atalhos salvos em {arquivo_saida}.")

if __name__ == '__main__':
    escanear_todos_atalhos()

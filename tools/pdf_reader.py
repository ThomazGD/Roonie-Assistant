from deep_translator import GoogleTranslator
import fitz  # PyMuPDF
import os
from textwrap import wrap
import sys
from pathlib import Path
import json
from datetime import datetime

# Adiciona o diretório pai ao path do Python
sys.path.append(str(Path(__file__).parent.parent))
from voz import speak

def traduzir_em_partes(texto, max_chars=4500):
    partes = wrap(texto, max_chars, break_long_words=False, replace_whitespace=False)
    traduzido = ""
    for i, parte in enumerate(partes):
        print(f"Traduzindo parte {i+1}/{len(partes)}...")
        traduzido += GoogleTranslator(source='auto', target='pt').translate(parte) + " "
    return traduzido.strip()

def get_pdfs_lidos(arquivo='memory/pdfs_lidos.json'):
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def salvar_pdf_lido(nome_arquivo, arquivo='memory/pdfs_lidos.json'):
    pdfs_lidos = get_pdfs_lidos(arquivo)
    pdfs_lidos[nome_arquivo] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(pdfs_lidos, f, indent=4, ensure_ascii=False)

def ler_pdfs_traduzidos(pasta='pdf'):
    textos_traduzidos = []
    pdfs_lidos = get_pdfs_lidos()

    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".pdf") and arquivo not in pdfs_lidos:
            caminho = os.path.join(pasta, arquivo)
            doc = fitz.open(caminho)
            texto = ""

            print(f"Lendo {arquivo}...")

            for pagina in doc[:10]:  # lê só as 10 primeiras páginas
                conteudo = pagina.get_text().strip()
                if conteudo:
                    texto += conteudo + "\n"

            doc.close()

            if texto:
                print(f"Traduzindo conteúdo de: {arquivo}")
                texto_pt = traduzir_em_partes(texto)
                textos_traduzidos.append({
                    "arquivo": arquivo,
                    "conteudo": texto_pt
                })
                salvar_pdf_lido(arquivo)

    return textos_traduzidos

def estudar_pdfs():
    from tools.pdf_reader import ler_pdfs_traduzidos

    speak("Ok, vou estudar os arquivos PDF agora.")
    textos = ler_pdfs_traduzidos()

    conhecimento = {}

    for item in textos:
        nome = item["arquivo"]
        conteudo = item["conteudo"]
        conhecimento[nome] = conteudo

    # Salvar na memória
    caminho_memoria = "memory/knowledge.json"
    if os.path.exists(caminho_memoria):
        with open(caminho_memoria, "r", encoding="utf-8") as f:
            try:
                memoria = json.load(f)
            except json.JSONDecodeError:
                memoria = {}
    else:
        memoria = {}

    memoria.update(conhecimento)

    with open(caminho_memoria, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

    speak("Aprendizado a partir dos PDFs concluído.")
    return "estudo_concluido"
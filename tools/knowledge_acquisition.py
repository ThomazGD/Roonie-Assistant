import json
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from tools.wiki_searcher import pesquisar_google
from tools.wiki_searcher import pesquisar_duckduckgo
from tools.wiki_searcher import resumo_wikipedia
from tools.pdf_reader import ler_pdfs_traduzidos

def estudar_assunto(assunto, arquivo='memory/knowledge.json'):
    conhecimento = {}

    # Tenta obter resumo de várias fontes
    resumo = resumo_wikipedia(assunto)
    if resumo:
        conhecimento['wikipedia'] = resumo

    resultado_google = pesquisar_google(assunto)
    if resultado_google:
        conhecimento['google'] = resultado_google

    resultado_duck = pesquisar_duckduckgo(assunto)
    if resultado_duck:
        conhecimento['duckduckgo'] = resultado_duck

    if not conhecimento:
        return "Não consegui encontrar informações suficientes sobre esse assunto."

    # Carrega conhecimento já salvo
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            memoria = json.load(f)
    else:
        memoria = {}

    memoria[assunto.lower()] = conhecimento

    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(memoria, f, indent=4, ensure_ascii=False)

    return f"Estudei sobre {assunto} e salvei na minha memória!"

def estudar_pdfs():
    textos = ler_pdfs_traduzidos()
    if not textos:
        return "Não encontrei nenhum PDF para estudar."

    for item in textos:
        nome_arquivo = os.path.basename(item["arquivo"])
        # Cria um nome mais curto e seguro usando apenas letras, números e underscore
        nome_base = ''.join(c for c in nome_arquivo if c.isalnum() or c == '_')[:50]
        if not nome_base:  # Se o nome ficar vazio, usa um nome padrão
            nome_base = "documento_pdf"
        conteudo = item["conteudo"]
        # Salva o conteúdo diretamente no arquivo de conhecimento
        salvar_conhecimento(nome_base, conteudo)

    return "Estudei todos os PDFs disponíveis!"

def salvar_conhecimento(assunto, conteudo, arquivo='memory/knowledge.json'):
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            memoria = json.load(f)
    else:
        memoria = {}

    memoria[assunto.lower()] = {'pdf': conteudo}

    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(memoria, f, indent=4, ensure_ascii=False)
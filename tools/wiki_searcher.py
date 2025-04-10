import wikipediaapi
import random
import re
import json
import os
from datetime import datetime

def limpar_termo(termo):
    termo = termo.lower()
    termo = re.sub(r"^(o que é|quem foi|explique|me explica|conceito de)\s+", "", termo).strip()
    return termo

def buscar_resumo(termo, idioma):
    wiki = wikipediaapi.Wikipedia(
        language=idioma,
        user_agent='RoonieAssistant/1.0 (https://seudominio.com)'
    )
    pagina = wiki.page(termo)
    return pagina.summary if pagina.exists() else None

def registrar_log_wiki(termo, resultado="sucesso"):
    log_path = 'memory/log.json'
    entrada = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "acao": "pesquisa_wikipedia",
        "conteudo": termo,
        "resultado": resultado
    }

    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(entrada)

    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

def resumo_wikipedia(termo):
    termo = limpar_termo(termo)

    resumo = buscar_resumo(termo, 'pt')
    if not resumo:
        resumo = buscar_resumo(termo, 'en')

    if resumo:
        introducoes = [
            "Claro! Aqui vai uma explicação rápida:",
            "Vamos lá! Descobri isso:",
            "Aqui está o que encontrei:",
            "Deixa comigo. Veja só:",
            "Isso é interessante! Olha só:" 
        ]
        introducao = random.choice(introducoes)
        resumo_traduzido = resumo.split(". ")[0:2]

        registrar_log_wiki(termo, "sucesso")
        return f"{introducao} {' '.join(resumo_traduzido)}."
    else:
        registrar_log_wiki(termo, "falha")
        return "Desculpe, não encontrei nada sobre esse assunto na Wikipédia."

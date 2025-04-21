import wikipediaapi
import requests
import random
import json
import os
from datetime import datetime

GOOGLE_API_KEY = "AIzaSyDrNdj-Y78o1c2-JH3k9wZwUltDMt0gdqw"
GOOGLE_CX = "103fdaa4b98794978"

def get_memory_path(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))  # tools/
    base_path = os.path.abspath(os.path.join(base_path, ".."))  # volta para a raiz (roonie-assistant/)
    memory_folder = os.path.join(base_path, "memory")
    os.makedirs(memory_folder, exist_ok=True)
    return os.path.join(memory_folder, filename)


log_path = get_memory_path("log.json")


def registrar_log(acao, conteudo, resultado="sucesso", arquivo=log_path):
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


def pesquisar_google(termo):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={termo}+site:br&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&hl=pt&gl=br"
        response = requests.get(url)
        data = response.json()
        if "items" in data:
            snippets = []
            for item in data["items"][:1]:  # Limita para o primeiro item
                snippet = item.get("snippet", "")
                if snippet:
                    snippets.append(snippet)
            return ' '.join(snippets)
        return ""
    except Exception as e:
        print(f"Erro ao pesquisar no Google: {e}")
        return ""

def pesquisar_duckduckgo(termo):
    try:
        response = requests.get(f"https://api.duckduckgo.com/?q={termo}+site:br&format=json&lang=pt")
        data = response.json()
        resultado = data.get("Abstract") or ""
        related_topics = data.get("RelatedTopics", [])

        # Limitar a quantidade de tópicos relacionados
        for topic in related_topics[:1]:  # Limita para o primeiro tópico relacionado
            resultado += " " + topic.get("Text", "")
        
        # Garantir que o texto esteja mais focado na pesquisa relevante
        if termo.lower() not in resultado.lower():
            return ""
        
        return resultado
    except Exception as e:
        print(f"Erro ao pesquisar no DuckDuckGo: {e}")
        return ""


def pesquisar_wikipedia(termo):
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='roonie/1.0', language='pt')
    pagina = wiki_wiki.page(termo)

    if pagina.exists():
        resumo = pagina.summary.split(". ")[:5]  # Limita para 2 frases
        return ' '.join(resumo)
    return ""



def escolher_melhor_resposta(respostas):
    respostas = [resp for resp in respostas if resp]
    if not respostas:
        return "Desculpe, não encontrei nenhuma informação confiável sobre isso."
    return random.choice(respostas)


def resumo_wikipedia(termo):
    registrar_log("pesquisa_explicacao", termo)
    google = pesquisar_google(termo)
    ddg = pesquisar_duckduckgo(termo)
    wiki = pesquisar_wikipedia(termo)

    resposta = escolher_melhor_resposta([google, ddg, wiki])
    introducoes = [
        "Claro! Aqui vai uma explicação rápida:",
        "Vamos lá! Descobri isso:",
        "Aqui está o que encontrei:",
        "Deixa comigo. Veja só:",
        "Isso é interessante! Olha só:"
    ]
    return f"{random.choice(introducoes)} {resposta}"


def analisar_rotina():
    if not os.path.exists(log_path):
        return None

    with open(log_path, 'r', encoding='utf-8') as f:
        logs = json.load(f)

    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M")
    comandos_recentes = [log for log in logs if log['acao'] == 'abrir' and log['resultado'] == 'sucesso']

    for entrada in reversed(comandos_recentes):
        hora_log = datetime.strptime(entrada['data'], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
        if hora_log == hora_atual:
            return f"Você costuma abrir '{entrada['conteudo']}' nesse horário. Deseja que eu abra novamente?"

    return None


def sugerir_correcao_comando(comando_usuario):
    if not os.path.exists(log_path):
        return None

    with open(log_path, 'r', encoding='utf-8') as f:
        logs = json.load(f)

    tentativas_falhas = [log for log in logs if log['acao'] == 'abrir' and log['resultado'] == 'falha']
    comandos_validos = [log for log in logs if log['acao'] == 'abrir' and log['resultado'] == 'sucesso']

    for falho in tentativas_falhas:
        if falho['conteudo'] in comando_usuario:
            for valido in comandos_validos:
                if valido['conteudo'].startswith(falho['conteudo']) or falho['conteudo'] in valido['conteudo']:
                    return f"Você quis dizer '{valido['conteudo']}'?"

    return None

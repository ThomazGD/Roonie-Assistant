import json
from datetime import datetime
from collections import defaultdict, Counter
import os

LOG_PATH = "memory/log.json"

def analisar_rotina():
    try:
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except:
        return None

    agora = datetime.now()
    hora_atual = agora.strftime("%H")
    comandos_horario = []

    for log in logs:
        data_log = datetime.strptime(log['data'], "%Y-%m-%d %H:%M:%S")
        if data_log.strftime("%H") == hora_atual and log['resultado'] == "sucesso":
            comandos_horario.append(log['conteudo'])

    if comandos_horario:
        mais_comum = Counter(comandos_horario).most_common(1)[0][0]
        return f"Você costuma usar '{mais_comum}' nesse horário. Deseja que eu abra para você?"

    return None

from difflib import get_close_matches

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
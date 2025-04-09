# tools/alias_manager.py

import json
import os
from collections import defaultdict, Counter

LOG_PATH = 'memory/log.json'
ALIAS_PATH = 'memory/aliases.json'

def atualizar_aliases():
    if not os.path.exists(LOG_PATH):
        return

    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        logs = json.load(f)

    ocorrencias = defaultdict(list)

    for entrada in logs:
        if entrada['acao'] == 'abrir' and entrada['resultado'] == 'sucesso':
            nome_oficial = entrada['conteudo'].lower().strip()
            ocorrencias[nome_oficial].append(nome_oficial)

        elif entrada['acao'] == 'abrir' and entrada['resultado'] == 'falha' and entrada['conteudo']:
            tentativa = entrada['conteudo'].lower().strip()
            for sucesso in ocorrencias:
                if sucesso.startswith(tentativa) or tentativa in sucesso:
                    ocorrencias[sucesso].append(tentativa)

    aliases = {oficial: list(set(tentativas)) for oficial, tentativas in ocorrencias.items()}

    with open(ALIAS_PATH, 'w', encoding='utf-8') as f:
        json.dump(aliases, f, ensure_ascii=False, indent=4)

def buscar_nome_oficial(alias):
    if not os.path.exists(ALIAS_PATH):
        return alias

    with open(ALIAS_PATH, 'r', encoding='utf-8') as f:
        aliases = json.load(f)

    for nome_real, apelidos in aliases.items():
        if alias.lower() == nome_real or alias.lower() in apelidos:
            return nome_real
    return alias

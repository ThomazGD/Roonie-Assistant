import json
import os

PREFS_PATH = "memory/preferences.json"

def carregar_preferencias():
    if os.path.exists(PREFS_PATH):
        with open(PREFS_PATH, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def salvar_preferencia(chave, valor):
    prefs = carregar_preferencias()
    prefs[chave] = valor
    with open(PREFS_PATH, 'w', encoding='utf-8') as f:
        json.dump(prefs, f, indent=4, ensure_ascii=False)

def obter_preferencia(chave):
    prefs = carregar_preferencias()
    return prefs.get(chave)

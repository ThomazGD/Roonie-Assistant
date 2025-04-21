# 🧠 Roonie - Assistente Pessoal por Voz em Python

**Roonie** é um assistente pessoal ativado por voz, desenvolvido em Python, com suporte para comandos em português. Ele reconhece a palavra de ativação ("ativar") e executa ações como abrir aplicativos, pesquisar na internet, registrar anotações, informar hora e data, e muito mais. Roonie também aprende com o tempo, registrando logs das ações realizadas para melhorar sua resposta aos comandos.

## 📌 Funcionalidades

- 🗣️ **Ativação por palavra-chave**: O assistente escuta o ambiente e responde quando ouve "ativar".
- 🔍 **Pesquisa na internet**: Pesquisa em múltiplas plataformas (Google, YouTube, Instagram, TikTok, Twitch).
- 🕹️ **Abertura de jogos e aplicativos**: Detecta atalhos (.exe, .lnk, .url) na Área de Trabalho e abre pelo nome.
- 🧠 **Memória de hábitos**: Registra logs de ações para entender sua rotina e facilitar comandos futuros.
- 🗓️ **Anotações por voz**: Você pode ditar anotações e depois pedir para ele ler tudo.
- ⏰ **Informação de data e hora atual**.
- 📁 **Gerenciamento de jogos**: Utiliza um arquivo `games.json` com nomes e caminhos de jogos, incluindo links Steam e atalhos.
- ⟳ **Modo sempre acordado**: Após a primeira ativação, ele permanece ouvindo comandos sem precisar repetir a palavra-chave.
- 📚 **Aprendizado de PDFs**: Lê e aprende com documentos PDF, traduzindo automaticamente para português.
- 🔎 **Pesquisa de conhecimento**: Responde perguntas sobre assuntos que já estudou.
- 🤖 **Estudo automático**: Pode estudar sobre qualquer assunto usando múltiplas fontes (Wikipedia, Google, DuckDuckGo).

## 🛠️ Requisitos

- Python 3.7+
- `pyttsx3`
- `speechrecognition`
- `pyaudio` (ou `pywin32`, conforme o sistema)
- `PyMuPDF` (para leitura de PDFs)
- `deep-translator` (para tradução de textos)
- Navegador padrão configurado no sistema

### Instale as dependências:

```bash
pip install pyttsx3 SpeechRecognition pymupdf deep-translator
```

> Se estiver no Windows e tiver problemas com microfone:
```bash
pip install pyaudio
```

## 🗂️ Estrutura de Arquivos

```
roonie/
├── main.py                   # Código principal do assistente
├── tools/                    # Módulos auxiliares
│   ├── apps.py              # Gerenciamento de aplicativos
│   ├── browser.py           # Pesquisa na internet
│   ├── notes.py             # Sistema de anotações
│   ├── time_utils.py        # Funções de data e hora
│   ├── wakeword.py          # Detecção de palavra-chave
│   ├── wiki_searcher.py     # Pesquisa em fontes de conhecimento
│   ├── knowledge_acquisition.py # Sistema de aprendizado
│   └── pdf_reader.py        # Leitura e tradução de PDFs
├── memory/
│   ├── games.json           # Lista de jogos com nomes e caminhos
│   ├── log.json             # Registro de ações realizadas
│   ├── knowledge.json       # Base de conhecimento
│   └── pdfs_lidos.json      # Registro de PDFs já processados
├── pdf/                     # Pasta para documentos PDF
└── voz.py                   # Sistema de fala
```

## 📋 Exemplo de `games.json`

```json
{
    "valorant": "D:\\Riot Games\\Riot Client\\RiotClientServices.exe",
    "marvel rivals": "steam://rungameid/2767030",
}
```

## 🚀 Como usar

1. Rode o `main.py`
2. Aguarde a frase: **"Roonie está pronto. Diga 'Ativar' para ativar."**
3. Diga **"ativar"** e depois o comando desejado, como:
   - "abrir valorant"
   - "pesquisar jogos novos"
   - "anotar comprar pão"
   - "ler anotações"
   - "que horas são?"
   - "qual a data de hoje?"
   - "estude sobre inteligência artificial"
   - "o que você sabe sobre python?"
   - "estude os arquivos pdf"
   - "encerrar"

## 🧠 Futuras melhorias

- Integração com APIs externas (clima, notícias, música).
- Respostas faladas mais naturais com vozes avançadas (TTS neural).
- Interface gráfica.
- Execução autônoma de tarefas rotineiras.
- Suporte a mais formatos de documentos.
- Sistema de aprendizado mais avançado.

---

Desenvolvido com ❤️ por Thomaz

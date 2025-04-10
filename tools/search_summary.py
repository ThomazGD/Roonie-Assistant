import wikipedia

def pesquisar_assunto(assunto):
    try:
        wikipedia.set_lang("pt")
        resumo = wikipedia.summary(assunto, sentences=2)
        return resumo
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Esse termo é ambíguo. Você quis dizer: {', '.join(e.options[:5])}?"
    except wikipedia.exceptions.PageError:
        return "Não encontrei nada sobre isso."
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}"

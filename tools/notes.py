def save_note(note, filename="notes.txt"):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(note + "\n")
    return "Nota salva com sucesso!"

def read_notes(filename="notes.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Nenhuma anotação encontrada."

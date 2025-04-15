import tkinter as tk
import threading
import sys
import os
import subprocess
import pyttsx3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Iniciar engine de voz
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)

# Variáveis globais
processo_roonie = None
pulsando = False
pulsar_direcao = 1
pulsar_tamanho = 0
circle = None

    
# Função para fala do Roonie e atualizar label
def speak(text):
    global pulsando
    print("Roonie:", text)
    label_fala.config(text=text)

    pulsando = True
    pulsar()  # inicia a animação

    engine.say(text)
    engine.runAndWait()

    pulsando = False  # para a animação

    
def pulsar():
    global pulsando, pulsar_direcao, pulsar_tamanho, circle

    if pulsando:
        if pulsar_tamanho >= 10 or pulsar_tamanho <= 0:
            pulsar_direcao *= -1
        pulsar_tamanho += pulsar_direcao

        novo_tamanho = 70 - pulsar_tamanho
        novo_limite = 130 + pulsar_tamanho

        canvas.coords(circle, novo_tamanho, novo_tamanho, novo_limite, novo_limite)
        root.after(50, pulsar)
    
# Ativação do assistente
def ativar_roonie():
    global processo_roonie

    python_exe = os.path.join(os.path.dirname(__file__), '..', 'venv', 'Scripts', 'python.exe')
    caminho_main = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))

    if not os.path.exists(python_exe):
        print(f"Erro: O Python do ambiente virtual não foi encontrado: {python_exe}")
    if not os.path.exists(caminho_main):
        print(f"Erro: O arquivo main.py não foi encontrado: {caminho_main}")

    label_status.config(text="Roonie está funcionando...", fg="green")
    canvas.itemconfig(circle, fill="#4CAF50")  # Muda a cor do círculo

    botao_ativar.pack_forget()

    processo_roonie = subprocess.Popen([python_exe, caminho_main])

    processo_roonie.wait()

    label_status.config(text="Roonie encerrado.")
    canvas.itemconfig(circle, fill="gray")
    botao_ativar.pack(pady=50)

def iniciar_assistente():
    threading.Thread(target=ativar_roonie).start()

# Construção da janela
root = tk.Tk()
root.title("Roonie - Assistente Virtual")
root.geometry("400x400")
root.iconbitmap("img/roonie.ico")

# Círculo clicável
canvas = tk.Canvas(root, width=150, height=150, highlightthickness=0)
circle = canvas.create_oval(10, 10, 140, 140, fill="gray")
canvas.pack(pady=20)
canvas.bind("<Button-1>", lambda e: iniciar_assistente())

# Status
label_status = tk.Label(root, text="Roonie está inativo.", font=("Arial", 14), fg="red")
label_status.pack(pady=10)

# Fala do Roonie
label_fala = tk.Label(root, text="", font=("Arial", 12), fg="blue", wraplength=350, justify="center")
label_fala.pack(pady=10)

# Botão alternativo
botao_ativar = tk.Button(root, text="Ativar Roonie", command=iniciar_assistente, font=("Arial", 14))
botao_ativar.pack(pady=10)

root.mainloop()

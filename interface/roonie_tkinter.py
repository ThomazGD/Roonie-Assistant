import tkinter as tk
import threading
import sys
import os
import subprocess


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from voz import speak

def ativar_roonie():
    python_exe = os.path.join(os.path.dirname(__file__), '..', 'venv', 'Scripts', 'python.exe')
    caminho_main = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))  # Caminho absoluto para main.py
    
    if not os.path.exists(python_exe):
        print(f"Erro: O Python do ambiente virtual não foi encontrado: {python_exe}")
    if not os.path.exists(caminho_main):
        print(f"Erro: O arquivo main.py não foi encontrado: {caminho_main}")
    
    label_status.config(text="Roonie está funcionando...", fg="green")
    
    botao_ativar.pack_forget()

    processo_roonie = subprocess.Popen([python_exe, caminho_main])

    processo_roonie.wait()

    label_status.config(text="Roonie encerrado.")
    botao_ativar.pack(pady=50) 

def iniciar_assistente():
    threading.Thread(target=ativar_roonie).start()

root = tk.Tk()
root.title("Roonie - Assistente Virtual")
root.geometry("400x300") 
root.iconbitmap("img/roonie.ico")

botao_ativar = tk.Button(root, text="Ativar Roonie", command=iniciar_assistente, font=("Arial", 16))
botao_ativar.pack(pady=50)

label_status = tk.Label(root, text="Roonie está inativo.", font=("Arial", 14), fg="red")
label_status.pack(pady=20)

root.mainloop()
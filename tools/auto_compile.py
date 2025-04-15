import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class CompileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):  # Se o arquivo modificado for um Python
            print(f"Arquivo alterado: {event.src_path}. Recompilando...")
            # Obtendo o caminho absoluto para as pastas
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Diretório raiz (roonie-assistant)
            memory_path = os.path.join(base_path, "memory")
            tools_path = os.path.join(base_path, "tools")
            img_path = os.path.join(base_path, "img")

            # Usando subprocess para rodar o pyinstaller corretamente
            subprocess.run([
                "pyinstaller", 
                "--onefile",        # Gera o .exe em um único arquivo
                "--noconsole",      # Sem a janela de console
                "--name", "roonie", # Nome do .exe
                "--icon=img/roonie.ico", # Ícone do .exe
                f"--add-data={memory_path};memory",  # Incluindo pasta memory
                f"--add-data={tools_path};tools",    # Incluindo pasta tools
                f"--add-data={img_path};img",        # Incluindo pasta img
                "main.py"           # Arquivo principal
            ], check=True)  # Substitua 'main.py' pelo seu arquivo principal

def monitorar():
    path = "."  # Diretório para monitorar (pasta raiz do projeto)
    event_handler = CompileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)  # Monitorando recursivamente
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitorar()

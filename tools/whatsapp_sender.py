from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def enviar_mensagem_whatsapp(contato, mensagem):
    options = EdgeOptions()
    options.set_capability("debuggerAddress", "127.0.0.1:9222")  # Conecta à aba já aberta

    # Conecta ao navegador já aberto com o perfil logado
    driver = webdriver.Edge(options=options)

    try:
        # Esperar um pouco para garantir que tudo está carregado
        time.sleep(5)

        # Procurar o contato
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        time.sleep(1)
        search_box.send_keys(contato)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)

        # Enviar mensagem
        msg_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        msg_box.click()
        msg_box.send_keys(mensagem)
        msg_box.send_keys(Keys.ENTER)
        time.sleep(2)

    except Exception as e:
        print("❌ Erro ao enviar mensagem:", e)

    finally:
        # NÃO fecha o navegador!
        pass
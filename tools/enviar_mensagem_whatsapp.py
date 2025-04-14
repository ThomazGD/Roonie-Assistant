def enviar_mensagem_whatsapp(contato, mensagem):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.edge.options import Options
    from time import sleep

    # Configurar o perfil do usuário real
    edge_options = Options()
    edge_options.add_argument("user-data-dir=C:\Users\Thomaz\AppData\Local\Microsoft\Edge\User Data\Profile 2")
    edge_options.add_argument("profile-directory=Profile 2")
    edge_options.add_argument("--start-maximized")

    # Iniciar o navegador com o perfil real
    driver = webdriver.Edge(options=edge_options)

    # Acessar o WhatsApp Web
    driver.get("https://web.whatsapp.com")
    sleep(5)

    try:
        # Buscar contato
        campo_pesquisa = driver.find_element(By.XPATH, '//div[@title="Caixa de texto de pesquisa"]')
        campo_pesquisa.click()
        campo_pesquisa.send_keys(contato)
        sleep(2)

        # Clicar no contato
        contato_encontrado = driver.find_element(By.XPATH, f'//span[@title="{contato}"]')
        contato_encontrado.click()
        sleep(2)

        # Digitar e enviar mensagem
        campo_mensagem = driver.find_element(By.XPATH, '//div[@title="Digite uma mensagem"]')
        campo_mensagem.send_keys(mensagem)
        campo_mensagem.send_keys(Keys.ENTER)

        print("Mensagem enviada com sucesso.")
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

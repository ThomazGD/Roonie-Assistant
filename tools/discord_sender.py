def enviar_mensagem_discord(servidor, canal, mensagem, navegador="chrome"):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from voz import speak

    import time

    options = None
    driver = None

    if navegador == "edge":
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Edge(options=options)
    else:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)

    driver.get("https://discord.com/channels/@me")

    speak("Faça login no Discord se necessário e pressione Enter para continuar.")
    input("Após o login, pressione Enter para continuar...")

    try:
        # Aguarda os elementos carregarem
        time.sleep(5)

        servidor_element = driver.find_element(By.XPATH, f"//div[@aria-label='{servidor}']")
        servidor_element.click()

        time.sleep(2)
        canal_element = driver.find_element(By.XPATH, f"//div[@role='treeitem'][.//span[text()='{canal}']]")
        canal_element.click()

        time.sleep(2)
        input_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
        input_box.send_keys(mensagem)
        input_box.send_keys(Keys.RETURN)

        time.sleep(2)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)
        speak("Houve um erro ao enviar a mensagem no Discord.")
    finally:
        driver.quit()

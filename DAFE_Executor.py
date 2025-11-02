from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Caminho local do HTML
HTML_PATH = "https://dafetech.com.br/DEMO/form.html"  # <-- altere para seu arquivo

def main():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        driver.get(HTML_PATH)

        # Espera o formulário carregar
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "formCadastro")))

        # Preenchendo os campos
        driver.find_element(By.ID, "nome").send_keys("João")
        driver.find_element(By.ID, "sobrenome").send_keys("Silva")
        driver.find_element(By.ID, "email").send_keys("joao.silva@example.com")
        driver.find_element(By.ID, "telefone").send_keys("11987654321")
        driver.find_element(By.ID, "empresa").send_keys("Corebot Solutions")
        driver.find_element(By.ID, "mensagem").send_keys("Interessado em conhecer a plataforma Corebot Py.")

        time.sleep(5)
        # Clicar no botão enviar
        driver.find_element(By.ID, "btnEnviar").click()

        print("Formulário da Corebot Py preenchido com sucesso!")

        time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

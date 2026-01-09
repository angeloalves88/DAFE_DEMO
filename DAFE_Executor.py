from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import sys
import time
import socket
from urllib.parse import urlparse

# URL do Selenium Grid Hub - usa variável de ambiente se disponível, senão usa padrão
SELENIUM_GRID_URL = os.getenv("SELENIUM_GRID_URL", "http://localhost:4444/wd/hub")

def check_host_resolution(url):
    """Verifica se o hostname da URL pode ser resolvido"""
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False, "Hostname não encontrado na URL"
        socket.gethostbyname(hostname)
        return True, None
    except socket.gaierror as e:
        hostname = parsed.hostname if 'parsed' in locals() else 'desconhecido'
        return False, f"Não foi possível resolver o hostname '{hostname}': {str(e)}"
    except Exception as e:
        return False, f"Erro ao verificar hostname: {str(e)}"

# Caminho local do HTML
HTML_PATH = "https://dafetech.com.br/DEMO/form.html"  # <-- altere para seu arquivo

def is_running_in_docker():
    """Detecta se está rodando dentro de um container Docker"""
    return os.path.exists("/.dockerenv") or os.getenv("DOCKER_CONTAINER") == "true"

def is_windows():
    """Detecta se está rodando no Windows"""
    return sys.platform.startswith("win")

def get_chrome_options():
    """Configura opções do Chrome baseado no ambiente"""
    chrome_options = ChromeOptions()
    
    # Opções necessárias para Docker/Linux
    if is_running_in_docker():
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        print(" Ambiente Docker detectado - opções de container aplicadas")
    
    # Opções recomendadas para ambos os ambientes
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    return chrome_options

def main():
    # Informações do ambiente
    print("=== Configuração do Ambiente ===")
    print(f"Plataforma: {'Windows' if is_windows() else 'Linux/Unix'}")
    print(f"Docker: {'Sim' if is_running_in_docker() else 'Não'}")
    print(f"Selenium Grid URL: {SELENIUM_GRID_URL}")
    print("================================\n")
    
    # Configurando opções do Chrome
    chrome_options = get_chrome_options()
    
    try:
        # Verificando resolução do hostname antes de tentar conectar
        print(f"Verificando conectividade com {SELENIUM_GRID_URL}...")
        can_resolve, error_msg = check_host_resolution(SELENIUM_GRID_URL)
        
        if not can_resolve:
            print(f"\n ERRO DE CONECTIVIDADE:")
            print(f"   {error_msg}")
            print(f"\n POSSÍVEIS SOLUÇÕES:")
            parsed = urlparse(SELENIUM_GRID_URL)
            hostname = parsed.hostname
            
            if hostname == "selenium-hub":
                print(f"   1. Verifique se o serviço 'selenium-hub' está rodando")
                print(f"   2. Se estiver usando Docker Compose, verifique se os containers estão na mesma rede")
                print(f"   3. Se estiver usando Docker, verifique se o container está na mesma network")
                print(f"   4. Tente usar 'localhost' ou o IP do host se estiver rodando localmente")
                print(f"   5. Verifique a variável de ambiente SELENIUM_GRID_URL:")
                print(f"      Valor atual: {SELENIUM_GRID_URL}")
                print(f"      Para usar localhost: export SELENIUM_GRID_URL=http://localhost:4444/wd/hub")
            else:
                print(f"   1. Verifique se o hostname '{hostname}' está correto")
                print(f"   2. Verifique se o serviço Selenium Grid está rodando")
                print(f"   3. Verifique conectividade de rede/DNS")
                print(f"   4. Valor atual da URL: {SELENIUM_GRID_URL}")
            
            raise ConnectionError(f"Não foi possível resolver o hostname: {error_msg}")
        
        print(" Hostname resolvido com sucesso")
        
        # Conectando ao Selenium Grid
        print(f"Conectando ao Selenium Grid em {SELENIUM_GRID_URL}...")
        driver = webdriver.Remote(
            command_executor=SELENIUM_GRID_URL,
            options=chrome_options
        )
        print(" Conexão estabelecida com sucesso!\n")
        
        # Maximizar janela (fallback se --start-maximized não funcionar)
        try:
            driver.maximize_window()
        except Exception:
            pass

        # Navegando para a página
        print(f"Navegando para: {HTML_PATH}")
        driver.get(HTML_PATH)

        # Espera o formulário carregar
        print("Aguardando formulário carregar...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "formCadastro")))
        print(" Formulário carregado\n")

        # Preenchendo os campos
        print("Preenchendo campos do formulário...")
        driver.find_element(By.ID, "nome").send_keys("João")
        driver.find_element(By.ID, "sobrenome").send_keys("Silva")
        driver.find_element(By.ID, "email").send_keys("joao.silva@example.com")
        driver.find_element(By.ID, "telefone").send_keys("11987654321")
        driver.find_element(By.ID, "empresa").send_keys("Corebot Solutions")
        driver.find_element(By.ID, "mensagem").send_keys("Interessado em conhecer a plataforma Corebot Py.")
        print("✓ Campos preenchidos\n")

        time.sleep(2)
        
        # Clicar no botão enviar
        print("Enviando formulário...")
        driver.find_element(By.ID, "btnEnviar").click()
        print(" Formulário enviado com sucesso!\n")

        time.sleep(3)

    except Exception as e:
        print(f"\n Erro durante execução: {str(e)}")
        raise
    finally:
        if 'driver' in locals():
            print("Encerrando driver...")
            driver.quit()
            print(" Driver encerrado")

if __name__ == "__main__":
    main()

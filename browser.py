from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from logger import Logger

logger = Logger.get_logger(__name__)

def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if os.environ.get('HEADLESS', 'false').lower() == 'true':
        logger.info("Executando em modo headless")
        options.add_argument("--headless")
    
    try:
        logger.info("Tentando inicializar Chrome usando Selenium Manager interno...")
        driver = webdriver.Chrome(options=options)
        logger.info("Chrome inicializado com sucesso usando Selenium Manager")
        return driver
    except Exception as e:
        logger.warning(f"Falha na abordagem 1 (Selenium Manager): {e}")
    
    try:
        logger.info("Tentando inicializar Chrome usando WebDriver Manager...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logger.info("Chrome inicializado com sucesso usando WebDriver Manager")
        return driver
    except Exception as e:
        logger.warning(f"Falha na abordagem 2 (WebDriver Manager): {e}")
    
    local_driver = os.path.join(os.getcwd(), "chromedriver.exe" if os.name == 'nt' else "chromedriver")
    if os.path.exists(local_driver):
        try:
            logger.info(f"Tentando usar ChromeDriver local em: {local_driver}")
            service = Service(executable_path=local_driver)
            driver = webdriver.Chrome(service=service, options=options)
            logger.info("Chrome inicializado com sucesso usando ChromeDriver local")
            return driver
        except Exception as e:
            logger.warning(f"Falha na abordagem 3 (ChromeDriver local): {e}")
    
    error_msg = "Não foi possível inicializar o Chrome WebDriver. Verifique a instalação do Chrome e do ChromeDriver."
    logger.error(error_msg)
    raise RuntimeError(error_msg)
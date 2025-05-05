import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from browser import get_chrome_driver
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from config import Config
from logger import Logger

logger = Logger.get_logger("test_saucedemo")

class TestSauceDemo(unittest.TestCase):
    def setUp(self):
        logger.info("Iniciando teste")
        
        self.driver = get_chrome_driver()
        
        self.login_page = LoginPage(self.driver)
        self.products_page = ProductsPage(self.driver)
    
    def tearDown(self):
        logger.info("Finalizando teste")
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def test_login_and_extract_products(self):
        logger.info("Iniciando teste de login e extração de produtos")
        
        self.login_page.navigate_to(Config.BASE_URL)
        
        logger.info(f"Fazendo login com usuário: {Config.USERNAME}")
        self.login_page.login(Config.USERNAME, Config.PASSWORD)
        
        self.assertTrue(self.login_page.is_login_successful(), "O acesso não foi bem-sucedido!")
        logger.info("Acesso realizado com sucesso")
        
        self.assertTrue(self.products_page.is_product_page_loaded(), "Pagina de produtos não foi carregada")
        logger.info("Páginaa de produtos carregada com sucesso")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = Config.OUTPUT_FILE if hasattr(Config, 'OUTPUT_FILE') else "produtos"
        
        if base_filename.lower().endswith('.csv'):
            base_name = base_filename[:-4] 
            csv_filename = f"{base_name}_{timestamp}.csv"
        else:
            csv_filename = f"{base_filename}_{timestamp}.csv"
            
        logger.info(f"Nome do arquivo CSV gerado: {csv_filename}")
        
        logger.info("Extraindo informações dos produtos...")
        csv_file = self.products_page.save_products_to_csv(csv_filename)
        
        self.assertTrue(os.path.exists(csv_file), f"Arquivo CSV não foi criado: {csv_file}")
        self.assertTrue(os.path.getsize(csv_file) > 0, "O arquivo CSV está vazio")
        
        logger.info(f"Dados extraidos com sucesso para: {csv_file}")
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Sauce Labs", content, "Conteudo do CSV não contém produtos esperados")
        
        logger.info("Teste concluído com sucesso")


if __name__ == "__main__":
    unittest.main()
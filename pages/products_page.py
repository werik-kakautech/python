from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import csv
import os
import time
from logger import Logger

class ProductsPage(BasePage):
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_DESC = (By.CLASS_NAME, "inventory_item_desc") 
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = Logger.get_logger(self.__class__.__name__)
    
    def is_product_page_loaded(self):
        return self.is_element_present(self.INVENTORY_CONTAINER)
    
    def get_all_products(self):

        products = []
        
        self.logger.info("Aguardando o container de inventário...")
        try:
            self.wait_for_element_visible(self.INVENTORY_CONTAINER)
            self.logger.info("Container de inventário encontrado!")
        except Exception as e:
            self.logger.warning(f"Erro ao encontrar o container de inventário: {e}")
            self.logger.info("Tentando navegação direta para página de inventário...")
            self.driver.get("https://www.saucedemo.com/inventory.html")
            time.sleep(2)
        
        try:
            self.logger.info("Extraindo produtos via JavaScript...")
            products_data = self.driver.execute_script("""
                const products = [];
                const items = document.querySelectorAll('.inventory_item');
                
                items.forEach(item => {
                    const nameElem = item.querySelector('.inventory_item_name');
                    const descElem = item.querySelector('.inventory_item_desc');
                    const priceElem = item.querySelector('.inventory_item_price');
                    
                    products.push({
                        name: nameElem ? nameElem.textContent : 'Nome não encontrado',
                        description: descElem ? descElem.textContent : 'Descrição não encontrada',
                        price: priceElem ? priceElem.textContent : 'Preço não encontrado'
                    });
                });
                
                return products;
            """)
            
            self.logger.info(f"Extraídos {len(products_data)} produtos via JavaScript")
            return products_data
        except Exception as e:
            self.logger.error(f"Erro na extração via JavaScript: {e}")
        
        self.logger.info("Usando método Selenium para extração")
        items = self.find_elements(self.PRODUCT_ITEMS)
        self.logger.info(f"Encontrados {len(items)} itens de produto")
        
        for i, item in enumerate(items):
            try:
                name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                description = item.find_element(By.CLASS_NAME, "inventory_item_desc").text
                price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
                
                products.append({
                    "name": name,
                    "description": description,
                    "price": price
                })
            except Exception as e:
                self.logger.warning(f"Erro ao processar produto {i+1}: {e}")
            
        self.logger.info(f"Total de produtos extraídos: {len(products)}")
        return products
    
    def save_products_to_csv(self, filename=None):
        if filename is None:
            filename = os.path.abspath(os.path.join(os.getcwd(), "produtos.csv"))
        
        self.logger.info(f"Iniciando extração de produtos para o arquivo CSV: {filename}")
        products = self.get_all_products()
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'description', 'price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                if not products:
                    self.logger.warning("Nenhum produto extraído para salvar no CSV")
                    writer.writerow({
                        'name': 'ERRO: Nenhum produto encontrado',
                        'description': 'Verifique os logs para mais detalhes',
                        'price': '0.00'
                    })
                else:
                    for product in products:
                        writer.writerow(product)
                
            self.logger.info(f"Salvos {len(products) if products else 0} produtos no arquivo {filename}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar no CSV: {e}")
            backup_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "produtos_backup.csv")
            self.logger.info(f"Tentando salvar em arquivo de backup: {backup_file}")
            
            with open(backup_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'description', 'price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                if products:
                    for product in products:
                        writer.writerow(product)
                        
            self.logger.info(f"Arquivo de backup salvo em: {backup_file}")
            return backup_file
            
        return filename
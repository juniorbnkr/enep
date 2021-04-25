from selenium import webdriver
import time

class Browser:
   
    def __init__(self):
        self = self
        self.driver = webdriver.Firefox(executable_path=r'./geckodriver')
        
    def go_to_page(self, ano):
        try:
            self.driver.get('https://www.sep.org.br/consulta_enep.php')
            time.sleep(1)
            #Selecionar item de ano
            ano_button = self.driver.find_element_by_id("radios-1")
            ano_button.click()
            time.sleep(1)
            #Digitar ano do ENEP
            busca = self.driver.find_element_by_id("Busca")
            busca.send_keys(ano)
            #Apertar botão de consulta para listar trabalhos
            consulta_button = self.driver.find_element_by_xpath("/html/body/form/fieldset/div[3]/div/input")
            consulta_button.click()
            time.sleep(3)
        except Exception as e:
            print(e)
            return False
        else:
            return self.driver

    def get_rows(self):
        try:
            rows = self.driver.find_elements_by_tag_name("tr")
            return rows
        except Exception as e:
            print(e)
            print("error in get rows.")
            return False 
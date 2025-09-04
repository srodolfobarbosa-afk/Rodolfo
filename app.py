from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route('/')
def home():
    # Esta linha vai procurar pelo arquivo 'index.html' na pasta 'templates'
    return render_template('index.html')


class WebAgent:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # Use ChromeDriverManager to automatically download and manage chromedriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def navigate(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def search(self, query, search_box_selector, submit_button_selector=None):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, search_box_selector))
        )
        search_box.send_keys(query)
        if submit_button_selector:
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector))
            )
            submit_button.click()
        else:
            search_box.submit()
        time.sleep(3) # Give time for page to load
        return self.driver.page_source

    def get_text_by_selector(self, selector):
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        return [elem.text for elem in elements]

    def close(self):
        self.driver.quit()

# Exemplo de uso (para testes internos)
if __name__ == "__main__":
    agent = WebAgent()
    try:
        print("Navegando para Google...")
        agent.navigate("https://www.google.com")
        print("Buscando por 'EcoGuardians'...")
        agent.search("EcoGuardians", "textarea[name=\'q\']") # Google search box selector
        print("Conteúdo da página após busca:")

        search_results = agent.get_text_by_selector("h3")
        print("Títulos dos resultados:")
        for title in search_results:
            print(f"- {title}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        agent.close()

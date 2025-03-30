from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time

def get_deputies_details_selenium(max_steps=5):

    BASE_URL = "https://www.cdep.ro/pls/parlam/structura2015.mp?idm=1&cam=2&leg=2024&pag=1&idl=1&prn=0&par="

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Edge(options=options)

    current_url = BASE_URL
    deputies = []
    step = 0 

    while current_url and step < max_steps:
        driver.get(current_url)
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        container = soup.find("div", class_="stiri-detalii clearfix")
        if container:
            deputies.append({
                "profil_link": current_url,
                "data_details_container": container.prettify()
            })

        next_btn = soup.find("a", id="action-right")
        if next_btn and next_btn.get("href"):
            current_url = "https://www.cdep.ro" + next_btn["href"]
            step += 1 
        else:
            break

    driver.quit()
    return deputies

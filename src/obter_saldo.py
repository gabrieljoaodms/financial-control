from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd
from datetime import date

def obter_saldo():

    load_dotenv()
    db = create_engine(os.getenv("DL_STRING"))

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    url_1 = "https://app.kinvo.com.br/login"
    driver.get(url_1)
 
    username_input = driver.find_element("name","email")
    password_input = driver.find_element("name","password")
    username_input.send_keys(os.getenv("EMAIL"))
    password_input.send_keys(os.getenv("PASS"))
    button = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
        (By.XPATH, '//button[.//div[text()="Entrar"]]')
    )
    )
    button.click()

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "sc-gbRWpc bXjJNa")))
    except:
        pass

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    html_saldo = list(soup.find_all('h2', class_='sc-gbRWpc bXjJNa'))[0].text
    saldo = float(html_saldo.split("\xa0")[1].replace('.','').replace(',','.'))
    print(saldo)

    tabela_db = pd.read_sql('saldo_investimentos', con = db)
    datas = list(tabela_db['data'])
    data = date.today()
    if data in datas:
        db.execute(f"DELETE FROM saldo_investimentos WHERE data = '{data}'")
    df = pd.DataFrame([[data, saldo]], columns = ['data', 'saldo'])
    df.to_sql('saldo_investimentos', con = db, index = False, if_exists = 'append')
    db.dispose()
    
    return saldo

obter_saldo()







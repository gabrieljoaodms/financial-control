from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def obter_saldo():

    driver = webdriver.Chrome(ChromeDriverManager().install())

    url_1 = "https://app.kinvo.com.br/login"
    driver.get(url_1)

    username_input = driver.find_element("name","email")
    password_input = driver.find_element("name","password")
    username_input.send_keys("gabriieljoaao@gmail.com")
    password_input.send_keys("Fd3jk99.")
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
    print(html)

    soup = BeautifulSoup(html, 'html.parser')
    html_saldo = list(soup.find_all('h2', class_='sc-gbRWpc bXjJNa'))[0].text
    saldo = float(html_saldo.split("\xa0")[1].replace('.','').replace(',','.'))
    print(saldo)
    
    return saldo








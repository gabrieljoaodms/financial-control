import streamlit as st
import pandas as pd
import numpy as np
import emoji
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from obter_categoria import obter_categoria
import matplotlib.pyplot as plt
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


def obter_saldo():

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
    
    return saldo


def main():
    st.sidebar.title('Menu')
    paginaSelecionada = st.sidebar.selectbox('Selecione a página', ['Adicionar Receita', 'Adicionar Saída','Acrescentar Categoria', 'Aportes',
                                                                    'Saldo Investimentos', 'Ajustar Orçamento'])

    operacao = ['Entrada', 'Saque']

    pessoas = ['Carol', 'João']

    saida_categoria = obter_categoria()

    receita_categoria = ['Salário', 'Vale-Refeição', 'Outros']

    investimento_categoria = ['Casamento', 'Reserva de Emergência']

    load_dotenv()
    db = create_engine(os.getenv("DL_STRING"))

    if paginaSelecionada == 'Adicionar Receita':
        with st.form(key="Receita"):
            trabalhador = st.selectbox(emoji.emojize('Trabalhador :briefcase:'), pessoas)
            categoria = st.selectbox(emoji.emojize('Categoria :file_cabinet:'), receita_categoria)
            valor = st.number_input(emoji.emojize('Valor :money-mouth_face:'))
            data_operacao = st.date_input(emoji.emojize('Dia :calendar:'))
            descricao = st.text_input(emoji.emojize('Descrição :pencil:'))
            input_button_submit = st.form_submit_button('Enviar')

        if input_button_submit:
            df = pd.DataFrame([['receita', trabalhador, categoria, data_operacao, valor, descricao]], 
            columns = ['operacao', 'pessoa','categoria', 'data_operacao', 'valor', 'descricao'])
            df.to_sql('operacao', con = db, index = False, if_exists = 'append')
            db.dispose()
            st.write(df)

    elif paginaSelecionada == 'Adicionar Saída':
        with st.form(key="Saída"):
            consumista = st.selectbox(emoji.emojize('Consumista :receipt:'), pessoas)
            categoria = st.selectbox(emoji.emojize("Categoria :file_cabinet:"), saida_categoria)
            valor = st.number_input(emoji.emojize('Valor :money_with_wings:'), min_value = 0.00)
            data_operacao = st.date_input(emoji.emojize('Dia :calendar:'))
            descricao = st.text_input(emoji.emojize('Descrição :pencil:'))
            input_button_submit = st.form_submit_button('Enviar')

        if input_button_submit:
            valor_arredondado = round(-valor, 2)
            df = pd.DataFrame([['saída', consumista, categoria, data_operacao, valor_arredondado, descricao]], 
            columns = ['operacao', 'pessoa','categoria', 'data_operacao', 'valor', 'descricao'])
            df.to_sql('operacao', con = db, index = False, if_exists = 'append')
            db.dispose()
            st.write(df)

    elif paginaSelecionada == 'Acrescentar Categoria':
        with st.form(key="Categoria"):
            nova_categoria = st.text_input(emoji.emojize('Nova categoria :file_cabinet:'))
            input_button_submit = st.form_submit_button('Enviar')
            st.write('Categorias já existentes:')
            st.write(pd.read_sql('categoria_saida', con = db))

        if input_button_submit:
            df = pd.DataFrame([nova_categoria], columns = ['categoria'])
            df.to_sql('categoria_saida', con = db, index = False, if_exists = 'append')
            db.dispose()
            st.write(pd.read_sql('categoria_saida', con = db))

    elif paginaSelecionada == 'Aportes':
        with st.form(key="Aportes"):
            investidor = st.selectbox(emoji.emojize('Investidor :briefcase:'), pessoas)      
            categoria_investimento = st.selectbox(emoji.emojize("Categoria :file_cabinet:"), investimento_categoria)
            aporte = st.number_input(emoji.emojize('Valor :money-mouth_face:'), min_value = 0.00)
            data = st.date_input(emoji.emojize('Dia :calendar:'))
            input_button_submit = st.form_submit_button('Enviar')

        if input_button_submit:
            df = pd.DataFrame([[investidor,categoria_investimento, aporte, data]], columns = ['pessoa','categoria_investimento', 'aporte', 'data'])
            df.to_sql('aportes_investimentos', con = db, index = False, if_exists = 'append')
            db.dispose()
            st.write(pd.read_sql('aportes_investimentos', con = db))

    elif paginaSelecionada == 'Saldo Investimentos':
        with st.form(key="Orçamento"):      
            input_button_submit = st.form_submit_button('Ver Saldo')

        if input_button_submit:

            tabela_db = pd.read_sql('saldo_investimentos', con = db)
            tabela_db = tabela_db.sort_values('data', ascending=False)

            saldo_atual = tabela_db.loc[tabela_db.index[0], 'saldo']
            saldo_anterior = tabela_db.loc[tabela_db.index[1], 'saldo']
            kpi1, kpi2 = st.columns(2)

            # fill in those three columns with respective metrics or KPIs
            kpi1.metric(
                label= emoji.emojize('Saldo Investimentos :money-mouth_face:'),
                value=f"R$ {round(saldo_atual)}",
                delta=f"R$ {round(saldo_atual) - round(saldo_anterior)}"
            )

            kpi2.metric(
                label= emoji.emojize('Última Atualização :calendar:'),
                value=f"{tabela_db.loc[tabela_db.index[0], 'data'].date()}"
            )

            fig, ax = plt.subplots()
            ax.plot(tabela_db['data'], tabela_db['saldo'])
            ax.set_xlabel('Data')
            ax.set_ylabel('Saldo')

            # Exibir o gráfico no Streamlit
            st.pyplot(fig)
            st.dataframe(tabela_db)

    elif paginaSelecionada == 'Ajustar Orçamento':
        with st.form(key="Orçamento"):
            
            input_button_submit = st.form_submit_button('Enviar')
        df = pd.DataFrame(
            np.random.randn(10, 5),
        columns=('col %d' % i for i in range(5)))
        st.table(df)
        if input_button_submit:
            st.write(pd.read_sql('categorias', con = db))
    return
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from log import logger
import os
from sqlalchemy import create_engine
import keyboard
import threading
import time
import pickle
from pathlib import Path
from main import main
import streamlit_authenticator as stauth

load_dotenv()
db = create_engine(os.getenv("DB_STRING"))

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()

def login_usuario(username,password):
    username = "'" + str(username) + "'"
    password = "'" + str(password) + "'"
    conta = pd.read_sql(f'SELECT * FROM login WHERE usuario = {username} and senha is NOT NULL and senha = crypt({password}, senha)', con = db)
    return len(conta) > 0

def click_login(usuario,senha):
    if login_usuario(usuario, senha):
        st.session_state['logado'] = True
    else:
        st.session_state['logado'] = False
        st.error("Usuário/Senha incorretos.")

placeholder = st.empty()

def pagina_login():
    with loginSection:
        if st.session_state['logado'] == False:
            usuario = st.text_input('Usuário')
            senha = st.text_input('Senha',type='password')
            st.button('login', on_click=click_login, args=(usuario, senha))
            logger.info('pagina de login')

with headerSection:
    st.title("Finanças João e Carol")
    st.subheader("Bora casar!!!")
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        pagina_login()
    else:
        if st.session_state['logado']:
            main()
        else:
            pagina_login()
 

    
    

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import keyboard
import threading
import time
#wait time to close page and open a new one.
wait_second = 0.8

#thread for closing page
def threadFunc():
   time.sleep(wait_second)
   keyboard.press_and_release('ctrl+w')

load_dotenv()
db = create_engine(os.getenv("DB_STRING"))

def login_usuario(username,password):
    username = "'" + str(username) + "'"
    password = "'" + str(password) + "'"
    conta = pd.read_sql(f'SELECT * FROM login WHERE usuario = {username} and senha is NOT NULL and senha = crypt({password}, senha)', con = db)
    st.write(conta)
    return len(conta) > 0

usuario = st.text_input('Usuário')
senha = st.text_input('Senha',type='password')
test = st.button('login')

if test:
    login = login_usuario(usuario,senha)
    if login:
        st.success("Logged In as {}".format(usuario))
        th = threading.Thread(target=threadFunc)
        th.start()
        os.system(r"streamlit run main.py")
        th.join()

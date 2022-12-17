import streamlit as st
import pandas as pd
import emoji
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()
db = create_engine(os.getenv("DB_STRING"))

def obter_categoria():
    categorias = pd.read_sql('categorias', con = db)
    lista_categorias = list(categorias['categoria'])
    return lista_categorias


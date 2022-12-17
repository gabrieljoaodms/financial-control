import streamlit as st
import pandas as pd
import numpy as np
import emoji
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from obter_categoria import obter_categoria


st.sidebar.title('Menu')
paginaSelecionada = st.sidebar.selectbox('Selecione a página', ['Adicionar Receita', 'Adicionar Saída','Acrescentar Categoria', 'Aportes',
                                                                'Saldo Investimentos', 'Ajustar Orçamento'])

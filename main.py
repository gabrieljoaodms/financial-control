import streamlit as st
import pandas as pd
import numpy as np
import emoji
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from obter_categoria import obter_categoria

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
    db = create_engine(os.getenv("DB_STRING"))

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
            st.write(pd.read_sql('categorias', con = db))

        if input_button_submit:
            df = pd.DataFrame([ nova_categoria], columns = ['categoria'])
            df.to_sql('categorias', con = db, index = False, if_exists = 'append')
            db.dispose()
            st.write(pd.read_sql('categorias', con = db))

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
            categoria_investimento = st.selectbox(emoji.emojize("Categoria :file_cabinet:"), investimento_categoria)
            saldo = st.number_input(emoji.emojize('Valor :money-mouth_face:'), min_value = 0.00)
            data = st.date_input(emoji.emojize('Dia :calendar:'))
            input_button_submit = st.form_submit_button('Enviar')

        if input_button_submit:
            df = pd.DataFrame([[categoria_investimento, saldo, data]], columns = ['categoria_investimento', 'saldo', 'data'])
            df.to_sql('saldo_investimentos', con = db, index = False, if_exists = 'append')
            db.dispose()
            st.write(pd.read_sql('saldo_investimentos', con = db))


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
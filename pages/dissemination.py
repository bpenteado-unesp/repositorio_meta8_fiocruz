import streamlit as st
from helper import *

render_menu()

# Corpo principal

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Ferramentas de disseminação de ciência de dados",
    layout="wide",  # Layout expandido para acomodar melhor os cards
    initial_sidebar_state="expanded"
)

path_arquivo = 'data/disseminacao.xlsx'

st.title("Ferramentas para disseminação de dados")

exibe_dados(path_arquivo)




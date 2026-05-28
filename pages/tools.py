import streamlit as st
from helper import *

render_menu()

# Corpo principal

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Ferramentas para desenvolvimento de software para ciência de dados",
    layout="wide",  # Layout expandido para acomodar melhor os cards
    initial_sidebar_state="expanded"
)

path_arquivo = 'data/ferramentas.xlsx'

st.title("Ferramentas para criação de scripts e programas de ciência de dados:")

exibe_dados(path_arquivo)

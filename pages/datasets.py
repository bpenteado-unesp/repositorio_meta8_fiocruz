import streamlit as st
import pandas as pd
from helper import render_menu, carregar_dados, carregar_ordenacao, carregar_quadro_sintese, popular_retorno, buscar


render_menu()

# Corpo principal

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Ferramentas de disseminação de ciência de dados",
    layout="wide",  # Layout expandido para acomodar melhor os cards
    initial_sidebar_state="expanded"
)

path_arquivo = 'data/datasets.xlsx'

st.title("Ferramentas de apoio à disseminação de pesquisas de ciência de dados na Vigilância Epidemiológica")



with st.expander("Clique para ver possíveis cenários de uso"):
	st.markdown("## Quadro de síntese:")
	carregar_quadro_sintese(path_arquivo)
with st.spinner("Carregando dados..."):
	st.markdown("## Ferramentas sugeridas:")
	dados = carregar_dados(path_arquivo)
	
	sub_busca, sub_total, sub_ranking = st.columns([5,2,3], vertical_alignment="center")

	with sub_busca:
		strBusca = st.text_input("Busque por texto...")
		if strBusca != "":
			dados = buscar(strBusca, dados)
	with sub_total:
		total_registros = len(dados) 
		st.metric(label="Total de Registros", value=total_registros)
	with sub_ranking:
		dados = carregar_ordenacao(dados)
	
	popular_retorno(dados)



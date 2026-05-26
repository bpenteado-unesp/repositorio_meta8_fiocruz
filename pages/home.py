import streamlit as st
from helper import render_menu

render_menu()
# 1. Configuração inicial da página
st.set_page_config(
    page_title="Repositório Fiocruz de ciência de dados para a vigilância epidemiológica",
    layout="wide",  # Layout expandido para acomodar melhor os cards
    initial_sidebar_state="expanded"
)

st.title("Repositório Fiocruz de recursos para ciência de dados na vigilância epidemiológica")
st.markdown(""" 
	Este projeto é parte da Meta 8 do TED XXX do Ministério da Saúde.
	Aqui é apresentado um repositório com recursos que podem ser usados para a condução de projetos de ciências de dados no âmbito da vigilância sanitária.

Isto é feito por meio de 3 entregáveis: 

* Modelo de processo integrado: permite que profissionais da vigilância possam compreender como a ciência de dados se corresponde a seu método tual e como estendê-lo;
* Recursos: apresenta recursos (ferramentas e bases de dados) que podem auxiliar o processo integrado de ciência de dados na vigilância epidemiológica;
* Glossário de termos de ciência de dados: traz o significado de muitos dos termos técnicos aplicados na área de ciência de dados.
	""")
st.markdown("""
	Abaixo temos a ilustração da integração entre os processos da ciência de dados e da VE, e a seguir as fontes utilizadas para esta integração.

	""")
st.image("img/processo_integrado.png", width=900, caption="Processo integrado de ciência de dados e vigilância epidemiológica")
st.markdown("""
	Este modelo integrado é baseado em padrões das áreas de ciência de dados (CRISP-DM [Chapman et al., 2000]) e 
			modelo de ciclo de vida de pesquisa em vigilância epidemiológica (REF).
	""")

img1, img2 = st.columns([1,1], vertical_alignment='center')
with img1:
	st.image("https://upload.wikimedia.org/wikipedia/commons/b/b9/CRISP-DM_Process_Diagram.png", width=350, caption="Modelo CRISP-DM de ciência de dados")
with img2:
	st.image("https://img.passeidireto.com/material/59553038/7857866d-fddf-4114-beb4-a279a9bef695.png", width=600, caption="Ações da Vigilância Epidemiológica")
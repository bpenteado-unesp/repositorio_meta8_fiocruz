import base64

import streamlit as st
from helper import *
import glob
import os

render_menu()

# Corpo principal

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Exemplos de códigos para tarefas de vigilância epidemiológica em linguagem R",
    layout="wide",  # Layout expandido para acomodar melhor os cards
    initial_sidebar_state="expanded"
)

path_arquivo = './scripts'

st.title("Exemplos de códigos para tarefas de vigilância epidemiológica em linguagem R")

st.markdown("""
Estes arquivos têm finalidade pedagógica e foram preparados para apoiar atividades práticas sobre modelagem e análise de dados aplicadas à vigilância epidemiológica, especialmente em cursos de Sistemas de Informação, Ciência de Dados, Computação em Saúde e áreas afins. O conjunto demonstra como tarefas corriqueiras, intermediárias e avançadas podem ser traduzidas em rotinas computacionais em R/RStudio, organizadas por etapas como entendimento do problema, obtenção dos dados, preparação, análise, validação e geração de saídas.

Os arquivos podem ser usados em aulas práticas, oficinas, estudos dirigidos ou projetos de iniciação científica, permitindo que os estudantes compreendam tanto o funcionamento técnico do código quanto a lógica analítica aplicada a bases epidemiológicas. Os CSVs incluídos são sintéticos e simulam problemas comuns de qualidade dos dados, enquanto os scripts com microdatasus mostram como acessar dados públicos do DATASUS diretamente em R; portanto, o material não tem finalidade operacional em saúde pública, mas sim formativa e demonstrativa.

Arquivos de exemplo para serem trabalhados com os scripts R:
            
			""")

col1, col2 = st.columns([2,8])
# habilita o download dos arquivos de dados de exemplo
with col1:
	with open("./static/demo/notificacoes.csv", "rb") as f:
		conteudo_base64 = base64.b64encode(f.read()).decode()
	url_dados = f"data:text/csv;base64,{conteudo_base64}"
	st.markdown(
		f'<a href="{url_dados}" download="notificacoes.csv">'
		'<button style="cursor:pointer; padding:8px 16px; border-radius:4px; border:1px solid #ccc;">'
		'Baixar CSV Notificações</button></a>', 
		unsafe_allow_html=True
	)
with col2:
	with open("./static/demo/populacao_municipal.csv", "rb") as f:
		conteudo_base64 = base64.b64encode(f.read()).decode()
	url_dados = f"data:text/csv;base64,{conteudo_base64}"
	st.markdown(
		f'<a href="{url_dados}" download="populacao_municipal.csv">'
		'<button style="cursor:pointer; padding:8px 16px; border-radius:4px; border:1px solid #ccc;">'
		'Baixar CSV População municipal</button></a>', 
		unsafe_allow_html=True
	)

# Busca todos os arquivos .r ou .R na pasta indicada
arquivos_r = sorted(glob.glob(os.path.join(path_arquivo, "*.[rR]")))

if not arquivos_r:
    st.warning(f"Nenhum arquivo .R encontrado no diretório: '{diretorio}'")
else:
    # Loop para processar e exibir cada arquivo encontrado
    for caminho_arquivo in arquivos_r:
        # Extrai apenas o nome do arquivo para usar no título
        nome_arquivo = os.path.basename(caminho_arquivo)

        try:
            # Abre e lê o conteúdo do script
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                conteudo_codigo = arquivo.read()

            # Cria um accordion individual para cada arquivo
            with st.expander(f"📄 Script: {nome_arquivo}"):
                st.code(conteudo_codigo, language="r")

        except Exception as e:
            st.error(f"Erro ao ler o arquivo {nome_arquivo}: {e}")


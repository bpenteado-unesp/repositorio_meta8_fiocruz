import streamlit as st

# 1. Defina todas as páginas do seu projeto indicando o caminho real do arquivo
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
datasets_page = st.Page("pages/datasets.py", title="Datasets públicos", icon=":material/dataset:")
preproc_page = st.Page("pages/preproc.py", title="Pré-processamento", icon=":material/auto_fix_high:")
storage_page = st.Page("pages/storage.py", title="Armazenamento", icon=":material/database:")
modeling_page = st.Page("pages/modeling.py", title="Modelagem", icon=":material/account_tree:")
dissemination_page = st.Page("pages/dissemination.py", title="Disseminação", icon=":material/campaign:")
glossary_page = st.Page("pages/glossario.py", title="Glossário", icon=":material/local_library:")


# 2. Crie a barra de navegação com a lista de páginas
pg = st.navigation([home_page, datasets_page, preproc_page, storage_page, modeling_page, dissemination_page, glossary_page])

# 3. Execute a navegação (isso vai desenhar o menu e carregar a página atual)
pg.run()
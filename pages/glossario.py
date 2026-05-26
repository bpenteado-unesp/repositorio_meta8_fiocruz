import streamlit as st
from helper import render_menu

render_menu()

st.title("Repositório Fiocruz de recursos para ciência de dados na vigilância epidemiológica")

import streamlit as st

# 1. Seus dados: termos e links/descrições associadas
termos = {
    "Analytics": "https://docs.streamlit.io/",
    "API": "https://docs.streamlit.io/develop/api-reference",
    "Banco de Dados": "Conexão com SQL e NoSQL.",
    "Botões": "Uso de st.button e st.form.",
    "Dashboard": "Exemplo prático de criação de painéis.",
    "Docker": "Empacotamento e deploy da aplicação.",
    "Deploy": "Como hospedar sua aplicação."
}

# 2. Agrupando os termos por letra inicial
indice = {}
for termo, descricao in sorted(termos.items()):
    letra = termo[0].upper()
    if letra not in indice:
        indice[letra] = []
    indice[letra].append((termo, descricao))

# 3. Criando a interface no Streamlit
st.title("📖 Índice Remissivo")
st.write("Navegue pelos termos organizados alfabeticamente.")

# Menu de atalhos no topo (opcional)
st.write("### Ir para:")
colunas = st.columns(len(indice))
for i, letra in enumerate(sorted(indice.keys())):
    with colunas[i]:
        st.markdown(f"[{letra}](#letra-{letra.lower()})", unsafe_allow_html=True)

st.divider()

# 4. Exibindo as seções com st.expander
for letra in sorted(indice.keys()):
    # Âncora HTML para o link do menu funcionar
    st.markdown(f"<div id='letra-{letra.lower()}'></div>", unsafe_allow_html=True)
    
    with st.expander(f"Letra {letra}", expanded=True):
        for termo, descricao in indice[letra]:
            if descricao.startswith("http"):
                st.markdown(f"- **{termo}**: [Acessar documentação]({descricao})")
            else:
                st.markdown(f"- **{termo}**: {descricao}")

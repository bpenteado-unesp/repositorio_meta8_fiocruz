import streamlit as st
import pandas as pd

def render_menu():
	st.logo("https://rondonia.fiocruz.br/wp-content/uploads/2024/12/marcafiocruz_horizontal_POSITIVA_24052024-scaled-1.jpg", size="small")
	st.sidebar.page_link("pages/home.py", label="Home", icon="🏠")
	st.sidebar.page_link("pages/datasets.py", label="Dados públicos", icon=":material/dataset:")
	st.sidebar.page_link("pages/preproc.py", label="Pré-processamento", icon=":material/auto_fix_high:")
	st.sidebar.page_link("pages/storage.py", label="Armazenamento", icon=":material/database:")
	st.sidebar.page_link("pages/modeling.py", label="Modelagem", icon=":material/account_tree:")
	st.sidebar.page_link("pages/dissemination.py", label="Disseminação", icon=":material/campaign:")
	st.sidebar.page_link("pages/tools.py", label="Desenvolvimento", icon=":material/code:")
	st.sidebar.divider()
	st.sidebar.page_link("pages/glossario.py", label="Glossário de termos", icon=":material/dictionary:")

	# Injeta CSS para ajustar a largura e altura do logo
	st.markdown(
		"""
		<style>
			/* 1. Alinha a caixa do cabeçalho ao centro */
			[data-testid="stSidebarHeader"] {
				height: auto !important;
				padding-bottom: 20px !important;
				display: flex !important;
				justify-content: center !important; /* Centraliza na horizontal */
				align-items: center !important;     /* Centraliza na vertical */
			}
			
			/* 2. Garante que a imagem se comporte bem ao centro */
			[data-testid="stSidebarHeader"] img {
				width: 180px !important;  /* Ajuste a largura como quiser */
				height: auto !important;
				max-height: none !important;
				margin: 0 auto !important; /* Força margens iguais nas laterais */
			}
		</style>
		""",
		unsafe_allow_html=True,
	)

def carregar_dados(path_arquivo):
	try:
		df = pd.read_excel(path_arquivo)
		return df
	except FileNotFoundError:
		st.error(f"Error: Arquivo não encontrado.")
	except Exception as e:
		st.error(f"Ocorreu um erro inesperado: {e}")

def carregar_ordenacao(df):
	opcoes_ranking = {
		"Ranking Geral": "rank_balanceado",
		"Ranking de Popularidade": "rank_popularidade_geral",
		"Ranking de Uso Institucional": "rank_uso_institucional_ve",
		"Ranking de Especificidade para a VE": "rank_especificidade_ve",
		"Ranking de Adequação à VE": "rank_adequacao_informes"
	}
	# Selectbox para escolha do ranking
	ranking_selecionado = st.selectbox(
		"Ordenar por:",
		options=list(opcoes_ranking.keys())
	)

	ascending_bool = True 
	
	# Mapeia qual é a coluna correspondente no Excel
	coluna_ordenacao = opcoes_ranking[ranking_selecionado]
	
	# 2. ORDENAÇÃO DINÂMICA DO DATAFRAME
	if coluna_ordenacao in df.columns:
		# Converte temporariamente para numérico ao ordenar caso os dados tenham vindo como texto
		df[coluna_ordenacao] = pd.to_numeric(df[coluna_ordenacao], errors='coerce')
		df = df.sort_values(by=coluna_ordenacao, ascending=ascending_bool).reset_index(drop=True)

	return df

def carregar_quadro_sintese(path_arquivo):
	# Customização de cor do expander (Collapse) via CSS
	st.html("""
		<style>
			/* Altera o bloco inteiro do expander */
			details {
				background-color: #ececff !important;  /* Fundo cinza bem claro */
				border: 2px solid #1E88E5 !important;   /* Borda Azul */
				border-radius: 8px !important;
				padding: 5px 15px !important;
			}
			
			/* Altera o texto do cabeçalho que o usuário clica */
			summary {
				color: #000000 !important;             /* Texto em Azul */
				font-weight: bold !important;
				font-size: 1.1rem !important;
			}
		/* #  Injeção de CSS customizado para a tabela */
		/* Estiliza o container da tabela e força bordas arredondadas */
		.stTable {
			border-collapse: collapse !important;
			width: 100% !important;
			border-radius: 8px !important;
			overflow: hidden !important;
			box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
		}

		/* Estiliza o cabeçalho (TH) da tabela */
		.stTable thead tr th {
			background-color: #1E88E5 !important; /* Fundo Azul Escuro */
			color: white !important;                /* Texto Branco */
			font-weight: bold !important;
			padding: 12px 15px !important;
			text-align: left !important;
		}

		/* Estiliza as células comuns (TD) */
		.stTable tbody tr td {
			padding: 10px 15px !important;
			border-bottom: 1px solid #E0E0E0 !important; /* Linha divisória fina */
			color: #333333 !important;
		}

		/* Cria o efeito de linhas alternadas (Zebra) */
		.stTable tbody tr:nth-child(even) {
			background-color: #F8F9FA !important;
		}

		/* Efeito visual ao passar o mouse por cima da linha */
		.stTable tbody tr:hover {
			background-color: #E3F2FD !important;
			transition: background-color 0.2s ease !important;
		}
	</style>
	""")
	# carrega os clusters de uso
	try:
		df = pd.read_excel(path_arquivo, sheet_name="sugestao_por_produto")
		# Renomeia colunas específicas
		df_renomeado = df.rename(columns={
			'cenario': 'Cenário',
			'ferramentas_sugeridas': 'Sugestões',
			'quando_usar': 'Quando usar'
		})
		st.table(df_renomeado[['Cenário','Sugestões', 'Quando usar']])
		return df_renomeado
	except FileNotFoundError:
		st.error(f"Error: Arquivo não encontrado.")
	except Exception as e:
		st.error(f"Ocorreu um erro inesperado: {e}")

@st.dialog("Detalhes da ferramenta")
def mostrar_detalhes(linha_dados):
    # Conteúdo detalhado dentro do modal
    st.image(f"{linha_dados['thumbnail_url']}")
    st.write(f"### {linha_dados['ferramenta']}")
    st.write(f"##### *Categoria:* {linha_dados['categoria']}")
    st.divider()
    st.write(f"**Escopo:** {linha_dados['escopo']}")
    st.divider()
    st.write(f"**Possíveis aplicações na VE:** `{linha_dados['casos_de_aplicacao_na_area']}`")
    st.divider()
    st.write(f"**Público-alvo:** {linha_dados['publico_alvo']}")
    
    # Botão manual para fechar o modal (além do 'X' nativo no canto superior)
    if st.button("Fechar Janela", type="secondary"):
        st.rerun()
        
def popular_retorno(dados):
	# st.dataframe(dados)
	
	if dados is not None:
		cols = st.columns(3)

		for index, row in dados.iterrows():
			col_idx = index % 3
			with cols[col_idx]:
				# Cria um container com borda que funciona como card
				with st.container(border=True):

                    # Layout: Thumbnail e Título lado a lado
					sub_col_img, sub_col_titulo = st.columns([2,8], vertical_alignment="center")
					
					with sub_col_img:
						caminho_imagem = row['thumbnail_url']
						if pd.notna(caminho_imagem) and str(caminho_imagem).strip() != "":
							try:
								st.image(caminho_imagem, width=64)
							except Exception:
								st.caption("⚠️ Erro")
						else:
							st.caption("🖼️ Sem foto")
                            
					with sub_col_titulo:
						st.markdown(f"### {row['ferramenta']}")

					#st.markdown(f"### {row['ferramenta']}")
					#st.image(f"{row['thumbnail_url']}")
					st.write(f"**Tipo:** {row['tipo']}")
					st.write(f"**Descrição:** {row['conteudo_principal']}")
					st.write(f"**Link:** {row['fonte']}")
					st.write(f"###### *{row['generica_ou_especifica_ve']}*")
					st.write(f"###### *{row['gratuita_ou_paga']}*")
					
					# Exemplo de adicionar um elemento interativo dentro do card
					submit = st.button("Ver Detalhes", key=f"btn_{index}")
					
					# É OBRIGATÓRIO passar uma chave única (key) para cada botão no loop
					if submit:
						# Dispara a função do modal passando os dados específicos da linha
						mostrar_detalhes(row)
	else:
		st.error(f"Não existem dados a serem mostrados")

def buscar(texto, df):
	dados_filtrados = df[
		df['ferramenta'].str.contains(texto, case=False, na=False) |
		df['categoria'].str.contains(texto, case=False, na=False) |
		df['conteudo_principal'].str.contains(texto, case=False, na=False)
	]
	return dados_filtrados

def exibe_dados(path_arquivo):
	with st.expander(":green-background[Clique para ver possíveis cenários de uso]"):
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
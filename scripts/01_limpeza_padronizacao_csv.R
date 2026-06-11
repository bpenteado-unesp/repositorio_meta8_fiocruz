# ============================================================
# CENARIO 01 - TAREFA CORRIQUEIRA
# Limpeza e padronizacao de bases epidemiologicas a partir de CSV
# Fonte de dados: arquivo CSV local
# Ambiente sugerido: RStudio
# ============================================================

# ------------------------------------------------------------
# 0. Objetivo do script
# ------------------------------------------------------------
# Este script recebe uma base epidemiologica em CSV e realiza uma
# limpeza inicial. A proposta e transformar uma base bruta, com
# possiveis inconsistencias de escrita, datas, categorias e idades,
# em uma base minimamente padronizada para analises posteriores.
#
# Exemplos de problemas tratados:
# - nomes de colunas em formatos diferentes;
# - nomes de municipios com acentos, espacos ou letras minusculas;
# - categorias de sexo escritas de formas diferentes;
# - datas em formato texto;
# - idades impossiveis ou fora de faixa plausivel;
# - criacao de faixas etarias.

# ------------------------------------------------------------
# 1. Preparacao do ambiente
# ------------------------------------------------------------
# Execute install.packages(...) apenas uma vez, se os pacotes ainda
# nao estiverem instalados no computador.

# install.packages(c("tidyverse", "lubridate", "janitor", "stringi"))

library(tidyverse)  # manipulacao de dados, leitura de CSV e escrita de saidas
library(lubridate)  # tratamento de datas
library(janitor)    # limpeza de nomes de colunas
library(stringi)    # remocao de acentos e normalizacao textual

# ------------------------------------------------------------
# 2. Definicao dos caminhos de entrada e saida
# ------------------------------------------------------------
# Ajuste o caminho do arquivo conforme a organizacao do seu projeto.
# Recomenda-se criar uma pasta chamada "dados" e colocar o CSV nela.

arquivo_entrada <- "dados/notificacoes.csv"
pasta_saida <- "saida/01_limpeza_padronizacao_csv"

dir.create(pasta_saida, recursive = TRUE, showWarnings = FALSE)

# ------------------------------------------------------------
# 3. Ingestao dos dados
# ------------------------------------------------------------
# A funcao read_csv() le o arquivo CSV. O argumento show_col_types = FALSE
# evita mensagens extensas sobre tipos de colunas no console.

notificacoes_brutas <- read_csv(
  file = arquivo_entrada,
  locale = locale(encoding = "UTF-8"),
  show_col_types = FALSE
)

# Inspecao inicial: ajuda o aluno a entender a estrutura da base.
glimpse(notificacoes_brutas)

# ------------------------------------------------------------
# 4. Preparacao e limpeza dos dados
# ------------------------------------------------------------
# A funcao clean_names() padroniza nomes de colunas para snake_case.
# Exemplo: "Data Notificacao" vira "data_notificacao".

notificacoes_limpas <- notificacoes_brutas %>%
  clean_names() %>%
  mutate(
    # Padronizacao do municipio:
    # - remove espacos extras;
    # - converte para letras maiusculas;
    # - remove acentos.
    municipio = municipio %>%
      str_trim() %>%
      str_to_upper() %>%
      stri_trans_general("Latin-ASCII"),

    # Padronizacao da UF.
    uf = uf %>%
      str_trim() %>%
      str_to_upper(),

    # Padronizacao de campos textuais relevantes.
    sexo = sexo %>% str_trim() %>% str_to_upper(),
    cid = cid %>% str_trim() %>% str_to_upper(),
    classificacao_final = classificacao_final %>% str_trim() %>% str_to_upper(),
    evolucao = evolucao %>% str_trim() %>% str_to_upper()
  ) %>%
  mutate(
    # Recodificacao da variavel sexo para categorias mais consistentes.
    sexo = case_when(
      sexo %in% c("M", "MASC", "MASCULINO") ~ "MASCULINO",
      sexo %in% c("F", "FEM", "FEMININO") ~ "FEMININO",
      sexo %in% c("I", "IGN", "IGNORADO", "NAO INFORMADO", "N/I") ~ "IGNORADO",
      is.na(sexo) | sexo == "" ~ "IGNORADO",
      TRUE ~ sexo
    )
  ) %>%
  mutate(
    # Conversao de datas.
    # dmy() assume o formato dia/mes/ano. Se sua base estiver em ano-mes-dia,
    # troque dmy() por ymd().
    data_notificacao = dmy(data_notificacao),
    data_sintomas = dmy(data_sintomas)
  ) %>%
  mutate(
    # Conversao da idade para numerico e remocao de valores improvaveis.
    idade = as.numeric(idade),
    idade = if_else(idade < 0 | idade > 120, NA_real_, idade),

    # Criacao de faixa etaria. As faixas podem ser alteradas conforme o agravo.
    faixa_etaria = case_when(
      is.na(idade) ~ "IGNORADA",
      idade < 1 ~ "<1 ANO",
      idade <= 4 ~ "1 A 4",
      idade <= 9 ~ "5 A 9",
      idade <= 19 ~ "10 A 19",
      idade <= 39 ~ "20 A 39",
      idade <= 59 ~ "40 A 59",
      idade >= 60 ~ "60+"
    )
  )

# ------------------------------------------------------------
# 5. Validacao da limpeza
# ------------------------------------------------------------
# A validacao nao prova que a base esta perfeita. Ela apenas fornece
# indicadores iniciais de qualidade para orientar a revisao.

resumo_validacao <- tibble(
  total_registros = nrow(notificacoes_limpas),
  datas_notificacao_ausentes = sum(is.na(notificacoes_limpas$data_notificacao)),
  datas_sintomas_ausentes = sum(is.na(notificacoes_limpas$data_sintomas)),
  municipios_ausentes = sum(is.na(notificacoes_limpas$municipio) | notificacoes_limpas$municipio == ""),
  idades_ausentes = sum(is.na(notificacoes_limpas$idade)),
  sexo_ignorado = sum(notificacoes_limpas$sexo == "IGNORADO", na.rm = TRUE)
)

print(resumo_validacao)

# ------------------------------------------------------------
# 6. Exportacao dos resultados
# ------------------------------------------------------------
# A base limpa sera usada por outros scripts do fluxo.

write_csv(notificacoes_limpas, file.path(pasta_saida, "notificacoes_limpa_padronizada.csv"))
write_csv(resumo_validacao, file.path(pasta_saida, "resumo_validacao_limpeza.csv"))

# Fim do script.

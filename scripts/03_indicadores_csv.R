# ============================================================
# CENARIO 03 - TAREFA CORRIQUEIRA
# Geracao de indicadores epidemiologicos basicos a partir de CSV
# Fonte de dados: arquivo CSV local
# Ambiente sugerido: RStudio
# ============================================================

# ------------------------------------------------------------
# 0. Objetivo do script
# ------------------------------------------------------------
# Este script calcula indicadores epidemiologicos simples, como:
# - numero de notificacoes;
# - casos confirmados;
# - obitos;
# - incidencia por 100 mil habitantes;
# - mortalidade por 100 mil habitantes;
# - letalidade percentual;
# - positividade de testes.
#
# Ele pressupoe uma base de notificacoes e uma base populacional.

# ------------------------------------------------------------
# 1. Preparacao do ambiente
# ------------------------------------------------------------

# install.packages(c("tidyverse", "lubridate", "janitor"))

library(tidyverse)
library(lubridate)
library(janitor)

# ------------------------------------------------------------
# 2. Caminhos
# ------------------------------------------------------------

arquivo_notificacoes <- "dados/notificacoes.csv"
arquivo_populacao <- "dados/populacao_municipal.csv"
pasta_saida <- "saida/03_indicadores_csv"
dir.create(pasta_saida, recursive = TRUE, showWarnings = FALSE)

# ------------------------------------------------------------
# 3. Ingestao dos dados
# ------------------------------------------------------------
# A base populacional deve conter pelo menos:
# municipio, uf, populacao.

notificacoes <- read_csv(arquivo_notificacoes, show_col_types = FALSE) %>%
  clean_names()

populacao <- read_csv(arquivo_populacao, show_col_types = FALSE) %>%
  clean_names()

# ------------------------------------------------------------
# 4. Preparacao dos dados
# ------------------------------------------------------------

notificacoes_prep <- notificacoes %>%
  mutate(
    data_notificacao = dmy(data_notificacao),
    ano = year(data_notificacao),
    mes = month(data_notificacao),
    semana_epidemiologica = isoweek(data_notificacao),

    municipio = str_to_upper(str_trim(municipio)),
    uf = str_to_upper(str_trim(uf)),

    classificacao_final = str_to_upper(str_trim(classificacao_final)),
    evolucao = str_to_upper(str_trim(evolucao)),
    resultado_teste = str_to_upper(str_trim(resultado_teste)),

    caso_confirmado = classificacao_final %in% c(
      "CONFIRMADO",
      "CONFIRMADO LABORATORIAL",
      "CONFIRMADO CLINICO",
      "CONFIRMADO CLINICO-EPIDEMIOLOGICO"
    ),

    obito = evolucao %in% c("OBITO", "OBITO PELO AGRAVO"),

    teste_realizado = !is.na(resultado_teste) & resultado_teste != "",

    teste_positivo = resultado_teste %in% c(
      "POSITIVO",
      "DETECTAVEL",
      "REAGENTE"
    )
  )

populacao_prep <- populacao %>%
  mutate(
    municipio = str_to_upper(str_trim(municipio)),
    uf = str_to_upper(str_trim(uf)),
    populacao = as.numeric(populacao)
  )

# ------------------------------------------------------------
# 5. Calculo dos indicadores
# ------------------------------------------------------------
# A agregacao abaixo gera indicadores mensais por municipio.
# Se quiser indicadores semanais, inclua semana_epidemiologica no group_by().

indicadores_municipais <- notificacoes_prep %>%
  group_by(uf, municipio, ano, mes) %>%
  summarise(
    notificacoes = n(),
    casos_confirmados = sum(caso_confirmado, na.rm = TRUE),
    obitos = sum(obito, na.rm = TRUE),
    testes_realizados = sum(teste_realizado, na.rm = TRUE),
    testes_positivos = sum(teste_positivo, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  left_join(populacao_prep, by = c("uf", "municipio")) %>%
  mutate(
    incidencia_100mil = if_else(populacao > 0, casos_confirmados / populacao * 100000, NA_real_),
    mortalidade_100mil = if_else(populacao > 0, obitos / populacao * 100000, NA_real_),
    letalidade_percentual = if_else(casos_confirmados > 0, obitos / casos_confirmados * 100, NA_real_),
    positividade_percentual = if_else(testes_realizados > 0, testes_positivos / testes_realizados * 100, NA_real_)
  ) %>%
  mutate(
    across(
      c(incidencia_100mil, mortalidade_100mil, letalidade_percentual, positividade_percentual),
      ~ round(.x, 2)
    )
  )

# ------------------------------------------------------------
# 6. Validacao
# ------------------------------------------------------------

resumo_validacao <- indicadores_municipais %>%
  summarise(
    municipios_analisados = n_distinct(municipio),
    linhas_com_populacao_ausente = sum(is.na(populacao)),
    total_notificacoes = sum(notificacoes, na.rm = TRUE),
    total_casos_confirmados = sum(casos_confirmados, na.rm = TRUE),
    total_obitos = sum(obitos, na.rm = TRUE)
  )

print(resumo_validacao)

# ------------------------------------------------------------
# 7. Exportacao
# ------------------------------------------------------------

write_csv(indicadores_municipais, file.path(pasta_saida, "indicadores_municipais.csv"))
write_csv(resumo_validacao, file.path(pasta_saida, "resumo_validacao_indicadores.csv"))

# Fim do script.

# ============================================================
# CENARIO 05 - TAREFA CORRIQUEIRA
# Identificacao de inconsistencias e subnotificacoes aparentes
# Fonte de dados: arquivo CSV local
# Ambiente sugerido: RStudio
# ============================================================

# ------------------------------------------------------------
# 0. Objetivo do script
# ------------------------------------------------------------
# Este script busca sinais simples de problemas de qualidade dos dados:
# - registros duplicados;
# - campos obrigatorios ausentes;
# - datas incoerentes;
# - atraso entre inicio de sintomas e notificacao;
# - quedas bruscas no volume semanal de notificacoes.
#
# Importante: uma queda brusca nao prova subnotificacao. Ela apenas
# indica um ponto que merece investigacao pela equipe de vigilancia.

# ------------------------------------------------------------
# 1. Preparacao do ambiente
# ------------------------------------------------------------

# install.packages(c("tidyverse", "lubridate", "janitor", "zoo"))

library(tidyverse)
library(lubridate)
library(janitor)
library(zoo)

# ------------------------------------------------------------
# 2. Caminhos
# ------------------------------------------------------------

arquivo_entrada <- "dados/notificacoes.csv"
pasta_saida <- "saida/05_inconsistencias_csv"
dir.create(pasta_saida, recursive = TRUE, showWarnings = FALSE)

# ------------------------------------------------------------
# 3. Ingestao
# ------------------------------------------------------------

dados <- read_csv(arquivo_entrada, show_col_types = FALSE) %>%
  clean_names()

# ------------------------------------------------------------
# 4. Preparacao
# ------------------------------------------------------------

dados_prep <- dados %>%
  mutate(
    data_notificacao = dmy(data_notificacao),
    data_sintomas = dmy(data_sintomas),
    atraso_notificacao_dias = as.numeric(data_notificacao - data_sintomas),
    ano = year(data_notificacao),
    semana_epidemiologica = isoweek(data_notificacao),
    classificacao_final = str_to_upper(str_trim(classificacao_final)),
    caso_confirmado = classificacao_final %in% c("CONFIRMADO", "CONFIRMADO LABORATORIAL", "CONFIRMADO CLINICO")
  )

# ------------------------------------------------------------
# 5. Analises de qualidade
# ------------------------------------------------------------

# 5.1 Duplicidades por identificador da notificacao.
duplicados_id <- dados_prep %>%
  filter(duplicated(id_notificacao) | duplicated(id_notificacao, fromLast = TRUE)) %>%
  arrange(id_notificacao)

# 5.2 Campos obrigatorios ausentes.
campos_obrigatorios <- c(
  "id_notificacao",
  "data_notificacao",
  "municipio",
  "sexo",
  "idade",
  "classificacao_final"
)

ausencia_campos <- dados_prep %>%
  summarise(
    across(
      all_of(campos_obrigatorios),
      ~ sum(is.na(.x) | .x == ""),
      .names = "ausentes_{.col}"
    )
  ) %>%
  pivot_longer(
    cols = everything(),
    names_to = "campo",
    values_to = "total_ausente"
  )

# 5.3 Datas incoerentes.
datas_incoerentes <- dados_prep %>%
  filter(
    data_sintomas > data_notificacao |
      data_notificacao > Sys.Date() |
      atraso_notificacao_dias < 0
  )

# 5.4 Atrasos de notificacao por categoria.
atrasos_notificacao <- dados_prep %>%
  filter(!is.na(atraso_notificacao_dias)) %>%
  mutate(
    categoria_atraso = case_when(
      atraso_notificacao_dias <= 2 ~ "0 A 2 DIAS",
      atraso_notificacao_dias <= 7 ~ "3 A 7 DIAS",
      atraso_notificacao_dias <= 14 ~ "8 A 14 DIAS",
      atraso_notificacao_dias > 14 ~ "MAIS DE 14 DIAS"
    )
  ) %>%
  count(categoria_atraso, sort = TRUE)

# 5.5 Quedas aparentes de notificacao.
serie_semanal <- dados_prep %>%
  group_by(ano, semana_epidemiologica) %>%
  summarise(
    notificacoes = n(),
    casos_confirmados = sum(caso_confirmado, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(ano, semana_epidemiologica) %>%
  mutate(
    media_movel_4_sem = rollmean(notificacoes, k = 4, fill = NA, align = "right"),
    variacao_percentual = (notificacoes - lag(notificacoes)) / lag(notificacoes) * 100,
    possivel_queda_subnotificacao = variacao_percentual <= -50
  )

quedas_aparentes <- serie_semanal %>%
  filter(possivel_queda_subnotificacao == TRUE)

# ------------------------------------------------------------
# 6. Resumo de validacao
# ------------------------------------------------------------

resumo_qualidade <- tibble(
  total_registros = nrow(dados_prep),
  total_duplicados_id = nrow(duplicados_id),
  total_datas_incoerentes = nrow(datas_incoerentes),
  atraso_medio_notificacao = mean(dados_prep$atraso_notificacao_dias, na.rm = TRUE),
  atraso_mediano_notificacao = median(dados_prep$atraso_notificacao_dias, na.rm = TRUE),
  semanas_com_queda_aparente = nrow(quedas_aparentes)
)

print(resumo_qualidade)

# ------------------------------------------------------------
# 7. Exportacao
# ------------------------------------------------------------

write_csv(duplicados_id, file.path(pasta_saida, "registros_duplicados_id.csv"))
write_csv(ausencia_campos, file.path(pasta_saida, "ausencia_campos_obrigatorios.csv"))
write_csv(datas_incoerentes, file.path(pasta_saida, "datas_incoerentes.csv"))
write_csv(atrasos_notificacao, file.path(pasta_saida, "atrasos_notificacao.csv"))
write_csv(serie_semanal, file.path(pasta_saida, "serie_semanal_qualidade.csv"))
write_csv(quedas_aparentes, file.path(pasta_saida, "quedas_aparentes_subnotificacao.csv"))
write_csv(resumo_qualidade, file.path(pasta_saida, "resumo_qualidade_dados.csv"))

# Fim do script.

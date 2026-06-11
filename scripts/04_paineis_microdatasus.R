# ============================================================
# CENARIO 04 - TAREFA CORRIQUEIRA
# Construcao de paineis e relatorios descritivos com microdatasus
# Fonte de dados: DATASUS via pacote microdatasus
# Ambiente sugerido: RStudio
# ============================================================

# ------------------------------------------------------------
# 0. Objetivo do script
# ------------------------------------------------------------
# Este script baixa dados do SIH-RD via microdatasus e gera tabelas
# e graficos descritivos para acompanhamento epidemiologico.
# A proposta e servir como base para relatorios ou paineis simples.

# ------------------------------------------------------------
# 1. Preparacao do ambiente
# ------------------------------------------------------------

# install.packages(c("tidyverse", "lubridate", "janitor", "microdatasus"))

library(tidyverse)
library(lubridate)
library(janitor)
library(microdatasus)

# ------------------------------------------------------------
# 2. Parametros do recorte
# ------------------------------------------------------------

uf_interesse <- "SP"
ano_inicio <- 2023
ano_fim <- 2023
mes_inicio <- 1
mes_fim <- 6

pasta_saida <- "saida/04_paineis_microdatasus"
pasta_graficos <- file.path(pasta_saida, "graficos")
dir.create(pasta_graficos, recursive = TRUE, showWarnings = FALSE)

# ------------------------------------------------------------
# 3. Ingestao dos dados
# ------------------------------------------------------------

sih_bruto <- fetch_datasus(
  year_start = ano_inicio,
  year_end = ano_fim,
  month_start = mes_inicio,
  month_end = mes_fim,
  uf = uf_interesse,
  information_system = "SIH-RD"
)

sih <- process_sih(sih_bruto) %>%
  clean_names()

# ------------------------------------------------------------
# 4. Preparacao dos dados
# ------------------------------------------------------------

sih_prep <- sih %>%
  mutate(
    data_referencia = suppressWarnings(ymd(dt_inter)),
    ano = year(data_referencia),
    mes = month(data_referencia),
    idade = as.numeric(idade),
    valor_total = as.numeric(valor_tot),
    dias_permanencia = as.numeric(dias_perm),
    obito_hospitalar = as.numeric(morte),
    cid_principal = str_to_upper(str_trim(diag_princ)),
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
# 5. Tabelas descritivas para painel
# ------------------------------------------------------------

serie_mensal <- sih_prep %>%
  group_by(ano, mes) %>%
  summarise(
    internacoes = n(),
    obitos_hospitalares = sum(obito_hospitalar, na.rm = TRUE),
    valor_total = sum(valor_total, na.rm = TRUE),
    dias_permanencia = sum(dias_permanencia, na.rm = TRUE),
    .groups = "drop"
  )

top_municipios <- sih_prep %>%
  count(munic_res, sort = TRUE) %>%
  rename(internacoes = n) %>%
  slice_max(internacoes, n = 10)

top_cids <- sih_prep %>%
  count(cid_principal, sort = TRUE) %>%
  rename(internacoes = n) %>%
  slice_max(internacoes, n = 10)

por_faixa_etaria <- sih_prep %>%
  count(faixa_etaria, sort = TRUE) %>%
  rename(internacoes = n)

# ------------------------------------------------------------
# 6. Graficos
# ------------------------------------------------------------

grafico_serie <- ggplot(serie_mensal, aes(x = mes, y = internacoes)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Internacoes por mes",
    x = "Mes",
    y = "Internacoes"
  ) +
  theme_minimal()

ggsave(file.path(pasta_graficos, "internacoes_por_mes.png"), grafico_serie, width = 10, height = 6)

grafico_municipios <- ggplot(top_municipios, aes(x = reorder(munic_res, internacoes), y = internacoes)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Top 10 municipios por internacoes",
    x = "Municipio de residencia",
    y = "Internacoes"
  ) +
  theme_minimal()

ggsave(file.path(pasta_graficos, "top10_municipios.png"), grafico_municipios, width = 10, height = 6)

grafico_cids <- ggplot(top_cids, aes(x = reorder(cid_principal, internacoes), y = internacoes)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Top 10 CIDs principais",
    x = "CID principal",
    y = "Internacoes"
  ) +
  theme_minimal()

ggsave(file.path(pasta_graficos, "top10_cids.png"), grafico_cids, width = 10, height = 6)

# ------------------------------------------------------------
# 7. Validacao e exportacao
# ------------------------------------------------------------

resumo_validacao <- tibble(
  total_registros = nrow(sih_prep),
  meses_analisados = n_distinct(sih_prep$mes),
  municipios_distintos = n_distinct(sih_prep$munic_res),
  cids_distintos = n_distinct(sih_prep$cid_principal),
  obitos_hospitalares = sum(sih_prep$obito_hospitalar, na.rm = TRUE)
)

write_csv(serie_mensal, file.path(pasta_saida, "serie_mensal.csv"))
write_csv(top_municipios, file.path(pasta_saida, "top10_municipios.csv"))
write_csv(top_cids, file.path(pasta_saida, "top10_cids.csv"))
write_csv(por_faixa_etaria, file.path(pasta_saida, "internacoes_por_faixa_etaria.csv"))
write_csv(resumo_validacao, file.path(pasta_saida, "resumo_validacao_painel.csv"))

# Fim do script.

# ============================================================
# CENARIO 06 - TAREFA INTERMEDIARIA
# Analise espaco-temporal de casos/internacoes usando microdatasus
# Fonte de dados: DATASUS via pacote microdatasus
# Ambiente sugerido: RStudio
# ============================================================

# ------------------------------------------------------------
# 0. Objetivo do script
# ------------------------------------------------------------
# Este script realiza uma analise espaco-temporal simples a partir
# de dados do SIH-RD obtidos pelo microdatasus. O foco e observar
# como eventos de interesse se distribuem por municipio e por tempo.
#
# Como exemplo, usamos internacoes hospitalares. Em vigilancia
# epidemiologica, a mesma logica poderia ser aplicada a notificacoes,
# casos confirmados, obitos ou exames positivos.
#
# Resultados esperados:
# - serie temporal mensal;
# - ranking de municipios;
# - matriz municipio x mes;
# - identificacao de municipios com maior concentracao de eventos;
# - grafico de tendencia temporal.

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
mes_fim <- 12

pasta_saida <- "saida/06_analise_espaco_temporal_microdatasus"
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
    municipio_residencia = munic_res,
    cid_principal = str_to_upper(str_trim(diag_princ))
  ) %>%
  filter(!is.na(ano), !is.na(mes), !is.na(municipio_residencia))

# ------------------------------------------------------------
# 5. Analise espaco-temporal
# ------------------------------------------------------------

# 5.1 Serie temporal geral por mes.
serie_mensal_uf <- sih_prep %>%
  group_by(ano, mes) %>%
  summarise(
    eventos = n(),
    .groups = "drop"
  ) %>%
  arrange(ano, mes)

# 5.2 Eventos por municipio e mes.
municipio_mes <- sih_prep %>%
  group_by(municipio_residencia, ano, mes) %>%
  summarise(
    eventos = n(),
    .groups = "drop"
  )

# 5.3 Ranking geral de municipios.
ranking_municipios <- municipio_mes %>%
  group_by(municipio_residencia) %>%
  summarise(
    total_eventos = sum(eventos, na.rm = TRUE),
    meses_com_evento = n_distinct(mes[eventos > 0]),
    media_mensal = mean(eventos, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(total_eventos))

# 5.4 Matriz municipio x mes para facilitar leitura em planilha.
matriz_municipio_mes <- municipio_mes %>%
  unite("ano_mes", ano, mes, sep = "_") %>%
  pivot_wider(
    names_from = ano_mes,
    values_from = eventos,
    values_fill = 0
  )

# 5.5 Identificacao simples de concentracao territorial.
# Aqui marcamos municipios no quartil superior de eventos.
limiar_q75 <- quantile(ranking_municipios$total_eventos, probs = 0.75, na.rm = TRUE)

municipios_maior_concentracao <- ranking_municipios %>%
  mutate(
    grupo_concentracao = if_else(total_eventos >= limiar_q75, "MAIOR CONCENTRACAO", "DEMAIS MUNICIPIOS")
  ) %>%
  filter(grupo_concentracao == "MAIOR CONCENTRACAO")

# ------------------------------------------------------------
# 6. Visualizacoes
# ------------------------------------------------------------

grafico_serie <- ggplot(serie_mensal_uf, aes(x = mes, y = eventos)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Serie temporal mensal de eventos",
    x = "Mes",
    y = "Eventos"
  ) +
  theme_minimal()

ggsave(file.path(pasta_graficos, "serie_temporal_mensal.png"), grafico_serie, width = 10, height = 6)

grafico_top_municipios <- ranking_municipios %>%
  slice_max(total_eventos, n = 15) %>%
  ggplot(aes(x = reorder(municipio_residencia, total_eventos), y = total_eventos)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Municipios com maior numero de eventos",
    x = "Municipio",
    y = "Total de eventos"
  ) +
  theme_minimal()

ggsave(file.path(pasta_graficos, "top15_municipios_eventos.png"), grafico_top_municipios, width = 10, height = 7)

# ------------------------------------------------------------
# 7. Validacao
# ------------------------------------------------------------

resumo_validacao <- tibble(
  total_registros = nrow(sih_prep),
  municipios_analisados = n_distinct(sih_prep$municipio_residencia),
  meses_analisados = n_distinct(sih_prep$mes),
  total_eventos_serie = sum(serie_mensal_uf$eventos, na.rm = TRUE),
  municipios_maior_concentracao = nrow(municipios_maior_concentracao)
)

print(resumo_validacao)

# ------------------------------------------------------------
# 8. Exportacao
# ------------------------------------------------------------

write_csv(serie_mensal_uf, file.path(pasta_saida, "serie_mensal_uf.csv"))
write_csv(municipio_mes, file.path(pasta_saida, "eventos_por_municipio_mes.csv"))
write_csv(ranking_municipios, file.path(pasta_saida, "ranking_municipios.csv"))
write_csv(matriz_municipio_mes, file.path(pasta_saida, "matriz_municipio_mes.csv"))
write_csv(municipios_maior_concentracao, file.path(pasta_saida, "municipios_maior_concentracao.csv"))
write_csv(resumo_validacao, file.path(pasta_saida, "resumo_validacao_espaco_temporal.csv"))

# Fim do script.

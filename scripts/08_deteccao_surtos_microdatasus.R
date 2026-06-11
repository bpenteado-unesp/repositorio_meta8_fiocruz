# ============================================================
# CENARIO 08 - TAREFA AVANCADA
# Deteccao automatica de surtos ou anomalias epidemiologicas
# Fonte de dados: DATASUS via pacote microdatasus
# Ambiente sugerido: RStudio
# ============================================================

# ------------------------------------------------------------
# 0. Objetivo do script
# ------------------------------------------------------------
# Este script cria um mecanismo simples de deteccao de anomalias
# em series temporais agregadas. Ele usa dados do SIH-RD via
# microdatasus e identifica meses em que o numero de eventos fica
# muito acima do comportamento historico recente.
#
# Importante:
# - Um alerta estatistico nao confirma surto.
# - O resultado deve ser interpretado por equipe tecnica.
# - Atraso de notificacao, mudanca de sistema e feriados podem gerar
#   falsos alertas.

# ------------------------------------------------------------
# 1. Preparacao do ambiente
# ------------------------------------------------------------

# install.packages(c("tidyverse", "lubridate", "janitor", "microdatasus", "zoo"))

library(tidyverse)
library(lubridate)
library(janitor)
library(microdatasus)
library(zoo)

# ------------------------------------------------------------
# 2. Parametros
# ------------------------------------------------------------

uf_interesse <- "SP"
ano_inicio <- 2022
ano_fim <- 2023
mes_inicio <- 1
mes_fim <- 12

# Opcional: filtrar por prefixo de CID.
# Exemplo: "J" para algumas doencas respiratorias no CID-10.
# Deixe NULL para nao filtrar.
prefixo_cid_interesse <- NULL

pasta_saida <- "saida/08_deteccao_surtos_microdatasus"
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
    cid_principal = str_to_upper(str_trim(diag_princ)),
    ano_mes = floor_date(data_referencia, unit = "month")
  ) %>%
  filter(!is.na(ano_mes), !is.na(municipio_residencia))

if (!is.null(prefixo_cid_interesse)) {
  sih_prep <- sih_prep %>%
    filter(str_starts(cid_principal, prefixo_cid_interesse))
}

# ------------------------------------------------------------
# 5. Serie temporal por municipio
# ------------------------------------------------------------

serie_municipal <- sih_prep %>%
  count(municipio_residencia, ano_mes, name = "eventos") %>%
  group_by(municipio_residencia) %>%
  complete(
    ano_mes = seq.Date(min(sih_prep$ano_mes), max(sih_prep$ano_mes), by = "month"),
    fill = list(eventos = 0)
  ) %>%
  arrange(municipio_residencia, ano_mes) %>%
  ungroup()

# ------------------------------------------------------------
# 6. Deteccao de anomalias
# ------------------------------------------------------------
# Estrategia usada:
# - calcula media movel dos 6 meses anteriores;
# - calcula desvio padrao movel dos 6 meses anteriores;
# - gera alerta quando o valor observado supera media + 2 desvios;
# - exige pelo menos 5 eventos para evitar alertas em numeros muito pequenos.
#
# Esta e uma abordagem simples e didatica, nao um protocolo oficial.

serie_alertas <- serie_municipal %>%
  group_by(municipio_residencia) %>%
  arrange(ano_mes) %>%
  mutate(
    media_6m_anterior = lag(rollmean(eventos, k = 6, fill = NA, align = "right")),
    dp_6m_anterior = lag(rollapply(eventos, width = 6, FUN = sd, fill = NA, align = "right")),
    limite_alerta = media_6m_anterior + 2 * dp_6m_anterior,
    alerta_anomalia = eventos >= 5 & !is.na(limite_alerta) & eventos > limite_alerta,
    razao_observado_esperado = eventos / media_6m_anterior
  ) %>%
  ungroup()

alertas <- serie_alertas %>%
  filter(alerta_anomalia == TRUE) %>%
  arrange(desc(razao_observado_esperado))

# ------------------------------------------------------------
# 7. Priorizacao dos alertas
# ------------------------------------------------------------
# A prioridade combina volume absoluto e razao observado/esperado.

alertas_priorizados <- alertas %>%
  mutate(
    prioridade = case_when(
      eventos >= 50 & razao_observado_esperado >= 2 ~ "ALTA",
      eventos >= 20 & razao_observado_esperado >= 1.5 ~ "MEDIA",
      TRUE ~ "BAIXA"
    )
  )

# ------------------------------------------------------------
# 8. Visualizacao da serie agregada
# ------------------------------------------------------------

serie_uf <- serie_alertas %>%
  group_by(ano_mes) %>%
  summarise(eventos = sum(eventos, na.rm = TRUE), .groups = "drop")

grafico_uf <- ggplot(serie_uf, aes(x = ano_mes, y = eventos)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Serie temporal agregada de eventos",
    x = "Mes",
    y = "Eventos"
  ) +
  theme_minimal()

ggsave(file.path(pasta_graficos, "serie_agregada_eventos.png"), grafico_uf, width = 10, height = 6)

# ------------------------------------------------------------
# 9. Validacao
# ------------------------------------------------------------

resumo_validacao <- tibble(
  registros_analisados = nrow(sih_prep),
  municipios_analisados = n_distinct(serie_alertas$municipio_residencia),
  meses_analisados = n_distinct(serie_alertas$ano_mes),
  total_alertas = nrow(alertas_priorizados),
  alertas_alta_prioridade = sum(alertas_priorizados$prioridade == "ALTA", na.rm = TRUE),
  alertas_media_prioridade = sum(alertas_priorizados$prioridade == "MEDIA", na.rm = TRUE)
)

print(resumo_validacao)

# ------------------------------------------------------------
# 10. Exportacao
# ------------------------------------------------------------

write_csv(serie_alertas, file.path(pasta_saida, "serie_municipal_com_alertas.csv"))
write_csv(alertas_priorizados, file.path(pasta_saida, "alertas_anomalia_priorizados.csv"))
write_csv(serie_uf, file.path(pasta_saida, "serie_agregada_uf.csv"))
write_csv(resumo_validacao, file.path(pasta_saida, "resumo_validacao_alertas.csv"))

# Fim do script.

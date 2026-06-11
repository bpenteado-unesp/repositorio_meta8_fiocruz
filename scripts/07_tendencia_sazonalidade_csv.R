# ============================================================
# CENARIO 07 - TAREFA INTERMEDIARIA
# Modelagem de tendencia e sazonalidade a partir de CSV
# Fonte de dados: arquivo CSV local
# Ambiente sugerido: RStudio
# ============================================================

# ------------------------------------------------------------
# 0. Objetivo do script
# ------------------------------------------------------------
# Este script analisa uma serie temporal epidemiologica para observar:
# - tendencia geral;
# - padroes sazonais;
# - medias moveis;
# - decomposicao simples da serie;
# - projecao exploratoria de curto prazo.
#
# O objetivo e didatico. Para decisao em saude publica, a modelagem
# precisa ser discutida com especialistas e validada cuidadosamente.

# ------------------------------------------------------------
# 1. Preparacao do ambiente
# ------------------------------------------------------------

# install.packages(c("tidyverse", "lubridate", "janitor", "forecast", "zoo"))

library(tidyverse)
library(lubridate)
library(janitor)
library(forecast)
library(zoo)

# ------------------------------------------------------------
# 2. Caminhos
# ------------------------------------------------------------

arquivo_entrada <- "dados/notificacoes.csv"
pasta_saida <- "saida/07_tendencia_sazonalidade_csv"
pasta_graficos <- file.path(pasta_saida, "graficos")
dir.create(pasta_graficos, recursive = TRUE, showWarnings = FALSE)

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
    classificacao_final = str_to_upper(str_trim(classificacao_final)),
    caso_confirmado = classificacao_final %in% c(
      "CONFIRMADO",
      "CONFIRMADO LABORATORIAL",
      "CONFIRMADO CLINICO",
      "CONFIRMADO CLINICO-EPIDEMIOLOGICO"
    )
  ) %>%
  filter(!is.na(data_notificacao))

# ------------------------------------------------------------
# 5. Serie temporal mensal
# ------------------------------------------------------------
# A agregacao mensal e mais estavel para demonstrar tendencia e sazonalidade.
# Para analises semanais, troque floor_date(..., "month") por "week".

serie_mensal <- dados_prep %>%
  filter(caso_confirmado == TRUE) %>%
  mutate(mes_referencia = floor_date(data_notificacao, unit = "month")) %>%
  count(mes_referencia, name = "casos_confirmados") %>%
  arrange(mes_referencia) %>%
  complete(
    mes_referencia = seq.Date(min(mes_referencia), max(mes_referencia), by = "month"),
    fill = list(casos_confirmados = 0)
  ) %>%
  mutate(
    media_movel_3_meses = rollmean(casos_confirmados, k = 3, fill = NA, align = "right"),
    indice_tempo = row_number()
  )

# ------------------------------------------------------------
# 6. Modelagem simples de tendencia
# ------------------------------------------------------------
# O modelo linear abaixo estima se os casos aumentam ou diminuem ao longo do tempo.
# Ele e simples e nao captura todos os aspectos epidemiologicos.

modelo_tendencia <- lm(casos_confirmados ~ indice_tempo, data = serie_mensal)

serie_mensal <- serie_mensal %>%
  mutate(
    tendencia_estimada = predict(modelo_tendencia, newdata = serie_mensal)
  )

resumo_modelo_tendencia <- broom::tidy(modelo_tendencia)

# ------------------------------------------------------------
# 7. Decomposicao e previsao exploratoria
# ------------------------------------------------------------
# A funcao ts() cria um objeto de serie temporal.
# frequency = 12 indica dados mensais.

serie_ts <- ts(
  serie_mensal$casos_confirmados,
  frequency = 12,
  start = c(year(min(serie_mensal$mes_referencia)), month(min(serie_mensal$mes_referencia)))
)

# stl() decompoe a serie em tendencia, sazonalidade e residuo.
# Para funcionar bem, a serie precisa ter extensao razoavel.
decomposicao <- tryCatch(
  stl(serie_ts, s.window = "periodic"),
  error = function(e) NULL
)

# ets() gera uma previsao exploratoria baseada em suavizacao exponencial.
modelo_ets <- ets(serie_ts)
previsao_6_meses <- forecast(modelo_ets, h = 6)

tabela_previsao <- tibble(
  horizonte = 1:6,
  previsao = as.numeric(previsao_6_meses$mean),
  limite_inferior_80 = as.numeric(previsao_6_meses$lower[, "80%"]),
  limite_superior_80 = as.numeric(previsao_6_meses$upper[, "80%"]),
  limite_inferior_95 = as.numeric(previsao_6_meses$lower[, "95%"]),
  limite_superior_95 = as.numeric(previsao_6_meses$upper[, "95%"])
)

# ------------------------------------------------------------
# 8. Graficos
# ------------------------------------------------------------

grafico_tendencia <- ggplot(serie_mensal, aes(x = mes_referencia, y = casos_confirmados)) +
  geom_line() +
  geom_point() +
  geom_line(aes(y = media_movel_3_meses), linetype = "dashed") +
  geom_line(aes(y = tendencia_estimada), linetype = "dotted") +
  labs(
    title = "Tendencia de casos confirmados",
    x = "Mes",
    y = "Casos confirmados"
  ) +
  theme_minimal()

ggsave(file.path(pasta_graficos, "tendencia_casos_confirmados.png"), grafico_tendencia, width = 10, height = 6)

png(file.path(pasta_graficos, "previsao_ets_6_meses.png"), width = 1000, height = 700)
plot(previsao_6_meses, main = "Previsao exploratoria para 6 meses")
dev.off()

if (!is.null(decomposicao)) {
  png(file.path(pasta_graficos, "decomposicao_stl.png"), width = 1000, height = 700)
  plot(decomposicao, main = "Decomposicao STL da serie")
  dev.off()
}

# ------------------------------------------------------------
# 9. Validacao
# ------------------------------------------------------------

resumo_validacao <- tibble(
  meses_na_serie = nrow(serie_mensal),
  total_casos_confirmados = sum(serie_mensal$casos_confirmados, na.rm = TRUE),
  media_mensal = mean(serie_mensal$casos_confirmados, na.rm = TRUE),
  inclinacao_tendencia = coef(modelo_tendencia)[["indice_tempo"]],
  aic_modelo_ets = modelo_ets$aic
)

print(resumo_validacao)

# ------------------------------------------------------------
# 10. Exportacao
# ------------------------------------------------------------

write_csv(serie_mensal, file.path(pasta_saida, "serie_mensal_tendencia.csv"))
write_csv(resumo_modelo_tendencia, file.path(pasta_saida, "resumo_modelo_tendencia.csv"))
write_csv(tabela_previsao, file.path(pasta_saida, "previsao_6_meses.csv"))
write_csv(resumo_validacao, file.path(pasta_saida, "resumo_validacao_tendencia_sazonalidade.csv"))

# Fim do script.

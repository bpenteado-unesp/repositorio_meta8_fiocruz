# ============================================================
# CENARIO 09 - TAREFA AVANCADA
# Modelagem preditiva de risco epidemiologico a partir de CSV
# Fonte de dados: arquivo CSV local
# Ambiente sugerido: RStudio
# ============================================================

# ------------------------------------------------------------
# 0. Objetivo do script
# ------------------------------------------------------------
# Este script demonstra uma modelagem preditiva de risco em uma base
# epidemiologica local. O exemplo estima o risco de um desfecho grave,
# como obito ou internacao, a partir de variaveis como idade, sexo,
# municipio, sintomas, comorbidades e resultado de teste.
#
# Atencao:
# - Este script e didatico.
# - O modelo nao deve ser usado para decisao clinica sem validacao.
# - Avalie vieses, qualidade dos dados e interpretabilidade.

# ------------------------------------------------------------
# 1. Preparacao do ambiente
# ------------------------------------------------------------

# install.packages(c("tidyverse", "lubridate", "janitor", "tidymodels", "vip"))

library(tidyverse)
library(lubridate)
library(janitor)
library(tidymodels)
library(vip)

# Para resultados reprodutiveis.
set.seed(123)

# ------------------------------------------------------------
# 2. Caminhos
# ------------------------------------------------------------

arquivo_entrada <- "dados/notificacoes.csv"
pasta_saida <- "saida/09_modelagem_risco_csv"
pasta_graficos <- file.path(pasta_saida, "graficos")
dir.create(pasta_graficos, recursive = TRUE, showWarnings = FALSE)

# ------------------------------------------------------------
# 3. Ingestao
# ------------------------------------------------------------

dados <- read_csv(arquivo_entrada, show_col_types = FALSE) %>%
  clean_names()

# ------------------------------------------------------------
# 4. Preparacao dos dados
# ------------------------------------------------------------
# Ajuste os nomes das variaveis conforme sua base real.
# Variaveis comuns em bases epidemiologicas:
# - idade;
# - sexo;
# - municipio;
# - sintomas;
# - comorbidades;
# - resultado_teste;
# - evolucao.

base_modelo <- dados %>%
  mutate(
    idade = as.numeric(idade),
    idade = if_else(idade < 0 | idade > 120, NA_real_, idade),

    sexo = str_to_upper(str_trim(sexo)),
    municipio = str_to_upper(str_trim(municipio)),
    resultado_teste = str_to_upper(str_trim(resultado_teste)),
    evolucao = str_to_upper(str_trim(evolucao)),

    # Variavel-alvo: desfecho grave.
    # Aqui consideramos obito como desfecho grave. Se a base tiver coluna
    # de internacao, e possivel incluir tambem essa condicao.
    desfecho_grave = case_when(
      evolucao %in% c("OBITO", "OBITO PELO AGRAVO") ~ "SIM",
      evolucao %in% c("CURA", "RECUPERADO", "ALTA") ~ "NAO",
      TRUE ~ NA_character_
    ),

    # Exemplo de padronizacao de teste positivo.
    teste_positivo = case_when(
      resultado_teste %in% c("POSITIVO", "DETECTAVEL", "REAGENTE") ~ "SIM",
      resultado_teste %in% c("NEGATIVO", "NAO DETECTAVEL", "NAO REAGENTE") ~ "NAO",
      TRUE ~ "IGNORADO"
    )
  ) %>%
  filter(!is.na(desfecho_grave)) %>%
  mutate(
    desfecho_grave = factor(desfecho_grave, levels = c("NAO", "SIM")),
    sexo = factor(sexo),
    municipio = factor(municipio),
    teste_positivo = factor(teste_positivo)
  )

# ------------------------------------------------------------
# 5. Divisao treino/teste
# ------------------------------------------------------------
# A divisao separa parte dos dados para treinar o modelo e parte para
# avaliar seu desempenho em registros nao vistos durante o treinamento.

split_dados <- initial_split(base_modelo, prop = 0.80, strata = desfecho_grave)
treino <- training(split_dados)
teste <- testing(split_dados)

# ------------------------------------------------------------
# 6. Receita de pre-processamento
# ------------------------------------------------------------
# A recipe define transformacoes antes do modelo:
# - imputacao de idade ausente pela mediana;
# - agrupamento de categorias raras de municipio;
# - criacao de variaveis dummy para categorias;
# - remocao de variaveis sem variacao.

receita <- recipe(desfecho_grave ~ idade + sexo + municipio + teste_positivo, data = treino) %>%
  step_impute_median(idade) %>%
  step_other(municipio, threshold = 0.01, other = "OUTROS") %>%
  step_dummy(all_nominal_predictors()) %>%
  step_zv(all_predictors())

# ------------------------------------------------------------
# 7. Especificacao do modelo
# ------------------------------------------------------------
# Usamos regressao logistica por ser interpretavel e adequada como
# primeiro modelo de classificacao binaria.

modelo_logistico <- logistic_reg(mode = "classification") %>%
  set_engine("glm")

workflow_modelo <- workflow() %>%
  add_recipe(receita) %>%
  add_model(modelo_logistico)

# ------------------------------------------------------------
# 8. Treinamento
# ------------------------------------------------------------

ajuste <- fit(workflow_modelo, data = treino)

# ------------------------------------------------------------
# 9. Predicao e avaliacao
# ------------------------------------------------------------

predicoes <- predict(ajuste, new_data = teste, type = "prob") %>%
  bind_cols(predict(ajuste, new_data = teste, type = "class")) %>%
  bind_cols(teste %>% select(desfecho_grave))

metricas <- metric_set(accuracy, sens, spec, roc_auc)

resultado_metricas <- metricas(
  predicoes,
  truth = desfecho_grave,
  estimate = .pred_class,
  .pred_SIM,
  event_level = "second"
)

matriz_confusao <- conf_mat(
  predicoes,
  truth = desfecho_grave,
  estimate = .pred_class
)

curva_roc <- roc_curve(
  predicoes,
  truth = desfecho_grave,
  .pred_SIM,
  event_level = "second"
)

# ------------------------------------------------------------
# 10. Visualizacoes
# ------------------------------------------------------------

grafico_roc <- autoplot(curva_roc) +
  labs(title = "Curva ROC do modelo de risco") +
  theme_minimal()

ggsave(file.path(pasta_graficos, "curva_roc_modelo_risco.png"), grafico_roc, width = 8, height = 6)

# Coeficientes do modelo logistico para interpretacao.
coeficientes <- tidy(extract_fit_parsnip(ajuste)$fit) %>%
  arrange(desc(abs(estimate)))

coeficientes_top <- coeficientes %>%
  filter(term != "(Intercept)") %>%
  slice_max(abs(estimate), n = 20)

grafico_coeficientes <- ggplot(coeficientes_top, aes(x = reorder(term, estimate), y = estimate)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Principais coeficientes do modelo logistico",
    x = "Variavel",
    y = "Coeficiente"
  ) +
  theme_minimal()

ggsave(file.path(pasta_graficos, "coeficientes_modelo_risco.png"), grafico_coeficientes, width = 10, height = 7)

# ------------------------------------------------------------
# 11. Validacao e alertas metodologicos
# ------------------------------------------------------------

resumo_validacao <- tibble(
  registros_modelagem = nrow(base_modelo),
  registros_treino = nrow(treino),
  registros_teste = nrow(teste),
  proporcao_desfecho_grave = mean(base_modelo$desfecho_grave == "SIM", na.rm = TRUE),
  variaveis_usadas = "idade, sexo, municipio, teste_positivo"
)

print(resultado_metricas)
print(matriz_confusao)
print(resumo_validacao)

# ------------------------------------------------------------
# 12. Exportacao
# ------------------------------------------------------------

write_csv(predicoes, file.path(pasta_saida, "predicoes_modelo_risco.csv"))
write_csv(resultado_metricas, file.path(pasta_saida, "metricas_modelo_risco.csv"))
write_csv(as_tibble(matriz_confusao$table), file.path(pasta_saida, "matriz_confusao_modelo_risco.csv"))
write_csv(curva_roc, file.path(pasta_saida, "curva_roc_modelo_risco.csv"))
write_csv(coeficientes, file.path(pasta_saida, "coeficientes_modelo_risco.csv"))
write_csv(resumo_validacao, file.path(pasta_saida, "resumo_validacao_modelagem_risco.csv"))

# Fim do script.

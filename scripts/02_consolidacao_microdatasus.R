# ============================================================
# CENARIO 02 - TAREFA CORRIQUEIRA
# Consolidacao de dados de diferentes fontes usando microdatasus
# Fonte de dados: DATASUS via pacote microdatasus
# Ambiente sugerido: RStudio
# ============================================================

# ------------------------------------------------------------
# 0. Objetivo do script
# ------------------------------------------------------------
# Este script exemplifica como baixar dados publicos do DATASUS
# usando o pacote microdatasus e consolidar informacoes em uma
# tabela analitica. O exemplo usa dados do SIH-RD, mas a estrutura
# pode ser adaptada para outros sistemas disponiveis no pacote.
#
# Observacao importante:
# O microdatasus depende da disponibilidade dos arquivos no DATASUS.
# Em alguns momentos, a conexao pode falhar ou o servidor pode estar
# instavel. Se isso ocorrer, tente novamente depois.

# ------------------------------------------------------------
# 1. Preparacao do ambiente
# ------------------------------------------------------------

# install.packages(c("tidyverse", "lubridate", "janitor", "microdatasus"))

library(tidyverse)
library(lubridate)
library(janitor)
library(microdatasus)

# ------------------------------------------------------------
# 2. Parametros do recorte de dados
# ------------------------------------------------------------
# UF usa sigla da unidade federativa.
# year_start/year_end e month_start/month_end definem o periodo.
# Altere conforme o exercicio da disciplina ou o projeto de pesquisa.

uf_interesse <- "SP"
ano_inicio <- 2023
ano_fim <- 2023
mes_inicio <- 1
mes_fim <- 3

pasta_saida <- "saida/02_consolidacao_microdatasus"
dir.create(pasta_saida, recursive = TRUE, showWarnings = FALSE)

# ------------------------------------------------------------
# 3. Ingestao dos dados pelo microdatasus
# ------------------------------------------------------------
# Para SIH-RD, o argumento information_system = "SIH-RD" acessa
# Autorizacoes de Internacao Hospitalar reduzidas.
# O argumento vars pode ser omitido para baixar todas as variaveis,
# mas selecionar variaveis torna o processo mais leve.

aih_bruta <- fetch_datasus(
  year_start = ano_inicio,
  year_end = ano_fim,
  month_start = mes_inicio,
  month_end = mes_fim,
  uf = uf_interesse,
  information_system = "SIH-RD"
)

# process_sih() transforma codigos em campos mais legiveis quando possivel.
aih_processada <- process_sih(aih_bruta)

# ------------------------------------------------------------
# 4. Preparacao dos dados
# ------------------------------------------------------------
# Como o DATASUS possui muitas variaveis codificadas, o objetivo aqui e
# produzir uma tabela sintetica por municipio, sexo, faixa etaria e CID.
# Os nomes das colunas podem variar conforme o sistema e a versao do pacote.
# Por isso, usamos clean_names() para padronizar os nomes.

aih_limpa <- aih_processada %>%
  clean_names() %>%
  mutate(
    # DT_INTER geralmente representa competencia ou data relacionada ao evento.
    # Em algumas bases a coluna pode vir como data de internacao ou competencia.
    data_referencia = suppressWarnings(ymd(dt_inter)),
    ano = year(data_referencia),
    mes = month(data_referencia),

    # Idade e sexo podem estar codificados conforme a origem dos dados.
    idade = as.numeric(idade),
    faixa_etaria = case_when(
      is.na(idade) ~ "IGNORADA",
      idade < 1 ~ "<1 ANO",
      idade <= 4 ~ "1 A 4",
      idade <= 9 ~ "5 A 9",
      idade <= 19 ~ "10 A 19",
      idade <= 39 ~ "20 A 39",
      idade <= 59 ~ "40 A 59",
      idade >= 60 ~ "60+"
    ),

    cid_principal = str_to_upper(str_trim(diag_princ))
  )

# ------------------------------------------------------------
# 5. Consolidacao analitica
# ------------------------------------------------------------
# Aqui agregamos os registros para gerar uma base de vigilancia.
# O mesmo raciocinio poderia ser usado para juntar SIH, SIM, SINAN
# ou bases laboratoriais, desde que haja chaves territoriais e temporais.

base_consolidada <- aih_limpa %>%
  group_by(ano, mes, munic_res, sexo, faixa_etaria, cid_principal) %>%
  summarise(
    internacoes = n(),
    valor_total = sum(as.numeric(val_tot), na.rm = TRUE),
    dias_permanencia = sum(as.numeric(dias_perm), na.rm = TRUE),
    obitos_hospitalares = sum(as.numeric(morte), na.rm = TRUE),
    .groups = "drop"
  )

# ------------------------------------------------------------
# 6. Validacao
# ------------------------------------------------------------
# A validacao confere volume, municipios, campos ausentes e totais.

resumo_validacao <- tibble(
  total_registros_baixados = nrow(aih_bruta),
  total_registros_processados = nrow(aih_limpa),
  total_linhas_consolidadas = nrow(base_consolidada),
  municipios_distintos = n_distinct(base_consolidada$munic_res),
  cid_principal_ausente = sum(is.na(aih_limpa$cid_principal) | aih_limpa$cid_principal == ""),
  internacoes_total = sum(base_consolidada$internacoes, na.rm = TRUE)
)

print(resumo_validacao)

# ------------------------------------------------------------
# 7. Exportacao
# ------------------------------------------------------------

write_csv(aih_limpa, file.path(pasta_saida, "aih_microdatasus_limpa.csv"))
write_csv(base_consolidada, file.path(pasta_saida, "base_consolidada_microdatasus.csv"))
write_csv(resumo_validacao, file.path(pasta_saida, "resumo_validacao_consolidacao.csv"))

# Fim do script.

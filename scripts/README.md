# Scripts R para modelagem e analise de dados em vigilancia epidemiologica

Este pacote contem 9 scripts em R, organizados conforme os cenarios levantados:

## Tarefas corriqueiras

1. `01_corriqueira_limpeza_padronizacao_csv.R`  
   Limpeza e padronizacao de bases epidemiologicas usando CSV local.

2. `02_corriqueira_consolidacao_microdatasus.R`  
   Consolidacao de dados obtidos do DATASUS via `microdatasus`.

3. `03_corriqueira_indicadores_csv.R`  
   Calculo de indicadores epidemiologicos basicos usando CSV local.

4. `04_corriqueira_paineis_microdatasus.R`  
   Tabelas e graficos descritivos usando dados do `microdatasus`.

5. `05_corriqueira_inconsistencias_csv.R`  
   Identificacao de inconsistencias e possiveis sinais de subnotificacao usando CSV local.

## Tarefas intermediarias

6. `06_intermediaria_analise_espaco_temporal_microdatasus.R`  
   Analise espaco-temporal por municipio e mes usando `microdatasus`.

7. `07_intermediaria_tendencia_sazonalidade_csv.R`  
   Modelagem de tendencia, sazonalidade e previsao exploratoria usando CSV local.

## Tarefas avancadas

8. `08_avancada_deteccao_surtos_microdatasus.R`  
   Deteccao automatica de anomalias/surtos usando serie temporal do `microdatasus`.

9. `09_avancada_modelagem_risco_csv.R`  
   Modelagem preditiva de risco epidemiologico usando CSV local.

## Alternancia de fontes

Os scripts alternam entre:

- CSV local;
- dados do DATASUS obtidos via pacote `microdatasus`.

A sequencia adotada foi:

1. CSV
2. microdatasus
3. CSV
4. microdatasus
5. CSV
6. microdatasus
7. CSV
8. microdatasus
9. CSV

## Estrutura didatica dos scripts

Cada script foi organizado com comentarios extensos e secoes como:

- objetivo;
- preparacao do ambiente;
- definicao de parametros;
- ingestao dos dados;
- preparacao dos dados;
- analise/modelagem;
- validacao;
- exportacao dos resultados.

## Pacotes utilizados

Os pacotes variam por script, mas o conjunto geral inclui:

```r
install.packages(c(
  "tidyverse",
  "lubridate",
  "janitor",
  "stringi",
  "microdatasus",
  "zoo",
  "forecast",
  "broom",
  "tidymodels",
  "vip"
))
```

## Observacoes importantes

- Os scripts sao modelos didaticos e devem ser adaptados a base real.
- O `microdatasus` depende da disponibilidade dos servidores do DATASUS.
- Resultados de alerta, risco ou previsao nao devem ser interpretados automaticamente como evidencia epidemiologica conclusiva.
- Para uso em vigilancia real, recomenda-se validacao por profissionais da area de saude, epidemiologia e gestao dos dados.

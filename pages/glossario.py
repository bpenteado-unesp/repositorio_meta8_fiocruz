import streamlit as st
from helper import render_menu

render_menu()

st.title("Glossário de termos da ciência de dados para a vigilância epidemiológica")

import streamlit as st

# 1. Seus dados: termos e links/descrições associadas
termos = {
    "Agente de software": "Programa que executa tarefas com algum grau de autonomia, como buscar dados, aplicar regras ou acionar alertas. Exemplo em VE: um agente monitora semanalmente a base de SRAG e envia alerta quando há aumento acima do esperado.",
    "Algoritmo": "Sequência de regras ou instruções para resolver um problema. Exemplo em VE: um algoritmo classifica municípios em baixo, médio ou alto risco para dengue com base em incidência, chuva e temperatura.",
    "Anonimização": "Processo de remover ou transformar informações pessoais para impedir a identificação de indivíduos. Exemplo em VE: antes de divulgar dados de notificações, nomes, CPF, endereço e datas muito específicas são removidos ou agregados.",
    "Aprendizagem de máquina (machine learning)": "Área da inteligência artificial em que modelos aprendem padrões a partir dos dados. Exemplo em VE: um modelo aprende com séries históricas de dengue para estimar o risco de aumento nas próximas semanas.",
    "Aprendizagem profunda (deep learning)": "Tipo de aprendizagem de máquina baseada em redes neurais com muitas camadas. Exemplo em VE: redes profundas podem analisar imagens de lâminas, radiografias ou padrões complexos em séries temporais de doenças respiratórias.",
    "Armazenamento de dados": "Processo de guardar dados de forma organizada, segura e acessível. Exemplo em VE: microdados brutos do SIVEP-Gripe são armazenados separadamente dos dados tratados usados em painéis.",
    "Automação de dados": "Uso de scripts, rotinas ou sistemas para executar tarefas repetitivas sem intervenção manual. Exemplo em VE: uma rotina baixa dados do OpenDataSUS toda segunda-feira e atualiza indicadores municipais.",
    "Banco de dados": "Estrutura organizada para armazenar, consultar e atualizar dados. Exemplo em VE: um banco relacional pode guardar notificações, resultados laboratoriais, internações e óbitos vinculados por chaves padronizadas.",
    "Big data": "Conjuntos de dados muito grandes, rápidos, variados ou complexos para métodos tradicionais. Exemplo em VE: integrar notificações, mobilidade, clima, redes sociais e registros assistenciais pode configurar um cenário de big data em saúde pública.",
    "Business intelligence (BI)": "Conjunto de práticas e ferramentas para transformar dados em relatórios, painéis e indicadores gerenciais. Exemplo em VE: um painel de BI mostra incidência, letalidade, cobertura vacinal e ocupação hospitalar por região de saúde.",
    "Catálogo de dados": "Inventário organizado das bases disponíveis, com descrição, origem, responsáveis e metadados. Exemplo em VE: um catálogo informa quais bases existem sobre dengue, SRAG, vacinação, mortalidade e capacidade hospitalar.",
    "Ciência de dados": "Campo interdisciplinar que combina estatística, computação, conhecimento do domínio e visualização para extrair valor dos dados. Exemplo em VE: ciência de dados pode apoiar previsão de surtos, detecção de anomalias e priorização de territórios.",
    "Ciência de dados populacionais": "Aplicação da ciência de dados a informações de populações, territórios e grupos sociais. Exemplo em VE: combinar SIM, SINASC, IBGE e SIH/SUS para estudar desigualdades de mortalidade infantil entre municípios.",
    "Ciclo de vida dos dados": "Conjunto de etapas pelas quais os dados passam, da criação à coleta, armazenamento, uso, compartilhamento e descarte. Exemplo em VE: uma notificação nasce na unidade de saúde, é consolidada, analisada, armazenada e depois usada em boletins.",
    "Classificação": "Tarefa de modelagem que atribui uma categoria a cada observação. Exemplo em VE: classificar municípios como “alerta”, “atenção” ou “normal” para arboviroses.",
    "Clusterização": "Técnica que agrupa observações semelhantes sem categorias previamente definidas. Exemplo em VE: agrupar municípios com padrões parecidos de incidência, clima e vulnerabilidade social.",
    "Código aberto": "Software ou código cujo conteúdo pode ser inspecionado, usado e modificado. Exemplo em VE: scripts em R ou Python abertos permitem que outras equipes reproduzam os indicadores de um boletim.",
    "Coleta de dados": "Processo de obter dados a partir de sistemas, formulários, sensores, APIs ou arquivos. Exemplo em VE: coletar notificações de dengue no SINAN e dados meteorológicos do INMET.",
    "Completude dos dados": "Grau em que campos importantes estão preenchidos. Exemplo em VE: avaliar a proporção de notificações de SRAG com informação de raça/cor, evolução e classificação final.",
    "Conjunto de dados: dataset": "Coleção organizada de registros e variáveis. Exemplo em VE: a base de casos de SRAG por ano é um dataset usado para análise de vírus respiratórios.",
    "Controle de qualidade dos dados": "Verificação de erros, inconsistências, duplicidades e valores ausentes. Exemplo em VE: identificar registros com data de óbito anterior à data de início dos sintomas.",
    "CRISP-DM": "Modelo clássico de processo para mineração de dados, com etapas de entendimento do negócio, entendimento dos dados, preparação, modelagem, avaliação e implantação. Exemplo em VE: adaptar o CRISP-DM para estruturar um projeto de previsão de dengue.",
    "Curadoria de dados": "Organização, limpeza, documentação e qualificação dos dados para uso analítico. Exemplo em VE: padronizar municípios, corrigir datas e aplicar critérios de caso confirmado antes da análise.",
    "Dashboard": "Painel visual interativo com indicadores, gráficos, mapas e filtros. Exemplo em VE: dashboard de dengue com incidência semanal, tendência, sorotipo, alertas e cobertura territorial.",
    "Data lake": "Repositório que armazena grandes volumes de dados em formatos variados, geralmente ainda brutos. Exemplo em VE: guardar arquivos CSV, JSON, PDF, planilhas e dados laboratoriais em um ambiente único.",
    "Data warehouse": "Banco estruturado e organizado para consultas analíticas e relatórios. Exemplo em VE: consolidar mensalmente dados de notificação, internação e óbito para análises de situação de saúde.",
    "Dados agregados": "Dados resumidos por grupos, períodos ou territórios, sem registros individuais. Exemplo em VE: número de casos de dengue por município e semana epidemiológica.",
    "Dados abertos": "Dados disponíveis ao público para acesso, uso e redistribuição. Exemplo em VE: bases do OpenDataSUS usadas para estudos sobre vacinação, SRAG e mortalidade.",
    "Dados de navegação": "Registros gerados pelo uso de sites, aplicativos ou sistemas digitais. Exemplo em VE: aumento de buscas por “febre alta” ou “teste de covid” pode ser usado como sinal complementar de vigilância.",
    "Dados estruturados": "Dados organizados em tabelas com linhas e colunas bem definidas. Exemplo em VE: uma tabela com município, semana epidemiológica, número de casos e óbitos.",
    "Dados não estruturados": "Dados sem organização tabular direta, como textos, imagens, áudios e PDFs. Exemplo em VE: notas técnicas, prontuários textuais, laudos ou notícias sobre surtos.",
    "Dados pessoais sensíveis": "Informações que exigem maior proteção, como dados de saúde, origem racial, biometria ou religião. Exemplo em VE: diagnóstico, resultado laboratorial e condição clínica de um caso notificado.",
    "Dados sintéticos": "Dados artificiais gerados para simular características de dados reais sem expor pessoas. Exemplo em VE: criar uma base sintética de notificações para treinar equipes em análise sem usar microdados reais.",
    "Deduplicação": "Identificação e remoção ou consolidação de registros repetidos. Exemplo em VE: dois registros do mesmo caso de dengue podem aparecer se o paciente procurou serviços diferentes.",
    "Dicionário de dados": "Documento que descreve variáveis, formatos, códigos e significados de uma base. Exemplo em VE: explicar que “EVOLUCAO=1” significa cura e “EVOLUCAO=2” significa óbito.",
    "Engenharia de atributos": "feature engineering: Criação de variáveis úteis para análise ou modelagem. Exemplo em VE: calcular atraso entre início dos sintomas e notificação, incidência acumulada ou média móvel de casos.",
    "Escalabilidade": "Capacidade de um sistema crescer e lidar com maior volume de dados ou usuários. Exemplo em VE: um pipeline deve suportar milhões de registros de vacinação sem travar.",
    "Extração, transformação e carga: ETL": "Processo de extrair dados, transformá-los e carregá-los em um destino. Exemplo em VE: baixar dados do OpenDataSUS, padronizar campos e carregar em um banco institucional.",
    "Fluxo de dados": "Caminho percorrido pelos dados entre origem, processamento, armazenamento, análise e uso. Exemplo em VE: a notificação sai da unidade de saúde, passa pelo sistema nacional, é extraída, tratada e exibida em painel.",
    "Fonte de dados": "Origem dos dados usados em uma análise. Exemplo em VE: SINAN, SIVEP-Gripe, SIM, SI-PNI, IBGE, INMET, mídias sociais, sensores IoT ou prontuários eletrônicos.",
    "Forecasting": "Previsão de valores futuros a partir de dados históricos e variáveis explicativas. Exemplo em VE: prever casos de dengue nas próximas quatro semanas por município.",
    "Governança de dados": "Conjunto de regras, responsabilidades e processos para garantir qualidade, segurança, acesso e uso adequado dos dados. Exemplo em VE: definir quem pode acessar microdados identificáveis de notificações.",
    "Granularidade dos dados": "Nível de detalhe dos dados, como indivíduo, município, semana ou mês. Exemplo em VE: dados por caso individual têm maior granularidade que dados agregados por estado.",
    "IA generativa": "Tipo de inteligência artificial capaz de gerar texto, imagens, código ou outros conteúdos. Exemplo em VE: gerar rascunhos de boletins epidemiológicos a partir de indicadores revisados por especialistas.",
    "Indicador": "Medida resumida usada para monitorar uma situação. Exemplo em VE: incidência de dengue por 100 mil habitantes, letalidade por SRAG ou cobertura vacinal.",
    "Inferência causal": "Conjunto de métodos para estimar efeitos de uma exposição, intervenção ou política. Exemplo em VE: avaliar se uma campanha de vacinação reduziu internações por influenza.",
    "Inteligência artificial: IA": "Campo que desenvolve sistemas capazes de executar tarefas associadas à inteligência humana. Exemplo em VE: IA pode apoiar classificação de risco, leitura de textos e detecção de padrões incomuns.",
    "Interoperabilidade": "Capacidade de sistemas diferentes trocarem e compreenderem dados. Exemplo em VE: integrar notificação, laboratório, internação e óbito usando padrões comuns.",
    "Internet das Coisas: IoT": "Rede de dispositivos conectados que coletam e transmitem dados. Exemplo em VE: sensores ambientais medem temperatura e umidade para apoiar modelos de arboviroses.",
    "Linkage de dados": "Processo de vincular registros de diferentes bases que pertencem à mesma pessoa, evento ou território. Exemplo em VE: vincular uma notificação de SRAG ao registro de internação e ao óbito no SIM.",
    "Linhagem dos dados": "Registro da origem, transformações e usos dos dados ao longo do tempo. Exemplo em VE: documentar que um indicador veio do SIVEP-Gripe extraído em determinada data e tratado por certo script.",
    "Metadados": "Dados que descrevem outros dados, como origem, periodicidade, responsável, formato e data de atualização. Exemplo em VE: informar que uma base de SRAG é atualizada semanalmente e contém registros desde 2019.",
    "Mineração de dados": "Exploração sistemática de grandes bases para descobrir padrões, associações ou anomalias. Exemplo em VE: identificar perfis de municípios com aumento recorrente de leptospirose após chuvas intensas.",
    "Modelo preditivo": "Modelo que estima a probabilidade ou valor futuro de um evento. Exemplo em VE: estimar quais municípios têm maior chance de ultrapassar o limiar epidêmico de dengue.",
    "Monitoramento em tempo quase real": "Acompanhamento frequente de dados com pequeno atraso em relação aos eventos. Exemplo em VE: atualizar diariamente notificações de síndrome gripal para detectar aumento recente.",
    "Mídias sociais como fonte de dados": "Uso de publicações em redes sociais como sinais complementares. Exemplo em VE: aumento de relatos sobre diarreia em uma cidade pode indicar evento que merece verificação.",
    "Nowcasting": "Estimativa da situação atual corrigindo atrasos e incompletudes dos dados recentes. Exemplo em VE: estimar o número real de casos de SRAG da semana atual antes que todas as notificações sejam digitadas.",
    "Ontologias": "Estruturas formais que organizam conceitos e relações de um domínio. Exemplo em VE: uma ontologia pode relacionar doença, agente etiológico, vetor, sintomas, exames e medidas de controle.",
    "Pipeline de dados": "Sequência automatizada de etapas para coletar, tratar, armazenar e disponibilizar dados. Exemplo em VE: pipeline que baixa dados de vacinação, calcula cobertura e atualiza um painel.",
    "Pirâmide DIKW": "Modelo que diferencia dados, informação, conhecimento e sabedoria. Exemplo em VE: registros de casos são dados; taxa de incidência é informação; interpretação do risco é conhecimento; decisão de intensificar controle vetorial é sabedoria aplicada.",
    "Privacidade diferencial": "Técnica que adiciona ruído estatístico para proteger indivíduos em análises agregadas. Exemplo em VE: divulgar indicadores por pequenos territórios reduzindo risco de reidentificação.",
    "Processamento de linguagem natural: PLN": "Área que permite analisar, classificar ou gerar linguagem humana. Exemplo em VE: extrair automaticamente sintomas e diagnósticos de textos de prontuários ou notificações.",
    "Proteção à privacidade": "Medidas para evitar exposição indevida de informações pessoais. Exemplo em VE: restringir acesso a endereço e nome de pacientes em bases de doenças de notificação compulsória.",
    "Qualidade dos dados": "Grau em que os dados são completos, consistentes, oportunos, válidos e adequados ao uso. Exemplo em VE: avaliar se os campos de data de sintomas, município e evolução estão preenchidos corretamente.",
    "Registro eletrônico de saúde": "Sistema digital que armazena informações clínicas e assistenciais de pacientes. Exemplo em VE: registros eletrônicos podem apoiar vigilância sindrômica a partir de sintomas informados em atendimentos.",
    "Representação do conhecimento": "Forma de estruturar conceitos, regras e relações para que sistemas computacionais possam usá-los. Exemplo em VE: representar regras de definição de caso para classificar notificações automaticamente.",
    "Reprodutibilidade": "Capacidade de repetir uma análise e obter os mesmos resultados com os mesmos dados e métodos. Exemplo em VE: um boletim de dengue deve poder ser refeito com os scripts e bases da data original.",
    "Saúde pública baseada em evidência": "Uso sistemático de dados, análises e evidências científicas para orientar decisões em saúde pública. Exemplo em VE: decidir alocação de equipes de controle vetorial com base em incidência, vulnerabilidade e tendência.",
    "Saúde pública de precisão": "Uso de dados mais detalhados para orientar intervenções mais oportunas e direcionadas a populações e territórios. Exemplo em VE: priorizar bairros com maior risco de arbovirose combinando casos, clima, saneamento e densidade populacional.",
    "Série temporal": "Sequência de observações ordenadas no tempo. Exemplo em VE: número semanal de casos de SRAG por estado ao longo dos anos.",
    "Sistema de alerta precoce": "Sistema que detecta risco antes que o evento se agrave. Exemplo em VE: alerta semanal de dengue quando incidência, clima e tendência indicam alta probabilidade de epidemia.",
    "Treinamento de modelo": "Processo de ajustar um modelo usando dados históricos. Exemplo em VE: treinar um algoritmo com dados de dengue de 2015 a 2024 para prever risco em 2025.",
    "Uso secundário de dados": "Uso de dados coletados originalmente para outra finalidade. Exemplo em VE: usar registros hospitalares do SIH/SUS, gerados para fins administrativos, em estudos de carga de doença.",
    "Validação de modelo": "Avaliação do desempenho e da utilidade de um modelo em dados não usados no treinamento. Exemplo em VE: testar se um modelo de alerta de dengue teria detectado surtos passados com antecedência.",
    "Variável": "Característica observada ou medida em uma base de dados. Exemplo em VE: idade, sexo, município, data de início dos sintomas, classificação final e evolução são variáveis de uma notificação.",
    "Viés algorítmico": "Erro sistemático produzido ou amplificado por um modelo. Exemplo em VE: um modelo pode subestimar risco em municípios que notificam pouco, confundindo silêncio epidemiológico com baixa transmissão.",
    "Viés da seletividade": "Distorção causada quando os dados representam apenas parte da população ou dos eventos. Exemplo em VE: dados de testes laboratoriais podem representar mais quem teve acesso ao serviço do que todos os infectados.",
    "Viés de vigilância": "Distorção causada por diferenças na capacidade de detectar, notificar ou investigar eventos. Exemplo em VE: municípios com vigilância mais ativa podem parecer ter mais casos simplesmente porque notificam melhor.",
    "Vigilância digital": "Uso de fontes digitais para detectar ou acompanhar eventos de saúde. Exemplo em VE: monitorar buscas na internet, redes sociais e atendimentos digitais para identificar sinais de síndrome gripal.",
    "Vigilância participatória": "Modelo em que a população contribui diretamente com informações sobre sintomas ou eventos. Exemplo em VE: cidadãos informam febre, dor no corpo e localização por aplicativo para apoiar vigilância de arboviroses.",
    "Vigilância sindrômica": "Monitoramento de sinais e sintomas antes da confirmação diagnóstica. Exemplo em VE: acompanhar atendimentos por síndrome gripal para detectar aumento precoce de vírus respiratórios.",
    "Visão computacional": "Área da IA voltada à análise automática de imagens e vídeos. Exemplo em VE: identificar focos de mosquito em imagens de drones ou apoiar leitura de exames de imagem em surtos respiratórios.",
    "Visualização de dados": "Representação gráfica de dados para facilitar interpretação e decisão. Exemplo em VE: mapas de calor, curvas epidêmicas e gráficos de tendência ajudam a comunicar risco a gestores e equipes locais.",
    "Acurácia": "Proporção total de classificações corretas de um modelo; em VE, pode indicar quantos municípios foram corretamente classificados como em alerta ou sem alerta.",
    "Ajuste de modelo (model fit)": "Processo de estimar os parâmetros de um modelo a partir dos dados; em VE, ajustar um modelo para prever internações por SRAG com base em séries históricas.",
    "Ajuste excessivo (overfit)": "Situação em que o modelo aprende detalhes demais dos dados de treinamento e perde capacidade de generalizar; em VE, um modelo pode funcionar bem para surtos passados, mas falhar em novas epidemias.",
    "Alfabetização em dados (data literacy)": "Capacidade de ler, interpretar, questionar e usar dados de forma adequada; em VE, permite que equipes compreendam indicadores, gráficos e alertas epidemiológicos.",
    "Análise de dados (data analytics)": "Processo de examinar dados para identificar padrões, tendências, relações e problemas; em VE, analisar a evolução semanal de casos de dengue por município.",
    "API": "Interface que permite que sistemas troquem dados ou serviços de forma padronizada; em VE, uma API pode fornecer dados atualizados de vacinação ou notificações.",
    "Aprendizagem não-supervisionada": "Técnica em que o modelo identifica padrões sem uma variável-resposta definida; em VE, agrupar municípios com perfis semelhantes de risco epidemiológico.",
    "Aprendizagem semi-supervisionada": "Técnica que combina poucos dados rotulados com muitos dados não rotulados; em VE, usar poucos casos confirmados e muitos registros suspeitos para apoiar classificação.",
    "Aprendizagem supervisionada": "Técnica em que o modelo aprende a partir de exemplos com resposta conhecida; em VE, treinar um modelo com municípios já classificados como surto ou não surto.",
    "Banco de dados": "Sistema organizado para armazenar, consultar e gerenciar dados; em VE, pode guardar notificações, exames, internações e óbitos.",
    "Banco de dados NoSQL": "Banco de dados flexível, não necessariamente tabular, usado para dados variados ou de grande volume; em VE, pode armazenar documentos clínicos, JSON de APIs ou registros de sensores.",
    "Banco de dados relacional": "Banco estruturado em tabelas relacionadas por chaves; em VE, pode relacionar casos, municípios, unidades de saúde e resultados laboratoriais.",
    "Computação em nuvem (cloud)": "Uso de servidores e serviços computacionais acessados pela internet; em VE, permite processar grandes bases nacionais sem infraestrutura local própria.",
    "Conjunto de teste": "Parte dos dados reservada para avaliar o desempenho final do modelo; em VE, anos recentes podem ser usados para testar previsão de dengue.",
    "Conjunto de treinamento": "Parte dos dados usada para ajustar o modelo; em VE, séries históricas de casos e clima podem treinar um modelo de previsão.",
    "Data lakehouse": "Arquitetura que combina flexibilidade de data lake com organização analítica de data warehouse; em VE, pode integrar microdados brutos, bases tratadas e tabelas para painéis.",
    "Data mart": "Subconjunto de dados organizado para uma área ou finalidade específica; em VE, um data mart pode conter apenas indicadores de arboviroses para análise municipal.",
    "Data mesh": "Abordagem em que áreas responsáveis pelos dados tratam seus conjuntos como produtos, com governança federada; em VE, equipes de imunização, mortalidade e agravos mantêm produtos de dados interoperáveis.",
    "DataOps": "Conjunto de práticas para automatizar, monitorar e melhorar fluxos de dados; em VE, ajuda a manter pipelines confiáveis para boletins semanais.",
    "DevOps": "Práticas que integram desenvolvimento e operação de sistemas; em VE, facilita implantar e manter painéis, APIs e modelos em produção.",
    "Descida de gradiente": "Método de otimização usado para ajustar modelos minimizando uma função de erro; em VE, pode ser usado no treinamento de modelos preditivos.",
    "ELT": "Processo de extrair, carregar e depois transformar dados no ambiente de destino; em VE, carregar dados brutos do OpenDataSUS em um data lake e tratá-los depois.",
    "Engenharia de dados": "Área responsável por construir pipelines, bancos, integrações e infraestrutura de dados; em VE, garante que notificações sejam coletadas, tratadas e disponibilizadas regularmente.",
    "Enriquecimento de dados": "Adição de informações externas a uma base original; em VE, combinar casos de dengue com chuva, temperatura, população e saneamento.",
    "Erro absoluto médio (MAE)": "Métrica que calcula a média dos erros absolutos entre valores previstos e observados; em VE, mede o erro médio de previsão de casos semanais.",
    "Erro de amostragem": "Diferença entre uma estimativa obtida em uma amostra e o valor real da população; em VE, pode afetar inquéritos sorológicos ou pesquisas de sintomas.",
    "Erro médio quadrático (MSE)": "Métrica que calcula a média dos erros ao quadrado, penalizando erros grandes; em VE, avalia previsões de internações ou casos.",
    "ETL": "Processo de extrair, transformar e carregar dados em um sistema de destino; em VE, baixar notificações, padronizar municípios e carregar em banco analítico.",
    "F-score": "Métrica que combina precisão e revocação em uma única medida; em VE, útil para avaliar modelos de alerta quando falsos positivos e falsos negativos importam.",
    "Falso negativo": "Caso em que o modelo indica ausência de evento, mas o evento realmente existe; em VE, não emitir alerta para um município que entra em surto.",
    "Falso positivo": "Caso em que o modelo indica presença de evento, mas o evento não existe; em VE, emitir alerta de surto para município sem aumento real de casos.",
    "Função de custo": "Função que mede o erro do modelo e orienta seu ajuste; em VE, pode penalizar mais falsos negativos em sistemas de alerta precoce.",
    "Hiperparâmetro": "Configuração definida antes do treinamento do modelo; em VE, número de árvores em um modelo de floresta aleatória para prever risco municipal.",
    "Matriz de confusão": "Tabela que compara classificações previstas e reais, mostrando verdadeiros positivos, falsos positivos, verdadeiros negativos e falsos negativos; em VE, avalia alertas de surto.",
    "Métricas de avaliação": "Medidas usadas para avaliar desempenho de modelos; em VE, incluem acurácia, precisão, revocação, F-score, erro absoluto médio e calibração.",
    "Modelagem de dados": "Definição da estrutura lógica dos dados, suas entidades, campos e relações; em VE, modelar casos, exames, óbitos, municípios e unidades notificadoras.",
    "Modelagem multivariada": "Análise que considera várias variáveis simultaneamente; em VE, avaliar associação entre incidência de dengue, chuva, temperatura e urbanização.",
    "Modelo de linguagem": "Modelo treinado para compreender ou gerar texto; em VE, pode resumir notas técnicas, classificar rumores ou extrair sintomas de textos clínicos.",
    "Negativo verdadeiro": "Resultado em que o modelo indica ausência de evento e isso está correto; em VE, município sem alerta e sem surto real.",
    "Observabilidade dos dados": "Capacidade de monitorar qualidade, atualização, falhas e comportamento dos dados em pipelines; em VE, detectar atraso ou queda inesperada nas notificações.",
    "On-premise": "Infraestrutura computacional instalada e mantida localmente pela instituição; em VE, servidores próprios de uma secretaria de saúde.",
    "Precisão": "Entre os casos classificados como positivos pelo modelo, proporção que realmente é positiva; em VE, entre municípios alertados, quantos realmente tiveram surto.",
    "Processamento em lote (batch processing)": "Processamento de dados em blocos ou períodos definidos; em VE, atualizar indicadores toda madrugada com dados acumulados do dia anterior.",
    "Raiz do erro quadrático médio (RMSE)": "Raiz quadrada do erro médio quadrático, expressa na mesma unidade da variável prevista; em VE, erro médio aproximado em número de casos previstos.",
    "Raspagem de dados (scraping)": "Coleta automatizada de informações de páginas web; em VE, extrair tabelas públicas de boletins epidemiológicos estaduais quando não há API.",
    "Rastreabilidade de dados": "Capacidade de acompanhar origem, transformações e uso dos dados; em VE, saber qual versão da base gerou determinado boletim.",
    "Rede Bayesiana": "Modelo probabilístico que representa relações de dependência entre variáveis; em VE, estimar risco de surto considerando clima, incidência anterior e cobertura de vigilância.",
    "Redes neurais artificiais (RNN)": "Modelos inspirados no funcionamento de redes de neurônios, usados para identificar padrões complexos; em VE, prever séries temporais de SRAG ou dengue.",
    "Redução de dimensionalidade": "Técnica para diminuir o número de variáveis preservando informações relevantes; em VE, resumir muitos indicadores socioambientais em poucos componentes de risco.",
    "Regressão linear": "Modelo que estima uma variável contínua a partir de uma ou mais variáveis explicativas; em VE, estimar taxa de internação a partir de idade média e cobertura vacinal.",
    "Regressão logística": "Modelo usado para estimar a probabilidade de um evento binário; em VE, estimar a chance de um caso evoluir para hospitalização.",
    "Revocação (recall)": "Entre os casos realmente positivos, proporção que o modelo conseguiu identificar; em VE, entre municípios que tiveram surto, quantos foram alertados.",
    "SDK": "Conjunto de ferramentas para desenvolver aplicações que usam determinada plataforma ou serviço; em VE, um SDK pode facilitar o acesso a serviços de nuvem ou APIs de dados.",
    "Seleção de modelos": "Processo de comparar modelos e escolher o mais adequado para o problema; em VE, escolher entre regressão, árvore de decisão e redes neurais para prever dengue.",
    "Serverless": "Modelo em que a infraestrutura é gerenciada pelo provedor e o usuário executa funções sob demanda; em VE, uma função serverless pode atualizar indicadores quando uma nova base chega.",
    "SQL": "Linguagem usada para consultar e manipular bancos de dados relacionais; em VE, consultar número de casos por município e semana epidemiológica.",
    "Streaming": "Processamento contínuo de dados à medida que chegam; em VE, acompanhar notificações quase em tempo real para detectar sinais precoces.",
    "Validação cruzada": "Técnica que avalia o modelo em diferentes divisões dos dados; em VE, testar se o modelo de previsão funciona em diferentes anos ou regiões.",
    "Verdadeiro positivo": "Resultado em que o modelo indica presença de evento e isso está correto; em VE, alerta emitido para município que realmente entrou em surto.",
    "Viés e variância": "Conceitos que descrevem erro sistemático do modelo e sensibilidade excessiva aos dados; em VE, ajudam a equilibrar modelos simples demais ou complexos demais.",
    "z-score": "Medida de quantos desvios-padrão um valor está acima ou abaixo da média; em VE, identificar semanas com incidência muito acima do padrão histórico.",
    "Análise de redes sociais": "Método para estudar relações entre pessoas, instituições, eventos ou lugares como uma rede de conexões; em VE, pode mapear fluxos de transmissão, contatos entre casos ou circulação de rumores sobre surtos.",
    "Aprendizagem por reforço": "Técnica em que um agente aprende a escolher ações por tentativa e erro, recebendo recompensas ou penalidades; em VE, pode apoiar simulações de estratégias de controle vetorial ou alocação dinâmica de recursos.",
    "Backcasting": "Método que parte de um resultado desejado ou observado e reconstrói caminhos possíveis para chegar até ele; em VE, pode analisar retrospectivamente quais sinais anteriores indicavam uma epidemia já ocorrida.",
    "Balanceamento de classes": "Técnica para lidar com bases em que uma categoria é muito mais frequente que outra; em VE, pode evitar que um modelo ignore surtos raros por haver muitos períodos sem surto.",
    "Ciência reprodutível": "Prática de documentar dados, códigos, métodos e versões para que uma análise possa ser repetida; em VE, permite refazer um boletim epidemiológico com a mesma base e obter os mesmos indicadores.",
    "Codificação de dados categóricos (one-hot encoding)": "Transformação de categorias em variáveis binárias para uso em modelos; em VE, transformar categorias como sexo, raça/cor ou classificação final em colunas numéricas para modelagem.",
    "Cold storage": "Armazenamento de baixo custo para dados acessados raramente; em VE, pode guardar versões antigas de bases de notificação para auditoria ou reanálise histórica.",
    "Conformidade legal": "Aderência a leis, normas e regulamentos aplicáveis ao uso de dados; em VE, inclui observar regras de proteção de dados pessoais, sigilo, compartilhamento institucional e publicação segura.",
    "Consentimento informado digital": "Autorização dada eletronicamente por uma pessoa após receber informações claras sobre uso de seus dados; em VE, pode ser usado em aplicativos participatórios de monitoramento de sintomas.",
    "Crowdsourcing de dados": "Coleta de informações fornecidas por muitas pessoas ou instituições de forma distribuída; em VE, cidadãos podem informar sintomas, presença de mosquitos ou falta de medicamentos por aplicativo.",
    "DAMA-DMBOK": "Guia de referência para gestão de dados, com temas como governança, qualidade, arquitetura, segurança e metadados; em VE, pode orientar políticas institucionais para gestão de bases epidemiológicas.",
    "Dados multimodais": "Dados que combinam diferentes tipos de informação, como tabelas, textos, imagens, áudio e localização; em VE, integrar notificações, laudos textuais, imagens de exames e dados climáticos.",
    "Dados semiestruturados": "Dados com alguma organização interna, mas não necessariamente em tabelas fixas, como JSON, XML e logs; em VE, APIs de saúde podem retornar registros em JSON com campos variáveis.",
    "Data wrangling": "Processo de organizar, limpar, transformar e combinar dados para análise; em VE, preparar bases de SINAN, IBGE e INMET para estudar risco de dengue.",
    "Deduplicação": "Identificação e tratamento de registros repetidos; em VE, consolidar notificações duplicadas do mesmo paciente registradas em unidades diferentes.",
    "Explainable AI (XAI)": "Conjunto de métodos para tornar modelos de inteligência artificial mais compreensíveis; em VE, explicar por que um município recebeu alerta de alto risco para arbovirose.",
    "HIPAA": "Lei dos Estados Unidos que estabelece regras de privacidade e segurança para informações de saúde; em VE, serve como referência internacional para proteção de dados clínicos, embora não substitua a legislação brasileira.",
    "Hot storage": "Armazenamento rápido para dados acessados frequentemente; em VE, manter dados recentes de SRAG em ambiente de consulta rápida para atualização de painéis.",
    "IA ética": "Desenvolvimento e uso de inteligência artificial com atenção a justiça, transparência, privacidade, segurança e responsabilidade; em VE, avaliar se um modelo de risco não penaliza territórios com menor capacidade de notificação.",
    "Imputação de dados faltantes": "Preenchimento estimado de valores ausentes por métodos estatísticos ou regras definidas; em VE, estimar campos ausentes de idade ou data quando isso for metodologicamente justificável.",
    "Ingestão de dados": "Entrada de dados em um sistema, banco ou pipeline analítico; em VE, carregar automaticamente arquivos do OpenDataSUS em um ambiente institucional.",
    "ISO 27001": "Norma internacional para sistemas de gestão de segurança da informação; em VE, pode orientar controles de acesso, gestão de riscos e proteção de microdados sensíveis.",
    "LGPD": "Lei Geral de Proteção de Dados brasileira, que regula o tratamento de dados pessoais, incluindo dados sensíveis de saúde; em VE, orienta minimização, segurança, finalidade e acesso controlado a microdados.",
    "Mascaramento de dados": "Técnica para ocultar ou substituir informações sensíveis sem eliminar a utilidade da base; em VE, mascarar CPF, endereço ou nome em bases compartilhadas para análise.",
    "Modelos espaciais": "Modelos que consideram localização, vizinhança e dependência geográfica; em VE, estimar risco de dengue levando em conta municípios próximos e características ambientais.",
    "Overfitting": "Mesmo que ajuste excessivo; ocorre quando o modelo aprende ruídos dos dados de treinamento e perde desempenho em novos dados; em VE, um alerta pode funcionar no passado, mas falhar em outro período epidêmico.",
    "Política de retenção de dados": "Regra que define por quanto tempo dados devem ser guardados, arquivados ou descartados; em VE, estabelecer prazos para manter microdados identificáveis, bases tratadas e snapshots históricos.",
    "Princípios FAIR": "Princípios para tornar dados encontráveis, acessíveis, interoperáveis e reutilizáveis; em VE, melhorar metadados, padrões e documentação de bases epidemiológicas.",
    "Proveniência de dados": "Registro da origem, trajetória e transformações aplicadas aos dados; em VE, saber de qual sistema, data de extração e script veio um indicador publicado.",
    "Segurança da informação": "Conjunto de práticas para proteger dados contra acesso indevido, perda, alteração ou vazamento; em VE, controlar permissões de acesso a bases com dados sensíveis de saúde.",
    "Tokenização": "Divisão de textos em unidades menores, como palavras, subpalavras ou caracteres; em VE, preparar descrições clínicas ou notas de investigação para análise por modelos de linguagem.",
    "Traços digitais (digital traces)": "Registros deixados por interações digitais, como buscas, cliques, posts, localização ou uso de aplicativos; em VE, aumento de buscas por sintomas pode indicar sinal complementar de circulação viral.",
    "Transformação de variáveis": "Modificação de variáveis para melhorar análise ou modelagem; em VE, transformar idade em faixas etárias ou converter datas em semanas epidemiológicas.",
    "Transformação digital em saúde": "Uso estratégico de tecnologias digitais para reorganizar processos, serviços e decisões em saúde; em VE, integrar notificações, painéis, APIs e alertas automatizados para resposta mais rápida.",
    "Underfitting": "Situação em que o modelo é simples demais para capturar os padrões dos dados; em VE, um modelo linear pode não captar sazonalidade complexa de dengue.",
    "Versionamento de dados": "Controle das diferentes versões de uma base ao longo do tempo; em VE, preservar snapshots semanais de notificações para entender mudanças retrospectivas nos números.",
    "Wearable": "Dispositivo vestível que coleta dados de saúde ou comportamento, como relógios inteligentes; em VE, dados agregados de frequência cardíaca, sono ou temperatura podem apoiar vigilância participatória."
    }

# 2. Agrupando os termos por letra inicial
indice = {}
for termo, descricao in sorted(termos.items()):
    letra = termo[0].upper()
    if letra not in indice:
        indice[letra] = []
    indice[letra].append((termo, descricao))

# 3. Criando a interface no Streamlit
st.markdown("## Índice Remissivo")
st.markdown("<div id='topo'></div>", unsafe_allow_html=True)
st.write("Navegue pelos termos organizados alfabeticamente.")

# Menu de atalhos no topo (opcional)
st.write("### Ir para:")
colunas = st.columns(len(indice))
for i, letra in enumerate(sorted(indice.keys())):
    with colunas[i]:
        st.markdown(f"[{letra}](#letra-{letra.lower()})", unsafe_allow_html=True)

st.divider()

# 4. Exibindo as seções com st.expander
for letra in sorted(indice.keys()):
    # Âncora HTML para o link do menu funcionar
    st.markdown(f"<div id='letra-{letra.lower()}'></div>", unsafe_allow_html=True)
    
    with st.expander(f"Letra {letra}", expanded=True):
        for termo, descricao in indice[letra]:
            if descricao.startswith("http"):
                st.markdown(f"- **{termo}**: [Acessar documentação]({descricao})")
            else:
                st.markdown(f"- **{termo}**: {descricao}")
        st.markdown("[↑ Voltar para o topo](#topo)")



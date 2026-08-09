# GP-A20 - Integração da Previsão Analítica com o Núcleo de Monitoramento Hídrico

Data: 27/06/2026

Status: CONCLUÍDA

## Contexto

A GP-A14 / AI-06 identificou que a camada `analytics` possuía decisões próprias para qualidade da água, especialmente em alertas preventivos e Water Health Score.

Pontos identificados na auditoria:

* Uso de `QUALITY_LIMITS` local.
* Alertas preventivos baseados em limites hardcoded.
* Penalidades de qualidade calculadas a partir de faixas locais.
* Risco de divergência com Dashboard e Qualidade da Água já integrados ao Núcleo de Monitoramento Hídrico.

## Alteração Arquitetural

A GP-A20 integrou a Previsão Analítica ao Núcleo de Monitoramento Hídrico para avaliações observacionais de qualidade da água.

Estado após integração:

* `AnalyticsHydricMonitoringAdapter` passa a traduzir medições analíticas de qualidade para parâmetros hídricos do catálogo.
* `PreventiveAlertService` passa a gerar alertas de limite de qualidade a partir de resultados observacionais do núcleo.
* `WaterHealthScoreCalculator` passa a calcular penalidades de qualidade a partir de resultados observacionais do núcleo.
* `QUALITY_LIMITS` deixou de ser usado como autoridade local de decisão observacional.
* Tendências continuam sob responsabilidade da camada `analytics`.
* Leitura dos CSVs continua via `AnalyticsRepository`.
* A interface visual de `PrevisaoAnaliticaPage` foi preservada.

## PA-01

Separação mantida:

* Analytics calcula tendências.
* Policy Engine seleciona a política observacional.
* `AvaliacaoObservacionalService` executa a avaliação.
* Analytics consome o resultado observacional como insumo para alertas e score.

## Limites e Conformidade

A GP-A20 não implementa conformidade legal completa.

As avaliações de qualidade usadas pela Previsão Analítica vêm de `limite_observacional` do catálogo, mantendo caráter observacional e operacional.

## Impacto na AI-06

Veredito atualizado:

INTEGRAÇÃO OBSERVACIONAL DE QUALIDADE CONCLUÍDA COM TENDÊNCIAS PRESERVADAS.

Prioridade remanescente:

MÉDIA.

Lacunas remanescentes:

* Tendências continuam com tolerâncias analíticas próprias, por serem responsabilidade legítima de `analytics`.
* Consumo, perdas e contexto ambiental ainda possuem regras preventivas próprias fora do núcleo hídrico.
* Water Health Score ainda possui pesos executivos/analíticos próprios, mas a decisão de qualidade vem do núcleo.
* Configuração Operacional ainda não define perfil/cenário da Previsão Analítica.

## Testes

Comando executado:

`python -m unittest discover -s tests`

Resultado:

* 56 testes executados.
* Todos passaram.

## Matriz de Conformidade GP-A20

| Critério | Resultado |
| -------- | --------- |
| Preservar interface visual da Previsão Analítica | Atendido |
| Preservar leitura via `AnalyticsRepository` | Atendido |
| Preservar cálculo de tendências | Atendido |
| Não implementar conformidade legal completa | Atendido |
| Analytics calcula tendências | Atendido |
| Policy Engine seleciona política observacional | Atendido |
| Motor Observacional executa avaliação | Atendido |
| Analytics consome resultado observacional como insumo | Atendido |
| Remover autoridade local `QUALITY_LIMITS` para decisão de qualidade | Atendido |
| Evitar divergência com Dashboard e Qualidade da Água | Atendido |
| Manter testes passando | Atendido |

## Veredito

GP-A20 concluída.

A Previsão Analítica continua exibindo tendências, alertas e Water Health Score, mas avaliações de qualidade da água baseadas em limites observacionais passam a vir do Núcleo de Monitoramento Hídrico.

---

# GP-A19 - Integração dos Relatórios Operacionais com o Núcleo de Monitoramento Hídrico

Data: 27/06/2026

Status: CONCLUÍDA

## Diagnóstico Passivo

A auditoria da GP-A19 localizou a responsabilidade de Relatórios Operacionais em `relatorios.py`, classe `RelatoriosPage`.

Achados:

* O módulo lê `data/qualidade_agua_medicoes.csv`, `data/dados_ambientais_medicoes.csv` e `data/consumo_distribuicao_medicoes.csv`.
* A leitura direta de CSV foi preservada nesta GP.
* O módulo exporta `reports/relatorio_operacional.txt`.
* A tela possuía `_quality_status` com limites hardcoded para pH, turbidez, oxigênio dissolvido, temperatura e agrotóxicos.
* O relatório calculava registros fora do padrão com `_quality_status`.
* A última medição de água exibia status calculado localmente.
* Não havia `CONAMA` nem `QUALITY_LIMITS`, mas havia autoridade observacional local equivalente.

## Alteração Arquitetural

A GP-A19 removeu a decisão observacional local dos Relatórios Operacionais.

Estado após integração:

* `OperationalReportsHydricMonitoringAdapter` criado.
* `RelatoriosPage` passou a consumir o adapter para status da última medição.
* `RelatoriosPage` passou a consumir o adapter para contar registros fora do padrão.
* `_quality_status` foi removido de `relatorios.py`.
* Limites hardcoded de qualidade foram removidos de `relatorios.py`.
* CSVs operacionais foram preservados.
* Interface visual e exportação TXT foram preservadas.

## PA-01

Separação mantida:

* Relatórios leem e apresentam dados.
* Policy Engine seleciona a política observacional.
* `AvaliacaoObservacionalService` executa a avaliação.
* Relatórios consomem o status derivado de `ResultadoAvaliacaoObservacional`.

## Impacto na AI-05

Veredito atualizado:

INTEGRAÇÃO OBSERVACIONAL CONCLUÍDA COM PERSISTÊNCIA CSV PRESERVADA.

Prioridade remanescente:

MÉDIA.

Lacunas remanescentes:

* Relatórios ainda leem CSVs diretamente.
* Relatórios ainda não usam Configuração Operacional para definir perfil/cenário.
* Sínteses de médias permanecem cálculos locais de relatório, sem caráter observacional normativo.

## Testes

Comando executado:

`python -m unittest discover -s tests`

Resultado:

* 60 testes executados.
* Todos passaram.

## Matriz de Conformidade GP-A19

| Critério | Resultado |
| -------- | --------- |
| Remover decisão observacional local dos relatórios | Atendido |
| Remover `_quality_status` | Atendido |
| Não usar `CONAMA` local | Atendido |
| Não usar `QUALITY_LIMITS` local como autoridade | Atendido |
| Usar Policy Engine para seleção | Atendido |
| Usar Motor Observacional para execução | Atendido |
| Consumir resultado observacional do núcleo | Atendido |
| Preservar CSV | Atendido |
| Preservar interface | Atendido |
| Preservar PA-01 | Atendido |
| Manter testes passando | Atendido |

## Veredito

GP-A19 concluída.

Os Relatórios Operacionais continuam apresentando resumo operacional, mas deixam de decidir status observacional localmente. O status de qualidade da água passa a ser derivado do Núcleo de Monitoramento Hídrico.

---

# GP-A21 - Integração da Governança Operacional com o Núcleo de Monitoramento Hídrico

Data: 27/06/2026

Status: CONCLUÍDA

## Diagnóstico Passivo

A auditoria da GP-A21 localizou a responsabilidade de Governança Operacional em `governanca_operacional.py` e no pacote `governance`.

Achados:

* A UI não interpreta medições diretamente.
* `OperationalGovernanceService` consome `AnalyticsService`.
* `OperationalGovernanceRules` transforma alertas analíticos em eventos operacionais.
* Não havia `CONAMA`, `QUALITY_LIMITS` ou `check_status` em `governance`.
* A severidade de eventos era copiada do alerta analítico.
* A Governança não persistia política aplicada, status observacional, severidade observacional, origem do limite ou explicabilidade.

## Alteração Arquitetural

A GP-A21 integrou a Governança Operacional ao Núcleo de Monitoramento Hídrico por meio de um adapter de rastreabilidade.

Estado após integração:

* `OperationalGovernanceHydricMonitoringAdapter` criado.
* `OperationalGovernanceService` passa a enriquecer alertas antes de sincronizar eventos.
* Alertas de qualidade da água são reavaliados pelo Núcleo quando possuem valor observado.
* `PolicyEngine` seleciona a política aplicável.
* `AvaliacaoObservacionalService` executa a avaliação.
* Eventos operacionais passam a persistir metadados opcionais de política, resultado observacional e explicabilidade.
* Eventos antigos continuam compatíveis com o JSON existente.
* Interface visual preservada.

## PA-01

Separação mantida:

* Governança acompanha eventos.
* Adapter conecta alertas ao Núcleo.
* Policy Engine seleciona política.
* Motor Observacional executa avaliação.
* Governança consome resultado e metadados, sem produzir avaliação própria.

## Impacto na AI-07

Veredito atualizado:

INTEGRAÇÃO DE RASTREABILIDADE OBSERVACIONAL CONCLUÍDA.

Prioridade remanescente:

MÉDIA.

Lacunas remanescentes:

* A Governança consome `AnalyticsSnapshot.alerts` como fronteira pública preservada.
* Alertas sem valor numérico explícito são preservados sem reavaliação pela Governança.
* A tela ainda não exibe colunas específicas para política e status observacional.

## Veredito C05 - Contrato de Origem de Alertas

Status: ENCERRADO.

O ponto mínimo de desacoplamento foi formalizado pelo protocolo `AlertProvider`, definido em `analytics/alert_provider.py`.

Fronteira preservada:

* `PreventiveAlertService` permanece como provedor padrão e proprietário atual da geração de alertas;
* `AnalyticsService` permanece como orquestrador e raiz de composição;
* `AnalyticsService.alert_service` conforma ao contrato `AlertProvider`;
* existe exatamente uma invocação do provedor por `AnalyticsService.build_snapshot`;
* os campos de `PreventiveAlert` permanecem `severity`, `domain`, `metric`, `message`, `evidence` e `recommendation`;
* o tipo e o significado de `AnalyticsSnapshot.alerts` permanecem inalterados;
* Governança Operacional, Inteligência Executiva, Recomendação Executiva e manutenção de histórico continuam consumindo a mesma fronteira pública;
* nenhuma regra de alerta foi movida e nenhum provedor paralelo foi criado.

Os testes contratuais estão registrados em `tests/test_alert_provider_contract.py` e cobrem encaminhamento de entradas, invocação única, equivalência do provedor padrão, ausência de geração paralela e preservação dos consumidores downstream.

Uma Fase 2 não se justifica pelas evidências atuais. Esta conclusão não autoriza substituição do provedor, mudança de proprietário ou movimentação de regras. Proveniência em nível de regra e fiscalização de efeitos colaterais em runtime permanecem fora do escopo de C05 e não constituem requisitos criados por este fechamento.

## Testes

Comando executado:

`python -m unittest discover -s tests`

Resultado:

* 62 testes executados.
* Todos passaram.

## Matriz de Conformidade GP-A21

| Critério | Resultado |
| -------- | --------- |
| Remover autoridade observacional local | Atendido |
| Não usar `CONAMA` | Atendido |
| Não usar `QUALITY_LIMITS` como decisão local | Atendido |
| Não usar `check_status` | Atendido |
| Policy Engine seleciona política | Atendido |
| Motor Observacional executa avaliação | Atendido |
| Governança consome resultado observacional | Atendido |
| Preservar interface | Atendido |
| Preservar JSON existente | Atendido |
| Preservar PA-01 | Atendido |
| Manter testes passando | Atendido |

## Veredito

GP-A21 concluída.

A Governança Operacional continua acompanhando eventos, mas passa a consumir metadados rastreáveis do Núcleo de Monitoramento Hídrico para alertas de qualidade da água.

---

# GP-A17 - Integracao dos Dados Ambientais com o Nucleo de Monitoramento Hidrico

Data: 27/06/2026

Status: CONCLUIDA SEM ADAPTER FUNCIONAL

## Auditoria Passiva

A auditoria da GP-A17 avaliou `dados_ambientais.py` e os consumidores relacionados aos dados ambientais.

Achados:

* `DadosAmbientaisPage` registra contexto ambiental manual.
* O modulo preserva leitura e escrita direta em `data/dados_ambientais_medicoes.csv`.
* O CSV mantem os campos `timestamp`, `temperatura_ambiente`, `umidade_relativa`, `chuva`, `pressao_atmosferica` e `observacao`.
* A tela exibe historico das medicoes ambientais sem produzir status observacional.
* Nao ha `CONAMA`, `QUALITY_LIMITS`, `check_status`, severidade local, conformidade local ou classificacao observacional local.
* Os ranges de `QDoubleSpinBox` sao restricoes de entrada de formulario, nao limites observacionais de qualidade hidrica.
* `AnalyticsRepository` consome o CSV ambiental como contexto.
* `RelatoriosPage` apresenta a ultima medicao ambiental sem classificar ou avaliar o dado ambiental.
* `DashboardPage` apresenta temperatura e umidade como resumo de contexto.
* Alertas preventivos envolvendo chuva permanecem na camada Analytics e nao na tela de Dados Ambientais.

## Diagnostico Arquitetural

Dados Ambientais atua como produtor de dados contextuais e camada de coleta operacional.

Nao foi identificada autoridade observacional local a ser removida da tela. Portanto, a criacao de `EnvironmentalDataHydricMonitoringAdapter` nao e necessaria nesta GP.

## Plano Aplicado

* Nao alterar codigo funcional.
* Nao alterar interface visual.
* Nao alterar CSV operacional.
* Nao criar adapter sem necessidade arquitetural.
* Registrar a decisao de manter Dados Ambientais como contexto/coleta.
* Manter PA-01 preservado.

## Integracao Existente

Nao ha integracao direta com:

* Configuracao Operacional.
* Catalogo Inteligente.
* Policy Engine.
* Motor Observacional.

Essa ausencia nao e lacuna critica nesta GP porque o modulo nao decide status observacional.

## PA-01

PA-01 preservado.

Dados Ambientais nao seleciona politica e nao executa avaliacao observacional. A tela apenas coleta, persiste e apresenta dados ambientais.

## Impacto na AI-03

Veredito atualizado:

INTEGRACAO POR AUDITORIA CONCLUIDA; ADAPTER HIDRICO NAO NECESSARIO NESTA ETAPA.

Prioridade remanescente:

BAIXA-MEDIA.

Lacunas remanescentes:

* Leitura e escrita direta em CSV permanecem por decisao de compatibilidade.
* Parametros ambientais ainda nao possuem catalogo/metadados operacionais proprios.
* Regras preventivas de chuva continuam na camada Analytics, onde devem ser avaliadas futuramente como regra analitica/contextual, nao como conformidade hidrica.

## Classificacao das Lacunas

| Codigo | Classificacao | Situacao GP-A17 |
| ------ | ------------- | --------------- |
| IA-01 | Duplicacao de Responsabilidade | Nao identificada na tela |
| IA-02 | Acoplamento Direto | Presente pela dependencia direta do CSV |
| IA-03 | Dependencia de CSV | Presente e preservada |
| IA-04 | Logica Duplicada | Nao identificada para avaliacao observacional |
| IA-05 | Servico Nao Utilizado | Nao aplicavel nesta etapa |
| IA-06 | Violacao do PA-01 | Nao identificada |
| IA-07 | Baixa Coesao | Nao identificada como bloqueio |
| IA-08 | Integracao Ausente | Aceita, pois nao ha decisao observacional local |

## Matriz de Conformidade GP-A17

| Criterio | Resultado |
| -------- | --------- |
| Auditar `dados_ambientais.py` | Atendido |
| Verificar ausencia de `CONAMA` | Atendido |
| Verificar ausencia de `QUALITY_LIMITS` | Atendido |
| Verificar ausencia de `check_status` | Atendido |
| Verificar ausencia de classificacao observacional local | Atendido |
| Preservar CSV | Atendido |
| Preservar interface | Atendido |
| Preservar PA-01 | Atendido |
| Criar adapter apenas se necessario | Atendido; adapter nao criado |
| Manter testes passando | Atendido |

## Testes

Comando executado:

`python -m unittest discover -s tests`

Resultado:

* 62 testes executados.
* Todos passaram.

## Veredito

GP-A17 concluida.

Dados Ambientais permanece como camada de contexto e coleta, sem autoridade observacional propria. Nenhuma integracao funcional foi necessaria porque nao havia decisao observacional local a remover.

---

# GP-A18 - Integracao de Consumo e Distribuicao com o Nucleo de Monitoramento Hidrico

Data: 27/06/2026

Status: CONCLUIDA SEM ADAPTER FUNCIONAL

## Auditoria Passiva

A auditoria da GP-A18 avaliou `consumo_distribuicao.py` e os consumidores relacionados ao CSV de consumo e distribuicao.

Achados:

* `ConsumoDistribuicaoPage` registra medicoes operacionais de consumo, distribuicao e perdas.
* O modulo preserva leitura e escrita direta em `data/consumo_distribuicao_medicoes.csv`.
* O CSV mantem os campos `timestamp`, `consumo_diario`, `consumo_mensal`, `volume_distribuido`, `perdas_estimadas` e `observacao`.
* A tela exibe historico das medicoes sem produzir status observacional.
* Nao ha `CONAMA`, `QUALITY_LIMITS`, `check_status`, severidade local, conformidade local ou classificacao observacional local.
* Os ranges de `QDoubleSpinBox` sao restricoes de entrada de formulario, nao limites observacionais hidricos.
* `DashboardPage` apresenta consumo diario e perdas como resumo operacional.
* `RelatoriosPage` apresenta a ultima medicao de consumo sem classificar ou avaliar o dado.
* `AnalyticsRepository` consome o CSV de consumo como insumo operacional.
* `analytics.alerts` e `analytics.scoring` possuem regras preventivas de perdas estimadas, mas essas regras pertencem a camada analitica/operacional e nao a tela de Consumo e Distribuicao.
* `Governanca Operacional` consome alertas derivados de Analytics, sem ler diretamente a tela.

## Diagnostico Arquitetural

Consumo e Distribuicao atua como produtor de dados operacionais e camada de coleta.

Nao foi identificada autoridade observacional local no modulo visual. Portanto, a criacao de `ConsumptionDistributionHydricMonitoringAdapter` nao e necessaria nesta GP.

As regras preventivas de perdas existentes em Analytics devem ser tratadas em uma evolucao propria de indicadores operacionais, sem confundir o Nucleo de Monitoramento Hidrico com motor generico de consumo/distribuicao.

## Plano Aplicado

* Nao alterar codigo funcional.
* Nao alterar interface visual.
* Nao alterar CSV operacional.
* Nao criar adapter sem necessidade arquitetural.
* Registrar a decisao de manter Consumo e Distribuicao como coleta operacional.
* Registrar que regras preventivas de perdas permanecem fora da tela e fora da autoridade observacional hidrica.
* Manter PA-01 preservado.

## Integracao Existente

Nao ha integracao direta com:

* Configuracao Operacional.
* Catalogo Inteligente.
* Policy Engine.
* Motor Observacional.

Essa ausencia nao e lacuna critica nesta GP porque o modulo nao decide status observacional hidrico.

## PA-01

PA-01 preservado.

Consumo e Distribuicao nao seleciona politica e nao executa avaliacao observacional. A tela apenas coleta, persiste e apresenta dados operacionais.

## Impacto na AI-04

Veredito atualizado:

INTEGRACAO POR AUDITORIA CONCLUIDA; ADAPTER HIDRICO NAO NECESSARIO NESTA ETAPA.

Prioridade remanescente:

BAIXA-MEDIA.

Lacunas remanescentes:

* Leitura e escrita direta em CSV permanecem por decisao de compatibilidade.
* Regras preventivas de perdas permanecem em Analytics como inteligencia operacional, nao como conformidade hidrica.

## Veredito C04 - Perdas Estimadas e Consumo

Status: ENCERRADO DOCUMENTALMENTE.

Os limiares `LOSS_MONITORING_THRESHOLD = 15.0` e `LOSS_HIGH_THRESHOLD = 30.0`, definidos em `analytics/loss_thresholds.py`, sao referencias analiticas nao normativas. Nao foi comprovada proveniencia normativa externa ou legal para esses valores.

Efeitos preservados no runtime:

* 15% gera alerta analitico de severidade media e reducao de 6 pontos no Water Health Score;
* 30% gera alerta analitico de severidade alta e reducao de 12 pontos no Water Health Score.

O intervalo de 0% a 100% configurado no campo visual de perdas estimadas e somente validacao de entrada. Ele nao constitui limiar analitico, politica operacional, limite observacional ou regra de conformidade.

Decisao arquitetural:

* nenhuma conformidade hidrica e atribuida a consumo, distribuicao ou perdas;
* o Policy Engine nao recebe autoridade sobre esses indicadores;
* uma camada dedicada de politica operacional nao se justifica pelas evidencias atuais;
* qualquer alteracao futura dos limiares exige nova autoridade e evidencia propria;
* os testes de fronteira permanecem em `tests/test_analytics_loss_thresholds.py`.

## Classificacao das Lacunas

| Codigo | Classificacao | Situacao GP-A18 |
| ------ | ------------- | --------------- |
| IA-01 | Duplicacao de Responsabilidade | Nao identificada na tela |
| IA-02 | Acoplamento Direto | Presente pela dependencia direta do CSV |
| IA-03 | Dependencia de CSV | Presente e preservada |
| IA-04 | Logica Duplicada | Nao identificada para avaliacao observacional hidrica |
| IA-05 | Servico Nao Utilizado | Nao aplicavel nesta etapa |
| IA-06 | Violacao do PA-01 | Nao identificada |
| IA-07 | Baixa Coesao | Nao identificada como bloqueio |
| IA-08 | Integracao Ausente | Aceita, pois nao ha decisao observacional local |

## Matriz de Conformidade GP-A18

| Criterio | Resultado |
| -------- | --------- |
| Auditar `consumo_distribuicao.py` | Atendido |
| Verificar ausencia de `CONAMA` | Atendido |
| Verificar ausencia de `QUALITY_LIMITS` | Atendido |
| Verificar ausencia de `check_status` | Atendido |
| Verificar ausencia de classificacao observacional local | Atendido |
| Verificar dependencias com Dashboard | Atendido |
| Verificar dependencias com Analytics | Atendido |
| Verificar dependencias com Governanca | Atendido |
| Verificar dependencias com Relatorios | Atendido |
| Preservar CSV | Atendido |
| Preservar interface | Atendido |
| Preservar comportamento operacional | Atendido |
| Preservar PA-01 | Atendido |
| Criar adapter apenas se necessario | Atendido; adapter nao criado |
| Manter testes passando | Atendido |

## Testes

Comando executado:

`python -m unittest discover -s tests`

Resultado:

* 62 testes executados.
* Todos passaram.

## Veredito

GP-A18 concluida.

Consumo e Distribuicao permanece como camada operacional de coleta, sem autoridade observacional propria. Nenhuma integracao funcional foi necessaria porque nao havia decisao observacional local a remover.

---

# Conclusao Institucional da GP-A14

Data: 27/06/2026

Status: FILA DE INTEGRACAO ENCERRADA

## GPs Executadas

* GP-A16 - Integracao de Qualidade da Agua / Monitoramento Hidrico.
* GP-A20 - Integracao da Previsao Analitica.
* GP-A19 - Integracao dos Relatorios Operacionais.
* GP-A21 - Integracao da Governanca Operacional.
* GP-A17 - Auditoria/integracao de Dados Ambientais como camada de coleta.
* GP-A18 - Auditoria/integracao de Consumo e Distribuicao como camada operacional de coleta.

## Integracoes Realizadas

* Qualidade da Agua passou a delegar status observacional ao Nucleo de Monitoramento Hidrico.
* Previsao Analitica passou a consumir resultados observacionais do Nucleo para qualidade da agua.
* Relatorios Operacionais passaram a consumir status observacional derivado do Nucleo.
* Governanca Operacional passou a consumir metadados rastreaveis de politica, resultado observacional e explicabilidade.

## Modulos Auditados

* Dashboard.
* Qualidade da Agua / Monitoramento Hidrico.
* Dados Ambientais.
* Consumo e Distribuicao.
* Relatorios Operacionais.
* Previsao Analitica.
* Governanca Operacional.
* Painel Executivo.

## Modulos Que Permaneceram Apenas Como Coleta

* Dados Ambientais.
* Consumo e Distribuicao.

Esses modulos nao possuem autoridade observacional local e nao exigiram adapters hidricos nesta etapa.

## Confirmacao do PA-01

PA-01 confirmado como principio operacional vigente:

* Policy Engine seleciona politicas.
* Motores especializados executam avaliacoes.
* Telas e camadas consumidoras apresentam ou interpretam resultados recebidos.
* Modulos de coleta nao selecionam politica nem executam avaliacao observacional.

## Autoridade Observacional Central

O Nucleo de Monitoramento Hidrico permanece confirmado como autoridade observacional central do sistema para qualidade da agua.

As regras de consumo, distribuicao, perdas e contexto ambiental continuam separadas como indicadores operacionais ou analiticos, sem serem promovidas indevidamente a conformidade hidrica.

## Veredito Institucional

GP-A14 encerrada institucionalmente.

A fila de integracao arquitetural definida pela auditoria foi executada. Os modulos com decisao observacional de qualidade da agua foram integrados ao Nucleo de Monitoramento Hidrico, e os modulos puramente operacionais foram formalmente preservados como coleta/contexto.

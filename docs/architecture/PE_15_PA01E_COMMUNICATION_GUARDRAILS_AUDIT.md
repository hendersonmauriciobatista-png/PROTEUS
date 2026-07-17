# PE-15 - Auditoria Arquitetural da PA-01E

## 1. Identificacao

Programa: **Plano Oficial de Evolucao do PROTEUS**.

Iniciativa: **PA-01 - Governanca de Limites, Responsabilidades e Comunicacao Segura**.

Frente auditada: **PA-01E - Guardrails de Comunicacao entre Camadas**.

Natureza: auditoria arquitetural pre-implementacao, exclusivamente analitica.

Status da GP: **CONCLUIDA**.

Parecer permitido emitido: **PA-01E APTA PARA IMPLEMENTACAO COM RESSALVAS**.

## 2. Objetivo

Auditar os fluxos de comunicacao entre camadas do PROTEUS, identificando comunicacoes conformes, dividas arquiteturais, riscos de bypass e guardrails candidatos para uma futura implementacao da PA-01E.

A auditoria delimita a GP-PE-16 e nao executa refatoracao, criacao de contratos ou alteracao de codigo funcional.

## 3. Escopo

Foram auditadas comunicacoes entre:

* Dashboard;
* telas de coleta e visualizacao;
* Monitoramento Hidrico;
* Analytics;
* Governanca;
* Executive;
* adapters;
* services;
* repositories;
* catalogos;
* configuracoes.

Ficaram fora do escopo:

* implementacao de guardrails;
* criacao de services, adapters ou facades;
* alteracao de contratos;
* alteracao de Analytics, Dashboard ou Executive;
* alteracao de persistencia;
* alteracao do ICFACTORY;
* implantacao de Discoveries congeladas.

## 4. Metodologia

A auditoria aplicou:

1. leitura das auditorias e certificacoes PA-01A a PA-01D;
2. inspecao dos imports e instanciacoes nos arquivos centrais;
3. mapeamento das chamadas diretas entre telas, services, adapters e repositories;
4. identificacao de fluxos via adapter, via service e via contrato;
5. analise de autoridade de comunicacao;
6. classificacao dos fluxos como conforme, divida arquitetural ou violacao;
7. classificacao de guardrails candidatos como obrigatorios, recomendados ou desnecessarios;
8. delimitacao do escopo permitido para GP-PE-16.

Nenhum teste foi executado nesta GP, pois a atividade e pre-implementacao e analitica. Testes existentes foram inspecionados como evidencia de cobertura de fronteira.

## 5. Inventario das comunicacoes

Foram inventariados **22 fluxos de comunicacao** relevantes.

| ID | Origem | Destino | Tipo | Contrato existente | Responsabilidade | Situacao |
| --- | --- | --- | --- | --- | --- | --- |
| C-01 | `DashboardPage` | `DashboardAnalyticsSnapshotService` | via service | Sim | obter serie visual do Water Health Score | Conforme |
| C-02 | `DashboardPage` | `DashboardMonitoringAdapter` | via adapter | Sim | obter status observacional resumido da ultima medicao | Conforme com ressalva |
| C-03 | `DashboardPage` | CSVs via `_read_csv()` | direta/local | Parcial | ler contagens e ultimos registros para cards | Divida arquitetural |
| C-04 | `PrevisaoAnaliticaPage` | `AnalyticsService` | via service | Sim | exibir snapshot analitico | Conforme |
| C-05 | `GovernancaOperacionalPage` | `OperationalGovernanceService` | via service | Sim | listar, sincronizar e transicionar eventos | Conforme |
| C-06 | `PainelExecutivoPage` | `ExecutiveIntelligenceService` | via service | Sim | exibir snapshot executivo | Conforme |
| C-07 | `RelatoriosPage` | CSVs via `_read_csv()` | direta/local | Parcial | compor relatorio operacional | Divida arquitetural |
| C-08 | `RelatoriosPage` | `OperationalReportsHydricMonitoringAdapter` | via adapter | Sim | status observacional e contagem de atencao | Conforme com ressalva |
| C-09 | `QualidadeAguaPage` | CSV de qualidade | direta/local | Parcial | gravar e ler medicoes manuais | Divida arquitetural |
| C-10 | `QualidadeAguaPage` | `QualidadeAguaMonitoringAdapter` | via adapter | Sim | status observacional por linha | Conforme com ressalva |
| C-11 | `DadosAmbientaisPage` | CSV ambiental | direta/local | Parcial | gravar e ler medicoes ambientais | Conforme local |
| C-12 | `ConsumoDistribuicaoPage` | CSV de consumo | direta/local | Parcial | gravar e ler medicoes de consumo | Conforme local |
| C-13 | `AnalyticsService` | `AnalyticsRepository` | via repository | Sim | carregar dados analiticos | Conforme |
| C-14 | `AnalyticsService` | `TrendAnalyzer`, `PreventiveAlertService`, `WaterHealthScoreCalculator` | via componentes internos | Sim | compor snapshot analitico | Conforme |
| C-15 | `PreventiveAlertService` | `AnalyticsHydricMonitoringAdapter` | via adapter | Sim | avaliar qualidade para alertas preventivos | Conforme com ressalva |
| C-16 | `WaterHealthScoreCalculator` | `AnalyticsHydricMonitoringAdapter` | via adapter | Sim | calcular penalidades observacionais do score | Conforme com ressalva |
| C-17 | `DashboardAnalyticsSnapshotService` | `AnalyticsRepository` e `WaterHealthScoreCalculator` | via service analitico | Sim | preparar serie temporal visual | Conforme |
| C-18 | `OperationalGovernanceService` | `AnalyticsService` | via service | Sim | obter alertas atuais para sincronizacao governada | Conforme |
| C-19 | `OperationalGovernanceService` | `OperationalGovernanceHydricMonitoringAdapter` | via adapter | Sim | enriquecer sinais conforme decisao controlada | Conforme com ressalva |
| C-20 | `OperationalGovernanceService` | `OperationalGovernanceRules` e `OperationalEventRepository` | via rules/repository | Sim | sincronizar e persistir eventos | Conforme |
| C-21 | `ExecutiveIntelligenceService` | `AnalyticsService` e `OperationalGovernanceService` | via services | Sim | consolidar snapshot executivo | Conforme com ressalva |
| C-22 | `ExecutiveRecommendationService` | snapshots consolidados de Analytics/Governanca | via dados consolidados | Sim | gerar recomendacoes sem acessar motores internos | Conforme |

Resumo quantitativo:

* comunicacoes conformes ou conformes com ressalva: **19**;
* dividas arquiteturais: **3**;
* violacoes bloqueantes: **0**.

## 6. Mapa arquitetural

Mapa observado:

```text
Interface PyQt
  -> services de leitura/decisao quando existentes
  -> adapters de apresentacao observacional quando existentes
  -> CSV local em telas operacionais historicas

Analytics
  -> AnalyticsRepository
  -> TrendAnalyzer
  -> PreventiveAlertService
  -> WaterHealthScoreCalculator
  -> AnalyticsHydricMonitoringAdapter
  -> Monitoramento Hidrico observacional

Governanca
  -> AnalyticsService
  -> decisao de reavaliacao controlada
  -> OperationalGovernanceHydricMonitoringAdapter
  -> OperationalGovernanceRules
  -> OperationalEventRepository

Executive
  -> AnalyticsService
  -> OperationalGovernanceService
  -> ExecutiveRules
  -> ExecutiveRecommendationService
  -> snapshots consolidados

Monitoramento Hidrico
  -> catalogo
  -> configuracoes
  -> politicas
  -> avaliacao observacional
  -> adapters especificos por consumidor
```

Direcao geral preservada: interface consome services/adapters; services coordenam repositories, rules e adapters; adapters encapsulam avaliacao observacional; repositories encapsulam persistencia.

## 7. Violacoes de fronteira

Nao foram identificadas violacoes bloqueantes.

Foram identificadas dividas arquiteturais e riscos evolutivos:

| ID | Situacao | Classificacao | Evidencia | Impacto |
| --- | --- | --- | --- | --- |
| VF-01 | `DashboardPage` ainda le CSVs diretamente para cards de contagem e ultimos registros. | Divida arquitetural | `main.py`, `_read_csv()` e constantes de CSV. | Pode permitir crescimento de logica de dados na UI. |
| VF-02 | `RelatoriosPage` le CSVs e escreve TXT diretamente. | Divida arquitetural | `relatorios.py`, `_read_csv()` e `export_report()`. | Relatorio pode acumular responsabilidade de repository/export. |
| VF-03 | Telas de coleta manipulam CSV diretamente. | Divida arquitetural local | `qualidade_agua.py`, `dados_ambientais.py`, `consumo_distribuicao.py`. | Aceitavel historicamente, mas exige guardrail para nao virar padrao em novas camadas. |
| VF-04 | Interfaces instanciam `PolicyEngine` e `AvaliacaoObservacionalService` para adapters. | Divida arquitetural | `main.py`, `qualidade_agua.py`, `relatorios.py`. | Pode estimular uso direto de motores por UI se nao houver regra clara. |
| VF-05 | Adapter de Governanca mantem rota de decisao por compatibilidade quando chamado sem `decisions`. | Divida arquitetural controlada | `governance_adapter.py`, `enriquecer_alertas()` e `enriquecer_alerta()`. | Pode ser mal interpretado como autoridade primaria por consumidor futuro. |

## 8. Analise de autoridade

| Fluxo | Autoridade | Consumidor | Contrato intermediario | Bypass identificado? | Conhece detalhe interno? |
| --- | --- | --- | --- | --- | --- |
| Dashboard - serie Water Health Score | Analytics | Dashboard | `DashboardAnalyticsSnapshotService` | Nao | Nao |
| Dashboard - status de qualidade | Monitoramento Hidrico | Dashboard | `DashboardMonitoringAdapter` | Nao | Parcial: UI instancia motores para o adapter |
| Previsao Analitica | Analytics | Tela de previsao | `AnalyticsService` | Nao | Nao |
| Governanca Operacional | Governanca | Tela de governanca | `OperationalGovernanceService` | Nao | Nao |
| Reavaliacao controlada | Governanca | Adapter de Governanca | decisao em `sync_from_analytics()` | Nao na cadeia critica | Adapter preserva fallback |
| Painel Executivo | Executive | Tela executiva | `ExecutiveIntelligenceService` | Nao | Nao |
| Recomendacao Executiva | Executive Recommendation | Executive | `ExecutiveRecommendationService` | Nao | Nao |
| Relatorios | Tela de relatorios | Usuario | Parcial, adapter observacional apenas | Sim, CSV direto | Sim, paths e estrutura CSV |
| Coleta operacional | Tela de coleta | Usuario | Parcial, CSV local | Sim, CSV direto | Sim, schema CSV |
| Configuracoes/Catalogo | Monitoramento Hidrico | Services internos | funcoes de catalogo/configuracao | Nao | Nao |

Conclusao: a autoridade das camadas principais esta preservada, mas ha necessidade de guardrails para impedir que dependencias locais historicas sejam copiadas para novos fluxos.

## 9. Relacao com PA-01A ate PA-01D

### PA-01A

Preservada.

Evidencias:

* `status_semantics.py` continua sendo fonte oficial para status comunicados.
* Adapters e Executive consomem constantes oficiais.
* Nao foi identificado novo vocabulario funcional conflitante na cadeia auditada.

Risco: novas telas ou relatorios podem reintroduzir termos ambiguos se nao houver guardrail de comunicacao semantica.

### PA-01B

Preservada.

Evidencias:

* Dashboard nao instancia `AnalyticsRepository` nem `WaterHealthScoreCalculator` para serie temporal.
* `DashboardAnalyticsSnapshotService` e o contrato intermediario para a serie do score.

Risco: Dashboard ainda le CSVs para cards locais; embora nao reintroduza o acoplamento PA-01B certificado, pode crescer para novo acoplamento se nao for limitado.

### PA-01C

Preservada.

Evidencias:

* adapters usam `quality_parameter_triples()`, `quality_parameter_analytics_entries()` e `quality_parameter_governance_mapping()`.
* Nao foi identificada nova lista paralela de parametros de qualidade nos fluxos auditados.

Risco: novos adapters podem recriar listas locais sem teste/guardrail de importacao.

### PA-01D

Preservada.

Evidencias:

* `OperationalGovernanceService.sync_from_analytics()` inicia a decisao de reavaliacao.
* `OperationalGovernanceHydricMonitoringAdapter` executa a decisao recebida na cadeia critica.
* `ExecutiveRecommendationService` declara e aplica consumo apenas de sinais consolidados.

Risco: chamadas diretas futuras ao adapter de Governanca sem `decisions` podem contornar a autoridade da Governanca.

## 10. Guardrails candidatos

### Guardrails obrigatorios

Foram identificados **5 guardrails obrigatorios**.

| ID | Guardrail | Motivo | Escopo sugerido |
| --- | --- | --- | --- |
| G-OBR-01 | Proibir UI de acessar `AnalyticsRepository` ou `WaterHealthScoreCalculator` diretamente. | Preserva PA-01B. | Teste estatico ja existente pode ser consolidado. |
| G-OBR-02 | Proibir consumidores externos de tratar adapters como autoridade primaria. | Preserva PA-01D. | Matriz de permissao e teste de uso do adapter de Governanca pela cadeia oficial. |
| G-OBR-03 | Proibir recriacao de listas locais de parametros de qualidade. | Preserva PA-01C. | Testes de importacao/strings para adapters e novos consumidores. |
| G-OBR-04 | Proibir novos textos funcionais de status fora do vocabulario oficial. | Preserva PA-01A. | Checklist e teste semantico para termos sensiveis. |
| G-OBR-05 | Proibir Executive de acessar CSV, PolicyEngine, AvaliacaoObservacionalService ou adapters hidricos diretamente. | Preserva separacao Executive. | Teste estatico de imports e documentacao de fronteira. |

### Guardrails recomendados

Foram identificados **4 guardrails recomendados**.

| ID | Guardrail | Motivo | Escopo sugerido |
| --- | --- | --- | --- |
| G-REC-01 | Documentar excecoes historicas de leitura CSV por telas de coleta e relatorios. | Evita que excecao vire padrao. | Matriz "permitido apenas para telas legadas". |
| G-REC-02 | Padronizar factories leves para adapters de UI que hoje recebem `PolicyEngine` e `AvaliacaoObservacionalService`. | Reduz conhecimento de motores pela interface. | Pode ser apenas documentado inicialmente; implementacao futura se necessaria. |
| G-REC-03 | Criar checklist PA-01 para novas telas/services. | Aumenta previsibilidade. | Documento/checklist sem mudanca funcional. |
| G-REC-04 | Ampliar testes de arquitetura para imports proibidos por camada. | Reduz regressao futura. | Testes estaticos semelhantes aos de PA-01B. |

### Guardrails desnecessarios

Foram identificadas **7 comunicacoes com guardrail adicional desnecessario no momento**:

* `PrevisaoAnaliticaPage` -> `AnalyticsService`;
* `GovernancaOperacionalPage` -> `OperationalGovernanceService`;
* `PainelExecutivoPage` -> `ExecutiveIntelligenceService`;
* `AnalyticsService` -> componentes internos de Analytics;
* `OperationalGovernanceService` -> `OperationalGovernanceRules`;
* `OperationalGovernanceService` -> `OperationalEventRepository`;
* `ExecutiveRecommendationService` -> snapshots consolidados.

## 11. Delimitacao da futura implementacao

### Dentro do escopo da GP-PE-16

Podera integrar a GP-PE-16:

* documento de matriz de comunicacoes permitidas e proibidas;
* checklist PA-01 de comunicacao entre camadas;
* testes estaticos de imports proibidos, quando viaveis;
* formalizacao das excecoes historicas de CSV local;
* guardrail para impedir que adapters sejam usados como autoridade primaria;
* guardrail para proteger a fonte unica PA-01C;
* guardrail para proteger vocabulario PA-01A;
* guardrail para preservar PA-01B e PA-01D.

### Fora do escopo da GP-PE-16

Nao deve integrar a GP-PE-16:

* refatoracao ampla de telas;
* criacao de nova arquitetura paralela;
* mudanca de schemas CSV;
* mudanca de persistencia JSON;
* alteracao de regras analiticas;
* alteracao de regras executivas;
* alteracao de politica observacional;
* event bus, scheduler ou workflow externo;
* mudanca metodologica no ICFACTORY;
* implantacao de Discoveries congeladas.

## 12. Achados

| ID | Descricao | Evidencia | Arquivo | Impacto | Severidade | Recomendacao | Bloqueante |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A-01 | Dashboard usa contrato analitico para serie do Water Health Score. | `DashboardAnalyticsSnapshotService`. | `main.py`, `analytics/dashboard_snapshot.py` | Preserva PA-01B. | OBSERVACIONAL | Manter guardrail. | Nao |
| A-02 | Dashboard ainda le CSVs diretamente para cards locais. | `_read_csv()` e constantes CSV. | `main.py` | Risco de crescimento de logica de dados na UI. | MEDIA | Documentar excecao e impedir expansao. | Nao |
| A-03 | Telas de coleta manipulam CSV diretamente. | `_ensure_storage()`, `save_measurement()`, `load_history()`. | `qualidade_agua.py`, `dados_ambientais.py`, `consumo_distribuicao.py` | Persistencia local historica exposta a UI. | MEDIA | Guardrail de excecao legada. | Nao |
| A-04 | Relatorios le CSVs e exporta TXT diretamente. | `_build_report()`, `_read_csv()`, `export_report()`. | `relatorios.py` | Pode acumular responsabilidades de repository/export. | MEDIA | Guardrail recomendado ou facade futura. | Nao |
| A-05 | Interfaces instanciam motores para construir adapters. | `PolicyEngine()` e `AvaliacaoObservacionalService()`. | `main.py`, `qualidade_agua.py`, `relatorios.py` | Risco de uso direto indevido dos motores. | MEDIA | Guardrail/factory leve em GP futura. | Nao |
| A-06 | Analytics acessa Monitoramento Hidrico por adapter, nao por UI. | `AnalyticsHydricMonitoringAdapter`. | `analytics/alerts.py`, `analytics/scoring.py` | Fronteira adequada. | OBSERVACIONAL | Manter. | Nao |
| A-07 | Governanca decide reavaliacao antes do adapter na cadeia critica. | `decisions = [...]` antes de `enriquecer_alertas()`. | `governance/service.py` | Preserva PA-01D. | OBSERVACIONAL | Proteger por guardrail. | Nao |
| A-08 | Adapter de Governanca ainda decide quando chamado diretamente sem `decisions`. | fallback em `enriquecer_alertas()` e `enriquecer_alerta()`. | `monitoramento_hidrico/governance_adapter.py` | Risco de bypass futuro. | ALTA | Guardrail obrigatorio. | Nao |
| A-09 | Executive consome services e snapshots consolidados. | `ExecutiveIntelligenceService` e `ExecutiveRecommendationService`. | `executive/service.py`, `executive_recommendation/service.py` | Fronteira preservada. | OBSERVACIONAL | Proteger imports proibidos. | Nao |

Total de achados: **9**.

## 13. Nao conformidades

Nao foram identificadas nao conformidades bloqueantes.

Foram registradas **3 dividas arquiteturais nao bloqueantes**:

* leitura direta de CSV pelo Dashboard para cards locais;
* leitura/exportacao direta pelo Relatorio;
* manipulacao direta de CSV por telas de coleta.

Total de nao conformidades: **0**.

## 14. Ressalvas

| ID | Ressalva | Impacto | Recomendacao |
| --- | --- | --- | --- |
| R-01 | Existem excecoes historicas de acesso direto a CSV em telas locais. | Medio se copiadas para novos fluxos. | Formalizar como excecao permitida apenas para telas legadas. |
| R-02 | UI instancia motores para construir adapters observacionais. | Medio para fronteira UI/dominio. | Definir guardrail e avaliar factory leve apenas se necessario. |
| R-03 | Adapter de Governanca possui fallback de decisao por compatibilidade. | Alto para consumidores futuros, baixo na cadeia certificada. | Guardrail obrigatorio: autoridade primaria da reavaliacao e `OperationalGovernanceService`. |
| R-04 | Testes de arquitetura cobrem PA-01B, mas ainda nao cobrem matriz completa de imports proibidos. | Medio para regressao futura. | GP-PE-16 pode criar testes estaticos proporcionais. |

Total de ressalvas: **4**.

## 15. Recomendacoes

1. Implementar na GP-PE-16 uma matriz formal de comunicacoes permitidas e proibidas.
2. Criar guardrails obrigatorios para proteger PA-01A, PA-01B, PA-01C e PA-01D.
3. Registrar excecoes historicas de CSV local como permitidas, mas nao replicaveis sem GP propria.
4. Adicionar testes estaticos de imports proibidos quando proporcionais.
5. Evitar refatoracoes amplas na GP-PE-16; a entrega deve ser documental e verificavel, com testes leves se necessario.
6. Nao implementar novas funcionalidades, event bus, scheduler, workflow, alteracoes executivas, analiticas ou de persistencia.

## 16. Parecer final

A arquitetura atual do PROTEUS apresenta comunicacoes majoritariamente coerentes com as frentes PA-01A, PA-01B, PA-01C e PA-01D.

Nao foram identificadas violacoes bloqueantes de fronteira. Foram identificadas dividas arquiteturais e riscos evolutivos que justificam a implementacao da PA-01E como uma camada de guardrails documentais e verificaveis.

Parecer final: **PA-01E APTA PARA IMPLEMENTACAO COM RESSALVAS**.


# PE-12 - Auditoria Arquitetural da PA-01D

## 1. Identificacao

Programa: **Plano Oficial de Evolucao do PROTEUS**.

Iniciativa: **PA-01 - Governanca de Limites, Responsabilidades e Comunicacao Segura**.

Frente auditada: **PA-01D - Governanca da Reavaliacao Controlada**.

Natureza: auditoria arquitetural pre-implementacao, exclusivamente analitica.

Status da GP: **CONCLUIDA**.

Parecer final: **PA-01D APTA PARA IMPLEMENTACAO COM RESSALVAS**.

## 2. Objetivo

Auditar os mecanismos atuais de reavaliacao, recalculo, recomposicao, sincronizacao, refresh, recarregamento e reconstrucao de informacoes derivadas do PROTEUS, delimitando com precisao o escopo de uma futura implementacao da PA-01D.

A auditoria nao pressupoe defeito: seu objetivo e descobrir a arquitetura atual, mapear responsabilidades e separar reavaliacoes que exigem governanca de atualizacoes locais ou visuais.

## 3. Escopo

Foram auditados mecanismos relacionados a:

* reavaliacao observacional;
* recalculo analitico;
* recomposicao de snapshots;
* sincronizacao de eventos;
* atualizacao de indicadores;
* refresh de telas;
* recarregamento de historicos;
* reconstrucao de informacoes derivadas.

Ficaram fora do escopo:

* alteracao de codigo;
* refatoracao;
* criacao de novos servicos;
* criacao de eventos;
* alteracao de modelos;
* alteracao de persistencia;
* alteracao de Dashboard;
* alteracao de Analytics;
* implementacao de PA-01D;
* implementacao de PA-01E;
* alteracao do ICFACTORY;
* implantacao de Discoveries congeladas.

## 4. Base documental

Foram utilizados:

* `docs/architecture/PE_03_PA01_IMPLEMENTATION_DECOMPOSITION.md`;
* `docs/architecture/PE_05_PA01A_IMPLEMENTATION_AUDIT.md`;
* `docs/architecture/PE_08_PA01B_POST_IMPLEMENTATION_AUDIT.md`;
* `docs/architecture/PE_11_PA01C_POST_IMPLEMENTATION_AUDIT.md`;
* `docs/pac/PE_01_IMPLEMENTATION_EXECUTION_STRATEGY.md`;
* `docs/pac/PAC_14_PROJECT_EVOLUTION_PLAN.md`;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`;
* codigo atual do PROTEUS;
* testes existentes;
* documentacao operacional e arquitetural vigente.

## 5. Metodologia

A auditoria aplicou:

1. busca textual por `refresh`, `reload`, `update`, `recalculate`, `recompute`, `rebuild`, `sync`, `invalidate`, `reprocess`, `reavaliar`, `atualizar`, `recalcular`, `carregar`, `build_snapshot`, `avaliar`, `enriquecer`, `load_`, `QTimer`, `connect`;
2. inspecao dos fluxos de Dashboard, Analytics, Governanca, Painel Executivo, Relatorios e telas de coleta;
3. classificacao dos mecanismos como manuais, automaticos, periodicos, observacionais, derivados, analiticos ou operacionais;
4. mapeamento de quem decide, quem executa, quem consome e se existe autoridade definida;
5. analise de reprocessamentos redundantes e consistencia temporal;
6. verificacao de relacao com PA-01A, PA-01B e PA-01C;
7. avaliacao da cobertura de testes existente.

Nenhum teste foi executado nesta GP, pois a atividade e pre-implementacao e analitica. Os testes existentes foram inspecionados como evidencia de cobertura.

## 6. Inventario das reavaliacoes

Mecanismos relevantes identificados: **14**.

| ID | Arquivo | Componente | Evento disparador | Dados utilizados | Resultado produzido | Classificacao |
| --- | --- | --- | --- | --- | --- | --- |
| RV-01 | `qualidade_agua.py` | `QualidadeAguaPage.load_history()` | Inicializacao e salvamento de medicao | CSV de qualidade | Tabela de historico e status observacional por linha | Manual/local/observacional |
| RV-02 | `dados_ambientais.py` | `DadosAmbientaisPage.load_history()` | Inicializacao e salvamento de medicao | CSV ambiental | Tabela de historico ambiental | Manual/local |
| RV-03 | `consumo_distribuicao.py` | `ConsumoDistribuicaoPage.load_history()` | Inicializacao e salvamento de medicao | CSV de consumo | Tabela de historico de consumo | Manual/local |
| RV-04 | `main.py` | `DashboardPage.refresh()` | Inicializacao e navegacao | CSVs de qualidade, ambiente e consumo; adapter de Dashboard; snapshot analitico | Cards, status de qualidade e grafico | Derivada/visual |
| RV-05 | `analytics/dashboard_snapshot.py` | `DashboardAnalyticsSnapshotService.water_health_score_series()` | Refresh do Dashboard | Historico de qualidade, ambiente e consumo | Serie temporal do Water Health Score | Analitica/derivada |
| RV-06 | `previsao_analitica.py` | `PrevisaoAnaliticaPage.refresh()` | Inicializacao e botao "Atualizar Analise" | `AnalyticsService.build_snapshot()` | Tabelas de tendencias, alertas e score | Manual/analitica |
| RV-07 | `analytics/service.py` | `AnalyticsService.build_snapshot()` | Chamadas de Previsao, Governanca, Executive e testes | CSVs via repository | Trends, alertas e Water Health Score | Analitica/derivada |
| RV-08 | `analytics/alerts.py` | `PreventiveAlertService.build_alerts()` | Build de snapshot analitico | Medicoes, tendencias e adapter hidrico | Alertas preventivos | Analitica/observacional |
| RV-09 | `analytics/scoring.py` | `WaterHealthScoreCalculator.calculate()` | Build de snapshot e serie temporal | Medicoes de qualidade, ambiente e consumo | Water Health Score e explicacoes | Analitica/observacional |
| RV-10 | `governance/service.py` | `OperationalGovernanceService.sync_from_analytics()` | Botao "Sincronizar Alertas" ou chamada de service | Eventos persistidos e snapshot analitico | Eventos criados/atualizados em JSON | Manual/operacional/derivada |
| RV-11 | `monitoramento_hidrico/governance_adapter.py` | `OperationalGovernanceHydricMonitoringAdapter.enriquecer_alerta()` | Sincronizacao de alertas de Governanca | Alerta analitico, evidencias textuais, PolicyEngine e motor observacional | `GovernanceHydricSignal` enriquecido | Observacional/reavaliacao |
| RV-12 | `governance/rules.py` | `OperationalGovernanceRules.sync_alerts()` e `update_existing_event()` | Sincronizacao de alertas | Eventos ativos e sinais enriquecidos | Evento novo ou atualizacao de evento ativo | Operacional/derivada |
| RV-13 | `painel_executivo.py`, `executive/service.py` | `PainelExecutivoPage.refresh()` e `ExecutiveIntelligenceService.build_snapshot()` | Inicializacao e botao "Atualizar Painel" | Snapshot analitico, eventos e resumo de governanca | Snapshot executivo e recomendacoes | Manual/derivada/executiva |
| RV-14 | `relatorios.py` | `RelatoriosPage.refresh()` e `_build_report()` | Inicializacao, navegacao e exportacao | CSVs e adapter de relatorio | Relatorio operacional em memoria/TXT | Manual/local/derivada |

Mecanismos puramente visuais identificados e nao contabilizados como candidatos centrais:

* `MainWindow._update_clock()` com `QTimer`, restrito ao relogio da barra de status;
* `WaterHealthScoreChart.set_points()`, restrito a pintura do grafico;
* `MainWindow._navigate()`, que apenas chama `refresh()` da pagina atual e foi considerado disparador indireto.

## 7. Cadeia de responsabilidades

### RV-10/RV-11/RV-12 - Cadeia critica de Governanca

```text
Operador aciona "Sincronizar Alertas"
    ->
Governanca decide sincronizar via OperationalGovernanceService.sync_from_analytics()
    ->
AnalyticsService.build_snapshot() recompõe alertas atuais
    ->
OperationalGovernanceHydricMonitoringAdapter.enriquecer_alertas()
    ->
Adapter reavalia alerta de qualidade quando ha valor numerico
    ->
OperationalGovernanceRules.sync_alerts()
    ->
Eventos sao criados ou atualizados
    ->
OperationalEventRepository.save_events()
```

Responsabilidade observada:

| Pergunta | Resposta |
| --- | --- |
| Quem decide reavaliar? | A decisao e implicita na chamada de `sync_from_analytics()`; o adapter decide por dominio/metrica/evidencia numerica. |
| Quem executa? | `OperationalGovernanceHydricMonitoringAdapter` executa a reavaliacao observacional. |
| Quem consome? | `OperationalGovernanceRules` e `OperationalEventRepository`, por meio de sinais enriquecidos. |
| Existe autoridade definida? | Parcialmente: o motor observacional ainda avalia, mas falta contrato explicito de pre-condicoes e finalidade. |
| Existe duplicidade de decisao? | Existe potencial: Analytics ja avaliou a qualidade para criar alerta e Governanca reavalia o valor textual. |

### RV-07/RV-08/RV-09 - Cadeia analitica

```text
Tela ou service solicita snapshot
    ->
AnalyticsService le CSVs
    ->
TrendAnalyzer calcula tendencias
    ->
PreventiveAlertService gera alertas
    ->
WaterHealthScoreCalculator calcula score
    ->
Consumidores exibem ou encaminham resultado
```

Responsabilidade observada: Analytics decide e executa recomposicao analitica; resultados nao sao persistidos diretamente nessa camada.

### RV-05 - Cadeia temporal do Dashboard

```text
Dashboard refresh
    ->
DashboardAnalyticsSnapshotService le historicos
    ->
Para cada medicao de qualidade, calcula score parcial ate aquele timestamp
    ->
Dashboard renderiza serie visual
```

Responsabilidade observada: service analitico intermediario executa recomposicao temporal para visualizacao. A UI consome o resultado, preservando PA-01B.

### RV-13 - Cadeia executiva

```text
Painel Executivo refresh
    ->
ExecutiveIntelligenceService.build_snapshot()
    ->
AnalyticsService.build_snapshot()
    ->
GovernanceService.list_events() e summarize_by_state()
    ->
ExecutiveRules e ExecutiveRecommendationService
    ->
Painel renderiza snapshot
```

Responsabilidade observada: camada executiva recompoe visao consolidada, sem acessar PolicyEngine ou motor observacional diretamente.

## 8. Analise de reprocessamentos

| ID | Mecanismo | Reprocessamento observado | Classificacao | Avaliacao |
| --- | --- | --- | --- | --- |
| RP-01 | `OperationalGovernanceService.sync_from_analytics()` | A cada sincronizacao, Analytics recompõe snapshot e Governanca pode reavaliar alertas de qualidade. | Necessario com ressalva | Exige governanca obrigatoria por persistir eventos e poder atualizar ocorrencias. |
| RP-02 | `OperationalGovernanceHydricMonitoringAdapter.enriquecer_alerta()` | Reavalia valor que originou alerta analitico. | Necessario com ressalva | Deve ser formalizado como enriquecimento, nao decisao primaria. |
| RP-03 | `OperationalGovernanceRules.sync_alerts()` | Repetir sync do mesmo alerta incrementa ocorrencia e atualiza timestamps/evidencias. | Necessario com ressalva | Evita duplicidade por fingerprint, mas precisa regra clara de idempotencia semantica. |
| RP-04 | `AnalyticsService.build_snapshot()` | Pode ser chamado por Previsao, Governanca e Executive, recomputando leituras e derivados. | Evitavel/recomendado | Recomposicao legitima, mas sem snapshot_id ou geracao temporal comum. |
| RP-05 | `DashboardAnalyticsSnapshotService.water_health_score_series()` | Recalcula score para varios recortes temporais. | Necessario para visualizacao | Pode ser custoso no futuro; hoje e visual e sem persistencia. |
| RP-06 | `ExecutiveIntelligenceService.build_snapshot()` | Rechama Analytics e Governanca ao montar painel. | Observacional/recomendado | Legitimamente consolidado, mas pode divergir temporalmente de uma sincronizacao recem executada. |
| RP-07 | Telas de coleta e relatorios | Releem CSV e recomputam visualizacao ao salvar, navegar ou exportar. | Local | Baixo risco; nao altera estado derivado relevante. |

## 9. Consistencia temporal

Riscos observados:

| ID | Situacao | Risco temporal | Impacto | Classificacao |
| --- | --- | --- | --- | --- |
| CT-01 | Governanca sincroniza a partir de um snapshot analitico gerado no momento da chamada. | Se os CSVs mudarem durante ou logo apos o snapshot, eventos persistidos podem representar um recorte temporal nao identificado. | Medio | Ressalva |
| CT-02 | Governanca reavalia valor extraido de texto do alerta, nao uma referencia estruturada a medicao original. | Perda de rastreabilidade entre alerta, medicao original e reavaliacao. | Medio/alto | Nao conformidade evolutiva |
| CT-03 | Executive monta novo snapshot analitico separado da sincronizacao de governanca. | Painel pode exibir analytics atuais e eventos gerados por snapshot anterior. | Medio | Ressalva |
| CT-04 | Dashboard temporal calcula score por prefixos de qualidade e filtra ambiente/consumo por timestamp. | Boa tentativa de consistencia temporal visual, mas registros sem timestamp entram em todos os recortes. | Baixo/medio | Ressalva |
| CT-05 | Repeticao de `sync_from_analytics()` atualiza `updated_at`, `last_seen_at` e `occurrence_count`. | Uma mesma evidencia recorrente pode parecer novo acompanhamento sem metadado de ciclo de sincronizacao. | Medio | Nao conformidade evolutiva |

Nao foi encontrado processamento periodico automatico relevante alem do relogio visual da barra de status.

## 10. Relacao com PA-01A, PA-01B e PA-01C

### PA-01A

Os mecanismos atuais preservam a semantica oficial:

* adapters usam rotulos observacionais oficiais;
* Water Health Score usa vocabulario oficial de score analitico;
* Painel Executivo usa status executivo observacional.

Ressalva: a reavaliacao de Governanca ainda comunica explicabilidade tecnica do motor (`resultado`, `origem`) sem contrato especifico de pre-condicao e finalidade para PA-01D.

### PA-01B

Preservada:

* Dashboard continua consumindo `DashboardAnalyticsSnapshotService`;
* Dashboard nao instancia diretamente `AnalyticsRepository` nem `WaterHealthScoreCalculator`;
* recomposicao temporal do score permanece fora da classe `DashboardPage`.

### PA-01C

Preservada:

* `OperationalGovernanceHydricMonitoringAdapter` consome `quality_parameter_governance_mapping()`;
* adapters analiticos e de UI usam a fonte oficial de parametros quando aplicavel;
* nao foi identificada lista paralela de parametros de qualidade introduzida por reavaliacao.

## 11. Analise dos testes

Testes existentes relacionados:

| Teste | Mecanismo exercitado | Cobertura |
| --- | --- | --- |
| `tests/test_governance_monitoring_adapter.py` | Enriquecimento/reavaliacao de alerta de qualidade e preservacao de alerta nao hidrico. | Parcial: cobre positivo e nao qualidade, mas nao valor ausente, motor nao observacional ou metadado de ciclo. |
| `tests/test_governance_service.py` | `sync_from_analytics()`, persistencia de eventos e transicoes manuais. | Parcial: cobre criacao e fluxo de estados, mas nao repeticao de sync, snapshot_id ou consistencia temporal. |
| `tests/test_governance_rules.py` | Duplicidade por fingerprint, `occurrence_count` e transicoes. | Adequada para regra atual; parcial para governanca futura de reavaliacao. |
| `tests/test_dashboard_analytics_snapshot.py` | Serie temporal do Dashboard e ausencia de dependencia direta no Dashboard. | Adequada para PA-01B; parcial para consistencia temporal ampliada. |
| `tests/test_analytics_alerts.py` | Alertas analiticos de qualidade e contexto. | Parcial para alertas; nao cobre rastreabilidade de reavaliacao pela Governanca. |
| `tests/test_water_health_score.py` | Recalculo do score analitico. | Adequada para score; fora da reavaliacao governada persistida. |
| `tests/test_executive_service.py` | Recomposicao do snapshot executivo. | Parcial para camada executiva; nao cobre divergencia temporal entre Analytics e Governanca. |

Classificacao geral da cobertura para PA-01D: **cobertura parcial**.

Nao foram criados ou alterados testes nesta GP.

## 12. Candidatos a governanca

### Governanca obrigatoria

Quantidade: **3**.

| ID | Mecanismo | Justificativa |
| --- | --- | --- |
| GOB-01 | `OperationalGovernanceService.sync_from_analytics()` | Altera estado derivado persistido, pode executar multiplas vezes e influencia eventos operacionais. |
| GOB-02 | `OperationalGovernanceHydricMonitoringAdapter.enriquecer_alerta()` | Reavalia valor numerico de alerta de qualidade e pode alterar severidade/metadados observacionais do sinal governado. |
| GOB-03 | `OperationalGovernanceRules.sync_alerts()` / `update_existing_event()` | Atualiza eventos ativos, timestamps, ocorrencias, evidencia e metadados observacionais. |

### Governanca recomendada

Quantidade: **5**.

| ID | Mecanismo | Justificativa |
| --- | --- | --- |
| GRE-01 | `AnalyticsService.build_snapshot()` | Ponto central de recomposicao analitica; recomendavel expor metadados de geracao quando consumido por Governanca/Executive. |
| GRE-02 | `PreventiveAlertService.build_alerts()` | Origem dos alertas reavaliados; recomendavel preservar contexto estruturado quando possivel. |
| GRE-03 | `WaterHealthScoreCalculator.calculate()` | Recalculo observacional para score; recomendavel manter separado da reavaliacao de Governanca. |
| GRE-04 | `DashboardAnalyticsSnapshotService.water_health_score_series()` | Recalculo temporal visual; recomendavel manter isolado e sem persistencia. |
| GRE-05 | `ExecutiveIntelligenceService.build_snapshot()` / `ExecutiveRecommendationService.build_snapshot()` | Recompõe visao executiva; recomendavel registrar que consome sinais consolidados e nao reavalia. |

### Governanca desnecessaria ou local

Quantidade: **6**.

| ID | Mecanismo | Justificativa |
| --- | --- | --- |
| LOC-01 | `QualidadeAguaPage.load_history()` | Recalculo local de tabela sem persistir derivado. |
| LOC-02 | `DadosAmbientaisPage.load_history()` | Recarregamento visual sem avaliacao. |
| LOC-03 | `ConsumoDistribuicaoPage.load_history()` | Recarregamento visual sem avaliacao. |
| LOC-04 | `RelatoriosPage.refresh()` / `_build_report()` | Recalculo local de relatorio; pode ser documentado, mas nao exige PA-01D obrigatoria. |
| LOC-05 | `DashboardPage.refresh()` | Composicao visual que delega analytics e adapter; governanca ja fica nos services consumidos. |
| LOC-06 | `MainWindow._navigate()` e `QTimer` do relogio | Disparadores visuais/locais; sem resultado derivado governavel. |

## 13. Delimitacao da futura implementacao

### Dentro do escopo da GP-PE-13

1. Formalizar contrato de reavaliacao controlada para `OperationalGovernanceHydricMonitoringAdapter`.
2. Declarar pre-condicoes para reavaliacao:
   * alerta de `qualidade_agua`;
   * metrica conhecida pela fonte PA-01C;
   * evidencia com valor numerico extraivel;
   * politica com motor observacional;
   * finalidade restrita a enriquecimento governado.
3. Registrar metadados de finalidade e origem da reavaliacao no sinal/evento sem alterar schema de forma incompatível.
4. Garantir que a reavaliacao nao substitui o alerta analitico original.
5. Tornar explicita a diferenca entre:
   * avaliacao original do Analytics;
   * enriquecimento observacional da Governanca;
   * persistencia do evento operacional.
6. Adicionar guardas para nao reavaliar sinais fora de qualidade da agua.
7. Adicionar ou ajustar testes de:
   * pre-condicoes;
   * nao reavaliacao;
   * repeticao de sync;
   * preservacao da avaliacao original;
   * rastreabilidade dos metadados.
8. Documentar que `sync_from_analytics()` e ponto governado de sincronizacao manual.

### Fora do escopo da GP-PE-13

* alterar Analytics;
* alterar formula do Water Health Score;
* alterar Dashboard;
* alterar Painel Executivo;
* mudar schema CSV;
* criar filas, eventos de dominio ou scheduler;
* transformar `AnalyticsService.build_snapshot()` em cache global;
* criar nova arquitetura de snapshot;
* implementar PA-01E;
* alterar regras executivas;
* alterar ICFACTORY;
* implantar Discoveries congeladas.

## 14. Achados

Quantidade de achados: **7**.

| ID | Titulo | Evidencia | Impacto | Severidade | Recomendacao | Bloqueante |
| --- | --- | --- | --- | --- | --- | --- |
| PE12-A01 | Reavaliacao governada existe e esta localizada | `OperationalGovernanceHydricMonitoringAdapter.enriquecer_alerta()` chama `evaluation_service.avaliar()`. | Permite implementar PA-01D de forma pequena. | ALTA | Formalizar pre-condicoes e finalidade. | Nao |
| PE12-A02 | Sincronizacao altera estado persistido | `OperationalGovernanceService.sync_from_analytics()` salva eventos apos sync. | Repeticoes podem alterar eventos. | ALTA | Governar sync como operacao manual rastreavel. | Nao |
| PE12-A03 | Repeticao de sync atualiza ocorrencias | `OperationalGovernanceRules.update_existing_event()` incrementa `occurrence_count` e timestamps. | Pode inflar leitura de recorrencia sem ciclo explicito. | MEDIA | Registrar ciclo/origem da sincronizacao em GP futura. | Nao |
| PE12-A04 | Reavaliacao usa valor extraido de texto | `_extract_current_value()` usa regex sobre `alert.evidence`. | Rastreabilidade estrutural limitada. | MEDIA | Preferir metadados estruturados se houver GP futura; por ora documentar limite. | Nao |
| PE12-A05 | Snapshots analiticos sao recomputados em varios consumidores | Previsao, Governanca e Executive chamam `build_snapshot()`. | Possivel divergencia temporal entre telas. | MEDIA | Nao alterar agora; registrar como ressalva temporal. | Nao |
| PE12-A06 | Dashboard temporal recalcula score por recorte | `water_health_score_series()` calcula score para cada medicao de qualidade. | Legitimo para visualizacao, mas pode ser custoso futuramente. | BAIXA | Manter isolado; nao incluir em PA-01D obrigatoria. | Nao |
| PE12-A07 | Cobertura de testes de PA-01D e parcial | Testes cobrem fluxo feliz e duplicidade por fingerprint, mas nao todas as pre-condicoes. | Risco de regressao em futura implementacao. | MEDIA | GP-PE-13 deve adicionar testes especificos. | Nao |

## 15. Nao conformidades

Quantidade de nao conformidades: **3**.

| ID | Situacao | Impacto | Recomendacao |
| --- | --- | --- | --- |
| NC-PA01D-01 | Reavaliacao de Governanca nao possui contrato explicito de pre-condicoes, finalidade e limites. | Pode ser interpretada como autoridade observacional paralela se expandida. | Criar contrato/guardas na GP-PE-13. |
| NC-PA01D-02 | Reavaliacao usa valor extraido da evidencia textual do alerta. | Dificulta rastrear a medicao original e distinguir avaliacao original de enriquecimento. | Documentar como limite e, se possivel sem schema amplo, registrar origem/finalidade do enriquecimento. |
| NC-PA01D-03 | Repeticao de sincronizacao atualiza evento ativo sem metadado de ciclo de sincronizacao. | Pode gerar ambiguidade entre novo evento, nova ocorrencia e reprocessamento do mesmo recorte. | Formalizar semantica de `occurrence_count`, `last_seen_at` e `updated_at` para reavaliacao. |

Nenhuma nao conformidade impede a implementacao futura, desde que a GP-PE-13 permaneça restrita.

## 16. Ressalvas

Quantidade de ressalvas: **4**.

1. `AnalyticsService.build_snapshot()` e recomposto por diferentes consumidores sem snapshot_id comum; isso e aceitavel no estado atual, mas deve ser reconhecido antes de governar sincronizacao.
2. `ExecutiveIntelligenceService.build_snapshot()` pode representar recorte temporal diferente dos eventos ja persistidos pela Governanca.
3. `DashboardAnalyticsSnapshotService.water_health_score_series()` recalcula scores historicos apenas para visualizacao; nao deve ser arrastado para PA-01D obrigatoria.
4. Telas e relatorios fazem refresh local e releitura de CSV; sao mecanismos locais e nao devem virar alvo de governanca pesada nesta frente.

## 17. Recomendacoes

1. Implementar a GP-PE-13 exclusivamente sobre a cadeia `sync_from_analytics()` -> `enriquecer_alertas()` -> `sync_alerts()`.
2. Declarar a reavaliacao da Governanca como **enriquecimento observacional governado**, nao como decisao primaria.
3. Preservar o alerta analitico original e adicionar metadados que diferenciem avaliacao original, reavaliacao e persistencia do evento.
4. Criar testes de nao reavaliacao para:
   * alerta fora de `qualidade_agua`;
   * metrica fora do mapeamento PA-01C;
   * evidencia sem valor numerico;
   * politica fora do motor observacional.
5. Testar repeticao de sync para garantir que `occurrence_count`, `last_seen_at` e `updated_at` tenham semantica documentada.
6. Nao alterar Analytics, Dashboard, Executive, CSV ou modelos amplos nesta etapa.
7. Manter PA-01E fora da GP-PE-13, exceto por referencias documentais aos limites de responsabilidade.

## 18. Parecer final

**PA-01D APTA PARA IMPLEMENTACAO COM RESSALVAS**.

Justificativa:

* o mecanismo central de reavaliacao esta localizado;
* a cadeia de responsabilidade foi mapeada;
* os pontos de reprocessamento foram identificados;
* ha testes parciais ja existentes;
* PA-01A, PA-01B e PA-01C permanecem preservadas;
* a futura implementacao pode ser pequena, testavel e reversivel;
* as nao conformidades sao evolutivas e delimitam exatamente o trabalho da GP-PE-13.

Condicao para a GP-PE-13:

Implementar apenas a governanca da reavaliacao na Governanca Operacional, sem alterar Analytics, Dashboard, Executive, persistencia CSV, ICFACTORY ou Discoveries congeladas.

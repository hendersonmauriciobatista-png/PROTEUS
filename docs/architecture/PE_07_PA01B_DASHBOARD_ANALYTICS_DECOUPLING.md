# PE-07 - Implementacao da PA-01B

## 1. Objetivo

Implementar a frente **PA-01B - Desacoplamento entre Dashboard e Analytics**, removendo exclusivamente os acoplamentos certificados pela GP-PE-06 entre `DashboardPage` e os componentes internos de Analytics.

## 2. Escopo

Esta GP atua somente sobre:

* dependencia direta de `DashboardPage` para `AnalyticsRepository`;
* dependencia direta de `DashboardPage` para `WaterHealthScoreCalculator`;
* composicao temporal analitica antes executada em `_water_health_score_series()`.

Ficam preservados:

* `DashboardMonitoringAdapter`;
* `WaterHealthScoreChart`;
* comportamento visual observavel;
* semantica oficial de status da PA-01A;
* persistencia CSV;
* formula e criterios do Water Health Score;
* componentes nao participantes dos tres acoplamentos certificados.

## 3. Base documental

Foram utilizados como base:

* `docs/architecture/PE_06_PA01B_ARCHITECTURAL_AUDIT.md`;
* `docs/architecture/PE_03_PA01_IMPLEMENTATION_DECOMPOSITION.md`;
* `docs/architecture/PE_02_PA01_ARCHITECTURAL_AUDIT.md`;
* `docs/architecture/PE_05_PA01A_IMPLEMENTATION_AUDIT.md`;
* `docs/pac/PE_01_IMPLEMENTATION_EXECUTION_STRATEGY.md`;
* `docs/pac/PAC_14_PROJECT_EVOLUTION_PLAN.md`;
* arquitetura atual do PROTEUS;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`.

## 4. Diagnostico herdado da GP-PE-06

A GP-PE-06 classificou como divida arquitetural da PA-01B:

| ID | Acoplamento | Situacao certificada |
| --- | --- | --- |
| NC-PA01B-01 | `DashboardPage` -> `AnalyticsRepository` | UI instanciava repositorio de Analytics para ler dados historicos. |
| NC-PA01B-02 | `DashboardPage` -> `WaterHealthScoreCalculator` | UI instanciava calculadora analitica para montar serie historica. |
| NC-PA01B-03 | `DashboardPage._water_health_score_series()` | UI filtrava medicoes por timestamp e calculava score progressivo. |
| NC-PA01B-04 | `DashboardPage` -> modelos de Analytics | UI dependia dos objetos retornados pelo repositorio analitico. |

Tambem foram classificados como conformes e preservados:

* uso de `DashboardMonitoringAdapter` para status observacional de qualidade;
* `WaterHealthScoreChart` como componente visual;
* ausencia de formula paralela do Water Health Score dentro do Dashboard.

## 5. Fluxo arquitetural anterior

Antes da implementacao, o fluxo do grafico era:

```text
DashboardPage.refresh()
  -> DashboardPage._water_health_score_series()
     -> AnalyticsRepository.load_quality()
     -> AnalyticsRepository.load_environment()
     -> AnalyticsRepository.load_consumption()
     -> DashboardPage._measurements_until()
     -> WaterHealthScoreCalculator.calculate()
  -> WaterHealthScoreChart.set_points()
```

Componentes envolvidos:

| Componente | Responsabilidade anterior |
| --- | --- |
| `DashboardPage` | Apresentacao, leitura de cards, acesso analitico, recorte temporal e montagem da serie. |
| `AnalyticsRepository` | Leitura dos CSVs e materializacao dos modelos analiticos. |
| `WaterHealthScoreCalculator` | Calculo do score a partir de medicoes historicas. |
| `WaterHealthScoreChart` | Renderizacao dos pontos recebidos. |

Risco anterior: a tela conhecia detalhes de persistencia analitica, modelos temporais e calculadora de score.

## 6. Fluxo arquitetural implementado

Fluxo proposto e implementado nesta GP:

```text
DashboardPage.refresh()
  -> DashboardAnalyticsSnapshotService.water_health_score_series()
     -> AnalyticsRepository.load_quality()
     -> AnalyticsRepository.load_environment()
     -> AnalyticsRepository.load_consumption()
     -> WaterHealthScoreCalculator.calculate()
  -> WaterHealthScoreChart.set_points()
```

O Dashboard passa a consumir somente uma serie temporal pronta para apresentacao. A composicao analitica, o acesso ao repositorio e o recorte por timestamp ficam encapsulados no novo servico de snapshot visual.

## 7. Componentes e arquivos alterados

Arquivos previstos para alteracao antes da implementacao:

| Arquivo | Motivo |
| --- | --- |
| `analytics/dashboard_snapshot.py` | Criar contrato intermediario minimo para dados analiticos do Dashboard. |
| `main.py` | Substituir dependencias diretas por consumo do novo contrato. |
| `tests/test_dashboard_analytics_snapshot.py` | Validar equivalencia, ordenacao, estado vazio e ausencia de dependencias proibidas. |
| `docs/architecture/PE_07_PA01B_DASHBOARD_ANALYTICS_DECOUPLING.md` | Registrar estrategia, implementacao, testes e parecer. |
| `docs/history/HISTORY.md` | Registrar governanca da GP-PE-07. |
| `docs/roadmap/ROADMAP.md` | Registrar GP-PE-07 como concluida. |

## 8. Contrato adotado

Contrato: `DashboardAnalyticsSnapshotService.water_health_score_series()`.

Saida:

```text
[
  {"label": "01/07", "score": 82, "status": "Score analitico bom"}
]
```

Caracteristicas do contrato:

* estrutura pronta para `WaterHealthScoreChart`;
* lista vazia quando ha menos de duas medicoes de qualidade;
* limite de ate 12 pontos finais, preservando o comportamento anterior;
* labels por data no formato `dd/mm` quando timestamp existe;
* labels numericos quando timestamp nao existe;
* nenhum tipo PyQt ou elemento visual na camada analitica.

## 9. Justificativa arquitetural

Foi criado um contrato pequeno em `analytics` porque a responsabilidade deslocada e analitica: ler datasets, filtrar medicoes por tempo e calcular o Water Health Score progressivo. Reutilizar `AnalyticsService.build_snapshot()` nao seria suficiente, pois ele produz apenas o snapshot analitico atual, nao a serie temporal historica exigida pelo grafico.

A solucao preserva:

* formula do Water Health Score;
* repositorios existentes;
* `DashboardMonitoringAdapter`;
* `WaterHealthScoreChart`;
* CSVs e schemas atuais;
* comportamento visual esperado.

## 10. Limites preservados

Nao foram implementados:

* PA-01C;
* PA-01D;
* PA-01E;
* redesenho visual;
* nova funcionalidade analitica;
* alteracao de persistencia;
* alteracao de criterio do score;
* reorganizacao geral do pacote `analytics`;
* alteracao do ICFACTORY;
* implantacao de Discoveries congeladas.

## 11. Testes executados

Foram executados:

```text
python -m unittest tests.test_dashboard_analytics_snapshot
python -m unittest tests.test_water_health_score tests.test_dashboard_monitoring_adapter tests.test_analytics_repository tests.test_analytics_trends
python -m unittest discover -s tests
```

Cobertura objetiva dos testes:

| Verificacao | Evidencia |
| --- | --- |
| Servico responsavel pela serie temporal | `tests/test_dashboard_analytics_snapshot.py`. |
| Calculo e ordenacao da serie | Testes de pontos, labels, recorte temporal e limite de 12 pontos. |
| Ausencia de `DashboardPage` -> `AnalyticsRepository` | Teste estatico sobre `main.py`. |
| Ausencia de `DashboardPage` -> `WaterHealthScoreCalculator` | Teste estatico sobre `main.py`. |
| Contrato consumido pelo `WaterHealthScoreChart` | Pontos com `label`, `score` e `status`. |
| Comportamento com dados presentes | Serie com duas ou mais medicoes gera pontos prontos. |
| Comportamento sem dados suficientes | Serie vazia preservada quando ha menos de duas medicoes de qualidade. |
| Compatibilidade com PA-01A | Status produzido pelo calculador existente e preservado no contrato visual. |

## 12. Resultados

Resultados:

```text
python -m unittest tests.test_dashboard_analytics_snapshot
Ran 5 tests
OK

python -m unittest tests.test_water_health_score tests.test_dashboard_monitoring_adapter tests.test_analytics_repository tests.test_analytics_trends
Ran 10 tests
OK

python -m unittest discover -s tests
Ran 91 tests
OK
```

Resultado arquitetural:

* `DashboardPage` deixou de importar `AnalyticsRepository`.
* `DashboardPage` deixou de importar `WaterHealthScoreCalculator`.
* `DashboardPage` deixou de conter `_water_health_score_series()`.
* `DashboardPage` deixou de conter `_measurements_until()` para composicao analitica temporal.
* A serie historica do Water Health Score passou a ser fornecida por `DashboardAnalyticsSnapshotService`.
* `DashboardMonitoringAdapter` foi preservado.
* `WaterHealthScoreChart` foi preservado.
* A formula do Water Health Score nao foi alterada.
* Persistencia CSV e modelos analiticos existentes nao foram alterados.

## 13. Limitacoes remanescentes

Limitacoes remanescentes:

* A leitura direta de CSVs pelo Dashboard para cards resumidos permanece inalterada, pois a GP-PE-06 classificou esse ponto como aceitavel com ressalva e fora do alvo primario da PA-01B.
* A montagem de `DashboardMonitoringAdapter` dentro da tela permanece preservada, conforme restricao de nao misturar PA-01B com PA-01E ou factory ampla de interfaces.
* O novo contrato cobre somente a serie historica do Water Health Score; nao cria snapshot geral do Dashboard.

## 14. Estrategia de rollback

Rollback simples e reversivel:

1. Restaurar em `DashboardPage` a composicao anterior do grafico.
2. Remover o contrato `DashboardAnalyticsSnapshotService`.
3. Remover os testes especificos do novo contrato.
4. Preservar dados CSV existentes, sem migracao ou alteracao persistida.

## 15. Parecer final

Status: CONCLUIDA.

A GP-PE-07 implementou a PA-01B de forma restrita, pequena, testavel e reversivel. Os tres acoplamentos certificados pela GP-PE-06 foram removidos do `DashboardPage` por meio do contrato `DashboardAnalyticsSnapshotService`, que encapsula acesso ao repositorio, calculo do Water Health Score e composicao temporal da serie.

O Dashboard permanece responsavel por apresentacao, atualizacao visual e interacao. A camada analitica permanece responsavel pela composicao da serie historica. Nao houve alteracao de criterio analitico, persistencia, schema, grafico, adapter conforme, ICFACTORY ou Discoveries congeladas.

Parecer institucional: a PA-01B esta implementada e validada, com regressao completa aprovada.

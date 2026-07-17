# PE-06 - Auditoria Arquitetural da PA-01B

## 1. Objetivo

Executar auditoria arquitetural da frente **PA-01B - Desacoplamento entre Dashboard e Analytics**, identificando de forma rastreavel as dependencias atuais entre `DashboardPage` e os componentes de Analytics.

Esta GP possui carater exclusivamente analitico. Nenhuma alteracao de codigo, refatoracao, adapter, contrato ou implementacao foi realizada.

## 2. Escopo

O escopo desta auditoria foi limitado ao relacionamento entre Dashboard e Analytics:

* dependencias diretas;
* dependencias indiretas;
* responsabilidades atuais;
* contratos utilizados;
* pontos de acoplamento;
* chamadas diretas;
* dependencias historicas;
* oportunidades de isolamento arquitetural.

Ficaram fora do escopo:

* refatoracao;
* alteracao de codigo;
* criacao de adapters;
* mudanca de contratos;
* alteracao em Analytics;
* alteracao no Dashboard;
* alteracao do ICFACTORY;
* implantacao de Discoveries congeladas.

## 3. Metodologia

A auditoria foi conduzida por inspecao passiva:

1. Releitura de `docs/architecture/PE_03_PA01_IMPLEMENTATION_DECOMPOSITION.md` para recuperar o escopo executivo da PA-01B.
2. Releitura de `docs/architecture/PE_02_PA01_ARCHITECTURAL_AUDIT.md` para recuperar NC-01, NC-06 e NC-09.
3. Releitura de `docs/architecture/PE_05_PA01A_IMPLEMENTATION_AUDIT.md` para confirmar que PA-01A foi concluida sem implementar PA-01B.
4. Releitura de `docs/pac/PE_01_IMPLEMENTATION_EXECUTION_STRATEGY.md` e `docs/pac/PAC_14_PROJECT_EVOLUTION_PLAN.md` para preservar a prioridade e os limites da PA-01.
5. Inspecao passiva do codigo atual: `main.py`, `analytics/repositories.py`, `analytics/scoring.py`, `analytics/service.py`, `analytics/models.py`, `monitoramento_hidrico/dashboard_adapter.py` e testes relacionados.
6. Classificacao de cada dependencia como conforme, aceitavel com ressalva ou nao conforme/evolutiva.

Nenhum teste foi executado nesta GP, pois o objetivo e exclusivamente diagnostico.

## 4. Arquitetura observada

### 4.1 Fluxo atual do Dashboard

O `DashboardPage` concentra tres tipos de leitura/apresentacao:

```text
DashboardPage
  -> leitura direta de CSVs para cards resumidos
  -> DashboardMonitoringAdapter para status observacional de qualidade
  -> AnalyticsRepository + WaterHealthScoreCalculator para serie historica do Water Health Score
```

Responsabilidades observadas:

| Componente | Responsabilidade atual |
| --- | --- |
| `DashboardPage` | Apresentar cards resumidos, total de registros e grafico de evolucao do Water Health Score. |
| `WaterHealthScoreChart` | Renderizar pontos ja calculados em grafico de linha. |
| `DashboardMonitoringAdapter` | Traduzir linha CSV de qualidade em status observacional para o Dashboard. |
| `AnalyticsRepository` | Ler CSVs e converter linhas em modelos analiticos. |
| `WaterHealthScoreCalculator` | Calcular Water Health Score a partir de medicoes de qualidade, ambiente e consumo. |
| `AnalyticsService` | Construir snapshot analitico consolidado para consumidores de Analytics. |

### 4.2 Historico arquitetural relevante

Registros historicos indicam:

* GP-A15 removeu avaliacao observacional hardcoded do Dashboard e criou `DashboardMonitoringAdapter`, preservando leitura direta de CSVs temporariamente.
* GP-A25 introduziu o grafico executivo do Water Health Score no Dashboard consumindo `AnalyticsRepository` e `WaterHealthScoreCalculator` diretamente, sem duplicar formula analitica.
* GP-PE-02 classificou esse consumo direto como parcialmente conforme e registrou NC-01.
* GP-PE-03 definiu PA-01B para encapsular a composicao da serie historica fora do Dashboard.
* GP-PE-05 confirmou que PA-01A nao implementou o desacoplamento Dashboard x Analytics.

## 5. Mapeamento das dependencias

### 5.1 Dependencias diretas do Dashboard

| Origem | Destino | Motivo da dependencia | Classificacao | Impacto arquitetural | Risco de alteracao | Recomendacao tecnica |
| --- | --- | --- | --- | --- | --- | --- |
| `DashboardPage` | `DashboardMonitoringAdapter` | Obter status observacional de qualidade sem regra local na tela. | Necessaria/conforme | Preserva limite entre UI e avaliacao observacional. | Baixo | Manter ate PA-01C/PA-01E definirem contrato mais amplo. |
| `DashboardPage` | `PolicyEngine` | Montar `DashboardMonitoringAdapter` dentro da tela. | Evitavel, mas fora do foco primario da PA-01B | UI conhece montagem interna do adapter. | Medio | Tratar futuramente em guardrails/factory de interface, nao misturar com serie analitica. |
| `DashboardPage` | `AvaliacaoObservacionalService` | Montar `DashboardMonitoringAdapter` dentro da tela. | Evitavel, mas ja mapeada em NC-06 | UI conhece motor observacional indiretamente. | Medio | Avaliar em PA-01E ou GP propria de factory/facade. |
| `DashboardPage` | `AnalyticsRepository` | Ler historico de qualidade, ambiente e consumo para montar serie do Water Health Score. | Evitavel/nao conforme para PA-01B | UI passa a conhecer fonte analitica e modelos de dados. | Medio-Alto | Encapsular em service/facade de snapshot visual do Dashboard. |
| `DashboardPage` | `WaterHealthScoreCalculator` | Calcular score progressivo por ponto da serie historica. | Evitavel/nao conforme para PA-01B | UI compoe logica analitica temporal. | Medio-Alto | Mover composicao para contrato intermediario sem alterar formula. |
| `DashboardPage` | CSVs locais via `_read_csv()` | Exibir cards de ultimas medicoes e totais. | Aceitavel com ressalva | Persistencia distribuida permanece no Dashboard. | Medio | Manter fora da PA-01B se a frente focar Water Health Score; mapear para PA-03/PA-01E futura. |
| `WaterHealthScoreChart` | Pontos fornecidos por `DashboardPage` | Renderizar serie ja calculada. | Necessaria/conforme | Componente visual nao calcula score. | Baixo | Manter como componente puramente visual. |

### 5.2 Dependencias indiretas

| Origem | Destino indireto | Caminho | Classificacao | Impacto | Recomendacao |
| --- | --- | --- | --- | --- | --- |
| `DashboardPage` | `AnalyticsHydricMonitoringAdapter` | `WaterHealthScoreCalculator` instancia adapter padrao. | Evitavel por composicao analitica na UI | Dashboard aciona cadeia analitica que chama nucleo hidrico. | Encapsular score historico em Analytics/facade. |
| `DashboardPage` | `PolicyEngine` e `AvaliacaoObservacionalService` via score | `WaterHealthScoreCalculator` -> `AnalyticsHydricMonitoringAdapter` -> nucleo hidrico. | Evitavel no contexto da serie historica | A tela dispara avaliacao observacional indiretamente para score. | Future facade deve assumir essa composicao. |
| `DashboardPage` | Modelos `QualityMeasurement`, `EnvironmentMeasurement`, `ConsumptionMeasurement` | `AnalyticsRepository.load_*()` retorna modelos analiticos usados no loop de serie. | Evitavel | UI passa a depender do formato temporal dos modelos de Analytics. | Retornar DTO visual simples para o grafico. |
| `DashboardPage` | `WaterHealthScore.status` | Pontos incluem `status`, embora grafico use principalmente `score`. | Baixo/evitavel | Campo extra carrega semantica analitica para UI. | Contrato visual deve declarar apenas campos necessarios. |

### 5.3 Chamadas diretas relevantes

| Metodo | Chamada | Leitura arquitetural |
| --- | --- | --- |
| `DashboardPage.__init__()` | `self.analytics_repository = AnalyticsRepository()` | Instanciacao direta de repositorio analitico na UI. |
| `DashboardPage.__init__()` | `self.score_calculator = WaterHealthScoreCalculator()` | Instanciacao direta de calculadora analitica na UI. |
| `DashboardPage.refresh()` | `self.score_chart.set_points(self._water_health_score_series())` | Tela aciona composicao da serie analitica. |
| `DashboardPage._water_health_score_series()` | `load_quality()`, `load_environment()`, `load_consumption()` | UI le datasets analiticos completos. |
| `DashboardPage._water_health_score_series()` | `score_calculator.calculate(...)` | UI calcula score progressivo ponto a ponto. |
| `DashboardPage._measurements_until()` | Filtra medicoes por timestamp | UI contem regra de composicao temporal da serie. |

## 6. Dependencias conformes

Foram consideradas conformes:

| Relacionamento | Justificativa |
| --- | --- |
| `DashboardPage` -> `DashboardMonitoringAdapter` para status de qualidade | Preserva remocao de avaliacao local da tela e delega ao adapter. |
| `WaterHealthScoreChart` recebendo `points` prontos | Componente visual apenas renderiza dados ja preparados. |
| `DashboardPage._quality_status()` delegando ao adapter | Tela nao recalcula status observacional. |
| `AnalyticsService` compondo snapshot analitico | Responsabilidade propria de Analytics, ja existente e separada do Dashboard. |
| `WaterHealthScoreCalculator` usando adapter hidrico interno | Responsabilidade analitica legitima, desde que nao seja chamado diretamente pela UI para montar serie. |

Essas dependencias nao exigem intervencao direta na futura PA-01B, salvo se um desenho de facade optar por reorganizar montagem de dependencias sem alterar comportamento.

## 7. Dependencias nao conformes

Foram consideradas nao conformes/evolutivas para PA-01B:

| ID | Origem | Destino | Situacao atual | Impacto arquitetural | Risco | Recomendacao |
| --- | --- | --- | --- | --- | --- | --- |
| NC-PA01B-01 | `DashboardPage` | `AnalyticsRepository` | UI instancia repositorio de Analytics para ler dados historicos. | Mistura apresentacao com acesso a dados analiticos. | Medio-Alto | Criar contrato de snapshot visual para Dashboard. |
| NC-PA01B-02 | `DashboardPage` | `WaterHealthScoreCalculator` | UI instancia calculadora para montar serie historica. | Mistura apresentacao com composicao analitica. | Medio-Alto | Encapsular calculo historico fora da UI. |
| NC-PA01B-03 | `DashboardPage._water_health_score_series()` | Logica temporal de serie | UI filtra medicoes por timestamp e calcula score progressivo. | Regra de composicao analitica temporal vive na tela. | Medio | Mover para service/facade com teste de equivalencia. |
| NC-PA01B-04 | `DashboardPage` | Modelos de Analytics | UI depende de objetos retornados por `AnalyticsRepository`. | Mudancas em modelos analiticos podem quebrar Dashboard. | Medio | Expor DTO visual simples: `label`, `score`, opcionalmente `status`. |

Nao foi identificada duplicacao da formula do Water Health Score dentro do Dashboard. A nao conformidade esta na composicao e orquestracao direta, nao na existencia de uma formula paralela.

## 8. Impacto arquitetural

### 8.1 Impacto atual

O impacto atual e classificado como **medio-alto**:

* o Dashboard continua sendo camada de apresentacao;
* porem, para o grafico do Water Health Score, ele tambem executa composicao analitica;
* a UI conhece `AnalyticsRepository`, `WaterHealthScoreCalculator`, modelos temporais e regra de recorte por timestamp;
* isso aumenta a chance de uma mudanca futura em Analytics exigir mudanca direta no Dashboard;
* tambem dificulta testar o contrato visual do Dashboard de modo isolado.

### 8.2 Risco de alteracao

O risco de alterar essa area em futura PA-01B e **medio**:

* a serie historica precisa permanecer numericamente equivalente;
* a formula do score nao pode mudar;
* os dados historicos e schemas CSV nao podem mudar;
* o estado vazio do grafico deve permanecer;
* o resultado visual esperado deve ser preservado.

### 8.3 Limites preservados atualmente

Mesmo com acoplamento, foram observados limites preservados:

* o Dashboard nao contem pesos do Water Health Score;
* o Dashboard nao contem limites observacionais;
* o Dashboard nao calcula status observacional de qualidade;
* o grafico nao calcula score;
* o Dashboard nao acessa `AnalyticsService.build_snapshot()` para reclassificar sinais executivos.

### 8.4 Relacao com PA-01A

A PA-01A estabilizou a linguagem do score e dos status, mas nao removeu o acoplamento tecnico. Portanto, PA-01B permanece necessaria e deve ser tratada como frente propria.

## 9. Recomendacoes para implementacao da PA-01B

Recomendacoes tecnicas para GP futura:

1. Criar contrato intermediario para o Dashboard, por exemplo `DashboardAnalyticsSnapshotService`, `DashboardSummaryService` ou facade equivalente.
2. Mover `_water_health_score_series()` para fora de `DashboardPage`.
3. Fazer o Dashboard consumir apenas uma lista de pontos visuais, por exemplo:

```text
[
  {"label": "01/07", "score": 82, "status": "Score analitico bom"}
]
```

4. Manter `WaterHealthScoreChart` como componente visual sem regra analitica.
5. Preservar `DashboardMonitoringAdapter` para status observacional de qualidade, sem misturar PA-01B com PA-01C.
6. Nao alterar `WaterHealthScoreCalculator`, `AnalyticsRepository`, CSVs, modelos ou formula de score nesta frente, salvo ajuste minimo de chamada exigido pelo novo contrato.
7. Adicionar teste de equivalencia entre a serie atual e a serie produzida pelo novo contrato.
8. Adicionar teste ou inspecao de dependencia garantindo que `DashboardPage` nao instancie `AnalyticsRepository` nem `WaterHealthScoreCalculator`.
9. Manter rollback simples: restaurar composicao anterior no Dashboard caso o contrato intermediario apresente regressao.
10. Deixar persistencia CSV direta dos cards fora da PA-01B, exceto se houver GP propria de persistencia ou guardrail.

## 10. Parecer Final

Status: CONCLUIDA.

A auditoria confirma que o relacionamento entre Dashboard e Analytics possui dependencias aceitaveis e dependencias evolutivas.

Sao adequadas as dependencias em que o Dashboard delega status de qualidade ao `DashboardMonitoringAdapter` e em que o `WaterHealthScoreChart` apenas renderiza pontos ja preparados.

Representam divida arquitetural da PA-01B as dependencias diretas de `DashboardPage` para `AnalyticsRepository` e `WaterHealthScoreCalculator`, bem como a composicao temporal da serie historica dentro da UI. Essas dependencias nao duplicam a formula analitica, mas colocam orquestracao analitica em camada de apresentacao.

Parecer institucional: a futura implementacao da PA-01B deve encapsular a serie historica do Water Health Score em contrato intermediario, preservando comportamento, formula, dados, schemas e resultado visual. Nenhuma alteracao foi realizada nesta GP.

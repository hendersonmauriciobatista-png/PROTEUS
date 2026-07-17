# PE-09 - Auditoria Arquitetural da PA-01C

## 1. Identificacao

Programa: **Plano Oficial de Evolucao do PROTEUS**.

Iniciativa: **PA-01 - Governanca de Limites, Responsabilidades e Comunicacao Segura**.

Frente auditada: **PA-01C - Centralizacao de listas**.

Natureza: auditoria arquitetural pre-implementacao, exclusivamente analitica.

Status da GP: **CONCLUIDA**.

Parecer final permitido aplicado: **PA-01C APTA PARA IMPLEMENTACAO COM RESSALVAS**.

## 2. Objetivo

Auditar listas, colecoes, conjuntos de opcoes, vocabularios e mapeamentos estaticos ou semiestaticos do PROTEUS, identificando duplicidades, fontes de autoridade, riscos de divergencia e limites para uma futura implementacao restrita da PA-01C.

## 3. Escopo

O escopo inclui:

* parametros de qualidade da agua;
* categorias, perfis e parametros do monitoramento hidrico;
* status e severidades;
* opcoes de projeto de monitoramento;
* schemas CSV e cabecalhos de interface;
* metricas de Analytics;
* estados de governanca;
* prioridades e acoes executivas;
* listas reproduzidas em testes.

Ficam fora do escopo:

* alteracao de codigo;
* criacao de modulo de constantes;
* criacao de enum;
* alteracao de formularios;
* alteracao de persistencia;
* alteracao de modelos;
* alteracao de testes;
* implementacao da PA-01D ou PA-01E;
* alteracao do ICFACTORY;
* implantacao de Discoveries congeladas.

## 4. Base documental

Foram utilizados:

* `docs/architecture/PE_02_PA01_ARCHITECTURAL_AUDIT.md`;
* `docs/architecture/PE_03_PA01_IMPLEMENTATION_DECOMPOSITION.md`;
* `docs/architecture/PE_05_PA01A_IMPLEMENTATION_AUDIT.md`;
* `docs/architecture/PE_06_PA01B_ARCHITECTURAL_AUDIT.md`;
* `docs/architecture/PE_07_PA01B_DASHBOARD_ANALYTICS_DECOUPLING.md`;
* `docs/architecture/PE_08_PA01B_POST_IMPLEMENTATION_AUDIT.md`;
* `docs/pac/PE_01_IMPLEMENTATION_EXECUTION_STRATEGY.md`;
* `docs/pac/PAC_14_PROJECT_EVOLUTION_PLAN.md`;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`;
* codigo atual do PROTEUS;
* testes existentes;
* catalogos e configuracoes operacionais;
* `monitoramento_hidrico/status_semantics.py`;
* modelos de dominio e componentes de interface.

## 5. Metodologia

A auditoria combinou:

1. busca textual por `QComboBox`, `addItem`, `CSV_FIELDS`, `setHorizontalHeaderLabels`, `STATUS`, `FIELDS`, `PARAMETERS`, `TOLERANCES`, `RISK_TRENDS`, `ACTIVE_STATES`, `VALID_TRANSITIONS` e estruturas literais;
2. inspecao semantica de adapters, catalogos, configuracoes, modelos e telas;
3. comparacao entre modulos que usam parametros de qualidade;
4. comparacao entre codigo e testes;
5. classificacao das listas por tipo arquitetural;
6. determinacao da fonte de autoridade recomendada;
7. delimitacao da futura implementacao.

Nenhum teste foi executado, pois esta GP e uma auditoria pre-implementacao sem alteracao funcional.

## 6. Inventario de listas

Total de listas relevantes inventariadas: **28**.

| ID | Arquivo | Componente | Conteudo ou finalidade | Tipo de lista | Origem atual |
| --- | --- | --- | --- | --- | --- |
| L-01 | `monitoramento_hidrico/qualidade_agua_adapter.py` | `PARAMETROS_QUALIDADE_AGUA` | Campos de qualidade -> parametro -> categoria. | dominio | Adapter de Qualidade da Agua |
| L-02 | `monitoramento_hidrico/dashboard_adapter.py` | `QUALITY_PARAMETER_FIELDS` | Campos de qualidade -> parametro -> categoria. | dominio | Adapter do Dashboard |
| L-03 | `monitoramento_hidrico/operational_reports_adapter.py` | `REPORT_QUALITY_PARAMETERS` | Campos de qualidade -> parametro -> categoria. | dominio | Adapter de Relatorios |
| L-04 | `monitoramento_hidrico/analytics_adapter.py` | `QUALITY_ANALYTICS_PARAMETERS` | Campos de qualidade -> parametro -> categoria -> label. | dominio | Adapter de Analytics |
| L-05 | `monitoramento_hidrico/governance_adapter.py` | `GOVERNANCE_QUALITY_PARAMETERS` | Metrica de alerta -> parametro -> categoria. | dominio | Adapter de Governanca |
| L-06 | `data/monitoramento_hidrico_catalogo.json` | `perfis_operacionais` | Perfis operacionais do catalogo hidrico. | catalogo | Catalogo JSON |
| L-07 | `data/monitoramento_hidrico_catalogo.json` | `categorias_parametros` | Categorias oficiais de parametros hidricos. | catalogo | Catalogo JSON |
| L-08 | `data/monitoramento_hidrico_catalogo.json` | `parametros_hidricos` | Parametros hidricos, unidades, categorias e limites observacionais. | catalogo | Catalogo JSON |
| L-09 | `data/monitoramento_hidrico_configuracoes.json` | `categorias_habilitadas` | Categorias habilitadas por configuracao operacional. | configuracao | Configuracao JSON |
| L-10 | `data/monitoramento_hidrico_configuracoes.json` | `parametros_habilitados` | Parametros habilitados por configuracao operacional. | configuracao | Configuracao JSON |
| L-11 | `monitoramento_hidrico/status_semantics.py` | `STATUS_SEMANTICS` | Fonte oficial de rotulos comunicacionais da PA-01A. | dominio | Fonte oficial PA-01A |
| L-12 | `monitoramento_hidrico/status_semantics.py` | `OBSERVATIONAL_ENGINE_STATUS_LABELS` | Traducao dos codigos tecnicos do motor observacional. | dominio | Fonte oficial PA-01A |
| L-13 | `monitoramento_hidrico/avaliacao.py` | `STATUS_*` e `SEVERIDADE_*` | Codigos tecnicos internos de avaliacao observacional. | tecnica | Motor observacional |
| L-14 | `monitoramento_hidrico/politicas.py` | `TIPO_*`, `MOTOR_OBSERVACIONAL` | Tipos e motor de politica. | tecnica | Policy Engine |
| L-15 | `qualidade_agua.py` | `CSV_FIELDS` | Schema CSV de qualidade da agua. | persistencia | Tela de coleta/persistencia |
| L-16 | `dados_ambientais.py` | `CSV_FIELDS` | Schema CSV de dados ambientais. | persistencia | Tela de coleta/persistencia |
| L-17 | `consumo_distribuicao.py` | `CSV_FIELDS` | Schema CSV de consumo e distribuicao. | persistencia | Tela de coleta/persistencia |
| L-18 | `analytics/trends.py` | `QUALITY_TOLERANCES` | Tolerancias de tendencias de qualidade. | tecnica | Camada analitica |
| L-19 | `analytics/trends.py` | `CONSUMPTION_TOLERANCES` | Tolerancias de tendencias de consumo. | tecnica | Camada analitica |
| L-20 | `analytics/trends.py` | `metrics` locais | Metricas e labels para tendencias de qualidade e consumo. | tecnica | Camada analitica |
| L-21 | `analytics/alerts.py` | `risk_directions` local | Direcoes de risco para alertas de tendencias de qualidade. | tecnica | Camada analitica |
| L-22 | `governance/models.py` | `EventState` | Estados oficiais de eventos operacionais. | dominio | Modelo de governanca |
| L-23 | `governance/rules.py` | `ACTIVE_STATES`, `VALID_TRANSITIONS` | Estados ativos e transicoes permitidas. | dominio | Regras de governanca |
| L-24 | `executive/rules.py` | `ACTIVE_EVENT_STATES`, `RISK_TRENDS`, `SEVERITY_ORDER` | Filtros e ordenacao executiva. | tecnica | Regras executivas |
| L-25 | `executive_recommendation/models.py` | `RecommendationPriority`, `RecommendationAction` | Prioridades e acoes de recomendacao executiva. | dominio | Modelo de recomendacao |
| L-26 | `monitoramento_hidrico/projeto_monitoramento.py` | `CONTEXTOS_OPERACIONAIS`, `PERFIS_OPERACIONAIS`, `PONTOS_PRINCIPAIS_COLETA`, `STATUS_PROJETO` | Opcoes e estados do projeto de monitoramento. | dominio | Modelo de projeto |
| L-27 | `projeto_monitoramento_page.py` | Combos de contexto e ponto de coleta | Itens de UI consumindo listas do modelo de projeto. | interface | Modelo de projeto |
| L-28 | Paginas PyQt e testes | Cabecalhos de tabelas, cards, fixtures e asserts literais | Rotulos visuais e fixtures. | interface/teste | Componentes locais ou testes |

## 7. Matriz de duplicidades

Duplicidades reais encontradas: **8**.

| ID | Valores repetidos | Arquivos envolvidos | Divergencia existente | Risco | Recomendacao |
| --- | --- | --- | --- | --- | --- |
| D-01 | `ph`, `turbidez`, `oxigenio_dissolvido`, `temperatura`, `agrotoxicos` com parametro/categoria | Cinco adapters hidricos: qualidade, dashboard, relatorios, analytics e governanca | Analytics acrescenta label; Governanca usa dicionario e omite label; demais usam listas identicas. | Alto | Centralizacao obrigatoria em contrato especifico de mapeamento de parametros de qualidade. |
| D-02 | Labels de qualidade: `pH`, `Turbidez`, `Oxigenio dissolvido`, `Temperatura da agua`, `Agrotoxicos` | `analytics_adapter.py`, `analytics/trends.py`, interfaces e relatorios | Grafias e acentos variam; algumas superficies usam labels abreviados como `OD`. | Medio | Centralizacao recomendada apenas se o contrato de parametros incluir label comunicacional por contexto. |
| D-03 | Status observacional normal/atencao como aliases por adapter | `qualidade_agua_adapter.py`, `dashboard_adapter.py`, `operational_reports_adapter.py` | Nomes locais diferentes apontam para os mesmos valores oficiais. | Baixo | Manter aliases toleraveis ou padronizar em futura GP sem alterar semantica. |
| D-04 | Codigos `ATENCAO`, `CRITICO`, `NAO_AVALIAVEL` usados em adapters e testes | Adapters, `avaliacao.py`, testes | Uso de codigos tecnicos internos misturado a testes de comportamento. | Baixo | Manter em `avaliacao.py`; nao centralizar em PA-01C alem da fonte tecnica atual. |
| D-05 | Metricas de qualidade repetidas entre CSV, Analytics e adapters | `qualidade_agua.py`, `analytics/repositories.py`, `analytics/trends.py`, adapters | Campo `temperatura` mapeia para parametro `temperatura_agua`; risco de confusao com `temperatura_ambiente`. | Medio | Tratar junto de D-01; preservar schema CSV. |
| D-06 | Estados de governanca repetidos como valores e filtros | `governance/models.py`, `governance/rules.py`, `governanca_operacional.py`, `executive/rules.py` | Valores replicados em regras executivas como strings. | Medio | Centralizacao recomendada usando `EventState` como autoridade; nao misturar com PA-01C de parametros se escopo ficar pequeno. |
| D-07 | Contextos/perfis de projeto e catalogo hidrico parcialmente sobrepostos | `projeto_monitoramento.py`, `data/monitoramento_hidrico_catalogo.json` | Projeto usa `urbana`/`agricola`; catalogo usa `urbano_saneamento`/`rural`; mapeamento e explicito. | Medio | Nao centralizar diretamente; manter mapeamento como contrato de traducao de contexto para perfil. |
| D-08 | Categorias e parametros do catalogo reproduzidos em testes | `data/monitoramento_hidrico_catalogo.json`, `tests/test_monitoramento_hidrico_catalog.py` | Teste lista nomes esperados manualmente. | Baixo | Duplicacao intencional de teste; manter para validar conteudo externo do catalogo. |

## 8. Fontes de autoridade

| Lista | Existe fonte oficial? | Fonte correta | Utilizada? | Copias paralelas? | Centralizar? |
| --- | --- | --- | --- | --- | --- |
| Parametros hidricos completos | Sim | `data/monitoramento_hidrico_catalogo.json` via `catalog.py` | Sim pelo motor e configuracoes | Parcialmente em adapters | Nao mover catalogo; criar contrato de mapeamento quando necessario. |
| Mapeamento campo CSV/modelo -> parametro/categoria | Nao como fonte unica | Novo contrato especifico em `monitoramento_hidrico`, derivado do catalogo quando aplicavel | Nao | Sim, cinco copias | Sim, obrigatorio. |
| Vocabulario de status comunicacional | Sim | `status_semantics.py` | Sim | Aliases locais toleraveis | Nao alterar semantica; apenas preservar. |
| Codigos tecnicos de avaliacao | Sim | `avaliacao.py` | Sim | Usos por adapters/testes | Permanecer tecnico. |
| Perfis/categorias/configuracoes | Sim | Catalogo/configuracao JSON | Sim | Testes e docs | Nao transformar em constante. |
| Estados de eventos | Sim | `governance.models.EventState` | Parcialmente | Strings em `executive/rules.py` | Recomendado em GP futura se escopo permitir. |
| Contextos e pontos de projeto | Sim | `projeto_monitoramento.py` | Sim pela UI | Testes | Permanecer no modelo de projeto. |
| Schemas CSV | Parcial | `CSV_FIELDS` por tela produtora | Sim | Repositorios consomem campos implicitamente | Manter; PA-01C nao deve migrar persistencia. |
| Headers e cards de UI | Sim local | Componente de interface | Sim | Nao relevante | Permanecer local. |

## 9. Listas candidatas a centralizacao

Centralizacao obrigatoria: **1**.

| ID | Lista | Categoria | Justificativa | Fonte recomendada |
| --- | --- | --- | --- | --- |
| C-OBR-01 | Mapeamento de parametros de qualidade usado por adapters | D-01 - obrigatoria | Influencia avaliacao, comunicacao e enriquecimento em cinco consumidores; divergencia pode alterar comportamento. | Contrato especifico no pacote `monitoramento_hidrico`, referenciando codigos do catalogo. |

Centralizacao recomendada: **3**.

| ID | Lista | Categoria | Justificativa | Fonte recomendada |
| --- | --- | --- | --- | --- |
| C-REC-01 | Labels comunicacionais dos parametros de qualidade | D-02 - recomendada | Reduz divergencia visual entre Analytics, relatorios e interfaces. | Mesmo contrato de parametros, com cuidado para labels por contexto. |
| C-REC-02 | Estados ativos e transicoes consumidos por Executive | D-06 - recomendada | `executive/rules.py` reproduz estados de governanca como strings. | `governance.models.EventState` e/ou contrato de consulta da Governanca. |
| C-REC-03 | Tolerancias e metricas analiticas de qualidade/consumo | L-18, L-19, L-20 - recomendada | Reduz duplicidade local entre dicionarios e listas `metrics` dentro de Analytics. | Modulo interno de Analytics, nao contrato global. |

## 10. Listas que devem permanecer locais

Listas que devem permanecer locais ou em sua fonte atual: **12**.

| ID | Lista | Motivo |
| --- | --- | --- |
| LOC-01 | `perfis_operacionais` do catalogo JSON | Configuracao/catalogo externo; nao converter em constante. |
| LOC-02 | `categorias_parametros` do catalogo JSON | Fonte oficial ja existente. |
| LOC-03 | `parametros_hidricos` do catalogo JSON | Fonte oficial ja existente. |
| LOC-04 | `categorias_habilitadas` e `parametros_habilitados` das configuracoes | Configuracao operacional por instancia. |
| LOC-05 | `STATUS_SEMANTICS` | Fonte PA-01A ja certificada; nao alterar na PA-01C. |
| LOC-06 | `OBSERVATIONAL_ENGINE_STATUS_LABELS` | Traducao semantica oficial da PA-01A. |
| LOC-07 | `STATUS_*` e `SEVERIDADE_*` tecnicos de `avaliacao.py` | Codigos internos do motor. |
| LOC-08 | `CSV_FIELDS` de qualidade, ambiente e consumo | Schemas de persistencia; centralizacao exigiria GP propria de persistencia. |
| LOC-09 | Cabecalhos de tabelas e cards das telas | Rotulos estritamente visuais. |
| LOC-10 | Combos de `ProjetoMonitoramentoPage` | Ja consomem o modelo de projeto. |
| LOC-11 | Expectativas manuais de catalogo nos testes | Fixture intencional para validar conteudo externo. |
| LOC-12 | Enums de recomendacao executiva | Modelo proprio da camada de recomendacao. |

## 11. Relacao com a PA-01A

`status_semantics.py` esta sendo respeitado como fonte oficial de vocabulario comunicacional.

Classificacao:

| Caso | Avaliacao |
| --- | --- |
| Aliases de status em adapters (`STATUS_QUALIDADE_*`, `DASHBOARD_STATUS_*`, `REPORT_STATUS_*`) | Copia toleravel: apontam para constantes oficiais e preservam linguagem local do consumidor. |
| `tests/test_status_semantics.py` reproduz lista de labels esperados | Uso conforme: valida a fonte oficial, nao cria vocabulário de runtime. |
| Codigos `NORMAL`, `ATENCAO`, `CRITICO`, `NAO_AVALIAVEL` | Uso conforme como codigos tecnicos internos do motor, traduzidos antes da comunicacao. |
| Relatorio persistido antigo com termo pre-PA-01A | Ressalva historica ja registrada na PE-08; nao e lista ativa da PA-01C. |

A futura PA-01C nao deve alterar significados, labels oficiais, codigos internos ou disclaimers certificados pela PA-01A.

## 12. Relacao com catalogos e configuracoes

O catalogo hidrico e a configuracao operacional ja exercem autoridade sobre:

* perfis operacionais;
* categorias de parametros;
* parametros hidricos;
* unidades;
* aplicabilidade por perfil;
* limites observacionais;
* configuracoes habilitadas por cenario.

Achado central: os adapters nao duplicam o catalogo inteiro, mas duplicam o **mapeamento operacional entre campo de entrada e parametro do catalogo**. Esse mapeamento nao existe hoje como contrato unico.

Recomendacao: a GP-PE-10 nao deve criar um arquivo generico de constantes; deve criar ou consolidar uma fonte especifica para o mapeamento de qualidade usado por adapters, preservando o catalogo JSON como autoridade de parametros.

## 13. Analise da interface

| Interface | Listas observadas | Avaliacao |
| --- | --- | --- |
| `QualidadeAguaPage` | `CSV_FIELDS`, inputs de qualidade, defaults, headers da tabela | Campos persistidos e UI local; nao centralizar indiscriminadamente. |
| `DashboardPage` | cards, navegacao, `WaterHealthScoreChart` | Listas visuais; fora da PA-01C. |
| `RelatoriosPage` | linhas de relatorio e medias de qualidade | Relatorio consome adapter; listas textuais locais. |
| `ProjetoMonitoramentoPage` | combos de contexto e ponto de coleta | Conforme: consome listas do modelo de projeto. |
| `GovernancaOperacionalPage` | cards por `EventState`, headers, cores | Usa enum para estados; cores e headers devem ficar locais. |
| `PrevisaoAnaliticaPage` e `PainelExecutivoPage` | headers de tabelas | Rotulos visuais; permanecer locais. |
| `DadosAmbientaisPage` e `ConsumoDistribuicaoPage` | campos CSV, inputs, headers | Persistencia/interface; fora da PA-01C salvo GP de schemas. |

## 14. Analise dos testes

| Teste | Lista reproduzida | Avaliacao |
| --- | --- | --- |
| `test_monitoramento_hidrico_catalog.py` | Perfis e categorias do catalogo | Duplicacao intencional para validar conteudo externo; manter. |
| `test_status_semantics.py` | Labels oficiais e termos proibidos | Uso conforme da PA-01A; manter. |
| `test_monitoramento_projeto.py` | Status e perfis do projeto | Testa contrato do dominio; manter. |
| `test_qualidade_agua_monitoring_adapter.py`, `test_dashboard_monitoring_adapter.py`, `test_operational_reports_adapter.py` | Valores de medicao para os cinco parametros de qualidade | Fixtures locais legitimas; apos centralizacao, adicionar teste de paridade do contrato compartilhado. |
| `test_analytics_trends.py`, `test_water_health_score.py` | Metricas e status analiticos | Testes de comportamento; nao importar cegamente listas de producao se isso reduzir capacidade de detectar regressao. |

## 15. Risco de centralizacao excessiva

Riscos identificados:

* criar um modulo generico de constantes que misture dominio, interface, persistencia e testes;
* transformar configuracoes JSON em codigo estatico;
* congelar dados persistidos por meio de listas globais;
* acoplar telas a catalogos profundos sem contrato de apresentacao;
* misturar labels visuais de tabela com valores de dominio;
* alterar schemas CSV sob pretexto de centralizacao;
* centralizar fixtures de teste e reduzir capacidade de detectar divergencia;
* usar PA-01C para antecipar PA-01E ou refatorar montagem de adapters.

Mitigacao: centralizar apenas mapeamentos certificados, com fonte especifica e testes de paridade.

## 16. Mapa arquitetural

### 16.1 Mapeamento de parametros de qualidade

```text
Origem atual:
  cinco adapters com listas/dicionario locais

Origem recomendada:
  contrato especifico de parametros de qualidade em monitoramento_hidrico
        ->
  adapters de Qualidade, Dashboard, Relatorios, Analytics e Governanca
```

Consumidores atuais: `QualidadeAguaMonitoringAdapter`, `DashboardMonitoringAdapter`, `OperationalReportsHydricMonitoringAdapter`, `AnalyticsHydricMonitoringAdapter`, `OperationalGovernanceHydricMonitoringAdapter`.

Consumidores futuros: testes de paridade de adapters e possivelmente docs de PA-01C.

Impacto de migracao: medio; deve preservar ordem, campos CSV/modelos, categorias e labels.

Risco de rollback: baixo/medio; restaurar listas locais anteriores.

### 16.2 Estados de governanca para Executive

```text
EventState
        ->
OperationalGovernanceRules
        ->
ExecutiveRules como consumidor de estados ativos
```

Impacto de migracao: baixo; recomendada apenas se a GP-PE-10 puder manter escopo pequeno.

### 16.3 Catalogo e configuracoes

```text
data/monitoramento_hidrico_catalogo.json
        ->
catalog.py / configuracoes.py
        ->
motor observacional e validacoes
```

Impacto de migracao: nao recomendado nesta frente; ja possui autoridade propria.

## 17. Delimitacao da futura implementacao

### Dentro do escopo provavel da GP-PE-10

* criar ou consolidar fonte especifica para mapeamento de parametros de qualidade usado por adapters;
* substituir listas locais duplicadas nos cinco adapters;
* preservar nomes de campos persistidos e atributos de modelos;
* preservar labels e ordem atuais ou documentar alias sem mudanca funcional;
* adicionar testes de paridade do contrato compartilhado;
* atualizar documentacao e governanca.

### Fora do escopo da GP-PE-10

* alterar catalogo JSON de parametros;
* alterar configuracoes operacionais;
* alterar schemas CSV;
* renomear campos persistidos;
* alterar limites observacionais;
* alterar status da PA-01A;
* alterar formula ou metricas do Water Health Score;
* redesenhar interface;
* implementar PA-01D ou PA-01E;
* criar modulo global de constantes;
* implantar Discoveries congeladas.

## 18. Achados

Quantidade de achados: **9**.

| ID | Titulo | Descricao | Evidencia | Tipo da lista | Fonte atual | Fonte recomendada | Impacto | Risco | Severidade | Recomendacao | Bloqueante |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PE09-A01 | Duplicidade central dos parametros de qualidade | Cinco adapters mantem mapeamentos equivalentes. | L-01 a L-05. | dominio | Adapters | Contrato especifico em `monitoramento_hidrico` | Alto | Medio | ALTA | Centralizacao obrigatoria na GP-PE-10. | Nao |
| PE09-A02 | Divergencia estrutural do mesmo mapeamento | Listas usam tuplas; Governanca usa dicionario; Analytics inclui label. | `analytics_adapter.py`, `governance_adapter.py`. | dominio | Adapters | Contrato com views por consumidor ou campos opcionais | Medio | Medio | MEDIA | Preservar formatos publicos dos adapters, mas consumir mesma fonte. | Nao |
| PE09-A03 | Campo `temperatura` representa `temperatura_agua` | CSV/modelo usa `temperatura`; catalogo usa `temperatura_agua`. | Adapters e `qualidade_agua.py`. | dominio/persistencia | Schema CSV + catalogo | Mapeamento explicito | Medio | Medio | MEDIA | Nao renomear schema; documentar no contrato. | Nao |
| PE09-A04 | Catalogo ja e autoridade para parametros | Catalogo JSON contem parametros, categorias, unidades e limites. | `data/monitoramento_hidrico_catalogo.json`. | catalogo | Catalogo | Manter | Alto | Alto se centralizado errado | OBSERVACIONAL | Nao substituir catalogo por constantes. | Nao |
| PE09-A05 | Status PA-01A preservados | Aliases locais importam constantes oficiais. | `status_semantics.py` e adapters. | dominio | PA-01A | Manter | Medio | Baixo | OBSERVACIONAL | Nao alterar semantica na PA-01C. | Nao |
| PE09-A06 | Estados de governanca parcialmente replicados | Executive usa strings para estados ativos. | `governance/models.py`, `executive/rules.py`. | dominio/tecnica | `EventState` | Reuso de `EventState` ou contrato de governanca | Medio | Baixo | BAIXA | Centralizacao recomendada, secundaria. | Nao |
| PE09-A07 | Contextos de projeto e perfis de catalogo sao distintos | Projeto traduz `urbana/agricola` para perfis. | `projeto_monitoramento.py`, catalogo JSON. | dominio | Modelo de projeto | Manter traducao local | Medio | Medio | OBSERVACIONAL | Nao fundir listas sem GP de dominio. | Nao |
| PE09-A08 | Headers e cards sao listas visuais | Varios `setHorizontalHeaderLabels` e cards. | Telas PyQt. | interface | Componentes | Local | Baixo | Baixo | OBSERVACIONAL | Nao centralizar. | Nao |
| PE09-A09 | Testes reproduzem listas oficiais intencionalmente | Testes de catalogo e status mantem valores esperados. | `tests/test_monitoramento_hidrico_catalog.py`, `tests/test_status_semantics.py`. | teste | Testes | Manter ou adicionar testes de paridade | Medio | Baixo | BAIXA | Nao substituir toda fixture por import da producao. | Nao |

## 19. Nao conformidades

Nao conformidades arquiteturais/evolutivas: **4**.

| ID | Situacao | Impacto | Recomendacao |
| --- | --- | --- | --- |
| NC-PA01C-01 | Mapeamento de parametros de qualidade duplicado em cinco adapters. | Risco de divergencia funcional e semantica. | Centralizar em contrato especifico. |
| NC-PA01C-02 | Labels e nomes de metricas de qualidade variam por camada. | Risco de comunicacao divergente. | Tratar como parte opcional do contrato, preservando contexto. |
| NC-PA01C-03 | `EventState` e estados ativos sao replicados como strings em camada executiva. | Risco pequeno de divergencia futura. | Reutilizar fonte de governanca em GP futura, se couber no escopo. |
| NC-PA01C-04 | Tolerancias e metricas de Analytics estao separadas em dicionarios e listas locais. | Risco de manutencao dentro de Analytics. | Consolidacao recomendada apenas dentro da camada analitica. |

Nenhuma nao conformidade e bloqueante para iniciar a implementacao, desde que a GP-PE-10 seja restrita.

## 20. Ressalvas

Ressalvas: **3**.

1. A centralizacao obrigatoria deve preservar os cinco parametros atualmente efetivos; nao deve expandir para todos os parametros do catalogo.
2. O catalogo hidrico e configuracoes JSON nao devem ser convertidos em constantes de codigo.
3. Algumas duplicidades em testes sao intencionais e devem continuar como verificacao externa, nao como consumo automatico da lista de producao.

## 21. Recomendacoes

1. Implementar primeiro apenas `C-OBR-01`.
2. Criar contrato especifico de mapeamento de qualidade, nao um modulo global de constantes.
3. Preservar schema CSV: `ph`, `turbidez`, `oxigenio_dissolvido`, `temperatura`, `agrotoxicos`.
4. Preservar mapeamento `temperatura` -> `temperatura_agua`.
5. Preservar categorias atuais: `quimicos`, `fisicos`, `contaminantes_agricolas`.
6. Preservar labels atuais do Analytics ou documentar alias por contexto.
7. Adicionar testes de paridade para os cinco adapters consumidores.
8. Nao alterar PA-01A, PA-01B, PA-01D ou PA-01E nesta frente.
9. Registrar rollback simples: restaurar listas locais dos adapters.

## 22. Parecer final

**PA-01C APTA PARA IMPLEMENTACAO COM RESSALVAS**.

Justificativa:

* ha diagnostico claro das listas relevantes;
* a duplicidade principal esta localizada e rastreada;
* existe fonte de autoridade para parametros hidricos, mas falta contrato unico para o mapeamento usado pelos adapters;
* a futura implementacao pode ser pequena, testavel e reversivel;
* a PA-01A deve ser preservada como autoridade semantica;
* a PA-01B permanece preservada, pois a auditoria nao recomenda reacoplar Dashboard e Analytics;
* os riscos de centralizacao excessiva foram delimitados.

Condicao final: PA-01C esta pronta para uma implementacao restrita na GP-PE-10, com foco no mapeamento compartilhado de parametros de qualidade e sem alteracao de comportamento funcional.

# PE-10 - Implementacao da PA-01C

## 1. Identificacao

Programa: **Plano Oficial de Evolucao do PROTEUS**.

Iniciativa: **PA-01 - Governanca de Limites, Responsabilidades e Comunicacao Segura**.

Frente implementada: **PA-01C - Centralizacao Controlada do Mapeamento de Parametros de Qualidade**.

Natureza: implementacao funcional restrita.

Status da GP: **CONCLUIDA**.

Status da PA-01C: **IMPLEMENTADA + TESTADA**.

Observacao de governanca: esta GP nao constitui auditoria pos-implementacao nem certificacao arquitetural da PA-01C.

## 2. Objetivo

Implementar exclusivamente a centralizacao obrigatoria identificada pela PE-09 para o mapeamento compartilhado de parametros de qualidade usado pelos adapters do PROTEUS.

A implementacao teve como objetivo remover as copias locais do mesmo mapeamento nos adapters, preservar o comportamento funcional existente e criar uma fonte oficial especifica, sem transformar catalogos, configuracoes, schemas CSV, telas ou testes em constantes globais.

## 3. Base documental

Foram utilizados como base obrigatoria:

* `docs/architecture/PE_09_PA01C_LIST_CENTRALIZATION_AUDIT.md`;
* `docs/architecture/PE_08_PA01B_POST_IMPLEMENTATION_AUDIT.md`;
* `docs/architecture/PE_07_PA01B_DASHBOARD_ANALYTICS_DECOUPLING.md`;
* `docs/architecture/PE_06_PA01B_ARCHITECTURAL_AUDIT.md`;
* `docs/architecture/PE_05_PA01A_IMPLEMENTATION_AUDIT.md`;
* `docs/architecture/PE_04_PA01A_SEMANTIC_STATUS_GOVERNANCE.md`;
* `docs/architecture/PE_03_PA01_IMPLEMENTATION_DECOMPOSITION.md`;
* `docs/architecture/PE_02_PA01_ARCHITECTURAL_AUDIT.md`;
* `docs/pac/PE_01_IMPLEMENTATION_EXECUTION_STRATEGY.md`;
* `docs/pac/PAC_14_PROJECT_EVOLUTION_PLAN.md`;
* documentacao arquitetural vigente;
* codigo atual do PROTEUS;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`.

## 4. Escopo implementado

Foi implementado apenas o item `C-OBR-01` da PE-09:

| Item | Descricao | Status |
| --- | --- | --- |
| C-OBR-01 | Centralizar o mapeamento de parametros de qualidade usado por adapters. | Implementado |

Nao foram implementadas as centralizacoes recomendadas:

| Item | Descricao | Status |
| --- | --- | --- |
| C-REC-01 | Centralizacao ampla de labels comunicacionais entre camadas. | Nao implementada nesta GP |
| C-REC-02 | Centralizacao de estados de governanca consumidos pela camada executiva. | Nao implementada nesta GP |
| C-REC-03 | Centralizacao de tolerancias e metricas internas de Analytics. | Nao implementada nesta GP |

## 5. Fonte oficial criada

Foi criada a fonte oficial especifica:

`monitoramento_hidrico/quality_parameter_mapping.py`

Essa fonte define:

* `QualityParameterMapping`;
* `QUALITY_PARAMETER_MAPPINGS`;
* `quality_parameter_triples()`;
* `quality_parameter_analytics_entries()`;
* `quality_parameter_governance_mapping()`.

Caracteristicas arquiteturais:

* modulo especifico do dominio de monitoramento hidrico;
* sem dependencia de PyQt;
* sem dependencia de Dashboard;
* sem dependencia de Analytics;
* sem dependencia de repositorios;
* sem dependencia de persistencia CSV;
* sem dependencia do catalogo JSON em runtime;
* sem alterar `monitoramento_hidrico/status_semantics.py`;
* sem criar modulo generico de constantes, `common`, `utils`, `lists`, `globals` ou equivalente.

## 6. Mapeamento oficial preservado

O contrato oficial preserva a ordem e os valores anteriores:

| Campo de entrada | Parametro hidrico | Categoria | Label preservado |
| --- | --- | --- | --- |
| `ph` | `ph` | `quimicos` | `pH` |
| `turbidez` | `turbidez` | `fisicos` | `Turbidez` |
| `oxigenio_dissolvido` | `oxigenio_dissolvido` | `quimicos` | `Oxigenio dissolvido` |
| `temperatura` | `temperatura_agua` | `fisicos` | `Temperatura da agua` |
| `agrotoxicos` | `agrotoxicos` | `contaminantes_agricolas` | `Agrotoxicos` |

O mapeamento `temperatura` -> `temperatura_agua` foi preservado explicitamente.

Os campos persistidos `ph`, `turbidez`, `oxigenio_dissolvido`, `temperatura` e `agrotoxicos` foram preservados.

## 7. Adapters migrados

Foram migrados os seguintes consumidores:

| Adapter | Autoridade local removida | Forma de consumo atual |
| --- | --- | --- |
| `monitoramento_hidrico/qualidade_agua_adapter.py` | `PARAMETROS_QUALIDADE_AGUA` | `quality_parameter_triples()` |
| `monitoramento_hidrico/dashboard_adapter.py` | `QUALITY_PARAMETER_FIELDS` | `quality_parameter_triples()` |
| `monitoramento_hidrico/operational_reports_adapter.py` | `REPORT_QUALITY_PARAMETERS` | `quality_parameter_triples()` |
| `monitoramento_hidrico/analytics_adapter.py` | `QUALITY_ANALYTICS_PARAMETERS` | `quality_parameter_analytics_entries()` |
| `monitoramento_hidrico/governance_adapter.py` | `GOVERNANCE_QUALITY_PARAMETERS` | `quality_parameter_governance_mapping()` |

Resultado: cinco copias locais foram removidas e substituidas por consumo de uma fonte especifica.

## 8. Arquivos alterados

Arquivos funcionais:

* `monitoramento_hidrico/quality_parameter_mapping.py`;
* `monitoramento_hidrico/qualidade_agua_adapter.py`;
* `monitoramento_hidrico/dashboard_adapter.py`;
* `monitoramento_hidrico/operational_reports_adapter.py`;
* `monitoramento_hidrico/analytics_adapter.py`;
* `monitoramento_hidrico/governance_adapter.py`.

Testes:

* `tests/test_quality_parameter_mapping.py`.

Documentacao e governanca:

* `docs/architecture/PE_10_PA01C_LIST_CENTRALIZATION_IMPLEMENTATION.md`;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`.

## 9. Justificativa arquitetural

A PE-09 identificou uma nao conformidade evolutiva: o mesmo mapeamento operacional entre campo de entrada, parametro hidrico e categoria estava duplicado em cinco adapters.

A centralizacao adotada reduz risco de divergencia sem expandir responsabilidade:

```text
Fonte especifica de parametros de qualidade
    -> adapters consumidores
        -> consumidores dos adapters
```

O novo modulo nao substitui o catalogo hidrico. Ele registra apenas o contrato operacional que traduz os campos efetivos usados pelos adapters para os parametros do dominio.

## 10. Preservacoes confirmadas

A implementacao preservou:

* semantica de status da PA-01A;
* contrato de desacoplamento Dashboard x Analytics da PA-01B;
* `DashboardAnalyticsSnapshotService`;
* `DashboardMonitoringAdapter`;
* `WaterHealthScoreChart`;
* formula do Water Health Score;
* catalogo hidrico JSON;
* configuracoes operacionais JSON;
* schemas CSV;
* campos persistidos;
* modelos de dominio;
* telas PyQt;
* limites observacionais;
* ICFACTORY;
* Discoveries congeladas.

## 11. Testes executados

Testes direcionados executados:

* `python -m unittest tests.test_quality_parameter_mapping` - 6 testes OK.
* `python -m unittest tests.test_qualidade_agua_monitoring_adapter tests.test_dashboard_monitoring_adapter tests.test_operational_reports_adapter tests.test_analytics_alerts tests.test_water_health_score tests.test_governance_monitoring_adapter tests.test_governance_service` - 21 testes OK.
* `python -m unittest tests.test_status_semantics` - 3 testes OK.
* `python -m unittest tests.test_dashboard_analytics_snapshot` - 5 testes OK.

Validacao textual executada:

* busca por autoridades locais antigas em `monitoramento_hidrico` retornou vazia para definicoes `PARAMETROS_QUALIDADE_AGUA =`, `QUALITY_PARAMETER_FIELDS =`, `REPORT_QUALITY_PARAMETERS =`, `QUALITY_ANALYTICS_PARAMETERS =` e `GOVERNANCE_QUALITY_PARAMETERS =`.

Regressao completa:

* `python -m unittest discover -s tests` - 97 testes OK.

## 12. Impactos observados

Impacto funcional esperado:

* nenhum comportamento funcional alterado;
* os mesmos parametros continuam sendo avaliados;
* a mesma ordem continua sendo usada;
* os mesmos labels do Analytics continuam sendo expostos;
* a Governanca continua recebendo a mesma estrutura de consulta;
* os adapters continuam selecionando politicas e avaliando resultados da mesma forma.

Impacto arquitetural:

* reducao de duplicidade entre adapters;
* fonte unica para o mapeamento operacional de qualidade;
* manutencao dos limites entre adapters, Analytics, Dashboard, Governanca e persistencia.

## 13. Limitacoes remanescentes

Permanecem fora desta GP:

* auditoria pos-implementacao da PA-01C;
* certificacao da PA-01C;
* centralizacao ampla de labels entre UI, relatorios e Analytics;
* centralizacao de estados de governanca consumidos pela camada executiva;
* centralizacao de tolerancias e metricas internas de Analytics;
* governanca da reavaliacao controlada da PA-01D;
* guardrails comunicacionais da PA-01E.

## 14. Risco e rollback

Risco de implantacao: baixo a medio.

Motivo: a alteracao substitui listas locais por uma fonte especifica preservando valores, ordem e formatos de consumo.

Rollback tecnico possivel:

* restaurar as listas locais anteriores nos cinco adapters;
* remover `monitoramento_hidrico/quality_parameter_mapping.py`;
* remover o teste de contrato compartilhado.

## 15. Parecer final

A GP-PE-10 implementou de forma restrita a PA-01C, conforme a delimitacao da PE-09.

Parecer:

**GP-PE-10 CONCLUIDA.**

**PA-01C IMPLEMENTADA + TESTADA.**

Condicao de governanca:

A PA-01C ainda deve passar por auditoria pos-implementacao propria antes de ser considerada auditada ou certificada.

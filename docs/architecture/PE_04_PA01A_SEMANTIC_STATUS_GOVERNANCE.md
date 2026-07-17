# PE-04 - PA-01A - Governanca Semantica de Status

## 1. Objetivo

Implementar a frente **PA-01A - Governanca Semantica de Status**, definida pela GP-PE-03, padronizando a terminologia de status comunicada pelo PROTEUS sem alterar regras de avaliacao, thresholds, score, governanca operacional, persistencia ou arquitetura de camadas.

## 2. Base documental

Foram utilizadas como referencia:

* `docs/architecture/PE_03_PA01_IMPLEMENTATION_DECOMPOSITION.md`;
* `docs/architecture/PE_02_PA01_ARCHITECTURAL_AUDIT.md`;
* `docs/pac/PE_01_IMPLEMENTATION_EXECUTION_STRATEGY.md`;
* `docs/pac/PAC_14_PROJECT_EVOLUTION_PLAN.md`;
* documentacao arquitetural vigente;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`.

## 3. Escopo implementado

A GP-PE-04 implementou exclusivamente governanca semantica de status:

* criou vocabulario oficial de rotulos comunicados em `monitoramento_hidrico/status_semantics.py`;
* substituiu rotulos ambiguos de qualidade em adapters por rotulos observacionais;
* substituiu status textuais do Water Health Score por rotulos de score analitico;
* substituiu status executivo bruto por rotulos executivos observacionais;
* converteu mensagens de Analytics que expunham codigos tecnicos para rotulos observacionais;
* preservou codigos tecnicos internos do motor observacional;
* preservou regras, thresholds, calculos, severidades, persistencia e fluxo entre camadas.

## 4. Inventario previo dos status

| Familia de status | Origem | Consumidores | Impacto potencial | Risco de alteracao |
| --- | --- | --- | --- | --- |
| Status observacional tecnico (`NORMAL`, `ATENCAO`, `CRITICO`, `NAO_AVALIAVEL`) | `monitoramento_hidrico/avaliacao.py` | Adapters hidricos, Analytics, Governanca, testes de nucleo | Alto se alterado, pois compoe contrato tecnico interno | Alto; preservado integralmente |
| Status visual de qualidade | Adapters de Qualidade, Dashboard e Relatorios | Telas de qualidade, Dashboard, Relatorios | Medio; altera comunicacao ao usuario | Medio; padronizado sem mudar decisao |
| Status do Water Health Score | `analytics/scoring.py` | Dashboard, Painel Executivo, Recommendation via snapshot | Medio; altera rotulo analitico | Medio; thresholds preservados |
| Status executivo | `executive/rules.py` e `executive/models.py` | Painel Executivo, testes executivos | Medio; altera comunicacao executiva | Medio; regra de classificacao preservada |
| Severidade de alertas/eventos | Analytics e Governanca | Governanca operacional, Painel Executivo, testes | Alto se alterada | Nao alterada |
| Status de Projeto | Dominio Projeto | Tela de Projeto, Dossie, testes de projeto | Fora do escopo PA-01A | Nao alterado |

## 5. Terminologia oficial implementada

| Contexto | Rotulos oficiais | Significado | Limite PA-01 |
| --- | --- | --- | --- |
| Avaliacao observacional agregada | `Avaliacao observacional normal`, `Avaliacao observacional requer atencao` | Resultado comunicavel dos adapters de qualidade | Nao representa conformidade legal, sanitaria, ambiental ou regulatoria |
| Codigo observacional tecnico comunicado | `Avaliacao observacional normal`, `Avaliacao observacional em atencao`, `Avaliacao observacional critica`, `Avaliacao observacional nao avaliavel` | Traducao de codigos tecnicos quando exibidos em mensagens | Codigo tecnico permanece interno |
| Water Health Score | `Score analitico sem dados`, `Score analitico excelente`, `Score analitico bom`, `Score analitico em atencao`, `Score analitico critico`, `Score analitico muito critico` | Faixa analitica preventiva calculada por Analytics | Nao representa certificacao ou laudo |
| Executivo | `Executivo observacional normal`, `Executivo observacional em atencao`, `Executivo observacional critico` | Sintese executiva de sinais consolidados | Nao substitui decisao humana |

## 6. Arquivos alterados

| Arquivo | Justificativa arquitetural |
| --- | --- |
| `monitoramento_hidrico/status_semantics.py` | Novo vocabulario oficial PA-01A para rotulos comunicados e significados. |
| `monitoramento_hidrico/qualidade_agua_adapter.py` | Substitui rotulos "Dentro/Fora do padrao" por rotulos observacionais padronizados. |
| `monitoramento_hidrico/dashboard_adapter.py` | Alinha status de qualidade do Dashboard ao vocabulario PA-01A. |
| `monitoramento_hidrico/operational_reports_adapter.py` | Alinha status de relatorios e introduz contagem com nome observacional. |
| `analytics/scoring.py` | Alinha status do Water Health Score a rotulos de score analitico e traduz codigos observacionais em explicacoes. |
| `analytics/alerts.py` | Traduz codigos observacionais em mensagens preventivas. |
| `executive/models.py` | Alinha status executivo a rotulos executivos observacionais. |
| `qualidade_agua.py` | Atualiza comparacao visual para o novo rotulo observacional normal. |
| `relatorios.py` | Atualiza texto de relatorio para "avaliacao observacional em atencao". |
| `painel_executivo.py` | Atualiza titulo do cartao para "Status executivo observacional". |
| `tests/test_status_semantics.py` | Cria testes especificos para o vocabulario PA-01A. |
| Testes impactados | Atualizam expectativas textuais sem mudar comportamento esperado. |

## 7. Impactos observados

* Dashboard: passa a receber status de qualidade em linguagem observacional padronizada.
* Qualidade da Agua: mantem a mesma regra de coloracao, mas comparando com o novo rotulo normal.
* Relatorios: mantem a mesma contagem, mas comunica "registros com avaliacao observacional em atencao".
* Analytics: mantem score e penalidades, mas comunica faixas como score analitico.
* Governanca: codigos tecnicos e eventos permanecem compativeis.
* Painel Executivo: comunica status executivo como observacional.
* Recommendation: permanece consumindo sinais consolidados; sem acesso novo a nucleo, CSV ou motor.

## 8. Compatibilidade

Foram preservados:

* codigos tecnicos do motor observacional;
* regras de avaliacao;
* limites observacionais;
* thresholds do Water Health Score;
* regras de classificacao executiva;
* severidades de alertas;
* schema de CSV e JSON;
* fluxo Dashboard, Analytics, Governanca e Painel Executivo.

A compatibilidade funcional foi validada por testes.

## 9. Testes executados

Comando de testes impactados:

```text
python -m unittest tests.test_status_semantics tests.test_qualidade_agua_monitoring_adapter tests.test_dashboard_monitoring_adapter tests.test_operational_reports_adapter tests.test_water_health_score tests.test_analytics_alerts tests.test_executive_rules tests.test_executive_service tests.test_executive_recommendation_service
```

Resultado:

```text
Ran 32 tests
OK
```

Comando de regressao completa:

```text
python -m unittest discover -s tests
```

Resultado:

```text
Ran 86 tests
OK
```

Observacao: `pytest` nao estava instalado no ambiente, portanto a validacao foi executada com `unittest`, que e a estrutura usada pelos testes existentes.

## 10. Limitacoes remanescentes

* A centralizacao de listas e catalogos duplicados permanece fora do escopo e deve ser tratada na PA-01C.
* O desacoplamento Dashboard x Analytics permanece fora do escopo e deve ser tratado na PA-01B.
* A reavaliacao controlada da Governanca permanece fora do escopo e deve ser tratada na PA-01D.
* Guardrails comunicacionais amplos entre camadas permanecem fora do escopo e devem ser tratados na PA-01E.
* O metodo `contar_fora_padrao()` foi mantido como alias de compatibilidade, mas os componentes atualizados usam a nomenclatura observacional nova.

## 11. Parecer final

Status: CONCLUIDA.

A GP-PE-04 implementou a Governanca Semantica de Status da PA-01A com escopo controlado. As ambiguidades principais apontadas pela GP-PE-02 foram tratadas nos componentes de runtime por meio de rotulos observacionais, analiticos e executivos explicitos.

A implementacao preserva a autoridade do motor observacional, a compatibilidade com Analytics, Governanca, Dashboard e Painel Executivo, e nao altera comportamento funcional. A rastreabilidade permanece preservada por documentacao, vocabulario oficial e testes automatizados.

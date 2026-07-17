# PE-16 — Implementação da PA-01E — Guardrails Obrigatórios de Comunicação

> **STATUS DESTE REGISTRO: CONCLUÍDA NO ESCOPO AUTORIZADO — VALIDAÇÃO APROVADA**

## 1. Identificação

Programa: **GP-PE-16 — Implementação dos Guardrails Obrigatórios de Comunicação (PA-01E)**.

Iniciativa: **PA-01 — Governança de Limites, Responsabilidades e Comunicação Segura**.

Frente: **PA-01E — Guardrails de Comunicação entre Camadas**.

Natureza: implementação documental e de testes estáticos, sem alteração funcional de runtime.

## 2. Fonte de autoridade e escopo

A autoridade desta implementação é a auditoria `docs/architecture/PE_15_PA01E_COMMUNICATION_GUARDRAILS_AUDIT.md`, que classificou cinco guardrails como obrigatórios e emitiu o parecer **PA-01E APTA PARA IMPLEMENTAÇÃO COM RESSALVAS**.

Esta intervenção está limitada a:

* implementar proteção verificável para G-OBR-01 a G-OBR-05;
* ajustar `tests/test_pa01_communication_guardrails.py`;
* manter este registro documental da GP-PE-16;
* executar a validação específica, os testes arquiteturais relacionados e a suíte completa.

Não integra o escopo:

* implementar guardrails classificados apenas como recomendados;
* criar checklist geral PA-01;
* formalizar exceções históricas como nova regra arquitetural;
* criar factories, services, adapters, facades ou novas camadas;
* alterar runtime, contratos, persistência, regras, políticas ou schemas;
* modificar a Constituição do ICFACTORY, Harnesses ou conceitos da GP-R03;
* corrigir falhas externas ao escopo desta GP.

## 3. Arquivos da intervenção

Arquivos autorizados e abrangidos pela intervenção:

| Arquivo | Finalidade |
| --- | --- |
| `tests/test_pa01_communication_guardrails.py` | Implementar cinco verificações estáticas, uma para cada guardrail obrigatório. |
| `docs/architecture/PE_16_PA01E_COMMUNICATION_GUARDRAILS_IMPLEMENTATION.md` | Registrar escopo, rastreabilidade, limitações, validação e conclusão baseada em evidências. |

Nenhum arquivo de runtime é alterado.

## 4. Guardrails obrigatórios

### G-OBR-01 — Fronteira entre UI e Analytics interno

A UI não pode importar ou instanciar diretamente `AnalyticsRepository` ou `WaterHealthScoreCalculator`. A proteção preserva `DashboardAnalyticsSnapshotService` como contrato intermediário consolidado pela PA-01B.

### G-OBR-02 — Autoridade da reavaliação governada

Consumidores externos não podem tratar `OperationalGovernanceHydricMonitoringAdapter` como autoridade primária. A cadeia oficial deve calcular as decisões em `OperationalGovernanceService.sync_from_analytics()` antes de enviá-las ao adapter.

### G-OBR-03 — Fonte única dos parâmetros de qualidade

Adapters de qualidade devem consumir funções de `monitoramento_hidrico/quality_parameter_mapping.py` e não podem recriar autoridades ou coleções locais de parâmetros compartilhados.

### G-OBR-04 — Vocabulário funcional de status

Superfícies de comunicação não podem reintroduzir textos funcionais sensíveis já classificados como ambíguos pela PA-01A. O consumo legítimo do vocabulário oficial de `monitoramento_hidrico/status_semantics.py` permanece permitido.

### G-OBR-05 — Fronteira da camada Executive

Executive e Executive Recommendation não podem acessar diretamente CSV, `PolicyEngine`, `AvaliacaoObservacionalService` ou adapters hídricos. O consumo do módulo oficial `monitoramento_hidrico.status_semantics` permanece permitido.

## 5. Matriz entre guardrails e testes

| Guardrail | Teste | Técnica principal | Evidência esperada |
| --- | --- | --- | --- |
| G-OBR-01 | `test_g_obr_01_ui_does_not_access_internal_analytics_dependencies` | AST de imports e chamadas | Ausência de dependências internas de Analytics nas telas. |
| G-OBR-02 | `test_g_obr_02_governance_service_retains_reevaluation_authority` | AST da cadeia oficial, ordem das chamadas e imports externos | Decisão produzida pela Governança antes do adapter e ausência de consumo externo direto. |
| G-OBR-03 | `test_g_obr_03_quality_adapters_use_the_central_parameter_mapping` | AST de imports, atribuições e coleções literais | Uso da fonte central e ausência de listas locais compartilhadas. |
| G-OBR-04 | `test_g_obr_04_runtime_avoids_non_official_sensitive_status_texts` | AST de literais de comunicação com normalização Unicode | Ausência de textos funcionais sensíveis não oficiais. |
| G-OBR-05 | `test_g_obr_05_executive_uses_no_hydric_engine_adapter_or_csv` | AST de imports, chamadas e literais de caminhos CSV | Ausência de acesso direto da camada Executive às dependências proibidas. |

Cada falha deve informar o identificador do guardrail, o arquivo responsável e a evidência sintática encontrada.

## 6. Arquivos abrangidos pelos testes

### 6.1 Superfícies de apresentação

* `main.py`;
* `qualidade_agua.py`;
* `relatorios.py`;
* `painel_executivo.py`;
* `previsao_analitica.py`;
* `governanca_operacional.py`;
* `dados_ambientais.py`;
* `consumo_distribuicao.py`;
* `projeto_monitoramento_page.py`.

### 6.2 Analytics

* `analytics/alerts.py`;
* `analytics/dashboard_snapshot.py`;
* `analytics/models.py`;
* `analytics/repositories.py`;
* `analytics/scoring.py`;
* `analytics/service.py`;
* `analytics/trends.py`.

### 6.3 Adapters de qualidade

* `monitoramento_hidrico/qualidade_agua_adapter.py`;
* `monitoramento_hidrico/dashboard_adapter.py`;
* `monitoramento_hidrico/operational_reports_adapter.py`;
* `monitoramento_hidrico/analytics_adapter.py`;
* `monitoramento_hidrico/governance_adapter.py`.

### 6.4 Executive

* `executive/service.py`;
* `executive/rules.py`;
* `executive/models.py`;
* `executive_recommendation/service.py`;
* `executive_recommendation/rules.py`;
* `executive_recommendation/models.py`.

### 6.5 Cadeia oficial de Governança

* `governance/service.py`.

## 7. Exceções arquiteturais preservadas

Os testes foram delimitados para não transformar ressalvas conhecidas em violações novas:

* leituras históricas de CSV pelas telas não são bloqueadas por G-OBR-01;
* a instanciação legada de motores exclusivamente para montagem de adapters de UI não é ampliada nem tratada como nova não conformidade;
* o fallback compatível de `monitoramento_hidrico/governance_adapter.py` quando chamado sem `decisions` permanece inalterado;
* G-OBR-02 protege a cadeia oficial e a autoridade de `OperationalGovernanceService`, sem remover o fallback;
* o consumo de `monitoramento_hidrico.status_semantics` pela camada Executive é permitido;
* os textos oficiais centralizados em `status_semantics.py` não são tratados como violações de G-OBR-04.

Essas exceções são apenas preservadas. Esta GP não as promove a padrão para novos fluxos e não implementa os guardrails recomendados da GP-PE-15.

## 8. Limitações dos testes estáticos

* A análise AST protege os arquivos explicitamente enumerados; novos arquivos exigirão inclusão deliberada na cobertura.
* A inspeção de imports e chamadas não observa dependências construídas dinamicamente em runtime.
* G-OBR-03 identifica autoridades conhecidas e coleções literais com múltiplos parâmetros; estruturas geradas dinamicamente podem exigir revisão arquitetural.
* G-OBR-04 protege os textos funcionais sensíveis identificados pela PA-01A, mas não substitui revisão semântica humana de todo novo texto.
* G-OBR-05 identifica imports, instanciações e referências literais a arquivos CSV; acesso indireto ou dinâmico deve continuar sujeito a auditoria.
* Aprovação dos testes demonstra conformidade com os guardrails codificados, não certificação integral de toda a arquitetura.

## 9. Validação

### 9.1 Ordem obrigatória

1. teste específico da PA-01E;
2. testes arquiteturais relacionados à PA-01A até PA-01D;
3. suíte completa de testes.

### 9.2 Comandos e resultados

Os comandos foram executados na ordem obrigatória.

#### 9.2.1 Teste específico da PA-01E — primeira execução

```text
python -m unittest tests.test_pa01_communication_guardrails
```

Resultado:

```text
Ran 5 tests in 0.180s
FAILED (failures=1)
```

Falha observada:

* G-OBR-04 classificou `painel_executivo.py:39`, título `Status executivo observacional`, como ocorrência do fragmento `status executivo`.

Análise:

* o texto é título estrutural específico do card, não valor funcional de status;
* nenhuma alteração em `painel_executivo.py` foi autorizada ou necessária;
* a detecção por fragmento produzia falso positivo e contrariava a exigência de preservar comunicação legítima.

Ajuste realizado exclusivamente no teste autorizado:

* comparação de rótulos ambíguos por igualdade exata após normalização Unicode, em vez de busca de fragmentos dentro de títulos mais específicos.

#### 9.2.2 Teste específico da PA-01E — execução final

```text
python -m unittest tests.test_pa01_communication_guardrails
```

Resultado:

```text
Ran 5 tests in 0.181s
OK
```

Todos os cinco guardrails obrigatórios foram aprovados.

#### 9.2.3 Testes relacionados à PA-01A

```text
python -m unittest tests.test_status_semantics tests.test_qualidade_agua_monitoring_adapter tests.test_dashboard_monitoring_adapter tests.test_operational_reports_adapter tests.test_water_health_score tests.test_analytics_alerts tests.test_executive_rules tests.test_executive_service tests.test_executive_recommendation_service
```

Resultado:

```text
Ran 34 tests in 0.079s
OK
```

#### 9.2.4 Testes relacionados à PA-01B

```text
python -m unittest tests.test_dashboard_analytics_snapshot tests.test_water_health_score tests.test_dashboard_monitoring_adapter tests.test_analytics_repository tests.test_analytics_trends
```

Resultado:

```text
Ran 15 tests in 0.038s
OK
```

#### 9.2.5 Testes relacionados à PA-01C

```text
python -m unittest tests.test_quality_parameter_mapping tests.test_qualidade_agua_monitoring_adapter tests.test_dashboard_monitoring_adapter tests.test_operational_reports_adapter tests.test_analytics_alerts tests.test_water_health_score tests.test_governance_monitoring_adapter tests.test_governance_service
```

Resultado:

```text
Ran 33 tests in 0.150s
OK
```

#### 9.2.6 Testes relacionados à PA-01D

```text
python -m unittest tests.test_governance_monitoring_adapter tests.test_governance_service tests.test_governance_rules tests.test_governance_repository
```

Resultado:

```text
Ran 14 tests in 0.020s
OK
```

#### 9.2.7 Suíte completa

```text
python -m unittest discover -s tests
```

Resultado:

```text
Ran 110 tests in 0.285s
OK
```

Resultado consolidado:

* validação específica da PA-01E aprovada;
* testes arquiteturais relacionados à PA-01A até PA-01D aprovados;
* suíte completa aprovada;
* falhas externas ao escopo: nenhuma;
* arquivos de runtime alterados: nenhum.

## 10. Inconsistência documental local fora do escopo

`docs/history/HISTORY.md` e `docs/roadmap/ROADMAP.md` possuem alterações locais preexistentes que já declaram a conclusão da GP-PE-16.

Esses registros:

* não foram produzidos nesta intervenção;
* não foram validados nesta intervenção;
* não foram incorporados como evidência desta implementação;
* não serão alterados, staged ou consolidados no escopo autorizado.

A inconsistência entre essas declarações preexistentes e a validação efetivamente registrada neste documento permanece fora do escopo da GP-PE-16 autorizada nesta intervenção.

## 11. Conclusão

Os cinco guardrails obrigatórios G-OBR-01 a G-OBR-05 foram implementados como verificações estáticas rastreáveis e a validação específica da PA-01E foi aprovada com cinco testes sem falhas.

Os testes relacionados à PA-01A, PA-01B, PA-01C e PA-01D e a suíte completa também foram aprovados, sem regressão observada. Nenhum arquivo de runtime, contrato, service, adapter, repository ou persistência foi alterado.

Com base exclusivamente nessas evidências, a **GP-PE-16 está CONCLUÍDA no escopo autorizado dos cinco guardrails obrigatórios**.

Essa conclusão não implementa os guardrails recomendados, não elimina as limitações dos testes estáticos e não incorpora ou valida os registros locais preexistentes de `HISTORY.md` e `ROADMAP.md`.

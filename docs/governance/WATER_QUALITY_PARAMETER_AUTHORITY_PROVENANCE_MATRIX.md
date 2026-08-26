# PROTEUS — Matriz de Autoridade e Proveniência dos Parâmetros de Qualidade da Água

## Controle documental

| Campo | Registro |
| --- | --- |
| Natureza | Matriz documental de governança e rastreabilidade |
| Escopo | Oito parâmetros operacionais identificados pelas auditorias PROT-AUD-001/002 e AUTH-TRACE-001/002/003 |
| Autoridade para criação | Product Owner — IOP `PROTEUS_AUTHORITY_MATRIX_WRITE_03` |
| Executor documental | Codex, sem autoridade de domínio |
| Estado | EXPERIMENTAL — EM VALIDAÇÃO |
| Efeito normativo | NENHUM |
| Estado do ICFACTORY | INALTERADO |

## Aviso obrigatório

Este documento registra o estado de proveniência e autoridade dos parâmetros atualmente utilizados pelo PROTEUS.

A presença de um valor neste documento **NÃO** constitui validação científica, sanitária ou normativa.

Valores sem autoridade técnica comprovada permanecem classificados como referências observacionais internas até validação por autoridade especializada competente.

## Limites de autoridade

- O Product Owner autorizou a criação e a estrutura de governança desta matriz, mas não validou tecnicamente os limiares.
- O Codex transcreveu somente fatos verificáveis no repositório e não selecionou fonte, norma ou valor técnico.
- A autoria Git ou documental de um valor não constitui autoridade técnica sobre ele.
- `DOCUMENT_FOUND` não equivale a `TECHNICALLY_VALIDATED`.
- `TEST_PASS` não equivale a correção científica, sanitária ou normativa.
- Campos dependentes de julgamento técnico permanecem marcados como `SPECIALIST_AUTHORITY_REQUIRED`.

## Modelo de rastreabilidade

`SOURCE/AUTHORITY → REQUIREMENT → RULE → CODE → TEST → OUTPUT`

No estado observado, o catálogo materializa as regras internas, porém a cadeia anterior ao catálogo não possui fonte ou autoridade técnica vinculada. Os documentos PAC registram essa insuficiência e requisitos de evolução; eles não validam os valores atuais.

## Matriz

### PARAMETER_ID: `turbidez`

| Campo | Registro |
| --- | --- |
| DISPLAY_NAME | Turbidez |
| CURRENT_VALUE_OR_RANGE | Máximo `5.0` |
| UNIT | `NTU` |
| CURRENT_USE | Limite observacional consumido pelo motor; o parâmetro integra o mapeamento operacional de qualidade, Analytics e saídas derivadas. |
| SOURCE | `UNVERIFIED_OR_NOT_LINKED` |
| SOURCE_VERSION | `PENDING_UNVERIFIED` |
| REQUIREMENT | PAC-01-005 registra fundamentação insuficiente; PAC-02-017 mantém a validação técnica dos limites como questão aberta. |
| APPLICABILITY_CONTEXT | O catálogo declara `rural`, `industrial`, `urbano_saneamento`, `ambiental_rio`, `eta` e `ete`; aplicabilidade técnica: `SPECIALIST_AUTHORITY_REQUIRED`. |
| TECHNICAL_AUTHORITY | `SPECIALIST_AUTHORITY_REQUIRED` |
| VALIDATION_STATUS | `NOT_TECHNICALLY_VALIDATED` |
| CODE_REFERENCE | `data/monitoramento_hidrico_catalogo.json`, parâmetro `turbidez`; `monitoramento_hidrico/avaliacao.py`, `AvaliacaoObservacionalService.avaliar`; `monitoramento_hidrico/quality_parameter_mapping.py`, `QUALITY_PARAMETER_MAPPINGS`. |
| TEST_REFERENCE | `tests/test_monitoramento_hidrico_avaliacao.py`, casos de fronteira `5.0`, `5.5`, `6.0` e `10.0`; testes demonstram comportamento do código, não correção de domínio. |
| NOTES | Critério registrado: “referencia operacional inicial, sem carater legal”. Cadeia atual: `SOURCE/AUTHORITY=PENDING → REQUIREMENT=PARCIAL → RULE=REGISTRADA → CODE=VINCULADO → TEST=ESPECÍFICO → OUTPUT=OPERACIONAL`. |

### PARAMETER_ID: `ph`

| Campo | Registro |
| --- | --- |
| DISPLAY_NAME | pH |
| CURRENT_VALUE_OR_RANGE | Mínimo `6.0`; máximo `9.5` |
| UNIT | `unidade de pH` conforme metadado do catálogo |
| CURRENT_USE | Faixa observacional consumida pelo motor; o parâmetro integra o mapeamento operacional de qualidade, Analytics e saídas derivadas. |
| SOURCE | `UNVERIFIED_OR_NOT_LINKED` |
| SOURCE_VERSION | `PENDING_UNVERIFIED` |
| REQUIREMENT | PAC-01-005 requer fundamentação ambiental completa por contexto; nenhuma fonte originadora específica foi vinculada. |
| APPLICABILITY_CONTEXT | O catálogo declara `rural`, `industrial`, `urbano_saneamento`, `ambiental_rio`, `eta` e `ete`; aplicabilidade técnica: `SPECIALIST_AUTHORITY_REQUIRED`. |
| TECHNICAL_AUTHORITY | `SPECIALIST_AUTHORITY_REQUIRED` |
| VALIDATION_STATUS | `NOT_TECHNICALLY_VALIDATED` |
| CODE_REFERENCE | `data/monitoramento_hidrico_catalogo.json`, parâmetro `ph`; `monitoramento_hidrico/avaliacao.py`, `AvaliacaoObservacionalService.avaliar`; `monitoramento_hidrico/quality_parameter_mapping.py`, `QUALITY_PARAMETER_MAPPINGS`. |
| TEST_REFERENCE | `tests/test_monitoramento_hidrico_avaliacao.py`, casos `6.0`, `7.0`, `7.2` e `9.5`; testes demonstram comportamento do código, não correção de domínio. |
| NOTES | Critério registrado: “faixa observacional inicial, sem carater legal”. Cadeia atual: `SOURCE/AUTHORITY=PENDING → REQUIREMENT=PARCIAL → RULE=REGISTRADA → CODE=VINCULADO → TEST=ESPECÍFICO → OUTPUT=OPERACIONAL`. |

### PARAMETER_ID: `oxigenio_dissolvido`

| Campo | Registro |
| --- | --- |
| DISPLAY_NAME | Oxigênio dissolvido |
| CURRENT_VALUE_OR_RANGE | Mínimo `5.0` |
| UNIT | `mg/L` |
| CURRENT_USE | Limite observacional consumido pelo motor; o parâmetro integra o mapeamento operacional de qualidade, Analytics e saídas derivadas. |
| SOURCE | `UNVERIFIED_OR_NOT_LINKED` |
| SOURCE_VERSION | `PENDING_UNVERIFIED` |
| REQUIREMENT | PAC-01-005 requer fundamentação ambiental completa por contexto; nenhuma fonte originadora específica foi vinculada. |
| APPLICABILITY_CONTEXT | O catálogo declara `rural`, `industrial`, `urbano_saneamento`, `ambiental_rio`, `eta` e `ete`; aplicabilidade técnica: `SPECIALIST_AUTHORITY_REQUIRED`. |
| TECHNICAL_AUTHORITY | `SPECIALIST_AUTHORITY_REQUIRED` |
| VALIDATION_STATUS | `NOT_TECHNICALLY_VALIDATED` |
| CODE_REFERENCE | `data/monitoramento_hidrico_catalogo.json`, parâmetro `oxigenio_dissolvido`; `monitoramento_hidrico/avaliacao.py`, `AvaliacaoObservacionalService.avaliar`; `monitoramento_hidrico/quality_parameter_mapping.py`, `QUALITY_PARAMETER_MAPPINGS`. |
| TEST_REFERENCE | `tests/test_monitoramento_hidrico_avaliacao.py`, casos `4.0` e `5.0`; testes demonstram comportamento do código, não correção de domínio. |
| NOTES | Critério registrado: “referencia observacional para atencao operacional”. Cadeia atual: `SOURCE/AUTHORITY=PENDING → REQUIREMENT=PARCIAL → RULE=REGISTRADA → CODE=VINCULADO → TEST=ESPECÍFICO → OUTPUT=OPERACIONAL`. |

### PARAMETER_ID: `dbo`

| Campo | Registro |
| --- | --- |
| DISPLAY_NAME | DBO |
| CURRENT_VALUE_OR_RANGE | Máximo `10.0` |
| UNIT | `mg/L` |
| CURRENT_USE | Regra disponível no catálogo e executável pelo motor genérico quando o parâmetro é submetido; não foi localizado mapeamento na entrada operacional corrente de qualidade da água. |
| SOURCE | `UNVERIFIED_OR_NOT_LINKED` |
| SOURCE_VERSION | `PENDING_UNVERIFIED` |
| REQUIREMENT | PAC-01-005 registra fundamentação insuficiente; PAC-02 recomenda contextualizar DBO em função do processo. |
| APPLICABILITY_CONTEXT | O catálogo declara `rural`, `industrial`, `urbano_saneamento`, `ambiental_rio`, `eta` e `ete`; aplicabilidade técnica: `SPECIALIST_AUTHORITY_REQUIRED`. |
| TECHNICAL_AUTHORITY | `SPECIALIST_AUTHORITY_REQUIRED` |
| VALIDATION_STATUS | `NOT_TECHNICALLY_VALIDATED` |
| CODE_REFERENCE | `data/monitoramento_hidrico_catalogo.json`, parâmetro `dbo`; `monitoramento_hidrico/avaliacao.py`, `AvaliacaoObservacionalService.avaliar`. |
| TEST_REFERENCE | `PENDING_UNVERIFIED` — nenhum teste numérico específico do limiar `10.0` foi localizado. |
| NOTES | Critério registrado: “referencia observacional para tendencia”. Cadeia atual: `SOURCE/AUTHORITY=PENDING → REQUIREMENT=PARCIAL → RULE=REGISTRADA → CODE=GENÉRICO → TEST=PENDING → OUTPUT_DIRETO=PENDING`. |

### PARAMETER_ID: `dqo`

| Campo | Registro |
| --- | --- |
| DISPLAY_NAME | DQO |
| CURRENT_VALUE_OR_RANGE | Máximo `50.0` |
| UNIT | `mg/L` |
| CURRENT_USE | Regra disponível no catálogo e executável pelo motor genérico quando o parâmetro é submetido; não foi localizado mapeamento na entrada operacional corrente de qualidade da água. |
| SOURCE | `UNVERIFIED_OR_NOT_LINKED` |
| SOURCE_VERSION | `PENDING_UNVERIFIED` |
| REQUIREMENT | PAC-01-005 registra fundamentação insuficiente; PAC-02 recomenda contextualizar DQO em função do processo. |
| APPLICABILITY_CONTEXT | O catálogo declara `rural`, `industrial`, `urbano_saneamento`, `ambiental_rio`, `eta` e `ete`; aplicabilidade técnica: `SPECIALIST_AUTHORITY_REQUIRED`. |
| TECHNICAL_AUTHORITY | `SPECIALIST_AUTHORITY_REQUIRED` |
| VALIDATION_STATUS | `NOT_TECHNICALLY_VALIDATED` |
| CODE_REFERENCE | `data/monitoramento_hidrico_catalogo.json`, parâmetro `dqo`; `monitoramento_hidrico/avaliacao.py`, `AvaliacaoObservacionalService.avaliar`. |
| TEST_REFERENCE | `PENDING_UNVERIFIED` — nenhum teste numérico específico do limiar `50.0` foi localizado. |
| NOTES | Critério registrado: “referencia observacional para tendencia”. Cadeia atual: `SOURCE/AUTHORITY=PENDING → REQUIREMENT=PARCIAL → RULE=REGISTRADA → CODE=GENÉRICO → TEST=PENDING → OUTPUT_DIRETO=PENDING`. |

### PARAMETER_ID: `cloro_residual`

| Campo | Registro |
| --- | --- |
| DISPLAY_NAME | Cloro residual |
| CURRENT_VALUE_OR_RANGE | Mínimo `0.2`; máximo `2.0` |
| UNIT | `mg/L` |
| CURRENT_USE | Regra disponível no catálogo e executável pelo motor genérico quando o parâmetro é submetido; o Policy Engine possui teste de seleção para o identificador, sem teste específico da faixa numérica. |
| SOURCE | `UNVERIFIED_OR_NOT_LINKED` |
| SOURCE_VERSION | `PENDING_UNVERIFIED` |
| REQUIREMENT | PAC-01-005 registra fundamentação insuficiente; PAC-02-017 mantém contexto operacional e validação técnica como questões abertas. |
| APPLICABILITY_CONTEXT | O catálogo declara `rural`, `industrial`, `urbano_saneamento`, `ambiental_rio`, `eta` e `ete`; aplicabilidade técnica: `SPECIALIST_AUTHORITY_REQUIRED`. |
| TECHNICAL_AUTHORITY | `SPECIALIST_AUTHORITY_REQUIRED` |
| VALIDATION_STATUS | `NOT_TECHNICALLY_VALIDATED` |
| CODE_REFERENCE | `data/monitoramento_hidrico_catalogo.json`, parâmetro `cloro_residual`; `monitoramento_hidrico/avaliacao.py`, `AvaliacaoObservacionalService.avaliar`. |
| TEST_REFERENCE | `tests/test_monitoramento_hidrico_policy_engine.py` verifica separação entre seleção e execução para `cloro_residual`; teste numérico específico da faixa: `PENDING_UNVERIFIED`. |
| NOTES | Critério registrado: “faixa operacional inicial, sem carater legal”. Cadeia atual: `SOURCE/AUTHORITY=PENDING → REQUIREMENT=PARCIAL → RULE=REGISTRADA → CODE=GENÉRICO → TEST=PARCIAL → OUTPUT_DIRETO=PENDING`. |

### PARAMETER_ID: `coliformes_totais`

| Campo | Registro |
| --- | --- |
| DISPLAY_NAME | Coliformes totais |
| CURRENT_VALUE_OR_RANGE | Máximo `0` |
| UNIT | `NMP/100 mL` |
| CURRENT_USE | Regra disponível no catálogo e executável pelo motor genérico quando o parâmetro é submetido; não foi localizado mapeamento na entrada operacional corrente de qualidade da água. |
| SOURCE | `UNVERIFIED_OR_NOT_LINKED` |
| SOURCE_VERSION | `PENDING_UNVERIFIED` |
| REQUIREMENT | PAC-01-005 requer fundamentação ambiental completa por contexto; nenhuma fonte originadora específica foi vinculada. |
| APPLICABILITY_CONTEXT | O catálogo declara `rural`, `urbano_saneamento`, `ambiental_rio`, `eta` e `ete`; aplicabilidade técnica: `SPECIALIST_AUTHORITY_REQUIRED`. |
| TECHNICAL_AUTHORITY | `SPECIALIST_AUTHORITY_REQUIRED` |
| VALIDATION_STATUS | `NOT_TECHNICALLY_VALIDATED` |
| CODE_REFERENCE | `data/monitoramento_hidrico_catalogo.json`, parâmetro `coliformes_totais`; `monitoramento_hidrico/avaliacao.py`, `AvaliacaoObservacionalService.avaliar`. |
| TEST_REFERENCE | `PENDING_UNVERIFIED` — nenhum teste numérico específico do limiar foi localizado. |
| NOTES | Critério registrado: “gatilho observacional conservador, sem carater legal”. Cadeia atual: `SOURCE/AUTHORITY=PENDING → REQUIREMENT=PARCIAL → RULE=REGISTRADA → CODE=GENÉRICO → TEST=PENDING → OUTPUT_DIRETO=PENDING`. |

### PARAMETER_ID: `e_coli`

| Campo | Registro |
| --- | --- |
| DISPLAY_NAME | E. coli |
| CURRENT_VALUE_OR_RANGE | Máximo `0` |
| UNIT | `NMP/100 mL` |
| CURRENT_USE | Regra disponível no catálogo e executável pelo motor genérico quando o parâmetro é submetido; não foi localizado mapeamento na entrada operacional corrente de qualidade da água. |
| SOURCE | `UNVERIFIED_OR_NOT_LINKED` |
| SOURCE_VERSION | `PENDING_UNVERIFIED` |
| REQUIREMENT | PAC-01-005 requer fundamentação ambiental completa por contexto; nenhuma fonte originadora específica foi vinculada. |
| APPLICABILITY_CONTEXT | O catálogo declara `rural`, `urbano_saneamento`, `ambiental_rio`, `eta` e `ete`; aplicabilidade técnica: `SPECIALIST_AUTHORITY_REQUIRED`. |
| TECHNICAL_AUTHORITY | `SPECIALIST_AUTHORITY_REQUIRED` |
| VALIDATION_STATUS | `NOT_TECHNICALLY_VALIDATED` |
| CODE_REFERENCE | `data/monitoramento_hidrico_catalogo.json`, parâmetro `e_coli`; `monitoramento_hidrico/avaliacao.py`, `AvaliacaoObservacionalService.avaliar`. |
| TEST_REFERENCE | `PENDING_UNVERIFIED` — nenhum teste numérico específico do limiar foi localizado. |
| NOTES | Critério registrado: “gatilho observacional conservador, sem carater legal”. Cadeia atual: `SOURCE/AUTHORITY=PENDING → REQUIREMENT=PARCIAL → RULE=REGISTRADA → CODE=GENÉRICO → TEST=PENDING → OUTPUT_DIRETO=PENDING`. |

## Pendências governadas

1. Identificar autoridade técnica especializada competente para cada contexto aplicável.
2. Registrar fontes candidatas sem promovê-las automaticamente a fontes válidas.
3. Submeter validade, versão, vigência e aplicabilidade de cada fonte à autoridade especializada.
4. Vincular requisitos tecnicamente autorizados aos parâmetros e contextos correspondentes.
5. Somente após validação especializada e decisão de implementação autorizada, avaliar alterações de regra, código e testes em operação separada.

Nenhuma pendência acima autoriza alteração de limiar, adoção de norma ou declaração de conformidade.

## Referências documentais existentes

- `data/monitoramento_hidrico_catalogo.json` — regras e metadados internos atualmente registrados, versão declarada do catálogo `GP-A11`.
- `monitoramento_hidrico/avaliacao.py` — execução determinística dos limites observacionais.
- `monitoramento_hidrico/quality_parameter_mapping.py` — mapeamento operacional corrente da entrada de qualidade da água.
- `tests/test_monitoramento_hidrico_avaliacao.py` — testes existentes para pH, turbidez e oxigênio dissolvido.
- `tests/test_monitoramento_hidrico_policy_engine.py` — teste parcial relacionado a cloro residual.
- `docs/pac/PAC_01_ENGINEERING_FINDINGS.md`, PAC-01-005 — fundamentação insuficiente dos limites observacionais.
- `docs/pac/PAC_02_ENGINEERING_SANITARY_FINDINGS.md`, PAC-02-016, PAC-02-017, PAC-02-018, PAC-02-022 e PAC-02-029 — contexto sanitário, validação técnica e matriz especializada ainda pendentes.

## Declaração de não promoção

Esta matriz não valida valores, não seleciona autoridade técnica, não interpreta normas, não cria requisito sanitário, não altera o catálogo e não promove componente experimental ao ICFACTORY.

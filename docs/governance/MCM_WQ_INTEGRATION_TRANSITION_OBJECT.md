# MCM-WQ — Integration Transition Object

Estado revisado em 2026-09-04 contra a baseline `62351f2dcdf1dcf753fe5e6fcbd8700e05a44af1`.

## Identidade, natureza e limites

- **Caso:** `PROTEUS`
- **Objeto:** `MCM_WQ_INTEGRATION_TRANSITION_OBJECT`
- **Natureza:** contrato governado da integração publicada e certificada
- **B5 técnico:** `CLOSED_AND_PUBLISHED`
- **B5 classificação:** `TECHNICALLY_CLOSED_WITH_DOCUMENTED_LIMITATIONS`
- **A5A:** `DEMONSTRATED_FOR_B5_TECHNICAL_SCOPE`
- **A5B:** `NOT_DEMONSTRATED`
- **B6:** `NOT_DEFINED`
- **B6 implementação:** `NOT_AUTHORIZED`
- **Cutover:** `NOT_AUTHORIZED`
- **Produção:** `NOT_READY`
- **Implementação deste objeto:** `CERTIFIED_AND_PUBLISHED`
- **Escopo do ato:** `BOUNDED_AUTHORITY_GATE_INTEGRATION`

Este documento define a fronteira governada para conectar a aplicabilidade de
authority B5 ao caminho temporal de avaliação. A realização de runtime está
publicada no Authority Gate certificado; este documento não altera schema, não
cria migration, não altera `record()`, não define B6 e não autoriza cutover ou
produção.

## Autoridade documental e disciplina de evidência

Este é o objeto governado canônico da transição em `docs/governance/`. Ele não
substitui os registros de certificação, a política de lifecycle, o contrato de
versão do Authority Gate, o Schema A ou o Schema B.

Fontes documentais e técnicas consideradas:

- `docs/governance/MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT.md`;
- `docs/governance/MCM_WQ_AUTHORITY_GATE_TECHNICAL_POLICY_VERSION_CONTRACT.md`;
- `docs/governance/MCM_WQ_AUTHORITY_ARTIFACT_VERIFICATION_SCHEMA_CONTRACT.md`;
- `docs/governance/MCM_WQ_EVALUATION_AUTHORITY_SNAPSHOT_SCHEMA_CONTRACT.md`;
- `docs/governance/MCM_WQ_B3_CERTIFICATION_RECORD.md`;
- `docs/governance/MCM_WQ_B4_CERTIFICATION_RECORD.md`;
- `docs/governance/MCM_WQ_B5_CERTIFICATION_RECORD.md`;
- `governed_core/evaluation_service.py`;
- `governed_core/authority_service.py`;
- `governed_core/rule_service.py`;
- `governed_core/repository.py`;
- `tests/test_governed_evaluation.py`;
- `tests/test_b5_authority_lifecycle.py`;
- migrations B5 `013`, `014`, `015`, `016` e migration 019.
- `docs/governance/MCM_WQ_LIFECYCLE_MATRIX_EVIDENCE_REGISTER.md`.

Disciplina de evidência:

- **PROVEN:** a baseline B5 demonstra, no escopo técnico publicado, a
  fundação de authority, applicability temporal, lifecycle, supersession
  atômica, enforcement temporal, timestamp governado e evidência rollback/
  fail-safe;
- **DOCUMENTED:** este registro define a integração futura, o resultado
  tipado, os reason codes, o limite transacional e a leitura de proveniência;
- **CERTIFIED_AND_PUBLISHED:** o Authority Gate integrado, a adaptação
  connection-aware e a persistência Schema B;
- **RECORDED_FROM_CONTROLLED_VALIDATION:** `58 PASS` focado e `347 PASS`
  completo, com Python `3.12.10` e runner `unittest`; esses resultados não
  são rerun por esta correção;
- **NOT_DEMONSTRATED:** testes, hashes, migrations, locators e comportamento
  de software não demonstram autoridade científica, legal, institucional,
  normativa ou de domínio. `A5B` permanece `NOT_DEMONSTRATED`.

## Bind obrigatório da política de lifecycle

O lifecycle technical admission do Authority Gate é regido explicitamente
por uma única política publicada:

~~~text
POLICY_ID::mcm-wq-authority-gate-technical-admission/v1
CANONICAL_POLICY_OBJECT::docs/governance/MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT.md
CANONICAL_POLICY_ROLE::PUBLISHED_LIFECYCLE_ADMISSIBILITY_POLICY_SOURCE_OF_TRUTH
POLICY_RESULT_DOMAIN::ELIGIBLE | INELIGIBLE | UNDEFINED
POLICY_RESULT_UNDEFINED::BLOCKED
MATRIX_NOT_DEFINED_CELLS::NONE
~~~

`MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT.md` é o Source of Truth
semântico da admissão técnica de lifecycle. A matriz publicada define as
consequências para as combinações de authority/applicability e os predicados
históricos exigidos; não existe, neste objeto de integração, uma lacuna
`NOT_DEFINED` de política para substituir essa matriz.

O resultado da política é calculado para uma candidatura única contra o
`measurement.measured_at` canônico. `ELIGIBLE` somente significa que todos os
predicados técnicos da política publicada foram positivamente provados;
`INELIGIBLE` e `UNDEFINED` bloqueiam. Nenhum resultado afirma validade
científica, legal, institucional, normativa ou de domínio.

Para a persistência Schema B, o resultado positivo da política é representado
pelo valor canônico exigido pelo Schema B:

~~~text
lifecycle_policy_decision::ELIGIBLE
lifecycle_policy_result::TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION
~~~

Essa representação não cria uma segunda política: `ELIGIBLE` é a decisão
tri-state da política publicada e `TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION`
é seu resultado positivo canônico no contrato do snapshot.

Os predicados devem usar `measured_at`, intervalos half-open `[start,end)` e
histórico completo de lifecycle/eventos. Estado corrente isolado, `created_at`,
`registered_at`, tempo de execução ou qualquer estado/política atual não pode
substituir a prova histórica. Se o histórico necessário estiver incompleto,
ambíguo ou não provado, o resultado da política é `UNDEFINED` e o Gate é
`BLOCKED`.

## Fronteira de integração

O escopo é somente o `evaluate_temporal()` integrado:

~~~text
MEASUREMENT
  -> temporal context resolution
  -> temporal APS resolution
  -> APS member authorization resolution
  -> AUTHORITY GATE
  -> RULE resolution
  -> final evaluation and Schema B persistence
~~~

O Authority Gate ocorre depois de contexto, APS temporal e autorização de
membro resolvidos e antes da resolução da RULE. `record()` permanece fora da
fronteira e inalterado. A medição factual continua distinta da avaliação e é
retida quando a fronteira bloqueia.

Entradas mínimas do Gate:

- `measurement_id`, `point_id` e lineage do ponto;
- `context_revision_id` imutável resolvido para `measured_at`;
- `parameter_reference`;
- `measured_at` canônico em UTC;
- proveniência da medição;
- identidade e versão do APS temporal resolvido;
- resultado da autorização temporal de membro;
- candidaturas de authority/applicability e suas evidências históricas e de
  verificação.

São proibidos como fallback `current_context`, `registration_time`,
`created_at`, estado corrente fora da janela medida, `rule_origin`,
applicability corrente, regra legada, seleção heurística, desempate silencioso
ou inferência de authority.

## GATE_RESULT_CONTRACT — resultado canônico tipado

O resultado do Authority Gate é exatamente uma união discriminada:

~~~text
AuthorityGateResult =
  RESOLVED {
    status: RESOLVED,
    authority_id,
    authority_version,
    authority_applicability_id,
    authority_lifecycle_event_id,
    authority_applicability_event_id,
    verification_id,
    authority_gate_policy_contract_version,
    lifecycle_policy_result: TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION,
    resolution_provenance,
    exact_member_authorization_basis: NONEMPTY_SET<APS_MEMBER_BASIS_ID>
  }
  |
  BLOCKED {
    status: BLOCKED,
    reason_code: GOVERNED_DETERMINISTIC_REASON_CODE,
    resolution_provenance: DIAGNOSTIC_PROVENANCE
  }
~~~

### `RESOLVED`

`RESOLVED` somente pode ser emitido quando houver exatamente uma candidatura
coerente, a política de lifecycle retornar `ELIGIBLE`, o policy identifier for
reconhecido, a applicability for temporalmente válida, os escopos e lineages
forem consistentes e houver verificação Schema A aceita para a mesma
authority/version.

`resolution_provenance` deve identificar, no mínimo, a policy id/version, o
`measured_at` avaliado, os inputs temporais, a candidatura selecionada, os
eventos históricos considerados, o estágio do resolvedor, a versão do
resolvedor e a base de autorização de membros. Esse campo não autoriza seleção
de vencedor: `RESOLVED` só existe após a cardinalidade única já estar provada.

`exact_member_authorization_basis` é um conjunto não vazio, exato e imutável
dos IDs de base de autorização de membro usados pela resolução. Não pode ser
reconstruído, reduzido ou enriquecido depois do fato.

### `BLOCKED`

`BLOCKED` sempre carrega um único `reason_code` governado e uma
`resolution_provenance` suficiente para diagnóstico, incluindo a medição,
inputs, contagem e IDs de candidaturas quando disponíveis, estágio que falhou,
referências de evidência e a regra aplicada.

O resultado `BLOCKED` não carrega campos de avaliação final, `evaluation_id`,
resultado de RULE ou qualquer payload de persistência Schema B. Não existe
snapshot, linha de base de membro ou outro fragmento de Schema B para um
resultado bloqueado. A medição factual é retida; nenhuma falha de authority é
convertida em `NAO_AVALIAVEL`.

## SCHEMA_B_MAPPING — mapeamento normativo

Para `RESOLVED`, a avaliação final e o snapshot são produzidos na mesma
transação. O mapeamento direto e obrigatório para os campos exatos do Schema B
é:

| Fonte governada | Campo Schema B | Regra normativa |
| --- | --- | --- |
| identidade da avaliação final criada no caminho integrado | `governed_evaluation_authority_snapshot.evaluation_id` | one-to-one com a avaliação; só existe em fluxo `RESOLVED` |
| `RESOLVED.authority_id` | `governed_evaluation_authority_snapshot.authority_id` | mesma authority identity/version validada |
| `RESOLVED.authority_version` | `governed_evaluation_authority_snapshot.authority_version` | versão imutável da authority resolvida |
| `RESOLVED.authority_applicability_id` | `governed_evaluation_authority_snapshot.authority_applicability_id` | applicability histórica resolvida |
| `RESOLVED.authority_lifecycle_event_id` | `governed_evaluation_authority_snapshot.authority_lifecycle_event_id` | evento histórico de lifecycle considerado |
| `RESOLVED.authority_applicability_event_id` | `governed_evaluation_authority_snapshot.authority_applicability_event_id` | evento histórico de applicability considerado |
| `RESOLVED.verification_id` | `governed_evaluation_authority_snapshot.verification_id` | único handoff para prova Schema A aceita |
| `RESOLVED.status` | `governed_evaluation_authority_snapshot.authority_gate_status` | invariavelmente `RESOLVED` |
| `RESOLVED.lifecycle_policy_result` | `governed_evaluation_authority_snapshot.lifecycle_policy_result` | invariavelmente `TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION` |
| resultado da RULE após Gate resolvido | `governed_evaluation_authority_snapshot.rule_resolution_outcome` | somente `ZERO_APPLICABLE_RULE` ou `ONE_APPLICABLE_RULE` |
| `RESOLVED.authority_gate_policy_contract_version` | `governed_evaluation_authority_snapshot.authority_gate_policy_contract_version` | exatamente `mcm-wq-authority-gate-technical-admission/v1` |

Invariantes do mapeamento:

~~~text
authority_gate_status == RESOLVED
rule_resolution_outcome == ZERO_APPLICABLE_RULE
  | ONE_APPLICABLE_RULE
exact_member_authorization_basis cardinality >= 1
~~~

`exact_member_authorization_basis` é persistido somente na relação filha
imutável de bases do snapshot, com um ou mais IDs exatos por snapshot. Ele não
é uma nova coluna direta nem pode ser substituído por reconstrução live.
`resolution_provenance` é satisfeita pelas referências relacionais imutáveis
do snapshot, pelas linhas de base e pelo encadeamento Schema A; não se adiciona
campo Schema B, JSON concorrente ou duplicação de locator/hash.

Um resultado `BLOCKED` não entra neste mapeamento e não produz nenhum payload
Schema B. Avaliações legadas continuam sem snapshot e não recebem backfill.

## CONNECTION_OWNERSHIP_CONTRACT — uma conexão e uma transação

O `evaluate_temporal()` integrado deve possuir uma única conexão governada e
uma única transação desde antes da resolução do contexto temporal até o
`COMMIT` final:

~~~text
ONE governed connection
ONE transaction
NO nested connection
NO intermediate commit
NO _optional_connection(None) inside the integrated path
~~~

A mesma conexão explícita deve ser passada, sem substituição ou reabertura,
para:

~~~text
temporal context resolution
 -> temporal APS resolution
 -> member authorization resolution
 -> Authority Gate
 -> rule resolution
 -> evaluation persistence
 -> all snapshot basis rows
 -> snapshot persistence
 -> final validation
 -> COMMIT
~~~

O serviço integrado é o dono da conexão e da transação. Repositórios e
serviços chamados nessa cadeia não podem abrir conexão própria, iniciar
transação aninhada, chamar `_optional_connection(None)` ou fazer commit
intermediário. APIs connection-aware podem ser adaptadas somente na medida
necessária para transmitir essa mesma conexão e preservar a fronteira.

Em `RESOLVED + ZERO_APPLICABLE_RULE` e `RESOLVED + ONE_APPLICABLE_RULE`, a
avaliação final, todas as linhas de base não vazias, o snapshot completo e a
validação final pertencem à mesma transação; o commit é atômico. Falha antes
do commit faz rollback sem avaliação final parcial, snapshot parcial ou base
parcial. `record()` permanece inalterado e fora dessa transação integrada.

## RUNTIME_SEMANTICS — comportamento futuro obrigatório

### Authority bloqueada

~~~text
AUTHORITY_BLOCKED
  -> factual measurement retained
  -> no final evaluation
  -> no Schema B snapshot
  -> no Schema B snapshot basis
~~~

Não há `NOT_EVALUABLE`, alerta, evento, ação, fallback ou seleção heurística
nesse ramo.

### Authority resolvida, zero RULE aplicável

~~~text
RESOLVED + ZERO_APPLICABLE_RULE
  -> NAO_AVALIAVEL
  -> final evaluation persisted
  -> complete nonempty exact basis set persisted
  -> complete Schema B snapshot persisted
  -> atomic COMMIT
~~~

`NAO_AVALIAVEL` é válido somente depois de `authority_gate_status == RESOLVED`
e somente para `ZERO_APPLICABLE_RULE`.

### Authority resolvida, uma RULE aplicável

~~~text
RESOLVED + ONE_APPLICABLE_RULE
  -> final evaluation persisted
  -> complete nonempty exact basis set persisted
  -> complete Schema B snapshot persisted
  -> atomic COMMIT
~~~

Mais de uma RULE aplicável resulta em `BLOCKED`, sem avaliação final, snapshot
ou base. A authority não é uma RULE, uma RULE não é uma medição e uma RULE
existente não é automaticamente a RULE aplicável.

## BLOCKED_REASON_CODE_CONTRACT — categorias determinísticas

O Gate emite exatamente um reason code por resultado `BLOCKED`. A classificação
é fail-safe, determinística e auditável. A ordem de decisão abaixo é fixa: a
primeira condição determinável na etapa aplicável define o código; nenhum
código genérico pode mascarar uma categoria específica.

| Ordem | `reason_code` | Condição governada |
| --- | --- | --- |
| 1 | `NO_AUTHORITY_CANDIDATE` | nenhuma candidatura foi encontrada para o contexto, parâmetro e `measured_at` |
| 2 | `CONFLICTING_AUTHORITY` | duas ou mais candidaturas, identidade, escopo, lifecycle ou proveniência são mutuamente incompatíveis |
| 3 | `MULTIPLE_AUTHORITY_CANDIDATES` | mais de uma candidatura coerente existe e não há política B6 de seleção |
| 4 | `MALFORMED_AUTHORITY_STATE` | estado, identidade, versão, evento ou estrutura da authority é inválido/malformado |
| 5 | `INCOMPLETE_AUTHORITY_HISTORY` | histórico de lifecycle/applicability exigido para `measured_at` está ausente, incompleto ou ambíguo |
| 6 | `APPLICABILITY_INVALID` | applicability ausente, inválida, inconsistente ou fora da janela temporal half-open |
| 7 | `AUTHORITY_SCOPE_MISMATCH` | authority, applicability, contexto, parâmetro ou lineage não coincidem |
| 8 | `UNKNOWN_POLICY_VERSION` | o policy identifier não é reconhecido exatamente; não há fallback para latest |
| 9 | `MISSING_VERIFICATION` | não existe `verification_id`/prova Schema A para a mesma authority/version |
| 10 | `VERIFICATION_NOT_ACCEPTED` | a prova existe, mas não tem resultado aceito ou falha em identidade/integridade |
| 11 | `LIFECYCLE_INELIGIBLE` | a política canônica retorna `INELIGIBLE` para a candidatura histórica |
| 12 | `LIFECYCLE_UNDEFINED` | a política canônica retorna `UNDEFINED` por prova insuficiente ou não resolvível |
| 13 | `TEMPORAL_CONTEXT_UNRESOLVED` | contexto temporal não foi resolvido de modo único e válido |
| 14 | `APS_MEMBER_AUTHORIZATION_UNRESOLVED` | APS temporal ou autorização de membro não foi resolvida de modo válido |
| 15 | `MULTIPLE_APPLICABLE_RULES` | a resolução posterior da RULE encontrou mais de uma RULE aplicável |
| 16 | `INTERNAL_RESOLUTION_FAILURE` | falha inesperada sem categoria específica determinável; permanece `BLOCKED` |

`CONFLICTING_AUTHORITY` é avaliado antes de
`MULTIPLE_AUTHORITY_CANDIDATES` quando a incompatibilidade material é
determinável. `MULTIPLE_AUTHORITY_CANDIDATES` não escolhe vencedor; ele se
aplica ao conjunto múltiplo coerente sem política B6 de seleção. Isso é
diagnóstico, não adjudicação B6. `MISSING_VERIFICATION` e
`VERIFICATION_NOT_ACCEPTED` somente se aplicam após a candidatura única estar
identificada.

Os códigos `LIFECYCLE_INELIGIBLE` e `LIFECYCLE_UNDEFINED` são a tradução
normativa dos resultados da política publicada. Em particular:

~~~text
policy_result::INELIGIBLE -> LIFECYCLE_INELIGIBLE -> BLOCKED
policy_result::UNDEFINED  -> LIFECYCLE_UNDEFINED  -> BLOCKED
~~~

Nenhum estado corrente `REVOKED` ou `SUPERSEDED`, isoladamente, decide a
admissibilidade histórica. A política canônica deve provar a terminalidade em
relação a `measured_at`; caso contrário, o resultado é `UNDEFINED`.

## POST_COMMIT_PROVENANCE_CONTRACT — prova histórica

Depois do commit, toda leitura de proveniência de uma avaliação governada deve
partir daquilo que foi persistido:

~~~text
immutable Schema B snapshot
  -> immutable exact member-basis rows
  -> verification_id
  -> accepted immutable Schema A verification evidence
  -> authority/artifact binding and artifact/hash/locator evidence
~~~

O `verification_id` é o único handoff do Schema B para o Schema A. Evidência
de artifact, hash e locator deve ser alcançada por esse encadeamento; Schema B
não duplica locator, bytes, digest, algoritmo, `verified_at` ou versão do
contrato de verificação.

Não é permitido reconstruir a prova histórica consultando authority,
applicability, lifecycle, APS ou relações live atuais, nem substituir o
snapshot persistido por uma projeção corrente. A base exata de autorização de
membros também não pode ser refeita de relações live. A leitura deve tolerar
que o estado/política atual seja diferente do estado que foi persistido.

## Falhas, atomicidade e invariantes preservadas

- `MEASUREMENT != EVALUATION`;
- `RULE != MEASUREMENT`;
- `CONFIGURATION != AUTHORITY`;
- `APPLICABLE_RULE != ANY_EXISTING_RULE`;
- `EVALUATION != ALERT`;
- `NO_APPLICABLE_RULE => VALID_MEASUREMENT + NOT_EVALUABLE` somente após
  authority `RESOLVED`;
- `MULTIPLE_APPLICABLE_RULES => BLOCKED`;
- `AUTHORITY_FAILURE => BLOCKED`, nunca `NOT_EVALUABLE`;
- medição factual retida em todo bloqueio;
- bloqueio não cria avaliação, snapshot ou basis rows;
- resultado resolvido exige basis set completo, exato e não vazio;
- `authority_gate_status == RESOLVED` em toda linha Schema B;
- `A5A=DEMONSTRATED_FOR_B5_TECHNICAL_SCOPE` não promove A5B;
- `A5B=NOT_DEMONSTRATED` permanece inalterado.

Não há efeito colateral de `ALERT`, `EVENT`, `ACTION`, GEO ou ação autônoma
em qualquer ramo deste objeto.

## Limites reservados para B6 e A5B

Este objeto não define precedência, adjudicação, seleção de vencedor,
resolução de conflito entre authorities, promoção de authority, validade
científica/legal/institucional/normativa ou qualquer outro B6. Ele somente
detecta condições incompatíveis e bloqueia sem escolher.

~~~text
B6_STATUS::NOT_DEFINED
B6_IMPLEMENTATION_AUTHORIZED::NO
A5B_STATUS::NOT_DEMONSTRATED
~~~

Também permanecem fora do escopo: GEO, cutover, readiness de produção,
remoção de legacy, alert/event/action e qualquer ação autônoma.

## Preservações obrigatórias

Esta correção documental preserva, sem alteração:

- `record()`;
- migration 019, inalterada;
- Schema A, inalterado;
- Schema B, inalterado;
- `A5B::NOT_DEMONSTRATED`;
- `B6::NOT_DEFINED`;
- ausência de GEO, cutover, alert/event/action e ação autônoma;
- ausência de backfill ou duplicação de locator/hash em Schema B;
- ausência de autorização para runtime, migration, schema, teste ou commit.

~~~text
MIGRATION_019_UNCHANGED::YES
SCHEMA_A_UNCHANGED::YES
SCHEMA_B_UNCHANGED::YES
GEO::NOT_IN_SCOPE
CUTOVER::NOT_AUTHORIZED
ALERT_EVENT_ACTION::NOT_IN_SCOPE
AUTONOMOUS_ACTION::NOT_IN_SCOPE
~~~

## Evidência requerida antes de implementação

Antes de qualquer autorização de runtime, uma auditoria independente futura
deve verificar, no mínimo:

- bind exato à policy id publicada e reconhecimento sem fallback;
- aplicação da matriz canônica para `ELIGIBLE`, `INELIGIBLE` e `UNDEFINED`;
- tipagem exclusiva `RESOLVED|BLOCKED` e ausência de payload Schema B em
  bloqueio;
- campos obrigatórios do resultado resolvido e base de membros não vazia,
  completa e exata;
- mapeamento integral aos onze campos diretos do Schema B e às linhas filhas;
- `authority_gate_status == RESOLVED` e outcomes de RULE restritos a zero ou
  uma;
- uma única conexão, uma única transação, ausência de conexão aninhada,
  commit intermediário e `_optional_connection(None)` na cadeia integrada;
- atomicidade de avaliação, snapshot, basis rows e rollback;
- retenção da medição e ausência de avaliação/snapshot/basis em todo bloqueio;
- leitura pós-commit a partir do snapshot/basis persistidos e travessia
  `verification_id -> Schema A`;
- não substituição por estado live, não duplicação de hash/locator e não uso
  de JSON como SSoT relacional;
- reason codes determinísticos, específicos e auditáveis;
- preservação de `record()`, migration 019, Schema A/B, B6 e A5B;
- ausência de efeitos alert/event/action/GEO/cutover/autonomous action.

Os resultados B5 `58 PASS` e `347 PASS` continuam evidência registrada de um
ciclo controlado anterior. Esta correção não executa testes e não reivindica
reprodutibilidade do ambiente histórico.

## Saída de validação da revisão

### STATUS

`REVISED_DOCUMENTARY_CONTRACT`

### FILES_CHANGED

`docs/governance/MCM_WQ_INTEGRATION_TRANSITION_OBJECT.md`

### LIFECYCLE_POLICY_BINDING

`mcm-wq-authority-gate-technical-admission/v1` vinculado explicitamente a
`docs/governance/MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT.md`, que é o
Source of Truth publicado. A matriz publicada é a única fonte da decisão de
admissão de lifecycle;
`MATRIX_NOT_DEFINED_CELLS::NONE` é preservado.

### GATE_RESULT_CONTRACT

Resultado canônico tipado `RESOLVED|BLOCKED`, com os campos obrigatórios,
proveniência diagnóstica, conjunto exato não vazio de bases em `RESOLVED` e
firewall sem avaliação/payload Schema B em `BLOCKED`.

### SCHEMA_B_FIELD_MAPPING

Os campos `evaluation_id`, `authority_id`, `authority_version`,
`authority_applicability_id`, `authority_lifecycle_event_id`,
`authority_applicability_event_id`, `verification_id`,
`authority_gate_status`, `lifecycle_policy_result`,
`rule_resolution_outcome` e `authority_gate_policy_contract_version` estão
mapeados normativamente aos campos homônimos do snapshot governado, sem
alteração de Schema B.

### CONNECTION_OWNERSHIP_CONTRACT

`evaluate_temporal()` integrado possui uma conexão, uma transação, sem conexão
aninhada, sem commit intermediário e sem `_optional_connection(None)`; a mesma
conexão percorre toda a cadeia até validação final e commit.

### BLOCKED_REASON_CODE_CONTRACT

Categorias determinísticas incluem `NO_AUTHORITY_CANDIDATE`,
`MULTIPLE_AUTHORITY_CANDIDATES`, `CONFLICTING_AUTHORITY`,
`LIFECYCLE_INELIGIBLE`, `LIFECYCLE_UNDEFINED`, `APPLICABILITY_INVALID`,
`AUTHORITY_SCOPE_MISMATCH`, `MISSING_VERIFICATION`,
`VERIFICATION_NOT_ACCEPTED`, `UNKNOWN_POLICY_VERSION`,
`MALFORMED_AUTHORITY_STATE` e `INCOMPLETE_AUTHORITY_HISTORY`, além das falhas
de contexto/APS/RULE e do catch-all fail-safe.

### POST_COMMIT_PROVENANCE_CONTRACT

A proveniência pós-commit parte do snapshot Schema B imutável e das basis rows;
artifact/hash/locator são alcançados por `verification_id` e Schema A. Não há
reconstrução live nem duplicação de locator/hash em Schema B.

### MATERIAL_FINDINGS_CLOSED

- bind ausente à política canônica: fechado com `POLICY_ID` e caminho SSoT
  explícitos;
- classificação de elegibilidade: fechada pela matriz publicada e pelo
  tri-state `ELIGIBLE|INELIGIBLE|UNDEFINED`;
- resultado do Gate não tipado: fechado pela união `RESOLVED|BLOCKED`;
- campos obrigatórios e base exata não definidos: fechados no contrato e no
  mapeamento Schema B;
- bloqueio sem firewall de persistência: fechado com ausência explícita de
  avaliação, snapshot e basis rows;
- posse de conexão/transação implícita: fechada pela sequência e pelas
  proibições de conexão aninhada/commit intermediário;
- reason codes não determinísticos: fechados pela taxonomia e ordem fixa;
- proveniência histórica pós-commit ambígua: fechada pelo snapshot/basis e
  handoff exclusivo `verification_id -> Schema A`.

### MINOR_FINDINGS_CLOSED

- nomenclatura e valores de policy/lifecycle alinhados aos contratos
  publicados;
- zero/uma RULE e `NAO_AVALIAVEL` explicitamente condicionados a authority
  `RESOLVED`;
- cardinalidade não vazia e imutabilidade da base de membros explicitadas;
- preservações de `record()`, migration 019, Schema A/B, B6, A5B e limites
  de escopo repetidas no ponto de validação;
- ausência de fallback, heurística, backfill, JSON concorrente e duplicação
  de hash/locator explicitada.

### UNRESOLVED_DECISIONS

Nenhuma decisão crítica de integração permanece implícita neste objeto
documental. Permanecem deliberadamente fora deste escopo e não são resolvidas
por ele: implementação futura, B6/precedência/adjudicação, A5B, validade de
domínio, GEO, alert/event/action, cutover, produção e remoção de legacy.

### SCOPE_AUDIT

`DOCUMENTARY_CORRECTION_ONLY::PASS`

Somente este arquivo é permitido como mudança. Runtime, testes, migrations,
records, schemas, `scratch/`, commit e push não fazem parte da operação.

### QUALITY_GATE

`PASS_DOCUMENTARY_SCOPE`

Critérios atendidos: findings materiais e menores documentados como fechados;
bind de lifecycle explícito; consistência declarada com Schema A/B; contrato de
conexão atômica; reason codes fail-safe; proveniência histórica pós-commit; e
firewalls A5B/B6/escopo preservados.

### NEXT_OPERATION

`GEO_DOCUMENTARY_RESEARCH_AND_SEMANTIC_MODEL`

## Gate de governança

~~~text
TRANSITION_OBJECT_STATUS::CERTIFIED_AND_PUBLISHED
IMPLEMENTATION_AUTHORIZED::YES_SCOPED_CERTIFIED_GATE
MIGRATION_CREATION_AUTHORIZED::NO
SCHEMA_CHANGE_AUTHORIZED::NO
TEST_CHANGE_AUTHORIZED::NO
COMMIT_AUTHORIZED::NO
PUSH_AUTHORIZED::NO
CUTOVER_AUTHORIZED::NO
GEO_IMPLEMENTATION_AUTHORIZED::NO
ALERT_EVENT_ACTION_AUTHORIZED::NO
A5B_STATUS::NOT_DEMONSTRATED
B6_STATUS::NOT_DEFINED
READY_FOR_INDEPENDENT_REAUDIT::YES
~~~

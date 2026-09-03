# MCM-WQ — Integration Transition Object

Estado de definição em 2026-09-03, contra a publicação `1e27a672e40b414e6c7b568e401eba55ce7d5e6b` e a baseline técnica B5 `c13593f3665f425ada833fe6c0ceb225136ec5e3`.

## Identidade e classificação

- **Caso:** `PROTEUS`
- **Objeto:** `MCM_WQ_INTEGRATION_TRANSITION_OBJECT`
- **Natureza:** contrato governado documental para futura integração
- **B5 técnico:** `CLOSED_AND_PUBLISHED`
- **B5 classificação:** `TECHNICALLY_CLOSED_WITH_DOCUMENTED_LIMITATIONS`
- **A5A:** `DEMONSTRATED_FOR_B5_TECHNICAL_SCOPE`
- **A5B:** `NOT_DEMONSTRATED`
- **B6:** `NOT_DEFINED`
- **B6 implementação:** `NOT_AUTHORIZED`
- **Cutover:** `NOT_AUTHORIZED`
- **Produção:** `NOT_READY`
- **Implementação deste objeto:** `NOT_AUTHORIZED`

Este documento define a menor fronteira governada necessária para conectar a aplicabilidade de autoridade B5 ao caminho temporal de avaliação. Ele não implementa runtime, não altera schema, não define B6 e não constitui autorização de cutover ou produção.

## Autoridade documental e disciplina de evidência

Este é um objeto governado canônico em `docs/governance/`, seguindo a estrutura dos registros MCM-WQ B3, B4 e B5. É uma definição de transição e não substitui os registros de certificação nem cria uma segunda fonte de verdade técnica.

As referências de evidência são:

- `docs/governance/MCM_WQ_B3_CERTIFICATION_RECORD.md`
- `docs/governance/MCM_WQ_B4_CERTIFICATION_RECORD.md`
- `docs/governance/MCM_WQ_B5_CERTIFICATION_RECORD.md`
- `governed_core/evaluation_service.py`
- `governed_core/authority_service.py`
- `governed_core/rule_service.py`
- `governed_core/repository.py`
- `governed_core/measurement_models.py`
- `tests/test_governed_evaluation.py`
- `tests/test_b5_authority_lifecycle.py`
- `migrations/011_mcm_wq_b3_evaluation_provenance.sql`
- `migrations/013_mcm_wq_b5_authority_foundation.sql`
- `migrations/014_mcm_wq_b5_authority_applicability.sql`
- `migrations/015_mcm_wq_b5_deferred_successor_fk.sql`
- `migrations/016_mcm_wq_b5_db_temporal_enforcement.sql`

Classificação das afirmações:

- **PROVEN:** a baseline B5 publicada demonstra, no escopo técnico certificado, a fundação de autoridade, aplicabilidade temporal, lifecycle, supersession atômica, enforcement temporal, timestamp governado e evidência rollback/fail-safe.
- **DOCUMENTED:** este documento define a fronteira, contratos e obrigações da transição futura.
- **RECORDED_FROM_CONTROLLED_VALIDATION:** os resultados `58 PASS` focado e `347 PASS` completo, com Python `3.12.10` e runner `unittest`, permanecem evidência registrada no ciclo controlado B5; não são rerun desta definição.
- **INFERRED:** a posição do gate é derivada da sequência atual de `evaluate_temporal()` e da API B5 existente; a integração ainda não foi implementada.
- **NOT_DEMONSTRATED:** testes, hashes, migrations, locators e comportamento de software não demonstram autoridade científica, legal, institucional ou normativa de domínio. `A5B` permanece `NOT_DEMONSTRATED`.
- **NOT_DEFINED:** B6, política de precedência/adjudicação de conflitos e semântica de alert/event/action.

As limitações B5 permanecem preservadas: `TERMINAL_OVERLAP_LIMITATION`, `MIGRATION_011_PROVENANCE_LIMITATION`, `HISTORICAL_ENVIRONMENT_REPRODUCIBILITY_LIMITATION` e `A5B_NOT_DEMONSTRATED`.

## Semântica de lifecycle e elegibilidade

### Fonte publicada

As migrations B5 `013`, `014` e `015` e a evidência em `tests/test_b5_authority_lifecycle.py` demonstram:

- `authority_state` possui os estados `PUBLISHED`, `ACTIVE`, `REVOKED` e `SUPERSEDED`;
- a transição de autoridade é `PUBLISHED → ACTIVE → REVOKED|SUPERSEDED`;
- `authority_applicability_state` possui `ACTIVE`, `REVOKED` e `SUPERSEDED`;
- a publicação de uma applicability produz estado `ACTIVE`;
- revocation/supersession fecha a janela temporal half-open da applicability e não permite reopen;
- a resolução B5 usa a janela temporal da applicability.

O teste B5 de criação e resolução cria a autoridade em `PUBLISHED`, cria uma applicability que fica `ACTIVE` e demonstra resolução temporal dessa applicability. Isso prova o comportamento de lifecycle e de janela temporal, mas não define se `PUBLISHED` ou `ACTIVE` da autoridade é admissível para uma avaliação futura.

`LIFECYCLE_ELIGIBILITY_STATUS::NOT_DEFINED`

Não há na autoridade B5 publicada uma matriz explícita de admissibilidade da autoridade para avaliação. O nome do estado, isoladamente, nunca constitui validade científica, legal, institucional ou de domínio.

### Matriz de estado

| Registro | Estado observado | O que B5 prova | Admissibilidade no futuro authority gate |
| --- | --- | --- | --- |
| Authority | `PUBLISHED` | Estado inicial e usado no teste B5 de resolução da applicability | `NOT_DEFINED`; não pode passar sem elegibilidade definida |
| Authority | `ACTIVE` | Transição de lifecycle permitida | `NOT_DEFINED`; não pode passar sem elegibilidade definida |
| Authority | `REVOKED` | Estado terminal e evento append-only | `NOT_DEFINED`; o nome do estado atual sozinho não decide admissibilidade histórica |
| Authority | `SUPERSEDED` | Estado terminal e sucessão governada | `NOT_DEFINED`; o nome do estado atual sozinho não decide admissibilidade histórica |
| Applicability | `ACTIVE` | Candidatura temporal resolvível quando a janela inclui `measured_at` | Candidatura identificada; admissibilidade final da authority permanece `NOT_DEFINED` |
| Applicability | `REVOKED` | Janela fechada a partir de `terminal_effective_at` | Fora da janela após o terminal; admissibilidade histórica anterior não é decidida aqui |
| Applicability | `SUPERSEDED` | Janela fechada e sucessor vinculado | Fora da janela após o terminal; admissibilidade histórica anterior não é decidida aqui |

`UNDEFINED_OR_UNPROVEN_ELIGIBILITY => BLOCKED`

`CURRENT_STATE_NAME_ALONE MUST NOT DETERMINE HISTORICAL ADMISSIBILITY`

A elegibilidade histórica da authority deve ser resolvida contra `measured_at`, o intervalo temporal aplicável, o histórico de lifecycle/eventos e uma política de admissibilidade de lifecycle definida separadamente. Não se infere se uma authority `PUBLISHED`, `ACTIVE`, `REVOKED` ou `SUPERSEDED` é admissível para um evento histórico.

Os eventos terminais da applicability podem fechar seus intervalos temporais nos pontos já provados por B5. Esse fechamento temporal não constitui, sozinho, uma política completa de admissibilidade da authority para avaliação.

Antes de qualquer autorização de runtime, uma decisão governada separada deve definir a elegibilidade técnica do par authority/applicability, inclusive sua relação com `measured_at`. Essa decisão não pode ser inferida deste documento nem tratada como política de precedência ou adjudicação B6.

## Cadeia governada atual e fronteira da transição

O caminho temporal atualmente evidenciado é:

`MEASUREMENT → APPLICABLE_CONTEXT/APS → APS_MEMBER_AUTHORIZATION → RULE_RESOLUTION → EVALUATION`

A capacidade B5 de resolução de aplicabilidade de autoridade existe separadamente e não é chamada pelo caminho atual de `evaluate_temporal()`. A transição definida neste documento acrescenta conceitualmente, antes da resolução da RULE:

`MEASUREMENT → APPLICABLE_CONTEXT → AUTHORITY_APPLICABILITY_GATE → APPLICABLE_RULE → EVALUATION`

O escopo é exclusivamente `evaluate_temporal()`:

- o gate ocorre depois da resolução exata do contexto temporal, APS temporal e autorização de membro;
- o gate ocorre antes da resolução da RULE;
- o gate ocorre antes da construção e persistência de uma avaliação final;
- `record()` permanece fora do escopo e não deve ser alterado por esta definição;
- a medição factual continua distinta da avaliação e permanece preservada quando o caminho é bloqueado.

## Contrato de entrada

O gate deve receber os dados já resolvidos do evento de medição, contexto e autorização temporal:

- `measurement_id`;
- `point_id` e demais dados de lineage do ponto;
- `context_revision_id` imutável, resolvido para `measured_at`;
- `parameter_reference`;
- `measured_at` canônico em UTC;
- proveniência da medição;
- identidade e versão do APS temporal resolvido;
- resultado da autorização `APS_MEMBER` temporal.

O valor factual da medição permanece dado da `MEASUREMENT`; ele não é usado para selecionar autoridade, RULE ou resultado de avaliação.

### Entradas proibidas como fallback

O gate não pode substituir os inputs acima por:

- `current_context`;
- `registration_time` ou `created_at`;
- estado atual do APS fora da janela de `measured_at`;
- `rule_origin`;
- aplicabilidade corrente, regra legada ou qualquer fallback;
- seleção heurística, desempate silencioso ou inferência de autoridade.

## Contrato de resolução de autoridade

O input mínimo da resolução B5 é:

`context_revision_id + parameter_reference + canonical measured_at`

O resultado governado deve ser tipado como `RESOLVED` ou `BLOCKED` e conter:

- `status`;
- `reason_code`;
- `candidate_count`;
- `candidate_ids`;
- `selected_applicability_id`, somente quando houver exatamente uma correspondência válida;
- `authority_id` e `authority_version`;
- intervalo temporal aplicável;
- estado de lifecycle observado e estado elegível exigido;
- `origin_locator`;
- `content_hash`;
- `resolution_provenance` e versão do resolvedor.

Campos de autoridade selecionada não podem ser tratados como resolvidos quando o resultado for `BLOCKED`. Candidatos e razão do bloqueio devem ser preservados para evidência.

O gate de autoridade nunca emite `NOT_EVALUABLE`. `NOT_EVALUABLE` pertence somente à resolução de RULE após uma autoridade ter sido resolvida com sucesso.

## Taxonomia transitional de reason codes

Na futura fronteira de integração, qualquer exceção ou resultado não resolvido do resolver deve ser convertido em um resultado determinístico `BLOCKED` com um reason code estável. O `ValueError` genérico atual não pode vazar como semântica governada.

Os códigos mínimos, alinhados ao padrão uppercase e descritivo já usado pela resolução de RULE, são:

- `AUTHORITY_ZERO_MATCH` — nenhuma candidatura de autoridade;
- `AUTHORITY_MULTIPLE_MATCH` — mais de uma candidatura sem resolução única;
- `AUTHORITY_MALFORMED` — registro ou input de autoridade malformado;
- `AUTHORITY_OUT_OF_WINDOW` — `measured_at` fora do intervalo aplicável;
- `AUTHORITY_LIFECYCLE_INELIGIBLE` — lifecycle explicitamente classificado como inelegível pela política separada;
- `AUTHORITY_PROVENANCE_INCOMPLETE_OR_INVALID` — provenance, locator ou hash ausente/inconsistente;
- `AUTHORITY_CONFLICT_DETECTED` — conflito detectado sem adjudicação;
- `AUTHORITY_ELIGIBILITY_NOT_DEFINED_OR_UNPROVEN` — elegibilidade não definida ou não provada;
- `AUTHORITY_RESOLUTION_UNEXPECTED_FAILURE` — falha inesperada do resolver sem categoria mais específica.

`AUTHORITY_RESOLUTION_UNEXPECTED_FAILURE` significa:

- falha inesperada do resolver `=> BLOCKED`;
- medição factual retida;
- nenhuma avaliação final persistida no futuro caminho integrado de `evaluate_temporal()`;
- evidência diagnóstica retida;
- nenhuma exceção genérica exposta como resultado governado;
- nenhum fallback;
- nenhuma seleção heurística.

O catch-all não pode substituir um reason code específico quando uma categoria governada for determinável. A tradução é requisito documental para a futura fronteira de integração; não está implementada neste estado.

Esta taxonomia não define precedência, adjudicação ou vencedor.

## Semântica por cardinalidade e falha

### Zero correspondências de autoridade

`ZERO_AUTHORITY_MATCH => VALID_MEASUREMENT + BLOCKED`

A medição permanece disponível; nenhuma avaliação final é persistida. Isso não é `NO_APPLICABLE_RULE`.

### Uma correspondência válida

`ONE_VALID_AUTHORITY_MATCH => RESOLVED`

A resolução só é válida se o escopo de contexto e parâmetro coincidir, `measured_at` estiver dentro do intervalo, o lifecycle for elegível e a identidade/proveniência da autoridade estiverem completas. Somente depois disso a resolução de RULE pode ocorrer.

### Múltiplas ou conflitantes

`MULTIPLE_OR_CONFLICTING_AUTHORITY => BLOCKED`

O transition object pode detectar candidatos múltiplos, sobreposição ou conflito e bloquear o caminho. Ele não seleciona vencedor, não aplica precedência e não adjudica o conflito.

### Outras falhas

Cada condição abaixo resulta em `BLOCKED`, sem fallback:

- autoridade ausente;
- autoridade malformada;
- intervalo inválido ou `measured_at` fora da janela;
- lifecycle explicitamente classificado como inelegível pela política separada;
- elegibilidade histórica não resolvível contra `measured_at`, intervalo temporal, histórico de eventos e política governada;
- referência, locator ou hash ausente/inconsistente;
- contexto temporal, APS ou autorização de membro não resolvidos;
- conflito entre a proveniência da medição, contexto, autoridade ou RULE;
- falha inesperada do resolver sem categoria mais específica.

Em todas as falhas, a medição factual permanece no bloco. Não há avaliação final, alerta, evento ou ação.

## Semântica após autoridade resolvida

Somente após `AUTHORITY_STATUS=RESOLVED`:

- `ZERO_APPLICABLE_RULE => VALID_MEASUREMENT + NOT_EVALUABLE`;
- `ONE_APPLICABLE_RULE => MAY_PROCEED_TO_EVALUATION`;
- `MULTIPLE_APPLICABLE_RULES => BLOCKED`.

A autoridade não é uma RULE, a RULE não é uma medição e uma RULE existente não é automaticamente a RULE aplicável. A resolução da RULE continua responsável por sua própria cardinalidade, referências e hash.

## Contrato de persistência

- A `MEASUREMENT` é persistida e permanece imutável quando o gate bloqueia.
- Para o futuro caminho integrado de `evaluate_temporal()`, nenhuma avaliação final existe antes de `AUTHORITY_STATUS=RESOLVED`.
- Para o futuro caminho integrado de `evaluate_temporal()`, nenhuma avaliação final é persistida em `AUTHORITY_STATUS=BLOCKED`.
- `record()` permanece fora deste transition object e inalterado; este contrato não implica que seu comportamento atual esteja submetido ao futuro authority gate.
- Uma avaliação bem-sucedida retém snapshot da aplicabilidade e da autoridade, intervalo temporal, lifecycle, locator, hash e proveniência da resolução.
- A proveniência de transição pode usar uma forma documentada em `explanation_data`, caso essa seja a decisão de implementação futura.
- Os campos adicionados pela migration 011 não devem ser apresentados como proveniência first-class completa; o caminho atual não demonstra seu preenchimento integral.
- A persistência deve ser atômica: falha após a resolução não pode deixar avaliação final parcial nem alterar a medição.
- Nenhum efeito colateral de `ALERT`, `EVENT` ou `ACTION` pertence a este objeto.

## Invariantes preservadas

- `MEASUREMENT != EVALUATION`
- `RULE != MEASUREMENT`
- `CONFIGURATION != AUTHORITY`
- `APPLICABLE_RULE != ANY_EXISTING_RULE`
- `EVALUATION != ALERT`
- `NO_APPLICABLE_RULE => VALID_MEASUREMENT + NOT_EVALUABLE`
- `MULTIPLE_APPLICABLE_RULES => BLOCKED`
- `AUTHORITY_FAILURE => BLOCKED`, nunca `NOT_EVALUABLE`
- a medição factual permanece no bloco;
- `A5A=DEMONSTRATED_FOR_B5_TECHNICAL_SCOPE` não promove `A5B`;
- `A5B=NOT_DEMONSTRATED` permanece inalterado.

## Limite reservado para B6

B6 permanece não definido. Este documento não define B6 por implicação.

Ficam reservados para decisão governada posterior:

- precedência entre autoridades;
- adjudicação e seleção de vencedor;
- política formal para conflito de autoridade;
- promoção, validade científica, legal, institucional ou normativa de autoridade;
- cutover, readiness de produção e remoção de legado;
- integração e semântica de `EVALUATION → ALERT/EVENT → ACTION`;
- promoção de `A5B`.

O transition object somente detecta e bloqueia conflito. A definição e aprovação deste objeto devem preceder qualquer definição ou implementação de B6.

## Evidência requerida antes de implementação

Antes de qualquer autorização de runtime, deve existir evidência independente de que:

- o gate ocupa a posição correta;
- a mudança é restrita ao caminho temporal;
- `record()` permanece inalterado e fora do gate;
- zero, uma e múltiplas candidaturas têm a semântica definida;
- a matriz de estados admissíveis está definida; enquanto não estiver, elegibilidade indefinida ou não provada bloqueia;
- eventos históricos com authority `REVOKED` ou `SUPERSEDED` são testados contra `measured_at` depois que a política de admissibilidade for governada;
- o nome do estado atual sozinho não decide admissibilidade histórica;
- a consistência de escopo entre `authority`, `authority_scope` e `authority_applicability` é verificada;
- a consistência entre `authority_temporal_boundary`, applicability temporal e `measured_at` é verificada;
- autoridade ausente, malformada, inativa, expirada ou fora da janela bloqueia;
- a medição é retida quando há bloqueio;
- nenhuma avaliação é persistida em bloqueio de autoridade;
- uma avaliação bem-sucedida retém positivamente o snapshot de authority/applicability e sua proveniência;
- `NOT_EVALUABLE` só ocorre após autoridade resolvida e zero RULE aplicável;
- múltiplas RULEs continuam `BLOCKED`;
- incompatibilidade de proveniência ou hash de autoridade/RULE bloqueia;
- falhas do resolver são mapeadas deterministicamente para reason codes `BLOCKED`, sem vazamento de exceção genérica;
- falha inesperada do resolver mapeia para `AUTHORITY_RESOLUTION_UNEXPECTED_FAILURE`;
- o catch-all não mascara reason code específico determinável;
- nenhuma exceção genérica do resolver aparece como resultado governado;
- persistência e rollback são atômicos;
- invariantes B3, B4 e B5 permanecem preservadas;
- nenhum efeito colateral de alert/event/action ocorre.

Os resultados B5 `58 PASS` e `347 PASS` são evidência registrada do ciclo controlado anterior. Eles não são rerun, nem demonstram por si só a integração definida neste documento ou a reprodutibilidade do ambiente histórico.

## Dependências e riscos

### Dependências

- baseline técnica B5 `c13593f3665f425ada833fe6c0ceb225136ec5e3`;
- publicação documental B5 `1e27a672e40b414e6c7b568e401eba55ce7d5e6b`;
- resolução temporal existente de contexto, APS, `APS_MEMBER` e RULE;
- invariantes e limites documentados nos registros B3 e B4;
- aprovação documental independente deste objeto antes de qualquer implementação;
- decisão governada posterior para qualquer proveniência first-class e para B6.
- decisão governada separada sobre elegibilidade de lifecycle antes de qualquer autorização de runtime.

### Riscos

- tratar `AuthorityService` como integrado quando ele ainda está fora de `evaluate_temporal()`;
- transformar exceção genérica em semântica não aprovada;
- selecionar autoridade por precedência implícita;
- perder snapshot temporal ou proveniência na avaliação;
- converter falha de autoridade em `NOT_EVALUABLE`;
- conflitar autoridade com RULE ou com configuração;
- criar efeitos downstream antes de existir contrato de alert/event/action;
- interpretar a definição como autorização de implementação, cutover, produção ou A5B.

## Status de implementação e migração

- **Migration requerida para esta definição:** `NO_FOR_DEFINITION`.
- **Proveniência first-class futura:** requer decisão governada separada.
- **Mudança de runtime futura:** necessária para implementar a chamada do gate; não autorizada por este documento.
- **Implementação autorizada:** `NO`.
- **Cutover autorizado:** `NO`.
- **Legacy removal:** não autorizado.

## Não-objetivos explícitos

Este documento não:

- edita ou implementa runtime, schema, migrations ou testes;
- define ou implementa B6;
- define política de conflito ou vencedor;
- estabelece autoridade científica, legal, institucional ou de domínio;
- altera `record()`;
- cria avaliação provisória antes do gate;
- cria `NOT_EVALUABLE` para falha de autoridade;
- cria alertas, eventos ou ações;
- autoriza cutover, produção ou remoção de legado;
- promove A5B;
- modifica `scratch/`.

## Gate de governança

`NEXT_REQUIRED_GOVERNED_OBJECT::MCM_WQ_INTEGRATION_TRANSITION_OBJECT`

`TRANSITION_OBJECT_STATUS::DEFINED_DOCUMENTARY_ONLY`

O objeto está definido documentalmente neste registro, mas sua implementação permanece não autorizada. Qualquer próxima operação deve ser uma auditoria documental independente e, se aprovada, uma decisão explícita de implementação separada.

`READY_FOR_INDEPENDENT_REAUDIT::YES`

`B6_STATUS::NOT_DEFINED`

`B6_IMPLEMENTATION_AUTHORIZED::NO`

`IMPLEMENTATION_AUTHORIZED::NO`

`CUTOVER_AUTHORIZED::NO`

`A5B_STATUS::NOT_DEMONSTRATED`

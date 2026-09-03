# MCM-WQ — Lifecycle Admissibility Policy Object

Estado de materialização em 2026-09-03, contra a baseline publicada `106b1d679d0b8a4797caf15e173b45a1122b0984`.

## Identidade e natureza

- **Caso:** `PROTEUS`
- **Modelo:** `MCM-WQ`
- **Objeto:** `MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT`
- **Natureza:** objeto governado documental para uma única candidatura authority/applicability contra uma única medição histórica
- **B5 técnico:** `CLOSED_AND_PUBLISHED`
- **B5 classificação:** `TECHNICALLY_CLOSED_WITH_DOCUMENTED_LIMITATIONS`
- **Transition object:** publicado e dependente deste limite de elegibilidade antes de runtime
- **Status de elegibilidade:** `NOT_DEFINED`
- **Status da decisão de política:** `PARTIAL_TECHNICAL_ONLY`
- **Implementação:** `NOT_AUTHORIZED`
- **B6:** `NOT_DEFINED`
- **Cutover:** `NOT_AUTHORIZED`
- **A5A:** `DEMONSTRATED_FOR_B5_TECHNICAL_SCOPE`
- **A5B:** `NOT_DEMONSTRATED`

Este objeto materializa a fronteira técnica interna autorizada para uma única candidatura e uma medição histórica. A admissibilidade dos estados da matriz permanece `NOT_DEFINED`; este registro não preenche decisões que B5 não prova, não implementa runtime e não autoriza avaliação final.

## Autoridade documental e fontes

Este registro segue a convenção canônica de `docs/governance/` usada pelos registros MCM-WQ B3, B4, B5 e pelo objeto de transição publicado. Não substitui esses registros nem cria fonte técnica concorrente.

Fontes examinadas:

- `docs/governance/MCM_WQ_B5_CERTIFICATION_RECORD.md`;
- `docs/governance/MCM_WQ_INTEGRATION_TRANSITION_OBJECT.md`;
- `governed_core/authority_models.py`;
- `governed_core/authority_service.py`;
- `governed_core/evaluation_service.py`;
- `tests/test_b5_authority_lifecycle.py`;
- `migrations/013_mcm_wq_b5_authority_foundation.sql`;
- `migrations/014_mcm_wq_b5_authority_applicability.sql`;
- `migrations/015_mcm_wq_b5_deferred_successor_fk.sql`;
- `migrations/016_mcm_wq_b5_db_temporal_enforcement.sql`.

Disciplina de evidência:

- **PROVEN:** existência dos estados, transições de lifecycle, eventos terminais de applicability, fechamento temporal half-open da applicability e inputs temporais canônicos, dentro do escopo técnico B5;
- **DEFINED_BUT_NOT_PROVEN:** a fronteira técnica documental, o contrato tri-state, o uso de histórico para uma medição histórica e o fail-safe requerido para futura integração; runtime e sua validação ainda não existem;
- **NOT_DEFINED:** admissibilidade de avaliação para qualquer combinação de estados authority/applicability;
- **OUT_OF_SCOPE:** validade científica, legal, institucional ou normativa; precedência, adjudicação, vencedor, B6, cutover, produção e A5B.

O comportamento de runtime descrito como futuro neste documento não é apresentado como implementado. Os resultados B5 `58 PASS` e `347 PASS` continuam apenas evidência registrada do ciclo controlado anterior; não são rerun nesta materialização.

## Pergunta governada

Dado:

- uma `MEASUREMENT`;
- uma authority candidate;
- uma authority-applicability candidate;

este objeto deve, após decisão e aprovação próprias, produzir uma classificação técnica para a candidatura no instante `measurement.measured_at`:

`ELIGIBLE | INELIGIBLE | UNDEFINED`

`UNDEFINED => BLOCKED` no futuro caminho integrado.

## Separações semânticas obrigatórias

- `CURRENT_STATE != HISTORICAL_STATE_AT_MEASURED_AT`;
- `AUTHORITY_STATE != APPLICABILITY_STATE`;
- `TEMPORAL_APPLICABILITY != EVALUATION_ADMISSIBILITY`;
- `TECHNICAL_PROVENANCE != DOMAIN_AUTHORITY`;
- `STATE_EXISTENCE != STATE_ADMISSIBILITY`;
- `STATE_TRANSITION != STATE_ADMISSIBILITY`;
- `MEASUREMENT != EVALUATION`;
- `RULE != MEASUREMENT`;
- `CONFIGURATION != AUTHORITY`;
- `APPLICABLE_RULE != ANY_EXISTING_RULE`;
- `EVALUATION != ALERT`.

Nenhum nome de estado ou resultado técnico pode ser interpretado como validade científica, legal, institucional ou normativa.

## O que B5 realmente prova

### Authority

As migrations B5 e `AuthorityService` provam que:

- `authority_state` aceita `PUBLISHED`, `ACTIVE`, `REVOKED` e `SUPERSEDED`;
- uma authority é criada inicialmente como `PUBLISHED`;
- a transição permitida é `PUBLISHED → ACTIVE → REVOKED|SUPERSEDED`;
- identidade, escopo e boundary da authority são imutáveis; eventos de authority são append-only; `authority_state` muda somente pelas transições de lifecycle permitidas;
- a authority possui identidade, versão, locator, hash e boundary temporal estrutural.

Isso não prova qual estado autoriza uma avaliação histórica.

### Authority applicability

As migrations B5, `AuthorityService` e o teste de lifecycle provam que:

- `authority_applicability_state` aceita `ACTIVE`, `REVOKED` e `SUPERSEDED`;
- um evento `PUBLISHED` de applicability produz estado `ACTIVE`;
- revocation/supersession produz evento terminal, fecha a janela temporal half-open e não permite reopen;
- a view temporal resolve applicability quando `effective_from <= measured_at < terminal_effective_at`, considerando terminal nulo como aberto;
- adjacência não é overlap;
- o teste B5 resolve uma applicability `ACTIVE` associada a uma authority ainda `PUBLISHED`.

Isso prova efeito temporal da applicability, não admissibilidade completa da authority para avaliação.

### Ausência de política existente

`AuthorityService.resolve_applicability()` consulta a view temporal de applicability, mas não consulta `authority_state` nem `authority_temporal_boundary` para produzir uma decisão de admissibilidade de avaliação. `create_applicability()` verifica a existência da authority, mas não estabelece uma política de estado admissível para avaliação.

`evaluate_temporal()` atualmente resolve contexto, APS, autorização de membro e RULE, mas não chama a resolução B5 de authority applicability. Portanto, não existe política de admissibilidade já aplicada ao evaluation path.

## Matriz de decisão de admissibilidade

Esta matriz classifica admissibilidade para avaliação, e não mera existência, transição ou efeito temporal. Nenhuma célula é preenchida por intuição.

| Authority \ Applicability | `ACTIVE` | `REVOKED` | `SUPERSEDED` |
| --- | --- | --- | --- |
| `PUBLISHED` | `NOT_DEFINED` | `NOT_DEFINED` | `NOT_DEFINED` |
| `ACTIVE` | `NOT_DEFINED` | `NOT_DEFINED` | `NOT_DEFINED` |
| `REVOKED` | `NOT_DEFINED` | `NOT_DEFINED` | `NOT_DEFINED` |
| `SUPERSEDED` | `NOT_DEFINED` | `NOT_DEFINED` | `NOT_DEFINED` |

`MATRIX_PROVEN_ADMISSIBLE::NONE`

`MATRIX_PROVEN_INADMISSIBLE::NONE`

`MATRIX_NOT_DEFINED_CELLS::ALL_12_STATE_COMBINATIONS`

O teste B5 que resolve uma applicability `ACTIVE` sob authority `PUBLISHED` não é base para classificar essa combinação como `PROVEN_ADMISSIBLE`; ele demonstra resolução temporal de applicability, não autorização de avaliação.

## Semântica histórica e temporal

A decisão futura deve avaliar a candidatura contra:

- `measured_at` canônico;
- o intervalo temporal aplicável da authority;
- o intervalo temporal da applicability;
- o histórico completo de lifecycle/eventos da authority;
- o histórico completo de lifecycle/eventos da applicability;
- a consistência de `context_revision_id`, `parameter_reference` e lineage da medição.

`CURRENT_STATE_NAME_ALONE MUST NOT DETERMINE HISTORICAL ADMISSIBILITY`.

Uma authority atualmente `REVOKED` ou `SUPERSEDED` não pode ser julgada para uma medição histórica somente pelo nome do estado atual. A decisão deve considerar o instante medido, os eventos efetivos e a política de admissibilidade aprovada separadamente.

Os eventos terminais da applicability podem fechar sua janela onde B5 já prova esse comportamento. Esse fechamento significa apenas que a applicability deixa de ser temporalmente aplicável fora da janela; não constitui, sozinho, política completa de admissibilidade da authority para avaliação.

Preservar:

- intervalos half-open `[start, end)`;
- adjacência sem overlap;
- `created_at != effective_from`;
- `measured_at` como tempo do fato;
- nenhuma substituição por `registered_at`, `created_at`, contexto corrente ou APS corrente.

## Contrato de entrada

O objeto deve operar sobre exatamente uma candidatura e exatamente uma medição e receber:

- `measurement_id`;
- `context_revision_id` imutável;
- `parameter_reference`;
- `measured_at` canônico;
- `authority_id`;
- `authority_version`;
- histórico de lifecycle/eventos da authority;
- boundary temporal da authority;
- identidade de proveniência da authority;
- `applicability_id`;
- escopo da applicability;
- histórico de lifecycle/eventos da applicability;
- intervalo temporal da applicability;
- lineage da medição e do contexto.

O objeto não recebe seleção de vencedor nem cardinalidade de candidatos. Zero candidatos e múltiplos/conflicting candidates são responsabilidades do authority gate de integração.

## Decisões que permanecem necessárias

Uma definição futura, independente deste registro, deve decidir explicitamente:

- se `PUBLISHED` authority pode ser admissível;
- se `ACTIVE` authority é necessária;
- como authority `REVOKED` ou `SUPERSEDED` atual é tratada quando `measured_at` precede ou sucede eventos terminais;
- se uma applicability `ACTIVE` basta ou requer combinação específica com authority state;
- como boundary temporal da authority e intervalo temporal da applicability se combinam;
- como eventos históricos e estados inconsistentes produzem `INELIGIBLE` ou `UNDEFINED`;
- qual base governada é necessária para cada célula não `NOT_DEFINED`.

Até essa decisão, nenhuma combinação é admissível por presunção:

`UNDEFINED_OR_UNPROVEN_ELIGIBILITY => BLOCKED`

## Fronteira de política técnica interna

`TECHNICAL_ADMISSIBILITY_SEPARABLE_FROM_DOMAIN_VALIDITY::YES`

Sob A5A, podem ser governados somente predicados técnicos determinísticos, sem afirmar que uma authority é cientificamente, legalmente, institucionalmente, normativamente ou domain-valid. A distinção é obrigatória:

- `ELIGIBLE`, `INELIGIBLE` e `UNDEFINED` são classificações técnicas de lifecycle para a candidatura e a medição;
- nenhum desses resultados prova autoridade de domínio;
- uma classificação técnica positiva não autoriza avaliação final sem os demais gates e sem qualquer gate externo de validade que seja exigido fora deste objeto.

São predicados tecnicamente governáveis sob A5A:

- `canonical measured_at` válido e usado como tempo do fato;
- requisito de reconstrução histórica de lifecycle/eventos;
- satisfação do `authority temporal boundary`;
- satisfação do intervalo temporal da applicability;
- consistência de linkage entre authority e applicability;
- consistência de `context_revision_id`;
- consistência de `parameter_reference`;
- consistência do lineage de medição/contexto;
- completude do histórico lifecycle/eventos;
- reconhecimento exclusivo de estados lifecycle conhecidos;
- consistência de escopo e proveniência.

Esses predicados podem produzir uma conclusão técnica somente para a candidatura concreta. Eles não autorizam, por si só, a preencher uma célula estática da matriz. A evidência B5 demonstra estados, transições e fechamento temporal da applicability, mas não uma consequência de admissibilidade de avaliação para qualquer estado.

### Semântica técnica dos estados

- `PUBLISHED` é o estado técnico inicial da authority; sua consequência de admissão permanece `NOT_DEFINED`.
- `ACTIVE` é um estado técnico de lifecycle após a transição permitida; sua consequência de admissão permanece `NOT_DEFINED`.
- `REVOKED` é um estado técnico terminal; o efeito histórico da authority não pode ser inferido pelo estado atual.
- `SUPERSEDED` é um estado técnico terminal associado à sucessão governada; o efeito histórico da authority não pode ser inferido pelo estado atual.
- Para applicability, eventos terminais fecham o intervalo temporal onde B5 já prova esse efeito; isso não constitui política completa de admissibilidade da authority.

`STATE_DOMAIN_SEMANTICS::NOT_DEMONSTRATED`

Nenhum significado científico, legal, institucional, normativo ou de domínio é derivado de `PUBLISHED`, `ACTIVE`, `REVOKED` ou `SUPERSEDED`.

### Política histórica técnica

A avaliação técnica futura deve usar `measured_at` e intervalos half-open `[start,end)`:

- `start` é inclusivo;
- o terminal `end` é exclusivo;
- adjacência não é overlap;
- `created_at` e tempo de registro nunca substituem tempo efetivo;
- estado lifecycle atual sozinho nunca decide admissibilidade histórica;
- fora de um intervalo temporal comprovado: `TECHNICALLY_INELIGIBLE => BLOCKED`;
- timing histórico ausente, ambíguo ou não provado: `UNDEFINED => BLOCKED`.

Esta semântica é uma fronteira técnica por candidatura; não classifica as doze células da matriz.

### Fail-safe técnico

- dado técnico obrigatório malformado, incompleto ou desconhecido: `UNDEFINED => BLOCKED`;
- inconsistência de escopo ou proveniência: `BLOCKED`;
- elegibilidade lifecycle indefinida ou não provada: `BLOCKED`;
- a medição factual permanece retida;
- nenhuma avaliação final é persistida;
- nenhum fallback, heurística ou seleção de vencedor.

O fail-safe permanece futuro/documental e não altera o runtime atual.

### Limites de autoridade externa e B6

Technical eligibility não substitui qualquer gate externo de autoridade de domínio que seja exigido antes da avaliação final. `A5A` permanece restrito a provenance, governança e integridade técnica; `A5B` permanece `NOT_DEMONSTRATED`.

Este objeto trata uma única candidatura. Precedência, resolução de conflito, adjudicação, seleção de vencedor, resolução multi-candidata e promoção de authority permanecem fora do escopo e em `B6_STATUS::NOT_DEFINED`.

### Limite da matriz

`PUBLISHED admission consequence=NOT_DEFINED`

`ACTIVE admission consequence=NOT_DEFINED`

`REVOKED admission consequence=NOT_DEFINED`

`SUPERSEDED admission consequence=NOT_DEFINED`

`MATRIX_PROVEN_ADMISSIBLE::NONE`

`MATRIX_PROVEN_INADMISSIBLE::NONE`

`MATRIX_NOT_DEFINED_CELLS::ALL_12_STATE_COMBINATIONS`

Nenhuma célula é alterada por esta emenda documental.

## Contrato de resultado

O resultado futuro deve ser exatamente um de:

- `ELIGIBLE` — a candidatura satisfaz a política técnica aprovada para aquela medição; pode continuar ao próximo passo do authority gate, mas não autoriza avaliação final, não seleciona RULE e não promove A5B;
- `INELIGIBLE` — a candidatura não pode autorizar avaliação para aquela medição; no `evaluate_temporal()` integrado, resulta em `BLOCKED`;
- `UNDEFINED` — a política ou evidência necessária está ausente, inconsistente ou não provada; no `evaluate_temporal()` integrado, resulta em `BLOCKED`.

Cada resultado deve carregar:

- `reason_code`;
- `evaluated_measured_at`;
- identity/version da authority;
- identity da applicability;
- referências relevantes de lifecycle/eventos;
- boundaries temporais relevantes;
- evidência de escopo;
- versão do policy object;
- base e proveniência da decisão.

O resultado não é uma avaliação, não é uma RULE e não é um ALERT/EVENT/ACTION.

## Fail-safe

- `UNKNOWN_STATE => UNDEFINED => BLOCKED`;
- `MALFORMED_HISTORY => UNDEFINED => BLOCKED`;
- `INCOMPLETE_TEMPORAL_DATA => UNDEFINED => BLOCKED`;
- `INCONSISTENT_SCOPE => INELIGIBLE_OR_UNDEFINED`, somente quando a distinção tiver base governada explícita; sem essa base, `UNDEFINED => BLOCKED`;
- nenhum fallback;
- nenhuma heurística;
- nenhuma seleção de vencedor;
- nenhuma conversão de falha de authority em `NOT_EVALUABLE`;
- a medição factual permanece preservada no bloco;
- nenhuma avaliação final é persistida no futuro `evaluate_temporal()` integrado quando o resultado for `INELIGIBLE` ou `UNDEFINED`.

O fail-safe é uma obrigação documental futura, não comportamento implementado no HEAD atual.

## Fronteira B6

Este objeto avalia somente uma candidatura. Ele não define:

- precedência entre authorities;
- conflito winner;
- adjudicação;
- seleção entre múltiplas candidaturas;
- promoção de authority;
- validade científica, legal, institucional ou domain-normative.

Se houver zero candidatos, o authority gate de integração trata a ausência. Se houver múltiplas ou conflitantes candidaturas, o gate bloqueia sem seleção. B6 permanece:

`B6_STATUS::NOT_DEFINED`

`B6_IMPLEMENTATION_AUTHORIZED::NO`

A admissibilidade de uma única candidatura é separável da política de conflito B6 porque não escolhe entre authorities nem estabelece validade de domínio.

## Fronteira A5

`A5A` pode apoiar somente identidade, provenance, integridade técnica e rastreabilidade do objeto dentro do escopo B5.

`A5B::NOT_DEMONSTRATED`

Nenhum estado, hash, locator, teste, migration ou resultado `ELIGIBLE` demonstra autoridade científica, legal, institucional ou normativa.

## Evidência requerida

Antes de implementação futura, deve haver evidência independente de:

- cada ramo da matriz, inclusive a justificativa de cada célula não `NOT_DEFINED`;
- casos `PUBLISHED` e `ACTIVE`;
- medições históricas antes, no instante e depois de eventos lifecycle;
- casos atuais `REVOKED` e `SUPERSEDED` sem inferência somente pelo estado atual;
- consistência authority/applicability de escopo;
- consistência com `context_revision_id` e `parameter_reference`;
- consistência entre authority boundary, applicability interval e `measured_at`;
- histórico lifecycle incompleto/malformado e estados desconhecidos;
- razão determinística para `ELIGIBLE`, `INELIGIBLE` e `UNDEFINED`;
- `ELIGIBLE` não ultrapassa o authority gate, RULE gate ou persistência final;
- `INELIGIBLE => BLOCKED`;
- `UNDEFINED => BLOCKED`;
- zero/múltiplas candidaturas não são selecionadas neste objeto;
- preservação da medição factual em bloqueio;
- ausência de `NOT_EVALUABLE` em falha de authority;
- `A5B` permanece `NOT_DEMONSTRATED`.

## Precondição de implementação

Este objeto deve ser:

`DEFINED → INDEPENDENTLY_AUDITED → APPROVED → PUBLISHED`

antes que qualquer implementação de admissibilidade de lifecycle seja autorizada. Depois disso, a implementação do authority gate em `evaluate_temporal()` continua sendo uma decisão separada.

`MIGRATION_REQUIRED_FOR_DEFINITION::NO`

`IMPLEMENTATION_AUTHORIZED::NO`

`CUTOVER_AUTHORIZED::NO`

## Não-objetivos

Este registro não:

- escolhe admissibilidade para qualquer estado não provado;
- implementa a política ou altera runtime;
- altera schema, migrations ou testes;
- altera `record()`;
- define B6;
- resolve conflitos ou seleciona winners;
- cria alertas, eventos ou ações;
- autoriza cutover ou produção;
- remove legacy;
- promove A5B;
- modifica `scratch/`.

## Status governado

`DOCUMENT_STRUCTURE_STATUS::COMPLETE`

`POLICY_DECISION_STATUS::PARTIAL_TECHNICAL_ONLY`

`LIFECYCLE_ADMISSIBILITY_STATUS::NOT_DEFINED`

`NEXT_REQUIRED_GOVERNED_DECISION::MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT`

`READY_FOR_INDEPENDENT_AUDIT::YES`

`B6_STATUS::NOT_DEFINED`

`B6_IMPLEMENTATION_AUTHORIZED::NO`

`IMPLEMENTATION_AUTHORIZED::NO`

`CUTOVER_AUTHORIZED::NO`

`A5B_STATUS::NOT_DEMONSTRATED`

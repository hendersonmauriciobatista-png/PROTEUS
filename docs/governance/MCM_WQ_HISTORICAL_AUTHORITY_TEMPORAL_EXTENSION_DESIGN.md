# MCM-WQ — Historical Authority Temporal Extension Design

## Status and scope

- **Case:** `PROTEUS`
- **Object:** `MCM_WQ_HISTORICAL_AUTHORITY_TEMPORAL_EXTENSION_DESIGN`
- **Design status:** `CLOSED`
- **Documentary status:** `PUBLISHED`
- **Implementation status:** `CERTIFIED_AND_PUBLISHED_IN_AUTHORITY_GATE_INTEGRATION`
- **A5 scope:** `TECHNICAL_ONLY`
- **A5B:** `NOT_DEMONSTRATED`
- **B6:** `NOT_DEFINED`
- **Cutover:** `NOT_AUTHORIZED`
- **Baseline HEAD:** `1fbe32d6033f7fe2d0644a2d2ccfea695ee7554b`
- **Design audit:** `PASS_INDEPENDENT_FINAL_TEMPORAL_DESIGN_REAUDIT`

This record materializes the independently audited historical authority temporal-extension design. It records decisions and proof obligations; the runtime realization is published in the certified Authority Gate integration and does not create new policy beyond the audited design.

## Problem and semantic distinctions

The current authority lifecycle cannot be historically reconstructed against `measured_at` because `authority_event` lacks authoritative `effective_at`.

The following remain distinct:

`registered_at != effective_at`  
`current_state != historical_state`  
`created_at != effective_from`

## Event historical source of truth

`authority_event` remains the historical lifecycle SSoT.

The forward extension requires:

- `effective_at` nullable only for legacy rows;
- canonical explicit `effective_at` for new governed events;
- `ACTIVE` represented through a forward migration;
- no competing historical table;
- no inferred historical backfill.

## Effective-time policy

An explicit governed `effective_at` is required. Allowed sources are:

- `CALLER_SUPPLIED_EXPLICIT_TIME`;
- `SYSTEM_GENERATED_IMMEDIATE_TIME`.

`SYSTEM_GENERATED_IMMEDIATE_TIME` is allowed only when the command explicitly requests immediate effect, the trusted clock is identified, and time-source provenance is retained. `effective_at` remains semantically distinct from `registered_at`; there is no automatic aliasing.

Inference from `registered_at`, `created_at`, `effective_from`, or current state is prohibited. Missing source or provenance fails closed.

## State and event-history separation

Current state-level mechanisms prove only the current transition graph:

- `PUBLISHED -> ACTIVE`;
- `ACTIVE -> REVOKED|SUPERSEDED`;
- terminal/no-reopen behavior.

Those proofs are not event-history integrity proofs. Future event-level guards must independently enforce:

- first `PUBLISHED` event;
- `ACTIVE` only after `PUBLISHED`;
- terminal event only after `ACTIVE`;
- no event after terminal;
- canonical explicit `effective_at`;
- unique and unambiguous temporal ordering;
- `SUPERSEDED` successor linkage;
- append-only history.

## Historical reconstruction

For an authority and canonical `measured_at`, reconstruct the state as the latest valid `authority_event` where:

`effective_at <= measured_at`

Semantics:

- before the first event: `UNDEFINED`;
- at an event boundary: the new state applies;
- between events: the latest valid prior state applies;
- at or after a terminal event: the terminal state applies.

Missing, invalid, or ambiguous history results in `UNDEFINED => BLOCKED`. There is no current-state fallback.

## Authority temporal boundary

These are separate concepts:

`authority_temporal_boundary != authority lifecycle event timeline != authority applicability interval`

As a new legitimate A5A technical policy, a candidate outside a proven authority temporal boundary is:

`OUTSIDE_PROVEN_AUTHORITY_TEMPORAL_BOUNDARY => TECHNICALLY_INELIGIBLE => BLOCKED`

Missing, invalid, or unproven boundary data results in `UNDEFINED => BLOCKED`.

This is not a B5-proven admission fact, not a lifecycle-admissibility matrix classification, and not domain validity.

## Supersession

Supersession requires an explicit predecessor effective time `T`, successor identity/version linkage, independently reconstructed successor history, and no implicit successor `ACTIVE` state. `PUBLISHED` and `ACTIVE` timing remains independent. Equality with `effective_from` is valid only when explicitly governed. Deferred successor foreign-key mechanics and atomicity remain preserved.

## Legacy policy

`LEGACY_TEMPORAL_STATUS=UNPROVEN`

No temporal fact may be backfilled from `registered_at`, current state, hash, locator, or technical provenance. `DATA_BACKFILL_REQUIRED=NO`.

Legacy unresolved history results in `UNDEFINED => BLOCKED`; the factual measurement is retained and no final evaluation is persisted.

## Persistence and enforcement design

| Requirement | Future enforcement |
|---|---|
| Canonical `effective_at` | DB + service |
| New-event completeness | DB + service |
| Event-type validity | DB + service |
| Event ordering | DB + service |
| Duplicate effective times | DB + service |
| Terminal/no-reopen | DB + service |
| Successor linkage | DB + service |
| Append-only history | DB |

An index is recommended for historical lookup but is not required for semantic correctness.

## Forward implementation requirements

- `MIGRATION_REQUIRED=YES`;
- `SCHEMA_CHANGE_REQUIRED=YES`;
- `SERVICE_CHANGE_REQUIRED=YES`;
- `TEST_CHANGE_REQUIRED=YES`;
- `NEW_COLUMN_REQUIRED=YES`;
- `NEW_TABLE_REQUIRED=NO`;
- `DATA_BACKFILL_REQUIRED=NO`.

Migrations `013`–`016` remain immutable. Applicability semantics from `014`–`016` remain unchanged, deferred successor mechanics remain preserved, and the canonical timestamp precedent in `016` may be reused without semantic conflation. No migration number is assigned by this document.

## Proof obligations

Future proof must cover canonical `effective_at`, source provenance, separation from `registered_at`, historical reconstruction at before/at/between/terminal/after boundaries, invalid ordering, duplicate/conflicting times, terminal/no-reopen, supersession timing, legacy missing times, current-state fallback prohibition, rollback/atomicity, direct SQL enforcement, and B5 invariant preservation.

No tests are executed by this materialization.

## Provenance classification

### SUPPORTED_B5_INVARIANTS

- `registered_at != effective_at`;
- `created_at != effective_from`;
- current `authority_state` is not historical lifecycle truth;
- authority and applicability lifecycle remain separate;
- append-only evidence principles;
- existing state-transition constraints;
- terminal/no-reopen state behavior;
- deferred successor linkage and atomicity;
- canonical timestamp precedent;
- migrations `013`–`016` remain immutable.

These B5 invariants do not prove historical authority `effective_at` reconstruction.

### NEW_LEGITIMATE_A5A_TECHNICAL_POLICY

- explicit governed authority-event `effective_at`;
- governed effective-time source and provenance;
- historical authority reconstruction against `measured_at`;
- event-level deterministic ordering;
- event-level terminal/no-reopen enforcement;
- candidate-level authority temporal-boundary predicate:

  `OUTSIDE_PROVEN_AUTHORITY_TEMPORAL_BOUNDARY => TECHNICALLY_INELIGIBLE => BLOCKED`

- missing, invalid, or unproven historical evidence:

  `UNDEFINED => BLOCKED`.

These are technical A5A policies only. They are not B5-proven admission facts, domain validity, A5B evidence, matrix classifications, or B6 policy.

### FUTURE_IMPLEMENTATION_REQUIREMENTS

- forward migration;
- `authority_event.effective_at` extension;
- `ACTIVE` event-domain support;
- persistence guards;
- service validation;
- effective-time provenance capture;
- historical resolver;
- proof and test obligations;
- preservation of B5 invariants.

These requirements are retained as traceability for the separately audited design and are realized by the published Authority Gate integration. They do not authorize scope beyond that bounded integration.

`IMPLEMENTATION_STATUS=CERTIFIED_AND_PUBLISHED`

## Matrix firewall

`TEMPORAL_MODEL_COMPLETE != MATRIX_POLICY_DECIDED`

`MATRIX_PROVEN_ADMISSIBLE=NONE`  
`MATRIX_PROVEN_INADMISSIBLE=NONE`  
`MATRIX_NOT_DEFINED_CELLS=NONE`

`MATRIX_EVIDENCE_REGISTER=docs/governance/MCM_WQ_LIFECYCLE_MATRIX_EVIDENCE_REGISTER.md`

Temporal reconstruction capability alone authorizes no matrix classification.

## Authority firewall

`A5A=TECHNICAL_ONLY`  
`A5B=NOT_DEMONSTRATED`  
`B6=NOT_DEFINED`

This object makes no claim of domain, scientific, legal, or institutional validity; performs no authority promotion, precedence, conflict resolution, winner selection, cutover, alert, or action behavior.

## Governance status

`SEMANTIC_MUTATION_FROM_AUDITED_DESIGN=NO`  
`NEW_POLICY_DECISIONS=NONE`  
`IMPLEMENTATION_AUTHORIZATION=CLOSED_BY_SCOPED_CERTIFIED_GATE`
`B6_STATUS=NOT_DEFINED`  
`CUTOVER_AUTHORIZED=NO`  
`A5B_STATUS=NOT_DEMONSTRATED`

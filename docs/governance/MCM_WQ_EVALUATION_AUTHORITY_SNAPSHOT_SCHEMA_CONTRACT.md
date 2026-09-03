# MCM-WQ Evaluation Authority Snapshot Schema Contract

## Status and authority boundary

This is the canonical documentary contract for Schema B: an evaluation authority snapshot persisted with a future Authority-Gate-governed evaluation. It defines persistence shape, identity, provenance, immutability, and transaction obligations. It is not the lifecycle-admissibility policy SSoT, the Authority Gate SSoT, the content-hash SSoT, an implementation, or domain/scientific/legal/institutional authority.

`SCHEMA_B_DESIGN_STATUS::CLOSED_AUDITED_DOCUMENTARY_CONTRACT`  
`IMPLEMENTATION_STATUS::NOT_IMPLEMENTED`  
`IMPLEMENTATION_AUTHORIZED::NO`  
`A5B_STATUS::NOT_DEMONSTRATED`  
`B6_STATUS::NOT_DEFINED`  
`REAL_EXTERNAL_DB_COMPATIBILITY::UNPROVEN`  
`TRANSACTION_IMPLEMENTATION_ADAPTATION::REQUIRED`

Baseline: `e3c02893fea33012e6405ac77e2b46dec5886fe5`. Current runtime behavior remains unchanged; `record()` remains outside this transition.

## Shape and rationale

`SNAPSHOT_SCHEMA_SHAPE::MINIMAL_HYBRID`

Schema B is a dedicated immutable, one-to-one snapshot for a governed final evaluation, plus a normalized immutable child relation containing the exact nonempty member-authorization basis set used by that snapshot. This shape is required for legacy compatibility, relational constraints, historical immutability, queryability, atomicity, and exact basis preservation. The child relation is not decorative normalization and must not be replaced by live reconstruction or enrichment.

Legacy evaluation rows remain as they are. They are not backfilled or fabricated with authority, applicability, event, verification, policy-version, or member-basis data.

## Direct snapshot fields

Every future governed snapshot contains exactly:

```text
evaluation_id
authority_id
authority_version
authority_applicability_id
authority_lifecycle_event_id
authority_applicability_event_id
verification_id
authority_gate_status
lifecycle_policy_result
rule_resolution_outcome
authority_gate_policy_contract_version
```

`evaluation_id` is the one-to-one owner. `authority_id` and `authority_version` identify the authority artifact and are cross-checked against applicability, lifecycle-event, and accepted verification records. No heuristic identity selection is permitted.

Applicability and applicability-event references preserve historical applicability proof. Historical authority lifecycle and applicability reconstruction is evaluated against the canonical `measured_at` of the governed measurement through the immutable evaluation-to-measurement relation. It must not substitute current time, evaluation execution time, `registered_at`, `created_at`, `effective_from`, `verified_at`, current `authority_state`, current `authority_applicability_state`, or the latest state/policy. A current-state projection is not the historical SSoT; valid history must be complete and consistent. The lifecycle-event reference identifies historical evidence without duplicating lifecycle state; current `authority_state` is not the snapshot SSoT.

`verification_id` is the sole Schema A handoff. It references accepted, immutable proof for the same authority identity and version. Schema B does not duplicate expected or computed digests, hash algorithm, hash-contract version, `verified_at`, locator, or artifact bytes.

The policy field is exactly `authority_gate_policy_contract_version`. The recognized identifier is `mcm-wq-authority-gate-technical-admission/v1`. Unknown identifiers block creation of a final row: no fallback to latest, Git, engine, or hash substitution. The persisted identifier is retained for historical interpretation.

## Status and rule outcomes

`authority_gate_status` is `RESOLVED` for every Schema-B-governed final snapshot. A `BLOCKED` authority-gate result never creates a snapshot.

`lifecycle_policy_result` is `TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION`. This is technical A5A only; it does not assert scientific, legal, regulatory, institutional, normative, or domain validity.

`rule_resolution_outcome` is `ZERO_APPLICABLE_RULE` or `ONE_APPLICABLE_RULE`. After authority resolution, zero applicable rules produce a valid measurement plus `NAO_AVALIAVEL` and a complete snapshot; one applicable rule may proceed to normal evaluation and a complete snapshot. Multiple applicable rules block and create no final evaluation or snapshot.

## Blocked firewall

Each Authority-Gate failure class, including authority absence or resolution failure, multiple or conflicting authority candidates, invalid or unaccepted verification evidence, an unknown or unrecognized policy-contract version, incomplete Authority-Gate proof, an incomplete required snapshot, and multiple applicable rules, results in `BLOCKED`. For each such failure:

```text
FACTUAL_MEASUREMENT_RETAINED::YES
FINAL_EVALUATION_ROW_PERSISTED::NO
DIAGNOSTIC_EVIDENCE::SEPARATE_FROM_FINAL_EVALUATION
FALLBACK::PROHIBITED
HEURISTIC_SELECTION::PROHIBITED
```

Authority failure never becomes `NAO_AVALIAVEL`. `NAO_AVALIAVEL` is valid only when `authority_gate_status == RESOLVED`, `rule_resolution_outcome == ZERO_APPLICABLE_RULE`, and the complete authority snapshot is persisted. This contract does not define a diagnostic-persistence schema.

Derived or deliberately non-duplicated data includes measurement identity and `measured_at`, parameter and context lineage, APS-set identity/version, authority temporal boundaries, applicability intervals, digest fields, algorithm, verification-contract version, `verified_at`, locator, bytes, and historical lifecycle state. Future cross-record consistency checks remain mandatory.

## Exact member-authorization basis

The member relation stores the exact basis IDs used by the snapshot with `ONE_OR_MORE_PER_GOVERNED_SNAPSHOT` cardinality. Each basis ID is unique per snapshot; ordering is irrelevant; the set is immutable after commit. It may not be reconstructed from a live relation or enriched after the fact. Each reference targets the authoritative immutable APS member-authorization-basis identity represented by the resolved context. Ownership and cross-identity checks prevent mixing authority versions.

## One-to-one and legacy boundaries

```text
legacy evaluation                       -> zero snapshot
unchanged record()                      -> zero snapshot
future gate-governed final evaluation   -> exactly one complete snapshot
governed snapshot                       -> one or more exact member refs
```

Snapshot-row presence is the discriminator; no redundant flag is introduced. Persisted governed evaluations must remain interpretable without mutable/current `authority_state`, `authority_applicability_state`, latest/current policy version, or live member relations. They use immutable references and the persisted policy version.

## Conceptual relational contract

The future conceptual FK graph is exactly:

```text
snapshot -> evaluation
snapshot -> authority identity/version
snapshot -> authority applicability
snapshot -> authority lifecycle event
snapshot -> applicability event
snapshot -> accepted Schema A verification evidence
member basis -> snapshot
member basis -> authoritative immutable APS basis identity
```

No FK points to a mutable current projection. Critical provenance must be relational, queryable, and constraintable, not only JSON. Snapshot and member rows are immutable: no rebinding, deletion, or update after commit.

## Transaction and service boundary

The future integrated `evaluate_temporal()` path owns one transaction for the evaluation, snapshot, and exact member-basis set. There are no partial snapshots or partial final evaluations. The same transaction applies to `NAO_AVALIAVEL` after successful authority resolution. `record()` is unchanged and outside this contract. Transaction-aware repository/service adaptation is required; this is not a reason to alter current behavior.

`SCHEMA_B_DESIGN_DEPENDENCY::SATISFIED`

`SCHEMA_B_MATERIALIZATION_DEPENDENCY::REQUIRES_PHYSICAL_SCHEMA_A_INFRASTRUCTURE_FIRST`

Schema A must exist physically before Schema B is materialized. Logical order is repository baseline through migration 017, migration 018 for artifact-verification infrastructure only, then migration 019 for evaluation-snapshot infrastructure only and only after Schema A. No migration is created, combined, or authorized here.

The future model is `GovernedEvaluationAuthoritySnapshot` plus a member-basis reference model. Future repository operations must persist and retrieve immutable snapshots and basis sets with connection awareness. Future service integration is limited to Authority-Gate-governed `evaluate_temporal()`; `record()` remains outside scope.

## Required future proof obligations

Future tests must prove: legacy preservation and no backfill; complete snapshots for successful evaluation and `NAO_AVALIAVEL`; no final row on Authority-Gate block or multiple rules; accepted and invalid Schema A verification; recognized, unknown, and retained policy versions; identity, applicability, lifecycle, context, APS, and parameter consistency; exact nonempty member sets; snapshot/member immutability; the current-state firewall; non-substitution of JSON; transaction rollback with no partials; fresh migration behavior and compatibility with persisted 017 data; and preservation of A5A/B6 boundaries.

## Explicit non-goals and limitations

This contract does not implement the physical schema, migration 019, the Authority Gate, lifecycle policy, alerts/events/actions, GEO behavior, cutover, legacy removal, or domain-authority promotion. It does not authorize implementation or historical backfill.

`MIGRATION_018_AUTHORIZED::NO`  
`MIGRATION_019_AUTHORIZED::NO`  
`AUTHORITY_GATE_IMPLEMENTATION_AUTHORIZED::NO`  
`GEO_IMPLEMENTATION_AUTHORIZED::NO`  
`CUTOVER_AUTHORIZED::NO`  
`HISTORICAL_BACKFILL_ALLOWED::NO`

The design preserves the limitations that A5B is not demonstrated, B6 is not defined, real external database compatibility is unproven, and transaction implementation adaptation is still required. This is a documentary design contract only and is ready for independent documentary re-audit.

# MCM-WQ — Lifecycle Matrix Evidence Register

Status: `O4_EVIDENCE_REGISTER_MATERIALIZED`

Baseline: `ca3b7cb3bb16fae8d27e1a65846a4bd77a92c5d1`

Semantic source: `MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT.md`

Integration source: `MCM_WQ_INTEGRATION_TRANSITION_OBJECT.md`

## Evidence interpretation

The matrix policy result is distinct from the integrated Authority Gate result.
`ELIGIBLE_IF_TECHNICAL_PREDICATES_PASS` becomes `RESOLVED` only when all
technical predicates pass. `INELIGIBLE` and `UNDEFINED` become `BLOCKED` and
produce no final evaluation, basis, or Schema B snapshot.

For terminal applicability, the temporal view excludes the applicability at
and after its terminal boundary. The integrated path therefore fails closed as
`APPLICABILITY_INVALID`; this is the runtime boundary translation of the
matrix's terminal `INELIGIBLE` outcome and does not select a winner or persist
a final result.

Terminal applicability states are valid database states created through the
governed lifecycle service. Invalid ordering, overlap, reopen, and malformed
post-017 authority histories are instead covered by structural prevention and
defensive unit evidence; they must not be fabricated in the database.

## Twelve-cell map

| # | Authority | Applicability | Expected policy outcome | Runtime outcome | Evidence type | Supporting evidence | Real DB state | Prevented at write | Closure |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `PUBLISHED` | `ACTIVE` | `ELIGIBLE_IF_TECHNICAL_PREDICATES_PASS` | `RESOLVED` when predicates pass | `DIRECT_INTEGRATION_TEST` | `test_real_path_invokes_gate_and_persists_complete_zero_snapshot`; `test_real_path_persists_one_rule_snapshot_and_exact_bindings` | Yes | No | `COVERED` |
| 2 | `ACTIVE` | `ACTIVE` | `ELIGIBLE_IF_TECHNICAL_PREDICATES_PASS` | `RESOLVED` when predicates pass | `DIRECT_UNIT_TEST` + `FAIL_SAFE_RESOLUTION` | `test_historical_authority_reconstructs_state_at_measured_at`; `authority_event_active_requires_published` | Yes | No | `COVERED` |
| 3 | `PUBLISHED` | `REVOKED` | `INELIGIBLE` | `BLOCKED` — `APPLICABILITY_INVALID` outside `[effective_from, terminal_effective_at)` | `STRUCTURAL_PREVENTION` + `FAIL_SAFE_RESOLUTION` | `authority_applicability_temporal`; `test_revocation_closes_half_open_interval`; `authority_app_terminal_once` | Yes | No | `COVERED` |
| 4 | `PUBLISHED` | `SUPERSEDED` | `INELIGIBLE` | `BLOCKED` — `APPLICABILITY_INVALID` outside the temporal window | `STRUCTURAL_PREVENTION` + `FAIL_SAFE_RESOLUTION` | `authority_applicability_temporal`; `test_supersession_linkage_and_projection`; `authority_app_no_reopen` | Yes | No | `COVERED` |
| 5 | `ACTIVE` | `REVOKED` | `INELIGIBLE` | `BLOCKED` — `APPLICABILITY_INVALID` outside the temporal window | `STRUCTURAL_PREVENTION` + `FAIL_SAFE_RESOLUTION` | `test_revocation_closes_half_open_interval`; `authority_applicability_temporal` | Yes | No | `COVERED` |
| 6 | `ACTIVE` | `SUPERSEDED` | `INELIGIBLE` | `BLOCKED` — `APPLICABILITY_INVALID` outside the temporal window | `STRUCTURAL_PREVENTION` + `FAIL_SAFE_RESOLUTION` | `test_supersession_linkage_and_projection`; `authority_applicability_temporal` | Yes | No | `COVERED` |
| 7 | `REVOKED` | `ACTIVE` | `INELIGIBLE_IF_TERMINALITY_PROVEN; OTHERWISE UNDEFINED` | `BLOCKED` — `LIFECYCLE_INELIGIBLE` when terminality is proven; otherwise `LIFECYCLE_UNDEFINED` | `DIRECT_INTEGRATION_TEST` + `DIRECT_UNIT_TEST` | `test_real_db_terminal_lifecycle_blocks_at_and_after_terminal`; `test_historical_authority_reconstructs_state_at_measured_at` | Yes | No | `COVERED` |
| 8 | `REVOKED` | `REVOKED` | `INELIGIBLE` | `BLOCKED` — `APPLICABILITY_INVALID` outside the temporal window | `STRUCTURAL_PREVENTION` + `FAIL_SAFE_RESOLUTION` | `authority_applicability_temporal`; `test_revocation_closes_half_open_interval`; `authority_event_terminal_requires_active` | Yes | No | `COVERED` |
| 9 | `REVOKED` | `SUPERSEDED` | `INELIGIBLE` | `BLOCKED` — `APPLICABILITY_INVALID` outside the temporal window | `STRUCTURAL_PREVENTION` + `FAIL_SAFE_RESOLUTION` | `authority_applicability_temporal`; `test_supersession_linkage_and_projection`; `authority_event_no_after_terminal` | Yes | No | `COVERED` |
| 10 | `SUPERSEDED` | `ACTIVE` | `INELIGIBLE_IF_TERMINALITY_PROVEN; OTHERWISE UNDEFINED` | `BLOCKED` — `LIFECYCLE_INELIGIBLE` when terminality is proven; otherwise `LIFECYCLE_UNDEFINED` | `DIRECT_UNIT_TEST` + `FAIL_SAFE_RESOLUTION` | `test_supersession_linkage_and_projection`; `authority_event_successor_contract`; `authority_event_no_after_terminal` | Yes | No | `COVERED` |
| 11 | `SUPERSEDED` | `REVOKED` | `INELIGIBLE` | `BLOCKED` — `APPLICABILITY_INVALID` outside the temporal window | `STRUCTURAL_PREVENTION` + `FAIL_SAFE_RESOLUTION` | `authority_applicability_temporal`; `test_revocation_closes_half_open_interval`; `authority_app_terminal_once` | Yes | No | `COVERED` |
| 12 | `SUPERSEDED` | `SUPERSEDED` | `INELIGIBLE` | `BLOCKED` — `APPLICABILITY_INVALID` outside the temporal window | `STRUCTURAL_PREVENTION` + `FAIL_SAFE_RESOLUTION` | `authority_applicability_temporal`; `test_supersession_linkage_and_projection`; `authority_app_no_reopen` | Yes | No | `COVERED` |

## Structural and defensive evidence

The following guards support the matrix without manufacturing invalid rows:

- migrations 013 and 016 enforce authority/applicability identity,
  immutability, temporal interval validity, overlap prevention, terminal
  uniqueness, and no reopen;
- migration 017 enforces canonical effective time, first `PUBLISHED` event,
  valid `ACTIVE` sequencing, terminal sequencing, no events after terminal,
  successor linkage, and unresolved legacy history;
- `AuthorityService.resolve_historical_authority()` uses `measured_at`,
  returns `TECHNICALLY_INELIGIBLE` for an authority boundary failure, and
  returns `UNDEFINED` for incomplete, ambiguous, or malformed history;
- `AuthorityGate` translates those results to deterministic blocked reason
  codes without final persistence.

## Closure decision

All 12 policy cells are explicitly defined and mapped. No production runtime
change, migration change, schema change, GEO work, B6 work, A5B promotion,
cutover, or alert/event/action implementation is authorized by this register.

`NEW_TESTS_REQUIRED::NO`

`RUNTIME_FILES_CHANGED::NONE`

`O4_EVIDENCE_READY::YES`

`A5B_STATUS::NOT_DEMONSTRATED`

`B6_STATUS::OPTIONAL_FUTURE_ENHANCEMENT`

`GEO_IMPLEMENTATION_AUTHORIZED::NO`

`CUTOVER_AUTHORIZED::NO`

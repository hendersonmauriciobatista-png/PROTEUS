# PROTEUS — Final Product Scope

## Governed status

| Field | Value |
| --- | --- |
| Case | PROTEUS |
| Current product identity | Sistema de Monitoramento de Águas |
| Baseline | `935181ccc96469336b04214aa8ecbd4c0217d1e6` |
| Final product target | `CASE_CLOSED_CLIENT_DELIVERABLE` |
| Target client delivery date | `2026-11-12` |
| Product profile | `LOCAL_DESKTOP_LICENSED_PRODUCT` |
| Scope status | `FROZEN_WITH_CONTROLLED_GEO_AMENDMENT` |
| Document status | `APPROVED_FROZEN_SCOPE` |
| Authority status | Canonical SSoT for final-product scope and completion gates |

This document is the canonical Source of Truth for final-product inclusion,
exclusion, completion objects, delivery profile, technical-debt closure, and
future scope amendments. It records approved scope decisions; it does not
certify that the product is complete or ready for delivery.

Specialized governance documents remain authoritative for their own semantics,
including:

- `MCM_WQ_B5_CERTIFICATION_RECORD.md`;
- `MCM_WQ_INTEGRATION_TRANSITION_OBJECT.md`;
- `MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT.md`;
- `MCM_WQ_HISTORICAL_AUTHORITY_TEMPORAL_EXTENSION_DESIGN.md`;
- `docs/operational/OP_00_OPERATIONAL_SCOPE_BOUNDARY_AUDIT.md`.

This SSoT references those documents instead of duplicating their detailed
technical or domain semantics.

## Final product intent

The final product is the completed current product within this frozen scope.
At `CASE_CLOSED`, no approved in-scope implementation, integration, policy,
test, documentation, or delivery work may remain intentionally deferred.

Future maintenance, defect correction, and genuinely new versions remain
permitted after closure. They are not technical debt of this product.

The supported delivery model is a locally installed, versioned desktop
application with documented environment requirements and controlled licensing
and use. A hosted service is not required by this scope.

The product remains observational and educational. Licensing does not authorize
scientific, regulatory, legal, institutional, normative, or domain-authority
claims.

## Frozen object classification

| Object | Classification | Scope decision |
| --- | --- | --- |
| O1 — Authority gate integration | `FINAL_PRODUCT_REQUIRED` | B5 authority applicability must join the temporal evaluation path to complete the internal technical authority architecture. |
| O2 — Historical authority temporal extension | `FINAL_PRODUCT_REQUIRED` | The published design must be implemented to complete the approved internal technical authority architecture. |
| O3 — Lifecycle admissibility policy | `FINAL_PRODUCT_REQUIRED` | Required to make authority-gated evaluation deterministic. The specialized policy object remains authoritative for its semantics. |
| O4 — Lifecycle matrix policy | `FINAL_PRODUCT_REQUIRED` | Required policy work for final authority-architecture completion. No lifecycle cell is classified by this document. |
| O5 — B6 precedence/adjudication | `OPTIONAL_FUTURE_ENHANCEMENT` | The final product detects multiple or conflicting authority candidates and blocks them without a winner, precedence, or promotion. |
| O6 — A5B domain authority | `OUT_OF_SCOPE_CURRENT_PRODUCT` | External domain authority is not a software-completion requirement for the bounded observational product. `A5B_STATUS=NOT_DEMONSTRATED`. |
| O7 — Alert/event boundary | `FINAL_PRODUCT_REQUIRED` | Observational alerts/events are in scope; evaluation, alert/event, and action remain distinct. |
| O8 — Deployment profile | `FINAL_PRODUCT_REQUIRED` | Local desktop delivery is required. Hosted/cloud deployment is an optional future enhancement. |
| O9 — Georeferencing core | `FINAL_PRODUCT_REQUIRED` | Governed spatial context is a required architectural dimension of monitoring. |
| O10 — Bounded configurability | `FINAL_PRODUCT_REQUIRED` | Supported, developer-controlled, and client-editable configuration must be explicitly bounded. Unlimited adaptability is optional. |
| O11 — Data and reset policy | `FINAL_PRODUCT_REQUIRED` | Demo/test/real data, persistence, reset, privacy responsibility, and provenance expectations must be defined and proven. |
| O12 — Controlled-use licensing | `FINAL_PRODUCT_REQUIRED` | Sufficient controlled-use licensing terms are required for lawful delivery. General commercialization strategy is out of scope. |
| O13 — Installation and reproducibility | `FINAL_PRODUCT_REQUIRED` | Clean installation, startup, supported environment, dependency reproducibility, and exact release identity are required. |
| O14 — Client workflow | `FINAL_PRODUCT_REQUIRED` | The supported workflow must run from startup through the intended observational outcome. |
| O15 — Documentation and support | `FINAL_PRODUCT_REQUIRED` | Quick Start, installation, workflow, data boundary, limitations, authority boundary, support, licensing, and release identification must be consistent. |

No final-scope object remains unresolved. Pending work is completion work inside
the frozen scope, not an unresolved scope decision.

## Georeferencing scope amendment

`GEO_ARCHITECTURAL_RELEVANCE=CONFIRMED`

`GEO_GOVERNED_CONTEXT_DIMENSION=REQUIRED`

The final architecture must preserve an explicit place for the geographic
identity or context of the monitored object. The applicable context must be
capable of carrying governed spatial context.

The existing MCM-WQ chain is preserved:

```text
MEASUREMENT
→ APPLICABLE_CONTEXT
→ AUTHORITY_APPLICABILITY
→ APPLICABLE_RULE
→ EVALUATION
```

The candidate relationship `MONITORING_POINT → GEO_REFERENCE` and
`MEASUREMENT → MONITORING_POINT` remains a design candidate, not a frozen
domain model.

`GEO_EXACT_DOMAIN_MODEL=NOT_DEFINED`

`GEO_SEMANTICS=NOT_DEFINED`

`GEO_IMPLEMENTATION_AUTHORIZED=NO`

`GEO_NORMATIVE_RESEARCH_REQUIRED=YES`

`MONITORING_POINT_MODEL_STATUS=RESEARCH_CANDIDATE`

`SPATIAL_TEMPORALITY_STATUS=RESEARCH_HYPOTHESIS`

Before GEO implementation, dedicated official-document research must
distinguish normative requirements, technical standards, operational practice,
and recommendations. This scope does not assert a mandatory datum, precision,
GPS, map, GIS, or historical-location rule.

Required before case closure:

- GEO documentary research complete;
- GEO semantic model approved;
- required GEO implementation complete;
- GEO integration complete;
- GEO tests complete;
- GEO traceability complete;
- GEO documentation complete;
- GEO client workflow proven.

`LIFECYCLE_DEPENDENCY=NO_DIRECT_DEPENDENCY_PROVEN`

GEO research is required before GEO implementation. No direct dependency on
lifecycle-admissibility work is established by the current repository evidence.

## Completion gates

### CODE_COMPLETE

- No approved in-scope implementation remains pending.
- The entrypoint, supported workflow, required fail-safe behavior, and required
  downstream boundaries are implemented.
- No authority-dependent behavior is exposed without its approved technical
  gate.

### ARCHITECTURE_COMPLETE

- The required Measurement → Context → Rule → Evaluation chain is complete.
- Required authority, provenance, temporal, spatial, and downstream boundaries
  are integrated.
- No required integration remains intentionally deferred.

### GOVERNANCE_COMPLETE

- Required policy decisions are approved.
- Lifecycle decisions are made only through separately authorized governance.
- B6 and A5B are either completed within scope or remain explicitly outside
  the current product boundary.
- No technical evidence is presented as domain authority.

### EVIDENCE_COMPLETE

- Clean installation and startup are independently demonstrated.
- The client workflow is independently demonstrated.
- Fail-safe, reset, data-boundary, provenance, and baseline-consistency
  evidence is complete.
- Evidence limitations remain explicit.

### DOCUMENTATION_COMPLETE

- Delivery instructions match the baseline.
- Workflow, data, support, licensing, authority limitations, and release identity
  are mutually consistent.
- No stale version or branch instructions remain.

### DELIVERY_COMPLETE

- The exact versioned package is identified.
- Installation and startup instructions are validated.
- Controlled-use terms and support boundaries are defined.
- Acceptance evidence is attached to the package.
- No prohibited claims or undocumented required behavior remain.

### CASE_CLOSED

All of the following must be zero:

- `KNOWN_IN_SCOPE_DEFERRED_IMPLEMENTATION`;
- `KNOWN_IN_SCOPE_DEFERRED_INTEGRATION`;
- `KNOWN_IN_SCOPE_DEFERRED_POLICY`;
- `KNOWN_IN_SCOPE_DEFERRED_TEST`;
- `KNOWN_IN_SCOPE_DEFERRED_DOCUMENTATION`;
- `KNOWN_IN_SCOPE_DELIVERY_BLOCKER`.

No known essential final-scope work may be moved after delivery to satisfy the
target date.

## Governed completion sequence

```text
SCOPE_FINAL_FROZEN
→ POLICY_DECISIONS
→ ARCHITECTURE_COMPLETE
→ IMPLEMENTATION_COMPLETE
→ INTEGRATION_COMPLETE
→ TESTS_AND_EVIDENCE
→ FINAL_DOCUMENTATION
→ CLEAN_INSTALL
→ ACCEPTANCE
→ LICENSED_DELIVERY
→ CASE_CLOSED
```

`NEXT_CRITICAL_OBJECT=MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_DECISION`

`PARALLEL_REQUIRED_OBJECT=GEO_DOCUMENTARY_RESEARCH_AND_SEMANTIC_MODEL`

The GEO parallel object is required before GEO implementation and is not
authorized for execution by this record.

## Governance firewalls

`A5B_STATUS=NOT_DEMONSTRATED`

`B6_STATUS=NOT_DEFINED`

`MATRIX_PROVEN_ADMISSIBLE=NONE`

`MATRIX_PROVEN_INADMISSIBLE=NONE`

`MATRIX_NOT_DEFINED_CELLS=ALL_12_STATE_COMBINATIONS`

`IMPLEMENTATION_AUTHORIZED=NO`

`CUTOVER_AUTHORIZED=NO`

`GEO_IMPLEMENTATION_AUTHORIZED=NO`

Recording scope inclusion does not authorize implementation, schema change,
migration, lifecycle-matrix classification, B6 definition, A5B promotion, or
cutover.

## Quality and schedule

`QUALITY_AND_GOVERNANCE=NON_NEGOTIABLE`

`QUALITY_GATE=OPEN_REQUIRED_COMPLETION_WORK`

`TARGET_DATE=2026-11-12`

`SCHEDULE_STATUS=AT_RISK_PENDING_COMPLETION_PLAN`

The target date does not authorize quality reduction or silent deferral of
required final-scope work.

# MCM-WQ Authority Gate Technical Policy Version Contract

## Status and documentary boundary

This is one canonical documentary contract for the stable runtime identity of
the MCM-WQ Authority Gate technical-admission policy. It identifies and
version-controls the governed technical admission semantics; it does not
replace or duplicate the semantic policy Source of Truth.

```text
CASE::PROTEUS
VERSIONED_SEMANTIC_OBJECT::MCM_WQ_AUTHORITY_GATE_TECHNICAL_ADMISSION_CONTRACT
VERSION_OBJECT_DECISION::COMBINED_AUTHORITY_GATE_TECHNICAL_ADMISSION_CONTRACT
CURRENT_POLICY_RUNTIME_STATUS::NOT_IMPLEMENTED
IMPLEMENTATION_AUTHORIZED::NO
```

This contract does not change lifecycle admissibility semantics, classify any
matrix cell, define B6, establish domain authority, design Schema B, create a
migration, or authorize runtime implementation.

## Versioned semantic object

The versioned object is the combined technical admission contract consumed as
one Authority Gate decision. Its scope is limited to:

- authority candidate cardinality;
- historical lifecycle admissibility;
- temporal applicability;
- technical scope and lineage predicates;
- authority temporal boundary;
- accepted artifact and content-hash proof requirement;
- fail-safe `BLOCKED` behavior.

This object does not imply scientific validity, legal validity, regulatory
validity, institutional competence, domain correctness, or any other A5B
authority.

## Canonical identifier

The current recognized identifier is exactly:

```text
mcm-wq-authority-gate-technical-admission/v1
```

Its vocabulary is:

```text
ASCII
LOWERCASE
NAMESPACE::mcm-wq
SEMANTIC_OBJECT::authority-gate-technical-admission
MAJOR_VERSION_SUFFIX::/vN
PATCH_MINOR_REQUIRED::NO
```

The identifier is stable, human-readable, machine-comparable, and safe for
persistence. It is not a Git SHA, migration number, engine version,
date-only identifier, document filename, or database schema version.

Only major identifiers are required: `v1`, `v2`, `v3`, and so on.

## Current policy mapping

The currently published and closed technical admission semantics map to:

```text
CURRENT_POLICY_MAPPING::mcm-wq-authority-gate-technical-admission/v1
```

This mapping records the current technical policy only. It does not claim that
the Authority Gate or the integrated evaluation path has been implemented.

The lifecycle policy remains the semantic Source of Truth for the admission
rules. This version contract gives those already-defined semantics a stable
runtime identity without restating the lifecycle matrix or its predicates.

## Version increment rule

A new major identifier is required whenever a semantic change can alter a
governed technical admission outcome. This includes changes to:

- candidate cardinality semantics;
- positive-admission predicates;
- historical lifecycle eligibility;
- `measured_at` temporal semantics;
- authority applicability semantics;
- authority temporal-boundary semantics;
- scope or lineage predicates;
- required artifact or hash-verification semantics;
- fail-safe `BLOCKED` behavior.

A new identifier is not required for a change that preserves those semantics,
including:

- editorial or documentation-only changes;
- additional tests;
- implementation refactors;
- storage or schema changes;
- performance optimizations.

```text
SEMANTIC_CHANGE_AFFECTING_ADMISSION_OUTCOME=>NEW_MAJOR_VERSION
EDITORIAL_OR_SEMANTICALLY_NEUTRAL_CHANGE=>NO_VERSION_CHANGE
```

## Immutability and historical interpretation

Once a policy identifier has governed a persisted evaluation, its semantic
meaning is immutable. A future semantic change creates a new major identifier;
it does not mutate `v1`.

Historical evaluations retain the identifier persisted with them. They must
not be reinterpreted using the current, latest, or default policy version.

## Recognition and fail-safe behavior

Future runtime may govern a new final evaluation only with an explicitly
recognized policy-contract identifier. The currently recognized value is:

```text
mcm-wq-authority-gate-technical-admission/v1
```

An unknown or unavailable identifier has the following consequence:

```text
UNKNOWN_POLICY_VERSION
  => GOVERNANCE_CONTRACT_UNAVAILABLE
  => BLOCKED
```

There is no fallback, latest-version alias, implicit upgrade, heuristic
mapping, or version winner selection. B6 is not involved in recognizing a
single known policy version.

## Semantic Source of Truth and supporting contracts

The semantic Source of Truth is:

```text
MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT
```

This contract identifies and versions the semantics owned by that policy
object. It is not a competing policy Source of Truth.

Supporting contracts are referenced without duplication:

- `MCM_WQ_INTEGRATION_TRANSITION_OBJECT`;
- `MCM_WQ_AUTHORITY_CONTENT_HASH_VERIFICATION_CONTRACT`;
- `MCM_WQ_AUTHORITY_ARTIFACT_VERIFICATION_SCHEMA_CONTRACT`;
- `MCM_WQ_HISTORICAL_AUTHORITY_TEMPORAL_EXTENSION_DESIGN`.

`FINAL_PRODUCT_SCOPE.md` remains the Source of Truth for final-product scope;
it does not define this runtime policy identifier.

## Separation from other versions

The Authority Gate policy version is distinct from the implementation engine
version:

```text
authority_gate_policy_contract_version != evaluation_engine_version
```

The policy version identifies governed admission semantics. The engine version
identifies software implementation or build behavior. Neither substitutes for
the other.

The Authority Gate policy version is also distinct from the artifact hash
verification version:

```text
authority_gate_policy_contract_version != verification_contract_version
```

The hash contract identifies exact artifact verification semantics. Schema B
receives that proof through `verification_id`; it does not duplicate the hash
contract version solely for convenience.

Git SHA may prove documentary development or publication provenance, but it is
not the runtime policy identity. Runtime behavior must not depend on repository
availability.

## Schema B handoff

The exact future first-class field concept is:

```text
authority_gate_policy_contract_version
```

For every future Authority-Gate-governed final evaluation, the field must
contain the recognized exact identifier used for that evaluation:

```text
authority_gate_policy_contract_version
  = mcm-wq-authority-gate-technical-admission/v1
```

The field is required for both paths:

```text
AUTHORITY_GATE::RESOLVED
+ ONE_APPLICABLE_RULE

AUTHORITY_GATE::RESOLVED
+ ZERO_APPLICABLE_RULE
  => NOT_EVALUABLE
```

An authority `BLOCKED` outcome creates no final evaluation row. Diagnostic
blocked persistence is outside this contract.

## Legacy policy behavior

Existing evaluations created before Authority Gate integration retain explicit
absence of this policy version:

```text
authority_gate_policy_contract_version::ABSENT_LEGACY
HISTORICAL_BACKFILL_ALLOWED::NO
```

No version may be fabricated or backfilled. Legacy evaluation rows are not
reinterpreted as Authority-Gate-governed success.

Historical evaluation meaning is determined by its persisted policy version,
never by current state, latest version, engine version, hash version, or Git
revision.

## A5B and B6 boundaries

```text
A5B_STATUS::NOT_DEMONSTRATED
B6_STATUS::NOT_DEFINED
```

This identifier and its versioning rules do not imply scientific, legal,
regulatory, institutional, normative, or domain correctness. They also do not
define precedence, adjudication, conflict resolution, winner selection, or
authority promotion.

## Future test contract

Future implementation tests must prove:

- recognized policy version is accepted;
- unknown policy version fails closed;
- successful governed evaluation persists the policy version;
- `NOT_EVALUABLE` after resolved authority persists the policy version;
- legacy rows retain absent version without fabricated backfill;
- old evaluations retain their old version after a new version exists;
- no latest-version fallback exists;
- engine version cannot substitute;
- hash-contract version cannot substitute;
- Git SHA cannot substitute;
- semantic change requires the next major version;
- editorial, refactor, and storage-only changes do not require a new version;
- the A5B firewall remains preserved.

No tests are executed by this documentary contract.

## Explicit non-goals

This contract does not:

- restate or amend the lifecycle admissibility matrix;
- redefine candidate discovery or Authority Gate cardinality;
- redefine artifact custody or hash proof;
- define B6;
- define or implement Schema B;
- edit runtime, schema, migrations, or tests;
- authorize implementation, cutover, production, or GEO work;
- promote A5B.

## Governed status

```text
POLICY_VERSION_CONTRACT_STATUS::DOCUMENTARY_CONTRACT_DEFINED
CURRENT_POLICY_RUNTIME_STATUS::NOT_IMPLEMENTED
SCHEMA_B_POLICY_VERSION_FIELD::authority_gate_policy_contract_version
IMPLEMENTATION_AUTHORIZED::NO
MIGRATION_CREATION_AUTHORIZED::NO
AUTHORITY_GATE_IMPLEMENTATION_AUTHORIZED::NO
GEO_IMPLEMENTATION_AUTHORIZED::NO
CUTOVER_AUTHORIZED::NO
A5B_STATUS::NOT_DEMONSTRATED
B6_STATUS::NOT_DEFINED
```

The contract is ready for independent documentary audit. Schema B design may
resume after this contract is independently audited and, if approved,
published.

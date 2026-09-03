# MCM-WQ Authority Content-Hash Verification Contract

## Status and authority boundary

This is one canonical documentary contract for future authority-artifact
content-hash verification in MCM-WQ. It records a technical contract only;
it does not implement runtime behavior, SQL, migrations, an Authority Gate,
GEO behavior, or cutover.

```text
CONTRACT_STATUS::DOCUMENTARY_CONTRACT_DEFINED
RUNTIME_STATUS::NOT_IMPLEMENTED
SOURCE_POLICY::MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT
SOURCE_CONTRACT_ANALYSIS::AUTHORITY_CONTENT_HASH_VERIFICATION_CONTRACT_DEFINITION
INDEPENDENT_AUDIT_RESULT::PASS_WITH_REQUIRED_HASH_CONTRACT_CORRECTIONS
```

The lifecycle policy remains the source of truth for `TECHNICAL_ADMISSION_ONLY`
and conditional eligibility. This contract is subordinate to that policy and
must not be read as domain, scientific, legal, regulatory, institutional, or
normative authority.

```text
A5B_STATUS::NOT_DEMONSTRATED
B6_STATUS::NOT_DEFINED
AUTHORITY_GATE_IMPLEMENTATION_AUTHORIZED::NO
IMPLEMENTATION_AUTHORIZED::NO
```

## Hashed object and custody

The verification object is exactly one `PACKAGED_REFERENCE_ARTIFACT`: a
repository-controlled authority artifact identified by `artifact_id` and
`artifact_version`.

```text
MCM_CONTROLLED_IMMUTABLE_ARTIFACT_CUSTODY::REQUIRED_FUTURE_CAPABILITY
GENERALIZED_ARTIFACT_STORE_REQUIRED::NO
```

The contract does not require a generalized artifact-management platform. It
does require a future MCM-controlled custody mechanism that makes the bound
artifact identity and bytes write-once or content-addressed.

Live remote representations are not admissible verification objects. Remote
URLs may remain documentary provenance metadata, but a mutable live URL is not
a frozen verification input.

## Canonical bytes and digest

The hash input is the exact raw byte sequence of the packaged artifact.

The following transformations are prohibited before hashing:

- text-mode conversion;
- newline normalization;
- encoding conversion;
- parsing or reserialization;
- semantic normalization;
- inclusion of filesystem metadata, path names, or timestamps.

```text
DIGEST_ALGORITHM::SHA-256
ALGORITHM_ID::sha-256/v1
DIGEST_ENCODING::LOWERCASE_ASCII_HEXADECIMAL
DIGEST_LENGTH::64
DIGEST_CHARACTER_SET::[0-9a-f]
```

Expected and computed digests must use this canonical representation before
comparison. `sha-256/v1` is an explicit MCM authority-artifact decision; it is
not inherited from governed-rule payload hashing.

## Expected-digest SSoT and artifact binding

The sole authoritative expected digest is:

```text
EXPECTED_DIGEST_SOT::governed_authority.content_hash
```

It is the expected digest for the immutable artifact bound to the exact
`authority_id + authority_version`.

The binding invariant is:

```text
authority_id + authority_version
  -> exactly one artifact_id + artifact_version + expected_digest
```

The binding becomes immutable no later than successful authority publication.
Changing artifact bytes while retaining the same governed binding is
prohibited. A content change requires a new governed artifact identity/version
and, where authority semantics or content change, the appropriate new authority
version.

One immutable artifact may be reused by multiple authority versions only when
each authority version is explicitly and independently bound to that artifact
and carries its governed expected digest. A one-to-one artifact-to-authority
constraint is not required by this contract.

## Artifact immutability

The current MCM runtime does not enforce this contract. The future invariant is:

```text
for a given artifact_id + artifact_version:
artifact byte sequence is WRITE_ONCE_OR_IMMUTABLE
```

Future implementation must either prevent mutation or make any mutation create
a new artifact identity/version. A label that merely says `immutable` is not
sufficient evidence.

## Legacy authority-reference hashes

`authority_reference.content_hash` is legacy, non-authoritative metadata. It
cannot independently satisfy `CONTENT_HASH_VERIFIED` and cannot create a second
Source of Truth.

```text
UNLINKED + missing       => ignored for positive admission
UNLINKED + equal         => metadata only
UNLINKED + different     => metadata only; no automatic conflict
LINKED + equal           => consistent metadata
LINKED + different       => PROVENANCE_CONFLICT => BLOCKED
```

Linkage must be explicit. It must never be inferred from a similar locator,
digest, title, URL, or content.

## Verification contract and evidence

```text
VERIFICATION_CONTRACT_VERSION::mcm-authority-artifact-hash/v1
```

Future immutable verification evidence must contain at minimum:

- `authority_id`;
- `authority_version`;
- `artifact_id`;
- `artifact_version`;
- artifact locator/reference;
- `algorithm_id`;
- `verification_contract_version`;
- `expected_digest`;
- `computed_digest`;
- `verification_result`;
- `verified_at`;
- `verification_provenance`.

`BYTE_LENGTH` is optional diagnostic evidence only. It is not an identity or
admission predicate.

`verified_at` is technical verification time and is distinct from authority
`effective_at`, measurement `measured_at`, and registration `registered_at`.
It uses the existing canonical MCM UTC grammar:

```text
YYYY-MM-DDTHH:MM:SS.ffffffZ
```

No timestamp aliasing is permitted.

## Verification timing and atomicity

Verification occurs before successful authority publication:

```text
artifact binding
  -> exact-byte retrieval
  -> digest computation
  -> expected/computed comparison
  -> immutable verification evidence
  -> authority publication
```

A positively admissible published authority must never be observable with a
missing binding, missing evidence, failed verification, digest mismatch, or
incomplete verification provenance. The artifact binding, verification,
evidence, and publication transition must satisfy this semantic atomicity
invariant. This document does not prescribe SQL implementation.

## Positive verification condition

```text
CONTENT_HASH_VERIFIED = TRUE
```

if and only if immutable evidence proves all of the following:

- exact authority identity and version;
- exact artifact identity and version;
- `algorithm_id == sha-256/v1`;
- recognized verification-contract version;
- canonical expected digest;
- canonical computed digest;
- `expected_digest == computed_digest`;
- complete and unambiguous artifact binding;
- `verification_result == VERIFIED`;
- complete immutable verification evidence.

Hash equality alone is insufficient.

## Prior verification reuse and TOCTOU

Future `evaluate_temporal()` integration need not rehash the artifact when
immutable prior verification evidence remains valid for the exact bound:

```text
authority identity/version
artifact identity/version
expected digest
algorithm
verification contract version
artifact byte identity
```

The future Authority Gate consumes this immutable evidence. If artifact
immutability or binding cannot be proven, then:

```text
CONTENT_HASH_VERIFIED != TRUE => BLOCKED
```

Prior verification is reusable only because the artifact identity/version
cannot later refer to different bytes. If that invariant becomes unproven,
the system must block and must not silently rebind stale evidence.

## Legacy policy

Existing `content_hash` values created before this contract are not evidence of
verification:

```text
HASH_PRESENT_WITHOUT_VERIFICATION_EVIDENCE
  => UNPROVEN
  => NOT_POSITIVELY_ADMITTED
  => BLOCKED
```

No historical verification may be inferred.

```text
HISTORICAL_BACKFILL_ALLOWED::NO
```

A legacy authority may receive a new explicit verification record in the
future if its exact bytes can be legitimately obtained and bound under this
contract. That record proves only that verification occurred at its explicit
`verified_at` time; it must not backdate or rewrite historical truth.

## Fail-safe behavior

Any of the following prevents `CONTENT_HASH_VERIFIED=TRUE`:

- missing or malformed expected digest;
- missing or unsupported algorithm;
- missing artifact identity/version;
- ambiguous artifact binding;
- missing artifact reference;
- missing or incomplete evidence;
- unavailable artifact;
- read/storage or hash-computation failure;
- digest mismatch;
- mutable artifact/source violation;
- verification-contract mismatch;
- linked provenance conflict;
- unexpected verification failure.

The governed outcome is:

```text
NOT_POSITIVELY_ADMITTED
  => AUTHORITY_GATE BLOCKED
  => FACTUAL_MEASUREMENT_RETAINED
  => NO_FINAL_EVALUATION
  => NO_FALLBACK
  => NO_HEURISTIC_SELECTION
```

Unexpected technical verification failures must map to:

```text
AUTHORITY_RESOLUTION_UNEXPECTED_FAILURE
  => BLOCKED
```

No uncaught generic exception may serve as a governed admission outcome.
Specific governed reason codes must be preserved whenever determinable; the
catch-all must not mask them.

## Hash firewall

`CONTENT_HASH_VERIFIED` proves only artifact byte identity and integrity under
this contract. It does not prove scientific validity, legal or regulatory
validity, institutional competence, institutional validity, or domain
correctness.

```text
A5B_STATUS::NOT_DEMONSTRATED
```

## Transaction boundaries

The future implementation must distinguish:

### Authority publication transaction

Artifact binding, verification, verification evidence, and publication must
satisfy the publication atomicity invariant.

### Evaluation transaction

The future integrated `evaluate_temporal()` path reads already-governed,
immutable verification evidence through its connection-aware transaction.
Evaluation-time rehash is not required when prior evidence remains valid. No
independent authority-side commit or re-resolution may occur during evaluation.

## Schema consequences

This document records requirements only; it does not design SQL or authorize a
migration.

```text
AUTHORITY_ARTIFACT_VERIFICATION_SCHEMA_REQUIRED::YES
EVALUATION_AUTHORITY_SNAPSHOT_SCHEMA_REQUIRED::YES
SAME_MIGRATION_REQUIRED::NOT_YET_DETERMINED
MIGRATION_018_AUTHORIZED::NO
```

These are distinct schema concerns. No migration number is assigned to
artifact-verification infrastructure here.

## Authority Gate consumption

The future Authority Gate may consume:

```text
CONTENT_HASH_VERIFIED::TRUE
```

from immutable verification evidence. The gate does not establish domain
authority and does not reinterpret artifact contents.

## Minimum future test contract

Future implementation evidence must cover:

- matching raw bytes and digest;
- digest mismatch;
- canonical lowercase digest;
- uppercase/noncanonical digest rejection;
- invalid digest length;
- missing or unsupported algorithm;
- missing or unavailable artifact;
- artifact mutation attempt;
- artifact identity/version collision;
- legacy hash without evidence;
- later explicit legacy verification without backdating;
- rejection of a mutable remote URL as verification object;
- immutable prior-verification reuse;
- linked reference hash match and conflict;
- unlinked reference hash difference without a second SSoT;
- verification-evidence immutability;
- publication atomicity;
- TOCTOU invariant;
- unexpected technical failure mapped to `BLOCKED`;
- no generic exception leakage;
- absence of positive proof blocks the gate;
- hash verification does not demonstrate A5B.

No tests are executed by this documentary materialization.

## Explicit non-goals

This document does not:

- implement authority-content verification;
- create migration 018;
- implement the Authority Gate;
- modify `evaluate_temporal()` or `record()`;
- define lifecycle admissibility matrix cells;
- define precedence, adjudication, conflict resolution, or winner selection;
- promote authority;
- establish A5B or domain validity;
- change GEO scope;
- authorize cutover, legacy removal, or production readiness.

## Traceability and current state

```text
DOCUMENTARY_SCOPE::ONE_CANONICAL_GOVERNANCE_CONTRACT
RUNTIME_CHANGED::NO
MIGRATION_CHANGED::NO
TESTS_CHANGED::NO
TESTS_EXECUTED::NO
AUTHORITY_GATE_IMPLEMENTED::NO
GEO_IMPLEMENTATION_AUTHORIZED::NO
CUTOVER_AUTHORIZED::NO
```

This document must be independently re-audited before any controlled
materialization or implementation decision.

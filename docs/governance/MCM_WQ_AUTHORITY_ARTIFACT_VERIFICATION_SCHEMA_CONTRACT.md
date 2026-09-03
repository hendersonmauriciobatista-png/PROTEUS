# MCM-WQ Authority Artifact Verification Schema Contract

## Status and scope

This document defines the minimum persistent schema contract required for
MCM_CONTROLLED_IMMUTABLE_ARTIFACT_CUSTODY and CONTENT_HASH_VERIFIED.
It is a documentary schema contract only. It does not create SQL, a migration,
runtime behavior, an Authority Gate, an evaluation snapshot, or any domain
authority.

~~~
SOURCE_POLICY::MCM_WQ_LIFECYCLE_ADMISSIBILITY_POLICY_OBJECT
SOURCE_CONTRACT::MCM_WQ_AUTHORITY_CONTENT_HASH_VERIFICATION_CONTRACT
SCHEMA_CONTRACT_STATUS::DOCUMENTARY_SCHEMA_CONTRACT_DEFINED
RUNTIME_STATUS::NOT_IMPLEMENTED
~~~

The lifecycle policy remains the Source of Truth for technical admission. This
contract is subordinate to it and must not be interpreted as scientific, legal,
regulatory, institutional, normative, or domain validity.

~~~
A5B_STATUS::NOT_DEMONSTRATED
B6_STATUS::NOT_DEFINED
IMPLEMENTATION_AUTHORIZED::NO
MIGRATION_CREATION_AUTHORIZED::NO
~~~

## Custody mechanism

~~~
CUSTODY_MECHANISM::MINIMAL_HYBRID
ARTIFACT_BYTES_CUSTODY::DATABASE_BYTES
GENERALIZED_ARTIFACT_STORE_REQUIRED::NO
~~~

The minimum mechanism is:

~~~
stable artifact_id + artifact_version
+ database-resident exact raw artifact bytes
+ immutable SHA-256 byte guard
~~~

Database-resident bytes are selected for the current local SQLite product
because they couple artifact bytes, binding, evidence, backup, restore, and
transactional publication without filesystem TOCTOU or live-remote availability
dependencies. The operational cost is database and backup growth; this design
therefore assumes bounded authority artifacts.

~~~
AUTHORITY_ARTIFACT_SIZE_PROFILE::BOUNDED
EXACT_OPERATIONAL_SIZE_LIMIT::NOT_YET_CALIBRATED
~~~

The exact size limit is an operational acceptance parameter, not a schema
semantic gap. If future artifacts exceed the bounded local-custody profile:

~~~
NEW_CUSTODY_DECISION_REQUIRED::YES
~~~

There is no automatic migration to filesystem or remote storage.

artifact_locator_reference is provenance metadata only. It is not the
evaluation-time byte source. A live remote URL is not a verification object.

## Schema objects

Exactly three new persistent objects are required:

~~~
1. authority_artifact
2. authority_artifact_binding
3. authority_artifact_verification
~~~

authority_artifact is necessary because governed_authority has no exact raw
bytes or independent artifact identity. authority_artifact_binding is
necessary to preserve legacy authorities with no fabricated binding and to
represent the authority-to-artifact relationship independently of verification
evidence. authority_artifact_verification is necessary because accepted
cryptographic evidence has its own immutable provenance and timestamp.

authority_reference cannot safely carry any of these responsibilities: it is
nullable legacy metadata and is not the governed authority SSoT. Lifecycle/event
tables cannot carry artifact bytes or verification evidence without conflating
lifecycle history and integrity proof.

## Artifact identity object

authority_artifact represents one immutable packaged authority artifact.
Conceptual fields are:

~~~
artifact_id
artifact_version
artifact_locator_reference
artifact_bytes
artifact_digest
digest_algorithm
registered_at
~~~

artifact_bytes is the exact raw byte sequence. artifact_locator_reference
records provenance/custody metadata only. artifact_digest is the computed
immutable byte guard; it is not the authoritative expected-digest SSoT.

## Artifact identity and digest roles

~~~
artifact_id + artifact_version
  => exactly one immutable raw-byte identity
~~~

The digest guards the identity but need not be the primary identity. Identical
bytes may legitimately exist under distinct governed artifact identities. No
global deduplication is required.

The digest contract is:

~~~
DIGEST_ALGORITHM::SHA-256
ALGORITHM_ID::sha-256/v1
DIGEST_ENCODING::LOWERCASE_ASCII_HEXADECIMAL
DIGEST_LENGTH::64
DIGEST_CHARACTER_SET::[0-9a-f]
~~~

The exact raw bytes must be hashed without text conversion, newline
normalization, encoding conversion, parsing, reserialization, semantic
normalization, or filesystem metadata.

## Expected-digest Source of Truth

~~~
governed_authority.content_hash
  = SOLE_AUTHORITATIVE_EXPECTED_DIGEST
~~~

The roles are distinct:

~~~
authority.content_hash
  = authoritative expected digest

artifact.artifact_digest
  = computed immutable byte guard

verification.expected_digest
  = immutable evidence copy of the authority SSoT

verification.computed_digest
  = immutable computed verification evidence
~~~

Required equality invariants are:

~~~
verification.expected_digest == governed_authority.content_hash
verification.computed_digest == authority_artifact.artifact_digest
VERIFIED => verification.expected_digest == verification.computed_digest
~~~

Any mismatch is:

~~~
PROVENANCE_CONFLICT
  => NOT_POSITIVELY_ADMITTED
  => BLOCKED
~~~

The evidence copy and artifact guard must not become competing expected-digest
Source of Truths.

## Authority-artifact binding

The binding is a dedicated relation with conceptual key and references:

~~~
authority_id + authority_version
  -> at most one artifact_id + artifact_version binding
~~~

The relation references the exact governed authority identity/version and the
exact artifact identity/version. Positive admission requires exactly one
binding. Multiple authority versions may reference the same immutable artifact.

The natural composite authority identity/version key is sufficient; a surrogate
binding_id is not required by this contract.

Verification evidence must have an exact composite relational linkage to this
binding. No evidence may exist for an authority/artifact combination that is
not the governed binding.

## Pre-publication and post-publication policy

There are no independently durable draft bindings. For a new governed
publication, the following must participate in one transaction:

~~~
artifact exists or is created
  -> authority identity/scope/boundary registered
  -> binding created
  -> accepted VERIFIED evidence created
  -> PUBLISHED state/event created
  -> commit
~~~

The authority row must exist before a foreign-keyed binding can reference it;
authority identity registration is distinct from the PUBLISHED lifecycle
transition. The required invariant concerns committed visibility, not literal
statement order.

Failure before commit produces full rollback. No durable partial binding,
verification evidence, or publication state is left by a failed pre-publication
workflow.

After committed governed publication:

~~~
binding::append_only_and_immutable
artifact binding::no update/rebinding/delete
~~~

A legacy authority may later acquire exactly one explicit artifact binding and
verification evidence through a governed explicit-verification operation. This
does not rewrite or backdate lifecycle history.

## Verification evidence object

authority_artifact_verification contains only authoritative positive evidence.
Conceptual fields are:

~~~
verification_id
authority_id
authority_version
artifact_id
artifact_version
algorithm_id
verification_contract_version
expected_digest
computed_digest
verification_result
verified_at
verification_provenance
~~~

The authority/artifact fields are immutable evidence values as well as exact
composite references to the binding and artifact. This makes the evidence
self-describing while preserving relational integrity.

## Verification result and version cardinality

The authoritative evidence object permits only:

~~~
verification_result::VERIFIED
~~~

Failed attempts do not enter this object. Diagnostic failed-attempt
persistence is outside this schema unless a separate governed requirement is
approved.

The cardinality is:

~~~
AT_MOST_ONE accepted VERIFIED evidence record
per authority binding + verification_contract_version
~~~

The current contract is:

~~~
VERIFICATION_CONTRACT_VERSION::mcm-authority-artifact-hash/v1
~~~

A later recognized contract version may produce a new immutable VERIFIED record
for the same binding. The future Authority Gate must request the exact
recognized contract version required by its policy. It must not choose a winner
among contract versions. Duplicate accepted evidence for the same binding and
required version is:

~~~
AMBIGUOUS_PROOF => BLOCKED
~~~

verification_id is globally unique and immutable. It is the sole immutable
identifier handed to the future evaluation authority snapshot for hash-proof
provenance.

## Verification time

~~~
verified_at::YYYY-MM-DDTHH:MM:SS.ffffffZ
~~~

verified_at is immutable technical verification time and must remain distinct
from:

~~~
effective_at
measured_at
registered_at
~~~

## Immutability enforcement responsibility

Minimum future enforcement is:

~~~
artifact identity uniqueness
  => DB primary/unique key

artifact bytes immutability
  => DB trigger + transaction

artifact digest immutability
  => DB trigger + service

bytes/digest equality
  => service cryptographic computation

binding cardinality
  => DB primary/unique constraint

post-publication binding immutability
  => DB trigger

verification evidence immutability
  => DB trigger

canonical digest format
  => DB constraint + service

canonical verified_at
  => DB constraint + service

recognized algorithm/contract version
  => DB constraint + service

orphan prevention
  => foreign keys; deferred only where transaction topology requires

verification.expected_digest == governed_authority.content_hash
  => combined DB/service guard

PUBLISHED requires valid proof
  => combined transaction/persistence guard
~~~

No SQL syntax is defined here.

## Publication atomicity

The committed-state invariant is:

~~~
POSITIVELY_ADMISSIBLE_PUBLISHED_AUTHORITY
requires atomically consistent:
authority identity
artifact
binding
accepted VERIFIED evidence
publication lifecycle transition
~~~

Deferred relational validation, database immutability guards, and service
transaction orchestration are conceptually sufficient. Existing legacy
PUBLISHED authorities must remain representable and must not be rejected
retroactively at migration/storage level. They remain unverified until explicit
proof exists.

## Legacy compatibility

Existing authorities with content_hash but no binding/evidence remain valid
stored legacy state:

~~~
LEGACY_CONTENT_HASH_WITHOUT_BINDING_OR_EVIDENCE
  => STORED_LEGACY_STATE_VALID
  => CONTENT_HASH_VERIFIED != TRUE
  => BLOCKED
~~~

No artifact identity, artifact bytes, computed digest, verified_at, or
verification evidence may be fabricated. Historical backfill is prohibited.

~~~
HISTORICAL_BACKFILL_ALLOWED::NO
~~~

Future explicit legacy verification uses actual verification time and does not
rewrite lifecycle history.

## Authority-reference legacy hash

~~~
authority_reference.content_hash
  = LEGACY_NON_AUTHORITATIVE_METADATA
~~~

It is not an FK or Source of Truth for this schema. No schema extension is
required now solely for legacy reference conflict detection. Unlinked metadata
differences cannot independently block or admit the authority. Explicitly
linked mismatch may be treated as provenance conflict by future governed logic.

## Relational proof for CONTENT_HASH_VERIFIED

The future Authority Gate must deterministically establish exactly one accepted
proof for the required contract version:

~~~
governed_authority
  -> exactly one authority_artifact_binding
  -> exactly one immutable authority_artifact
  -> exactly one accepted verification evidence
~~~

The proof must establish:

- same authority identity/version across all relations;
- same artifact identity/version across all relations;
- complete and unique binding;
- authority.content_hash == verification.expected_digest;
- artifact.artifact_digest == verification.computed_digest;
- expected digest equals computed digest;
- recognized sha-256/v1 and verification contract version;
- canonical digest and timestamp formats;
- immutable accepted evidence;
- exact composite evidence-to-binding linkage;
- no ambiguity or orphan relation.

No live remote fetch or evaluation-time verification commit is permitted.

## TOCTOU chain

~~~
database raw bytes
  -> immutable artifact identity/version
  -> immutable artifact_digest
  -> immutable binding
  -> immutable accepted evidence
  -> immutable verification_id
  -> evaluation consumption
~~~

Any mutable dependency capable of changing the meaning of historical evidence
is prohibited. Runtime enforcement remains future work.

## Migration boundary

The repository sequence ends at migration 017. If authorized, the next number
would be:

~~~
NEXT_MIGRATION_NUMBER_IF_AUTHORIZED::018
MIGRATION_018_LOGICAL_SCOPE::AUTHORITY_ARTIFACT_VERIFICATION_INFRASTRUCTURE_ONLY
MIGRATION_018_AUTHORIZED::NO
~~~

Migration 018 must not include the evaluation authority snapshot merely for
numbering convenience. The snapshot is a separate schema concern and consumes
the stable verification_id reference defined here.

Future migration compatibility must prove:

- fresh 001→018 migration;
- persisted 017→018 migration;
- legacy and legacy PUBLISHED rows retained;
- no inferred proof;
- no destructive rewrite of migrations 013–017;
- transactional rollback;
- no foreign-key or trigger bypass.

~~~
REAL_EXTERNAL_DB_COMPATIBILITY::UNPROVEN
~~~

## Future model, repository, and service surface

Conceptual model types are:

~~~
GovernedAuthorityArtifact
AuthorityArtifactBinding
AuthorityArtifactVerification
~~~

Future repository operations are limited to:

- create/fetch immutable artifact;
- create/fetch binding;
- record/fetch accepted verification evidence;
- execute a connection-aware CONTENT_HASH_VERIFIED proof query.

Future service behavior is limited to:

- exact-byte SHA-256 computation;
- artifact/binding/evidence/publication orchestration;
- explicit legacy verification;
- deterministic failure translation;
- no live remote verification during evaluation.

No runtime implementation is authorized by this document.

## Future schema test contract

TEST_CONTRACT_CORRECTIONS::

Future tests must cover:

- database byte-for-byte artifact round trip;
- backup/restore preserving exact bytes and digest;
- artifact identity/version uniqueness;
- artifact mutation prevention;
- binding cardinality and immutability;
- pre-publication failure and full rollback;
- authority identity registration before publication state;
- post-publication immutability;
- verification evidence immutability;
- canonical digest, algorithm, and contract version;
- canonical verified_at;
- digest mismatch cannot create VERIFIED evidence;
- cross-row expected-digest SSoT mismatch;
- exact composite evidence-to-binding linkage;
- orphan binding/evidence prevention;
- accepted evidence uniqueness by contract version;
- explicit re-verification under a later contract version;
- duplicate same-version accepted evidence blocked/prevented;
- no publication with missing accepted evidence;
- legacy PUBLISHED rows survive migration;
- legacy PUBLISHED without proof remains BLOCKED;
- no backdating;
- stable verification_id;
- TOCTOU chain stability;
- fresh and persisted-017 migration paths;
- rollback;
- preservation of the A5B firewall.

No tests are executed by this documentary operation.

## Explicit non-goals

This contract does not:

- design SQL syntax;
- create migration 018;
- design the evaluation authority snapshot;
- implement artifact custody or verification;
- implement the Authority Gate;
- define lifecycle admissibility matrix cells;
- define B6 precedence, adjudication, conflict resolution, or winner selection;
- establish A5B or domain validity;
- change GEO scope;
- authorize cutover, legacy removal, or production readiness.

~~~
A5B_STATUS::NOT_DEMONSTRATED
B6_STATUS::NOT_DEFINED
IMPLEMENTATION_AUTHORIZED::NO
MIGRATION_CREATION_AUTHORIZED::NO
AUTHORITY_GATE_IMPLEMENTATION_AUTHORIZED::NO
GEO_IMPLEMENTATION_AUTHORIZED::NO
CUTOVER_AUTHORIZED::NO
~~~

## Contract closure

The following schema-semantic decisions are closed by this document:

~~~
CUSTODY_MECHANISM::MINIMAL_HYBRID
ARTIFACT_BYTES_CUSTODY::DATABASE_BYTES
SCHEMA_OBJECT_COUNT::3
EXPECTED_DIGEST_SOT::governed_authority.content_hash
BINDING_CARDINALITY::AT_MOST_ONE; EXACTLY_ONE_FOR_POSITIVE_ADMISSION
VERIFICATION_RESULT::VERIFIED_ONLY
VERIFICATION_VERSION_CARDINALITY::ONE_PER_BINDING_PER_CONTRACT_VERSION
PUBLICATION_ATOMICITY::REQUIRED
LEGACY_COMPATIBILITY::PRESERVED
CONTENT_HASH_VERIFIED_PROOF::DETERMINISTIC_JOINED_IMMUTABLE_EVIDENCE
EVALUATION_REFERENCE::verification_id
~~~

Exact SQL syntax, index syntax, trigger syntax, migration execution, and
service implementation details remain deferred implementation-design work; they
do not reopen the semantic schema contract.

~~~
DOCUMENTARY_STATUS::CORRECTED_NOT_MATERIALIZED
READY_FOR_INDEPENDENT_DOCUMENTARY_REAUDIT::YES
~~~

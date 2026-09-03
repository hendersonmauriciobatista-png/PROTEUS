# MCM-WQ Authority Artifact Verification Schema A Physical Implementation Design

## Identity and boundary

DOCUMENT_CLASS::PHYSICAL_IMPLEMENTATION_DESIGN_CONTRACT
OBJECT::MCM_WQ_AUTHORITY_ARTIFACT_VERIFICATION_SCHEMA_A
STATUS::DESIGN_CLOSED_IMPLEMENTATION_NOT_AUTHORIZED
AUTHORITATIVE_BASELINE::a7e5ea68c579773579cef4c4053e8fac2640cd49
PRIMARY_SSoT::MCM_WQ_AUTHORITY_ARTIFACT_VERIFICATION_SCHEMA_CONTRACT
SCHEMA_B_CONTRACT::MCM_WQ_EVALUATION_AUTHORITY_SNAPSHOT_SCHEMA_CONTRACT
IMPLEMENTATION_AUTHORIZED::NO
MIGRATION_018_AUTHORIZED::NO
MIGRATION_019_AUTHORIZED::NO

This documentary contract materializes the independently audited physical implementation design for Schema A. It authorizes no implementation, migration, runtime behavior, Schema B, Authority Gate, A5B, B6, GEO, cutover, or production readiness, and introduces no new semantic policy decision.

The primary SSoT remains MCM_WQ_AUTHORITY_ARTIFACT_VERIFICATION_SCHEMA_CONTRACT.

## 1. Exactly three persistent objects

authority_artifact
authority_artifact_binding
authority_artifact_verification

No fourth persistent object is required.

## 2. authority_artifact

Candidate physical columns:

artifact_id TEXT NOT NULL
artifact_version INTEGER NOT NULL CHECK (artifact_version > 0)
artifact_locator_reference TEXT NOT NULL
artifact_bytes BLOB NOT NULL
artifact_digest TEXT NOT NULL
digest_algorithm TEXT NOT NULL
registered_at TEXT NOT NULL
PRIMARY KEY (artifact_id, artifact_version)

artifact_bytes is true SQLite BLOB custody of the exact raw byte sequence. Identity/version, bytes, digest, and locator metadata are immutable. Changed bytes require a new artifact identity/version. No normalization, encoding or newline conversion, parsing, reserialization, or remote byte substitution is permitted. registered_at is custody registration time only.

The semantic-role separation is explicit:

    registered_at != effective_at
    registered_at != measured_at
    registered_at != verified_at

These inequalities distinguish governed event roles. They do not require
different physical timestamp values when independently governed events
legitimately occur at the same instant. No field substitutes for another, no
timestamp is inferred from another, and no backdating is permitted.

The four timestamp roles are:

    registered_at = artifact custody registration time
    verified_at = actual artifact verification time
    effective_at = authority lifecycle effective time
    measured_at = governed measurement time

The bounded-artifact operational assumption remains uncalibrated. Exceeding it requires a separate custody decision; there is no automatic filesystem or remote-storage fallback.

## 3. Digest and algorithm

For accepted evidence:

authority_artifact.digest_algorithm
==
authority_artifact_verification.algorithm_id
==
sha-256/v1

Digest roles remain distinct:

governed_authority.content_hash = sole expected-digest SSoT
authority_artifact.artifact_digest = computed exact-byte guard
authority_artifact_verification.expected_digest = immutable SSoT evidence copy
authority_artifact_verification.computed_digest = immutable computed evidence

Required equalities:

verification.expected_digest == governed_authority.content_hash
verification.computed_digest == authority_artifact.artifact_digest
verification.expected_digest == verification.computed_digest

Digests are lowercase ASCII hexadecimal, exactly 64 characters, restricted to [0-9a-f]. Crypto computes SHA-256 over exact raw BLOB bytes. Database cross-row triggers/guards and service validation enforce the invariant; it is not delegated to impossible SQLite cross-table CHECK logic.

## 4. authority_artifact_binding

authority_id TEXT NOT NULL
authority_version INTEGER NOT NULL
artifact_id TEXT NOT NULL
artifact_version INTEGER NOT NULL
PRIMARY KEY (authority_id, authority_version)
UNIQUE (authority_id, authority_version, artifact_id, artifact_version)

Foreign keys:

(authority_id, authority_version) -> governed_authority(authority_id, authority_version)
(artifact_id, artifact_version) -> authority_artifact(artifact_id, artifact_version)

An authority identity/version has at most one explicit binding; positive admission requires exactly one. Immutable artifacts may be explicitly shared by multiple authority versions. No binding is inferred from hash, URL, title, locator, filename, or metadata.

## 5. authority_artifact_verification

Required non-null fields:

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
PRIMARY KEY (verification_id)

The authority/artifact columns have an exact composite foreign key to the binding's four-column unique key. verification_id is globally unique and immutable. Only verification_result = VERIFIED is stored in the authoritative evidence object; failed attempts are outside this schema.

At most one accepted record is allowed per authority binding and recognized verification contract version:

UNIQUE(authority_id, authority_version, verification_contract_version)
VERIFICATION_CONTRACT_VERSION::mcm-authority-artifact-hash/v1

Later separately governed contract versions may create new immutable evidence. No winner, precedence, or adjudication is defined.

## 6. Locator and provenance

The authoritative immutable locator path is:

authority_artifact_verification
  -> authority_artifact_binding
  -> authority_artifact
  -> artifact_locator_reference

verification_provenance separately records provenance of the verification operation. The locator is provenance metadata only, never an evaluation-time byte source. No duplicated locator, live-source inference, remote retrieval, or evaluation-time rehash is permitted.

## 7. verified_at

verified_at TEXT NOT NULL
FORMAT::YYYY-MM-DDTHH:MM:SS.ffffffZ

Reuse proven migration 016/017 validation semantics: UTC Z, six microseconds, valid calendar and leap year, hour 00-23, minute 00-59, second 00-59, and no leap seconds.

    verified_at != effective_at
    verified_at != measured_at
    verified_at != registered_at

These inequalities express semantic-role separation only; they do not require
different physical timestamp values when independently governed events occur at
the same instant. verified_at remains actual artifact verification time and is
not inferred from any other timestamp. No field substitutes for another, no
timestamp is inferred from another, and no backdating is permitted.

## 8. Immutability and enforcement split

The database must reject UPDATE and DELETE for all three Schema A objects. Existing governed_authority.content_hash immutability remains part of the proof chain; digest equality alone does not establish storage immutability.

DATABASE: keys, foreign keys, uniqueness, canonical guards, cross-row guards, immutability triggers, publication guards.
SERVICE: raw-byte handling, validation, binding, contract validation, transaction orchestration.
CRYPTO: SHA-256 exact-byte computation and digest comparison.

## 9. Publication transaction

artifact
  -> governed_authority registration
  -> authority scope/boundary
  -> binding
  -> accepted VERIFIED evidence
  -> authority_state = PUBLISHED
  -> PUBLISHED authority_event
  -> commit

One connection and one outer transaction owner are required. No nested commits or independent publication connection are permitted. Any failure rolls back the complete transaction. A newly governed positively admissible PUBLISHED authority must not become durably observable without successful proof.

AUTHORITY_REGISTRATION != AUTHORITY_PUBLICATION. The current create_authority() combines these phases and requires a future connection-aware adaptation. Uncommitted registration may temporarily lack lifecycle state, but no invalid intermediate state may be durably committed.

## 10. Legacy compatibility

Existing legacy PUBLISHED authorities survive migration unchanged. No artifact, bytes, digest, binding, verification, verified_at, or historical lifecycle state may be fabricated. Historical backfill is prohibited.

legacy authority without actual proof:
  stored::YES
  CONTENT_HASH_VERIFIED::NO

Later explicit verification is allowed only with real bytes, real proof, and actual verification time. No backdating or lifecycle rewrite.

## 11. Schema B handoff

Schema B consumes only verification_id. Immutable relational traversal obtains the verification, binding, artifact, and authority identity/version. Schema B does not fetch live bytes, retrieve a remote locator, rehash at evaluation time, or duplicate digest evidence.

## 12. Prospective migration 018

018 = AUTHORITY_ARTIFACT_VERIFICATION_INFRASTRUCTURE_ONLY
MIGRATION_018_AUTHORIZED::NO

If separately authorized, migration 018 may contain only Schema A tables, indexes, checks, foreign keys, and triggers. It must not contain Schema B, evaluation snapshots, Authority Gate runtime, GEO, B6, A5B, cutover, or unrelated cleanup. Migration 018 does not currently exist.

The design supports fresh 001->018, persisted 017->018, rollback with no partial Schema A or false migration record, and legacy preservation.

## 13. Future implementation surface

migrations/018_mcm_wq_authority_artifact_verification.sql
governed_core/authority_models.py
governed_core/repository.py
governed_core/authority_service.py
targeted artifact-verification tests

No Schema A change is required in evaluation_service.py, measurement_models.py, rule_service.py, or migrations 013-017. These are future requirements, not current functionality.

## 14. Future test contract

Future tests must cover:

- fresh 001->018, persisted 017->018, rollback, and no false migration record;
- legacy PUBLISHED survival and no fabricated backfill;
- raw binary BLOB round trip, byte identity, backup/restore, digest validation, and mismatch rejection;
- artifact, binding, and verification immutability;
- artifact sharing, binding uniqueness, exact composite linkage, and orphans;
- same-version uniqueness and later-contract-version reverification;
- canonical verified_at, invalid calendar, and invalid leap-year rejection;
- registration/publication separation, atomic publication, and all failure rollbacks;
- no nested transaction;
- expected-digest immutability after verification;
- algorithm equality and mismatch rejection;
- Schema B verification_id handoff;
- deterministic failure mapping with no generic exception leakage;
- A5B and B6 firewall preservation.

TESTS_EXECUTED::NO

## 15. Failure firewall

technical proof failure
  -> NOT_POSITIVELY_ADMITTED
  -> BLOCKED
  -> factual measurement retained
  -> no final evaluation row
  -> no fallback
  -> no heuristic selection

Authority proof failure never becomes NAO_AVALIAVEL.

## 16. A5B and B6 boundaries

A5B_STATUS::NOT_DEMONSTRATED
B6_STATUS::NOT_DEFINED

Artifact/hash proof establishes technical identity, integrity, and provenance only. It does not establish scientific, legal, regulatory, institutional, normative, or domain validity. No ranking, precedence, winner selection, adjudication, or conflict resolution is defined.

## 17. Limitations and current truth

SCHEMA_A_CONTRACT_PUBLISHED::YES
SCHEMA_A_PHYSICAL_DESIGN_CLOSED::YES
SCHEMA_A_PHYSICAL_DESIGN_INDEPENDENTLY_REAUDITED::YES
SCHEMA_B_CONTRACT_PUBLISHED::YES
PRODUCTION_READINESS::NO
CUTOVER_READINESS::NO
REAL_EXTERNAL_DB_COMPATIBILITY::UNPROVEN
BOUNDED_ARTIFACT_OPERATIONAL_SIZE_LIMIT::UNCALIBRATED
SCHEMA_A_RUNTIME_IMPLEMENTED::NO
SCHEMA_A_PHYSICAL_TABLES_EXIST::NO
MIGRATION_018_EXISTS::NO
SCHEMA_B_RUNTIME_IMPLEMENTED::NO
AUTHORITY_GATE_RUNTIME_IMPLEMENTED::NO
IMPLEMENTATION_AUTHORIZED::NO
MIGRATION_018_AUTHORIZED::NO
MIGRATION_019_AUTHORIZED::NO
AUTHORITY_GATE_IMPLEMENTATION_AUTHORIZED::NO
GEO_IMPLEMENTATION_AUTHORIZED::NO
CUTOVER_AUTHORIZED::NO

This is a closed documentary design contract, not an implementation, authorization, production-readiness claim, or runtime capability publication.

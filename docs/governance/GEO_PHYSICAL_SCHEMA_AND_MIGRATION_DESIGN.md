# PROTEUS — GEO Physical Schema and Migration Design

## Governed status

| Field | Value |
|---|---|
| Case | `PROTEUS` |
| Object | `GEO_PHYSICAL_SCHEMA_AND_MIGRATION_DESIGN` |
| Baseline | `2014958aeec254e0d80eb85e639634d0916e583f` |
| Semantic authority | `docs/governance/GEO_SEMANTIC_MODEL_AND_SCHEMA_STRATEGY.md` |
| Scope authority | `docs/governance/FINAL_PRODUCT_SCOPE.md` |
| Design status | `APPROVED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION_REVIEW` |
| Migration | `020_FUTURE_GEO_NORMALIZATION` |
| Implementation authorization | `NO` |
| A5B | `NOT_DEMONSTRATED` |
| Map with pins | `OPTIONAL_FUTURE_ENHANCEMENT` |
| Cutover | `NOT_AUTHORIZED` |

This document closes the physical schema and migration design for the approved
GEO semantic contract. It does not create SQL, change runtime behavior, install
dependencies, or authorize implementation.

The documentary chain remains:

`OFFICIAL_SOURCE → RESEARCH_FINDING → SEMANTIC_AUTHORITY → PHYSICAL_DESIGN`

The approved semantic authority remains authoritative for meaning. This record
is authoritative only for the bounded physical implementation contract.

## Non-negotiable preservation rules

- `POINT_CONTEXT_REVISION` remains the sole temporal authority.
- GEO introduces no independent temporal intervals.
- `measured_at` resolves the historical context and its GEO reference.
- Existing `point_context_revision.geo_reference TEXT` values are preserved
  unchanged and are never interpreted or backfilled semantically.
- Historical measurements are never rewritten.
- Authority Gate, Schema A, Schema B, A5B, B6, alerts, events, actions, map UI,
  and cutover remain outside this design.
- Migration 019 is unchanged.

## 1. CRS resolver decision

### Selected deterministic provider

The implementation provider is:

`pyproj==3.7.2`

The supported implementation runtime is Python 3.12. The release manifest must
pin the platform wheel hash and record the runtime values returned by
`pyproj.show_versions()`, including the PROJ runtime and database versions.
The current verified development interpreter is Python 3.12.10; the final
delivery manifest must identify the exact supported interpreter artifact.

The provider choice is an implementation design decision, not Brazilian domain
authority. It is based on the provider's CRS and transformation APIs. The
official documentation exposes `Transformer.from_crs`, `always_xy`, and
strict transformation options; it also states that transformation grids are
not included in pyproj 3 wheels. References:

- https://pyproj4.github.io/pyproj/stable/api/transformer.html
- https://pyproj4.github.io/pyproj/stable/transformation_grids.html
- https://pyproj4.github.io/pyproj/stable/_modules/pyproj/_show_versions.html

### Reproducibility contract

- `pyproj` version is pinned exactly to `3.7.2`.
- The release contains a platform-specific dependency lock with artifact
  hashes; an unpinned installation is not a supported deployment.
- The PROJ data directory is a bundled, versioned release artifact with a
  manifest containing SHA-256 hashes for `proj.db` and every transformation
  grid used by the supported product paths.
- `PROJ_NETWORK=OFF` is mandatory. No runtime grid download or live network
  lookup is permitted.
- Startup records and validates the pyproj, PROJ runtime, PROJ database, and
  bundled-data manifest versions. A mismatch is a deployment failure.
- The implementation must not use an ambient system PROJ installation or
  ambient system data directory as a fallback.

### Resolver and transformer separation

`CRSResolver` and `CoordinateTransformer` are separate interfaces:

```text
CRSResolver.resolve(identifier)
  → RESOLVED_CRS | CRS_UNRESOLVED

CoordinateTransformer.transform(source_crs, target_crs, source_pair)
  → TRANSFORMED_COORDINATE | TRANSFORMATION_UNAVAILABLE
```

The resolver validates that the identifier is explicit, parseable, and
resolvable by the pinned local provider. For an `AVAILABLE` record, the target
CRS must be a resolvable two-dimensional geographic CRS whose output is
explicitly interpreted as latitude/longitude for storage.

The transformer uses the pinned provider with:

- `always_xy=True` at the provider boundary;
- explicit application conversion to stored latitude, longitude order;
- `only_best=True`;
- `allow_ballpark=False`;
- no heuristic operation selection;
- no silent source or target CRS substitution.

When source and target CRS differ, transformation method and provenance are
required. If the required operation or grid is unavailable locally, the write
does not become `AVAILABLE`; it is rejected or recorded as `UNVERIFIED` with
typed reason `TRANSFORMATION_UNAVAILABLE`.

### CRS failure semantics

`AVAILABLE` requires successful source CRS resolution, target CRS resolution,
axis validation, and any required transformation. The following are typed
failures, never fallbacks:

- `CRS_UNRESOLVED`;
- `CRS_NOT_GEOGRAPHIC_LATLON`;
- `CRS_AXIS_ORDER_UNRESOLVED`;
- `TRANSFORMATION_UNAVAILABLE`;
- `TRANSFORMATION_PROVENANCE_MISSING`.

SIRGAS2000 remains the preferred target for newly controlled Brazilian data,
not a universal default. A non-SIRGAS source is valid when explicitly resolved
and governed. An unknown or unresolvable CRS cannot be silently relabeled.

## 2. Context/GEO cardinality decision

The design uses database-enforced ownership with a bidirectional deferred
identity link. This closes the direct-SQL reverse-cardinality gap without
adding a second temporal authority.

### Identity link

`point_context_revision` receives an additive `geo_reference_id` column with a
deferrable foreign key to `geo_reference.geo_reference_id`.

`geo_reference` contains:

- `context_revision_id NOT NULL`;
- `UNIQUE(context_revision_id)`;
- a deferrable foreign key to `point_context_revision.context_revision_id`.

The two links are checked by insert/update triggers so that a parent context
cannot point to a GEO row belonging to another context. The parent link is
immutable after creation. Existing rows are populated transactionally by
migration 020; new rows require a non-null matching link.

### Resulting cardinality

- One context revision has exactly one GEO classification after migration 020.
- One context revision can have no more than one GEO row.
- One GEO row belongs to exactly one context revision.
- One provenance row may be referenced by multiple immutable GEO rows, but each
  `AVAILABLE` or `UNVERIFIED` GEO row must have a provenance reference.
- A measurement resolves one context revision and therefore one GEO row at its
  `measured_at` instant.

### Creation and succession transaction invariant

Context creation and context succession must write the complete identity unit
in one transaction:

```text
POINT / provenance (when needed)
→ GEO_REFERENCE
→ POINT_CONTEXT_REVISION with geo_reference_id
→ current-context reference / governance event
→ COMMIT
```

The child GEO foreign key is deferred so a new GEO row may be inserted before
its new context row. The parent foreign key is also deferred. Commit fails if
either side is absent or cross-linked.

Direct SQL is governed by the same constraints:

- context insertion without a matching GEO link is rejected;
- a mismatched GEO/context pair is rejected;
- a second GEO for one context is rejected;
- changing the GEO link is rejected;
- orphaned deferred rows fail at commit.

## 3. Physical provenance model

### `location_provenance`

| Column | Type | Nullability / rule |
|---|---|---|
| `provenance_id` | `TEXT` | primary key, nonempty |
| `source_reference` | `TEXT` | required, nonempty; not an Authority Gate reference |
| `source_coordinate_1_raw` | `TEXT` | required, nonempty; preserved source value |
| `source_coordinate_2_raw` | `TEXT` | required, nonempty; preserved source value |
| `source_coordinate_1_numeric` | `REAL` | nullable; required for accepted transformation |
| `source_coordinate_2_numeric` | `REAL` | nullable; required for accepted transformation |
| `source_axis_order` | `TEXT` | required: `LATITUDE_LONGITUDE`, `LONGITUDE_LATITUDE`, `SOURCE_DECLARED_AXES`, or `UNKNOWN` |
| `source_crs_identifier` | `TEXT` | required, nonempty; never defaulted |
| `acquisition_method` | `TEXT` | nullable, nonempty when supplied |
| `captured_at` | `TEXT` | nullable canonical UTC timestamp |
| `captured_at_status` | `TEXT` | required: `KNOWN` or `UNKNOWN` |
| `transformation_method` | `TEXT` | nullable; required when CRS transformation occurs |
| `transformation_parameters` | `TEXT` | nullable, opaque provider metadata |
| `transformation_provenance` | `TEXT` | nullable; required with transformation method |
| `accuracy_or_uncertainty_kind` | `TEXT` | nullable: `ACCURACY` or `UNCERTAINTY` |
| `accuracy_or_uncertainty_value` | `REAL` | nullable, finite and nonnegative |
| `accuracy_or_uncertainty_unit` | `TEXT` | nullable, required when value/kind supplied |
| `registered_at` | `TEXT` | required canonical UTC timestamp |

Required cross-field checks:

- `captured_at_status=KNOWN` requires `captured_at`; `UNKNOWN` requires null
  `captured_at`.
- Numeric source coordinates, when supplied, are finite; no geographic bounds
  are applied because the source CRS may be projected.
- Accuracy fields are either all null or all populated.
- Transformation provenance and method are either both null or both populated.
- `AVAILABLE` requires numeric source coordinates and a known source axis order.
- Raw source coordinate values remain available even when numeric parsing or
  transformation fails.

All provenance updates and deletes are rejected. Provenance is insert-only.

### `geo_reference`

| Column | Type | Nullability / rule |
|---|---|---|
| `geo_reference_id` | `TEXT` | primary key, nonempty |
| `context_revision_id` | `TEXT` | required, unique, deferred FK |
| `availability_state` | `TEXT` | required: `AVAILABLE`, `UNAVAILABLE`, `UNVERIFIED`, or `LEGACY_UNCLASSIFIED` |
| `latitude` | `REAL` | required only for `AVAILABLE` |
| `longitude` | `REAL` | required only for `AVAILABLE` |
| `crs_identifier` | `TEXT` | required only for `AVAILABLE`, nonempty |
| `location_provenance_id` | `TEXT` | required for `AVAILABLE` and `UNVERIFIED` |
| `state_reason` | `TEXT` | required and nonempty for non-available states |
| `registered_at` | `TEXT` | required canonical UTC timestamp |

Canonical coordinate checks:

- numeric and finite;
- latitude in `[-90, 90]`;
- longitude in `[-180, 180]`;
- stored order is latitude then longitude;
- no fixed decimal scale;
- `0,0` is data, never an absence sentinel.

State checks:

```text
AVAILABLE
  latitude + longitude + CRS + provenance present
  state_reason absent

UNAVAILABLE
  canonical coordinates + CRS + provenance absent
  nonempty state_reason present

UNVERIFIED
  canonical coordinates + canonical CRS absent
  provenance + nonempty state_reason present

LEGACY_UNCLASSIFIED
  canonical coordinates + CRS + provenance absent
  nonempty state_reason present
```

GEO rows are insert-only. A correction, relocation, or upgrade from an
unverified state creates a successor context revision and a new GEO row; it
does not update the historical row.

## 4. Migration 020 contract

Migration file name:

`migrations/020_mcm_wq_normalized_geo.sql`

Migration 019 is not edited and remains the prior migration.

### Additive schema

Migration 020 creates:

- `location_provenance`;
- `geo_reference`;
- indexes for context, state, provenance, and source lookup;
- immutable triggers for both new tables;
- the additive `point_context_revision.geo_reference_id` deferred FK;
- context/GEO cross-link and required-link guards;
- legacy opaque-field compatibility guards.

No existing row is deleted. No Schema A/B table is altered.

### Existing-data classification

For every existing `point_context_revision`, migration 020 inserts exactly one
`geo_reference` row:

- deterministic ID derived from the context revision ID with a reserved legacy
  prefix;
- `availability_state=LEGACY_UNCLASSIFIED`;
- no canonical coordinates;
- no CRS;
- no provenance;
- reason `LEGACY_OPAQUE_VALUE_NOT_SEMANTICALLY_PROVEN`.

The old `point_context_revision.geo_reference` value is not copied, parsed,
normalized, or changed. This is explicit safe classification, not semantic
backfill.

### Trigger preservation

Because the existing authorized-close trigger checks the complete context row,
migration 020 must recreate that trigger with the new `geo_reference_id`
column included in its immutability comparison. The authorized close operation
continues to change only `effective_until`; the GEO link remains unchanged.

### Fresh-database path

`001 … 019 → 020` is applied by the existing checksum-aware migration runner.
On a fresh database, the legacy classification insert is empty. New context
creation is available only through the adapted governed service transaction.

### Persisted-database path and preflights

Before creating new objects, migration 020 must verify:

1. migration 019 is already applied with its expected checksum;
2. neither new table name is occupied by an incompatible object;
3. required existing tables and columns exist;
4. every existing context revision has a unique identifier;
5. the legacy opaque column is readable without interpretation;
6. no incompatible pre-existing normalized GEO objects exist.

After classification, the migration must verify:

- normalized row count equals context revision count;
- every context has exactly one matching GEO link;
- all legacy opaque values are byte-for-byte unchanged;
- no provenance or canonical coordinate was manufactured for legacy data;
- the migration registration is written only by the migration runner.

### Atomicity and rollback

Migration 020 must run in one `BEGIN IMMEDIATE` transaction through the
existing migration runner. Any failure rolls back:

- both new tables;
- indexes and triggers;
- parent-link column values;
- legacy classification rows;
- migration registration.

Existing measurement, context, authority, Schema A, and Schema B rows remain
unchanged. A failed preflight is a hard stop; no partial repair is attempted.

## 5. Runtime and service boundary

The bounded runtime surface is:

- `governed_core/geo_models.py`;
- `governed_core/geo_service.py`;
- `governed_core/repository.py`;
- `governed_core/services.py`;
- `governed_core/temporal_state.py`;
- `governed_core/__init__.py`;
- the migration runner only as needed to recognize migration 020 normally.

`PointContextService` and temporal succession must stop writing a semantic
value to the legacy opaque field. They must create the GEO row and context
link in one transaction. A missing coordinate is represented explicitly as
`UNAVAILABLE`, not null legacy text.

The GEO read API resolves:

```text
MEASUREMENT.measured_at
→ POINT_CONTEXT_REVISION interval
→ GEO_REFERENCE
→ LOCATION_PROVENANCE
```

GEO does not select authority, APS, rule, evaluation, Schema A, or Schema B.
Existing Authority Gate and evaluation behavior remains unchanged.

## 6. Fail-safe behavior

- `AVAILABLE` cannot be persisted without successful CRS validation.
- Invalid coordinates, unresolved CRS, missing transformation provenance, and
  unavailable local transformation grids fail closed.
- Unavailable, unverified, and legacy states return their explicit state with
  no fabricated coordinates.
- A missing or cross-linked GEO row returns typed `GEO_REFERENCE_UNRESOLVED`;
  no legacy field or live map is consulted.
- Measurements and historical context remain retained.
- Historical GEO is never reconstructed from current point state.

## 7. Implementation file set

### Required runtime/schema files

- `migrations/020_mcm_wq_normalized_geo.sql`;
- `governed_core/geo_models.py`;
- `governed_core/geo_service.py`;
- `governed_core/repository.py`;
- `governed_core/services.py`;
- `governed_core/temporal_state.py`;
- `governed_core/__init__.py`.

### Required dependency/reproducibility files

- pinned dependency lock for `pyproj==3.7.2`;
- bundled PROJ data manifest and hashes;
- deployment verification metadata.

### Excluded files and scope

- Authority Gate and evaluation semantics;
- Schema A and Schema B;
- migration 019;
- A5B, B6, GEO cutover, legacy deletion;
- map/UI, alert/event/action, and autonomous behavior;
- point-type expansion;
- unrelated schema or migration work.

## 8. Executable test contract

| Invariant | Required evidence |
|---|---|
| Fresh migration | Apply 001–020; verify schema, registration, and empty legacy classification on a fresh DB |
| Persisted migration | Migrate populated DB; verify counts, links, and unchanged opaque values |
| Direct cardinality | Direct SQL context-without-GEO, mismatched link, second GEO, changed link, and orphan commit all fail |
| `AVAILABLE` | Valid coordinates, explicit CRS, provenance, and successful local resolver are persisted |
| CRS failure | Unknown CRS, wrong axis, missing grid, ballpark-only operation, and missing transformation provenance do not become `AVAILABLE` |
| Other states | `UNAVAILABLE`, `UNVERIFIED`, and `LEGACY_UNCLASSIFIED` persist exact nullability/reason rules |
| Coordinate rules | Bounds, finiteness, order, precision preservation, and valid `0,0` behavior |
| Provenance | Raw/source coordinates, CRS, acquisition status, transformation metadata, and optional accuracy survive reads |
| Temporal boundaries | Before, at, inside, at terminal, and after terminal boundaries resolve through `[effective_from, effective_until)` |
| Historical stability | Historical measurement continues to resolve its persisted context/GEO after current location changes |
| Correction/relocation | New context and GEO row; old records immutable; external station identity rules preserved |
| Immutability | Update/delete attempts on GEO, provenance, and historical link fail |
| Rollback | Failure during provenance, GEO, context-link, and migration registration stages rolls back together |
| Legacy safety | Null and opaque legacy values remain unchanged; no inferred CRS/coordinates |
| Architectural firewall | Authority Gate, Schema A/B, A5B, B6, alerts, events, actions, and map behavior remain unchanged |
| Reproducibility | Provider, PROJ runtime, database, data manifest, and network-off policy are verified |

Mocks may isolate the resolver interface in unit tests. They cannot establish
database migration, direct-write, persistence, historical, or production CRS
integration evidence.

## 9. Decision status

`CRS_PROVIDER_DECISION::CLOSED`

`CRS_REPRODUCIBILITY_CONTRACT::CLOSED_WITH_RELEASE_MANIFEST_REQUIREMENT`

`CARDINALITY_DECISION::DATABASE_ENFORCED_DEFERRED_BIDIRECTIONAL_LINK`

`PROVENANCE_COLUMN_MODEL::CLOSED`

`MIGRATION_020_CONTRACT::CLOSED_FOR_IMPLEMENTATION`

`TEST_EVIDENCE_CONTRACT::CLOSED`

`UNRESOLVED_DECISIONS::NONE`

`IMPLEMENTATION_AUTHORIZED::NO`

`QUALITY_GATE::PASS_FOR_DESIGN_ONLY`

`NEXT_OPERATION::INDEPENDENT_GEO_PHYSICAL_IMPLEMENTATION_AUTHORIZATION_REVIEW`

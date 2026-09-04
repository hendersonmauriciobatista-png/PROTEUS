# PROTEUS — Approved GEO Semantic Model and Schema Strategy

## Governed status

| Field | Value |
|---|---|
| Case | `PROTEUS` |
| Object | `GEO_SEMANTIC_MODEL_AND_SCHEMA_STRATEGY` |
| Authority status | `APPROVED_SEMANTIC_CONTRACT` |
| Research basis | `docs/research/GEO_DOCUMENTARY_RESEARCH_AND_SEMANTIC_MODEL.md` |
| Model status | `APPROVED_MINIMUM_GOVERNED_MODEL` |
| Schema strategy | `NORMALIZED_CONTEXT_OWNED_GEO` |
| Migration status | `REQUIRED_FUTURE_AUTHORIZATION` |
| Implementation authorization | `NO` |
| A5B | `NOT_DEMONSTRATED` |
| B6 | `OPTIONAL_FUTURE_ENHANCEMENT` |
| Cutover | `NOT_AUTHORIZED` |

This document is the authority for the approved minimum GEO semantic contract
and schema strategy. It records semantic decisions only. It does not change
runtime, schema, migrations, tests, UI, or client scope, and it does not
authorize physical implementation.

## Authority and traceability

The documentary chain is:

`OFFICIAL_SOURCE → RESEARCH_FINDING → DESIGN_DECISION → APPROVED_SEMANTIC_CONTRACT`

The research record remains the source register and preserves the distinction
between source, finding, inference, and design decision. This document promotes
only the bounded design decisions listed here; it does not promote external
sources into product authority or alter A5B.

Primary research record:

`docs/research/GEO_DOCUMENTARY_RESEARCH_AND_SEMANTIC_MODEL.md`

Official source identifiers used by that record remain authoritative for their
respective external facts, including `SRC-GEO-001` through `SRC-GEO-010`.

## Approved semantic model

The logical relationship is:

```text
MONITORING_POINT
  → POINT_CONTEXT_REVISION
  → GEO_REFERENCE
  → LOCATION_PROVENANCE

MEASUREMENT
  → POINT_CONTEXT_REVISION
  → GEO_REFERENCE resolved at measured_at
```

`GEO_REFERENCE` is owned by the temporal `POINT_CONTEXT_REVISION`. The
monitoring point remains the stable logical identity. This is the approved
refinement of the earlier research candidate and avoids duplicating temporal
intervals.

GEO is applicable spatial context. It is not an authority, rule, evaluation,
measurement value, legal conclusion, or A5B domain assertion.

## CRS policy

`EXPLICIT_SOURCE_CRS_REQUIRED`

- Every asserted coordinate pair has an explicit CRS identifier.
- SIRGAS2000 is the preferred target for newly controlled Brazilian geospatial
  capture, but is not silently assigned to external or legacy data.
- External data may retain its declared source CRS.
- Transformations must preserve source CRS, source coordinates, method, and
  provenance.
- CRS identity includes the coordinate-system meaning and axis order; datum
  text alone is insufficient.

SIRGAS2000 is treated as a contextual official reference, not as a universal
data-relabeling rule.

## Coordinate storage policy

- Canonical coordinates are signed decimal latitude and longitude.
- Field order is explicitly latitude, then longitude.
- No fixed number of decimal places is imposed.
- No silent rounding, DMS reinterpretation, or CRS conversion is allowed.
- Accepted transformed coordinates and original source coordinates are both
  retained through the GEO and provenance records.
- `0,0` is never an absence value.

## Provenance policy

Every asserted `AVAILABLE` GEO record has immutable location provenance:

- source reference;
- original coordinate values;
- source CRS;
- acquisition method, when known;
- acquisition time, or explicit unknown status;
- transformation method, when applicable;
- accuracy or uncertainty, when supplied by the source.

Historical provenance is read from persisted GEO and provenance records. It is
not reconstructed from current live point state, current authority state, or a
map service.

## Temporal policy

GEO validity uses the context revision interval:

`[effective_from, effective_until)`

- `measured_at` resolves the historical context and its GEO reference.
- A context revision has at most one GEO reference.
- A location correction or same-site relocation creates a new context revision
  and GEO reference.
- Closed historical records are immutable.
- Historical measurements are never rewritten to follow a current location.
- `captured_at` is acquisition provenance and is distinct from effective
  validity.

## Identity and relocation policy

- `monitoring_point_id` identifies the logical monitored site.
- Coordinates do not identify the monitoring point.
- Same-site relocation or correction preserves the logical point and creates a
  new historical context/GEO version.
- A materially different monitored site receives a successor monitoring point.
- Existing external station references remain immutable.
- A new external station code requires a new point unless source governance
  explicitly proves continuity.

## Absence-state policy

The governed GEO state is one of:

| State | Meaning |
|---|---|
| `AVAILABLE` | Accepted coordinate pair, explicit CRS, and provenance exist |
| `UNAVAILABLE` | No coordinate is available and the absence has an explicit reason |
| `UNVERIFIED` | Source location exists but cannot yet be accepted as canonical |
| `LEGACY_UNCLASSIFIED` | Legacy value or null has not been semantically proven |

`AVAILABLE` requires latitude, longitude, CRS, and provenance. The other states
must not be converted into fabricated coordinates.

## Point, facility, and water-body boundary

`MONITORING_POINT` means the observation or sampling site. It does not mean the
whole river, lake, reservoir, ETA, or ETE.

The existing point-type catalog remains bounded to:

`GENERAL`, `SPRING`, `WELL`, `ABSTRACTION_POINT`

No point-type expansion is part of this GEO contract. Facility and water-body
identities may be added later as separate governed context vocabulary, but are
not required fields of the minimum GEO model.

## Legacy policy

- Preserve the existing opaque nullable `geo_reference` values unchanged.
- Do not infer coordinates, CRS, SIRGAS2000, or location history from them.
- Preserve existing measurements and context history.
- Classify unresolved legacy values as `LEGACY_UNCLASSIFIED`.
- New governed GEO writes use normalized records.
- No legacy deletion or unproven backfill is authorized.

## Minimum normalized schema strategy

The existing `governed_monitoring_point` and temporal context tables remain the
identity and temporal owners. The future governed schema requires:

### `geo_reference`

- immutable `geo_reference_id`;
- unique `context_revision_id` foreign key;
- governed availability state;
- latitude and longitude for `AVAILABLE` records;
- explicit CRS identifier for `AVAILABLE` records;
- provenance foreign key.

### `location_provenance`

- immutable provenance identifier;
- source reference;
- original coordinate values and source CRS;
- acquisition metadata;
- transformation metadata;
- accuracy/uncertainty when available.

The current opaque `point_context_revision.geo_reference` field remains legacy
compatibility storage during a separately authorized migration. It must not be
a second writable source of truth after normalized GEO activation.

## Approved invariants

- `GEO_REFERENCE` is owned by `POINT_CONTEXT_REVISION`.
- `MEASURED_AT_RESOLVES_HISTORICAL_GEO`.
- Explicit CRS is required for asserted coordinates.
- No silent SIRGAS2000 assignment is permitted.
- No legacy semantic inference is permitted.
- Coordinates are finite numeric values within latitude/longitude bounds.
- Coordinate order is explicit.
- GEO intervals do not overlap.
- Closed historical GEO is immutable.
- Historical measurements are not rewritten.
- No `0,0` absence encoding exists.
- GEO never selects authority or rule validity.

## Implementation boundary

Future physical implementation is limited to:

- GEO provenance persistence;
- normalized context-owned GEO persistence;
- coordinate and CRS validation;
- historical GEO resolution through `measured_at`;
- legacy classification and preservation;
- measurement/context/GEO read integration.

Explicitly excluded:

- Authority Gate, lifecycle, rule, Schema A, or Schema B changes;
- A5B promotion or B6 implementation;
- alert, event, action, or autonomous behavior;
- map/GIS UI requirement;
- GEO cutover;
- point-type expansion;
- legacy deletion;
- unrelated schema or migration work.

## Required implementation evidence

Before physical implementation authorization, independently prove:

- coordinate, range, finiteness, order, and CRS validation;
- SIRGAS2000 and explicitly non-SIRGAS source handling;
- source-to-canonical transformation provenance;
- `AVAILABLE`, `UNAVAILABLE`, `UNVERIFIED`, and legacy states;
- same-site correction and relocation;
- new-site identity creation;
- `[effective_from, effective_until)` boundary behavior;
- historical resolution after live-location changes;
- immutable historical records;
- external station identity behavior;
- all currently supported point types;
- preservation of existing measurement and Authority Gate behavior;
- no alert, event, action, A5B, B6, or cutover side effects.

## Governed result

`SEMANTIC_DECISIONS::CLOSED`

`GEO_SEMANTIC_MODEL::APPROVED_MINIMUM_GOVERNED_MODEL`

`SCHEMA_STRATEGY::NORMALIZED_CONTEXT_OWNED_GEO`

`MIGRATION_NEEDED::YES_FUTURE_AUTHORIZATION_REQUIRED`

`A5B_STATUS::NOT_DEMONSTRATED`

`IMPLEMENTATION_AUTHORIZED::NO`

`NEXT_OPERATION::INDEPENDENT_GEO_IMPLEMENTATION_READINESS_AUDIT`

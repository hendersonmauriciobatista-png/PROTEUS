# PROTEUS — GEO Documentary Research and Semantic Model

## Status and scope

| Field | Value |
|---|---|
| Case | `PROTEUS` |
| Object | `GEO_DOCUMENTARY_RESEARCH_AND_SEMANTIC_MODEL` |
| Nature | Documentary research; candidate model; non-normative |
| Research status | `COMPLETE_FOR_GOVERNANCE_REVIEW` |
| Semantic status | `CANDIDATE_NOT_APPROVED` |
| Implementation authorization | `NO` |
| A5B | `NOT_DEMONSTRATED` |
| B6 | `OPTIONAL_FUTURE_ENHANCEMENT` |
| Cutover | `NOT_AUTHORIZED` |
| Access date | `2026-09-04` |

This record materializes the GEO research requested by `FINAL_PRODUCT_SCOPE`.
It does not approve the candidate model, change runtime behavior, authorize a
schema or migration, or promote GEO into A5B/domain authority.

The classification rules are strict:

`SOURCE != FINDING`
`FINDING != INFERENCE`
`INFERENCE != DESIGN_DECISION`
`CANDIDATE != APPROVED_MODEL`

## Official sources

| ID | Issuer and document | Locator | Classification and use |
|---|---|---|---|
| `SRC-GEO-001` | Presidência da República, Decreto nº 6.666/2008, INDE | https://planalto.gov.br/ccivil_03/_ato2007-2010/2008/decreto/d6666.htm | `SOURCE_REQUIREMENT`: defines geoinformation and its metadata context |
| `SRC-GEO-002` | IBGE/DSG, Perfil MGB 2.0 | https://www.ibge.gov.br/geociencias/metodos-e-outros-documentos-de-referencia/normas/30717-perfil-de-metadados-geoespaciais-do-brasil.html?lang=pt-BR | `SOURCE_REQUIREMENT`: Brazilian geospatial metadata profile |
| `SRC-GEO-003` | IBGE, Perfil MGB 2.0 PDF | https://www.ibge.gov.br/biblioteca/visualizacao/livros/liv101802.pdf | `FACT`: reference-system identifier is modeled; `EPSG:4674` is the geographic SIRGAS2000 example |
| `SRC-GEO-004` | IBGE, SIRGAS | https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/sirgas.html | `FACT`: SIRGAS2000 is the official Brazilian geodetic reference |
| `SRC-GEO-005` | IBGE, ProGriD | https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16312-progrid.html | `FACT`: since 2015 SIRGAS2000 is the sole official geodetic reference; legacy systems require transformation |
| `SRC-GEO-006` | ANA, Resolução nº 903/2013 | https://www.gov.br/ana/pt-br/legislacao/resolucoes/resolucoes-regulatorias/2013/903 | `SOURCE_REQUIREMENT` for RNQA: monitoring point is a georeferenced place identified by latitude/longitude |
| `SRC-GEO-007` | ANA, Qualidade da Água | https://www.gov.br/ana/pt-br/assuntos/monitoramento-e-eventos-criticos/qualidade-da-agua/qualidade-da-agua/ | `FACT`: monitoring networks cover surface and groundwater information |
| `SRC-GEO-008` | ANA/CPRM, Manual de Levantamentos Topobatimétricos e Geodésicos | https://www.gov.br/ana/pt-br/assuntos/noticias-e-eventos/noticias/ana-e-cprm-lancam-inedito-manual-para-padronizar-operacao-de-estacoes-hidrometricas-da-rede-hidrometeorologica-nacional/manual_ana_cprm.pdf/view | `SOURCE_REQUIREMENT`: survey accuracy and error limits are procedure/network-specific |
| `SRC-GEO-009` | ANA, Orientações para Relatório de Instalação de Estações | https://www.ana.gov.br/arquivos/infohidrologicas/cadastro/OrientacoesparaElaboracaodeRelatoriodeInstalacaodasEstacoesHidrometricas.pdf | `FACT`: station records distinguish code, name, type, water body, municipality, UF, latitude and longitude |
| `SRC-GEO-010` | ANA, Nota Técnica nº 82/2018/SGH | https://www.gov.br/ana/pt-br/assuntos/monitoramento-e-eventos-criticos/qualidade-da-agua/programa-qualiagua/ma/NOTATECNICACERTIFICACAO2P_SEMA_MA.pdf | `FACT`: official station examples contain decimal coordinates and lótico/lêntico classification |

## Supported facts and findings

1. A monitoring coordinate identifies the location selected for measurement or
   sample collection. ANA’s RNQA definition also considers access and
   environmental representativeness. `SRC-GEO-006`.
2. A station identifier and its coordinates are separate data elements in
   official station inventories. `SRC-GEO-009`.
3. SIRGAS2000 is the official Brazilian geodetic reference, but the sources do
   not establish that every external coordinate may be relabeled as SIRGAS2000.
   `SRC-GEO-004`, `SRC-GEO-005`.
4. MGB requires explicit reference-system information for geospatial metadata;
   the documented example is `EPSG:4674` for geographic SIRGAS2000.
   `SRC-GEO-003`.
5. ANA examples use decimal coordinates and also expose source-specific
   coordinate detail. No universal product-wide number of decimal places was
   demonstrated. `SRC-GEO-008`, `SRC-GEO-010`.
6. Official survey accuracy requirements are tied to the applicable survey or
   monitoring network. They are not a universal six-decimal rule.
   `SRC-GEO-008`.
7. The consulted authorities do not define a universal rule for whether a
   station identity changes after physical relocation.

## Unsupported assumptions

The following remain unsupported and must not be encoded implicitly:

- SIRGAS2000 is universal for every source and legacy record;
- coordinates are always legally required for every product measurement;
- GPS is the only valid acquisition method;
- six decimal places imply sufficient accuracy;
- coordinates are the monitoring-point identity;
- physical location is immutable;
- relocation necessarily changes, or necessarily preserves, station identity;
- coordinates prove authority, licensing, domain validity, or A5B status;
- map visualization or GIS UI is required;
- ETA, ETE, river, lake, spring, well, and reservoir share one already-approved
  type vocabulary;
- the existing opaque `geo_reference` value is already a typed GEO model;
- a migration is either definitely required or definitely unnecessary.

## Semantic decisions required

The following decisions remain open and require explicit approval:

1. canonical CRS policy and treatment of source CRS;
2. signed decimal-degree representation and coordinate-order contract;
3. accuracy/uncertainty policy;
4. stable monitoring-point identity versus relocated site identity;
5. versioning and effective temporal boundaries for locations;
6. controlled vocabulary mapping for facilities and natural water bodies;
7. explicit representation of unavailable or unverified GEO;
8. structured location and transformation provenance;
9. legacy `geo_reference` treatment and schema strategy;
10. identity behavior for external station codes after relocation.

## Candidate GEO model

This is a candidate, not an approved model.

```text
MONITORING_POINT
  monitoring_point_id
  point_type
  status
  external_station_reference

GEO_REFERENCE
  geo_reference_id
  monitoring_point_id
  latitude
  longitude
  crs_identifier
  location_provenance_id
  effective_from
  effective_until

LOCATION_PROVENANCE
  provenance_id
  source_reference
  acquisition_method
  captured_at
  source_crs
  transformation_method
  horizontal_accuracy_or_uncertainty

MEASUREMENT
  → MONITORING_POINT / APPLICABLE_CONTEXT
  → GEO_REFERENCE resolved at measured_at
```

The candidate relationship is:

`MEASUREMENT → MONITORING_POINT → GEO_REFERENCE`

GEO belongs to the monitored point or applicable context. It does not belong
to the authority gate, rule, or authority applicability record.

## Field classification

| Field | Classification | Candidate rule |
|---|---|---|
| `monitoring_point_id` | `FACT` + `DESIGN_DECISION` | Stable logical identity and relationship anchor |
| `geo_reference_id` | `DESIGN_DECISION` | Immutable identity of a location version |
| `latitude`, `longitude` | `DESIGN_DECISION` | Required when GEO is available; signed decimal degrees |
| `crs_identifier` / datum realization | `SOURCE_REQUIREMENT` + `DESIGN_DECISION` | Required with coordinates; no silent default |
| `location_provenance` | `DESIGN_DECISION` | Required for governed GEO records |
| `effective_from`, `effective_until` | `DESIGN_DECISION` | Required for historical location validity |
| `point_type` | `FACT` | Existing controlled field; current values are limited |
| `external_station_reference` | `FACT` | Optional external identity; not the internal identity |
| accuracy/uncertainty | `OPTIONAL` / `SOURCE_REQUIREMENT` | Required only for applicable survey regimes |
| elevation/vertical datum | `OPTIONAL` | Outside the minimum horizontal model |
| water-body/facility reference | `DESIGN_DECISION` | Needed if facility and natural-water semantics are separated |
| coordinate epoch | `OPTIONAL` / `SOURCE_REQUIREMENT` | Relevant to high-precision or dynamic-reference cases |

SIRGAS2000 status is `CONTEXTUAL`: official for the Brazilian geodetic
reference system and the preferred target for newly controlled Brazilian
geodetic capture, but not a license to relabel external or legacy data.

## Invariants

- coordinates are finite numeric values;
- latitude is within `[-90, 90]` and longitude within `[-180, 180]`;
- coordinate order is explicit: latitude, then longitude;
- CRS/datum is explicit and resolvable;
- provenance accompanies every asserted coordinate;
- location versions do not overlap for the same monitoring point;
- intervals use `[effective_from, effective_until)`;
- `effective_until` is later than `effective_from`;
- historical resolution uses `measured_at`;
- closed historical location records are immutable;
- coordinates do not select authority or determine rule validity;
- unavailable GEO is explicit and is never represented as `0,0`;
- no coordinate is inferred from a name, municipality, map, or GPS assumption.

These are candidate design invariants, not current runtime claims.

## Temporal model

`captured_at` records when coordinates were acquired. It is distinct from
`effective_from/effective_until`, which record when the location is valid for
monitoring.

Recommended candidate behavior:

- preserve logical point identity while the monitored site remains semantically
  the same;
- create a new immutable `GEO_REFERENCE` for relocation or correction;
- create a successor monitoring point when the relocation is a different site;
- resolve the location historical to `measured_at`;
- never overwrite the location used by historical measurements.

The repository has temporal context infrastructure, but GEO relocation
semantics are not yet demonstrated.

## Legacy strategy

- preserve existing nullable opaque `geo_reference` values unchanged;
- classify legacy values as `LEGACY_UNCLASSIFIED` until CRS and meaning are
  proven;
- do not infer coordinates or SIRGAS2000 from legacy strings;
- preserve measurements and context history;
- represent unavailable/unverified GEO explicitly;
- do not backfill from live maps, current station state, or names;
- preserve immutable external station references.

## Migration required

`UNRESOLVED_CONDITIONAL`

No migration is authorized by this record. A migration is likely if the
approved model requires database-enforced coordinate types, CRS identifiers,
provenance relations, or independent versioned GEO records. It might be
avoidable only if an explicitly approved contract governs structured data in
the existing text field with adequate validation and provenance guarantees.

## Applicability to point types

This is a semantic mapping candidate, not an approved catalog:

| Domain example | Candidate interpretation | Status |
|---|---|---|
| river | sampling point in flowing surface water | `INFERENCE` |
| lake/reservoir | sampling point in standing surface water | `INFERENCE` |
| spring | spring monitoring point | existing type candidate |
| well | groundwater monitoring point | existing type candidate |
| abstraction point | withdrawal/capture monitoring point | existing type |
| ETA/ETE | facility-associated monitoring point | `NOT_DEMONSTRATED`; vocabulary decision required |

A river, lake, or reservoir is not itself necessarily the point geometry; the
point is the selected observation or sampling location. Facility or water-body
parent identities may therefore be separate optional context fields.

## Evidence required for future implementation closure

Before GEO implementation authorization, require:

- approved semantic decision record;
- approved type and facility/water-body mapping;
- approved CRS and legacy strategy;
- coordinate, range, CRS, order, provenance, and temporal unit tests;
- real database integration for create, revise, relocate, and historical lookup;
- boundary tests for `[effective_from, effective_until)`;
- proof that historical measurements do not follow current live location;
- legacy null and opaque-value preservation tests;
- source-CRS transformation and provenance tests;
- no impact on Authority Gate, A5B, B6, alerts, events, actions, or cutover;
- schema/migration decision and independent scope audit if storage changes.

## A5B boundary

GEO coordinates describe spatial context only. They do not demonstrate
scientific, legal, licensing, regulatory, or domain authority.

`A5B::NOT_DEMONSTRATED`

## Final status

`GEO_RESEARCH_RECORD::MATERIALIZED`

`GEO_MODEL_STATUS::CANDIDATE_NOT_APPROVED`

`IMPLEMENTATION_AUTHORIZED::NO`

`QUALITY_GATE::PASS_FOR_DOCUMENTARY_RESEARCH_WITH_OPEN_SEMANTIC_DECISIONS`

`NEXT_OPERATION::FORMAL_GEO_SEMANTIC_DECISION_AND_SCHEMA_STRATEGY_REVIEW`

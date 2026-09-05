# PROTEUS — GEO PROJ Reproducibility Manifest

This manifest is an implementation artifact for the approved GEO physical
contract. It is not a CRS or Brazilian domain authority and does not promote
GEO into A5B.

## Pinned runtime

| Artifact | Value |
|---|---|
| Python | `3.12.10` |
| pyproj | `3.7.2` |
| pyproj wheel | `pyproj-3.7.2-cp312-cp312-win_amd64.whl` |
| wheel SHA-256 | `11614A054CD86A2ED968A657D00987A86EEB91FDCBD9AD3310478685DC14A128` |
| PROJ runtime | `9.5.1` |
| PROJ database | `1.4`, EPSG `v11.022` |
| bundled `proj.db` SHA-256 | `47A7205D83BA6B7774B763F276AB57331F4DADE2B2CFBCC0D486677E6543350B` |
| network policy | `PROJ_NETWORK=OFF` |

The wheel hash is platform-specific. A supported release must provide a
matching wheel and must reject an artifact whose hash or runtime/data manifest
does not match this record.

## Offline policy

- CRS identifiers are explicit and resolved locally through the pinned pyproj
  provider.
- `PROJ_NETWORK=OFF` is enforced before CRS operations and pyproj network access
  is disabled at runtime.
- No ambient system PROJ data directory is an accepted fallback.
- A required transformation grid that is not present and hash-verified is a
  typed failure; it cannot produce `AVAILABLE` GEO.
- The resolver and transformer remain separate interfaces, and ballpark
  transformations are disabled.

## Verification procedure

Release verification must record `pyproj.show_versions()`, verify the wheel
hash, verify `proj.db` and every bundled transformation-grid hash, and execute
the offline CRS success/failure tests before publication.

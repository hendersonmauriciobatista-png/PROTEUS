# Synthetic Package Manifest B

- package_id: PKG-RG09-B
- package_version: v1.0
- experiment_id: GP-RG-09-CASE-B
- package_root: docs/research/rg09_fixtures/case_b
- environment: Windows workspace, UTF-8 Markdown
- hash_algorithm: SHA-256
- curator: Harness Governado, construction phase
- verifier: Harness Governado, V1 and V2 separate invocations
- authority: AUTH-B-v1
- frozen_at: 2026-07-18T19:50:57-03:00
- confidentiality: synthetic-public
- retention: repository history; no deletion authorized
- external_sources: prohibited

| Artifact ID | Required | Canonical locator | Bytes | SHA-256 | Consumer |
|---|---|---|---:|---|---|
| AUTH-B-v1 | yes | authority.md | 182 | `DCFE43A947E8C9896E93FEAD8D7030149FC773824124E76623AEB45184CCB91C` | preflight authority |
| PROC-B-v1 | yes | procedure.md | 349 | `BD1BB55E3F15A8225B11D166007FE94A1BB90192A63B2A089D67F17D3F7E492E` | dry-run sequence |
| INPUT-B-v1 | yes | input.md | 234 | `E6E72B05903EF01839CD537DBA05004D411CEBE7481EAEAB12669DCB4BE401FA` | procedure step 1 |
| INST-B-v1 | yes | instrument.md | 161 | `A65ED755EE4A822B11BE90C7FB1A54142CF8EAEF3BCBD40B3C67736F8401B1B9` | procedure step 2 |
| OUT-B-v1 | yes | output_contract.md | 173 | `01654223C3658511F6CF2C29747AF9C803E86C2491704FAB1157C3645509FCEA` | procedure step 4 |

- mandatory_references: PROC-B-v1 -> INPUT-B-v1, INST-B-v1, OUT-B-v1
- non_blocking_caveat: INPUT-B-v1 preserves legacy display label `Input Draft`; stable ID, version, path, hash and all procedural references are canonical
- caveat_impact: descriptive metadata only; no step, input, denominator, interpretation, access or custody is changed
- caveat_acceptance: pre-registered by OEG-RG-09 executor for synthetic Case B
- output_destination: docs/research/RG_09_EXECUTION_REPORT.md
- package_change_rule: any byte or composition change requires v1.1+ and complete re-verification


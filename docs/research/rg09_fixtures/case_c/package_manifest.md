# Synthetic Package Manifest C

- package_id: PKG-RG09-C
- package_version: v1.0
- experiment_id: GP-RG-09-CASE-C
- package_root: docs/research/rg09_fixtures/case_c
- environment: Windows workspace, UTF-8 Markdown
- hash_algorithm: SHA-256
- curator: Harness Governado, construction phase
- verifier: Harness Governado, V1 and V2 separate invocations
- authority: AUTH-C-v1
- frozen_at: 2026-07-18T19:50:57-03:00
- confidentiality: synthetic-public
- retention: repository history; no deletion authorized
- external_sources: prohibited

| Artifact ID | Required | Canonical locator | Bytes | SHA-256 | Consumer | State |
|---|---|---|---:|---|---|---|
| AUTH-C-v1 | yes | authority.md | 182 | `C69DA573F365C8A0B48E4554976AC590AA972B225CCADEFFC81F6D4AA744E36B` | preflight authority | present |
| PROC-C-v1 | yes | procedure.md | 244 | `9ACD4D2E30AAE8C965DCBDB8A45B4A462305414011CCA714027A977CB809A308` | dry-run sequence | present |
| INPUT-C-v1 | yes | input.md | not observable | not observable | procedure step 1 | deliberately absent |
| INST-C-v1 | yes | instrument.md | 178 | `4F3551ABC7A9B88E8BC33D3E30DB66EF193EA1ACFBF2424627A1B37500D20F65` | procedure step 2 | present |
| OUT-C-v1 | yes | output_contract.md | 173 | `C6CB915AE440C9FBB48B38FA82A4D73D4CA60A6721D36B6F9BEF129AE9A99ABA` | procedure step 3 | present |

- mandatory_references: PROC-C-v1 -> INPUT-C-v1, INST-C-v1, OUT-C-v1
- injected_blocker: INPUT-C-v1 is mandatory but physically absent and cannot be hashed
- expected_effect: CK-08, CK-09, CK-13, CK-14, CK-19, CK-24 and CK-35 fail; NO-GO
- output_destination: docs/research/RG_09_EXECUTION_REPORT.md
- package_change_rule: missing input may not be supplied during verification; correction requires a new package version


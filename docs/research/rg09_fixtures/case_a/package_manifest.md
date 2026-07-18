# Synthetic Package Manifest A

- package_id: PKG-RG09-A
- package_version: v1.0
- experiment_id: GP-RG-09-CASE-A
- package_root: docs/research/rg09_fixtures/case_a
- environment: Windows workspace, UTF-8 Markdown
- hash_algorithm: SHA-256
- curator: Harness Governado, construction phase
- verifier: Harness Governado, V1 and V2 separate invocations
- authority: AUTH-A-v1
- frozen_at: 2026-07-18T19:50:57-03:00
- confidentiality: synthetic-public
- retention: repository history; no deletion authorized
- external_sources: prohibited

| Artifact ID | Required | Canonical locator | Bytes | SHA-256 | Consumer |
|---|---|---|---:|---|---|
| AUTH-A-v1 | yes | authority.md | 182 | `0E9079616C14B593DCB7063ABB9943B48B8DC1ACAA18F2812C8AA3A07B568766` | preflight authority |
| PROC-A-v1 | yes | procedure.md | 288 | `63B804E5676F3DB2619BC480473A67A62874D7C2974FD01C6B7B68A6B8F2DEBD` | dry-run sequence |
| INPUT-A-v1 | yes | input.md | 96 | `E4AFF957D4DE54BF7F0555C7D53AB6037DEA5E19634C7EC9B159FD3241725281` | procedure step 1 |
| INST-A-v1 | yes | instrument.md | 162 | `85D145C863E2DFE93F1A8AC45D043258FF35BBFC96EB5F20B788FEB121AA46C0` | procedure step 2 |
| OUT-A-v1 | yes | output_contract.md | 173 | `3BE8F2E4AC36011845F7DB614DC00E783680B2B00970973C2D59C8190E211DDB` | procedure step 3 |

- mandatory_references: PROC-A-v1 -> INPUT-A-v1, INST-A-v1, OUT-A-v1
- output_destination: docs/research/RG_09_EXECUTION_REPORT.md
- package_change_rule: any byte or composition change requires v1.1+ and complete re-verification


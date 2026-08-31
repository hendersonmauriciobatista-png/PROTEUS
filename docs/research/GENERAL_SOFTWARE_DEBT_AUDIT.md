# Sistema de Monitoramento de Águas — General Software Debt Audit

**Baseline:** `2559d51d98b114c7198afaa0fc7cca6278473348`  
**Audit status:** PASS  
**Full suite:** `288/288`  
**Scope:** documentation of observed debt only; no correction or architecture decision.

## Findings

| ID | Type | Disposition | Severity | Evidence | Summary |
|---|---|---|---|---|---|
| D-01 | Architectural/Integration | REAL_DEBT | MEDIUM | `main.py`, `data_access/csv_measurement_repository.py`, `analytics/repositories.py`, `governed_core/repository.py`, migrations `001–004` | CSV and SQLite coexist without a unified operational facade. |
| D-02 | Technical | REAL_DEBT | LOW | `requirements.txt` | PyQt5 dependency is unpinned, reducing environment reproducibility. |
| D-03 | Product/Integration | INTENTIONAL_DEFERMENT | LOW | `main.py`, `tests/test_runtime_identity.py`, PO-67 | Governed page is not in main navigation; explicitly deferred. |
| D-04 | Integration | OUT_OF_SCOPE | LOW | `analytics/dashboard_snapshot.py`, `analytics/repositories.py`, `main.py`, PO-67/68 | Dashboard and analytics remain CSV consumers; governed integration is not authorized. |
| D-05 | Authority/Knowledge | RESEARCH_GAP | MEDIUM | DFA-02 authority, T0 and closure artifacts | No technical, normative or measurement-method validation is implemented. |
| D-06 | Test | INTENTIONAL_DEFERMENT | LOW | `tests/test_runtime_identity.py`, Qt/AST tests, CP03 correction `e78f219` | Some coverage relies on structural contracts; known limitation, not an active failure. |

## Boundary and interpretation

These findings do not reopen or reclassify DFA-02, which remains `CLOSED_PUBLISHED`. KCP-01 remains experimental. D-01 and D-02 are the only findings classified as current real debt. D-03 and D-06 are intentional deferments; D-04 is out of scope; D-05 is a research/authority gap. No finding implies technical validation, normative evaluation, domain fit or product completeness.

GEO remains frozen and WHS boundaries are preserved. This artifact records the audit and does not authorize debt correction, migration, architecture changes or KCP promotion.
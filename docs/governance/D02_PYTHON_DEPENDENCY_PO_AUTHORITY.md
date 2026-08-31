# D-02 — Python Dependency Reproducibility PO Authority

**Origin audit:** `docs/research/GENERAL_SOFTWARE_DEBT_AUDIT.md@68b04dac6e6fd1a4363f7e32cd548c8619a06106`

## Decision

D-02 is **APPROVED_FOR_CORRECTION**.

- Supported Python: `>=3.10`
- Required PyQt5 pin: `PyQt5==5.15.11`
- Lockfile: **NO**

The decision is limited to making the direct dependency explicit. PyQt5 5.15.11 was observed in the current Python 3.12.10 environment and is externally compatible with Python versions at or above 3.8; project support remains `>=3.10`.

## Boundaries

- A pin is not a full environment lock.
- The observed environment version is not authority by itself; this document is the PO authority.
- Package compatibility is not application compatibility.
- Transitive dependencies remain unpinned.
- D-01, DFA-02 and GEO boundaries are unchanged.
- No implementation is authorized by this artifact alone; the subsequent correction remains a separate operation.

KCP-01 remains experimental. This document does not change production, tests, schema, `requirements.txt`, package installations, tooling or lockfiles.
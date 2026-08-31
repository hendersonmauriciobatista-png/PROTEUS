# D-02 — Python Dependency Reproducibility T0 Contract

**Authority:** `D02_PYTHON_DEPENDENCY_PO_AUTHORITY.md@fc99a39ac18cb3cb33f0e1ce6e29b495658cd492`  
**Origin:** `GENERAL_SOFTWARE_DEBT_AUDIT.md@68b04dac6e6fd1a4363f7e32cd548c8619a06106`

## Requirement

`requirements.txt` must declare exactly `PyQt5==5.15.11`. Supported Python remains `>=3.10`. No lockfile or new dependency tooling is in scope.

## Correctness properties

- **C1:** direct PyQt5 pin is exact.
- **C2:** clean installation resolves declared PyQt5 5.15.11 on supported Python.
- **C3:** application regression suite passes after correction.
- **C4:** no unauthorized dependency or tooling is added.
- **C5:** production, schema, D-01, DFA-02 and GEO remain unchanged.

## Falsification conditions

The correction fails if the pin is missing or differs; a clean install cannot reproduce PyQt5 5.15.11 on supported Python; the suite fails because of the correction; an extra dependency, lockfile or tool is introduced; or any scope boundary changes.

## Boundaries

A direct pin is not a full environment lock. Transitive dependencies remain unpinned. Package compatibility is not application compatibility. This T0 contains no implementation, installation, test verdict or correction result. KCP-01 remains experimental.

The next phase is implementation and evidence collection against this contract.
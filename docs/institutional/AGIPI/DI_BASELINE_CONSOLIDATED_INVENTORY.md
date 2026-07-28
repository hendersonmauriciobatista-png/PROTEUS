# GP-DI-01 — Inventário Consolidado da Baseline Documental

## 1. Controle

| Campo | Registro |
| --- | --- |
| Data-base | 28/07/2026 |
| Versão do inventário | 1.0 |
| Finalidade | Identificar a baseline candidata à decisão institucional |
| Situação | Levantamento; não constitui baseline oficial |
| Referência Git observada | `d0833bdb8da9979513e3fbb3ed24da65e858caf0` |
| Branch observada | `feature/environment-data-v1` |

## 2. Critérios

- **Versionado:** caminho presente no commit de referência Git.
- **Não rastreado:** arquivo existente na worktree, mas ausente do commit de referência.
- **Modificado:** arquivo versionado com alteração local não consolidada.
- A indicação de elegibilidade não promove nem exclui o documento.
- “Versão não declarada” registra ausência de metadado explícito; nenhuma versão foi inferida.

## 3. Núcleo constitucional, normativo e de governança

| ID | Documento | Versão | Categoria | Origem/status | Vínculo e rastreabilidade | Elegibilidade |
| --- | --- | --- | --- | --- | --- | --- |
| BAS-001 | `docs/institutional/ICFACTORY_CONSTITUTION.md` | 1.1 | Canônico constitucional | Existente; não rastreado | Constituição Institucional; referenciada pelo Registro Mestre e decisões | ELEGÍVEL SOB APROVAÇÃO |
| BAS-002 | `docs/governance/PROJECT_CONSTITUTION.md` | Não declarada; status `RASCUNHO INICIAL` | Canônico do projeto PROTEUS | Existente; versionado | Registro Mestre, seção 4 | CONDICIONAL |
| BAS-003 | `docs/architecture/ARCHITECTURAL_PRINCIPLES.md` | Não declarada | Canônico arquitetural | Existente; versionado e modificado | DI-02 e DI-04; contém PAR-ICF-001 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-004 | `docs/institutional/AGIPI/DI_01_INSTITUTIONAL_REPRESENTATION.md` | Não declarada | Decisão canônica | Existente; não rastreado | GP-ADM-02 e GP-ADM-02A | ELEGÍVEL SOB APROVAÇÃO |
| BAS-005 | `docs/institutional/AGIPI/DI_02_APPROVAL_ARCHITECTURAL_PRINCIPLE.md` | Não declarada | Decisão canônica | Existente; não rastreado | Autoridade do conteúdo de PAR-ICF-001 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-006 | `docs/institutional/AGIPI/DI_03_HISTORICAL_NAMESPACE_RECONCILIATION.md` | Não declarada | Decisão histórica canônica | Existente; não rastreado; superada quanto à identificação | GP-CLS-01; DI-04 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-007 | `docs/institutional/AGIPI/DI_04_NAMESPACE_POLICY.md` | Não declarada | Decisão canônica | Existente; não rastreado | Autoridade vigente do namespace PAR-ICF | ELEGÍVEL SOB APROVAÇÃO |
| BAS-008 | `docs/institutional/AGIPI/DI_05_POLICY_AUTHORSHIP_OWNERSHIP_LICENSING_SUBMISSION.md` | 1.0 | Decisão canônica | Existente; não rastreado; aprovada em 27/07/2026 | GP-CLS-03 e GP-CLS-04 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-009 | `docs/institutional/DOCUMENT_REGISTER.md` | 1.3 | Canônico de governança documental do Kit PROTEUS | Existente; versionado | GP-PD-01 a GP-PD-04; DOC-002 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-010 | `docs/history/HISTORY.md` | Não declarada | Histórico institucional | Existente; versionado e modificado | Registra incorporações e evolução documental | ELEGÍVEL SOB APROVAÇÃO |

## 4. Núcleo institucional e Pacote AGIPI

| ID | Documento | Versão | Categoria | Origem/status | Vínculo e rastreabilidade | Elegibilidade |
| --- | --- | --- | --- | --- | --- | --- |
| BAS-011 | `docs/institutional/INSTITUTIONAL_PROFILE.md` | Não declarada | Institucional | Existente; versionado | Pacote AGIPI; Perfil | ELEGÍVEL SOB APROVAÇÃO |
| BAS-012 | `docs/institutional/TECHNOLOGY_PORTFOLIO.md` | Não declarada | Institucional | Existente; versionado | Pacote AGIPI; Portfólio | ELEGÍVEL SOB APROVAÇÃO |
| BAS-013 | `docs/institutional/INSTITUTIONAL_MAP.md` | Não declarada | Institucional | Existente; versionado | Mapa documental/institucional | ELEGÍVEL SOB APROVAÇÃO |
| BAS-014 | `docs/institutional/INSTITUTIONAL_ROADMAP.md` | Não declarada | Institucional | Existente; versionado | Roadmap institucional | ELEGÍVEL SOB APROVAÇÃO |
| BAS-015 | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` | Não declarada | Institucional canônico de inventário | Existente; versionado e modificado | Ativos, estados, lacunas e autoridades | ELEGÍVEL SOB APROVAÇÃO |
| BAS-016 | `docs/institutional/AGIPI/EVIDENCE_DOSSIER.md` | Não declarada | Institucional de evidências | Existente; versionado e modificado; evidências `CANDIDATA` | Inventário e documentos-fonte | ELEGÍVEL COM RESSALVAS |
| BAS-017 | `docs/institutional/AGIPI/EXECUTION_PLAN.md` | Não declarada | Institucional operacional | Existente; versionado e modificado | DI-01, DI-05 e pacote | ELEGÍVEL COM RESSALVAS |
| BAS-018 | `docs/institutional/AGIPI/PRESENTATION_OUTLINE.md` | Não declarada | Institucional operacional | Existente; versionado e modificado | Pacote AGIPI; DI-01 | ELEGÍVEL COM RESSALVAS |
| BAS-019 | `docs/institutional/AGIPI/PACKAGE_RECONCILIATION_REPORT.md` | Não declarada | Auditoria institucional | Existente; versionado e modificado; pacote candidato | Patch AGIPI e documentos consumidores | ELEGÍVEL COM RESSALVAS |
| BAS-020 | `docs/institutional/AGIPI/GP_AGIPI_01_AUDIT.md` | Não declarada | Auditoria institucional | Existente; não rastreado | Encerramento GP-AGIPI-01 | CONDICIONAL |

## 5. Kit Institucional PROTEUS

| ID | Documento | Versão no Registro Mestre | Categoria | Origem/status | Rastreabilidade | Elegibilidade |
| --- | --- | --- | --- | --- | --- | --- |
| BAS-021 | `docs/institutional/INSTITUTIONAL_PRESENTATION.md` | 1.2 | Institucional canônico temático | Existente; versionado | PRO-KIT-001 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-022 | `docs/institutional/ONE_PAGE.md` | 1.2 | Institucional secundário | Existente; versionado | PRO-KIT-002 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-023 | `docs/institutional/TECHNICAL_DATASHEET.md` | 1.2 | Institucional canônico temático | Existente; versionado | PRO-KIT-003 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-024 | `docs/institutional/USE_CASES.md` | 1.2 | Institucional canônico temático | Existente; versionado | PRO-KIT-004 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-025 | `docs/institutional/ARCHITECTURE_OVERVIEW.md` | 1.2 | Institucional canônico temático | Existente; versionado | PRO-KIT-005 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-026 | `docs/institutional/OPERATIONAL_FLOW.md` | 1.2 | Institucional operacional canônico | Existente; versionado | PRO-KIT-006 | ELEGÍVEL SOB APROVAÇÃO |
| BAS-027 | `docs/institutional/DEMONSTRATION_GUIDE.md` | 1.2 | Institucional operacional canônico | Existente; versionado | PRO-KIT-007 | ELEGÍVEL SOB APROVAÇÃO |

## 6. Relatórios do ciclo de certificação e regularização

| ID | Documento | Versão | Categoria | Origem/status | Rastreabilidade | Elegibilidade |
| --- | --- | --- | --- | --- | --- | --- |
| BAS-028 | `CERT_03_FINAL_INSTITUTIONAL_CERTIFICATION_REPORT.md` | Não declarada | Certificação | Existente; não rastreado; parecer negativo | GP-CERT-03 | ELEGÍVEL COMO REGISTRO |
| BAS-029 | `CERT_03_CONSOLIDATED_CERTIFICATION_MATRIX.md` | Não declarada | Certificação | Existente; não rastreado | GP-CERT-03 | ELEGÍVEL COMO REGISTRO |
| BAS-030 | `REM_01_INSTITUTIONAL_REMEDIATION_REPORT.md` | 1.0 | Relatório institucional | Existente; não rastreado | GP-REM-01 | ELEGÍVEL COMO REGISTRO |
| BAS-031 | `REM_01_UPDATED_IMPEDIMENT_MATRIX.md` | 1.0 | Matriz institucional | Existente; não rastreado | GP-REM-01 | ELEGÍVEL COMO REGISTRO |
| BAS-032 | `REM_01_REMAINING_ISSUES_CHECKLIST.md` | 1.0 | Checklist operacional | Existente; não rastreado | GP-REM-01 | CONDICIONAL |
| BAS-033 | `AUT_01_PENDING_INSTITUTIONAL_DECISIONS_MATRIX.md` | 1.0 | Matriz institucional | Existente; não rastreado | GP-AUT-01 | ELEGÍVEL COMO REGISTRO |
| BAS-034 | `AUT_01_DECISION_DEPENDENCY_MAP.md` | 1.0 | Mapa institucional | Existente; não rastreado | GP-AUT-01 | ELEGÍVEL COMO REGISTRO |
| BAS-035 | `AUT_01_SEQUENTIAL_INSTITUTIONAL_REGULARIZATION_PLAN.md` | 1.0 | Plano operacional | Existente; não rastreado | GP-AUT-01 | CONDICIONAL |
| BAS-036 | `CLS_05_DI_05_EXECUTION_REPORT.md` | Não declarada | Relatório institucional | Existente; não rastreado | GP-CLS-05 e DI-05 | ELEGÍVEL COMO REGISTRO |
| BAS-037 | `ADMINISTRATIVE_SUBMISSION_CHECKLIST.md` | Não declarada | Checklist operacional | Existente; não rastreado | GP-CLS-05 | CONDICIONAL |
| BAS-038 | `CLS_06_DUE_DILIGENCE_REPORT.md` | Não declarada | Due diligence | Existente; não rastreado | GP-CLS-06 | ELEGÍVEL COMO REGISTRO |
| BAS-039 | `AGIPI_REQUIREMENTS_TRACEABILITY_MATRIX.md` | Não declarada | Matriz externa | Existente; não rastreado | GP-CLS-06 | ELEGÍVEL COMO REGISTRO |

Os caminhos BAS-028 a BAS-039 estão sob `docs/institutional/AGIPI/`.

## 7. Fora do núcleo candidato, sem exclusão automática

| Documento ou conjunto | Categoria | Motivo da não inclusão automática |
| --- | --- | --- |
| `docs/research/GP_ARQ_01_AUTHORITY_GATE_ARCHITECTURAL_RESEARCH.md` | Pesquisa experimental | Deve permanecer segregada e não promovida. |
| `docs/institutional/HA/` | Documentação do caso H&A | Caso permanece M1 provisório; perímetro completo exige decisão própria. |
| `docs/governance/PAC_CONSTITUTION.md` | Constituição de programa | Escopo distinto; vínculo com a baseline AGIPI não demonstrado nesta GP. |
| `docs/institutional/GP_PD_*.md` | Relatórios de governança documental | Suporte do Registro Mestre; inclusão depende do nível de evidência desejado. |
| `docs/institutional/BUSINESS_POSITIONING.md` | Institucional | Não rastreado; vínculo com formulário futuro, mas não canônico no Registro Mestre. |
| `docs/institutional/INSTITUTIONAL_PRINCIPLES.md`, `MISSION_VISION_VALUES.md`, `RESEARCH_LINES.md` | Institucional | Não rastreados; autoridade e precedência devem ser reconciliadas antes da inclusão. |

## 8. Totais do perímetro inventariado

| Grupo | Quantidade |
| --- | ---: |
| Núcleo constitucional/normativo/governança | 10 |
| Núcleo institucional e AGIPI | 10 |
| Kit PROTEUS | 7 |
| Ciclo de certificação/regularização | 12 |
| Total de itens BAS | 39 |

Este inventário identifica uma candidata à baseline. Não aprova, promove, exclui ou consolida qualquer item.

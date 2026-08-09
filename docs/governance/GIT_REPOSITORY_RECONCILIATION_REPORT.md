# GP-GIT-02 — Relatório de Reconciliação do Estado do Repositório

## 1. Identificação

| Campo | Estado verificado |
| --- | --- |
| Data | 28/07/2026 |
| Branch | `feature/environment-data-v1` |
| Upstream | `origin/feature/environment-data-v1` |
| HEAD local | `d0833bdb8da9979513e3fbb3ed24da65e858caf0` |
| HEAD remoto | `0c24e74aab9a514d2cab0ccc19a5eafd654621a9` |
| Relação local/remoto | 1 commit à frente; 0 atrás |
| Índice Git | Vazio |
| Conflitos registrados | Nenhum |
| Alterações modificadas | 13 |
| Arquivos não rastreados | 310 antes deste relatório |
| Grupos identificados | 9 |

## 2. Estado da branch e do remoto

O `fetch` executado imediatamente antes desta auditoria atualizou as referências do remoto. A branch local e sua upstream possuem o mesmo ancestral remoto:

`0c24e74aab9a514d2cab0ccc19a5eafd654621a9`

Não existem commits remotos ausentes localmente. Existe um commit local ainda não publicado.

## 3. Commit local pendente

| Hash | Mensagem | Arquivos | Situação |
| --- | --- | ---: | --- |
| `d0833bdb8da9979513e3fbb3ed24da65e858caf0` | `GP-AGIPI-01` | 9 | LOCAL; NÃO PUBLICADO |

O commit contém:

- `docs/institutional/AGIPI/EVIDENCE_DOSSIER.md`
- `docs/institutional/AGIPI/EXECUTION_PLAN.md`
- `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md`
- `docs/institutional/AGIPI/PACKAGE_RECONCILIATION_REPORT.md`
- `docs/institutional/AGIPI/PRESENTATION_OUTLINE.md`
- `docs/institutional/INSTITUTIONAL_MAP.md`
- `docs/institutional/INSTITUTIONAL_PROFILE.md`
- `docs/institutional/INSTITUTIONAL_ROADMAP.md`
- `docs/institutional/TECHNOLOGY_PORTFOLIO.md`

Os cinco arquivos AGIPI desse commit possuem modificações adicionais na worktree. Portanto, o commit local representa um estado anterior ao conjunto documental atualmente pendente.

## 4. Resumo por grupo

Estado anterior à criação deste relatório:

| Grupo | Modificados | Não rastreados | Total |
| --- | ---: | ---: | ---: |
| Governança AGIPI | 5 | 87 | 92 |
| Documentação institucional | 0 | 28 | 28 |
| Governança e pesquisa | 3 | 2 | 5 |
| Código-fonte e scripts | 2 | 1 | 3 |
| Testes | 0 | 1 | 1 |
| Dados | 2 | 1 | 3 |
| Mídia e produção audiovisual | 0 | 143 | 143 |
| Dependências e binários | 0 | 47 | 47 |
| Relatórios operacionais | 1 | 0 | 1 |
| **Total** | **13** | **310** | **323** |

Não foram identificados arquivos nomeados ou localizados explicitamente como cache ou temporário. Há saídas derivadas de análise, montagem e exportação dentro do conjunto audiovisual; elas foram classificadas como mídia de produção, não como temporários.

## 5. Inventário dos arquivos modificados

### 5.1 Governança AGIPI — 5

- `docs/institutional/AGIPI/EVIDENCE_DOSSIER.md`
- `docs/institutional/AGIPI/EXECUTION_PLAN.md`
- `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md`
- `docs/institutional/AGIPI/PACKAGE_RECONCILIATION_REPORT.md`
- `docs/institutional/AGIPI/PRESENTATION_OUTLINE.md`

### 5.2 Governança e pesquisa — 3

- `docs/architecture/ARCHITECTURAL_PRINCIPLES.md`
- `docs/history/HISTORY.md`
- `docs/roadmap/ROADMAP.md`

### 5.3 Código-fonte — 2

- `main.py`
- `relatorios.py`

### 5.4 Dados — 2

- `data/dados_ambientais_medicoes.csv`
- `data/qualidade_agua_medicoes.csv`

### 5.5 Relatório operacional — 1

- `reports/relatorio_operacional.txt`

## 6. Inventário dos arquivos não rastreados

### 6.1 Governança AGIPI — 87

#### Administração, certificação e remediação — 12

- `ADMINISTRATIVE_SUBMISSION_CHECKLIST.md`
- `AGIPI_REQUIREMENTS_TRACEABILITY_MATRIX.md`
- `AUT_01_DECISION_DEPENDENCY_MAP.md`
- `AUT_01_PENDING_INSTITUTIONAL_DECISIONS_MATRIX.md`
- `AUT_01_SEQUENTIAL_INSTITUTIONAL_REGULARIZATION_PLAN.md`
- `CERT_03_CONSOLIDATED_CERTIFICATION_MATRIX.md`
- `CERT_03_FINAL_INSTITUTIONAL_CERTIFICATION_REPORT.md`
- `CLS_05_DI_05_EXECUTION_REPORT.md`
- `CLS_06_DUE_DILIGENCE_REPORT.md`
- `REM_01_INSTITUTIONAL_REMEDIATION_REPORT.md`
- `REM_01_REMAINING_ISSUES_CHECKLIST.md`
- `REM_01_UPDATED_IMPEDIMENT_MATRIX.md`

#### Baseline e deliberação DI-DEC-01 — 14

- `DI_01A_APPROVED_DOCUMENTS.md`
- `DI_01A_BASELINE_DELIBERATION_MINUTES.md`
- `DI_01A_CONDITIONED_DOCUMENTS.md`
- `DI_01A_DELIBERATION_JUSTIFICATIONS_AND_HISTORY.md`
- `DI_01A_EXCLUDED_DOCUMENTS.md`
- `DI_BASELINE_CONSOLIDATED_INVENTORY.md`
- `DI_BASELINE_CONSOLIDATION_PENDING_REPORT.md`
- `DI_BASELINE_ELIGIBILITY_MATRIX.md`
- `DI_DEC_01_INCORPORATION_REGISTER.md`
- `DI_PROPOSED_OFFICIAL_DOCUMENTARY_BASELINE.md`
- `OFFICIAL_DOCUMENTARY_BASELINE.md`
- `OFFICIAL_DOCUMENTARY_BASELINE_FINAL_MATRIX.md`
- `OFFICIAL_DOCUMENTARY_BASELINE_HISTORY.md`
- `OFFICIAL_DOCUMENTARY_BASELINE_TRACEABILITY_REPORT.md`

#### Decisões, preparação e registros oficiais — 34

- `DI_01_INSTITUTIONAL_REPRESENTATION.md`
- `DI_02_APPROVAL_ARCHITECTURAL_PRINCIPLE.md`
- `DI_02_AUTHORSHIP_EVIDENCE_INVENTORY.md`
- `DI_02_AUTHORSHIP_OWNERSHIP_DELIBERATION_PREPARATORY_REPORT.md`
- `DI_02_AUTHORSHIP_OWNERSHIP_GAP_MATRIX.md`
- `DI_02_OWNERSHIP_EVIDENCE_INVENTORY.md`
- `DI_03_HISTORICAL_NAMESPACE_RECONCILIATION.md`
- `DI_03_LICENSING_DELIBERATION_PREPARATORY_REPORT.md`
- `DI_03_LICENSING_DOCUMENT_DEPENDENCY_MAP.md`
- `DI_03_LICENSING_EVIDENCE_INVENTORY.md`
- `DI_03_LICENSING_GAP_MATRIX.md`
- `DI_04_NAMESPACE_POLICY.md`
- `DI_04_PROPONENT_DELIBERATION_PREPARATORY_REPORT.md`
- `DI_04_PROPONENT_DOCUMENT_DEPENDENCY_MAP.md`
- `DI_04_PROPONENT_EVIDENCE_INVENTORY.md`
- `DI_04_PROPONENT_GAP_MATRIX.md`
- `DI_05_POLICY_AUTHORSHIP_OWNERSHIP_LICENSING_SUBMISSION.md`
- `DI_05_SUBMISSION_AUTHORIZATION_DELIBERATION_PREPARATORY_REPORT.md`
- `DI_05_SUBMISSION_AUTHORIZATION_DOCUMENT_DEPENDENCY_MAP.md`
- `DI_05_SUBMISSION_AUTHORIZATION_EVIDENCE_INVENTORY.md`
- `DI_05_SUBMISSION_AUTHORIZATION_GAP_MATRIX.md`
- `DI_DEC_02_INCORPORATION_HISTORY.md`
- `DI_DEC_02_INCORPORATION_REGISTER.md`
- `DI_DEC_02_TRACEABILITY_MATRIX.md`
- `DI_DEC_03_INCORPORATION_HISTORY.md`
- `DI_DEC_03_INCORPORATION_REGISTER.md`
- `DI_DEC_03_TRACEABILITY_MATRIX.md`
- `DI_DEC_04_INCORPORATION_HISTORY.md`
- `DI_DEC_04_INCORPORATION_REGISTER.md`
- `DI_DEC_04_TRACEABILITY_MATRIX.md`
- `DI_DEC_04_UPDATED_DOCUMENTS_REGISTER.md`
- `OFFICIAL_INSTITUTIONAL_AUTHORSHIP_REGISTER.md`
- `OFFICIAL_PROVISIONAL_INSTITUTIONAL_OWNERSHIP_REGISTER.md`
- `OFFICIAL_PROVISIONAL_INSTITUTIONAL_PROPONENT_REGISTER.md`

#### Licenciamento, auditoria e encerramento — 4

- `GP_AGIPI_01_AUDIT.md`
- `OFFICIAL_PROVISIONAL_LICENSING_COVERED_ASSETS.md`
- `OFFICIAL_PROVISIONAL_LICENSING_POLICY_REGISTER.md`
- `PATCH_AGIPI_CLOSURE_EVALUATION.md`

#### SUB-001 — 23

- `SUB_001_CONSOLIDATED_STATUS_REPORT.md`
- `SUB_001_DOCUMENTARY_COMPLIANCE_OPINION.md`
- `SUB_001_EXTERNAL_EVIDENCE_INCORPORATION_HISTORY.md`
- `SUB_001_EXTERNAL_EVIDENCE_INCORPORATION_REGISTER.md`
- `SUB_001_EXTERNAL_EVIDENCE_OFFICIAL_REGISTER.md`
- `SUB_001_EXTERNAL_EVIDENCE_POINT_COMPLIANCE_REVIEW.md`
- `SUB_001_EXTERNAL_EVIDENCE_TRACEABILITY_UPDATE.md`
- `SUB_001_EXTERNAL_REQUIREMENTS_COMPLIANCE_MATRIX.md`
- `SUB_001_EXTERNAL_REQUIREMENTS_VERIFICATION_REPORT.md`
- `SUB_001_HISTORY.md`
- `SUB_001_OFFICIAL_EXTERNAL_REQUIREMENTS_INVENTORY.md`
- `SUB_001_OFFICIAL_REGISTER.md`
- `SUB_001_PENDING_REQUIREMENTS_REGISTER.md`
- `SUB_001_TRACEABILITY_MATRIX.md`
- `SUB_001_UEPG_AGIPI_DOCUMENTARY_SUFFICIENCY_OPINION.md`
- `SUB_001_UEPG_AGIPI_GAP_MATRIX.md`
- `SUB_001_UEPG_AGIPI_UNIT_PROCESS_EVIDENCE_INVENTORY.md`
- `SUB_001_UEPG_AGIPI_UNIT_PROCESS_IDENTIFICATION_REPORT.md`
- `SUB_001_UNIT_PROCESS_DOCUMENTARY_SUFFICIENCY_OPINION.md`
- `SUB_001_UNIT_PROCESS_EVIDENCE_INVENTORY.md`
- `SUB_001_UNIT_PROCESS_GAP_MATRIX.md`
- `SUB_001_UNIT_PROCESS_IDENTIFICATION_REPORT.md`
- `SUB_001_UPDATED_DOCUMENTS_REGISTER.md`

### 6.2 Documentação institucional — 28

#### ICFACTORY Core — 11 — registro histórico dos antigos caminhos locais

A lista abaixo preserva os caminhos observados na data da auditoria como evidência histórica. A fonte vigente do framework é o [repositório canônico ICFACTORY](https://github.com/hendersonmauriciobatista-png/icfactory-framework).

- `ICFACTORY_CORE_v1/CONSTITUTION.md`
- `ICFACTORY_CORE_v1/CONSTITUTIONAL_LEXICON.md`
- `ICFACTORY_CORE_v1/DOCUMENT_MAP.md`
- `ICFACTORY_CORE_v1/GETTING_STARTED.md`
- `ICFACTORY_CORE_v1/GOVERNANCE_ARCHITECTURE.md`
- `ICFACTORY_CORE_v1/PROJECT_CONSTITUTION_TEMPLATE.md`
- `ICFACTORY_CORE_v1/concepts/ACI.md`
- `ICFACTORY_CORE_v1/concepts/ALO.md`
- `ICFACTORY_CORE_v1/concepts/AUDIT_PLAYBOOK.md`
- `ICFACTORY_CORE_v1/concepts/CIEX.md`
- `ICFACTORY_CORE_v1/concepts/OSE.md`

#### Documentação institucional geral — 9

- `docs/institutional/BUSINESS_POSITIONING.md`
- `docs/institutional/GP_PD_01_DOCUMENT_GOVERNANCE_IMPLEMENTATION.md`
- `docs/institutional/GP_PD_02_INSTITUTIONAL_RECONCILIATION_REPORT.md`
- `docs/institutional/GP_PD_03_DOCUMENT_ARCHITECTURE_REPORT.md`
- `docs/institutional/GP_PD_04_EVIDENCE_VALIDATION_REPORT.md`
- `docs/institutional/ICFACTORY_CONSTITUTION.md`
- `docs/institutional/INSTITUTIONAL_PRINCIPLES.md`
- `docs/institutional/MISSION_VISION_VALUES.md`
- `docs/institutional/RESEARCH_LINES.md`

#### H&A — 8

- `docs/institutional/HA/HA_ARCHITECTURAL_MAP.md`
- `docs/institutional/HA/HA_EVIDENCE_INVENTORY.md`
- `docs/institutional/HA/HA_INSTITUTIONAL_CORE_AUDIT.md`
- `docs/institutional/HA/HA_INSTITUTIONAL_DOSSIER.md`
- `docs/institutional/HA/HA_INSTITUTIONAL_PROFILE.md`
- `docs/institutional/HA/HA_PATRIMONIAL_RECONCILIATION.md`
- `docs/institutional/HA/HA_REPOSITORY_INTEGRATION_REPORT.md`
- `docs/institutional/HA/HA_SOURCE_VERIFICATION.md`

### 6.3 Governança e pesquisa — 2

- `docs/research/GP_ARQ_01_AUTHORITY_GATE_ARCHITECTURAL_RESEARCH.md`
- `docs/research/OEG_GIT_07_PHASE_I_INSTITUTIONAL_CLOSURE_REPORT.md`

### 6.4 Código, testes e dados — 3

- `administracao.py` — código-fonte
- `tests/test_administracao.py` — teste
- `data/eventos_operacionais.json` — dados operacionais

### 6.5 Mídia e produção audiovisual — 143

| Subconjunto | Quantidade | Conteúdo |
| --- | ---: | --- |
| Arquivos raiz e cenas SC001–SC012 | 15 | MP4s brutos/intermediários e `README.md` |
| `analysis/contact_sheets/` | 19 | JPGs de auditoria visual |
| `analysis/post_production_v1/` | 2 | PNGs de revisão |
| `audio/` sem dependências | 54 | narração, masters, ambiência, efeitos e homologação |
| `captures/` | 12 | PNGs das cenas institucionais |
| `exports/` | 8 | montagens, versões beta, RC e filme final |
| `external_assets/` | 2 | mídia externa declarada |
| `manifests/` | 3 | manifestos e relatório de montagem |
| `official_scenes/raw/` | 3 | tomadas brutas |
| `project/` | 9 | guias, checklists e projetos Kdenlive |
| `scripts/` | 6 | scripts de geração e montagem |
| `subtitles/` | 4 | SRTs e revisão |
| `titles/` | 3 | imagens de títulos |
| `visual_assets/` | 3 | ativos visuais RC |
| **Total** | **143** | |

### 6.6 Dependências e binários — 47

| Caminho | Quantidade | Classificação |
| --- | ---: | --- |
| `media/proteus_institutional_video/tools/python_libs/` | 46 | biblioteca OpenCV empacotada, metadados, DLL e `cv2.pyd` |
| `media/proteus_institutional_video/tools/wheels/` | 1 | wheel binário do OpenCV |

## 7. Dependências entre os grupos

| Conjunto | Dependências observadas |
| --- | --- |
| Commit local `GP-AGIPI-01` | Cinco documentos do commit possuem revisões posteriores na worktree |
| Governança AGIPI | Referencia Constituição, princípios arquiteturais, HISTORY, roadmap, baseline, decisões e registros institucionais ainda não rastreados |
| SUB-001 | Depende dos registros de proponente, autoria, titularidade, licenciamento e baseline do grupo AGIPI |
| Documentação H&A | É consumida pelo inventário, dossiê e relatórios AGIPI; mantém classificação própria |
| GP-ARQ-01 | Deve permanecer segregada como pesquisa experimental; não pertence ao patrimônio consolidado |
| Código operacional | `main.py` e `relatorios.py` coexistem com `administracao.py`, dados operacionais e `test_administracao.py` |
| Dados e relatório operacional | São produtos ou insumos do conjunto funcional; não integram o pacote documental AGIPI |
| Produção audiovisual | Scripts dependem de cenas, áudio, capturas, projetos e ativos externos |
| Dependências e binários | Servem aos scripts audiovisuais; são distintos da mídia final e da documentação |

## 8. Conjuntos potencialmente publicáveis de forma independente

| Conjunto | Separabilidade objetiva | Condição registrada |
| --- | --- | --- |
| Commit local `d0833bd` | Tecnicamente independente e linear em relação ao remoto | Representa estado anterior às cinco revisões AGIPI pendentes |
| Governança AGIPI/Fase I | Documentalmente distinguível de código, dados e mídia | Possui dependências cruzadas com documentos institucionais, arquitetura, HISTORY e roadmap |
| SUB-001 | Identificável por prefixo e cadeia própria | Depende de autoridades e registros da Fase I; permanece em preparação |
| ICFACTORY Core | Diretório autônomo com 11 documentos | Não está incorporado ao conjunto AGIPI por esta auditoria |
| H&A | Diretório documental autônomo com 8 arquivos | É referenciado por documentos AGIPI e deve preservar sua classificação |
| Código/testes/dados operacionais | Conjunto funcional distinguível | Código, teste, dados e relatório devem permanecer coerentes entre si |
| Produção audiovisual | Árvore própria e distinguível | Mídia, scripts, projetos, ativos externos e dependências formam subgrupos distintos |

A tabela registra separabilidade técnica e documental. Não constitui autorização de publicação.

## 9. Ponto seguro de sincronização

### Remoto

O histórico está linear: não há commits remotos a integrar e não existe conflito de histórico.

### Worktree

Não existe ponto seguro para um único commit abrangendo toda a worktree, porque:

- há nove grupos materialmente distintos;
- o índice está vazio;
- o conjunto mistura documentação, código, testes, dados, mídia e binários;
- cinco arquivos do commit local já possuem revisões posteriores;
- documentos AGIPI possuem referências cruzadas a outros documentos ainda não rastreados;
- GP-ARQ-01 deve permanecer segregada como pesquisa experimental;
- a árvore audiovisual contém mídia final, material bruto, scripts e dependências empacotadas.

O único ponto Git já delimitado é o commit local `d0833bd`; sua publicação isolada seria tecnicamente possível, mas não representaria o estado documental atual do Patch.

## 10. Impedimentos objetivos

1. Ausência de delimitação autorizada dos arquivos para cada commit.
2. Mistura de nove grupos na mesma worktree.
3. Dependências documentais cruzadas entre AGIPI e documentos institucionais não rastreados.
4. Revisões pendentes sobre cinco arquivos já presentes no commit local.
5. Código, testes, dados e relatório operacional não estão separados no índice.
6. Produção audiovisual contém 143 arquivos de mídia/produção e 47 dependências ou binários.
7. Nenhum arquivo está em staging.

## 11. Estado após o entregável

A criação deste relatório adiciona um único arquivo não rastreado:

- `docs/governance/GIT_REPOSITORY_RECONCILIATION_REPORT.md`

Após o entregável:

| Medida | Quantidade |
| --- | ---: |
| Arquivos modificados | 13 |
| Arquivos não rastreados | 311 |
| Arquivos em staging | 0 |
| Commits locais pendentes | 1 |
| Grupos materiais | 9 |

## 12. Validações

- Nenhum `git add` executado.
- Nenhum commit executado.
- Nenhum push executado.
- Nenhum merge ou rebase executado.
- Nenhum arquivo preexistente alterado, movido ou excluído.
- Nenhum conflito resolvido.
- Somente este relatório foi criado.

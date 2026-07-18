# GP-GIT-02 — Auditoria do Estado Pendente do Repositório

Data da auditoria: 18/07/2026  
Repositório: `SistemaAnaliseAgua`  
Branch: `feature/environment-data-v1`  
HEAD e upstream no início da auditoria: `fee8f66ef12e7f41f29973094915aab64e4ac8c7`  
Natureza: auditoria passiva, classificação e plano de particionamento  
Decisão: **NÃO_PRONTO**

## 1. Escopo e preservação

Esta auditoria examinou o estado pendente sem executar `git add`, `git commit`, `git push`, `git stash`, `git restore`, movimentação, renomeação ou exclusão. Nenhum arquivo preexistente foi editado. Este relatório é o único artefato criado, conforme autorização da OEG-GIT-02.

O snapshot auditado, anterior à criação deste relatório, continha 255 itens: 249 arquivos não rastreados e 6 arquivos rastreados modificados. Após a criação deste relatório, o total esperado passa a 256, sendo 250 não rastreados e 6 modificados.

## 2. Sumário executivo

| Grupo | Natureza | Não rastreados | Modificados | Tamanho dos não rastreados |
|---|---|---:|---:|---:|
| A | Pesquisa GDC-R / RG-01 a RG-09 / Fase I | 68 | 0 | 581.646 bytes |
| B | Institucional/metodológico fora de GDC-R | 3 | 0 | 26.482 bytes |
| C | Documental de outras iniciativas | 25 | 2 | 468.473 bytes |
| D | Funcional/dados operacionais | 1 | 2 | 17.622 bytes |
| E | Audiovisual e artefatos de produção | 97 | 0 | 267.630.116 bytes |
| F | Scripts, binários e dependências de tooling | 53 | 0 | 161.453.594 bytes |
| G | Temporário/gerado localmente | 2 | 0 | 3.834 bytes |
| H | Registros institucionais com conteúdo misto | 0 | 2 | — |
| **Total do snapshot** |  | **249** | **6** | **430.181.767 bytes** |

O corpus GDC-R é identificável, mas o encerramento institucional não pode ser versionado com integridade no estado atual. `HISTORY.md` e `ROADMAP.md` contêm alterações de GDC-R misturadas com PAC, produto, audiovisual, Build Week e governança de harnesses. Além disso, `PHASE_I_CONSOLIDATED_REPORT.md` não é citado em nenhum dos dois registros.

## 3. Método de classificação exaustiva

Os grupos abaixo são mutuamente exclusivos e cobrem todos os 255 itens do snapshot. A classificação foi aplicada nesta ordem de precedência:

1. Grupo A: arquivos `docs/research/RG_01_*` a `RG_09_*`, `docs/research/rg09_fixtures/**`, o relatório consolidado, PI-07A e os dois relatórios de apresentação exigidos por RG-06;
2. Grupo B: os três documentos institucionais listados na seção 5;
3. Grupo D: `data/**` pendente;
4. Grupo F: `media/**/scripts/**` e `media/**/tools/**`;
5. Grupo G: os dois manifests locais de concatenação listados na seção 10;
6. Grupo E: todo o restante de `media/proteus_institutional_video/**` e de `docs/presentation/**`;
7. Grupo C: os demais documentos pendentes;
8. Grupo H: os dois registros rastreados com diffs semanticamente mistos.

Assim, inclusive os arquivos com espaços no nome, todos os itens recebem uma única classificação. As contagens foram conferidas contra `git status --porcelain=v1 -uall`.

## 4. Grupo A — Pesquisa GDC-R e dependências diretas (68)

### 4.1 RG-01 a RG-05 e fundação PI-07/07A (23)

- `docs/research/RG_01_CLOSURE_REPORT.md`
- `docs/research/RG_01_RESEARCH_CONSTITUTION.md`
- `docs/research/RG_01_RESEARCH_ROADMAP.md`
- `docs/research/RG_02_CLOSURE_REPORT.md`
- `docs/research/RG_02_CONCEPTUAL_MODEL.md`
- `docs/research/RG_02_SEMANTIC_MATRIX.md`
- `docs/research/RG_03_ARCHITECTURAL_DIAGRAM.md`
- `docs/research/RG_03_ARCHITECTURE.md`
- `docs/research/RG_03_CLOSURE_REPORT.md`
- `docs/research/RG_03_INVARIANTS.md`
- `docs/research/RG_04_CLOSURE_REPORT.md`
- `docs/research/RG_04_DYNAMIC_MODEL.md`
- `docs/research/RG_04_PROPAGATION_MODEL.md`
- `docs/research/RG_04_STATE_MACHINE.md`
- `docs/research/RG_05_CASE_SELECTION_FRAMEWORK.md`
- `docs/research/RG_05_CLOSURE_REPORT.md`
- `docs/research/RG_05_EXPERIMENTAL_PROTOCOL.md`
- `docs/research/RG_05_HYPOTHESIS_OPERATIONALIZATION.md`
- `docs/research/RG_05_METRICS_AND_INTERPRETATION.md`
- `docs/research/RG_05_THREATS_TO_VALIDITY.md`
- `docs/research/PI_07A_DECISION_FOUNDATION_GOVERNANCE_REPORT.md`
- `docs/presentation/PI_07_KDENLIVE_PRE_POSTPRODUCTION_AUDIT.md`
- `docs/presentation/PI_07_POST_PRODUCTION_EXECUTION_REPORT.md`

### 4.2 RG-06 (6)

- `docs/research/RG_06_CASE_SELECTION.md`
- `docs/research/RG_06_CLOSURE_REPORT.md`
- `docs/research/RG_06_CP01_AUDIT.md`
- `docs/research/RG_06_CP01_EXECUTION.md`
- `docs/research/RG_06_CP01_RESULTS.md`
- `docs/research/RG_06_PREREGISTRATION.md`

### 4.3 RG-07 (7)

- `docs/research/RG_07_AUDIT.md`
- `docs/research/RG_07_CLOSURE_REPORT.md`
- `docs/research/RG_07_COMPARATIVE_MATRIX.md`
- `docs/research/RG_07_EXECUTION_A.md`
- `docs/research/RG_07_EXECUTION_B.md`
- `docs/research/RG_07_EXPERIMENT_PLAN.md`
- `docs/research/RG_07_INDEPENDENCE_PROTOCOL.md`

### 4.4 RG-08 (6)

- `docs/research/RG_08_ARCHITECTURAL_IMPACTS.md`
- `docs/research/RG_08_CLASSIFICATION_CRITERIA.md`
- `docs/research/RG_08_CLOSURE_REPORT.md`
- `docs/research/RG_08_EXECUTABILITY_CHECKLIST.md`
- `docs/research/RG_08_EXECUTABILITY_FRAMEWORK.md`
- `docs/research/RG_08_PACKAGE_INTEGRITY_PROTOCOL.md`

### 4.5 RG-09 e fixtures (25)

- `docs/research/RG_09_CLOSURE_REPORT.md`
- `docs/research/RG_09_EXECUTION_REPORT.md`
- `docs/research/RG_09_FINAL_ANALYSIS.md`
- `docs/research/RG_09_RESULTS_MATRIX.md`
- `docs/research/RG_09_SYNTHETIC_EXPERIMENT_PLAN.md`
- `docs/research/RG_09_TEST_CASES.md`
- `docs/research/RG_09_THREATS_TO_VALIDITY.md`
- `docs/research/rg09_fixtures/case_a/authority.md`
- `docs/research/rg09_fixtures/case_a/input.md`
- `docs/research/rg09_fixtures/case_a/instrument.md`
- `docs/research/rg09_fixtures/case_a/output_contract.md`
- `docs/research/rg09_fixtures/case_a/package_manifest.md`
- `docs/research/rg09_fixtures/case_a/procedure.md`
- `docs/research/rg09_fixtures/case_b/authority.md`
- `docs/research/rg09_fixtures/case_b/input.md`
- `docs/research/rg09_fixtures/case_b/instrument.md`
- `docs/research/rg09_fixtures/case_b/output_contract.md`
- `docs/research/rg09_fixtures/case_b/package_manifest.md`
- `docs/research/rg09_fixtures/case_b/procedure.md`
- `docs/research/rg09_fixtures/case_c/authority.md`
- `docs/research/rg09_fixtures/case_c/instrument.md`
- `docs/research/rg09_fixtures/case_c/output_contract.md`
- `docs/research/rg09_fixtures/case_c/package_manifest.md`
- `docs/research/rg09_fixtures/case_c/procedure.md`
- `docs/research/rg09_fixtures/case_d/SCENARIO_DECLARATION.md`

### 4.6 Consolidação (1)

- `docs/research/PHASE_I_CONSOLIDATED_REPORT.md`

## 5. Grupo B — Institucional/metodológico fora da pesquisa GDC-R (3)

- `docs/governance/PAC_CONSTITUTION.md` — constituição do PAC;
- `docs/research/DISCOVERY_CATALOG.md` — catálogo institucional de discoveries;
- `docs/research/HARNESS_GOVERNANCE_RESEARCH_DOSSIER.md` — dossiê GP-HA08.

Esses documentos possuem valor institucional, mas não pertencem ao fechamento GDC-R e exigem commits próprios.

## 6. Grupo C — Documentação de outras iniciativas (27 itens: 25 novos e 2 modificados)

### 6.1 Não rastreados (25)

- `docs/adoption/ADOPTION_CHECKLIST.md`
- `docs/adoption/CONTACT_PACKAGE.md`
- `docs/adoption/FIRST_CONTACT_CANDIDATE.md`
- `docs/adoption/FIRST_CONTACT_MESSAGE.md`
- `docs/adoption/FIRST_CONTACT_STRATEGY.md`
- `docs/adoption/USER_TARGET_MAP.md`
- `docs/buildweek/BW_01_ACTION_PLAN.md`
- `docs/buildweek/BW_01_OPENAI_BUILD_WEEK_AUDIT.md`
- `docs/buildweek/BW_01_SOURCE_REGISTER.md`
- `docs/domain/GP_D01C_PERSISTENCE_STRATEGY_AUDIT.md`
- `docs/pac/PAC_01_ENGINEERING_FINDINGS.md`
- `docs/pac/PAC_02_ENGINEERING_SANITARY_FINDINGS.md`
- `docs/pac/PAC_03_SOFTWARE_ARCHITECTURE_FINDINGS.md`
- `docs/pac/PAC_04_SOFTWARE_ENGINEERING_FINDINGS.md`
- `docs/pac/PAC_05_INFORMATION_SECURITY_FINDINGS.md`
- `docs/pac/PAC_06_DATABASE_PERSISTENCE_FINDINGS.md`
- `docs/pac/PAC_07_UX_UI_FINDINGS.md`
- `docs/pac/PAC_08_PRODUCT_MANAGEMENT_FINDINGS.md`
- `docs/pac/PAC_09_ACADEMIC_EVALUATION_FINDINGS.md`
- `docs/pac/PAC_12A_FINAL_COLLECTION_AUDIT.md`
- `docs/pac/PAC_13_OFFICIAL_CONVERGENCE_CONSOLIDATION.md`
- `docs/pac/PAC_14_PROJECT_EVOLUTION_PLAN.md`
- `docs/pac/PAC_CONSOLIDATED_FINDINGS.md`
- `docs/pac/PAC_FIRST_CYCLE_CONSOLIDATION.md`
- `docs/pac/PE_01_IMPLEMENTATION_EXECUTION_STRATEGY.md`

### 6.2 Modificados (2)

- `README.md`
- `reports/relatorio_operacional.txt`

## 7. Grupo D — Funcional/dados operacionais (3 itens: 1 novo e 2 modificados)

- `data/eventos_operacionais.json` — não rastreado;
- `data/dados_ambientais_medicoes.csv` — modificado;
- `data/qualidade_agua_medicoes.csv` — modificado.

Este grupo altera estado de dados do PROTEUS e não deve ser incluído em nenhum commit documental sem validação funcional própria.

## 8. Grupo E — Audiovisual e produção (97)

Inventário exaustivo por conjunto, após excluir os dois documentos do Grupo A, os scripts/tooling do Grupo F e os manifests locais do Grupo G:

- 9 documentos em `docs/presentation/`: `PROTEUS_ANIMATIC_V1_REVIEW.md`, `PROTEUS_AUDIOVISUAL_PRODUCTION_READINESS.md`, `PROTEUS_FILM_REVIEW.md`, `PROTEUS_INSTITUTIONAL_FILM_PRODUCTION_REPORT.md`, `PROTEUS_INSTITUTIONAL_VIDEO_SCRIPT.md`, `PROTEUS_INSTITUTIONAL_VIDEO_STORYBOARD.md`, `PROTEUS_SCREEN_CAPTURE_PLAN.md`, `PROTEUS_SHORT_VIDEO_SCRIPT.md` e `PROTEUS_VIDEO_EDITING_GUIDE.md`;
- 19 JPEGs em `media/proteus_institutional_video/analysis/contact_sheets/`;
- 2 PNGs em `media/proteus_institutional_video/analysis/post_production_v1/`;
- 15 arquivos de narração em `media/proteus_institutional_video/audio/narration/assembly_cut_v1/`;
- 4 arquivos de narração diretamente em `media/proteus_institutional_video/audio/narration/`;
- 12 PNGs em `media/proteus_institutional_video/captures/`;
- 3 MP4s em `media/proteus_institutional_video/exports/`;
- 3 manifests Markdown em `media/proteus_institutional_video/manifests/`;
- 8 arquivos de projeto em `media/proteus_institutional_video/project/`, incluindo um `.kdenlive`;
- `media/proteus_institutional_video/README.md`;
- 14 gravações MP4 diretamente em `media/proteus_institutional_video/`: `SC001.mp4` a `SC012.mp4`, `2026-07-12 23-22-56.mp4` e `2026-07-12 23-26-35.mp4`;
- 4 arquivos em `media/proteus_institutional_video/subtitles/`;
- 3 PNGs em `media/proteus_institutional_video/titles/`.

Distribuição por extensão: 38 `.md`, 19 `.jpg`, 17 `.png`, 15 `.mp4`, 3 `.srt`, 2 `.txt` e 1 `.kdenlive`. O maior arquivo é `SC002.mp4`, com 160.793.525 bytes. O grupo requer decisão sobre Git LFS, retenção de fontes, autoria/licenças e duplicidade de exports antes de versionamento.

## 9. Grupo F — Scripts, binários e dependências de tooling (53)

- 6 scripts em `media/proteus_institutional_video/scripts/`: quatro scripts de build (`.ps1`/`.cmd`) e dois scripts Python;
- 46 arquivos de uma instalação extraída de OpenCV em `media/proteus_institutional_video/tools/python_libs/`, incluindo `cv2.pyd` (85.848.064 bytes), `opencv_videoio_ffmpeg500_64.dll` (30.876.160 bytes), stubs, metadados e licenças;
- 1 wheel em `media/proteus_institutional_video/tools/wheels/opencv_python_headless-5.0.0.93-cp37-abi3-win_amd64.whl` (43.825.962 bytes).

Os 6 scripts autorais são logicamente separáveis das 47 dependências vendorizadas. As dependências não devem ser publicadas antes de uma decisão explícita entre lockfile/instalação reproduzível, release artifact, Git LFS ou vendor controlado, acompanhada de revisão de licença e segurança.

## 10. Grupo G — Temporários/gerados localmente (2)

- `media/proteus_institutional_video/exports/assembly_cut_v1/assembly_cut_v1.ffconcat`
- `media/proteus_institutional_video/exports/final/institutional_film_v1_concat.txt`

São listas de concatenação de build e não devem entrar nos commits propostos. A decisão futura adequada é confirmar sua regenerabilidade e então autorizar exclusão e/ou regra de `.gitignore`; nenhuma dessas ações foi executada nesta auditoria.

Também foram encontrados 3.502 caminhos ignorados. Desses, 3.426 pertencem a `venv/`; 76 estão fora de `venv/` e são caches Python (`__pycache__`/`.pyc`), inclusive 9 sob tooling audiovisual. Nenhum ignorado deve ser versionado.

## 11. Grupo H — HISTORY e ROADMAP mistos (2)

### `docs/history/HISTORY.md`

Diff total: 2.708 linhas adicionadas e 124 removidas. O primeiro hunk (`@@ -2,0 +3,412 @@`) contém RG-01 a RG-09 e PI-07/PI-07A. Os hunks seguintes incluem, no mesmo arquivo, iniciativas patrimoniais, PAC, produto, audiovisual, GP-HA08 e Build Week. O hunk final inicia em `@@ -2786,0 +5326,45 @@` e pertence a Build Week.

### `docs/roadmap/ROADMAP.md`

Diff total: 965 linhas adicionadas e 1 removida. O bloco da família GP-RG começa no hunk `@@ -1161,0 +1969,107 @@`; os demais hunks incluem produto, PAC, audiovisual, Build Week e GP-HA08.

Conclusão: nenhum dos dois arquivos pode ser adicionado integralmente a um commit exclusivo de GDC-R. O uso de staging interativo dos hunks existentes também é inadequado para o fechamento institucional: preservaria um registro parcial enquanto o relatório consolidado não consta dos arquivos e deixaria iniciativas interdependentes sem registro coerente.

## 12. Dependências RG-01 a RG-09

Foram examinadas referências Markdown no corpus do Grupo A. Resultado:

- 227 ocorrências apontam para 49 documentos não rastreados únicos do próprio corpus;
- 6 ocorrências apontam para arquivos rastreados;
- os dois alvos rastreados únicos são `docs/history/HISTORY.md` e `docs/roadmap/ROADMAP.md`;
- não foram encontrados alvos Markdown quebrados ou ambíguos;
- os nomes repetidos `authority.md`, `input.md`, `instrument.md`, `output_contract.md`, `package_manifest.md` e `procedure.md` são fixtures deliberadamente isoladas por caso, não duplicidades acidentais;
- `PHASE_I_CONSOLIDATED_REPORT.md` existe, mas não é referenciado por `HISTORY.md` nem por `ROADMAP.md`, caracterizando documento órfão no plano registral.

Há ainda fontes de autoridade citadas textualmente, mas não preservadas como arquivos do repositório: deliberação formal de RG-05, OEG-RG-06, OEG-RG-07, OEG/DF-RG-08 e OEG/DF-RG-09. RG-07 registra expressamente que a OEG-RG-06 ficou fora do workspace. Isso é uma lacuna de proveniência externa, não um link Markdown quebrado, e não deve ser corrigido retroativamente sem nova autoridade.

Fluxo lógico apurado:

`RG-01 → RG-02 → RG-03 → RG-04 → RG-05 → RG-06 → RG-07 → RG-08 → RG-09 → PHASE_I_CONSOLIDATED_REPORT`

RG-06 também depende dos dois relatórios PI-07 de `docs/presentation/`; por isso eles foram classificados no Grupo A, apesar da localização.

## 13. Duplicidades e documentos órfãos

Duplicidades de conteúdo exato encontradas fora de GDC-R:

- sete PNGs audiovisuais compartilham o mesmo SHA-256: as três imagens de abertura, a imagem de encerramento e os três títulos;
- as duas cópias de `LICENSE.txt` do OpenCV são idênticas;
- as duas cópias de `LICENSE-3RD-PARTY.txt` do OpenCV são idênticas.

Essas duplicidades exigem decisão nos commits audiovisual/tooling, mas não afetam a integridade do corpus GDC-R. O único órfão institucional identificado no Grupo A é o relatório consolidado ausente de HISTORY/ROADMAP. As autoridades externas ausentes constituem ressalva de proveniência.

## 14. Plano de commits proposto

Nenhum commit deste plano está autorizado por este relatório. A execução deve ocorrer somente após nova aprovação e nova conferência do status.

### Sequência GDC-R

1. **`Establish GDC-R research baseline through RG-05`** — exatamente os 23 arquivos da seção 4.1. Dependência: preservar a ressalva sobre a autoridade externa de RG-05.
2. **`Add GDC-R empirical pilots RG-06 and RG-07`** — exatamente os 13 arquivos das seções 4.2 e 4.3. Dependência: commit 1; preservar os registros históricos de autoridade externa.
3. **`Define GX-PKG executability protocol in RG-08`** — exatamente os 6 arquivos da seção 4.4. Dependência: commit 2.
4. **`Validate GX-PKG with RG-09 synthetic pilot`** — exatamente os 25 arquivos da seção 4.5. Dependência: commit 3.
5. **`Finalize Phase I of GDC-R research`** — `docs/research/PHASE_I_CONSOLIDATED_REPORT.md` e atualizações integrais, previamente autorizadas e já desmisturadas, de `docs/history/HISTORY.md` e `docs/roadmap/ROADMAP.md`. Dependência: commits 1–4 e resolução registral do Grupo H.

O arquivo desta auditoria deve integrar um commit institucional próprio ou o commit que formalizar a política de particionamento; não deve ser inserido silenciosamente em nenhum dos cinco commits científicos.

### Sequência paralela necessária para árvore limpa

1. commit(s) institucionais separados para Grupo B;
2. commits por iniciativa para adoção, Build Week, domínio/PAC e demais itens do Grupo C;
3. validação funcional e commit separado para Grupo D;
4. decisão de retenção/LFS/licenças e commits próprios para Grupo E;
5. separar os 6 scripts autorais e resolver as 47 dependências vendorizadas do Grupo F;
6. autorizar tratamento de Grupo G e caches ignorados;
7. somente depois, consolidar integralmente `HISTORY.md` e `ROADMAP.md` com todas as iniciativas efetivamente versionadas.

Para evitar que o estado misto da árvore atual contamine os commits, a execução futura deve usar seleção por listas exatas e validação de `git diff --cached --name-status` e `git diff --cached --check` antes de cada commit. Uma worktree limpa dedicada é recomendável se houver autorização para copiar os arquivos pendentes controladamente; não foi criada nesta auditoria.

## 15. Critério de árvore limpa

A publicação exclusiva dos 68 arquivos do Grupo A não produzirá árvore limpa: restariam 181 arquivos não rastreados do snapshot, 6 modificados e este relatório. Portanto, a árvore limpa depende da resolução legítima dos Grupos B a H, não de descarte genérico.

Antes de qualquer push, devem ser verificados:

- cada commit contém somente a iniciativa declarada;
- nenhum arquivo dos Grupos D, E, F ou G entrou por `git add .`;
- `HISTORY.md` e `ROADMAP.md` refletem apenas conteúdo já versionado;
- o relatório consolidado deixa de estar órfão;
- `git status --short` fica vazio no ambiente de publicação;
- HEAD local e remoto correspondem após o push.

## 16. Decisão final

**NÃO_PRONTO**.

Fundamentos objetivos:

1. `HISTORY.md` e `ROADMAP.md` estão semanticamente misturados e não podem compor um commit de encerramento GDC-R íntegro;
2. `PHASE_I_CONSOLIDATED_REPORT.md` ainda não está registrado em HISTORY/ROADMAP;
3. as ordens/deliberações externas citadas por RG-05 a RG-09 não estão preservadas no repositório;
4. há 430.181.767 bytes de novos arquivos, dos quais aproximadamente 408 MB são audiovisual/tooling e exigem decisão específica;
5. o versionamento do Grupo A, isoladamente, não satisfaz o requisito de árvore limpa;
6. os dois arquivos gerados do Grupo G e os caches ignorados exigem tratamento autorizado, não descarte automático.

O corpus científico pode ser preparado em quatro commits incrementais (RG-01–05, RG-06–07, RG-08 e RG-09), mas o quinto commit de encerramento institucional permanece bloqueado até autorização para corrigir o registro consolidado e particionar as demais iniciativas.

## 17. Aprovação requerida

Solicita-se aprovação explícita, em nova ordem, para:

1. preparar e revisar os quatro commits científicos incrementais, sem commit/push automático;
2. autorizar a atualização registral mínima de `HISTORY.md` e `ROADMAP.md` para a Fase I;
3. definir a política para mídia, Git LFS, tooling vendorizado e arquivos gerados;
4. somente após essas decisões, preparar o commit institucional final e apresentar o diff staged para aprovação.

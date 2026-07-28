# GP-CERT-03 — Matriz Consolidada de Certificação

## Identificação

| Campo | Registro |
| --- | --- |
| Data-base | 27/07/2026 |
| Objeto | Pacote Institucional ICFACTORY para submissão à AGIPI/sprinT |
| Natureza | Certificação documental consolidada |
| Escala | ATENDE; ATENDE COM RESSALVAS; NÃO ATENDE |

## Matriz consolidada

| Domínio auditado | Classificação | Evidências utilizadas | Pendências remanescentes |
| --- | --- | --- | --- |
| Constituição vigente | ATENDE COM RESSALVAS | `docs/institutional/ICFACTORY_CONSTITUTION.md`; histórico das GPs; verificação da worktree | O documento está presente e não foi alterado por esta GP, porém não integra a baseline Git atual. |
| Arquitetura institucional | ATENDE COM RESSALVAS | `docs/architecture/ARCHITECTURAL_PRINCIPLES.md`; DI-02; DI-03; DI-04; PAR-ICF-001 | O conteúdo arquitetural e sua cadeia de autoridade são coerentes, mas o documento arquitetural está modificado e os documentos canônicos das decisões ainda não estão versionados. |
| Maturidade normativa | ATENDE COM RESSALVAS | DI-01 a DI-05; PAR-ICF-001; Constituição; `HISTORY.md` | As autoridades e limites estão documentados; falta consolidá-los na baseline. DI-05 disciplina o processo, mas não preenche autoria, titularidade, licença ou autorização específica. |
| Governança documental | ATENDE COM RESSALVAS | `HISTORY.md`; Inventário; Dossiê; Relatório de Reconciliação; GP-CLS-01 a GP-CLS-06 | Existem inventário, histórico, estados e ressalvas. A worktree mista, os documentos não rastreados e as evidências `CANDIDATA` impedem considerar o conjunto consolidado. |
| Rastreabilidade das decisões | ATENDE COM RESSALVAS | DI-01; DI-02; DI-03 histórica; DI-04; DI-05; PAR-ICF-001; `HISTORY.md` | A cadeia lógica está documentada, inclusive a superação histórica da DI-03 pela DI-04. A cadeia ainda não está preservada em uma baseline Git consolidada. |
| Conformidade com PAR-ICF-001 | ATENDE COM RESSALVAS | `ARCHITECTURAL_PRINCIPLES.md`; DI-02; DI-03; DI-04; documentos das GPs de incorporação | Auditoria, decisão, documento canônico e incorporação foram separados. A incorporação permanece sem consolidação de versionamento, e esta certificação não pode substituí-la. |
| Política de namespaces | ATENDE COM RESSALVAS | DI-04; DI-03 histórica; identificador `PAR-ICF-001` no documento arquitetural | A colisão foi resolvida documentalmente e os aliases históricos foram preservados. DI-04 e DI-03 ainda não integram a baseline Git. |
| Integridade do patrimônio institucional | ATENDE COM RESSALVAS | Inventário Institucional; Relatório de Reconciliação; Dossiê de Evidências | Os ativos e suas limitações estão inventariados; o pacote continua candidato à consolidação e contém evidências ainda candidatas ou lacunas declaradas. |
| Segregação de pesquisas experimentais | ATENDE | Relatório de Reconciliação; Plano Executivo; Inventário; GP-ARQ-01 | GP-ARQ-01 permanece experimental, fora da Constituição e do portfólio consolidado; não foi identificada promoção implícita. |
| Maturidade dos casos institucionais | ATENDE COM RESSALVAS | Inventário; Portfólio; Dossiê; Relatório de Reconciliação | PROTEUS e H&A estão representados sem elevação artificial; H&A permanece M1 provisório. Evidências operacionais e validações externas permanecem limitadas. |
| Representação institucional | ATENDE | DI-01; Plano Executivo; Roteiro de Apresentação | Henderson Mauricio Batista está designado para interlocução, com competências e limites expressos. A representação não equivale a autorização de submissão. |
| Autoria institucional | NÃO ATENDE | DI-05; GP-CLS-03; relatório GP-CLS-05 | Autoria intelectual não está formalizada por ativo. |
| Titularidade | NÃO ATENDE | DI-05; Inventário; relatório GP-CLS-05 | Não existe documento próprio formalizando a titularidade do patrimônio metodológico/documental. |
| Licenciamento | NÃO ATENDE | DI-05; relatório GP-CLS-05; checklist administrativo | Existe apenas proposta sem efeito normativo; nenhuma licença institucional foi aprovada para o pacote. |
| Autorização para submissão | NÃO ATENDE | DI-01; DI-05; Plano Executivo; checklist administrativo | Não existe decisão específica autorizando o envio nem aprovação da versão exata a submeter. |
| Regularização administrativa | NÃO ATENDE | GP-CLS-03; GP-CLS-04; GP-CLS-05; checklist administrativo | DI-05 criou a política, mas as definições e autorizações exigidas por ela continuam pendentes. |
| Aderência aos requisitos externos | NÃO ATENDE | GP-CLS-06; `AGIPI_REQUIREMENTS_TRACEABILITY_MATRIX.md` | A due diligence registrou 3 requisitos que atendem, 10 que atendem parcialmente e 12 que não atendem. |
| Campus, proponente e formulário | NÃO ATENDE | GP-CLS-06; checklist administrativo | Campus e forma do proponente não definidos; formulário aplicável não concluído; chamada e requisitos do campus não integralmente confirmados. |
| Baseline documental | NÃO ATENDE | GP-CERT-02; GP-CLS-02; estado Git verificado em 27/07/2026 | Constituição, DI-01 a DI-05 e relatórios recentes existem localmente, mas permanecem fora da baseline Git; há worktree mista e arquivos institucionais não rastreados. |
| Prontidão para submissão externa | NÃO ATENDE | Conjunto integral acima, especialmente DI-05, GP-CLS-05 e GP-CLS-06 | Persistem impedimentos administrativos, documentais, de versionamento e dependências externas. |

## Consolidação das certificações anteriores

| Entrada obrigatória | Evidência disponível nesta certificação | Efeito preservado |
| --- | --- | --- |
| GP-CERT-01 | Resultado histórico do ciclo e documentos que motivaram GP-CLS-01 | Ausência canônica da DI-03 foi o ponto documental tratado posteriormente. |
| GP-CERT-02 | Resultado histórico do ciclo; estado Git atual; DI-03 canônica | DI-03 foi regularizada, mas baseline, validação, evidências e submissão permaneceram pendentes. |
| GP-CLS-01 | DI-03 canônica e `HISTORY.md` | Não conformidade da ausência documental da DI-03 resolvida. |
| GP-CLS-02 | Estado atual do Git e inventário documental | Preparação não equivale a consolidação; documentos permanecem fora da baseline. |
| GP-CLS-03 | DI-05 e relatório GP-CLS-05 | Lacunas administrativas foram identificadas sem presunção. |
| GP-CLS-04 | DI-05 canônica, Inventário, Dossiê, Relatório de Reconciliação e Histórico | Política incorporada; seu conteúdo não resolve automaticamente os requisitos. |
| GP-CLS-05 | `CLS_05_DI_05_EXECUTION_REPORT.md` e checklist | Regularização administrativa permanece parcial. |
| GP-CLS-06 | Relatório e matriz de aderência | Parecer preservado: não pronto para submissão. |

## Limitação documental

Não foram localizados artefatos autônomos denominados GP-CERT-01, GP-CERT-02, GP-CLS-02 ou GP-CLS-03 na árvore documental atual. Esta matriz utiliza somente seus efeitos materializados nos documentos posteriores, no histórico e no estado do repositório. Nenhum conteúdo ausente foi reconstruído.

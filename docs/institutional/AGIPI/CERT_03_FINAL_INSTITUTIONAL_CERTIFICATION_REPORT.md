# GP-CERT-03 — Certificação Final do Pacote Institucional AGIPI

## 1. Identificação

| Campo | Registro |
| --- | --- |
| Instrumento | GP-CERT-03 |
| Data-base | 27/07/2026 |
| Objeto | Estado consolidado do Pacote Institucional ICFACTORY |
| Natureza | Exclusivamente certificadora |
| Alteração normativa | Nenhuma |
| Commit, push ou submissão | Não executados |

## 2. Base da certificação

Foram examinados os efeitos documentais disponíveis das GPs GP-CERT-01, GP-CERT-02 e GP-CLS-01 a GP-CLS-06, além da Constituição, DI-01 a DI-05, PAR-ICF-001, Inventário, Dossiê, Relatório de Reconciliação, Plano Executivo, checklist administrativo, histórico e estado Git.

GP-CERT-01, GP-CERT-02, GP-CLS-02 e GP-CLS-03 não foram localizadas como relatórios autônomos na árvore atual. Seus resultados somente foram considerados quando preservados por documentos posteriores, histórico ou estado verificável do repositório.

## 3. Conformidades comprovadas

1. A Constituição permanece como referência institucional e não foi alterada por esta certificação.
2. DI-01 documenta a representação institucional e preserva limites que impedem autorização automática de submissão.
3. DI-02 preserva a autoridade do conteúdo do princípio.
4. DI-03 está documentada como decisão exclusivamente histórica, superada pela DI-04 quanto à identificação.
5. DI-04 institui o namespace vigente `PAR-ICF` e o identificador `PAR-ICF-001`.
6. PAR-ICF-001 está incorporado ao documento de Princípios Arquiteturais.
7. DI-05 institui a governança de autoria, titularidade, licenciamento e submissão sem preencher automaticamente essas matérias.
8. GP-ARQ-01 permanece experimental e fora do patrimônio institucional consolidado.
9. H&A permanece M1 provisório, sem elevação artificial de maturidade.
10. O processo externo vigente e seus requisitos gerais foram objeto de due diligence oficial na GP-CLS-06.

## 4. Maturidade institucional

### 4.1 Maturidade arquitetural

**ATENDE COM RESSALVAS.**

A arquitetura possui princípios identificados, cadeia de autoridade e segregação entre auditoria, decisão e incorporação documental. A ressalva decorre da ausência de consolidação Git dos documentos canônicos e da modificação ainda não consolidada do documento arquitetural.

### 4.2 Maturidade normativa

**ATENDE COM RESSALVAS.**

DI-01 a DI-05 possuem conteúdos e limites coerentes. DI-03 foi preservada historicamente, e DI-04 permanece a autoridade vigente do namespace. O conjunto normativo existe localmente, mas não integra integralmente a baseline versionada.

### 4.3 Maturidade documental

**ATENDE COM RESSALVAS.**

O pacote contém Perfil, Portfólio, Inventário, Dossiê, Plano, Mapa, decisões e relatórios. Entretanto:

- o Relatório de Reconciliação ainda o classifica como candidato à consolidação;
- o Dossiê contém evidências `CANDIDATA`;
- documentos obrigatórios permanecem não rastreados pelo Git;
- a worktree é mista e não representa uma baseline consolidada.

### 4.4 Maturidade administrativa

**NÃO ATENDE.**

Persistem, conforme DI-05, GP-CLS-05 e checklist:

- autoria intelectual por ativo não formalizada;
- titularidade não formalizada;
- licenciamento não aprovado;
- proponente não definido;
- autorização específica de submissão inexistente;
- versão exata para envio não aprovada.

### 4.5 Maturidade para submissão externa

**NÃO ATENDE.**

Além das pendências administrativas, GP-CLS-06 comprovou:

- campus destinatário não escolhido;
- chamada e formulário do campus não integralmente confirmados;
- formulário não preenchido;
- dados de equipe e negócio incompletos para a inscrição;
- 12 requisitos externos classificados como `NÃO ATENDE`;
- 10 requisitos classificados como `ATENDE PARCIALMENTE`.

## 5. Governança e rastreabilidade

A cadeia decisória disponível é:

`GP-ADM-02 → DI-01 → GP-ADM-02A → EUREKA → DI-02 → DI-03 histórica → DI-04 → PAR-ICF-001 → arquitetura normativa`

A DI-05 acrescenta a política administrativa sem substituir DI-01 ou alterar PAR-ICF-001.

Essa estrutura é compatível com o PAR-ICF-001 quanto à separação entre auditoria, autoridade, decisão, documento canônico e incorporação. A ressalva é material: os documentos canônicos ainda não estão preservados em baseline Git consolidada.

## 6. Pendências administrativas

1. formalização da autoria;
2. formalização da titularidade;
3. aprovação do licenciamento aplicável;
4. definição do proponente;
5. decisão autorizativa da submissão;
6. aprovação da versão exata do pacote.

## 7. Dependências externas

1. obtenção do inteiro teor oficial do regulamento vigente;
2. escolha e confirmação do campus destinatário;
3. confirmação da chamada, vagas, formulário e documentos aplicáveis;
4. confirmação de categorias de proponente não expressamente documentadas, se pretendidas;
5. avaliação oficial do nível e da elegibilidade pela sprinT.

## 8. Impedimentos objetivos à submissão

- inexistência de autorização institucional específica;
- autoria, titularidade e licenciamento pendentes;
- proponente e campus indefinidos;
- formulário aplicável não concluído;
- baseline documental não consolidada;
- aderência externa incompleta conforme GP-CLS-06.

## 9. Parecer Final de Certificação

**NÃO CERTIFICADO PARA SUBMISSÃO.**

O Pacote Institucional possui arquitetura e governança normativas estruturadas, decisões rastreáveis e separação adequada das pesquisas experimentais. Essas conformidades não eliminam os impedimentos administrativos, documentais, de versionamento e externos comprovados.

Este parecer preserva os resultados anteriores: não reabre decisões, não modifica classificações sem evidência e não substitui a autoridade da Direção do Projeto.

## 10. Preservação e validações

Esta certificação:

- não criou requisito, política ou decisão;
- não alterou Constituição, princípios, decisões ou documentos canônicos;
- não preencheu lacunas por inferência;
- não executou commit, push ou submissão;
- utilizou somente evidências documentais existentes;
- mantém GP-ARQ-01 experimental e H&A em M1 provisório.

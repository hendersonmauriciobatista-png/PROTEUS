# GP-GIT-03 — Plano de Reorganização para Publicação

## 1. Identificação

| Campo | Registro |
| --- | --- |
| Documento de referência | `docs/governance/GIT_REPOSITORY_RECONCILIATION_REPORT.md` |
| Branch observada pela GP-GIT-02 | `feature/environment-data-v1` |
| Data | 28/07/2026 |
| Natureza | Planejamento documental |
| Operações Git executadas | Nenhuma |
| Reorganização executada | Nenhuma |

## 2. Critério de decomposição

Os 9 grupos amplos da GP-GIT-02 foram decompostos conforme:

- finalidade documental ou operacional;
- cadeia de autoridade;
- vínculo com o Patch AGIPI ou com a SUB-001;
- caráter experimental;
- dependência funcional;
- presença de mídia, arquivos derivados ou binários;
- possibilidade de formar um commit semanticamente único.

O plano identifica 12 conjuntos. Um deles é o commit local já existente; os outros 11 classificam os 325 arquivos pendentes após a criação deste plano.

## 3. Inventário consolidado dos conjuntos

| ID | Conjunto | Arquivos | Natureza | Publicação isolada |
| --- | --- | ---: | --- | --- |
| PUB-00 | Commit local `GP-AGIPI-01` | 9 já commitados | Documentação institucional AGIPI inicial | Tecnicamente possível |
| PUB-01 | Fundação documental ICFACTORY | 20 | Documentação institucional | Possível após validação de perímetro |
| PUB-02 | Núcleo documental H&A | 8 | Documentação institucional de caso | Possível, preservando M1 provisório |
| PUB-03 | Governança, arquitetura e encerramento científico | 4 | Documentação de governança | Possível após reconciliação das referências |
| PUB-04 | Pesquisa experimental GP-ARQ-01 | 1 | Pesquisa experimental | Possível somente como pesquisa segregada |
| PUB-05 | Patch AGIPI — Fase I | 69 | Governança e documentação institucional | Possível como pacote documental próprio |
| PUB-06 | SUB-001 vigente — AGIPI/UEPG | 19 | Governança de submissão | Possível após PUB-05 |
| PUB-07 | Artefatos históricos fora do perímetro vigente da SUB-001 | 4 | Identificação institucional superada | Não publicar no fluxo vigente |
| PUB-08 | Governança da reconciliação Git | 2 | Relatórios GP-GIT-02 e GP-GIT-03 | Possível como lote de auditoria |
| PUB-09 | Alterações funcionais do PROTEUS | 8 | Código, teste, dados e relatório operacional | Depende de validação funcional própria |
| PUB-10 | Produção audiovisual PROTEUS | 143 | Mídia, projetos, scripts e derivados | Depende de reorganização prévia |
| PUB-11 | Dependências e binários audiovisuais | 47 | Biblioteca empacotada, DLL, `pyd` e wheel | Não publicar junto aos demais conjuntos |

### Reconciliação quantitativa

| Medida | Quantidade |
| --- | ---: |
| Arquivos pendentes antes da GP-GIT-03 | 324 |
| Arquivo criado por esta GP | 1 |
| Arquivos pendentes classificados após o plano | 325 |
| Arquivos já contidos no commit local PUB-00 | 9 |
| Conjuntos identificados | 12 |

Os 9 arquivos de PUB-00 já pertencem ao histórico local e não são somados aos 325 arquivos da worktree.

## 4. Descrição dos conjuntos

## PUB-00 — Commit local GP-AGIPI-01

### Finalidade

Publicar o primeiro estado commitado do Patch AGIPI.

### Conteúdo

Nove documentos institucionais, conforme inventário da GP-GIT-02.

### Dependências

- é pai necessário de qualquer novo commit criado sobre o HEAD atual;
- cinco documentos contidos no commit possuem revisões posteriores em PUB-05.

### Estado

**PUBLICÁVEL IMEDIATAMENTE SOB O CRITÉRIO ESTRITAMENTE TÉCNICO.**

Sua publicação isolada não representa o estado final da Fase I.

## PUB-01 — Fundação documental ICFACTORY

### Finalidade

Versionar a base institucional geral e o diretório ICFACTORY Core.

### Conteúdo — 20 arquivos

- 11 arquivos em `ICFACTORY_CORE_v1/`;
- 9 documentos institucionais gerais:
  - `BUSINESS_POSITIONING.md`;
  - `GP_PD_01_DOCUMENT_GOVERNANCE_IMPLEMENTATION.md`;
  - `GP_PD_02_INSTITUTIONAL_RECONCILIATION_REPORT.md`;
  - `GP_PD_03_DOCUMENT_ARCHITECTURE_REPORT.md`;
  - `GP_PD_04_EVIDENCE_VALIDATION_REPORT.md`;
  - `ICFACTORY_CONSTITUTION.md`;
  - `INSTITUTIONAL_PRINCIPLES.md`;
  - `MISSION_VISION_VALUES.md`;
  - `RESEARCH_LINES.md`.

### Dependências

É referenciado por PUB-03, PUB-05 e PUB-06.

### Estado

**DEPENDE DE REORGANIZAÇÃO PRÉVIA**, pois reúne duas famílias documentais fisicamente distintas.

## PUB-02 — Núcleo documental H&A

### Finalidade

Versionar os oito documentos institucionais do caso H&A.

### Conteúdo

`docs/institutional/HA/`, 8 arquivos.

### Dependências

- é consumido por inventários e dossiês de PUB-05;
- deve preservar a classificação M1 provisória.

### Estado

**PUBLICÁVEL ISOLADAMENTE APÓS DELIMITAÇÃO DO MANIFESTO.**

## PUB-03 — Governança, arquitetura e encerramento científico

### Finalidade

Versionar os documentos gerais modificados de governança e o encerramento científico já registrado.

### Conteúdo — 4 arquivos

- `docs/architecture/ARCHITECTURAL_PRINCIPLES.md`;
- `docs/history/HISTORY.md`;
- `docs/roadmap/ROADMAP.md`;
- `docs/research/OEG_GIT_07_PHASE_I_INSTITUTIONAL_CLOSURE_REPORT.md`.

### Dependências

- princípios, histórico e roadmap são referenciados por PUB-05;
- o relatório científico não promove pesquisa experimental.

### Estado

**DEPENDE DE REORGANIZAÇÃO PRÉVIA**, devido à combinação de três documentos transversais modificados e um relatório novo.

## PUB-04 — Pesquisa experimental GP-ARQ-01

### Finalidade

Versionar a Pesquisa Arquitetural do Gate de Autoridade.

### Conteúdo — 1 arquivo

- `docs/research/GP_ARQ_01_AUTHORITY_GATE_ARCHITECTURAL_RESEARCH.md`.

### Dependências

Não depende funcionalmente dos demais lotes. Sua classificação experimental depende de preservação explícita.

### Estado

**PUBLICÁVEL SOMENTE COMO PESQUISA EXPERIMENTAL SEGREGADA.**

Não deve integrar PUB-05 como patrimônio institucional consolidado.

## PUB-05 — Patch AGIPI — Fase I

### Finalidade

Versionar o encerramento institucional e documental do Patch AGIPI.

### Conteúdo — 69 arquivos

- 5 documentos AGIPI modificados;
- 64 documentos AGIPI não rastreados, excluídos os 23 da SUB-001.

Inclui:

- auditoria, certificação e remediação;
- baseline e matrizes de elegibilidade;
- decisões e registros de incorporação;
- autoria, titularidade, licenciamento e proponente;
- inventários e rastreabilidade;
- avaliação de encerramento do Patch.

### Dependências

- sucede PUB-00;
- referencia documentos de PUB-01;
- referencia arquitetura, HISTORY e roadmap de PUB-03;
- consome evidências H&A de PUB-02;
- deve manter PUB-04 fora do patrimônio consolidado.

### Estado

**DEPENDE DE REORGANIZAÇÃO PRÉVIA.**

É um conjunto documental coerente, mas suas referências cruzadas impedem tratá-lo como totalmente independente das fundações.

## PUB-06 — SUB-001 vigente — AGIPI/UEPG

### Finalidade

Versionar a governança atual da submissão, sem certificação ou autorização.

### Conteúdo — 19 arquivos

- registros oficiais da SUB-001;
- GP-SUB-02R;
- GP-SUB-03;
- GP-SUB-03A;
- GP-SUB-04;
- evidência externa incorporada apenas por referência.

### Dependências

- requer PUB-05, especialmente baseline, proponente, autoria, titularidade e licenciamento;
- não inclui o PDF externo;
- preserva estado `EM PREPARAÇÃO`.

### Estado

**PUBLICÁVEL APÓS PUB-05.**

## PUB-07 — Artefatos fora do perímetro vigente

### Finalidade original

Registrar a identificação inicial produzida pela GP-SUB-02.

### Conteúdo — 4 arquivos

- `SUB_001_UNIT_PROCESS_EVIDENCE_INVENTORY.md`;
- `SUB_001_UNIT_PROCESS_GAP_MATRIX.md`;
- `SUB_001_UNIT_PROCESS_IDENTIFICATION_REPORT.md`;
- `SUB_001_UNIT_PROCESS_DOCUMENTARY_SUFFICIENCY_OPINION.md`.

### Dependências

Foram sucedidos no estado vigente pela GP-SUB-02R, que delimitou AGIPI/UEPG.

### Estado

**NÃO DEVEM SER PUBLICADOS NO FLUXO VIGENTE DA SUB-001.**

Sua inclusão junto a PUB-06 introduziria duas estruturas destinatárias incompatíveis no mesmo lote.

## PUB-08 — Governança da reconciliação Git

### Finalidade

Preservar a auditoria da worktree e este plano.

### Conteúdo — 2 arquivos

- `docs/governance/GIT_REPOSITORY_RECONCILIATION_REPORT.md`;
- `docs/governance/GIT_PUBLICATION_REORGANIZATION_PLAN.md`.

### Dependências

Referencia os estados e contagens dos demais conjuntos, sem alterar seus conteúdos.

### Estado

**PUBLICÁVEL COMO LOTE DE AUDITORIA**, mantendo as contagens históricas registradas.

## PUB-09 — Alterações funcionais do PROTEUS

### Finalidade

Versionar alterações operacionais relacionadas à administração e aos dados ambientais.

### Conteúdo — 8 arquivos

- `main.py`;
- `relatorios.py`;
- `administracao.py`;
- `tests/test_administracao.py`;
- `data/dados_ambientais_medicoes.csv`;
- `data/qualidade_agua_medicoes.csv`;
- `data/eventos_operacionais.json`;
- `reports/relatorio_operacional.txt`.

### Dependências

Código, teste, dados e relatório operacional formam uma cadeia funcional. A GP-GIT-02 não contém validação técnica desse conjunto.

### Estado

**DEPENDE DE VALIDAÇÃO E REORGANIZAÇÃO PRÓPRIAS.**

Não deve integrar commits documentais.

## PUB-10 — Produção audiovisual PROTEUS

### Finalidade

Versionar os ativos e o projeto do vídeo institucional.

### Conteúdo — 143 arquivos

- cenas e tomadas;
- capturas;
- narração e áudio;
- versões exportadas;
- projetos Kdenlive;
- manifestos;
- scripts de montagem;
- legendas;
- ativos externos;
- imagens de análise e revisão.

### Dependências

- scripts dependem dos ativos e ferramentas;
- projetos dependem de mídia bruta;
- versões finais derivam de cenas, áudio e projetos;
- ativos externos possuem documentação de origem própria.

### Estado

**DEPENDE DE REORGANIZAÇÃO PRÉVIA.**

Material bruto, derivados, projetos e entregáveis finais não constituem uma unidade única.

## PUB-11 — Dependências e binários audiovisuais

### Finalidade observada

Fornecer OpenCV local aos scripts da produção audiovisual.

### Conteúdo — 47 arquivos

- 46 arquivos em `media/proteus_institutional_video/tools/python_libs/`;
- 1 wheel em `media/proteus_institutional_video/tools/wheels/`.

Inclui DLL, `cv2.pyd`, metadados de distribuição, stubs e wheel binário.

### Dependências

É consumido pelos scripts de PUB-10, mas não constitui documentação nem mídia final.

### Estado

**NÃO DEVE SER PUBLICADO JUNTO AOS DEMAIS CONJUNTOS.**

Sua eventual publicação exige decisão própria sobre dependências vendorizadas e binários; essa decisão não existe nos documentos auditados.

## 5. Dependências entre conjuntos

```text
PUB-00 — commit local
   ↓
PUB-01 — fundação institucional
   ├── PUB-03 — governança transversal
   ├── PUB-02 — caso H&A
   └── PUB-05 — Patch AGIPI
          ↓
       PUB-06 — SUB-001 vigente

PUB-04 — pesquisa experimental segregada
PUB-08 — auditoria Git independente
PUB-09 — fluxo funcional independente
PUB-10 — produção audiovisual
   └── PUB-11 — dependências/binários separados

PUB-07 — fora do fluxo vigente
```

### Dependências encontradas

| Origem | Destino | Dependência |
| --- | --- | --- |
| PUB-05 | PUB-00 | Revisões posteriores aos documentos do commit local |
| PUB-05 | PUB-01 | Constituição, princípios e documentação institucional |
| PUB-05 | PUB-02 | Evidências e classificação do H&A |
| PUB-05 | PUB-03 | Princípios arquiteturais, HISTORY e roadmap |
| PUB-06 | PUB-05 | Baseline, decisões e registros institucionais |
| PUB-09 | interno | Código, teste, dados e relatório devem permanecer coerentes |
| PUB-10 | interno | Mídia bruta, projetos, scripts e derivados |
| PUB-10 | PUB-11 | Scripts podem consumir a biblioteca empacotada |

## 6. Classificação de prontidão

### Publicáveis imediatamente ou como unidade já delimitada

| Conjunto | Limite |
| --- | --- |
| PUB-00 | Tecnicamente publicável; não representa o estado final |
| PUB-08 | Lote documental de auditoria, sem efeito sobre os demais conjuntos |

### Dependem de reorganização ou validação prévia

- PUB-01;
- PUB-02;
- PUB-03;
- PUB-04, para assegurar segregação experimental;
- PUB-05;
- PUB-06;
- PUB-09;
- PUB-10.

### Não devem ser publicados no fluxo atual

- PUB-07, por estar fora do perímetro institucional vigente da SUB-001;
- PUB-11, por conter dependências vendorizadas e binários sem decisão de publicação.

## 7. Ordem sugerida de publicação

| Ordem | Conjunto | Justificativa documental |
| ---: | --- | --- |
| 1 | PUB-00 | É o único commit local existente e pai dos futuros commits |
| 2 | PUB-01 | Estabelece a fundação documental referenciada pelos lotes seguintes |
| 3 | PUB-03 | Consolida princípios, histórico e roadmap consumidos pelo Patch |
| 4 | PUB-02 | Disponibiliza o núcleo H&A referenciado nos inventários AGIPI |
| 5 | PUB-05 | Consolida a Fase I após suas autoridades e fontes documentais |
| 6 | PUB-06 | Registra a submissão como processo posterior e dependente da Fase I |
| 7 | PUB-08 | Preserva a auditoria e o plano após os lotes documentais principais |
| 8 | PUB-04 | Pode ser publicado separadamente, mantendo classificação experimental |
| 9 | PUB-09 | Fluxo funcional separado, condicionado a validação própria |
| 10 | PUB-10 | Fluxo audiovisual separado após decomposição entre fontes e derivados |

PUB-07 e PUB-11 não integram a sequência proposta.

## 8. Riscos objetivos de publicação fora da sequência

| Risco | Ocorrência |
| --- | --- |
| Referências quebradas ou autoridades ausentes | Publicar PUB-05 antes de PUB-01 e PUB-03 |
| Dossiê AGIPI sem evidência H&A correspondente | Publicar PUB-05 antes de PUB-02 |
| SUB-001 sem baseline, proponente ou política institucional | Publicar PUB-06 antes de PUB-05 |
| Promoção implícita de pesquisa experimental | Misturar PUB-04 com PUB-05 |
| Destinatários institucionais incompatíveis no mesmo lote | Misturar PUB-07 com PUB-06 |
| Código sem teste ou dados coerentes | Fragmentar PUB-09 sem validação |
| Repositório inflado por brutos, derivados e múltiplas exportações | Publicar PUB-10 como unidade indivisa |
| Inclusão de binários e dependências vendorizadas sem autoridade | Misturar PUB-11 com PUB-10 ou documentação |
| Publicação de estado institucional intermediário | Publicar apenas PUB-00 e apresentá-lo como encerramento final |

## 9. Limites

Este plano:

- não cria autorização de publicação;
- não seleciona arquivos para staging;
- não valida conteúdo funcional;
- não decide política de mídia ou binários;
- não modifica a classificação da GP-ARQ-01;
- não modifica o estado da SUB-001;
- não executa a sequência proposta.

## 10. Validações

- Conjuntos identificados: 12.
- Arquivos pendentes classificados: 325.
- Dependências entre conjuntos registradas: 8 relações principais.
- Nenhum arquivo preexistente modificado.
- Somente `GIT_PUBLICATION_REORGANIZATION_PLAN.md` criado.
- Nenhuma operação Git de escrita executada.
- Nenhum staging preparado.
- Nenhum commit ou push realizado.

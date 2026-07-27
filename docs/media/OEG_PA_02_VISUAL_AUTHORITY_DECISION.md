# OEG-PA-02 — Definição da Autoridade Visual do Vídeo Institucional

Data: 18/07/2026
Natureza: decisória e não destrutiva
Parecer: **CANDIDATO A DESIGNADO COMO AUTORIDADE VISUAL OFICIAL**

## 1. Objetivo

Definir uma única autoridade visual para a continuidade da pós-produção do vídeo institucional do PROTEUS, com base na integridade, editabilidade, rastreabilidade, reprodutibilidade e governança dos dois artefatos identificados pela OEG-PA-01.

Esta decisão não constitui picture lock, não aprova publicação externa e não autoriza edição, renderização, exportação, sincronização, áudio, legendagem, créditos ou qualquer alteração de ativo audiovisual.

## 2. Contexto

A OEG-PA-01 estabeleceu que o pacote audiovisual contém dois artefatos visualmente relacionados, mas com papéis técnicos diferentes:

- um projeto Kdenlive editável de 108 segundos, com 12 cenas SC001–SC012, que preserva a timeline do Assembly Cut V1;
- um MP4 silencioso de 111,966667 segundos, produzido fora da timeline por uma cadeia não destrutiva que acrescenta fades, legendas abertas e cartela final.

A coexistência desses artefatos sem uma hierarquia formal criava risco de origem dupla. A presente OEG elimina essa ambiguidade ao separar **autoridade de edição** de **evidência de acabamento derivado**.

## 3. Artefatos avaliados

### 3.1 Candidato A — Assembly Cut V1

| Propriedade | Evidência |
|---|---|
| Artefato | `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive` |
| Tipo | projeto Kdenlive/MLT editável |
| SHA-256 | `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B` |
| Duração | 108,000 s / 3.240 frames a 30 fps |
| Estrutura | 12 cenas SC001–SC012 em ordem, sem lacunas ou sobreposições |
| Fontes | 12/12 localizadas e íntegras no baseline OEG-PA-01 |
| Estado | Assembly Cut íntegro e congelado; sem picture lock |

### 3.2 Candidato B — Derivado Visual V1

| Propriedade | Evidência |
|---|---|
| Artefato | `media/proteus_institutional_video/exports/post_production_v1/PROTEUS_INSTITUTIONAL_VIDEO_V1_POST_PRODUCED.mp4` |
| Tipo | MP4 H.264 achatado, silencioso |
| SHA-256 | `681734FF429E66F49B4D5FE3C30EEF16BB74FB7CF4A316E4151023EDDE88790B` |
| Duração | 111,966667 s / 3.359 frames a 30 fps |
| Acabamento | fades de abertura e fechamento, 12 legendas abertas e cartela final |
| Origem | derivação externa do Candidato A pelo script `build_post_production_v1.cmd` |
| Estado | saída visual V1 válida com ressalvas; não é projeto editável nem master |

O MP4-base intermediário da derivação possui SHA-256 `B493145F7EAB7641D85D2DB8718CB60A0007B9D4B668CE5D7A334C39A856B432` e duração de 108 segundos. O script aplica sobre ele o SRT, o lockup oficial, os fades e a cartela final. Esses componentes não estão incorporados à timeline do Candidato A.

## 4. Critérios utilizados

Foram aplicados os seguintes critérios:

1. **Integridade:** consistência estrutural, identidade verificável e preservação da relação com as fontes.
2. **Rastreabilidade:** capacidade de reconstruir a sequência de decisões e distinguir origem, transformação e saída.
3. **Reprodutibilidade:** possibilidade de obter novamente a saída a partir de insumos identificados.
4. **Editabilidade:** capacidade de sustentar alterações futuras sem perda estrutural ou recodificação geracional.
5. **Governança:** adequação como baseline único, controle de versões e continuidade da cadeia de auditoria.
6. **Risco:** impacto da adoção de cada candidato como autoridade, e não apenas como artefato válido.

A avaliação foi documental e por operações de leitura. Foram confrontados a OEG-PA-01, os relatórios PI-07/PI-07A, os hashes atuais, a estrutura já auditada da timeline e o conteúdo do pipeline de derivação. Nenhum pipeline foi executado e nenhum ativo audiovisual foi aberto para edição, salvo ou modificado.

## 5. Comparação técnica

| Critério | Candidato A — projeto editável | Candidato B — MP4 derivado |
|---|---|---|
| Integridade estrutural | Alta: preserva timeline, cortes, ordem, fontes e parâmetros do projeto | Alta como arquivo de exibição; baixa como estrutura editorial, pois timeline, camadas e vínculos foram achatados |
| Rastreabilidade | Alta: representa diretamente a montagem de SC001–SC012 | Média-alta como saída documentada, mas depende da cadeia externa para explicar suas intervenções |
| Reprodutibilidade | Alta no ambiente auditado; limitada por caminhos absolutos | Média-alta no ambiente auditado, desde que projeto, render-base ou renderizador, SRT, logo, script e versões das ferramentas permaneçam disponíveis |
| Editabilidade | Alta: é a origem própria para evolução da timeline | Baixa: alterações exigem nova derivação ou edição destrutiva/recodificação do arquivo achatado |
| Preservação temporal | Exata para a montagem de 108 s | Registra uma extensão de aproximadamente 4 s e tratamentos que não existem na timeline |
| Adequação à pós-produção | Alta como fonte de novas versões governadas | Adequada como referência visual e saída de conferência, não como origem editorial |

O Candidato B é tecnicamente válido e contém decisões visuais relevantes. Contudo, sua validade como produto não o converte em autoridade de edição. A sua reprodutibilidade decorre justamente da existência do Candidato A e dos demais insumos identificados.

## 6. Comparação de governança

### 6.1 Candidato A

O Candidato A preserva a cadeia natural de autoridade:

`fontes SC001–SC012 → projeto/timeline → render-base → tratamento externo → derivados`

Ele permite:

- congelar uma identidade binária inequívoca pelo SHA-256;
- auditar cortes e ordem diretamente na timeline;
- produzir novas versões sem tomar um export achatado como fonte;
- separar baseline, transformação e produto;
- manter o versionamento futuro explícito, sem sobrescrever o Assembly Cut V1.

### 6.2 Candidato B

O Candidato B preserva evidência útil de uma aplicação específica de acabamento, mas não contém a arquitetura editorial que o produziu. Promovê-lo a autoridade inverteria a cadeia origem–derivado e criaria dois problemas:

- decisões futuras seriam feitas sobre um arquivo achatado ou exigiriam retorno informal ao projeto que deixou de ser autoridade;
- fades, legendas e cartela poderiam ser confundidos com elementos nativos da timeline, embora sejam aplicados pelo pipeline externo.

Sua função de governança correta é provar e orientar a conformidade visual do acabamento V1, não comandar a evolução editorial.

## 7. Avaliação de riscos

| Candidato adotado como autoridade | Risco | Probabilidade | Impacto | Tratamento |
|---|---|---:|---:|---|
| A | caminhos absolutos podem deixar fontes offline em outra raiz | média | alto | manter o ambiente auditado ou realizar relink apenas sob nova OEG, sem sobrescrever o baseline |
| A | fades, legendas e cartela do derivado podem regredir em nova saída | média | médio | usar B somente como referência auxiliar de conformidade e auditar cada nova derivação |
| A | a designação ser interpretada como picture lock | média | alto | registrar expressamente que a autoridade não equivale a picture lock ou aprovação final |
| B | inversão entre fonte e derivado | alta | alto | não designar B como autoridade |
| B | perda de editabilidade e de relações de timeline | alta | alto | manter B como saída achatada de referência |
| B | legendas abertas impedirem desligamento, revisão ou localização sem nova renderização | alta | médio | tratar SRT e pipeline como componentes separados em versões futuras |
| B | recodificação geracional e retrabalho em alterações visuais | alta | médio | derivar sempre do projeto-fonte, nunca do MP4 como origem |
| B | divergência silenciosa entre MP4 e projeto em evoluções futuras | alta | alto | exigir versão e relatório para todo novo derivado |

O risco residual do Candidato A é controlável por versionamento, hashes e conferência contra a referência auxiliar. Os riscos do Candidato B decorrem da sua própria natureza de export achatado e não podem ser eliminados sem retornar ao Candidato A.

## 8. Fundamentação da decisão

A autoridade visual deve ser o artefato que preserva a estrutura capaz de originar, explicar e manter os produtos futuros. O Candidato A satisfaz esse requisito porque contém a timeline oficial, mantém a relação verificável com as 12 fontes e pode gerar novas derivações sem perda estrutural.

O Candidato B contém acabamento mais avançado, porém esse acabamento é uma transformação documentada do Candidato A. A duração adicional, os fades, as legendas abertas e a cartela final são decisões válidas da saída V1, mas residem no pipeline externo e no MP4 resultante, não no projeto editável. Assim, maior acabamento aparente não equivale a maior autoridade arquitetural.

A decisão também preserva a continuidade documental: OEG-PA-01 reconheceu o `.kdenlive` como baseline imutável e o MP4 como derivado visual candidato. A OEG-PA-02 converte essa recomendação em hierarquia formal sem reclassificar o Assembly como rough cut, fine cut ou picture lock.

## 9. Decisão e regras de autoridade

### 9.1 Autoridade única

Fica designado como **AUTORIDADE VISUAL OFICIAL DO VÍDEO INSTITUCIONAL DO PROTEUS**:

`media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive`

Identidade da baseline: `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`.

### 9.2 Classificação do Candidato B

O arquivo `PROTEUS_INSTITUTIONAL_VIDEO_V1_POST_PRODUCED.mp4` fica classificado como:

**DERIVADO VISUAL V1 HOMOLOGADO COMO REFERÊNCIA AUXILIAR DE CONFORMIDADE.**

Ele:

- não é autoridade visual;
- não é fonte de edição;
- não é master;
- não representa picture lock;
- não pode substituir silenciosamente o projeto Kdenlive;
- pode ser consultado para verificar o tratamento de fades, a presença e o posicionamento das legendas abertas e a cartela final da derivação V1.

### 9.3 Regras para trabalhos futuros

1. Toda OEG posterior deve citar o Candidato A e seu hash como autoridade de origem.
2. O Candidato A permanece congelado e não deve ser sobrescrito; evolução editorial requer novo projeto/versionamento derivado e autoridade formal própria.
3. O Candidato B pode ser citado apenas como evidência ou referência auxiliar, nunca como origem editorial.
4. Qualquer novo render deve declarar projeto-fonte, hash, insumos, pipeline, duração e relação com o derivado anterior.
5. Divergência entre uma nova saída e a autoridade deve ser deliberada e registrada, não absorvida implicitamente.
6. A passagem a rough cut, fine cut, picture lock, pós-produção de áudio ou masterização exige autorização posterior específica.
7. A alteração desta autoridade exige nova decisão formal; não pode ocorrer por simples criação ou renomeação de export.

## 10. Ressalvas

- A autoridade é reproduzível no ambiente auditado, mas os caminhos absolutos do projeto reduzem portabilidade.
- A revisão visual anterior do derivado foi amostral; não existe certificação de playback humano integral em tela cheia nesta OEG.
- A designação não resolve a decisão pendente sobre SC009, legibilidade das cenas densas, política final de legendas, narração, música, efeitos, créditos ou licenças.
- O MP4 legado de 437,967 segundos permanece fora desta autoridade e não deve ser tratado como master ou concorrente dos candidatos avaliados.
- Nenhuma conclusão deste documento autoriza alteração do projeto ou dos ativos.

## 11. Parecer final

**AUTORIDADE VISUAL DEFINIDA — CANDIDATO A APROVADO.**

A autoridade visual oficial é o projeto editável `PROTEUS_ASSEMBLY_CUT_V1.kdenlive`, com 108 segundos, 12 cenas e SHA-256 `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`.

A escolha se fundamenta em três dimensões convergentes:

- **técnica:** o projeto preserva timeline, fontes, cortes e editabilidade;
- **documental:** seu hash e sua integridade possuem continuidade verificável entre PI-07, OEG-PA-01 e esta decisão;
- **arquitetural:** ele ocupa a posição correta de origem na cadeia de derivação, enquanto o MP4 registra uma saída transformada.

O derivado silencioso de 111,966667 segundos permanece preservado como **referência auxiliar de conformidade visual V1**, sem autoridade editorial. Todos os trabalhos futuros deverão partir exclusivamente do Candidato A como autoridade e poderão usar o Candidato B apenas para conferência dos tratamentos já demonstrados.

**PARECER: AUTORIDADE_VISUAL_CANDIDATO_A — DECISÃO APROVADA COM RESSALVAS, SEM PICTURE LOCK E SEM AUTORIZAÇÃO DE EDIÇÃO.**

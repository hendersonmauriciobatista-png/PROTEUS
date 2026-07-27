# OEG-PA-06 — Avaliação Comparativa das Candidatas SC009

Data: 18/07/2026
Natureza: avaliação comparativa, sem edição ou promoção
Autoridade preservada: `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive`
SHA-256 da autoridade: `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`
Parecer: **TAKE 01 SELECIONADA COMO MELHOR CANDIDATA À FUTURA SUBSTITUIÇÃO**

## 1. Objetivo

Comparar a SC009 original com as três candidatas produzidas na OEG-PA-05 e selecionar, de forma técnica e auditável, a tomada que elimina mais completamente as não conformidades editoriais identificadas na OEG-PA-03.

Esta decisão limita-se à seleção. Ela não substitui arquivo, não edita a timeline, não promove a candidata para `approved/` e não altera a autoridade visual.

## 2. Artefatos avaliados

| ID | Arquivo | Duração bruta | Frames | SHA-256 |
|---|---|---:|---:|---|
| ORIGINAL | `media/proteus_institutional_video/SC009.mp4` | 8,766667 s | 263 | `342BECB6183492320FD4A087E55F4CAA3C0FC8120FDA36CBE43E7DDCF28E1B94` |
| TAKE 01 | `media/proteus_institutional_video/official_scenes/raw/SC009_TAKE_01.mp4` | 10,766667 s | 323 | `EFC9159AC0F9A1ECE9F386A1297D03491C4E56EA2AFED286D4F23A65E0C0CFE0` |
| TAKE 02 | `media/proteus_institutional_video/official_scenes/raw/SC009_TAKE_02.mp4` | 10,800000 s | 324 | `BAD9F9DCFEFF2221FDD980F8C8AB03105812B0A07B31C08A563C3B4855C43391` |
| TAKE 03 | `media/proteus_institutional_video/official_scenes/raw/SC009_TAKE_03.mp4` | 10,800000 s | 324 | `3C5211CEF9387BAEE9A67C20219CCF3357A6F182305FEDF20A4669A8779A0A96` |

Todos os arquivos foram avaliados sem modificação.

## 3. Metodologia

### 3.1 Janela comparativa

Para evitar que a diferença entre a duração da fonte original e os handles das candidatas distorcesse o resultado, foram usados:

- os 249 frames efetivamente empregados pela SC009 original na timeline;
- uma janela comum de 249 frames em cada candidata, complementada pela inspeção dos respectivos handles brutos.

A janela de 249 frames representa os 8,3 segundos autorizados para uma futura substituição sem alteração estrutural da timeline.

### 3.2 Verificações executadas

- inspeção visual dos frames inicial, intermediários e final;
- folhas de contato em intervalos de um segundo;
- conferência de resolução, codec, pixel format, frame rate, duração, frames e streams;
- decodificação integral;
- comparação com os frames de saída de SC008 e entrada de SC010;
- detecção de quadros pretos;
- contagem de frames consecutivos idênticos;
- análise de diferença entre frames, excluindo a região do relógio da aplicação;
- rastreamento do percurso do cursor entre tendências, alertas e score;
- confronto com o plano OEG-PA-04 e o relatório de execução OEG-PA-05.

### 3.3 Métricas temporais

| Artefato | Frames avaliados | Pares com movimento detectável | Pares estáticos ou quase estáticos | Duplicatas consecutivas no bruto |
|---|---:|---:|---:|---:|
| ORIGINAL | 249 | 0 | 248 | 8 em 263 frames |
| TAKE 01 | 249 | 137 | 111 | 63 em 323 frames |
| TAKE 02 | 249 | 118 | 130 | 69 em 324 frames |
| TAKE 03 | 249 | 121 | 127 | 67 em 324 frames |

Na original, a baixa quantidade de hashes duplicados no bruto não representa movimento editorial: diferenças de captura/relógio alteram pixels periféricos, enquanto a área útil permaneceu imóvel nos 249 frames analisados. Nas candidatas, o movimento detectável corresponde ao cursor atravessando as três zonas narrativas.

As métricas não substituem julgamento editorial, mas diferenciam objetivamente a regularidade das tomadas produzidas pelo mesmo roteiro.

## 4. Critérios utilizados

### 4.1 Continuidade

- compatibilidade visual com o encerramento de SC008 — Relatórios;
- compatibilidade visual com a abertura de SC010 — Governança Operacional;
- progressão semântica Relatórios → Analytics → Governança;
- existência de frames estáveis aptos a cortes secos.

### 4.2 Estabilidade

- ausência de tremor ou salto do enquadramento;
- suavidade e continuidade do cursor;
- ausência de mudança inesperada de tela, dados ou foco;
- regularidade de frames.

### 4.3 Ritmo

- percurso completo em janela compatível com 8,3 segundos;
- tempo de reconhecimento de cada zona visual;
- existência de respiro inicial e final nos handles;
- ausência de pressa, espera excessiva ou movimento redundante.

### 4.4 Hierarquia visual

- score como resultado agregado dominante;
- explicações imediatamente associadas ao score;
- tendências como evidência analítica intermediária;
- alertas como consequência preventiva;
- ocupação equilibrada do quadro.

### 4.5 Legibilidade

- título e mensagem determinística reconhecíveis;
- score, status, cabeçalhos e alertas legíveis em 1920×1080;
- ausência de terminal, logs, desktop, notificações ou distrações;
- dados demonstrativos sem informação sensível.

### 4.6 Fidelidade ao plano

- H.264, 1920×1080, 30 fps constante e yuv420p;
- pelo menos 249 frames utilizáveis;
- percurso tendências → alertas → Water Health Score;
- ausência de clique, digitação, rolagem ou alteração de dados;
- conteúdo obrigatório simultaneamente visível.

## 5. Avaliação da SC009 original

### 5.1 Continuidade

A posição narrativa entre Relatórios e Governança é correta, mas a imagem não estabelece uma camada analítica visualmente distinta. Ela repete o caráter textual de SC008 e transfere para SC010 a responsabilidade de recuperar hierarquia e cor.

### 5.2 Estabilidade e ritmo

A captura é estável, mas integralmente estática na área útil. Em 249 frames, nenhum par apresentou movimento editorial detectável. A estabilidade converte-se em imobilidade, sem orientação do olhar.

### 5.3 Hierarquia e legibilidade

O conteúdo técnico ocupa pequena região do quadro, com grande área vazia. Water Health Score, tendências, explicações e alertas não aparecem como quatro componentes reconhecíveis. Texto pequeno e saída semelhante a console impedem leitura institucional imediata.

### 5.4 Classificação

**REPROVADA.**

A original não elimina nenhuma das causas centrais registradas na OEG-PA-03 e permanece inadequada ao Picture Lock.

## 6. Avaliação individual das candidatas

### 6.1 TAKE 01

#### Continuidade

Mantém o tema escuro, a sidebar e a geometria das telas adjacentes. A passagem de Relatórios para uma tela analítica estruturada é inequívoca; a saída para Governança preserva a progressão sinais → eventos.

#### Estabilidade

O enquadramento permanece absolutamente estável. O cursor percorre as zonas sem clique, tremor ou mudança de foco. Na janela comum, TAKE 01 apresentou 137 pares com movimento detectável — o maior valor entre as candidatas — e a menor incidência de frames consecutivos idênticos no arquivo bruto.

#### Ritmo

O cursor alcança tendências, alertas e score com permanência suficiente para reconhecimento. Há handles antes e depois do percurso. A tomada possui 323 frames brutos, um frame a menos que TAKE 02 e TAKE 03, mas ainda oferece 74 frames além dos 249 necessários.

#### Hierarquia visual e legibilidade

Score `100/100` e status ocupam a zona dominante superior. Quatro explicações permanecem associadas ao card. Tendências preenchem a área central e dois alertas ocupam a área inferior. Não há grande vazio sem função, terminal, notificação ou janela externa.

#### Fidelidade ao plano

Conforme quanto a resolução, codec, fps, duração útil, conteúdo, percurso e ausência de interação. Permanece a ressalva procedimental comum da OEG-PA-05: captura FFmpeg no lugar do perfil OBS inexistente e bitrate efetivo inferior ao target configurado.

#### Classificação

**APROVADA — MELHOR CANDIDATA.**

### 6.2 TAKE 02

#### Continuidade

Equivalente à TAKE 01 em conteúdo, tema e integração semântica com SC008/SC010.

#### Estabilidade

Não apresenta tremor ou interação indevida. Entretanto, registrou 69 frames consecutivos idênticos no bruto e 118 pares com movimento detectável na janela comum, o menor índice de continuidade de movimento das três candidatas.

#### Ritmo

A duração bruta é exata em 10,8 segundos/324 frames e os três focos são atingidos. A cadência do cursor é discretamente mais segmentada que na TAKE 01, embora permaneça utilizável.

#### Hierarquia visual e legibilidade

Idênticas às da TAKE 01. Todo o conteúdo obrigatório permanece visível e legível.

#### Fidelidade ao plano

Conforme nos requisitos editoriais e técnicos principais, com as ressalvas comuns de ferramenta e bitrate.

#### Classificação

**APROVADA COM RESSALVAS.**

Não é selecionada porque não oferece vantagem visual sobre TAKE 01 e possui movimento comparativamente menos contínuo.

### 6.3 TAKE 03

#### Continuidade

Equivalente às demais candidatas e adequada ao encadeamento SC008 → SC009 → SC010.

#### Estabilidade

Enquadramento estável e ausência de interação indevida. Apresentou 121 pares com movimento detectável e 67 duplicatas consecutivas no bruto, resultado intermediário entre TAKE 01 e TAKE 02.

#### Ritmo

Possui 324 frames e percurso completo. O cursor chega às mesmas zonas, mas a regularidade medida permanece ligeiramente inferior à TAKE 01.

#### Hierarquia visual e legibilidade

Idênticas às demais candidatas; score, explicações, tendências e alertas são simultaneamente visíveis.

#### Fidelidade ao plano

Conforme nos requisitos principais, com as ressalvas comuns de ferramenta e bitrate.

#### Classificação

**APROVADA COM RESSALVAS.**

Não é selecionada porque não demonstra ganho editorial sobre TAKE 01.

## 7. Comparações diretas com a original

| Comparação | Vantagem da candidata | Limitação remanescente | Resultado |
|---|---|---|---|
| ORIGINAL × TAKE 01 | substitui texto isolado por score dominante, explicações, nove linhas de tendência e dois alertas; adiciona o percurso mais contínuo | um frame bruto a menos que as demais; ressalvas de ferramenta/bitrate | TAKE 01 vence integralmente |
| ORIGINAL × TAKE 02 | elimina vazio, baixa hierarquia e imobilidade; apresenta todos os elementos obrigatórios | maior incidência comparativa de frames repetidos durante o percurso | TAKE 02 vence a original |
| ORIGINAL × TAKE 03 | demonstra Analytics como camada própria e adiciona movimento guiado | continuidade de cursor ligeiramente inferior à TAKE 01 | TAKE 03 vence a original |

Todas as candidatas corrigem a causa-raiz da reprovação original. A diferença entre elas não está no conteúdo ou enquadramento — que são equivalentes —, mas na regularidade temporal do cursor.

## 8. Comparação TAKE 01 × TAKE 02 × TAKE 03

| Critério | TAKE 01 | TAKE 02 | TAKE 03 |
|---|---|---|---|
| Resolução / codec / fps | conforme | conforme | conforme |
| Frames brutos | 323 | 324 | 324 |
| Janela útil de 249 frames | disponível | disponível | disponível |
| Conteúdo obrigatório | completo | completo | completo |
| Enquadramento | integral | integral | integral |
| Integração SC008/SC010 | alta | alta | alta |
| Pares com movimento detectável | **137** | 118 | 121 |
| Duplicatas consecutivas no bruto | **63** | 69 | 67 |
| Suavidade relativa | **melhor** | terceira | segunda |
| Legibilidade | equivalente | equivalente | equivalente |
| Ressalva temporal | 323 frames, -1 frente às demais | nenhuma | nenhuma |
| Classificação | **APROVADA** | APROVADA COM RESSALVAS | APROVADA COM RESSALVAS |
| Seleção | **VENCEDORA** | não selecionada | não selecionada |

O frame bruto adicional das TAKEs 02 e 03 não compensa a menor continuidade de movimento. Todas possuem folga muito superior aos 249 frames necessários, portanto o critério editorial de suavidade prevalece.

## 9. Justificativa técnica da seleção

TAKE 01 elimina integralmente as não conformidades da original porque:

1. ocupa o quadro com estrutura funcional real, sem composição externa;
2. torna Water Health Score o elemento dominante;
3. mantém explicações, tendências e alertas simultaneamente presentes;
4. substitui imobilidade total por percurso natural e orientador;
5. preserva linguagem visual, sidebar e tema das cenas adjacentes;
6. não contém clique, rolagem, digitação ou mudança de dados;
7. oferece mais de 8,3 segundos utilizáveis e handles;
8. apresenta a melhor continuidade de movimento entre as três candidatas.

A duração um frame menor não cria risco estrutural: a tomada dispõe de 323 frames, enquanto a futura substituição exige somente 249. Esse frame não deve ser compensado por retiming; a futura etapa deverá apenas selecionar o in/out apropriado dentro do arquivo íntegro.

## 10. Ressalvas

- A seleção não elimina a necessidade de playback humano integral antes da promoção.
- As três candidatas compartilham as ressalvas de captura FFmpeg e bitrate registradas na OEG-PA-05.
- A interface permanece estruturalmente estática; o movimento provém do cursor. Essa escolha é adequada ao plano aprovado, mas não equivale a animação da UI.
- A futura substituição deverá definir exatamente uma janela de 249 frames e validar os cortes com SC008 e SC010.
- TAKE 02 e TAKE 03 permanecem preservadas como alternativas/rejeitadas pela seleção, sem exclusão ou renomeação nesta OEG.
- Nenhuma candidata foi movida para `approved/`.

## 11. Recomendação final

Recomenda-se submeter exclusivamente:

`media/proteus_institutional_video/official_scenes/raw/SC009_TAKE_01.mp4`

SHA-256:

`EFC9159AC0F9A1ECE9F386A1297D03491C4E56EA2AFED286D4F23A65E0C0CFE0`

à futura OEG de autorização de promoção/substituição.

A etapa futura deverá:

1. executar playback humano em tela cheia;
2. definir in/out de 249 frames sem retiming;
3. validar os cortes SC008→TAKE 01 e TAKE 01→SC010;
4. criar uma nova versão derivada do projeto, sem sobrescrever o Assembly Cut V1;
5. reconferir hashes da autoridade, da original e da candidata;
6. retornar à revisão de Picture Lock após a substituição autorizada.

## 12. Parecer conclusivo

**SC009_TAKE_01 É A MELHOR CANDIDATA PARA FUTURA SUBSTITUIÇÃO DA SC009.**

Classificação final:

- SC009 original: **REPROVADA**;
- SC009_TAKE_01: **APROVADA — MELHOR CANDIDATA**;
- SC009_TAKE_02: **APROVADA COM RESSALVAS — NÃO SELECIONADA**;
- SC009_TAKE_03: **APROVADA COM RESSALVAS — NÃO SELECIONADA**.

A TAKE 01 corrige a baixa hierarquia, a grande área vazia, a baixa legibilidade e a ausência de movimento da original, apresentando a melhor regularidade temporal entre as candidatas. Ela está apta a ser submetida a uma futura autorização de promoção, mas permanece sem autoridade e fora da timeline.

**PARECER: `SC009_TAKE_01_SELECIONADA — PROMOCAO_E_SUBSTITUICAO_NAO_AUTORIZADAS`.**

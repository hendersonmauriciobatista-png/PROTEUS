# OEG-PA-05 — Execução da Recaptura da SC009

Data: 18/07/2026
Natureza: execução controlada de captura
Autoridade preservada: `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive`
SHA-256 da autoridade: `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`
Parecer: **TRÊS TOMADAS CANDIDATAS PRODUZIDAS — AGUARDANDO AVALIAÇÃO FORMAL**

## 1. Objetivo

Produzir exatamente três tomadas independentes da tela funcional Previsão Analítica, em conformidade com o percurso editorial da OEG-PA-04, preservando o Assembly Cut V1, a SC009 vigente e todas as demais cenas.

Esta OEG não seleciona, aprova ou promove tomada; não substitui mídia na timeline e não cria nova versão do Assembly.

## 2. Pré-condições verificadas

Antes da gravação foram confirmados:

- projeto Kdenlive com SHA-256 `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`;
- SC009 vigente com SHA-256 `342BECB6183492320FD4A087E55F4CAA3C0FC8120FDA36CBE43E7DDCF28E1B94`;
- tela física de 1920×1080;
- ambiente virtual do PROTEUS com PyQt5 funcional;
- dados exclusivamente demonstrativos já existentes;
- Water Health Score `100/100 — Score analitico excelente`;
- cinco explicações disponíveis;
- cinco tendências de qualidade úteis e quatro tendências de consumo exibidas;
- dois alertas preventivos de severidade baixa;
- diretório `official_scenes/raw/` vazio para os nomes solicitados;
- ausência prévia de `SC009_TAKE_01.mp4`, `SC009_TAKE_02.mp4` e `SC009_TAKE_03.mp4`.

Nenhum dado foi criado, alterado ou excluído para preparar a captura.

## 3. Metodologia de captura

### 3.1 Sessão visual

A aplicação foi iniciada pelo ambiente `venv`, exibida em fullscreen 1920×1080 e navegada programaticamente até a página Previsão Analítica antes da gravação. O refresh executado na abertura foi exclusivamente de leitura.

O preflight visual confirmou, simultaneamente:

- título e subtítulo da página;
- card de Water Health Score com valor, status e explicações;
- tabela de tendências preenchida;
- tabela de alertas preenchida;
- barra lateral e identidade do PROTEUS;
- ausência de terminal, desktop, barra de tarefas, notificações ou outra janela na área capturada.

### 3.2 Gravação

As três tomadas foram capturadas na mesma sessão fullscreen, com o mesmo estado de dados e o mesmo enquadramento. A captura direta da sessão gráfica foi realizada pelo FFmpeg `gdigrab`, pois o OBS instalado não possuía o perfil `PROTEUS_FILM_OFFICIAL_SCENES` nem a coleção `PROTEUS_WINDOW_CAPTURE` configurados. Essa substituição de ferramenta é registrada como ressalva procedimental; os parâmetros audiovisuais explícitos da OEG-PA-05 foram preservados.

Parâmetros aplicados:

| Parâmetro | Configuração |
|---|---|
| Área capturada | tela fullscreen exclusiva do PROTEUS |
| Resolução | 1920×1080 |
| Proporção | 16:9 |
| Frame rate | 30 fps constante |
| Codec | H.264 / libx264 |
| Pixel format | yuv420p |
| Target de codificação | 16.000 Kbps; máximo 20.000 Kbps |
| GOP | 60 frames / 2 s |
| Áudio | desativado; nenhum stream de áudio produzido |
| Duração bruta solicitada | aproximadamente 10,8 s por tomada |

### 3.3 Percurso executado

Em cada tomada:

1. cursor iniciou em área neutra no canto inferior direito;
2. deslocou-se lentamente para a tabela de tendências;
3. deslocou-se para a tabela de alertas;
4. deslocou-se para o card de Water Health Score;
5. retornou à área neutra e permaneceu estável até o encerramento.

Não houve clique, digitação, rolagem, alteração de filtro, acionamento do botão Atualizar Análise, mudança de dados ou interação operacional.

O movimento foi produzido em curva suave, com três focos narrativos e retorno final. A interface permaneceu estável; apenas o cursor atuou como guia visual.

## 4. Inventário das três tomadas

| Tomada | Caminho | Duração | Frames | Resolução | FPS | Codec | Pixel format | Áudio | Tamanho | SHA-256 |
|---|---|---:|---:|---|---|---|---|---|---:|---|
| TAKE 01 | `media/proteus_institutional_video/official_scenes/raw/SC009_TAKE_01.mp4` | 10,766667 s | 323 | 1920×1080 | 30/1 CFR | H.264 | yuv420p | ausente | 1.200.421 bytes | `EFC9159AC0F9A1ECE9F386A1297D03491C4E56EA2AFED286D4F23A65E0C0CFE0` |
| TAKE 02 | `media/proteus_institutional_video/official_scenes/raw/SC009_TAKE_02.mp4` | 10,800000 s | 324 | 1920×1080 | 30/1 CFR | H.264 | yuv420p | ausente | 1.194.499 bytes | `BAD9F9DCFEFF2221FDD980F8C8AB03105812B0A07B31C08A563C3B4855C43391` |
| TAKE 03 | `media/proteus_institutional_video/official_scenes/raw/SC009_TAKE_03.mp4` | 10,800000 s | 324 | 1920×1080 | 30/1 CFR | H.264 | yuv420p | ausente | 1.196.041 bytes | `3C5211CEF9387BAEE9A67C20219CCF3357A6F182305FEDF20A4669A8779A0A96` |

As três tomadas possuem mais que os 249 frames necessários para uma futura janela útil de 8,3 segundos.

### 4.1 Bitrate observado

Embora o encoder tenha sido configurado com target de 16 Mbps e máximo de 20 Mbps, a baixa complexidade de um quadro majoritariamente estável produziu bitrates médios de vídeo entre aproximadamente 881 e 888 Kbps. Não foram observados blocos, perda de nitidez ou falha de decodificação nas amostras 1920×1080. O valor observado permanece registrado para decisão da auditoria de seleção; nenhuma tomada é aprovada automaticamente por esta OEG.

## 5. Validações técnicas

| Verificação | TAKE 01 | TAKE 02 | TAKE 03 |
|---|---|---|---|
| H.264 | conforme | conforme | conforme |
| 1920×1080 | conforme | conforme | conforme |
| 30 fps constante | conforme | conforme | conforme |
| janela útil ≥ 249 frames | conforme | conforme | conforme |
| ausência de áudio | conforme | conforme | conforme |
| decodificação integral | conforme, código 0 | conforme, código 0 | conforme, código 0 |
| frames pretos detectados | nenhum | nenhum | nenhum |
| notificações/janelas externas | nenhuma nas amostras | nenhuma nas amostras | nenhuma nas amostras |
| hashes independentes | conforme | conforme | conforme |

TAKE 01 terminou um frame antes das demais, com 323 frames e 10,766667 s. Essa diferença de 0,033333 s não compromete a janela futura de 249 frames, mas deve permanecer como ressalva comparativa.

## 6. Avaliação preliminar das candidatas

### 6.1 TAKE 01

| Critério | Avaliação preliminar |
|---|---|
| Estabilidade | conforme; interface estável e movimento restrito ao cursor |
| Continuidade visual | compatível com o tema, sidebar e densidade de SC008/SC010 |
| Legibilidade | score, cabeçalhos, tendências e alertas reconhecíveis em 1920×1080 |
| Enquadramento | tela completa; sem recorte ou área externa |
| Ritmo | percurso completo e handles suficientes |
| Aderência à OEG-PA-04 | conforme com ressalva de um frame a menos e uso de FFmpeg em vez do perfil OBS previsto |
| Status | **CANDIDATA TECNICAMENTE VÁLIDA — NÃO APROVADA** |

### 6.2 TAKE 02

| Critério | Avaliação preliminar |
|---|---|
| Estabilidade | conforme; interface estável e movimento contínuo do cursor |
| Continuidade visual | compatível com a passagem Relatórios → Analytics → Governança |
| Legibilidade | conteúdo obrigatório simultaneamente visível |
| Enquadramento | 1920×1080 integral e consistente |
| Ritmo | 324 frames, duração bruta exata de 10,8 s e handles suficientes |
| Aderência à OEG-PA-04 | conforme nos elementos editoriais, com ressalva da ferramenta de captura |
| Status | **CANDIDATA TECNICAMENTE VÁLIDA — NÃO APROVADA** |

### 6.3 TAKE 03

| Critério | Avaliação preliminar |
|---|---|
| Estabilidade | conforme; sem tremor, clique ou mudança de tela |
| Continuidade visual | compatível com SC008 e SC010 |
| Legibilidade | score, explicações, tendências e alertas presentes |
| Enquadramento | aplicação fullscreen, sem elementos externos |
| Ritmo | 324 frames, duração bruta exata de 10,8 s e percurso completo |
| Aderência à OEG-PA-04 | conforme nos elementos editoriais, com ressalva da ferramenta de captura |
| Status | **CANDIDATA TECNICAMENTE VÁLIDA — NÃO APROVADA** |

## 7. Comparação preliminar

As três tomadas apresentam o mesmo estado funcional e o mesmo percurso visual. TAKE 02 e TAKE 03 possuem regularidade temporal ligeiramente superior por conterem exatamente 324 frames. Essa observação não constitui seleção editorial.

Uma OEG posterior deverá reproduzir integralmente as três tomadas em tela cheia, comparar a naturalidade fina do cursor, escolher ou rejeitar uma candidata e, somente depois, avaliar autorização de substituição.

## 8. Ressalvas

1. O perfil e a coleção OBS prescritos pela OEG-PA-04 não existiam na estação; foi usada captura direta FFmpeg com os mesmos parâmetros essenciais.
2. O bitrate médio resultante ficou abaixo do target configurado por causa da baixa complexidade visual; a qualidade aparente está preservada, mas a auditoria de seleção deve deliberar sobre o valor.
3. A detecção automática de congelamento com limiar de -50 dB classifica o fundo da interface como estático; o movimento editorial está concentrado no cursor e deve ser avaliado por playback humano.
4. A avaliação desta OEG é preliminar e baseada em metadados, decodificação integral e folhas de contato. Não substitui a seleção humana em tempo real.
5. Nenhuma tomada recebeu nome ou status de arquivo aprovado.

## 9. Preservação da autoridade

Após a captura foram reconfirmados:

- o projeto Kdenlive permaneceu byte a byte inalterado;
- a SC009 vigente permaneceu byte a byte inalterada;
- nenhum arquivo foi substituído;
- nenhuma timeline foi aberta para edição ou salva;
- nenhuma outra cena foi modificada;
- nenhum Assembly foi renderizado ou exportado;
- nenhuma tomada foi movida para `official_scenes/approved/`;
- foram produzidos exatamente os três MP4s autorizados.

## 10. Conclusão

A OEG-PA-05 produziu e preservou três candidatas independentes da SC009 com resolução, codec, frame rate, conteúdo e duração útil compatíveis com a autorização operacional. Todas demonstram simultaneamente Water Health Score, explicações, tendências e alertas, e executam o percurso visual tendências → alertas → score sem interação funcional.

As três candidatas são tecnicamente válidas para ingressar em uma futura auditoria comparativa. Nenhuma é declarada aprovada, nenhuma substituição está autorizada e o Assembly Cut V1 permanece como única autoridade visual.

**PARECER: `TRES_CANDIDATAS_SC009_PRODUZIDAS — AVALIACAO_E_SUBSTITUICAO_PENDENTES`.**

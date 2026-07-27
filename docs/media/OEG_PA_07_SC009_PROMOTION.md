# OEG-PA-07 — Promoção Controlada da SC009 para a Autoridade Visual

Data: 18/07/2026
Natureza: promoção editorial controlada, limitada à SC009
Parecer: **SC009_TAKE_01 PROMOVIDA — AUTORIDADE VISUAL V2 ESTABELECIDA**

## 1. Objetivo

Promover exclusivamente `SC009_TAKE_01.mp4`, selecionada pela OEG-PA-06, para substituir a SC009 original na autoridade visual do vídeo institucional do PROTEUS, preservando integralmente a autoridade V1 e a estrutura das demais cenas.

Esta OEG não concede Picture Lock e não autoriza pós-produção de áudio, títulos, legendas, créditos, masterização ou render institucional.

## 2. Autoridade anterior e preservação

| Artefato | Caminho | Tamanho | SHA-256 |
|---|---|---:|---|
| Autoridade Visual V1 | `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive` | 165.520 bytes | `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B` |
| SC009 original preservada | `media/proteus_institutional_video/SC009.mp4` | 6.688.012 bytes | `342BECB6183492320FD4A087E55F4CAA3C0FC8120FDA36CBE43E7DDCF28E1B94` |

A V1 não foi sobrescrita, renomeada ou modificada. A SC009 original também permanece no local e com o hash previamente documentado. Os relatórios OEG-PA-01 a OEG-PA-06 permaneceram inalterados.

## 3. Ativo promovido e ativo substituído

### 3.1 Ativo promovido

- Arquivo: `media/proteus_institutional_video/official_scenes/raw/SC009_TAKE_01.mp4`
- SHA-256: `EFC9159AC0F9A1ECE9F386A1297D03491C4E56EA2AFED286D4F23A65E0C0CFE0`
- Tamanho: 1.200.421 bytes
- Formato: H.264, 1920×1080, 30 fps
- Duração bruta: 10,766667 s / 323 frames
- Áudio: ausente

### 3.2 Ativo substituído na timeline

- Arquivo: `media/proteus_institutional_video/SC009.mp4`
- SHA-256: `342BECB6183492320FD4A087E55F4CAA3C0FC8120FDA36CBE43E7DDCF28E1B94`
- Uso anterior: 249 frames / 8,3 s na posição editorial SC009

A substituição ocorreu somente por referência no novo projeto. Nenhum arquivo de mídia foi alterado, recodificado, movido ou excluído.

## 4. Justificativa

A OEG-PA-03 identificou a SC009 original como o único bloqueio de recaptura obrigatória. A OEG-PA-04 definiu o plano de recaptura; a OEG-PA-05 produziu três candidatas; e a OEG-PA-06 aprovou `SC009_TAKE_01.mp4` como a melhor substituição.

A TAKE 01 corrige as não conformidades centrais da original:

- apresenta Water Health Score, explicações, tendências e alertas simultaneamente;
- substitui a imagem estática e de baixa hierarquia por percurso visual orientador;
- preserva tema, sidebar, resolução e linguagem visual das cenas adjacentes;
- não contém cliques, digitação, rolagem ou mudança de dados;
- oferece handles suficientes para uma seleção exata de 249 frames, sem retiming.

## 5. Procedimento de promoção

Foi criada uma nova versão do projeto, mantendo a V1 como baseline histórica:

`media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V2.kdenlive`

Na posição editorial da SC009, a referência à mídia original foi substituída pela TAKE 01. A janela promovida foi definida como:

- frame inicial da fonte: 52;
- frame final da fonte: 300, inclusivo;
- in: `00:00:01.733`;
- out: `00:00:10.000`;
- duração: 249 frames / 8,3 s;
- velocidade: 100%, sem retiming.

A janela descarta o handle inicial excedente, contém o percurso Tendências → Alertas → Water Health Score e termina em quadro estável. A posição da cena e a duração da timeline foram preservadas.

## 6. Nova autoridade visual e cadeia de derivação

```text
Autoridade Visual V1
PROTEUS_ASSEMBLY_CUT_V1.kdenlive
SHA-256 F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B
        │
        └── substituição exclusiva da SC009 original por SC009_TAKE_01
            frames 52–300, 249 frames, sem retiming
        ↓
Autoridade Visual V2
PROTEUS_ASSEMBLY_CUT_V2.kdenlive
SHA-256 B205A2C7E2BC30237959A68AF82C43B8FFA75DA7557566E76617A4562F54DCAC
```

A partir desta OEG, `PROTEUS_ASSEMBLY_CUT_V2.kdenlive` passa a ser a autoridade visual oficial para as etapas subsequentes. A V1 permanece como autoridade histórica imutável e origem verificável da derivação.

## 7. Evidências e verificações de integridade

### 7.1 Estrutura da timeline

| Verificação | V1 | V2 | Resultado |
|---|---:|---:|---|
| Cenas na sequência oficial | 12 | 12 | conforme |
| Duração total | 3.240 frames / 108 s | 3.240 frames / 108 s | preservada |
| Duração da SC009 | 249 frames / 8,3 s | 249 frames / 8,3 s | preservada |
| Duração de SC001–SC008 e SC010–SC012 | baseline | idêntica à baseline | preservada |
| Gaps introduzidos | — | 0 | conforme |
| Overlaps introduzidos | — | 0 | conforme |
| Retiming | — | nenhum | conforme |

A comparação estrutural entre os projetos confirmou que somente os recursos internos e os pontos de entrada/saída associados à SC009 foram atualizados. Nenhuma outra cena, posição editorial, transição ou duração foi modificada.

### 7.2 Referências de mídia

- referências à TAKE 01 na V2: 2, correspondentes ao item de projeto e à instância de timeline;
- referências à SC009 original na V2: 0;
- arquivo original preservado fisicamente: sim;
- TAKE 02 e TAKE 03 preservadas e não utilizadas: sim.

### 7.3 Integridade do projeto Kdenlive

- XML da V2 analisado com sucesso;
- sequência SC001–SC012 preservada;
- projeto validado com o motor MLT/Kdenlive usando consumidor nulo;
- processamento integral concluído com código de saída 0;
- nenhuma mídia offline ou falha de decodificação impeditiva foi detectada;
- nenhum arquivo de render foi produzido.

Durante a validação MLT ocorreram avisos não impeditivos `UDTA parsing failed retrying raw` em fontes OBS preexistentes de outras cenas. Os avisos já pertenciam ao corpus anterior, não interromperam a decodificação e não foram causados pela TAKE 01.

### 7.4 Continuidade visual

Foram inspecionados os quadros limítrofes:

- saída da SC008 × entrada da TAKE 01;
- saída da TAKE 01 × entrada da SC010.

As duas junções preservam o tema escuro, a sidebar, a geometria de interface e a progressão narrativa Relatórios → Previsão Analítica → Governança Operacional. Não foram observados quadro preto, salto de enquadramento, interação indevida ou ruptura visual impeditiva.

## 8. Hashes finais

| Artefato | SHA-256 final |
|---|---|
| Autoridade Visual V1 preservada | `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B` |
| Autoridade Visual V2 | `B205A2C7E2BC30237959A68AF82C43B8FFA75DA7557566E76617A4562F54DCAC` |
| SC009 original preservada | `342BECB6183492320FD4A087E55F4CAA3C0FC8120FDA36CBE43E7DDCF28E1B94` |
| SC009_TAKE_01 promovida | `EFC9159AC0F9A1ECE9F386A1297D03491C4E56EA2AFED286D4F23A65E0C0CFE0` |

## 9. Restrições observadas

- nenhuma alteração em SC002, SC005, SC008 ou SC012;
- nenhuma alteração em qualquer outra cena;
- nenhuma mudança de cortes, transições, títulos, legendas ou créditos;
- nenhuma narração, trilha, mixagem ou masterização;
- nenhum render ou export institucional;
- nenhum Picture Lock concedido;
- nenhum commit, staging ou push executado.

## 10. Ressalvas

- A V2 referencia a TAKE 01 em seu local de preservação `official_scenes/raw/`; o arquivo não foi movido ou duplicado, evitando alteração desnecessária do ativo aprovado.
- A substituição elimina o bloqueio obrigatório da SC009, mas não resolve automaticamente as ressalvas editoriais remanescentes de SC002, SC005, SC008, SC012 e do encerramento visual.
- A concessão de Picture Lock depende da OEG-PA-08 e de nova avaliação editorial formal.

## 11. Parecer final

**PROMOÇÃO APROVADA E EXECUTADA.**

`SC009_TAKE_01.mp4` substitui integralmente a SC009 original na nova autoridade visual V2. A timeline mantém 12 cenas, 3.240 frames e 108 segundos, sem gaps, overlaps ou retiming. A V1, a mídia original, as candidatas não selecionadas e a cadeia documental permanecem preservadas.

A nova autoridade visual oficial é:

`media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V2.kdenlive`

SHA-256:

`B205A2C7E2BC30237959A68AF82C43B8FFA75DA7557566E76617A4562F54DCAC`

**PARECER: `SC009_TAKE_01_PROMOVIDA — AUTORIDADE_VISUAL_V2_ESTABELECIDA — PICTURE_LOCK_NAO_CONCEDIDO`.**

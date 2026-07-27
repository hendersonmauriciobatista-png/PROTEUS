# OEG-PA-08 — Reavaliação do Picture Lock sobre a Autoridade Visual V2

Data: 18/07/2026
Natureza: auditoria editorial observacional e comparativa
Autoridade avaliada: `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V2.kdenlive`
SHA-256: `B205A2C7E2BC30237959A68AF82C43B8FFA75DA7557566E76617A4562F54DCAC`
Parecer: **PICTURE LOCK MANTIDO COMO REPROVADO**

## 1. Objetivo

Reavaliar o estado editorial da Autoridade Visual V2 e determinar, de forma objetiva, quais bloqueios registrados pela OEG-PA-03 foram eliminados pela promoção da `SC009_TAKE_01.mp4` e quais permanecem ativos.

Esta OEG é uma reavaliação focada na evolução V1 → V2. Não constitui nova auditoria integral e não autoriza edição, recaptura, renderização ou pós-produção de áudio.

## 2. Autoridade e referências documentais

### 2.1 Autoridade avaliada

| Artefato | Função | SHA-256 |
|---|---|---|
| `PROTEUS_ASSEMBLY_CUT_V2.kdenlive` | autoridade visual vigente e objeto desta auditoria | `B205A2C7E2BC30237959A68AF82C43B8FFA75DA7557566E76617A4562F54DCAC` |
| `PROTEUS_ASSEMBLY_CUT_V1.kdenlive` | referência histórica comparativa | `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B` |
| `SC009_TAKE_01.mp4` | ativo promovido na V2 | `EFC9159AC0F9A1ECE9F386A1297D03491C4E56EA2AFED286D4F23A65E0C0CFE0` |

### 2.2 Evidências documentais

- OEG-PA-03: parecer editorial original e identificação dos bloqueios;
- OEG-PA-04: plano de remediação da SC009;
- OEG-PA-05: execução e preservação das candidatas;
- OEG-PA-06: seleção técnica da TAKE 01;
- OEG-PA-07: promoção controlada e cadeia de derivação V1 → V2.

## 3. Metodologia

Foram executadas somente operações observacionais:

1. confronto das pendências e decisões registradas na OEG-PA-03 com as evidências da OEG-PA-07;
2. leitura estrutural dos XMLs MLT das autoridades V1 e V2;
3. comparação das 12 entradas da timeline, de seus produtores, pontos de entrada/saída e duração;
4. verificação das referências à SC009 original e à TAKE 01;
5. reconferência dos hashes da V1 e da V2;
6. validação de abertura e decodificação da V2 pelo motor MLT/Kdenlive com consumidor nulo, sem gerar render;
7. reavaliação da continuidade SC008 → SC009 → SC010 com base nos quadros limítrofes já validados na promoção e na preservação estrutural confirmada nesta auditoria;
8. classificação individual de cada pendência como Resolvida, Mantida ou Reclassificada.

Não foi realizada sessão humana presencial de playback contínuo em tempo real e tela cheia. A decodificação integral automatizada comprova integridade técnica, mas não substitui esse requisito editorial humano.

## 4. Comparação V1 × V2

| Critério | Autoridade V1 | Autoridade V2 | Evolução |
|---|---|---|---|
| Sequência | SC001–SC012 | SC001–SC012 | preservada |
| Cenas | 12 | 12 | preservada |
| Duração total | 3.240 frames / 108 s | 3.240 frames / 108 s | preservada |
| Entrada estrutural alterada | — | somente cena 9 | mudança controlada |
| SC009 usada | original | TAKE 01, frames 52–300 | remediada |
| Duração da SC009 | 249 frames / 8,3 s | 249 frames / 8,3 s | preservada |
| SC001–SC008 e SC010–SC012 | baseline V1 | idênticas à baseline V1 | sem evolução editorial |
| Gaps | 0 | 0 | preservado |
| Overlaps | 0 | 0 | preservado |
| Retiming | nenhum | nenhum | preservado |
| Encerramento editável | ausente | ausente | pendência mantida |

A análise das entradas da timeline identificou somente a entrada 9 como diferente. Portanto, não existe fundamento documental ou estrutural para declarar resolvida qualquer pendência das cenas SC002, SC005, SC008 ou SC012 por efeito da promoção da SC009.

## 5. Validação da remediação da SC009

### 5.1 Não conformidades anteriores

Na OEG-PA-03, a SC009 original foi reprovada por apresentar:

- saída textual pequena;
- grande área ociosa;
- baixa legibilidade;
- ausência de elemento analítico visual dominante;
- imagem essencialmente estática e sem orientação do olhar.

### 5.2 Resultado na V2

A SC009 promovida apresenta simultaneamente:

- Water Health Score `100/100` como elemento dominante;
- explicações associadas ao score;
- tendências na região central;
- alertas na região inferior;
- percurso visual Tendências → Alertas → Water Health Score;
- quadro integralmente ocupado por interface funcional legível;
- movimento controlado, sem clique, digitação, rolagem ou mudança de dados.

### 5.3 Continuidade, ritmo e legibilidade

- **Com SC008:** a transição Relatórios → Previsão Analítica mantém tema, sidebar e geometria de interface, enquanto cria progressão semântica clara da produção de relatório para a interpretação analítica.
- **Com SC010:** a transição Previsão Analítica → Governança Operacional preserva a linguagem visual e sustenta a progressão sinais e alertas → eventos e rastreabilidade.
- **Ritmo:** a janela promovida possui exatamente os mesmos 249 frames/8,3 s da SC009 anterior, sem deslocar os cortes; o percurso visual introduz progressão interna ausente na original.
- **Legibilidade:** score, explicações, tendências e alertas permanecem reconhecíveis no enquadramento 1920×1080.

### 5.4 Eficácia da remediação

**CLASSIFICAÇÃO: RESOLVIDA.**

A TAKE 01 elimina as causas específicas que motivaram a recaptura obrigatória. A SC009 deixa de ser bloqueio de recaptura e está editorialmente apta a permanecer na próxima candidata a Picture Lock.

Essa conclusão é específica à SC009. Ela não concede aprovação global da montagem.

## 6. Situação atual das pendências

| Item | Situação na OEG-PA-03 | Evidência na V2 | Classificação atual | Fundamentação |
|---|---|---|---|---|
| SC009 | requer recaptura obrigatória | substituída pela TAKE 01; hierarquia, ocupação, movimento e legibilidade corrigidos | **Resolvido** | a causa-raiz foi eliminada sem alterar duração ou cortes |
| SC002 | requer ajuste de ritmo; 12 s com dois holds longos | entrada, mídia e duração inalteradas | **Mantido** | falta playback humano para deliberar encurtamento ou progressão visual |
| SC005 | requer ajuste de ritmo; hold de 11,3 s e grande margem sobre a locução | entrada, mídia e duração inalteradas | **Mantido** | nenhuma evidência nova elimina o risco de permanência excessiva |
| SC008 | requer ajuste de hierarquia e legibilidade; texto pequeno e grande área vazia | entrada, mídia e duração inalteradas | **Mantido** | continua sendo bloqueio visual material |
| SC012 | requer ajuste; conteúdo denso e estático, sem tratamento de saída | entrada, mídia e duração inalteradas | **Mantido** | a cena e seu corte final permanecem iguais |
| Encerramento visual institucional | ausente da autoridade editável | V2 mantém corte no fim da timeline, sem fade, cartela ou decisão institucional documentada | **Mantido** | nenhuma solução de encerramento foi incorporada |
| Playback humano integral em tela cheia | não realizado | decodificação integral automatizada executada; sessão humana ainda não registrada | **Mantido** | validação técnica não substitui aprovação editorial humana |

Nenhuma pendência foi reclassificada. Uma pendência foi resolvida e seis permanecem mantidas.

## 7. Integridade da Autoridade V2

| Verificação | Resultado |
|---|---|
| XML MLT íntegro | conforme |
| Abertura pelo motor MLT/Kdenlive | conforme |
| Decodificação integral dos 3.240 frames | conforme |
| Código de término da validação | sucesso |
| Mídia offline impeditiva | não detectada |
| Cenas na ordem SC001–SC012 | 12, conforme |
| Duração total | 108 s, preservada |
| Gaps | 0 |
| Overlaps | 0 |
| Alterações fora da SC009 | não detectadas |
| Continuidade editorial técnica | preservada |

Foram emitidos avisos não impeditivos `UDTA parsing failed retrying raw` em fontes OBS preexistentes de outras cenas. O motor concluiu o processamento; os avisos não caracterizam mídia offline, corrupção da V2 ou regressão causada pela SC009 promovida.

## 8. Resumo executivo

A promoção da `SC009_TAKE_01.mp4` foi eficaz e eliminou o único requisito de recaptura obrigatória registrado pela OEG-PA-03. A Autoridade Visual V2 é estruturalmente íntegra, mantém a duração de 108 segundos e melhora materialmente o trecho analítico sem introduzir gaps, overlaps ou mudanças em outras cenas.

O avanço, entretanto, é localizado. Permanecem ativos:

1. ajuste de ritmo da SC002;
2. ajuste de ritmo da SC005;
3. remediação visual da SC008;
4. ajuste editorial da SC012;
5. definição e implementação do encerramento visual institucional;
6. playback humano integral, contínuo, em tempo real e tela cheia.

Entre esses itens, SC008 e o encerramento visual continuam sendo bloqueios materiais diretamente observáveis. SC002, SC005 e a cadência global dependem de deliberação em playback humano. A SC012 permanece associada tanto à densidade do plano quanto à ausência de tratamento final.

## 9. Estado do Picture Lock

O estado **Picture Lock Condicional** não é concedido porque ainda existem alterações visuais potencialmente necessárias em quatro cenas e no encerramento. Uma condição editorial só seria apropriada se a imagem estivesse congelada e restassem confirmações que não pudessem alterar duração ou conteúdo; esse não é o estado atual.

O estado **Picture Lock Concedido** também não é cabível porque os bloqueios remanescentes não foram resolvidos e a revisão humana integral continua ausente.

Consequentemente, o parecer geral permanece:

**PICTURE LOCK MANTIDO COMO REPROVADO.**

## 10. Próximas condições para nova avaliação

Uma futura candidata somente deverá retornar à revisão de Picture Lock após autorização e execução específicas para:

1. deliberar e, se necessário, ajustar o ritmo de SC002 e SC005;
2. remediar a apresentação visual da SC008;
3. revisar SC012 em conjunto com a decisão de encerramento;
4. definir e incorporar o encerramento visual oficial na autoridade editável;
5. executar playback humano integral em tela cheia e registrar data, ambiente e revisor;
6. revalidar estrutura, cortes, duração e hash da nova autoridade.

## 11. Parecer conclusivo

**A remediação da SC009 foi formalmente validada e seu bloqueio foi eliminado.**

Continuam impedindo a concessão definitiva do Picture Lock:

- SC002 e SC005, por ritmo ainda não deliberado em playback humano;
- SC008, por baixa hierarquia, pequena área útil de informação e grande área vazia;
- SC012, por densidade, estaticidade e relação não resolvida com o fim do vídeo;
- ausência de encerramento visual institucional na autoridade editável;
- ausência de playback humano integral, contínuo e em tela cheia.

A Autoridade Visual V2 permanece válida e íntegra como baseline para a próxima remediação, mas ainda não pode ser congelada para início da pós-produção de áudio.

**PARECER: `SC009_RESOLVIDA — PENDENCIAS_SC002_SC005_SC008_SC012_ENCERRAMENTO_E_PLAYBACK_MANTIDAS — PICTURE_LOCK_REPROVADO`.**

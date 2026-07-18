# GP-PI-07 — Auditoria Previa Da Pos-Producao Do Video Institucional Do PROTEUS

## 1. Objetivo

Auditar integralmente o projeto Kdenlive e seu acervo antes de qualquer edicao, conforme a GP-PI-07 e as diretrizes DG-01 a DG-12. Esta auditoria distingue observacoes, inferencias e decisoes e nao investiga raciocinio interno de modelo de IA.

## 2. Momento E Preservacao

Auditoria executada em 17/07/2026 antes de qualquer modificacao desta GP.

O arquivo auditado foi:

`media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive`

SHA-256 anterior a pos-producao:

`F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`

O projeto e os ativos foram somente lidos durante esta etapa.

## 3. Metodologia

Foram utilizados:

* leitura e validacao XML do projeto;
* inventario das propriedades MLT e Kdenlive;
* resolucao e verificacao fisica de todos os recursos referenciados;
* comparacao entre tamanhos declarados no projeto e tamanhos observados;
* inspecao de codecs, streams, resolucao, frame rate, duracao e audio com `ffprobe`;
* decodificacao integral da timeline com `melt` para consumidor nulo;
* decodificacao integral do MP4 preexistente com `ffmpeg`;
* leitura dos manifestos, roteiros, narracoes, legendas e relatorios anteriores;
* verificacao visual da folha de contato consolidada das 12 cenas;
* verificacao dos logos institucionais e de seus hashes.

Ferramentas observadas:

* Kdenlive 26.04.3;
* MLT 7.40.0;
* `melt`, `ffmpeg` e `ffprobe` disponiveis em `C:/Program Files/kdenlive/bin`;
* perfil do projeto: HD 1080p, 1920x1080, progressivo, 30 fps, Rec. 709.

## 4. Integridade Do Projeto Kdenlive

| Item | Evidencia observada | Resultado |
|---|---|---|
| XML | documento carregado sem erro de sintaxe | INTEGRO |
| perfil | 1920x1080, 30/1 fps, progressivo, Rec. 709 | CONSISTENTE |
| estrutura | 24 chains, 2 producers, 9 playlists, 6 tractors, 4 transitions e 8 filters | LEGIVEL |
| timeline principal | 12 entradas consecutivas em `playlist6` | INTEGRA |
| duracao | 3.240 frames; `00:01:48.000`, ultimo frame em `00:01:47.967` | CONSISTENTE |
| render de prova | `melt` percorreu os 3.240 frames e encerrou com codigo 0 | APROVADO COM AVISOS |
| midias offline | nenhuma das 12 midias referenciadas esta ausente | ZERO |
| tamanhos | os 24 registros duplicados de recurso conferem com os 12 arquivos fisicos | CONFORME |
| proxies | desabilitados; nenhum proxy externo requerido | CONFORME |
| audio de timeline | `hasAudio=0`; quatro playlists de audio vazias | AUSENTE |
| legendas de timeline | nenhum SRT ou track de subtitle incorporado | AUSENTE |
| efeitos editoriais | filtros de audio internos desabilitados; sem transicoes narrativas entre cenas | ASSEMBLY CUT |

Aviso nao bloqueante: `melt` emitiu mensagens `UDTA parsing failed retrying raw` ao ler metadados dos MP4 de origem. A decodificacao prosseguiu ate 100% e terminou com codigo 0. Nao foi observada perda de frame ou midia offline.

Inconsistencia textual nao bloqueante: a propriedade de nome da sequencia contem `Sequ?ncia 1`. Nao ha caractere de substituicao UTF-8 no arquivo; o ponto de interrogacao e literal e afeta apenas o rotulo interno.

## 5. Timeline Auditada

| Cena | Trecho de origem | Duracao na timeline |
|---|---:|---:|
| SC001 | 00:00:00.000–00:00:08.967 | 9,0 s |
| SC002 | 00:00:37.000–00:00:48.967 | 12,0 s |
| SC003 | 00:00:00.500–00:00:08.767 | 8,3 s |
| SC004 | 00:00:01.000–00:00:10.167 | 9,2 s |
| SC005 | 00:00:00.500–00:00:11.767 | 11,3 s |
| SC006 | 00:00:00.200–00:00:08.267 | 8,1 s |
| SC007 | 00:00:00.500–00:00:08.967 | 8,5 s |
| SC008 | 00:00:00.400–00:00:08.967 | 8,6 s |
| SC009 | 00:00:00.300–00:00:08.567 | 8,3 s |
| SC010 | 00:00:00.100–00:00:08.067 | 8,0 s |
| SC011 | 00:00:00.400–00:00:08.567 | 8,2 s |
| SC012 | 00:00:00.500–00:00:08.967 | 8,5 s |

Total: 108,0 segundos.

Nao foram observados gaps entre as entradas da playlist de video.

## 6. Integridade Dos Assets

Os recursos efetivamente referenciados pelo projeto sao `SC001.mp4` a `SC012.mp4`. Todos existem dentro de `media/proteus_institutional_video`, possuem video H.264, 1920x1080, 30 fps e audio AAC 48 kHz estereo em seus arquivos de origem. O audio de origem nao esta inserido na timeline.

Hashes SHA-256:

| Ativo | SHA-256 |
|---|---|
| SC001.mp4 | `4007EF48840009542D85E88394222A7B86336D93787195A52EED244F20C428D2` |
| SC002.mp4 | `7F220B9E14920B5B1F91F11B275074D216E84D09C28249091EDBB3E126F2B542` |
| SC003.mp4 | `11AD83436761DAB750AF5D59BE17E71F1DD579E380F827C7BB2131CD1F36DF29` |
| SC004.mp4 | `A16A4BD4ECE379AC3796D598E020D09046CAB36A162B2DA44DFD66E14B467BD1` |
| SC005.mp4 | `684EC7A5916F3781E1C004F1E6800F37BE1AE6F1C7B5B8980EE4D06FF07C4770` |
| SC006.mp4 | `2EAA0D8127703306F3C3496BD0B3F30741882712F0B8F9D2877B84F246CAA365` |
| SC007.mp4 | `25F5F7261CACFF2256F0733440F1054EA54A008541BB59A6E240145D81940342` |
| SC008.mp4 | `D83DD01331C0F66270BD6CF257FAC5CB37102AD100CAD839626B18AA1BA34E09` |
| SC009.mp4 | `342BECB6183492320FD4A087E55F4CAA3C0FC8120FDA36CBE43E7DDCF28E1B94` |
| SC010.mp4 | `F7D853855C827504B14AE282756956AC1C15325F539FE746CB6D3A21A7488BBD` |
| SC011.mp4 | `A23F6D4EF696E824EB76295A04376BDC5E2E81A77636A63BA4E87B2C2BE4AC1B` |
| SC012.mp4 | `7F56B23CAC55D82405C08ABE1060825F85FEBBA50C2D29B25A913D204818E770` |

Os caminhos do projeto sao absolutos. Eles sao validos na maquina auditada, mas reduzem a portabilidade para outra raiz de checkout.

## 7. Narracoes

Foram localizados:

* roteiro final textual do filme de 15 cenas;
* roteiro master do animatic;
* doze textos individuais `NARRACAO_SC001.md` a `NARRACAO_SC012.md` para o Assembly Cut;
* plano de sincronizacao e auditoria cinematografica da locucao.

Nao foi localizado WAV, MP3, FLAC, M4A, AAC ou OGG de narracao. A documentacao GP-PI-06 declara que a narracao foi preparada para gravacao humana e que nenhum TTS ou audio foi produzido.

Conclusao observavel: existe narracao textual, mas nao existe narracao em audio disponivel para sincronizacao.

## 8. Legendas

| Arquivo | Blocos | Termino | Compatibilidade com 108 s |
|---|---:|---:|---|
| `proteus_animatic_v1_pt-BR.srt` | 15 | 00:06:12,000 | NAO |
| `proteus_institutional_film_v1_pt-BR.srt` | 15 | 00:06:50,000 | NAO |

Ambos os arquivos sao UTF-8 legiveis e possuem 15 blocos, mas pertencem a estruturas narrativas diferentes da timeline Kdenlive de 12 cenas. Reutiliza-los sem nova sincronizacao produziria legendas fora de cena.

## 9. Logos Institucionais

Foram localizados quatro arquivos oficiais em `website/assets/logo`:

* `favicon.png`, 310x252;
* `proteus-symbol.png`, 310x252;
* `proteus-dark-signature.png`, 300x220;
* `proteus-official-lockup.png`, 555x445.

Os arquivos sao PNG RGBA validos. O projeto Kdenlive nao os referencia diretamente. O logo aparece visualmente nas capturas de abertura, mas nao existe cartela final adicional na timeline.

## 10. Estrutura De Diretorios

| Diretorio | Arquivos | Volume aproximado | Observacao |
|---|---:|---:|---|
| analysis | 19 | 1,86 MB | folhas de contato |
| audio | 19 | 37 KB | somente documentos textuais |
| captures | 12 | 96 KB | capturas estaticas |
| exports | 3 | 1,44 MB | MP4 estatico e listas |
| manifests | 3 | 15 KB | manifestos e relatorios |
| official_scenes | 0 | 0 | estrutura vazia |
| project | 8 | 190 KB | projeto e guias |
| scripts | 5 | 22 KB | automacao de montagem |
| subtitles | 3 | 4 KB | dois SRT e uma revisao |
| titles | 3 | 13 KB | cartelas estaticas |
| tools | 56 | 161,45 MB | OpenCV local e wheel |

A estrutura prevista existe. `official_scenes` esta vazio, mas as gravacoes oficiais SC001–SC012 estao na raiz do pacote e sao as midias referenciadas pelo projeto.

## 11. Consistencia Entre Projeto, Manifestos E Exportacoes

Foram observadas tres estruturas distintas:

1. Assembly Cut Kdenlive: 12 cenas, 108 s, capturas dinamicas, sem audio e sem legenda.
2. Filme estatico planejado: 15 cenas, manifesto de 6 min 30 s.
3. MP4 preexistente em `exports/final`: 7 min 17,967 s, H.264 1920x1080 a 30 fps, sem audio.

O SRT final termina em 6 min 50 s, tambem divergente do manifesto de 6 min 30 s.

O MP4 preexistente foi decodificado integralmente sem erro, mas sua duracao, origem por concat de imagens e ausencia de audio demonstram que ele nao e uma renderizacao da timeline Kdenlive auditada.

## 12. Riscos E Limitacoes

| ID | Risco ou limitacao | Impacto | Prioridade | Bloqueia pos-producao visual |
|---|---|---|---|---|
| R-01 | nenhuma narracao em audio disponivel | filme nao pode ser certificado como narrado | ALTA | nao |
| R-02 | SRTs existentes incompatíveis com 108 s | legendas fora de sincronismo se reutilizadas | ALTA | nao, se novo SRT for criado |
| R-03 | caminhos absolutos no Kdenlive | baixa portabilidade | MEDIA | nao na maquina atual |
| R-04 | MP4 final preexistente diverge do projeto e do manifesto | ambiguidade de autoridade audiovisual | ALTA | nao, se a nova saida for nomeada de forma inequivoca |
| R-05 | textos pequenos em telas densas | legibilidade limitada em telas menores | MEDIA | nao |
| R-06 | `UDTA` gera avisos no MLT | ruido de metadados | BAIXA | nao |
| R-07 | rotulo interno `Sequ?ncia 1` | defeito textual de metadado | BAIXA | nao |
| R-08 | ausencia de trilha licenciada | filme permanece silencioso | MEDIA | nao |

## 13. Alternativas Razoaveis

### Alternativa A — Editar diretamente o XML Kdenlive

Nao escolhida. A timeline esta integra e a alteracao manual do formato interno aumentaria risco de corrupcao sem beneficio necessario.

### Alternativa B — Adotar o MP4 preexistente de 7:17 como V1 final

Nao escolhida. O arquivo e decodificavel, mas nao corresponde a timeline Kdenlive, ao manifesto de 6:30 ou ao SRT de 6:50.

### Alternativa C — Bloquear toda a pos-producao ate existir voz humana

Nao escolhida. Ha evidencia suficiente para concluir a camada visual e de acessibilidade, mantendo a ausencia de audio como ressalva explicita.

### Alternativa D — Pos-producao nao destrutiva da timeline validada

Escolhida. Renderizar o Kdenlive sem altera-lo, criar SRT especifico para as 12 cenas, aplicar fades, legendas abertas e cartela final com logo oficial, sem inventar voz ou trilha.

Grau de confianca: ALTO para a integridade tecnica e MEDIO-ALTO para a adequacao editorial, porque nao houve revisao humana do video final ainda.

## 14. Conclusao

O projeto Kdenlive e seus 12 ativos estao integros, online e renderizaveis. A timeline e coerente com o Assembly Cut V1 e pode iniciar pos-producao visual nao destrutiva.

A ausencia de narracao em audio, a incompatibilidade dos SRTs existentes e a divergencia entre as tres duracoes impedem declarar o pacote atual como filme institucional final completo antes da nova renderizacao e validacao.

## 15. Parecer

**APTO COM RESSALVAS PARA POS-PRODUCAO NAO DESTRUTIVA**

# OEG-PA-01 — Auditoria Cinematográfica do Assembly Cut V1

Data: 18/07/2026
Projeto auditado: `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive`
Natureza: observacional e não destrutiva
Parecer: **BASELINE ESTABELECIDO — ASSEMBLY CUT ÍNTEGRO COM RESSALVAS**

## 1. Objetivo

Determinar o estado real do projeto audiovisual institucional do PROTEUS e estabelecer um baseline operacional verificável para a retomada da produção, sem editar, salvar, renderizar, exportar ou substituir qualquer ativo.

## 2. Escopo

A auditoria abrangeu o projeto Kdenlive Assembly Cut V1, as 12 mídias referenciadas, a estrutura MLT da timeline, os recursos disponíveis no pacote, os renders preexistentes e a documentação audiovisual relacionada.

Nenhum projeto, mídia, timeline, áudio, narração, legenda, render ou diretório audiovisual foi modificado. O presente relatório é o único arquivo criado.

## 3. Metodologia

Foram executadas somente operações de leitura:

- cálculo SHA-256 do projeto e das 12 fontes;
- parsing XML do arquivo `.kdenlive`;
- inspeção de chains, producers, playlists, tractors, filters e transitions;
- reconstrução em frames da timeline a 30 fps;
- resolução de caminhos e comparação dos tamanhos físicos com os metadados embutidos;
- leitura técnica dos 15 MP4s relevantes por `ffprobe`, sem decodificação para saída;
- comparação com `ASSEMBLY_CUT_V1_REPORT.md` e os relatórios PI-07;
- inspeção das folhas de contato já existentes, sem gerar novas imagens;
- inventário de áudio, narração, legendas, títulos, imagens e exports;
- fingerprint SHA-256 agregado dos 152 arquivos do pacote audiovisual.

O MLT instalado é 7.40.0, igual à versão declarada pelo projeto. O projeto declara Kdenlive 26.04.3. Uma tentativa de consultar `kdenlive.exe --version` iniciou um processo GUI vazio, sem abrir o projeto; esse processo foi encerrado e os hashes/diretórios foram reconferidos. Para evitar locks, autosave, cache ou alteração de preferências, o projeto não foi aberto interativamente nem salvo.

Consequentemente, “abertura correta” foi validada estruturalmente, mas mensagens da interface gráfica não foram reobservadas nesta OEG. A auditoria PI-07 anterior registrou abertura/leitura MLT completa com somente avisos `UDTA parsing failed retrying raw`, não bloqueantes. Como o projeto e as 12 fontes permanecem byte a byte idênticos, não há evidência de regressão desde essa validação.

## 4. Baseline de integridade

| Evidência | Resultado |
|---|---|
| SHA-256 do projeto | `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B` |
| SHA-256 anterior e posterior à PI-07 | idêntico ao valor atual |
| Fingerprint dos 152 arquivos do pacote | `AD17F9BB5971F21963B82C818A2D135870BB9748D468D91B03906197D69D61FB` |
| XML | bem-formado; raiz `mlt` |
| MLT do projeto / instalado | 7.40.0 / 7.40.0 |
| Perfil | HD 1080p, 1920×1080, progressivo, 30/1 fps, Rec.709 |
| Referências únicas | 12 |
| Referências resolvidas | 12/12 |
| Mídias offline | 0 |
| Divergências de tamanho | 0 |
| Hashes das fontes vs. PI-07 | 12/12 idênticos |

Os caminhos são absolutos e apontam para `C:/Users/Guiuliano/SistemaAnaliseAgua/...`. Eles funcionam na máquina auditada, mas reduzem a portabilidade do projeto.

## 5. Inventário do projeto

| Elemento MLT | Quantidade | Observação |
|---|---:|---|
| Chains | 24 | 12 chains de timeline e 12 duplicatas no bin |
| Producers | 2 | incluindo background preto e estrutura auxiliar |
| Playlists | 9 | `playlist6` contém as 12 cenas; sete playlists de trilha estão vazias; `main_bin` é o bin |
| Tractors | 6 | quatro trilhas lógicas, sequência e tractor raiz |
| Transitions | 4 | 2 `mix` e 2 `qtblend`, todos internos/always-active; não são transições narrativas |
| Filters | 8 | filtros internos de áudio; os relevantes estão desabilitados |
| Grupos | 0 | lista vazia |
| Guides | 0 | lista vazia |
| Proxies | desabilitados | nenhum proxy declarado |

Não foram encontrados title producers, referências SRT, imagens, músicas ou arquivos de narração na timeline.

## 6. Inventário da timeline

### 6.1 Estrutura

- sequência: `Sequência 1`;
- duração: 3.240 frames / 108,000 s;
- último frame: `00:01:47.967`;
- ordem: SC001 → SC012;
- trilhas lógicas: 4;
- áudio: 2 trilhas vazias;
- vídeo: 2 trilhas, uma vazia e uma com as 12 cenas;
- propriedade da sequência: `hasVideo=1`, `hasAudio=0`;
- gaps/blanks na playlist usada: 0;
- overlaps: 0;
- transições temporizadas entre cenas: 0;
- padrão editorial: cortes secos consecutivos.

### 6.2 Cenas e cortes

| # | Cena | Trecho da fonte | Frames | Duração | Posição na timeline |
|---:|---|---|---:|---:|---|
| 1 | SC001 — Home | 00:00:00.000–00:00:08.967 | 270 | 9,0 s | 00:00:00.000–00:00:09.000 |
| 2 | SC002 — Sobre | 00:00:37.000–00:00:48.967 | 360 | 12,0 s | 00:00:09.000–00:00:21.000 |
| 3 | SC003 — Plataforma | 00:00:00.500–00:00:08.767 | 249 | 8,3 s | 00:00:21.000–00:00:29.300 |
| 4 | SC004 — Dashboard | 00:00:01.000–00:00:10.167 | 276 | 9,2 s | 00:00:29.300–00:00:38.500 |
| 5 | SC005 — Qualidade da Água | 00:00:00.500–00:00:11.767 | 339 | 11,3 s | 00:00:38.500–00:00:49.800 |
| 6 | SC006 — Dados Ambientais | 00:00:00.200–00:00:08.267 | 243 | 8,1 s | 00:00:49.800–00:00:57.900 |
| 7 | SC007 — Consumo e Distribuição | 00:00:00.500–00:00:08.967 | 255 | 8,5 s | 00:00:57.900–00:01:06.400 |
| 8 | SC008 — Relatórios | 00:00:00.400–00:00:08.967 | 258 | 8,6 s | 00:01:06.400–00:01:15.000 |
| 9 | SC009 — Previsão Analítica | 00:00:00.300–00:00:08.567 | 249 | 8,3 s | 00:01:15.000–00:01:23.300 |
| 10 | SC010 — Governança Operacional | 00:00:00.100–00:00:08.067 | 240 | 8,0 s | 00:01:23.300–00:01:31.300 |
| 11 | SC011 — Painel Executivo | 00:00:00.400–00:00:08.567 | 246 | 8,2 s | 00:01:31.300–00:01:39.500 |
| 12 | SC012 — Dossiê Final | 00:00:00.500–00:00:08.967 | 255 | 8,5 s | 00:01:39.500–00:01:48.000 |

Os 12 cortes coincidem exatamente com o relatório original do Assembly. Não há evidência estrutural de corte incorreto. A continuidade visual observada nas folhas de contato é estável. Avaliação de movimento, microtravamentos e legibilidade quadro a quadro requer reprodução humana posterior em tela cheia.

### 6.3 Observação cinematográfica

- a progressão narrativa é coerente: identidade → contexto → plataforma → operação → análise → governança → síntese;
- SC002 é a cena mais longa e utiliza somente o trecho institucional 37–49 s da fonte de 208,5 s;
- SC006, SC007, SC011 e SC012 exibem tabelas densas e exigem validação de leitura em tamanho de exibição final;
- SC009 permanece visualmente mais fraca: predomínio textual, menor hierarquia gráfica e pouco movimento significativo;
- cortes secos são coerentes com um assembly; não constituem fine cut ou acabamento final.

## 7. Inventário dos recursos

| Recurso | Disponibilidade | Incorporação no projeto | Estado |
|---|---|---|---|
| Vídeos SC001–SC012 | 12/12, H.264 1920×1080 30 fps; AAC 48 kHz estéreo nas fontes | 12/12 como vídeo; áudio oculto | CONCLUÍDO PARA ASSEMBLY |
| Gravações alternativas na raiz | 2 MP4s | não referenciadas | DISPONÍVEL / AUTORIDADE INDEFINIDA |
| Imagens de cenas | 12 capturas PNG | não referenciadas | DISPONÍVEL PARA OUTRAS VERSÕES |
| Títulos | 3 PNGs | não referenciados | PARCIAL |
| Encerramento/cartela | 1 captura e cartela no derivado visual | não incorporado ao `.kdenlive` | PARCIAL |
| Narração textual do Assembly | 12 textos SC001–SC012, guia e plano de sincronização | não referenciada | CONCLUÍDA COMO TEXTO |
| Narração em áudio | 0 WAV/MP3/FLAC/M4A/AAC/OGG/OPUS | ausente | AUSENTE |
| Música | nenhum arquivo musical | ausente | AUSENTE |
| Efeitos sonoros | nenhum arquivo | ausente | AUSENTE |
| Legendas | 3 SRTs; somente `proteus_post_production_v1_pt-BR.srt` possui 12 blocos compatíveis com as cenas | nenhuma no projeto | PARCIAL |
| Créditos | nenhum ativo ou sequência específica | ausente | AUSENTE / NÃO DEFINIDO |

### 7.1 Legendas disponíveis

- `proteus_animatic_v1_pt-BR.srt`: 15 blocos, 00:00–06:12; incompatível com o Assembly;
- `proteus_institutional_film_v1_pt-BR.srt`: 15 blocos, 00:00–06:50; incompatível com o Assembly;
- `proteus_post_production_v1_pt-BR.srt`: 12 blocos, 00:00:00.800–00:01:47.200; sincronizado para o derivado visual.

### 7.2 Renders preexistentes

| Arquivo | Duração | Vídeo | Áudio | Relação com o projeto |
|---|---:|---|---|---|
| `PROTEUS_ASSEMBLY_CUT_V1_BASE.mp4` | 108,000 s | H.264, 1920×1080, 30 fps | nenhum | render-base correspondente à timeline |
| `PROTEUS_INSTITUTIONAL_VIDEO_V1_POST_PRODUCED.mp4` | 111,967 s | H.264, 1920×1080, 30 fps | nenhum | derivado com fades, legendas abertas e cartela final |
| `PROTEUS_INSTITUTIONAL_FILM_V1.mp4` | 437,967 s | H.264, 1920×1080, 30 fps | nenhum | versão estática anterior/divergente; não corresponde à timeline Assembly |

As folhas de contato do derivado de 111,967 s mostram 12 legendas legíveis, abertura tratada e cartela final. Esse acabamento não está salvo no projeto Kdenlive: foi produzido como derivação não destrutiva. Portanto, o MP4 derivado não transforma o `.kdenlive` em fine cut ou picture lock.

## 8. Estado atual do Assembly

### Classificação do projeto editável

**ASSEMBLY CUT ÍNTEGRO E CONGELADO.**

Fundamentação:

- contém a seleção e a ordem definitiva do assembly de 12 fontes;
- cortes conferem com o relatório de montagem;
- não possui gaps, overlaps ou mídia offline;
- possui somente uma trilha de vídeo efetivamente usada;
- não contém narração, música, SFX, legendas, títulos, créditos ou transições editoriais;
- não há aprovação de picture lock nem mixagem/masterização.

Ele não deve ser classificado como Rough Cut, Fine Cut ou Picture Lock.

### Classificação do pacote de produção

**ASSEMBLY CUT PRESERVADO + DERIVADO DE PÓS-PRODUÇÃO VISUAL V1, COM PÓS-PRODUÇÃO DE ÁUDIO NÃO INICIADA.**

O derivado visual representa progresso real de acabamento e acessibilidade, mas permanece silencioso e separado do projeto editável. A produção total ainda não alcançou masterização nem versão institucional final certificada.

## 9. Pendências

### Prioridade alta

1. Definir formalmente a autoridade de retomada: timeline Kdenlive de 108 s ou derivado visual de 111,967 s.
2. Congelar o formato narrativo final: versão curta de 12 cenas versus filme planejado de 15 cenas/6m30s; o MP4 legado de 437,967 s não pode ser tratado como master.
3. Executar abertura e reprodução humana controlada do projeto em Kdenlive, sem salvar, para confirmar ausência de mensagens GUI, playback, cortes e legibilidade em movimento.
4. Aprovar picture lock visual antes de iniciar áudio; registrar explicitamente se SC009 será mantida ou recapturada.
5. Gravar e editar a narração dos 12 textos, ou deliberar formalmente por uma versão silenciosa.
6. Definir música/ambiência e comprovar licença, ou formalizar ausência deliberada de trilha.
7. Sincronizar, mixar e normalizar voz/música/SFX; atualmente não existe pós-produção de áudio.
8. Escolher a política de legendas: SRT sidecar acessível, legendas abertas ou ambas; validar sincronia na versão efetivamente escolhida.
9. Definir créditos, direitos, identidade final e autorização de publicação externa.

### Prioridade média

1. Avaliar recaptura de SC009 com resultado visual mais forte.
2. Validar legibilidade em tela cheia de SC006, SC007, SC011 e SC012.
3. Converter caminhos absolutos em estratégia portátil somente após backup e nova autoridade.
4. Reconciliar `official_scenes/` vazio com a localização real das fontes na raiz.
5. Definir nomenclatura inequívoca para assembly, derivado visual, fine cut, picture lock e master.
6. Atualizar manifesto de produção somente depois da escolha de autoridade visual.
7. Avaliar correção de cor, consistência de contraste, safe areas e ritmo de entrada/saída.

### Prioridade baixa

1. Organizar gravações alternativas, exports legados e arquivos de concatenação sem eliminar evidência histórica.
2. Criar guides/markers de cenas na timeline para facilitar áudio e revisão.
3. Avaliar proxies e empacotamento portátil para colaboração futura.
4. Padronizar miniaturas, pastas e metadados do bin.

## 10. Riscos

| Risco | Prioridade | Impacto |
|---|---|---|
| três durações/linhas editoriais concorrentes | alta | versão errada pode ser tratada como final |
| projeto editável e derivado visual separados | alta | alterações futuras podem não ser reproduzíveis no Kdenlive |
| ausência total de áudio final | alta | impede filme narrado/musicado e masterização |
| ausência de picture lock formal | alta | áudio e legendas podem ser sincronizados sobre edição ainda mutável |
| GUI não reaberta nesta OEG | média | mensagens específicas da interface permanecem não revalidadas |
| caminhos absolutos | média | mídias podem ficar offline em outra máquina/raiz |
| SC009 e tabelas densas | média | menor impacto ou legibilidade em exibição real |
| créditos/licenças não fechados | média | bloqueio de publicação externa |
| exports antigos sem autoridade inequívoca | média | confusão operacional e retrabalho |

## 11. Recomendações

1. Tratar o `.kdenlive` atual como baseline imutável `Assembly Cut V1`.
2. Não sobrescrever o projeto; qualquer evolução deve criar versão derivada explicitamente identificada.
3. Adotar o derivado de 111,967 s como candidato visual somente após revisão humana, não como master automático.
4. Realizar uma OEG específica de picture lock antes de voz, música e mixagem.
5. Em seguida, executar uma OEG exclusiva de produção de áudio, com arquivos, licenças, loudness e critérios de aprovação definidos.
6. Manter o MP4 de 437,967 s como legado separado e não autoritativo para o Assembly.
7. Preservar hashes, cortes e fontes atuais como baseline de comparação em todas as etapas futuras.

## 12. Parecer final

**BASELINE OPERACIONAL ESTABELECIDO — ASSEMBLY CUT V1 ÍNTEGRO, ONLINE E COERENTE, MAS NÃO FINAL.**

O estado exato é:

- projeto Kdenlive de 12 cenas, 108 s, íntegro, sem gaps/overlaps e com cortes secos corretos;
- fontes 12/12 online e byte a byte idênticas ao baseline PI-07;
- timeline sem áudio, legenda, títulos, créditos ou acabamento editorial final;
- derivado visual silencioso de 111,967 s disponível e tecnicamente mais avançado, porém externo à timeline;
- narração em texto disponível, mas áudio, música, mixagem, picture lock e masterização ausentes;
- versão legada de 437,967 s divergente e não autoritativa para este Assembly.

A retomada é tecnicamente viável, mas deve começar pela decisão de autoridade visual e por uma revisão humana de picture lock. Nenhuma edição deve iniciar diretamente sobre o baseline sem essa deliberação.

# GP-PI-07A — Relatorio De Governanca Das Premissas E Fundamentacao Das Decisoes

## 1. Natureza E Limite Cientifico

Artefato experimental produzido durante a GP-PI-07 para investigar a rastreabilidade da cadeia observavel que conduz a decisoes de execucao.

Este documento nao descreve, infere ou audita raciocinio interno de modelo. Registra apenas premissas declaradas, evidencias verificaveis, inferencias identificadas como tais, fundamentacoes, decisoes e validacoes observaveis.

Diretrizes aplicadas: DG-01 a DG-12.

## 2. Premissas

| ID | Descricao | Origem | Motivo da adocao | Estado |
|---|---|---|---|---|
| P-001 | a solicitacao GP-PI-07/07A e a autoridade operacional desta execucao | comando fornecido pelo responsavel | delimitar escopo e governanca | confirmada |
| P-002 | `PROTEUS_ASSEMBLY_CUT_V1.kdenlive` e a referencia editorial a ser auditada | manifesto do Assembly Cut e plano de sincronizacao GP-PI-06 | ambos apontam explicitamente para o arquivo | confirmada |
| P-003 | nenhuma edicao pode anteceder a auditoria completa | GP-PI-07 | requisito expresso | confirmada |
| P-004 | somente elementos locais, licenciados ou oficiais podem integrar a saida | README e manifestos audiovisuais | evitar introducao de propriedade externa sem licenca | confirmada |
| P-005 | ausencia de evidencia de licenca ou gravacao impede presumir disponibilidade de voz ou musica | DG-06, DG-08 e DG-11 | impedir que ausencia seja substituida por hipotese | confirmada |
| P-006 | a saida visual pode ser produzida sem alterar o projeto-fonte quando a cadeia for reproduzivel | natureza nao destrutiva da pos-producao | preservar a baseline auditada | confirmada |
| P-007 | `FontSize=34` e `MarginV=48` produziriam legenda proporcional em 1920x1080 | estimativa inicial de estilo ASS | viabilizar a primeira renderizacao | rejeitada |
| P-008 | `FontSize=12` e `MarginV=14` produzem legenda legivel e menos obstrutiva neste pipeline | revisao baseada na primeira folha de contato | corrigir a escala observada | confirmada |

Nenhuma premissa foi omitida intencionalmente. P-006 foi confirmada pela execucao. P-007 foi rejeitada por evidencia visual e substituida explicitamente por P-008.

## 3. Evidencias

| ID | Origem | Metodo | Natureza | Confiabilidade | Limitacoes |
|---|---|---|---|---|---|
| E-001 | solicitacao GP-PI-07/07A e DG-01–DG-12 | leitura integral | leitura de arquivo/comando | alta | define objetivos, nao prova estado tecnico |
| E-002 | projeto Kdenlive | parser XML | inspecao do projeto | alta | nao substitui revisao visual humana |
| E-003 | 12 recursos SC001–SC012 | `Test-Path`, tamanho e SHA-256 | resultado de comando | alta | hash prova identidade, nao qualidade editorial |
| E-004 | streams dos MP4 | `ffprobe` | resultado de comando | alta | metadados nao provam legibilidade visual |
| E-005 | timeline completa | `melt` para consumidor nulo | resultado de comando | alta | valida decodificacao, nao gosto editorial |
| E-006 | folha de contato | inspecao visual direta | observacao direta | media-alta | amostragem, nao todos os frames |
| E-007 | narracoes | inventario e leitura dos arquivos | leitura de arquivo | alta | existem textos, nao audio |
| E-008 | pasta de audio | busca por extensoes de midia sonora | resultado de comando | alta | limitada ao acervo local auditado |
| E-009 | dois SRTs | parser de timecodes | leitura de arquivo | alta | nao avalia percepcao humana de leitura |
| E-010 | logos oficiais | `ffprobe`, tamanho e SHA-256 | resultado de comando | alta | oficialidade deriva da localizacao e documentacao do repositorio |
| E-011 | MP4 preexistente | `ffprobe` e decodificacao `ffmpeg` | resultado de comando | alta | nao informa intencao autoral original |
| E-012 | manifestos e relatorios PI-05/PI-06 | leitura integral | leitura de arquivo | alta | contem planos e pareceres, nao audio ausente |
| E-013 | instalacao Kdenlive | localizacao de executaveis | resultado de comando | alta | valida ambiente atual apenas |
| E-014 | primeira saida e folha de contato | render e inspecao visual | observacao direta | alta para o defeito observado | amostra de quatro frames |
| E-015 | segunda saida e folhas de contato | render e inspecao de 12 cenas e cartela | observacao direta | media-alta | amostragem de frames, sem sessao humana de playback integral |
| E-016 | segunda saida | `ffprobe`, contagem de frames e decodificacao integral | resultado de comando | alta | nao mede compreensao humana |
| E-017 | projeto-fonte apos a execucao | SHA-256 | resultado de comando | alta | prova identidade binaria, nao intencao editorial |
| E-018 | SRT final | parser de timecodes e SHA-256 | resultado de comando | alta | conforto de leitura depende tambem do espectador |

## 4. Inferencias

| ID | Descricao | Evidencias | Premissas | Confianca | Limitacoes |
|---|---|---|---|---|---|
| I-001 | o projeto Kdenlive esta estruturalmente apto para renderizacao | E-002, E-003, E-004, E-005 | P-002, P-003 | alta | nao equivale a aprovacao editorial final |
| I-002 | o MP4 de 7:17 nao e render direto da timeline Kdenlive de 1:48 | E-002, E-011, E-012 | P-002 | alta | nao exclui que seja outro prototipo legitimo |
| I-003 | os SRTs existentes nao podem ser reutilizados sem ressincronizacao | E-002, E-009 | P-002 | alta | novo timing ainda precisa ser validado visualmente |
| I-004 | nao existe narracao pronta para insercao | E-007, E-008, E-012 | P-005 | alta | limitada ao acervo local; gravacao externa nao fornecida pode existir |
| I-005 | a estrategia de menor risco e preservar o Kdenlive e aplicar pos-processamento reproduzivel sobre sua renderizacao | E-002, E-005, E-013 | P-004, P-006 | media-alta | depende da validacao do render final |
| I-006 | criar voz ou musica nesta GP sem fonte e licenca acrescentaria risco nao fundamentado | E-008, E-012 | P-004, P-005 | alta | nao avalia uma futura gravacao legitimamente fornecida |
| I-007 | a primeira configuracao tipografica obstrui conteudo relevante e nao pode ser aprovada | E-014 | P-007 | alta | conclusao restrita ao estilo usado nesse pipeline |
| I-008 | a configuracao revisada preserva legibilidade com menor obstrucao nas 12 cenas amostradas | E-015, E-018 | P-008 | media-alta | requer revisao humana integral para certificacao editorial definitiva |

Inferencias nao sao apresentadas como fatos observados.

## 5. Decisoes E Fundamentacao

### D-001 — Preservar O Projeto Kdenlive

* Premissas: P-002, P-003, P-006.
* Evidencias: E-002, E-003, E-005.
* Inferencias: I-001, I-005.
* Fundamentacao: o projeto e integro e renderizavel; modifica-lo manualmente nao e necessario para gerar uma camada final reproduzivel.
* Decisao: manter o SHA-256 do `.kdenlive` e renderizar de forma nao destrutiva.
* Impacto esperado: baseline preservada e comparacao objetiva antes/depois.
* Riscos: pipeline externo pode divergir de uma edicao interativa.
* Alternativas: edicao manual do XML; edicao GUI; bloqueio total.
* Motivo da escolha: menor risco de corrupcao e maior reprodutibilidade.
* Confianca: alta.
* Validacao: APROVADA. O SHA-256 do projeto permaneceu `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B` antes e depois da execucao.

### D-002 — Criar Legenda Especifica Para As 12 Cenas

* Premissas: P-002, P-004.
* Evidencias: E-007, E-009, E-012.
* Inferencias: I-003.
* Fundamentacao: ha doze textos de narracao aprovados para os doze trechos, enquanto os SRTs existentes possuem quinze blocos e duracoes incompatíveis.
* Decisao: converter os textos SC001–SC012 em SRT sincronizado com 108 s, mantendo no maximo duas linhas por bloco.
* Impacto esperado: acessibilidade e coerencia narrativa sem inventar conteudo.
* Riscos: leitura humana pode requerer microajustes posteriores.
* Alternativas: reutilizar SRT de 6:12; reutilizar SRT de 6:50; omitir legendas.
* Motivo da escolha: e a unica alternativa compatível com a timeline e com os textos governados.
* Confianca: alta para timing estrutural; media-alta para conforto de leitura.
* Validacao: APROVADA COM RESSALVA. O SRT possui 12 blocos, nenhum intervalo invalido ou sobreposto e termina em `00:01:47,200`. As 12 cenas foram amostradas visualmente; falta revisao humana integral.

### D-003 — Nao Gerar Voz Ou Trilha

* Premissas: P-004, P-005.
* Evidencias: E-007, E-008, E-012.
* Inferencias: I-004, I-006.
* Fundamentacao: nao existe arquivo de narracao, trilha licenciada ou autorizacao para substituir a gravacao humana planejada por TTS.
* Decisao: manter a saida sem audio e registrar a limitacao.
* Impacto esperado: nenhuma fonte ou licenca e presumida.
* Riscos: menor impacto cinematografico e necessidade de versao narrada futura.
* Alternativas: TTS local; reaproveitar audio das capturas; trilha externa.
* Motivo da escolha: as alternativas nao possuem fundamentacao ou licenca observavel suficiente.
* Confianca: alta.
* Validacao: APROVADA COM RESSALVA. A saida contem somente stream de video, conforme decidido. A ausencia de narracao continua sendo limitacao material declarada.

### D-004 — Aplicar Somente Tratamentos Visuais Minimos

* Premissas: P-004, P-006.
* Evidencias: E-005, E-006, E-010.
* Inferencias: I-005.
* Fundamentacao: a narrativa visual ja esta montada; fades, legendas abertas e cartela final oficial aumentam acabamento sem reordenar ou reinterpretar as cenas.
* Decisao: fade de abertura, fade de fechamento da timeline, legendas abertas e cartela final de quatro segundos com o lockup oficial.
* Impacto esperado: acabamento institucional e encerramento inequívoco.
* Riscos: sobreposicao de legenda em conteudo denso; cartela aumenta a duracao para aproximadamente 112 s.
* Alternativas: watermark permanente; transicoes entre todas as cenas; nenhuma intervencao.
* Motivo da escolha: watermark pode obstruir a interface e transicoes mudariam o ritmo validado.
* Confianca: media-alta.
* Validacao inicial: REJEITADA. `FontSize=34` e `MarginV=48` produziram legendas desproporcionais e obstrutivas, confirmando I-007 e rejeitando P-007.
* Correcao: estilo revisado para `FontSize=12` e `MarginV=14`, sem alterar texto ou timecodes.
* Validacao final: APROVADA COM RESSALVA. A segunda folha de contato de quatro quadros e a folha de contato das 12 cenas confirmam escala e posicao adequadas nas amostras, sustentando I-008. Falta sessao humana integral.

## 6. Cadeia Consolidada Inicial

P-001–P-008

↓

E-001–E-018

↓

I-001–I-008

↓

fundamentacoes D-001–D-004

↓

decisoes D-001–D-004

↓

validacoes registradas, incluindo uma rejeicao e uma correcao

## 7. Registro De Revisoes

### REV-001 — Escala Das Legendas

* Premissa original: P-007.
* Motivo da invalidacao: E-014 demonstrou que o texto cobria parcela material da interface.
* Nova evidencia: E-014.
* Nova inferencia: I-007.
* Nova fundamentacao: reduzir escala e margem, sem alterar conteudo, timing ou decisao de acessibilidade.
* Nova premissa: P-008.
* Nova evidencia de validacao: E-015.
* Nova inferencia: I-008.
* Impacto sobre a decisao: D-004 foi mantida em seu objetivo, mas teve seus parametros tipograficos alterados.

O historico da primeira configuracao permanece neste documento; ele nao foi ocultado ou reescrito como se a primeira tentativa tivesse sido aprovada.

## 8. Resultado Tecnico Observado

* arquivo: `media/proteus_institutional_video/exports/post_production_v1/PROTEUS_INSTITUTIONAL_VIDEO_V1_POST_PRODUCED.mp4`;
* duracao: `111,966667` segundos;
* video: H.264, 1920x1080, 30 fps, yuv420p;
* frames decodificados: 3.359;
* audio: ausente por decisao D-003;
* tamanho: 2.627.425 bytes;
* SHA-256: `681734FF429E66F49B4D5FE3C30EEF16BB74FB7CF4A316E4151023EDDE88790B`;
* decodificacao integral: codigo 0;
* projeto Kdenlive preservado: hash anterior e posterior identicos.

## 9. Auditoria Final

### Quantificacao

* Premissas utilizadas: 8.
* Premissas que permaneceram validas ou foram confirmadas: 7.
* Premissas revisadas durante a execucao: 1 cadeia de revisao, P-007 → P-008.
* Premissas rejeitadas: 1, P-007.
* Evidencias utilizadas: 18.
* Inferencias produzidas: 8.
* Inferencias que permaneceram validas: 8, cada uma dentro de suas limitacoes declaradas.
* Inferencias revisadas: 0; novas inferencias I-007 e I-008 foram adicionadas quando surgiram novas evidencias.

### Respostas Obrigatorias

**Alguma decisao foi alterada apos revisao das inferencias?**

Sim. D-004 manteve o objetivo, mas seus parametros de fonte e margem foram alterados apos E-014 e I-007.

**Todas as decisoes possuem fundamentacao rastreavel?**

Sim. D-001 a D-004 ligam premissas, evidencias, inferencias, justificativa, alternativas, decisao e validacao.

**Existe alguma decisao baseada apenas em inferencia nao corroborada?**

Nao. Todas as decisoes citam evidencias observaveis. As inferencias possuem limitacoes declaradas.

**Existe alguma decisao cuja fundamentacao seja insuficiente?**

Nao para o escopo visual executado. Nao ha fundamentacao suficiente para declarar uma versao narrada ou musical; por isso nenhuma decisao de inserir voz ou trilha foi tomada.

**O resultado final confirma a consistencia da cadeia de governanca?**

Sim, com ressalva. A cadeia permitiu detectar, rejeitar e corrigir uma decisao parametrica sem ocultar a tentativa inicial. A consistencia editorial definitiva ainda depende de revisao humana integral do video.

## 10. Conclusao Experimental

O experimento demonstra que a cadeia Premissas → Evidencias → Inferencias → Fundamentacao → Decisao → Validacao produziu rastreabilidade operacional suficiente para reconstruir as quatro decisoes relevantes e sua correcao.

Resultado experimental: **CADEIA DE GOVERNANCA CONSISTENTE COM RESSALVAS**.

# GP-PI-07 — Relatorio De Execucao Da Pos-Producao Do Video Institucional V1

## 1. Objetivo

Concluir a camada visual de pos-producao do Video Institucional V1 a partir da timeline Kdenlive auditada, preservando o projeto-fonte e registrando todas as limitacoes materiais.

## 2. Autoridades E Evidencias

* `docs/presentation/PI_07_KDENLIVE_PRE_POSTPRODUCTION_AUDIT.md`;
* `docs/research/PI_07A_DECISION_FOUNDATION_GOVERNANCE_REPORT.md`;
* `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive`;
* textos de narracao GP-PI-06 para SC001–SC012;
* logo `website/assets/logo/proteus-official-lockup.png`;
* ferramentas Kdenlive/MLT/FFmpeg locais.

## 3. Escopo Executado

1. Renderizacao nao destrutiva dos 3.240 frames da timeline Kdenlive.
2. Criacao de SRT UTF-8 com 12 blocos sincronizados aos 108 segundos.
3. Aplicacao de fade de abertura e fade no encerramento da timeline.
4. Insercao de legendas abertas em portugues.
5. Insercao de cartela final branca de aproximadamente quatro segundos com o lockup oficial.
6. Exportacao H.264 em 1920x1080, 30 fps e yuv420p.
7. Validacao de streams, duracao, frames, hashes, decodificacao e amostras visuais.

Nao foram inseridos voz, musica, efeito sonoro, material externo, nova funcionalidade ou nova arquitetura.

## 4. Artefatos Produzidos

| Artefato | Finalidade |
|---|---|
| `media/proteus_institutional_video/subtitles/proteus_post_production_v1_pt-BR.srt` | legenda sincronizada das 12 cenas |
| `media/proteus_institutional_video/scripts/build_post_production_v1.cmd` | pipeline reproduzivel |
| `media/proteus_institutional_video/exports/post_production_v1/PROTEUS_ASSEMBLY_CUT_V1_BASE.mp4` | render-base do Kdenlive |
| `media/proteus_institutional_video/exports/post_production_v1/PROTEUS_INSTITUTIONAL_VIDEO_V1_POST_PRODUCED.mp4` | saida pos-produzida |
| `media/proteus_institutional_video/analysis/post_production_v1/POST_PRODUCTION_V1_CONTACT.png` | evidencia de abertura, legenda, fechamento e cartela |
| `media/proteus_institutional_video/analysis/post_production_v1/POST_PRODUCTION_V1_ALL_CAPTIONS.png` | evidencia amostral das 12 legendas |

## 5. Resultado Tecnico

| Propriedade | Resultado |
|---|---|
| duracao | 111,966667 s |
| frames | 3.359 |
| resolucao | 1920x1080 |
| frame rate | 30/1 fps |
| codec | H.264 |
| pixel format | yuv420p |
| audio | ausente |
| tamanho | 2.627.425 bytes |
| SHA-256 | `681734FF429E66F49B4D5FE3C30EEF16BB74FB7CF4A316E4151023EDDE88790B` |
| decodificacao integral | APROVADA, codigo 0 |

O render-base possui 108,000000 segundos, H.264, 1920x1080 e 30 fps.

## 6. Validacao Das Legendas

* 12 blocos;
* nenhum bloco sobreposto ou com intervalo invalido;
* ultimo bloco termina em `00:01:47,200`, antes do encerramento da timeline;
* no maximo duas linhas definidas por bloco;
* termos institucionais preservados;
* acentos UTF-8 renderizados corretamente nas amostras;
* as 12 cenas foram amostradas em folha de contato.

### Correcao Executada

A primeira renderizacao usou fonte 34 e margem 48. A inspecao visual demonstrou obstrucao relevante da interface. Essa configuracao foi rejeitada.

A segunda renderizacao usou fonte 12 e margem 14. As folhas de contato confirmaram menor obstrucao e legibilidade adequada nas amostras. O historico da correcao esta preservado no relatorio GP-PI-07A.

## 7. Integridade Do Projeto-Fonte

SHA-256 anterior:

`F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`

SHA-256 posterior:

`F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`

Conclusao: o projeto Kdenlive nao foi modificado.

## 8. Riscos E Ressalvas Remanescentes

| Risco ou ressalva | Impacto | Acao recomendada | Bloqueia a saida visual |
|---|---|---|---|
| ausencia de narracao humana | reduz impacto cinematografico | gravar os 12 textos e produzir versao sonora governada | nao |
| ausencia de trilha licenciada | video permanece silencioso | manter silencio ou fornecer trilha com licenca verificavel | nao |
| revisao visual realizada por amostragem | pode haver detalhe nao percebido entre frames amostrados | playback humano integral em tela cheia | nao |
| caminhos absolutos no Kdenlive | limita reproducao em outra raiz | relink governado ou pacote portavel futuro | nao na maquina atual |
| `UDTA` gera avisos no MLT | ruido de log | normalizar metadados apenas em etapa futura autorizada | nao |

## 9. Limitacao De Escopo

Esta entrega conclui a pos-producao visual e de acessibilidade aberta. Ela nao certifica uma versao narrada, musicada ou aprovada para publicacao externa. A ausencia de audio foi deliberadamente preservada por falta de arquivo e licenca observaveis.

## 10. Conclusao

A timeline Kdenlive foi renderizada sem alteracao, recebeu tratamento visual minimo, legenda sincronizada e cartela institucional final. A saida e reproduzivel e tecnicamente valida.

A primeira configuracao de legenda foi rejeitada e corrigida com rastreabilidade completa, demonstrando o funcionamento pratico da governanca experimental GP-PI-07A.

## 11. Veredito

**POS-PRODUCAO VISUAL V1 CONCLUIDA COM RESSALVAS**

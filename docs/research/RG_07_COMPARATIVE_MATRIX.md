# GP-RG-07 - Matriz Comparativa Interavaliadores

## 1. Congelamento Das Saidas

| Avaliador | Bytes | SHA-256 | Encerramento |
|---|---:|---|---|
| A | 24212 | `30258BF68A53310564495CDC6AD64E3D9BDF907614E0897CE5EBF0666403C350` | suspenso; `TESTE_INCONCLUSIVO` |
| B | 25835 | `60540ABC84FA56C4F203F5654238E88F95C439030AB00D6E8B203054D2584601` | suspenso; `TESTE_INCONCLUSIVO` |

Os arquivos foram lidos pelo coordenador somente depois do encerramento de ambos. Nenhuma saida individual foi editada, corrigida ou submetida a consenso.

## 2. Resultado Comparativo Principal

Ambos os avaliadores detectaram de forma independente a mesma falha bloqueante: 12/13 artefatos eram resolviveis e o `pasted-text.txt` da OEG-RG-06, apesar de hashado, nao possuia localizador resolvivel no plano entregue. Ambos suspenderam antes da selecao substantiva e recusaram substituir a ausencia pelo resumo, memoria ou fonte externa.

Isso demonstra convergencia na aplicacao do gate de integridade, mas nao produz observacoes sobre reproducao da selecao, reconstrucao ou auditoria de um caso. O resultado de H-RG-004/OV-06 permanece `TESTE_INCONCLUSIVO`.

## 3. Matriz Dos Criterios Obrigatorios

| Criterio | Avaliador A | Avaliador B | Comparacao |
|---|---|---|---|
| selecao do caso | nenhum; triagem nao iniciada | nenhum; triagem nao iniciada | convergencia operacional 1/1; nao e acordo sobre elegibilidade de caso |
| premissas | pacote integral obrigatorio; ausencia nao imputavel | mesmas duas premissas centrais | convergencia semantica |
| evidencias | 12 hashes conformes; OEG nao localizada; regra de suspensao | mesmas tres evidencias centrais | convergencia semantica |
| inferencias | pacote/igualdade nao auditavel; prosseguir seria D3 | mesmas inferencias, separadas em duas | convergencia de conteudo; extensao de granularidade em B |
| fundamentacao | controles impedem substituir OEG por resumo | mesma fundamentacao | convergencia |
| decisoes | suspender antes da selecao | suspender e nao solicitar copia alternativa | mesma decisao principal; B explicita decisao secundaria |
| validacao | cadeia de suspensao possui V explicita | validacao aparece em texto, sem no V separado | divergencia de formalizacao, sem mudanca da suspensao |
| classificacao global | `TESTE_INCONCLUSIVO` | `TESTE_INCONCLUSIVO` | convergencia |
| limitacoes | caminho do anexo ausente; pacote incompleto; plataforma comum | mesmas limitacoes | convergencia |
| independencia declarada | sem comunicacao/leitura alheia/fonte externa | sem comunicacao/leitura alheia/fonte externa | convergencia declaratoria; ausencia de log de acesso limita verificacao |

## 4. Acordos Quantitativos Descritivos

| Unidade | Acordo | Denominador | Resultado | Limite |
|---|---:|---:|---:|---|
| status de integridade por artefato | 13 | 13 | 100,0% | mede deteccao do pacote, nao caso |
| decisao principal de suspensao | 1 | 1 | 100,0% | resposta ao mesmo bloqueio |
| selecao operacional | 1 | 1 | 100,0% | ambos selecionaram nenhum; nao aplicaram CI/CE/GC |
| estados dos cinco OV autorizados | 5 | 5 | 100,0% | todos `TESTE_INCONCLUSIVO` |
| estados das hipoteses comuns pre-registradas H-RG-001/004/007 | 1 | 3 | 33,3% | acordo somente em H-RG-004 |
| estados/valores exatos das 15 metricas individuais | 2 | 15 | 13,3% | acordo exato em MA-04 e MA-05; demais diferem principalmente no codigo de ausencia |
| caminhos decisorios de caso | NAO_COLETADO | 0 | `NAO_APLICAVEL` | nenhum caso analisado |
| classificacoes P/E/I/F/D/V de caso | NAO_COLETADO | 0 | `NAO_APLICAVEL` | nenhum item de caso lido |

Nao foi calculado kappa/alpha: nao ha unidades de caso codificadas, e o pequeno conjunto de estados metodologicos nao sustenta coeficiente corrigido por acaso defensavel.

## 5. Convergencias

1. 12 hashes confirmados e um artefato obrigatorio nao localizado;
2. falha classificada como bloqueante antes da analise;
3. nenhum CP selecionado ou excluido substantivamente;
4. nenhuma reconstrucao de caso produzida;
5. fonte adicional necessaria registrada e nao consultada;
6. OV-01/02/04/05/06 classificados `TESTE_INCONCLUSIVO`;
7. H-RG-004 classificada `TESTE_INCONCLUSIVO`;
8. nenhuma hipotese promovida;
9. mesmos sete documentos lidos em conteudo; sete documentos de caso/arquitetura apenas hashados;
10. ausencia declarada de comunicacao, conclusao alheia e fonte externa.

## 6. Divergencias

| ID | Natureza | Registro | Impacto |
|---|---|---|---|
| DV-07-01 | D-EXTENSAO | B separa duas inferencias e duas decisoes; A usa uma inferencia/decisao e uma V explicita | baixo/moderado; nao muda o caminho central nem a suspensao |
| DV-07-02 | D-CLASSIFICACAO | A usa `NAO_APLICAVEL_AO_CASO`/`NAO_COLETADO` em varias metricas com denominador zero; B usa `TESTE_INCONCLUSIVO` com denominador `DESCONHECIDO` | moderado; evidencia ambiguidade na precedencia entre codigo de ausencia, estado de metrica e estado experimental |
| DV-07-03 | D-INTERPRETATIVA | H-RG-001: A `NAO_TESTADO`; B `TESTE_INCONCLUSIVO` | alto/material; mesmo bloqueio gerou estados diferentes |
| DV-07-04 | D-INTERPRETATIVA | H-RG-007: A `EVIDENCIA_INSUFICIENTE`; B `TESTE_INCONCLUSIVO` | alto/material; regra de estado nao foi suficientemente deterministica |
| DV-07-05 | D-EXTENSAO | B registra erro inicial de caminho de dois PI-07 corrigido antes da leitura; A nao registra incidente equivalente | baixo; sem impacto nos hashes ou resultado |

Divergencias materiais pre-registradas: 2 (DV-07-03 e DV-07-04). Elas nao foram resolvidas. DV-07-02 nao muda a conclusao global, mas recomenda refinamento da regra de dados ausentes.

## 7. Matriz De Estados

| Objeto | A | B | Acordo |
|---|---|---|---|
| OV-01 | TESTE_INCONCLUSIVO | TESTE_INCONCLUSIVO | SIM |
| OV-02 | TESTE_INCONCLUSIVO | TESTE_INCONCLUSIVO | SIM |
| OV-04 | TESTE_INCONCLUSIVO | TESTE_INCONCLUSIVO | SIM |
| OV-05 | TESTE_INCONCLUSIVO | TESTE_INCONCLUSIVO | SIM |
| OV-06 | TESTE_INCONCLUSIVO | TESTE_INCONCLUSIVO | SIM |
| H-RG-001 | NAO_TESTADO | TESTE_INCONCLUSIVO | NAO |
| H-RG-004 | TESTE_INCONCLUSIVO | TESTE_INCONCLUSIVO | SIM |
| H-RG-007 | EVIDENCIA_INSUFICIENTE | TESTE_INCONCLUSIVO | NAO |

Estados de H-RG-002/003/005/006 nao integram o conjunto principal comum do plano; B os detalhou e A os abrangeu por regra geral. Nao foram forjados pares adicionais.

## 8. Causas Das Divergencias

* a OEG-RG-06 nao foi resolvida, portanto faltou o objeto substantivo que produziria unidades comuns;
* RG-05 distingue codigos de ausencia e estados experimentais, mas o plano nao fixou precedencia quando a suspensao ocorre antes da unidade existir;
* o esquema obrigatorio exigiu cadeia completa, mas nao fixou granularidade minima de I/D/V para uma decisao de suspensao;
* A e B interpretaram de modo diferente `NAO_TESTADO`, `EVIDENCIA_INSUFICIENTE` e `TESTE_INCONCLUSIVO` sob falha de gate.

## 9. Decisao Comparativa Governada

Premissas: acordo sob falha de entrada nao equivale reproducao do metodo aplicado a um caso. Evidencias: hashes A/B, matriz de estados, zero unidades de caso e duas divergencias interpretativas materiais. Inferencia: o gate de suspensao foi aplicado convergentemente, mas a questao da GP-RG-07 nao foi testada. Fundamentacao: nao houve selecao, reconstrucoes nem codificacao compartilhada; comparacao das conclusoes de caso e impossivel. Decisao: atribuir H-RG-004 e OV-06 `TESTE_INCONCLUSIVO`, preservar convergencia procedural e divergencias de estado separadamente. Validacao: a decisao usa estado permitido, nao transforma ausencia em apoio e nao edita A/B.

Alternativas descartadas: considerar a suspensao 100% convergente como apoio a H-RG-004; fornecer retrospectivamente o caminho do anexo; recalcular estados por consenso. Limitacoes: dois avaliadores da mesma plataforma, filesystem comum, declaracoes de independencia sem telemetria de leitura e nenhum caso analisado. Confianca: ALTA nas comparacoes textuais; MEDIA na independencia observavel; NENHUMA para reprodutibilidade documental da GDC-R em caso.

# GP-RG-06 - Resultados Do CP-01

## 1. Limite De Interpretacao

Resultados restritos ao CP-01, ao pacote congelado e a duas passagens do mesmo executor em 18/07/2026. Eles nao validam a metodologia, nao demonstram eficacia, nao sustentam generalidade e nao promovem qualquer hipotese.

## 2. Resultados Por Objeto De Validacao

| OV | Estado permitido | Fundamentacao resumida | Evidencia contraria/limite |
|---|---|---|---|
| OV-01 - coerencia conceitual | `REQUER_REFINAMENTO` | 46/47 unidades tiveram classificacao convergente e E/I permaneceram separadas | a correcao de D-004 possui simultaneamente funcao de revisao, decisao e validacao; a falta de IDs de F/V amplia ambiguidade |
| OV-02 - integridade arquitetural | `PARCIALMENTE_APOIADO` | AP/RI/INV foram aplicaveis e detectaram lacunas bloqueantes, altas e uma ambiguidade material | um caso nao mede sensibilidade/especificidade; a cadeia original ficou `NAO_CONFORME` e nao havia caso inadequado rotulado independentemente |
| OV-04 - rastreabilidade | `APOIADO_NO_CONTEXTO_TESTADO` | 4/4 D tiveram caminho D<-F<-E reconstruido; REV-001 teve predecessor, motivo, sucessor e impacto recuperados | relacoes sao semanticas, nao arestas formalizadas; correcao de D-004 nao possui sucessor inequivoco |
| OV-05 - auditabilidade | `PARCIALMENTE_APOIADO` | fontes, metodos, alternativas, confianca, limites, validacoes e revisao puderam ser inventariados | Manifesto e estados ausentes; E-001 nao resolve ate artefato autonomo no pacote; auditor nao independente |
| OV-06 - reprodutibilidade documental | `TESTE_INCONCLUSIVO` | A/B convergiram em 46/47 unidades e nos quatro caminhos | mesmo executor, memoria entre passagens e uma divergencia material impedem inferencia de reproducao independente |

OV-03, OV-07 e OV-08: `NAO_TESTADO` por exclusao expressa da OEG-RG-06.

## 3. Resultados Por Hipotese

| Hipotese | Estado permitido | Resultado capaz de contrariar observado | Interpretacao limitada |
|---|---|---|---|
| H-RG-001 | `PARCIALMENTE_APOIADO` | nao houve D sem caminho, mas houve dependencia do interprete/ausencia de independencia e falhas estruturais | rastreabilidade/auditabilidade receberam apoio parcial/contextual; reproducao ficou inconclusiva; nada se infere sobre generalidade ou significancia |
| H-RG-002 | `EVIDENCIA_INSUFICIENTE` | E e I foram distinguiveis, mas nao existiu registro misto comparador nem medida de facilitacao | separacao foi observada; efeito causal de facilitar reconstrucao nao foi testado |
| H-RG-003 | `EVIDENCIA_INSUFICIENTE` | a tentativa rejeitada foi recuperada, mas nao houve comparacao com cadeia equivalente sem historico | ha compatibilidade observacional com a hipotese, insuficiente para apoio experimental |
| H-RG-004 | `TESTE_INCONCLUSIVO` | uma divergencia material apareceu e os avaliadores nao eram independentes | o desenho nao satisfaz a condicao minima de dois avaliadores independentes |
| H-RG-007 | `NAO_TESTADO` | so existe um agente/executor observavel | acordo entre duas passagens do mesmo agente nao testa consistencia entre agentes |
| H-RG-010 | `EVIDENCIA_INSUFICIENTE` | a sucessao P-007/P-008 foi recuperada, mas nao havia snapshots/version_ids nem comparador | recuperabilidade pontual observada; aumento atribuivel a snapshots/sucessao nao testado |

Demais hipoteses: `NAO_TESTADO`.

## 4. Resultados Contrarios E Nao Conformidades

1. ausencia de Manifesto original;
2. ausencia de IDs proprios para F, V e arestas;
3. ausencia de perfil declarado antes da cadeia fundadora;
4. estados incompletos para E/I/F/D/Manifesto;
5. confianca nao individualizada em F/V;
6. D-004 sem sucessor formal apos correcao parametrica;
7. uma proveniencia nao resolvida integralmente dentro do pacote;
8. uma divergencia material A/B;
9. independencia experimental ausente.

Esses achados nao foram corrigidos retrospectivamente.

## 5. Decisao Interpretativa Governada

Premissas: estados RG-05 sao obrigatorios e apoio em um caso nao promove hipotese. Evidencias: metricas e nao conformidades congeladas em `RG_06_CP01_EXECUTION.md`. Inferencias: o caso oferece apoio contextual a rastreabilidade, mas revela incompletude formal e nao testa independencia. Fundamentacao: caminhos foram recuperados, enquanto controles de identidade/estado e comparadores faltaram. Decisao: atribuir os estados das secoes 2 e 3 sem extrapolacao. Validacao: todos os OV e hipoteses participantes receberam estado permitido; OV excluidos permaneceram `NAO_TESTADO`.

Alternativas descartadas: declarar a metodologia validada; tratar 97,9% como limiar de sucesso; considerar o relatorio PI-07A referencia independente; promover H-RG-002/H-RG-003 pela observacao de um caso. Confianca: ALTA para contagens documentais; MEDIA para classificacao semantica; BAIXA para causalidade, independencia e generalidade.

## 6. Resultado Global Do Piloto

**`PARCIALMENTE_APOIADO` NO CONTEXTO DOCUMENTAL TESTADO, COM OV-01 `REQUER_REFINAMENTO`, OV-06 `TESTE_INCONCLUSIVO` E CADEIA ORIGINAL `NAO_CONFORME` A CONTROLES FORMAIS POSTERIORES.**

O estado global e apenas sintese descritiva do conjunto; nao substitui os estados separados e nao constitui validacao da GDC-R.

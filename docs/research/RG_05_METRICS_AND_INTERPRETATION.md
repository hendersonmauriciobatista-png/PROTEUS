# GP-RG-05 — Metricas E Regras De Interpretacao

## 1. Objetivo

Definir metricas candidatas, denominadores, regras de dados ausentes e estados de interpretacao para experimentos futuros. Nenhuma metrica foi calculada nesta GP e nenhum limiar representa resultado validado.

## 2. Classificacao Epistemica

Todas as metricas deste documento sao **EXPERIMENTAIS**.

Uma metrica:

* mede aspecto delimitado;
* nao prova hipotese isoladamente;
* nao substitui evidencia qualitativa relevante;
* nao deve ser escolhida pelo resultado observado;
* exige unidade, denominador, versao e limitacao;
* pode falhar como medida do construto e deve ser revisada.

## 3. Distincoes Obrigatorias

| Termo | Funcao |
|---|---|
| metrica | medida observada ou calculada |
| criterio de aceitacao | condicao para gate, conformidade ou completude |
| regra de interpretacao | mapeia conjunto de evidencias para estado de resultado |
| limiar | valor pre-registrado de diferenca, adequacao ou risco |
| Criterio de Avaliacao | hipotese observacional sobre conceito organizador mais amplo; externo a GDC-R |

Recorrencia dessas funcoes sera registrada como evidencia futura, sem promocao conceitual.

## 4. Convencoes De Calculo

* `N_aplicavel`: unidades para as quais a regra se aplica;
* `N_atende`: unidades que atendem a regra;
* `N_total`: unidades observadas antes de exclusoes;
* percentual = `N_atende / N_aplicavel × 100`;
* sempre relatar numerador, denominador e ausentes junto ao percentual;
* denominador zero produz `NAO_APLICAVEL`, nao 0%;
* arredondamento e regra de exclusao devem ser pre-registrados;
* intervalos/incerteza devem acompanhar estimativas quando desenho permitir;
* agregacao entre casos exige justificativa de comparabilidade.

## 5. Metricas Conceituais

| ID | Metrica | Definicao candidata | Unidade | Limite |
|---|---|---|---|---|
| MC-01 | concordancia de tipo | proporcao/acordo corrigido entre classificacoes P/E/I/F/D/V | elemento/avaliador | depende de prevalencia e treinamento |
| MC-02 | matriz de confusao conceitual | contagem de pares de tipos divergentes | elemento | exige referencia ou consenso separado |
| MC-03 | justificativa classificatoria completa | classificacoes com regra/fronteira citada | classificacao | qualidade da justificativa e parcialmente qualitativa |
| MC-04 | casos `NAO_DETERMINADO` | elementos que nao podem ser classificados sem forcar enquadramento | elemento | alto valor pode indicar ambiguidade ou entrada ruim |

## 6. Metricas Estruturais

| ID | Metrica | Formula/registro | Unidade | OV |
|---|---|---|---|---|
| MS-01 | decisoes com fundamentacao rastreavel | D com caminho `D←F←E` / D aplicaveis | Decisao | OV-02/04 |
| MS-02 | inferencias ligadas a evidencias | I com AR-02 ativa / I aplicaveis | Inferencia | OV-01/02 |
| MS-03 | evidencias com proveniencia | E com fonte, metodo, alcance e limites / E | Evidencia | OV-02/05 |
| MS-04 | relacoes proibidas detectadas | contagem por AP-01 a AP-15 e severidade | cadeia/subgrafo | OV-02 |
| MS-05 | invariantes violados | contagem INV/ID por severidade e versao | cadeia | OV-02/03 |
| MS-06 | completude do perfil | requisitos atendidos / requisitos PMG ou PCP aplicaveis | cadeia | OV-02 |
| MS-07 | elementos orfaos | nos sem relacoes obrigatorias / nos aplicaveis | cadeia | OV-02/04 |
| MS-08 | conflitos declarados | conflitos documentados / conflitos do conjunto de referencia | cadeia | OV-02/05 |

MS-04/05 altos podem indicar cadeia ruim ou detector sensivel; interpretacao exige casos intencionalmente conformes e inadequados.

## 7. Metricas Dinamicas

| ID | Metrica | Definicao candidata | Requisito de referencia | OV |
|---|---|---|---|---|
| MD-01 | precisao de propagacao | impactos relevantes previstos / todos os impactos previstos | conjunto independente de impactos esperados | OV-03 |
| MD-02 | cobertura de propagacao | impactos relevantes previstos / impactos relevantes esperados | conjunto independente de impactos esperados | OV-03 |
| MD-03 | transicoes invalidas detectadas | transicoes proibidas detectadas / inseridas ou observadas | cenarios rotulados antes | OV-03 |
| MD-04 | preservacao de historico | predecessores/revisoes reconstruiveis / revisoes aplicaveis | inventario de versoes | OV-03/04 |
| MD-05 | latencia de revisao | diferenca temporal/logica entre nova E e abertura/conclusao de R | relogio ou ordem predefinida | OV-03/07 |
| MD-06 | decisoes reabertas | D que entram em reavaliacao por evento / D vigentes | evento/cadeia | OV-03 |
| MD-07 | propagacao excessiva | elementos reavaliados sem impacto de referencia / reavaliados | conjunto independente | OV-03/07 |
| MD-08 | impacto sem origem | IM sem EV/caminho / IM | cadeia | OV-02/03 |

Precisao/cobertura nao podem ser calculadas com referencia criada pelo mesmo avaliador sem declarar circularidade.

## 8. Metricas De Auditabilidade E Reproducao

| ID | Metrica | Definicao candidata | Unidade | OV |
|---|---|---|---|---|
| MA-01 | sucesso de reconstrucao | componentes/caminhos corretamente reconstruidos segundo referencia independente | tarefa/cadeia | OV-04/05/06 |
| MA-02 | concordancia entre avaliadores | acordo bruto e, quando adequado, kappa/alpha/coeficiente predefinido | item/avaliador | OV-01/06 |
| MA-03 | divergencias materiais | classificacoes/conclusoes que mudam conformidade, caminho ou interpretacao | item/cadeia | OV-06 |
| MA-04 | ambiguidades | pontos marcados ambiguos ou `NAO_DETERMINADO` | item/cadeia | OV-01/05/06 |
| MA-05 | esclarecimentos adicionais | perguntas/fontes extras necessarias alem do pacote congelado | tarefa | OV-04/05/06 |
| MA-06 | tempo de auditoria | tempo ativo por tarefa/unidade | avaliador/cadeia | OV-05/07 |
| MA-07 | erros de proveniencia | atribuicoes incorretas ou nao resolvidas | elemento/cadeia | OV-04/05 |

Se nao houver referencia objetiva, relatar divergencia sem rotular automaticamente um avaliador como errado.

## 9. Metricas Operacionais

| ID | Metrica | Registro | Advertencia |
|---|---|---|---|
| MO-01 | esforco documental | pessoa-tempo/agente-tempo por atividade | agentes IA e humanos nao sao convertidos sem regra |
| MO-02 | tempo de aplicacao | duracao/ordem logica ate marco predefinido | depende de contexto e interrupcoes |
| MO-03 | complexidade percebida | escala/instrumento pre-registrado | percepcao nao substitui estrutura |
| MO-04 | volume de artefatos | itens, campos, arestas, bytes/paginas quando comparaveis | volume nao equivale a qualidade |
| MO-05 | custo de manutencao | esforco por revisao/versao e custodia | janela de observacao necessaria |
| MO-06 | utilidade percebida | escala por papel e justificativa qualitativa | risco de expectativa/novidade |
| MO-07 | carga de esclarecimento | interacoes adicionais por cadeia | pode refletir complexidade do caso |

## 10. Metricas De Generalidade

| ID | Metrica | Definicao candidata | Limite |
|---|---|---|---|
| MG-01 | aplicabilidade do nucleo | requisitos centrais utilizaveis sem redefinicao / requisitos aplicaveis | nao prova universalidade |
| MG-02 | carga de extensao | extensoes de dominio necessarias, por tipo/materialidade | quantidade nao mede impacto sozinha |
| MG-03 | elementos nao aplicaveis | elementos centrais `NAO_APLICAVEL` com justificativa | pode indicar escopo legitimo ou falha |
| MG-04 | diversidade do portfolio | dominios, tipos de agente, temporalidades e fenomenos | diversidade nominal pode ser superficial |
| MG-05 | falhas por contexto | violacoes/inaplicabilidades agrupadas por dominio/agente | amostra pequena limita inferencia |

## 11. Metricas De Versionamento E Proveniencia

| ID | Metrica | Definicao candidata |
|---|---|---|
| MT-01 | recuperacao de snapshot | estados/elementos reconstruidos corretamente / esperados |
| MT-02 | inconsistencias temporais | referencias a versao/estado incorreto por cadeia |
| MT-03 | mapas de sucessao completos | sucessoes com predecessor, motivo e compatibilidade / sucessoes |
| MP-01 | proveniencia preservada em convergencia | origens/versoes reconstruiveis / elementos importados |
| MP-02 | conflitos de origem preservados | conflitos mantidos / conflitos de referencia |

## 12. Metricas De Qualidade Decisoria

H-RG-006 exige metricas externas a qualidade documental.

| ID | Metrica | Regra |
|---|---|---|
| MQ-01 | resultado decisorio de dominio | definido por autoridade de dominio antes do resultado |
| MQ-02 | adequacao a restricoes/objetivos | criterios independentes da presenca de GDC-R |
| MQ-03 | consequencias adversas/retrabalho | janela e classificacao pre-registradas |

Nao existe MQ universal. MS/MA altos nao contam como MQ alta. Se criterio de qualidade independente nao existir, H-RG-006 permanece nao testada naquele caso.

## 13. Dados Ausentes E Excecoes

Codigos obrigatorios:

| Codigo | Significado |
|---|---|
| `AUSENTE` | deveria existir, nao encontrado |
| `NAO_COLETADO` | coleta nao realizada |
| `NAO_APLICAVEL` | regra nao se aplica, com justificativa |
| `PERDIDO` | existiu, indisponivel/corrompido |
| `RETIDO` | existe, acesso limitado por governanca |
| `DESCONHECIDO` | estado nao determinavel |

Imputacao e proibida salvo metodo pre-registrado e analise de sensibilidade. Ausentes devem acompanhar resultados.

## 14. Limiar E Diferenca Pratica

Antes do experimento, para cada metrica principal:

* definir direcao esperada sem declarar sucesso inevitavel;
* definir diferenca minima de interesse ou justificar analise apenas descritiva;
* definir incerteza/intervalo quando aplicavel;
* definir tratamento de empates e resultados mistos;
* definir multiplicidade de metricas;
* definir prioridade primaria/secundaria/exploratoria;
* definir condicoes contrarias.

Limiar nao pode ser escolhido olhando os resultados. Ausencia de base para limiar torna o primeiro piloto exploratorio e impede alegacao “significativamente melhor”.

## 15. Estados De Interpretacao

| Estado | Condicao |
|---|---|
| `NAO_TESTADO` | desenho/caso nao avaliou a hipotese/componente |
| `TESTE_INCONCLUSIVO` | dados, comparabilidade ou incerteza impedem interpretacao |
| `PARCIALMENTE_APOIADO` | parte predefinida recebe apoio e parte nao/contraria |
| `APOIADO_NO_CONTEXTO_TESTADO` | condicoes de apoio pre-registradas atendidas naquele contexto, sem bloqueio contrario |
| `CONTRARIADO_NO_CONTEXTO_TESTADO` | condicoes contrarias pre-registradas atendidas naquele contexto |
| `REQUER_REFINAMENTO` | construto/regra/medida demonstrou ambiguidade ou escopo inadequado |
| `NAO_APLICAVEL_AO_CASO` | hipotese/componente nao se aplica, com justificativa |
| `EVIDENCIA_INSUFICIENTE` | observacoes insuficientes; nao equivale a apoio ou contradicao |

“Apoiado” nunca significa validado universalmente. “Contrariado” em um caso nao exige rejeicao geral automatica.

## 16. Regra De Interpretacao Por Hipotese

Para atribuir estado:

1. confirmar versao e pre-registro;
2. verificar elegibilidade/comparabilidade;
3. verificar desvios;
4. reunir metricas primarias e evidencia qualitativa contraria;
5. aplicar condicoes de apoio/contradicao pre-registradas;
6. declarar incerteza e dados ausentes;
7. limitar a caso, fase, dominio e agente;
8. registrar analises alternativas razoaveis;
9. separar resultado confirmatorio de exploratorio;
10. impedir promocao automatica.

## 17. Concordancia Entre Avaliadores

Pre-registrar:

* unidade de codificacao;
* categorias;
* se multiplas classificacoes sao permitidas;
* coeficiente adequado ao nivel de medida;
* tratamento de prevalencia e categorias raras;
* limiar contextual e justificativa;
* processo de consenso separado do valor independente;
* dados individuais preservados.

Consenso posterior nao substitui concordancia independente inicial.

## 18. Comparacao Entre Grupos

Relatar:

* valores por grupo e caso;
* diferencas absolutas/relativas quando adequadas;
* incerteza;
* nao equivalencias;
* custo/esforco;
* efeitos adversos;
* resultados que favorecem o convencional;
* analises de sensibilidade pre-registradas.

Nao criar escore composto global sem formula, pesos e interpretacao pre-registrados. Um escore nao pode ocultar falha bloqueante.

## 19. Criterios De Aceitacao Experimentais

Criterios de gate podem incluir:

* pacote completo;
* denominadores resolvidos;
* independencia minima;
* ausencia de desvio D3/D4;
* confiabilidade do instrumento;
* cobertura de casos prevista.

Atender gate permite interpretar; nao confirma hipotese.

## 20. Relatorio Minimo De Metricas

Para cada metrica:

* ID/nome;
* OV/QE/H;
* definicao e versao;
* unidade;
* numerador/denominador;
* ausentes;
* valor/incerteza;
* grupo/caso/agente;
* desvio;
* limitacao;
* interpretacao permitida e proibida.

## 21. Limitacoes

* metricas nao foram pilotadas;
* propriedades de medida desconhecidas;
* limiares nao calibrados;
* referencias independentes podem divergir;
* amostras pequenas limitam estatistica;
* custo de coleta pode influenciar completude;
* metricas quantitativas podem induzir falsa precisao;
* percepcao sofre expectativa e desejabilidade;
* DGA-01 nao esta comprovada.

## 22. Estado Final

**METRICAS E INTERPRETACAO FORMALIZADAS COMO CANDIDATAS EXPERIMENTAIS — NENHUM VALOR CALCULADO**

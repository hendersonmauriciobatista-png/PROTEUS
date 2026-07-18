# GP-RG-05 — Vieses, Ameacas A Validade E Mitigacoes

## 1. Objetivo

Definir ameacas que futuros experimentos GDC-R devem pre-registrar, monitorar e relatar. Medidas propostas reduzem exposicao; nenhuma e declarada capaz de eliminar completamente o risco.

## 2. Modelo De Registro

Cada ameaca futura deve conter:

* `threat_id`;
* categoria;
* descricao contextualizada;
* causa/mecanismo observavel;
* fase afetada;
* probabilidade e impacto pre-experimento;
* sinal de deteccao;
* mitigacao planejada;
* incidente observado;
* risco residual;
* impacto sobre interpretacao;
* autoridade responsavel.

Escalas de probabilidade/impacto devem ser pre-registradas. Pontuacao nao substitui descricao.

## 3. Ameacas De Construto

| ID | Ameaca | Efeito possivel | Sinais | Mitigacoes candidatas | Risco residual |
|---|---|---|---|---|---|
| TV-01 | ambiguidade semantica | P/E/I/F/D/V classificados inconsistentemente | baixa concordancia, muitos `NAO_DETERMINADO` | treinamento versionado; exemplos/contraexemplos; dupla codificacao | definicoes podem continuar ambiguas |
| TV-02 | metrica nao representa propriedade | falsa conclusao sobre rastreabilidade/utilidade | metrica diverge de auditoria qualitativa | triangulacao; validade de conteudo por revisores; relatar dimensoes separadas | construtos abstratos nunca sao capturados integralmente |
| TV-03 | documentacao confundida com qualidade decisoria | apoio indevido a H-RG-006 | MS/MA melhora sem MQ externa | criterio de qualidade independente; separar OV-07 de resultado decisorio | contrafactual permanece dificil |
| TV-04 | volume confundido com completude | incentivo a documentacao performativa | mais artefatos sem caminhos/uso | usar integridade/denominadores; auditar orfaos; medir custo | completude tambem pode ser inflada |
| TV-05 | criterio/metricas/interpretacao confundidos | metas pos-hoc ou circularidade | limiar derivado do resultado | distincoes formais; pre-registro; auditoria de versoes | fronteira de `Criterio de Avaliacao` segue experimental |

## 4. Ameacas De Validade Interna

| ID | Ameaca | Efeito possivel | Sinais | Mitigacoes candidatas | Risco residual |
|---|---|---|---|---|---|
| TV-06 | viés de confirmacao | selecao/interpretacao favorece GDC-R | omissao de dado contrario; justificativas assimetricas | pre-registro; avaliador cego quando viavel; analise contraria obrigatoria | autores conhecem a teoria |
| TV-07 | selecao favoravel de casos | desempenho superestimado | apenas casos maduros/bem-sucedidos | registro do universo; criterios prévios; incluir falhas/conflitos | acesso pode limitar universo |
| TV-08 | dependencia do pesquisador | resultado depende de quem criou o modelo | alta divergencia com externos | avaliadores independentes; papeis separados; dados individuais | recursos podem impedir independencia plena |
| TV-09 | circularidade | GDC-R avaliada por referencia produzida pela propria GDC-R | conjunto de verdade criado pelo mesmo avaliador | referencia independente/painel; cenarios rotulados antes; auditoria | referencia tambem pode divergir |
| TV-10 | conhecimento previo/contaminacao | reconstrucao parece melhor por familiaridade | avaliador conhece decisao/resultado | pacotes cegos; declarar conhecimento; ordem contrabalanceada | cegamento completo pode ser impossivel |
| TV-11 | efeito de treinamento | melhora atribuida a GDC-R vem de treinamento | grupos recebem instrucao desigual | treinamento equivalente; medir experiencia; desenho cruzado quando viavel | aprendizagem transfere entre condicoes |
| TV-12 | maturacao/historia | mudancas externas afetam prospectivo | eventos fora do protocolo | log temporal; janela delimitada; grupo comparavel | decisao real nao e isolavel por completo |
| TV-13 | instrumentacao | mudanca de instrumento altera medida | versoes diferentes no mesmo estudo | congelar versao; calibrar antes; emenda governada | instrumento inicial pode ser inadequado |
| TV-14 | expectativa/novidade | utilidade percebida inflada | percepcao alta sem evidencia estrutural | separar MO-06; avaliacao tardia; perguntas neutras | percepcao continua subjetiva |

## 5. Ameacas Retrospectivas

| ID | Ameaca | Efeito | Mitigacoes candidatas | Limite residual |
|---|---|---|---|---|
| TV-15 | reconstrucao retrospectiva | elos criados com conhecimento do resultado | avaliador cego; distinguir registro original de reconstruido; marcar inferencias retrospectivas | documentos nao nasceram sob GDC-R |
| TV-16 | viés de sobrevivencia documental | apenas artefatos preservados entram | inventariar lacunas, descartes e fontes ausentes | acervo perdido nao pode ser recuperado por inferencia |
| TV-17 | autoridade retrospectiva | significado atual imposto ao registro historico | preservar terminologia/versao original; nao reescrever fontes | contexto tacito pode faltar |

Fase A nunca sustenta sozinha eficacia prospectiva.

## 6. Ameacas De Comparacao

| ID | Ameaca | Efeito | Sinais | Mitigacoes candidatas | Risco residual |
|---|---|---|---|---|---|
| TV-18 | casos/grupos nao equivalentes | diferenca atribuida a GDC-R indevidamente | complexidade, agentes ou entradas diferentes | pareamento; estratificacao; comparacao descritiva; declarar nao equivalencia | equivalencia perfeita rara |
| TV-19 | comparador artificialmente fraco | superioridade trivial | grupo convencional sem pratica realista | usar pratica vigente autentica; revisar comparador externamente | variabilidade da pratica convencional |
| TV-20 | contaminacao entre grupos | metodo GDC-R influencia convencional | mesmos agentes/ordem | separar equipes; washout; ordem pre-registrada | conhecimento nao pode ser desaprendido |
| TV-21 | esforço desigual | mais tempo produz melhor documentacao | MO-01/MO-02 muito diferentes | limitar/medir recursos; analisar custo-beneficio | igualdade de esforço pode prejudicar validade ecologica |

## 7. Ameacas De Validade Externa

| ID | Ameaca | Efeito | Mitigacoes candidatas | Risco residual |
|---|---|---|---|---|
| TV-22 | generalizacao indevida | resultado local declarado universal | estados “no contexto”; portfolio multidominio; replicacao | nenhum portfolio finito prova universalidade |
| TV-23 | dependencia PROTEUS/ICFACTORY | DGA-01 aparente, nao real | caso externo; nucleo comum; extensoes separadas | acesso externo pode ser limitado |
| TV-24 | dependencia tecnologica | resultado depende de ferramenta/modelo | registrar tecnologia; variar quando possivel; procedimento neutro | ferramentas mudam |
| TV-25 | tipo de agente limitado | conclusao sobre humanos/IA alem da amostra | diversidade e estratificacao por agente | representatividade permanece limitada |
| TV-26 | decisao artificial | desempenho de exercicio nao transfere a decisao real | relevancia real; fases prospectivas | controle e realismo entram em tensao |
| TV-27 | escala | grafos pequenos ocultam custo/complexidade | variar C1-C4; medir MO | pilotos iniciais provavelmente pequenos |

## 8. Ameacas De Validade De Conclusao

| ID | Ameaca | Efeito | Mitigacoes candidatas | Risco residual |
|---|---|---|---|---|
| TV-28 | amostra insuficiente | incerteza alta tratada como ausencia/apoio | justificar amostra por OV; intervalos; estado inconclusivo | recursos limitam tamanho |
| TV-29 | multiplicidade de metricas | achado oportunista | metricas primarias predefinidas; relatar todas; correcao quando adequada | dependencia entre metricas |
| TV-30 | limiar pos-hoc | “significancia” escolhida apos resultado | diferenca pratica pre-registrada; piloto exploratorio | limiar inicial pode ser arbitrario |
| TV-31 | falsa precisao | numeros transmitem certeza indevida | numerador/denominador, incerteza e narrativa | leitores podem superinterpretar |
| TV-32 | dados ausentes | vies ou denominador incorreto | codigos de ausencia; sensibilidade; nao imputar sem plano | mecanismo de ausencia pode ser desconhecido |
| TV-33 | agregacao inadequada | divergencias entre dominios ocultas | relatar por caso/dominio antes de agregar | amostras por estrato pequenas |

## 9. Ameacas De Agentes De IA

| ID | Ameaca | Efeito | Mitigacoes candidatas | Risco residual |
|---|---|---|---|---|
| TV-34 | influencia do prompt | classificacao atribuida ao modelo, mas causada pela instrucao | versionar prompts; variar apenas se pre-registrado | interacao prompt/modelo complexa |
| TV-35 | nao independencia de avaliacoes | agentes compartilham modelo/contexto/dados | declarar infraestrutura; separar sessoes; usar tipos distintos | treinamento comum permanece desconhecido |
| TV-36 | variabilidade/nondeterminismo | baixa reproducao | registrar configuracoes; repeticoes predefinidas | detalhes internos podem nao ser observaveis |
| TV-37 | conhecimento externo nao controlado | fontes fora do pacote influenciam resultado | restringir ferramentas; registrar acesso; auditar citacoes | isolamento pode ser imperfeito |
| TV-38 | autoridade indevida | resposta de IA tratada como validacao | revisao humana; papel limitado; evidencias observaveis | automacao pode induzir deferencia |
| TV-39 | inferencia sobre estado interno | explicacao verbal confundida com mecanismo real | proibir conclusao interna; analisar apenas saida/artefato | linguagem antropomorfica persiste |
| TV-40 | mudanca de modelo/servico | comparacao temporal invalida | registrar versao/data; congelar quando possivel; tratar como fator | provedores podem atualizar silenciosamente |

## 10. Ameacas Operacionais, Eticas E De Custodia

| ID | Ameaca | Efeito | Mitigacoes candidatas |
|---|---|---|---|
| TV-41 | sobrecarga documental | abandono, atalhos ou dados performativos | PMG/PCP, medir custo, amostrar, simplificar somente por revisao |
| TV-42 | confidencialidade/propriedade | dano, uso nao autorizado | classificacao, autorizacao, minimizacao, acesso controlado |
| TV-43 | perda/corrupcao | cadeia irrecuperavel | hashes, backup/custodia, manifestos, verificacao |
| TV-44 | incentivo adverso | agentes ocultam falhas para parecer conformes | separar avaliacao de punicao, preservar negativos, auditoria |
| TV-45 | risco humano/material | experimento interfere em decisao de alto impacto | limitar piloto, autoridade humana, criterios de parada |
| TV-46 | documentacao seletiva | narrativa mais coerente que evidencia | inventario de entradas, registros brutos, auditoria DG-09 |

## 11. Ameacas A DGA-01

| ID | Ameaca | Teste documental | Mitigacao candidata |
|---|---|---|---|
| TDGA-01 | campo/procedimento exige entidade de projeto | remover nomes do caso e verificar executabilidade | nucleo neutro e extensao separada |
| TDGA-02 | portfolio apenas interno | contar dominios/agentes/origens | incluir CP-05 externo antes de alegacao |
| TDGA-03 | extensao redefine conceito central | comparar schema/instrumento com RG-02/03 | classificar nao conformidade ou revisar teoria |
| TDGA-04 | resultado de uma tecnologia e generalizado | estratificar por tecnologia/agente | limitar conclusao e replicar |
| TDGA-05 | dominio nominalmente diferente, estruturalmente igual | auditar diversidade substantiva | criterios de diversidade pre-registrados |

DGA-01 permanece propriedade de desenho ate evidencia multidominio adequada.

## 12. Matriz Ameaca × Fase

| Fase | Ameacas prioritarias |
|---|---|
| A retrospectiva | TV-06/07/10/15/16/17/22 |
| B prospectiva | TV-08/11/12/13/41/45 |
| C independente | TV-01/08/10/20/34-40 |
| D multidominio | TV-18/22-27/33 e TDGA |
| E monitoramento | TV-13/24/40/42/45 e formalizacao insuficiente de indicadores |

## 13. Registro De Incidentes E Desvios

Quando ameaca se materializar:

1. registrar evento sem alterar dado bruto;
2. classificar desvio D1-D4;
3. suspender quando risco exigir;
4. avaliar componentes afetados;
5. limitar ou reclassificar analise;
6. preservar versao/pre-registro anterior;
7. registrar alternativa de interpretacao;
8. atualizar risco residual;
9. incluir no relatorio final.

## 14. Independencia E Conflitos De Interesse

Declarar para cada agente:

* autoria/participacao na GDC-R;
* relacao com caso/projeto;
* conhecimento do resultado;
* incentivo institucional/pessoal;
* acesso a outros avaliadores;
* dependencia tecnologica comum;
* papeis acumulados.

Independencia deve ser descrita por dimensao, nao como rotulo binario.

## 15. Analise De Sensibilidade

Quando pre-registrada e viavel:

* recalcular excluindo casos de alto risco;
* variar tratamento de ausentes;
* comparar limiares justificados previamente;
* separar agentes/domínios;
* comparar com/sem desvios D2;
* relatar se interpretacao muda.

Analise criada apos resultados e exploratoria.

## 16. Criterio Para Resultado Comprometido

Classificar `EXPERIMENTO_COMPROMETIDO` quando:

* D3/D4 afeta metrica/hipotese primaria;
* pre-registro inexistente ou materialmente alterado pos-resultado;
* dados brutos essenciais nao sao auditaveis;
* comparador foi redefinido apos resultado;
* confidencialidade impede verificacao essencial;
* independencia alegada era falsa/materialmente comprometida.

Dados podem permanecer como evidencia exploratoria, com limites; nao devem ser apagados nem apresentados como confirmatorios.

## 17. Limitacoes Desta Analise

* registro e baseado no bloco teorico, sem incidentes reais;
* probabilidade/impacto nao foram calibrados;
* lista pode ser incompleta;
* mitigacoes podem introduzir novas ameacas;
* independencia plena pode ser inviavel;
* requisitos eticos/juridicos dependem de jurisdicao/caso futuro;
* nao foi realizada revisao externa.

## 18. Estado Final

**AMEACAS E MITIGACOES FORMALIZADAS — RISCO RESIDUAL OBRIGATORIO — NENHUM EXPERIMENTO AVALIADO**

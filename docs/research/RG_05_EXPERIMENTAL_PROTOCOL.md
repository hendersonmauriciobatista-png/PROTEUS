# GP-RG-05 — Protocolo Experimental De Validacao Da GDC-R

## 1. Identidade E Estado

| Campo | Registro |
|---|---|
| Identificador | GP-RG-05 |
| Natureza | pesquisa documental e planejamento experimental |
| Estado | PROTOCOLO FORMALIZADO — NENHUM EXPERIMENTO EXECUTADO |
| Objeto | futura avaliacao empirica da GDC-R e de suas hipoteses |
| Unidade principal | cadeia de decisao versionada |
| Proxima execucao possivel | GP-RG-06, somente mediante autorizacao e pre-registro proprios |
| Generalidade | DGA-01 preservada; ainda nao comprovada |
| Conceito experimental | `Criterio de Avaliacao` permanece hipotese observacional externa |

Este protocolo governa validacoes futuras. Ele nao apresenta resultados, nao escolhe definitivamente casos, nao aplica GDC-R, nao promove hipoteses e nao declara eficacia.

## 2. Objetivo

Definir objetos de validacao, questoes, unidades, fases, controles, evidencias, papeis, pre-registro, mudancas e regras de interpretacao suficientes para que experimentos futuros nao inventem procedimentos apos observar resultados.

## 3. Autoridades

| ID | Artefato | Autoridade exercida | Limitacao |
|---|---|---|---|
| E-RG05-001 | `RG_01_RESEARCH_CONSTITUTION.md` | objeto, limites, H-RG-001 a H-RG-007 e principios | bloco teorico |
| E-RG05-002 | `RG_02_CONCEPTUAL_MODEL.md` | definicoes e regras conceituais | validade multidominio pendente |
| E-RG05-003 | `RG_02_SEMANTIC_MATRIX.md` | fronteiras e ambiguidades | concordancia independente nao testada |
| E-RG05-004 | `RG_03_ARCHITECTURE.md` | GDC-R, relacoes, proibicoes, integridade e propriedades | arquitetura nao testada |
| E-RG05-005 | `RG_03_INVARIANTS.md` | INV-01 a INV-31 | severidades nao calibradas |
| E-RG05-006 | `RG_04_DYNAMIC_MODEL.md` | estados, versoes, propriedades e H-RG-008 a H-RG-011 | dinamica nao testada |
| E-RG05-007 | `RG_04_STATE_MACHINE.md` | transicoes permitidas/proibidas | maquina documental |
| E-RG05-008 | `RG_04_PROPAGATION_MODEL.md` | dependencias, impacto e propagacao | calibracao pendente |
| E-RG05-009 | `RG_04_CLOSURE_REPORT.md` | bloqueio anterior e alternativas | anterior a deliberação atual |
| E-RG05-010 | Deliberacao Formal do Escopo GP-RG-05 | resolve RG-05 como Protocolo Experimental | nao autoriza execucao |

## 4. Principios Experimentais

1. **Pre-registro:** questoes, casos, versao, procedimentos, metricas e criterios antes dos resultados.
2. **Separacao epistemica:** observacao, inferencia, interpretacao e decisao experimental permanecem distintas.
3. **Nao superioridade presumida:** GDC-R e grupo convencional sao tratados simetricamente.
4. **Evidencia contraria:** o desenho deve permitir enfraquecimento ou rejeicao.
5. **Resultados negativos preservados:** falhas e inconclusoes integram o acervo.
6. **Comparabilidade declarada:** diferencas entre casos/grupos nunca sao ocultadas.
7. **Independencia avaliativa:** conflitos de papel e conhecimento previo sao registrados.
8. **Versionamento:** protocolo, instrumentos e desvios sao imutaveis por versao.
9. **Proporcionalidade:** custo e rigor acompanham risco, sem omitir elemento relevante.
10. **DGA-01:** procedimentos centrais nao dependem de dominio, projeto, tecnologia ou tipo de agente.
11. **Nao acesso interno:** avaliacao usa somente artefatos observaveis.
12. **Generalizacao limitada:** conclusao nunca excede casos, agentes e dominios observados.

## 5. Objetos De Validacao

| ID | Objeto | Pergunta central | Evidencia futura minima | Resultado que nao pode ser inferido automaticamente |
|---|---|---|---|---|
| OV-01 | Coerencia conceitual | P/E/I/F/D/V sao identificados e diferenciados consistentemente? | classificacoes independentes, justificativas e divergencias | ontologia universal ou ausencia de ambiguidade |
| OV-02 | Integridade arquitetural | relacoes, proibicoes, regras e invariantes sao aplicaveis/verificaveis? | auditoria de cadeias conformes e deliberadamente inadequadas | completude universal da arquitetura |
| OV-03 | Comportamento dinamico | estados, transicoes, revisoes, conflitos e propagacao representam evolucao observavel? | snapshots, eventos, impactos e reavaliacoes esperadas/observadas | previsao perfeita de toda mudanca |
| OV-04 | Rastreabilidade | uma D pode ser reconstruida ate origens e revisoes? | tarefas cegas de reconstrucao e caminhos documentais | correcao ou qualidade da D |
| OV-05 | Auditabilidade | terceiro identifica fontes, I, limites, alternativas e mudancas? | auditoria independente com registro de lacunas | certificacao externa geral |
| OV-06 | Reprodutibilidade documental | avaliadores produzem analises suficientemente convergentes? | dois ou mais avaliadores, mesmos artefatos/regras, concordancia e divergencias | identidade de julgamentos ou mecanismos internos |
| OV-07 | Utilidade operacional | GDC-R melhora organizacao, explicitacao e controle documental? | comparacao, custo, elementos implicitos, revisoes e percepcao separada | eficacia decisoria geral |
| OV-08 | Generalidade DGA-01 | nucleo permanece aplicavel ao mudar dominio, projeto, tecnologia ou agente? | portfolio multidominio e multiagente | generalidade por um caso ou dominio |

## 6. Questoes Experimentais Obrigatorias

| ID | Questao | OV relacionados |
|---|---|---|
| QE-01 | Os seis conceitos fundamentais sao distinguiveis em aplicacoes reais? | OV-01 |
| QE-02 | Uma decisao pode ser reconstruida a partir dos elementos documentados? | OV-04/05 |
| QE-03 | Relacoes proibidas detectam cadeias estruturalmente inadequadas? | OV-02 |
| QE-04 | Invariantes identificam perda de integridade ou rastreabilidade? | OV-02/04 |
| QE-05 | Propagacao indica corretamente elementos a reavaliar apos alteracao? | OV-03 |
| QE-06 | Avaliadores independentes classificam os mesmos elementos convergentemente? | OV-01/06 |
| QE-07 | GDC-R reduz elementos implicitos ou nao fundamentados? | OV-07 |
| QE-08 | A arquitetura permanece aplicavel quando dominio, agente ou tipo de D muda? | OV-08 |
| QE-09 | Quais componentes produzem maior custo documental? | OV-07 |
| QE-10 | Quais componentes apresentam ambiguidade ou baixa aplicabilidade? | OV-01/03/07/08 |

Questoes adicionais exigem adendo pre-registrado e nao substituem as obrigatorias.

## 7. Unidades De Analise

### 7.1 Unidade Principal

**Cadeia de decisao versionada**, identificada por Manifesto, versao e snapshot.

Campos experimentais requeridos quando aplicaveis:

* identificador;
* dominio e contexto;
* agente(s) e papeis;
* P/E/I/F/D/V;
* relacoes;
* estados e transicoes;
* revisoes e conflitos;
* versoes e compatibilidade;
* limitacoes;
* resultado observado;
* classe de conformidade;
* instrumento e versao do protocolo.

### 7.2 Unidades Secundarias

* elemento individual;
* relacao;
* subgrafo;
* Registro de Revisao;
* ciclo completo;
* snapshot;
* comparacao entre versoes;
* avaliacao individual;
* par ou conjunto de casos comparados.

Analises devem declarar unidade e denominador. Nao e permitido misturar medidas de elementos, cadeias e avaliadores sem explicitar agregacao.

## 8. Estrategia Experimental Incremental

### Fase A — Reconstrucao Retrospectiva

Objetivos:

* testar identificacao de elementos;
* reconstruir cadeias;
* avaliar rastreabilidade;
* detectar lacunas.

Entrada: decisao concluida e acervo anterior suficiente.

Controle: avaliadores recebem conjunto de artefatos congelado; conhecimento externo permitido/proibido e pre-registrado.

Saida: cadeias reconstruidas, lacunas, ambiguidades, tempo/esforco e divergencias.

Limite obrigatorio: retrospectiva nao prova eficacia prospectiva, pois documentos nao nasceram sob GDC-R.

### Fase B — Aplicacao Prospectiva Controlada

Objetivos:

* observar cadeia em formacao;
* registrar estados/transicoes;
* testar propagacao;
* observar revisoes/conflitos.

Entrada: decisao ainda nao concluida, escopo controlavel e autorizacao propria.

Controle: versao GDC-R, papeis, eventos observaveis, instrumentos e criterios congelados antes da decisao.

Saida: snapshots, eventos, IM, revisoes, D/V e desvios.

### Fase C — Avaliacao Independente

Objetivos:

* medir convergencia;
* identificar ambiguidades;
* testar reproducao documental;
* detectar dependencia do interprete.

Entrada: mesmo pacote documental para dois ou mais avaliadores.

Controle: independencia, ordem, treinamento, prompts e comunicacao entre avaliadores pre-registrados.

Saida: classificacoes individuais antes de consenso, concordancia, divergencias e justificativas.

### Fase D — Comparacao Entre Dominios

Objetivos:

* testar variacao de aplicabilidade;
* localizar dependencias de contexto;
* avaliar progressivamente DGA-01.

Entrada: pelo menos dois dominios substantivamente distintos; um unico dominio nunca atende OV-08.

Portfolio candidato: software, auditoria, governanca de projeto, editorial, operacional, monitoramento e caso externo.

Controle: nucleo/instrumentos comuns e extensoes de dominio identificadas separadamente.

### Fase E — Monitoramento ICFACTORY

Objetivo prospectivo: avaliar GDC-R na fundamentacao de alertas e recomendacoes de maturidade.

Bloqueio: nao pode iniciar sem formalizacao propria dos indicadores, limites, fontes e governanca da EUREKA de monitoramento.

Esta fase nao e pre-requisito para preservar DGA-01 e nao pode ser usada como unica evidencia de generalidade.

## 9. Ordem E Gates Das Fases

Fases nao precisam ocorrer todas no mesmo caso, mas a passagem deve respeitar:

| Gate | Requisito | Efeito da falha |
|---|---|---|
| GX-00 | autorizacao formal da GP/caso | nao iniciar |
| GX-01 | pergunta, OV e hipoteses identificados | nao iniciar |
| GX-02 | caso elegivel e conflitos de interesse registrados | nao iniciar |
| GX-03 | pacote de entrada e versao GDC-R congelados | nao iniciar |
| GX-04 | pre-registro completo e imutavel publicado | nao iniciar |
| GX-05 | confidencialidade, propriedade e riscos aprovados | nao iniciar |
| GX-06 | papeis, independencia e treinamento declarados | nao iniciar |
| GX-07 | instrumentos/metricas testaveis e denominadores definidos | nao iniciar coleta |
| GX-08 | desvios e incidentes registrados durante execucao | suspender analise ate classificar impacto |
| GX-09 | dados/resultados congelados antes da interpretacao conjunta | nao consolidar analise |
| GX-10 | analises contrarias, ausencias e limitacoes registradas | nao emitir parecer |
| GX-11 | auditoria de encerramento e custodia | experimento permanece aberto |

GP-RG-05 define os gates; nao os executa contra casos.

## 10. Grupos De Comparacao

### Grupo GDC-R

Decisao documentada explicitamente conforme versao pre-registrada da GDC-R.

### Grupo Convencional

Decisao equivalente documentada por pratica tradicional ou sem estrutura GDC-R explicita.

### Regras De Comparabilidade

Pre-registrar:

* dominio e tipo de decisao;
* complexidade e impacto;
* volume/qualidade inicial da documentacao;
* experiencia dos agentes;
* tempo e recursos disponiveis;
* retrospectiva ou prospectiva;
* informacao acessivel;
* diferencas inevitaveis.

Se equivalencia suficiente nao existir, classificar como comparacao descritiva, nao causal. Ausencia de grupo e limitacao, nao permissao para presumir superioridade.

## 11. Pacote Experimental Obrigatorio

Cada experimento futuro deve produzir:

1. termo de autorizacao;
2. pre-registro versionado;
3. ficha do caso e justificativa de selecao;
4. inventario/hashes dos documentos de entrada;
5. versao GDC-R e instrumentos;
6. matriz de papeis/agentes;
7. registros brutos individuais;
8. cadeia(s) produzida(s);
9. log de eventos, desvios e revisoes;
10. dataset de metricas com denominadores;
11. analise individual antes de consenso;
12. matriz de divergencias;
13. interpretacao conforme estados permitidos;
14. ameacas e limitacoes atualizadas;
15. relatorio de encerramento;
16. manifestos de custodia, acesso e redacao.

## 12. Pre-Registro

Antes de qualquer contato com resultados, registrar:

| Bloco | Conteudo obrigatorio |
|---|---|
| identidade | experimento, responsavel, versao e autorizacao |
| objetivo | OV, QE e hipoteses |
| caso | candidato, selecao, inclusao/exclusao e justificativa |
| entradas | documentos, versoes, hashes, informacao externa permitida |
| desenho | fase, grupo, unidade, amostra e sequencia |
| agentes | papeis, independencia, treinamento e conflitos |
| procedimento | passos replicaveis e instrumentos |
| metricas | definicoes, denominadores, ausentes e limiares/contexto |
| interpretacao | estados possiveis e evidencias favoraveis/contrarias |
| ameacas | riscos conhecidos e mitigacoes |
| mudancas | regra de emenda, parada e desvio |
| custodia | confidencialidade, acesso, retencao e publicacao |

### 12.1 Emendas

Emenda apos pre-registro:

* recebe versao e motivo;
* preserva texto anterior;
* declara se ocorreu antes ou depois de qualquer resultado conhecido;
* classifica impacto (`SEM_IMPACTO`, `INTERPRETACAO_LIMITADA`, `ANALISE_EXPLORATORIA` ou `EXPERIMENTO_COMPROMETIDO`);
* nunca e aplicada retroativamente sem identificacao.

Analise adicionada apos resultados e rotulada **EXPLORATORIA POS-HOC**.

## 13. Governanca Dos Agentes

| Papel | Responsabilidade | Incompatibilidade/controle |
|---|---|---|
| agente decisor | realiza ou autoriza a decisao do caso | nao valida sozinho a eficacia do proprio processo |
| agente documentador | registra cadeia e eventos | suas escolhas de classificacao sao auditaveis |
| agente avaliador | classifica e mede conforme instrumentos | deve registrar conhecimento previo e independencia |
| agente validador | compara resultado esperado/observado | nao confundir com avaliador da metodologia |
| agente auditor | examina protocolo, dados e rastreabilidade | preferir independencia dos demais papeis |
| coordenador experimental | controla versoes, gates e desvios | nao altera criterios apos resultados |

Acumulo de papeis e permitido somente se inevitavel, declarado e tratado como ameaca.

### 13.1 Agentes De IA

Registrar:

* sistema/modelo e versao quando observavel;
* papel;
* documentos fornecidos;
* instrucoes/prompts relevantes e versoes;
* ferramentas e acesso externo;
* configuracoes observaveis;
* limitacoes e variabilidade;
* revisao humana;
* comunicacao/contaminacao entre avaliacoes;
* justificativa de independencia ou sua ausencia.

Resposta verbal isolada de IA nao e validacao cientifica. Nao se infere raciocinio interno.

## 14. Requisitos De Evidencia

Evidencia experimental deve possuir:

* origem e metodo;
* versao e integridade;
* unidade/denominador;
* momento relativo ao pre-registro;
* agente coletor;
* alcance e limitacoes;
* transformacoes aplicadas;
* possibilidade de auditoria;
* status de confidencialidade.

Ausencia de dado e codificada como `AUSENTE`, `NAO_COLETADO`, `NAO_APLICAVEL`, `PERDIDO` ou `RETIDO`, nunca como zero ou confirmacao.

## 15. Analise E Interpretacao

O plano detalhado esta em `RG_05_METRICS_AND_INTERPRETATION.md`.

Regras centrais:

* preservar dados brutos e analises individuais;
* calcular metricas somente com denominadores declarados;
* separar analise pre-registrada de exploratoria;
* nao usar percepcao como substituto de integridade estrutural;
* nao agregar dominios incompatíveis sem justificativa;
* relatar efeitos, incerteza, divergencias e ausencias;
* usar estados graduais, nao binario validada/refutada;
* limitar conclusao ao contexto observado.

## 16. Criterios De Parada E Suspensao

Suspender futura execucao quando:

* confidencialidade/propriedade estiver em risco;
* autorizacao ou consentimento aplicavel estiver ausente;
* pre-registro/instrumento tiver mudanca material nao governada;
* independencia estiver comprometida sem possibilidade de analise;
* dados de entrada forem corrompidos/incompletos alem do previsto;
* conflito de interesse material surgir;
* versao GDC-R nao puder ser determinada;
* resultado adverso de risco exigir autoridade humana.

Parada nao apaga dados. O experimento termina como suspenso, inconclusivo ou comprometido, com fundamentacao.

## 17. Controle De Desvios

| Classe | Definicao | Tratamento |
|---|---|---|
| `D0` | sem desvio | seguir plano |
| `D1` | operacional menor, sem impacto plausivel | registrar e justificar |
| `D2` | pode afetar metrica/interpretacao | limitar analise e executar sensibilidade quando predefinida |
| `D3` | altera caso, instrumento, grupo ou criterio | resultado confirmatorio invalidado; manter como exploratorio/inconclusivo |
| `D4` | viola etica, confidencialidade ou integridade | suspender, isolar material e acionar governanca |

## 18. Criterio De Avaliacao — Tratamento Experimental

Status: **HIPOTESE OBSERVACIONAL EXTERNA A CADEIA OFICIAL**.

Distincoes:

* **metrica:** medida calculada/observada;
* **criterio de aceitacao:** requisito para concluir gate ou conformidade;
* **regra de interpretacao:** mapeamento de evidencias para estado de resultado;
* **Criterio de Avaliacao:** hipotese de conceito mais amplo que pode organizar essas regras.

O protocolo registra onde a funcao aparece, mas nao cria no oficial. Recorrencia futura sera evidencia para analise, nao promocao automatica.

## 19. DGA-01

O nucleo do protocolo e neutro quanto a:

* dominio;
* projeto;
* tecnologia;
* linguagem;
* arquitetura de software;
* agente humano, institucional ou de IA.

Casos internos podem compor fases iniciais, mas OV-08 exige casos externos/multidominio antes de qualquer alegacao de generalidade. Codex, PROTEUS e ICFACTORY nao sao dependencias do procedimento.

## 20. Governanca De Versoes Do Protocolo

* `vMAJOR.MINOR`;
* `MINOR`: esclarecimento compativel antes de execucao ou correcao sem alterar hipoteses/metricas;
* `MAJOR`: muda objeto, desenho, unidade, grupo, metrica ou interpretacao;
* versao usada por experimento fica congelada;
* mudanca futura nao reinterpreta silenciosamente experimento anterior;
* protocolo anterior, caso exista, deve ser inventariado e comparado antes de substituicao.

Nesta auditoria documental nao foi identificado protocolo RG-05 anterior. A afirmacao limita-se ao acervo RG auditado; ausencia fora do escopo nao e presumida.

## 21. Encerramento De Experimento Futuro

Um experimento encerra somente quando:

* gates aplicaveis foram avaliados;
* pacote experimental esta completo ou lacunas declaradas;
* desvios foram classificados;
* dados/analises foram congelados;
* hipoteses receberam estados permitidos;
* evidencias contrarias e limitacoes foram registradas;
* custodia/confidencialidade foram resolvidas;
* nenhuma conclusao excede o escopo.

## 22. Saida Para GP-RG-06

GP-RG-06 somente podera iniciar apos:

1. autorizacao formal;
2. escolha fundamentada do(s) caso(s) conforme framework;
3. pre-registro completo;
4. definicao de avaliadores e independencia;
5. congelamento de versoes/instrumentos;
6. aprovacao de confidencialidade e propriedade;
7. definicao de metricas/limiares contextuais antes dos resultados;
8. declaracao de que o primeiro piloto e exploratorio e nao valida generalidade.

## 23. Limitacoes Do Protocolo

* nao foi pilotado;
* metricas e limiares ainda nao calibrados;
* casos nao foram selecionados;
* tamanho amostral nao pode ser universal antes do desenho de cada OV;
* independencia entre agentes pode ser imperfeita;
* comparacao convencional pode sofrer nao equivalencia;
* custo do proprio protocolo e desconhecido;
* DGA-01 permanece propriedade de desenho;
* nenhuma hipotese esta promovida;
* nenhum resultado empirico existe nesta GP.

## 24. Estado Final

**PROTOCOLO EXPERIMENTAL GDC-R FORMALIZADO — SEM EXECUCAO EMPIRICA**

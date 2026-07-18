# GP-RG-03 — Arquitetura Da Cadeia De Governanca Da Fundamentacao Das Decisoes

## 1. Identidade E Alcance

| Campo | Registro |
|---|---|
| Identificador | GP-RG-03 |
| Natureza | arquitetura documental da pesquisa |
| Nome arquitetural | GDC-R — Grafo Dirigido de Governanca com Revisoes Controladas |
| Estado | ARQUITETURA DOCUMENTAL FORMALIZADA — VALIDACAO EMPIRICA PENDENTE |
| Objeto | registros observaveis e relacoes que fundamentam decisoes |
| Nao objeto | arquitetura de software, funcionamento interno de agentes ou mecanismo cognitivo |
| Hipoteses | H-RG-001 a H-RG-007 permanecem sem promocao |
| Conceito experimental | `Criterio de Avaliacao` permanece HIPOTESE OBSERVACIONAL e externo ao nucleo |

“Oficial” neste documento significa arquitetura de referencia aprovada para continuidade da linha de pesquisa GP-RG. Nao significa validacao empirica, adocao normativa pelo ICFACTORY ou alteracao da arquitetura do PROTEUS.

## 2. Objetivo

Organizar os conceitos formalizados pela GP-RG-02 em uma estrutura documental versionavel, rastreavel e auditavel, especificando elementos, relacoes, ciclos de revisao, regras de integridade, estados verificaveis e criterios de conformidade.

### 2.1 Diretriz De Generalidade DGA-01

O nucleo GDC-R e independente de dominio, projeto, organizacao, tecnologia e tipo de agente decisor. PROTEUS, ICFACTORY e GP-PI-07A fornecem proveniencia de pesquisa e exemplos de formacao da arquitetura; nao integram seus elementos obrigatorios, regras, relacoes, estados ou perfis.

A arquitetura deve admitir instancias em:

* desenvolvimento de software;
* auditorias;
* documentacao;
* pesquisa cientifica;
* gestao de projetos;
* tomada de decisao humana;
* sistemas assistidos por IA;
* outros dominios que exijam fundamentacao documental de decisoes.

Regras de neutralidade:

1. nenhum campo estrutural pode exigir entidade propria de um projeto;
2. nenhum tipo de no pode pressupor ferramenta, formato de arquivo ou agente especifico;
3. vocabularios de dominio somente podem aparecer em extensoes ou conteudo de instancias;
4. extensoes nao podem redefinir P, E, I, F, D ou V nem enfraquecer invariantes;
5. exemplos particulares nao se tornam requisitos gerais;
6. identidade do agente pode ser humana, institucional, automatizada, assistida por IA ou composta, desde que declarada no registro aplicavel;
7. aplicabilidade geral permanece objetivo arquitetural, nao resultado empirico, ate validacao multidominio.

Confianca: **ALTA** quanto a ausencia de dependencias de projeto no nucleo definido; **BAIXA** quanto a aplicabilidade efetiva em todos os dominios listados, pois ela ainda nao foi testada.

## 3. Autoridades E Base De Evidencias

| ID | Artefato | Contribuicao | Limitacao |
|---|---|---|---|
| E-RG03-001 | `RG_01_RESEARCH_CONSTITUTION.md` | objeto, limites, hipotese central e principios | constituicao, nao teste da arquitetura |
| E-RG03-002 | `RG_01_RESEARCH_ROADMAP.md` | gates e papel documental previsto para RG-03 | planejamento prospectivo |
| E-RG03-003 | `RG_02_CONCEPTUAL_MODEL.md` | tipos, regras RC-01 a RC-18, cardinalidades e estados | modelo nao validado multidominio |
| E-RG03-004 | `RG_02_SEMANTIC_MATRIX.md` | fronteiras, ambiguidades e testes de classificacao | nao aplicado por avaliadores independentes |
| E-RG03-005 | `RG_02_CLOSURE_REPORT.md` | decisoes D-RG02-001 a D-RG02-006 e recomendacoes | conclusao documental, nao empirica |
| E-RG03-006 | `PI_07A_DECISION_FOUNDATION_GOVERNANCE_REPORT.md` | caso fundador com multiplas evidencias, revisao e validacao negativa | um caso audiovisual/documental |

Inferencia arquitetural I-RG03-001: os artefatos sustentam estruturar relacoes e revisoes, mas nao sustentam afirmar que a estrutura e universal, suficiente em todos os dominios ou superior a arquiteturas alternativas.

## 4. Decisao De Topologia

### 4.1 Alternativas Avaliadas

| Alternativa | Adequacao observada | Limitacao decisiva | Decisao |
|---|---|---|---|
| sequencia | representa a leitura Premissa → Evidencia → Inferencia → Fundamentacao → Decisao → Validacao | nao representa compartilhamento, multiplas entradas nem retorno de Validacao | rejeitada como topologia; preservada como vista didatica |
| arvore | representa ramificacoes hierarquicas | um no teria um unico ascendente logico; evidencias e fundamentacoes podem ser reutilizadas | rejeitada |
| grafo dirigido aciclico | representa multiplas entradas e dependencias | nao representa revisao que retroalimenta a cadeia | rejeitada |
| grafo dirigido com ciclos livres | representa retornos | admite circularidade probatoria e ciclos que podem ocultar ausencia de origem independente | rejeitada |
| grafo dirigido, versionado, com ciclos de revisao controlados | representa multiplas relacoes, retroacao, preservacao historica e restricoes de integridade | ainda depende de validacao em outros casos | adotada |

### 4.2 Arquitetura Adotada

O GDC-R e um **grafo dirigido, tipado, versionado e com ciclos de revisao controlados**.

Formalmente, uma cadeia `C` e representada pela tupla:

`C = (M, N, A, R, S)`

Onde:

* `M` e o Manifesto da Cadeia;
* `N` e o conjunto de nos conceituais tipados;
* `A` e o conjunto de arestas relacionais tipadas;
* `R` e o conjunto de Registros de Revisao;
* `S` e o Estado Verificavel do snapshot.

Os tipos conceituais oficiais de `N` permanecem exclusivamente:

`P = Premissa`, `E = Evidencia`, `I = Inferencia`, `F = Fundamentacao`, `D = Decisao`, `V = Validacao`.

Manifesto, aresta e registro de revisao sao controles estruturais, nao novos conceitos epistemicos da cadeia.

### 4.3 Grau De Confianca Da Escolha

* **ALTA** para representar o caso fundador e as regras atualmente formalizadas;
* **MEDIA** para a coerencia estrutural interna;
* **BAIXA** para completude multidominio, eficiencia operacional e superioridade comparativa.

## 5. Elementos Arquiteturais

### 5.1 Manifesto Da Cadeia (`M`)

Registro de controle que delimita uma instancia da cadeia.

Campos obrigatorios:

* `chain_id`;
* titulo e objetivo;
* dominio e escopo;
* autoridade ou responsavel logico;
* versao do snapshot;
* perfil de conformidade;
* estado verificavel;
* identificadores dos nos e revisoes integrantes;
* limitacoes gerais;
* data ou ordem logica de abertura e ultima revisao.

O Manifesto nao substitui Fundamentacao nem Decisao.

### 5.2 No Conceitual (`N`)

Registro tipado conforme a GP-RG-02.

Campos estruturais obrigatorios:

* `node_id` imutavel;
* `chain_id`;
* `node_type` em `{P,E,I,F,D,V}`;
* `version_id`;
* conteudo declarado;
* origem ou agente registrador;
* estado atual;
* limitacoes;
* ordem logica de criacao;
* referencia ao predecessor quando revisado.

Campos especificos seguem as definicoes RG-02. Ausencia deve ser marcada como `NAO_INFORMADO`, `NAO_APLICAVEL` ou `PENDENTE`, com justificativa; campo vazio nao equivale a inexistencia.

### 5.3 Aresta Relacional (`A`)

Registro que torna explicita uma dependencia, contribuicao, contestacao, sucessao ou avaliacao.

Campos obrigatorios:

* `edge_id`;
* `chain_id`;
* `source_node_id`;
* `target_node_id`;
* `relation_type`;
* justificativa da relacao;
* estado (`ATIVA`, `CONTESTADA`, `SUPERADA` ou `INVALIDA`);
* versao e ordem logica;
* limitacoes quando aplicaveis.

A direcao canonica e **antecedente documental → elemento dependente ou posterior**. A consulta reversa permanece obrigatoria para auditoria.

### 5.4 Registro De Revisao (`R`)

Controle estrutural append-only que documenta por que e como um elemento ou relacao mudou.

Campos obrigatorios:

* `revision_id`;
* gatilho e origem;
* elemento anterior;
* estado anterior;
* elemento sucessor ou estado `REVISAO_PENDENTE`;
* motivo e fundamentacao da mudanca;
* impacto propagado;
* autoridade da revisao;
* validacao posterior requerida;
* ordem logica.

Revisao nao e um setimo tipo conceitual e nao autoriza sobrescrever o registro anterior.

### 5.5 Estado Verificavel (`S`)

Todo snapshot deve declarar exatamente um estado arquitetural:

| Estado | Significado |
|---|---|
| `EM_CONSTRUCAO` | cadeia aberta; lacunas identificadas |
| `AGUARDANDO_DECISAO` | fundamentacao existe, mas nao ha decisao autorizada |
| `AGUARDANDO_VALIDACAO` | decisao existe, mas resultado ainda nao foi validado |
| `VALIDADA_APROVADA` | validacao aprovou no escopo declarado |
| `VALIDADA_COM_RESSALVAS` | validacao aprovou parcialmente ou com limites materiais |
| `VALIDADA_REJEITADA` | validacao rejeitou o resultado |
| `VALIDACAO_INCONCLUSIVA` | evidencia nao permite conclusao |
| `EM_REVISAO` | gatilho abriu ciclo de revisao ainda nao encerrado |
| `ENCERRADA_SEM_ACAO` | decisao governada de nao agir foi encerrada e verificada no escopo |
| `NAO_CONFORME` | uma ou mais regras bloqueantes de integridade falharam |

Estado verificavel nao significa resultado positivo. Rejeicao, inconclusao e nao conformidade sao estados validos quando registrados sem omissao.

## 6. Catalogo De Relacoes

### 6.1 Relacoes De Sustentacao E Composicao

| ID | Relacao | Origem → Destino | Obrigatoriedade | Semantica |
|---|---|---|---|---|
| AR-01 | `CONDICIONA` | P → I | opcional por I | premissa delimita a inferencia |
| AR-02 | `SUPORTA` | E → I | obrigatoria, minimo 1 por I | evidencia sustenta derivacao interpretativa |
| AR-03 | `COMPOE_FUNDAMENTACAO` | P → F | opcional por F | premissa integra o suporte decisorio |
| AR-04 | `COMPOE_FUNDAMENTACAO` | E → F | obrigatoria, minimo 1 por F | evidencia integra diretamente a fundamentacao |
| AR-05 | `COMPOE_FUNDAMENTACAO` | I → F | opcional por F | inferencia integra a fundamentacao |
| AR-06 | `FUNDAMENTA` | F → D | obrigatoria, minimo 1 por D | fundamentacao sustenta decisao |
| AR-07 | `SUBMETE_A_VALIDACAO` | D → V | obrigatoria para V; requerida para D executada | validacao avalia resultado da decisao |
| AR-08 | `PRODUZ_OBSERVACAO` | V → E | obrigatoria para validacao concluida, minimo 1 | resultado observado retorna como nova evidencia |

### 6.2 Relacoes De Contestacao E Revisao

| ID | Relacao | Origem → Destino | Efeito permitido |
|---|---|---|---|
| AR-09 | `CONFIRMA` | E → P | pode confirmar estado da premissa no escopo |
| AR-10 | `CONTESTA` | E → P, E → I ou E → F | abre avaliacao de impacto; nao invalida automaticamente |
| AR-11 | `SUPERADA_POR` | versao anterior → versao sucessora do mesmo tipo | preserva predecessor e ativa sucessor |
| AR-12 | `REVISA` | D anterior → D sucessora | mantem, altera ou revoga compromisso com justificativa |
| AR-13 | `REVALIDA` | V anterior → V sucessora | registra novo teste sem apagar resultado anterior |
| AR-14 | `MOTIVA_REVISAO` | V → R | validacao negativa, inconclusiva ou limitada abre revisao |
| AR-15 | `IMPLEMENTA_REVISAO` | R → no ou aresta sucessora | vincula o controle de revisao ao novo estado |
| AR-16 | `DECLARA_CONFLITO` | no → no do mesmo ou de outro tipo compativel | explicita contradicao ainda nao resolvida |

AR-11 a AR-15 formam ciclos **logicos** de revisao ao longo das versoes; nao formam ciclos de sustentacao dentro do mesmo snapshot.

### 6.3 Relacoes Opcionais De Contexto

| ID | Relacao | Origem → Destino | Condicao |
|---|---|---|---|
| AR-17 | `REFINA` | I → I | a inferencia sucessora ainda deve ter evidencia propria |
| AR-18 | `RELACIONA_ALTERNATIVA` | F → D candidata ou registro externo identificado | alternativas razoaveis devem permanecer distinguiveis da decisao escolhida |
| AR-19 | `COMPARTILHA` | E → I ou F em outra cadeia | origem, escopo e limitacoes devem ser preservados; nao copiar sem proveniencia |
| AR-20 | `DEPENDE_DE_DECISAO` | D → D | dependencia entre decisoes sem substituir FUNDAMENTA |

## 7. Matriz Por Conceito

| Conceito | Relacoes permitidas principais | Obrigatorias | Podem iniciar revisao | Podem contribuir para invalidacao | Podem levar a nova decisao |
|---|---|---|---|---|---|
| Premissa | P→I, P→F, P antiga→P nova | origem e estado; vinculos quando utilizada | nova/revisada P pode abrir R | premissa rejeitada compromete dependentes | somente via nova F |
| Evidencia | E→I, E→F, E→P/I/F por confirmacao ou contestacao | fonte, metodo, alcance; E→I para cada I; E→F para cada F | nova E ou E contestada pode abrir R | sim, por contestacao formal e propagacao | somente via I/F |
| Inferencia | I→F, I antiga→I nova, I→I por refinamento | ao menos uma E→I | I revisada/rejeitada abre impacto | sim, sobre F dependentes | somente via F |
| Fundamentacao | F→D, F antiga→F nova | ao menos uma E→F; F→D para toda D | F insuficiente/contestada abre revisao de D | sim, pode retirar suporte vigente | sim, F nova pode sustentar D nova |
| Decisao | D→V, D→D por revisao/dependencia | ao menos uma F→D | decisao revisada ou revogada abre ciclo | pode substituir estado de D anterior, nunca apaga-la | sim, por D sucessora formal |
| Validacao | D→V, V→E, V→R, V antiga→V nova | referencia a D; resultado observado para conclusao | negativa, inconclusiva ou ressalvada pode abrir R | sim, como gatilho formal, nao por sobrescrita | somente via E/I/F e nova D |

## 8. Relacoes Proibidas

| ID | Proibicao | Motivo |
|---|---|---|
| AP-01 | P → D como unico suporte | Decisao exige Fundamentacao |
| AP-02 | E → D como unico suporte | evidencia nao substitui composicao decisoria |
| AP-03 | I → D como unico suporte | inferencia isolada nao e Fundamentacao |
| AP-04 | V alterar diretamente o conteudo de D, P, I ou F | revisao exige novo registro e historico |
| AP-05 | D servir como Evidencia de sua propria correcao | circularidade |
| AP-06 | F ser sustentada apenas pela D que pretende fundamentar | circularidade de fundamentacao |
| AP-07 | I existir sem E → I ativa | viola RC-05 |
| AP-08 | F existir sem elemento relacional e sem ao menos uma E → F | viola RC-08 e identidade de Fundamentacao |
| AP-09 | V concluida sem D → V e sem resultado observado | validacao sem objeto ou sem evidencia |
| AP-10 | aresta apontar para no inexistente ou versao apagada | referencia pendente e perda de integridade |
| AP-11 | sucessor sobrescrever predecessor | elimina rastreabilidade historica |
| AP-12 | ciclo de sustentacao no mesmo snapshot | permite que elementos se sustentem apenas entre si |
| AP-13 | `Criterio de Avaliacao` ser tipado como no oficial P/E/I/F/D/V | conceito permanece hipotese observacional |
| AP-14 | ausencia de evidencia ser representada como evidencia de inexistencia sem busca delimitada | extrapolacao indevida |
| AP-15 | estado positivo ocultar conflito, ressalva ou revisao pendente material | viola consistencia e nao seletividade |

## 9. Ciclo Oficial De Revisao

### 9.1 Gatilhos

Um ciclo deve ser aberto quando ocorrer pelo menos um dos eventos:

1. nova Evidencia relevante;
2. Evidencia contestada, invalidada ou superada;
3. nova Premissa aplicavel;
4. Premissa confirmada, contestada, rejeitada ou substituida;
5. Inferencia revisada ou rejeitada;
6. Fundamentacao declarada insuficiente ou modificada;
7. Decisao revista, revogada ou dependente de nova decisao;
8. Validacao negativa, inconclusiva ou aprovada com ressalva material;
9. conflito estrutural ou semantico detectado;
10. falha de regra bloqueante de integridade.

### 9.2 Etapas Obrigatorias

1. **Detectar:** registrar gatilho e evidencia observavel.
2. **Abrir R:** criar Registro de Revisao com escopo e autoridade.
3. **Congelar snapshot anterior:** impedir sobrescrita; manter estado historico.
4. **Calcular alcance:** percorrer arestas ativas a partir do elemento afetado.
5. **Classificar impacto:** `SEM_IMPACTO`, `REAVALIAR`, `INVALIDAR_ESTADO` ou `INCONCLUSIVO`.
6. **Produzir sucessores:** criar novos nos/arestas quando necessario.
7. **Recompor Fundamentacao:** incluir informacao nova, contraria e alternativas.
8. **Declarar Decisao:** manter, revisar, revogar ou criar nova D.
9. **Revalidar:** criar nova V quando houver resultado verificavel.
10. **Encerrar R:** registrar resultado, pendencias, limitacoes e novo estado `S`.

### 9.3 Propagacao

* P afetada: revisar I e F que dependem dela; D somente muda por nova F e ato decisorio.
* E afetada: revisar I e F que a utilizam; marcar dependencias transitivas para avaliacao.
* I afetada: revisar F dependentes e, por consequencia, D sustentadas.
* F afetada: revisar suficiencia das D dependentes.
* D afetada: revisar V pendentes ou resultados cuja interpretacao dependa do escopo anterior.
* V negativa: produzir E do resultado, abrir R e reconstruir a cadeia necessaria.

Propagacao nao equivale a invalidacao automatica. Cada mudanca de estado exige justificativa e registro.

## 10. Perfis De Conformidade

### 10.1 Perfil Minimo Governado (`PMG`)

Aplicavel quando risco e complexidade permitirem documentacao reduzida.

Requer:

* Manifesto;
* pelo menos uma Evidencia;
* Fundamentacao;
* Decisao;
* Validacao ou estado justificado `AGUARDANDO_VALIDACAO`/`ENCERRADA_SEM_ACAO`;
* Premissa e Inferencia quando efetivamente utilizadas, nunca omitidas para simplificar;
* historico e limitacoes.

### 10.2 Perfil Completo De Pesquisa (`PCP`)

Requer os seis tipos P/E/I/F/D/V, alternativas, confianca, riscos, limitacoes, revisoes, manifestos e todos os vinculos de integridade. E o perfil recomendado para GP-RG-04/05.

### 10.3 Regra De Proporcionalidade

O perfil deve ser declarado antes da avaliacao da conformidade. A escolha de PMG nao autoriza omitir elemento relevante. Decisoes de alto impacto, alta incerteza ou baixa reversibilidade devem usar PCP ou justificar perfil mais rigoroso. A eficacia dessa regra ainda nao foi testada.

## 11. Regras De Integridade Arquitetural

| ID | Regra | Severidade |
|---|---|---|
| RI-01 | todo no e aresta pertence a um Manifesto existente | BLOQUEANTE |
| RI-02 | identificadores sao unicos e imutaveis no escopo | BLOQUEANTE |
| RI-03 | toda Evidencia possui origem, metodo, alcance e limitacoes | BLOQUEANTE |
| RI-04 | toda Inferencia possui ao menos uma aresta AR-02 ativa | BLOQUEANTE |
| RI-05 | toda Fundamentacao possui ao menos uma AR-04 e relacoes explicitadas | BLOQUEANTE |
| RI-06 | toda Decisao possui ao menos uma AR-06 ativa | BLOQUEANTE |
| RI-07 | toda Validacao referencia Decisao por AR-07 | BLOQUEANTE |
| RI-08 | Validacao concluida registra resultado observavel por AR-08 | BLOQUEANTE |
| RI-09 | revisao preserva predecessor, sucessor e motivo | BLOQUEANTE |
| RI-10 | nenhum alvo de aresta e inexistente | BLOQUEANTE |
| RI-11 | nenhum ciclo de sustentacao existe no mesmo snapshot | BLOQUEANTE |
| RI-12 | conflitos ativos estao declarados | ALTA |
| RI-13 | alternativas razoaveis e informacao contraria estao preservadas | ALTA |
| RI-14 | estado do Manifesto corresponde aos estados dos nos | ALTA |
| RI-15 | confianca e limitacoes acompanham I, F, D e V quando aplicaveis | ALTA |
| RI-16 | compartilhamento entre cadeias preserva proveniencia e escopo | ALTA |
| RI-17 | campos ausentes possuem marcacao e justificativa | MEDIA |
| RI-18 | conceito experimental nao e confundido com no oficial | BLOQUEANTE |

Falha bloqueante torna a cadeia `NAO_CONFORME`. Falha alta impede declarar completude. Falha media exige ressalva e plano de correcao.

## 12. Propriedades Arquiteturais

| Propriedade | Definicao operacional | Evidencia arquitetural minima | Limite |
|---|---|---|---|
| Rastreabilidade | capacidade de percorrer relacoes entre D e seus antecedentes e sucessores | caminho D←F←E e, quando usados, I/P; D→V; revisoes encadeadas | caminho existente nao prova verdade |
| Auditabilidade | capacidade de terceiro inspecionar tipos, origens, estados, conflitos e mudancas | Manifesto, identificadores, arestas tipadas e historico | utilidade por auditor independente nao testada |
| Reprodutibilidade | capacidade potencial de repetir coleta, derivacao ou validacao com registros declarados | metodo, entradas, versoes, limitacoes e resultado esperado | arquitetura habilita; nao garante reproducao bem-sucedida |
| Consistencia | ausencia de estados mutuamente incompatíveis nao declarados | verificacao de estados, arestas e conflitos | conflitos declarados podem permanecer abertos |
| Completude | atendimento do perfil declarado e ausencia de lacunas nao justificadas | checklist PMG/PCP e RI aplicaveis | nao equivale a cobertura de toda realidade relevante |
| Integridade | identidade, proveniencia, referencias e historico preservados | RI-01 a RI-18 | integridade documental nao e integridade factual absoluta |
| Nao Ambiguidade | tipo primario e semantica de relacao identificaveis | `node_type`, `relation_type` e desmembramento de registros mistos | interpretacoes de dominio podem divergir |
| Versionamento | sucessao explicita sem sobrescrita | `version_id`, AR-11/12/13 e R | nao define tecnologia de armazenamento |
| Revisibilidade | capacidade de incorporar informacao nova com impacto rastreado | ciclo oficial de revisao | nao garante baixo custo |
| Explicabilidade Documental | capacidade de reconstruir justificativa declarada sem estados internos | F, alternativas, limites e caminhos do grafo | nao representa raciocinio interno nem garante persuasao |

Uma propriedade e **suportada arquiteturalmente** quando os controles existem; somente sera **demonstrada empiricamente** apos aplicacao e avaliacao em protocolo apropriado.

## 13. Consistencia E Completude

### 13.1 Classificacao De Conformidade

| Classe | Condicao |
|---|---|
| `CONFORME` | todas as regras bloqueantes e altas atendidas; perfil completo |
| `CONFORME_COM_RESSALVAS` | bloqueantes atendidas; falhas medias ou limitacoes declaradas |
| `INCOMPLETA` | faltam elementos do perfil, mas lacunas estao identificadas e nao ha falsa declaracao de completude |
| `INCONSISTENTE` | conflitos ativos nao declarados ou estados incompatíveis |
| `NAO_CONFORME` | pelo menos uma regra bloqueante violada |

### 13.2 Testes Estruturais Minimos

1. todos os IDs sao unicos;
2. todas as referencias resolvem;
3. todo I e alcancavel a partir de pelo menos uma E;
4. toda D e alcancavel a partir de pelo menos uma F e uma E;
5. toda V concluida e alcancavel a partir de D e conduz a pelo menos uma E de resultado;
6. nao existe ciclo composto apenas por AR-01 a AR-08 dentro do mesmo snapshot;
7. toda versao superada permanece acessivel;
8. conflitos e lacunas alteram corretamente a classe e o estado;
9. o perfil declarado corresponde aos elementos presentes;
10. nenhum registro experimental e contado como tipo oficial.

## 14. Criterio De Avaliacao — Tratamento Experimental

Durante a modelagem surgiu naturalmente a necessidade de uma regra que associe resultado observado a qualificacao de Validacao. Isso constitui **evidencia arquitetural adicional de utilidade potencial**, nao evidencia de autonomia conceitual nem validacao multidominio.

Tratamento adotado:

* pode ser registrado como anotacao externa versionada associada a V ou a requisitos de D/F;
* nao recebe `node_type` oficial;
* nao e contado para completude da cadeia conceitual;
* sua origem e momento de definicao devem ser preservados;
* eventual alteracao posterior deve ser registrada;
* permanece **HIPOTESE OBSERVACIONAL** ate GP-RG-05 e decisao formal posterior.

Interpretacoes alternativas — no autonomo, atributo de V ou restricao de D/F — permanecem abertas.

## 15. Hipoteses Preservadas

| Hipotese | Estado apos a arquitetura |
|---|---|
| H-RG-001 | VALIDACAO PENDENTE |
| H-RG-002 | SUSTENTADA EM UM CASO; NAO VALIDADA |
| H-RG-003 | SUSTENTADA EM UM CASO; NAO VALIDADA |
| H-RG-004 | PENDENTE |
| H-RG-005 | PENDENTE |
| H-RG-006 | PENDENTE |
| H-RG-007 | PENDENTE |

A existencia de uma arquitetura coerente nao confirma rastreabilidade significativa, reproducibilidade independente, melhoria da qualidade, aplicabilidade multidominio ou consistencia entre agentes.

## 16. Limitacoes

* arquitetura derivada de documentos internos e um unico caso fundador;
* nenhum teste com cadeias extensas, concorrentes ou multidominio;
* nenhuma medicao de custo, desempenho documental ou concordancia entre auditores;
* cardinalidades de decisoes compostas ainda dependem de experimento;
* perfis PMG e PCP nao foram validados;
* severidades das regras sao decisoes arquiteturais desta GP, nao resultados empiricos;
* estados verificaveis podem exigir extensao apos novos casos;
* compartilhamento entre cadeias nao foi testado;
* nenhuma tecnologia de armazenamento, schema de software ou mecanismo de execucao foi definido;
* `Criterio de Avaliacao` permanece conceitualmente aberto;
* arquitetura documental nao representa mecanismo interno de agente.

## 17. Conclusao

O GDC-R organiza os seis tipos conceituais em grafo dirigido e versionado, permite multiplas evidencias e fundamentacoes, controla retroalimentacao por registros de revisao e proibe ciclos de sustentacao. Regras, estados, propriedades, perfis e testes tornam a conformidade documental verificavel sem exigir acesso a processos internos.

A arquitetura e formalmente coerente com as autoridades RG-01/RG-02 no alcance documental auditado. Sua adequacao geral e eficacia permanecem hipoteses dependentes das GP-RG-04 e GP-RG-05.

## 18. Estado Final

**ARQUITETURA GDC-R FORMALIZADA PARA PESQUISA — VALIDACAO EMPIRICA PENDENTE**

# GP-D07A - Auditoria Dos Eventos Institucionais Do Projeto

## Objetivo

Auditar, exclusivamente em nivel documental e de dominio, se o Projeto de Monitoramento deve reconhecer Eventos Institucionais.

A auditoria distingue Evento Institucional de evento operacional, log tecnico, medicao, alteracao de estado, evidencia documental e registro para Dossie Final.

Esta GP nao implementa codigo, nao altera persistencia, nao altera interface, nao altera o Dossie Final, nao cria nova camada e nao cria entidade `Evento`.

## Escopo

Foram avaliados:

* definicao conceitual de Evento Institucional do Projeto;
* eventos que podem existir no ciclo de vida do Projeto;
* eventos permanentes;
* eventos apenas operacionais;
* relacao entre evento, estado, evidencia, responsabilidade e Dossie Final;
* necessidade ou nao de entidade propria;
* necessidade ou nao de colecao no Projeto;
* impacto sobre PA-01;
* impacto sobre as Discoveries PA-02 e PA-03.

Ficaram fora do escopo:

* implementacao de entidade, colecao, repositorio, tela ou persistencia de eventos institucionais;
* alteracao dos eventos operacionais existentes;
* alteracao de `data/eventos_operacionais.json`;
* alteracao do Dossie Final;
* criacao de nova Discovery sem justificativa explicita.

## Estado Atual Do Dominio

O dominio atual possui identificacao do Projeto, cliente, contexto operacional, perfil operacional, persistencia, estados, ciclo de vida, encerramento, arquivamento, Dossie Final, conteudo permanente do Dossie Final, imutabilidade substantiva, responsabilidades auditadas, evidencias auditadas e referencias permanentes as evidencias.

Tambem existe, fora do dominio permanente do Projeto, a Governanca Operacional com eventos operacionais, estados observacionais, rastreamento de ocorrencias e persistencia propria. Esses eventos operacionais acompanham alertas, pendencias ou ocorrencias de operacao, mas nao sao automaticamente Eventos Institucionais do Projeto.

O Dossie Final ja reconhece "eventos relevantes" como conteudo consolidado, mas isso nao equivale a uma entidade formal de evento institucional. O estado atual suporta registro conceitual e sintese documental, sem exigir estrutura propria.

## Definicao Conceitual De Evento Institucional

Evento Institucional do Projeto e um acontecimento relevante para a memoria, governanca documental ou ciclo institucional do Projeto de Monitoramento.

Um Evento Institucional caracteriza-se por:

* marcar um fato relevante do Projeto como unidade de dominio;
* possuir valor de compreensao futura apos encerramento ou arquivamento;
* explicar decisao, marco, excecao, responsabilidade ou preservacao documental;
* poder ser descrito como registro ou sintese sem duplicar logs, medicoes ou eventos operacionais granulares;
* nao executar avaliacao observacional, nao selecionar politica e nao recalcular sinais.

Evento Institucional nao e qualquer ocorrencia tecnica. Ele deve responder: "este acontecimento ajuda a compreender o Projeto como memoria institucional?".

## Distincoes Conceituais

| Conceito | Definicao | Pertence ao dominio permanente do Projeto? | Observacao |
| --- | --- | --- | --- |
| Evento Institucional | Acontecimento relevante para memoria, ciclo, decisao ou custodia do Projeto | Sim, como conceito documental | Deve ser seletivo e permanente. |
| Evento operacional | Ocorrencia de operacao ou governanca diaria, como alerta, pendencia ou resolucao | Nao automaticamente | Pode originar sintese institucional se for relevante. |
| Log tecnico | Registro de runtime, erro, processamento ou auditoria tecnica | Nao | Pertence a trilhas tecnicas, nao ao Projeto permanente. |
| Medicao | Dado observado em campo ou fonte operacional | Nao como evento | Medicao compoe base operacional e pode sustentar evidencias consolidadas. |
| Alteracao de estado | Transicao formal do Projeto, como `ativo` para `encerrado` | Sim, como marco de ciclo | A transicao altera estado; o evento apenas documenta o acontecimento. |
| Evidencia documental | Referencia verificavel que sustenta decisao, resultado ou memoria | Sim, quando permanente | Pode sustentar um evento institucional. |
| Registro para Dossie Final | Sintese ou referencia preservada no Dossie | Sim, quando permanente | Nao exige entidade propria de evento. |

## Matriz De Inclusao

| Evento candidato | Classificacao | Incluir no dominio? | Integrar Dossie? | Justificativa |
| --- | --- | --- | --- | --- |
| Criacao ou formalizacao do Projeto | Institucional permanente | Sim, conceitualmente | Sim, como identidade/contexto | Marca existencia do Projeto como unidade institucional. |
| Definicao ou mudanca formal de escopo operacional | Institucional permanente futura | Sim, se formalizada | Sim, como historico resumido | Explica por que o Projeto foi conduzido sob determinado escopo. |
| Inicio efetivo do ciclo monitorado | Institucional permanente | Sim, como marco | Sim, se relevante | Delimita a memoria temporal do Projeto. |
| Encerramento do Projeto | Institucional permanente | Sim, ja relacionado ao ciclo de vida | Sim | Marca conclusao operacional e sustenta Dossie Final. |
| Arquivamento do Projeto | Institucional permanente | Sim, ja relacionado ao ciclo de vida | Sim, como referencia de preservacao | Marca transferencia para memoria historica consultavel. |
| Emissao do Dossie Final | Institucional permanente | Sim, conceitualmente | Sim | Registra consolidacao documental oficial. |
| Evento critico relevante consolidado | Institucional derivado | Sim, se afetar leitura final | Sim, consolidado | Pode explicar resultado, recomendacao ou encerramento. |
| Excecao ou pendencia relevante justificada | Institucional permanente | Sim, se afetar encerramento | Sim, consolidada | Evita fechamento silencioso de lacunas. |
| Responsabilidade institucional assumida ou transferida | Institucional futura | Sim, se formalizada | Sim, quando permanente | Ajuda a auditar autoridade e custodia. |
| Referencia de custodia documental | Institucional futura | Sim, se formalizada | Sim, se existir | Sustenta arquivamento e preservacao. |

## Matriz De Exclusao

| Evento candidato | Excluir do dominio permanente? | Excluir do Dossie? | Justificativa |
| --- | --- | --- | --- |
| Medicao individual registrada | Sim | Sim | E dado operacional granular, nao evento institucional. |
| Log de sistema | Sim | Sim | Evidencia runtime, nao memoria de Projeto. |
| Erro tecnico transitorio | Sim | Sim | Pertence a suporte ou operacao tecnica. |
| Alerta operacional repetitivo | Sim | Sim, salvo consolidacao relevante | Pode ser importante para Governanca, mas nao para memoria permanente integral. |
| Mudanca interna de estado de evento operacional | Sim | Sim | Pertence ao ciclo de vida da Governanca Operacional, nao ao Projeto. |
| Recalculo analitico intermediario | Sim | Sim | Pertence a Analytics e nao deve ser reificado no Projeto. |
| Acao de interface | Sim | Sim | Nao representa acontecimento institucional. |
| Edicao administrativa sem impacto | Sim | Sim | Pode existir na operacao, mas nao agrega memoria permanente. |
| Rascunho documental | Sim | Sim | Preparacao nao e marco institucional final. |
| Anexo bruto ou arquivo temporario | Sim | Sim | Exige gestao documental nao aprovada e pode gerar duplicacao. |

## Eventos Permanentes

Eventos permanentes sao acontecimentos que ajudam a compreender o Projeto depois de encerrado ou arquivado.

Podem ser reconhecidos documentalmente:

* formalizacao do Projeto;
* inicio do ciclo monitorado, quando houver marco formal;
* mudanca formal de escopo, se aprovada em GP futura;
* encerramento do Projeto;
* emissao ou consolidacao do Dossie Final;
* arquivamento do Projeto;
* excecoes ou pendencias relevantes justificadas;
* eventos criticos consolidados que afetem resultado, recomendacao ou encerramento;
* assuncao ou transferencia formal de responsabilidade, se houver necessidade objetiva;
* referencia de custodia documental, se formalizada.

Esses eventos devem permanecer como sintese ou referencia documental, nao como trilha operacional completa.

## Eventos Operacionais Excluidos

Eventos apenas operacionais sao necessarios para executar e acompanhar a operacao, mas nao devem ser promovidos automaticamente a memoria institucional.

Incluem:

* alertas de rotina;
* pendencias operacionais de baixa relevancia;
* transicoes internas de eventos da Governanca Operacional;
* medicoes individuais;
* logs;
* tentativas de processamento;
* eventos de interface;
* tarefas administrativas sem impacto;
* registros temporarios;
* resultados intermediarios de Analytics ou Motor Observacional.

Esses eventos podem permanecer em fontes operacionais ou na Governanca Operacional, mas nao exigem entidade ou colecao no Projeto.

## Relacao Com Ciclo De Vida

Eventos Institucionais podem marcar acontecimentos do ciclo de vida, mas nao substituem estados.

O estado do Projeto responde a situacao vigente: `ativo`, `encerrado` ou `arquivado`.

O Evento Institucional responde ao acontecimento documentado: criacao, inicio, encerramento, emissao do Dossie, arquivamento ou excecao relevante.

Assim, eventos nao devem alterar estado por si mesmos. Uma transicao de estado pode gerar ou justificar um registro institucional, mas a autoridade da transicao continua pertencendo ao dominio de ciclo de vida do Projeto.

## Relacao Com Encerramento

O encerramento e um marco institucional permanente.

Um evento de encerramento pode registrar que o ciclo operacional terminou, qual data foi considerada, quem respondeu pelo fechamento e quais excecoes ou pendencias foram justificadas. Contudo, nesta GP, esse registro permanece conceitual e documental.

Evento nao cria encerramento autonomo. O encerramento continua dependente dos criterios e responsabilidades auditados anteriormente.

## Relacao Com Arquivamento

O arquivamento tambem e marco institucional permanente, distinto e posterior ao encerramento.

Um evento de arquivamento pode registrar que o Projeto encerrado foi preservado para consulta historica, incluindo referencia de custodia quando existir.

Arquivamento nao transforma eventos operacionais em institucionais. Apenas preserva a memoria seletiva aprovada para o Projeto.

## Relacao Com Responsabilidades

Eventos Institucionais podem gerar ou exigir responsabilidades quando registram autoria, autoridade, custodia ou justificativa.

Exemplos:

* encerramento exige responsavel institucional ou operacional autorizado;
* emissao do Dossie pode exigir responsavel pela consolidacao documental;
* arquivamento pode exigir responsavel pela custodia;
* excecao relevante pode exigir justificativa atribuivel.

Isso nao exige entidade propria agora. A relacao entre evento e responsabilidade deve permanecer como conceito documental ate que exista necessidade objetiva de workflow, historico de papeis ou auditoria formal de autoria.

## Relacao Com Evidencias

Eventos Institucionais podem gerar evidencias e tambem podem ser sustentados por evidencias.

Um evento de encerramento pode ser sustentado por Dossie Final, relatorio consolidado, recomendacoes emitidas ou referencia documental. Um evento critico consolidado pode originar evidencia permanente se afetar a conclusao do Projeto.

Nem todo evento gera evidencia permanente. Eventos operacionais, logs e medicoes individuais podem sustentar analises, mas permanecem fora da memoria institucional se nao agregarem valor permanente.

## Relacao Com Dossie Final

Eventos Institucionais permanentes devem integrar o Dossie Final apenas de forma seletiva e consolidada.

Devem integrar quando:

* explicam encerramento;
* explicam arquivamento;
* justificam excecao ou pendencia relevante;
* registram marco institucional permanente;
* sustentam recomendacao, conclusao ou memoria historica.

Nao devem integrar quando:

* representam rotina operacional;
* duplicam eventos de Governanca Operacional sem relevancia final;
* sao logs, medicoes, estados intermediarios ou dados temporarios;
* exigem gestao documental ainda nao aprovada.

Esta GP nao altera o Dossie Final ja implementado.

## Impacto Arquitetural

Nao ha necessidade de nova camada arquitetural.

Tambem nao ha justificativa objetiva para criar entidade `Evento` ou colecao de eventos no Projeto agora. O conceito agrega valor como classificacao documental, mas sua materializacao exigiria requisitos ainda inexistentes: cadastro de eventos institucionais, autoria formal, historico imutavel, consulta estruturada, workflow, filtros, persistencia dedicada ou integracao com Dossie.

Tratamento recomendado por alternativa:

* entidade propria: nao recomendada agora;
* colecao no Projeto: nao recomendada agora;
* atributo textual ou sintese no Dossie: ja existe caminho suficiente por eventos relevantes consolidados, sem alterar nesta GP;
* conceito documental: recomendado neste momento;
* materializacao futura: somente se houver necessidade objetiva e GP propria.

## Impacto De Dominio

O impacto de dominio e conceitual.

O Projeto passa a reconhecer que existem acontecimentos com valor institucional, mas a fronteira permanece clara:

* Eventos Institucionais pertencem a memoria do Projeto quando permanentes;
* eventos operacionais pertencem a Governanca Operacional ou a fontes de operacao;
* logs tecnicos pertencem ao runtime;
* medicoes pertencem as bases operacionais;
* estados pertencem ao ciclo de vida;
* evidencias sustentam acontecimentos, mas nao substituem eventos;
* Dossie Final consolida memoria, mas nao vira trilha integral.

## Analise PA-01

PA-01 permanece integralmente preservado.

Esta GP nao altera `PolicyEngine`, Motor Observacional, Analytics, Governanca, Recommendation, Dashboard, Relatorios, CSVs, runtime ou interface.

Evento Institucional nao seleciona politica, nao executa avaliacao, nao interpreta parametros, nao calcula Water Health Score, nao resolve alertas e nao decide severidade. Ele apenas registra ou descreve acontecimentos relevantes ao Projeto como memoria documental.

## Analise Das Discoveries

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Resultado:

* PA-02 foi reforcada: Eventos Institucionais agregam valor por enriquecimento documental do dominio existente, sem criacao de nova camada.
* PA-03 foi reforcada: o conceito deve permanecer reconhecido antes de qualquer materializacao de entidade, colecao, persistencia ou interface.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida automaticamente.
* Nenhuma nova Discovery candidata foi identificada.

## Observacoes da IA / Hipoteses Metodologicas

As observacoes abaixo nao alteram o escopo da GP-D07A, nao sao implementadas automaticamente, nao modificam PA-01, PA-02 ou PA-03 e nao integram oficialmente o ICFACTORY sem auditoria e validacao humana.

| Padrao observado | Evidencia usada | Possivel impacto | Recomendacao | Status sugerido |
| --- | --- | --- | --- | --- |
| Conceitos de dominio recorrentes amadurecem primeiro como auditoria documental antes de qualquer materializacao. | GP-D04A, GP-D05A, GP-D06A e GP-D07A reconheceram conceitos permanentes sem criar entidade imediata quando nao havia necessidade objetiva. | Reduz risco de inflar o dominio com estruturas prematuras. | Manter a pratica de auditar conceito, valor permanente e necessidade objetiva antes de implementar. | Observacao simples |
| A fronteira entre memoria permanente e operacao diaria aparece como criterio recorrente. | Dossie Final, Responsabilidades, Evidencias e Eventos Institucionais excluem medicoes individuais, logs, estados intermediarios e registros granulares. | Fortalece consistencia documental e evita transformar o Projeto em repositorio operacional paralelo. | Usar explicitamente a pergunta "agrega valor permanente ao Projeto?" em GPs futuras de dominio. | Hipotese em monitoramento |
| Eventos Institucionais podem se tornar ponto de convergencia entre ciclo de vida, evidencias e responsabilidades se forem materializados cedo demais. | Encerramento, arquivamento, Dossie, evidencias e responsabilidades possuem relacoes com eventos, mas ainda nao ha necessidade de workflow ou colecao. | Criar entidade agora poderia duplicar Dossie, Governanca Operacional ou Registro de Encerramento futuro. | Exigir GP propria antes de qualquer materializacao e comparar alternativas: sintese no Dossie, registro de encerramento ou colecao formal. | Observacao simples |
| As Discoveries PA-02 e PA-03 continuam suficientes para explicar a decisao de nao materializar eventos agora. | `DISCOVERY_CATALOG.md` define enriquecimento de camadas existentes e materializacao sob necessidade; a GP-D07A nao encontrou principio novo. | Evita criar Discovery candidata redundante. | Nao registrar nova Discovery candidata nesta GP; apenas monitorar recorrencia em auditorias futuras. | Observacao simples |

## Respostas Obrigatorias

### 1. O que caracteriza um Evento Institucional do Projeto?

Um acontecimento com valor permanente para memoria, ciclo, decisao, responsabilidade, encerramento, arquivamento ou custodia documental do Projeto.

### 2. Quais eventos podem existir?

Podem existir formalizacao do Projeto, inicio do ciclo, mudanca formal de escopo, encerramento, emissao do Dossie Final, arquivamento, excecao relevante, evento critico consolidado, transferencia formal de responsabilidade e referencia de custodia.

### 3. Quais eventos sao permanentes?

Sao permanentes os que ajudam a compreender o Projeto apos encerramento ou arquivamento: formalizacao, encerramento, Dossie Final, arquivamento, excecoes justificadas, eventos criticos consolidados e custodia documental quando formalizada.

### 4. Quais eventos sao apenas operacionais?

Alertas de rotina, medicoes individuais, logs, transicoes internas de eventos operacionais, erros tecnicos, tarefas administrativas sem impacto, acoes de interface e resultados intermediarios.

### 5. Eventos alteram estado ou apenas registram acontecimentos?

Eventos apenas registram acontecimentos. Alteracoes de estado pertencem ao ciclo de vida do Projeto. Uma transicao pode justificar um evento institucional, mas o evento nao altera estado por si so.

### 6. Eventos devem integrar o Dossie Final?

Somente eventos permanentes e relevantes devem integrar o Dossie Final, de forma consolidada ou referenciada. Eventos operacionais rotineiros devem permanecer fora.

### 7. Eventos geram evidencias?

Podem gerar evidencias quando documentam acontecimento relevante, mas nem todo evento gera evidencia permanente. Eventos tambem podem ser sustentados por evidencias ja existentes.

### 8. Eventos geram responsabilidades?

Podem gerar ou exigir responsabilidades quando envolvem autoria, encerramento, arquivamento, custodia, justificativa ou emissao documental. Isso nao exige entidade propria agora.

### 9. Evento exige entidade propria agora?

Nao. Nao ha justificativa arquitetural objetiva para entidade propria nesta GP.

### 10. Evento exige colecao no Projeto agora?

Nao. Uma colecao no Projeto seria prematura sem necessidade operacional objetiva de cadastro, busca, autoria, workflow ou persistencia estruturada.

### 11. Evento deve permanecer apenas como conceito documental neste momento?

Sim. Este e o tratamento recomendado para preservar PA-01, evitar ampliacao de escopo e respeitar PA-03.

## Conclusao

Eventos Institucionais sao relevantes para o dominio do Projeto, mas devem permanecer como conceito documental neste momento.

O modelo atual ja suporta memoria de eventos relevantes por sintese no Dossie Final e por referencias documentais, sem exigir nova entidade, colecao, persistencia ou interface. A evolucao futura so deve ocorrer se houver necessidade objetiva de registrar eventos institucionais com autoria, data, tipo, evidencia, responsabilidade e relacao formal com ciclo de vida.

## Veredito Final

Modelo de Eventos Institucionais suportado como conceito documental, sem implementacao.

Nao criar entidade `Evento` agora. Nao criar colecao no Projeto agora. Nao alterar Dossie Final agora. Eventos Institucionais devem permanecer delimitados documentalmente ate que uma GP futura demonstre necessidade objetiva de materializacao.

## Declaracao ICFACTORY E IA

1. A execucao permaneceu sob governanca ICFACTORY.
2. Nenhuma decisao da auditoria principal foi tomada por extrapolacao da IA fora das regras da GP; as conclusoes derivam das auditorias anteriores, do estado atual do dominio e do `DISCOVERY_CATALOG.md`.
3. Nao houve implementacao criativa fora da auditoria.
4. O Codex executou a GP-D07A e tambem registrou observacoes metodologicas separadas, autorizadas pelo complemento do pedido, sem incorpora-las ao escopo oficial nem ao nucleo ICFACTORY.
5. Validacao humana e recomendada antes de qualquer GP futura que materialize entidade, colecao, persistencia, workflow ou alteracao do Dossie Final para Eventos Institucionais.
6. As hipoteses e sugestoes externas ao escopo principal nao integram oficialmente o ICFACTORY sem auditoria e validacao humana.

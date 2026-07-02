# GP-D05A - Auditoria Das Responsabilidades Do Projeto

## Objetivo

Auditar, sem implementacao, quais responsabilidades devem existir no dominio do Projeto de Monitoramento.

A auditoria responde quem responde pelo Projeto ao longo de sua existencia, quais papeis pertencem ao dominio, quais responsabilidades sao permanentes, quais sao apenas operacionais e quais devem ou nao ser preservadas no Dossie Final.

## Escopo

Foram avaliados:

* papeis possiveis dentro de um Projeto;
* papeis obrigatorios;
* papeis opcionais;
* responsabilidades tecnicas;
* responsabilidades operacionais;
* responsabilidades administrativas;
* responsabilidades de aprovacao;
* responsabilidades ligadas ao encerramento;
* responsabilidades ligadas ao arquivamento;
* relacao das responsabilidades com o Dossie Final;
* diferencas entre participante, responsavel, operador, supervisor e aprovador.

Esta GP nao implementa codigo, nao altera persistencia, nao altera interface, nao altera o Dossie Final e nao cria nova camada arquitetural.

## Estado Atual Do Dominio

O dominio do Projeto ja possui identificacao, cliente, contexto operacional, perfil operacional, estados, ciclo de vida, encerramento, arquivamento, Dossie Final, conteudo permanente do Dossie Final e imutabilidade substantiva do Dossie Final.

No modelo atual, o unico campo que representa uma pessoa ou responsabilidade operacional explicita e `coletor_responsavel`. Esse campo cumpre uma funcao minima: registrar o responsavel principal pela coleta dentro do Projeto. Nao existe, neste momento, modelo de papeis, lista de participantes, cadeia de aprovacao, historico de substituicoes ou matriz formal de responsabilidades.

Esse estado e coerente com a evolucao incremental do Projeto: existe uma responsabilidade operacional minima, mas ainda nao ha evidencia suficiente para transformar responsabilidades em entidade propria ou workflow.

## Analise Conceitual

Responsabilidade de Projeto nao deve ser confundida com qualquer participacao operacional. A pergunta central nao e apenas "quem fez algo", mas "quem responde por algo relevante para compreender o Projeto como unidade de dominio".

Para esta auditoria, os conceitos sao separados da seguinte forma:

* Participante: pessoa ou grupo que participa de atividades do Projeto. Pode ser util em operacao diaria, mas nao necessariamente possui valor permanente.
* Responsavel: pessoa ou area que responde formalmente por uma dimensao do Projeto. Tende a possuir valor permanente quando ligada a identidade, execucao principal, encerramento, arquivamento ou custodia documental.
* Operador: executa atividades praticas, como coleta, lancamento ou verificacao de dados. Normalmente pertence a operacao diaria, salvo quando for o operador principal reconhecido como responsavel.
* Supervisor: acompanha qualidade, conformidade ou aderencia operacional. Pode ser relevante em Projetos futuros, mas ainda nao e obrigatorio no modelo atual.
* Aprovador: valida encerramento, dossie ou decisao formal. E conceito potencialmente valioso, mas depende de workflow de aprovacao ainda nao aprovado.

O criterio institucional "Agrega Valor ao Projeto?" indica que apenas responsabilidades que ajudem a entender, auditar ou preservar o Projeto devem entrar no dominio permanente. Responsabilidades de rotina, substituicoes temporarias e tarefas reconstruiveis a partir de logs nao agregam valor permanente suficiente neste momento.

## Matriz De Inclusao

| Responsabilidade | Classificacao | Incluir No Dominio? | Preservar No Dossie? | Justificativa |
| --- | --- | --- | --- | --- |
| Responsavel principal pelo Projeto | Permanente | Sim, em evolucao futura | Sim, quando existir | Identifica quem responde pelo Projeto como unidade operacional. Agrega valor historico e administrativo. |
| Coletor responsavel principal | Permanente minima ja existente | Sim, ja existe como atributo | Sim, ja preservado | Ajuda a compreender a execucao principal do monitoramento sem criar estrutura adicional. |
| Area operacional responsavel | Permanente contextual | Sim, ja representada por contexto/area | Sim, ja preservada | Vincula o Projeto ao ambiente operacional que deu origem ao monitoramento. |
| Responsavel pelo encerramento | Permanente futura | Sim, se o encerramento exigir autoria formal | Sim, quando existir | Ajuda a auditar quem formalizou o fim operacional do Projeto. |
| Responsavel pelo arquivamento | Permanente futura | Sim, se houver necessidade de custodia | Sim, como referencia documental se existir | Ajuda a preservar a rastreabilidade da custodia apos encerramento. |
| Responsavel pela geracao do Dossie Final | Permanente documental futura | Sim, se a geracao do Dossie for formalizada | Sim | Identifica quem consolidou a memoria documental sem substituir os dados operacionais. |
| Supervisor tecnico | Opcional | Nao agora | Apenas se formalmente definido | Pode agregar valor em Projetos mais complexos, mas ainda nao ha necessidade objetiva. |
| Aprovador de encerramento | Opcional/futuro | Nao agora | Apenas se workflow de aprovacao for aprovado | Exige conceito de aprovacao ainda fora do escopo atual. |

## Matriz De Exclusao

| Responsabilidade | Excluir Do Dominio Permanente? | Excluir Do Dossie? | Justificativa |
| --- | --- | --- | --- |
| Operadores eventuais | Sim | Sim | Pertencem a rotina diaria e podem gerar ruido documental. |
| Substituicoes temporarias | Sim | Sim | Sao eventos operacionais, nao memoria permanente do Projeto. |
| Responsaveis por lancamentos pontuais | Sim | Sim | Atribuicao granular deve permanecer em logs ou trilhas operacionais, quando existirem. |
| Responsabilidades internas de interface | Sim | Sim | Nao representam responsabilidade de dominio. |
| Responsabilidades de sistemas, adapters ou motores | Sim | Sim | Componentes tecnicos produzem evidencias, mas nao respondem pelo Projeto. |
| Aprovacoes informais | Sim | Sim | Sem formalizacao de workflow, nao devem ser promovidas a responsabilidade permanente. |
| Tarefas administrativas de rotina | Sim | Sim | Podem apoiar a operacao, mas nao explicam o Projeto anos depois. |

## Responsabilidades Permanentes

Responsabilidades permanentes sao aquelas que ajudam a compreender o Projeto mesmo apos seu encerramento ou arquivamento.

Nesta auditoria, elas sao:

* responsavel principal pelo Projeto, como conceito recomendado para evolucao futura;
* coletor responsavel principal, ja existente;
* area operacional responsavel ou contexto operacional, ja representado;
* responsavel pelo encerramento, se o encerramento passar a exigir autoria formal;
* responsavel pelo arquivamento, se a custodia documental passar a exigir rastreabilidade;
* responsavel pela geracao do Dossie Final, se a geracao minima do Dossie for formalizada em GP futura.

Essas responsabilidades agregam valor porque conectam a memoria do Projeto a pessoas, areas ou autoridades que explicam sua conducao, fechamento e preservacao.

## Responsabilidades Operacionais

Responsabilidades operacionais sao necessarias para executar o monitoramento, mas nao devem ser automaticamente elevadas a memoria permanente.

Incluem:

* operadores de medicoes individuais;
* lancadores de dados;
* revisores pontuais;
* substitutos temporarios;
* contatos operacionais ocasionais;
* tarefas administrativas de rotina;
* execucoes internas de componentes tecnicos.

Essas informacoes podem existir em fontes operacionais, logs ou trilhas futuras, mas nao devem compor o Projeto como conceito central nem o Dossie Final como memoria permanente, salvo consolidacao formal posterior.

## Impacto No Dominio

A auditoria nao altera o conceito atual de Projeto. Ela apenas delimita que responsabilidades podem vir a enriquecer o dominio sem transformar o Projeto em sistema de usuarios, workflow ou gestao administrativa.

O modelo atual permanece adequado com ressalvas: `coletor_responsavel` cobre a responsabilidade operacional minima ja aprovada, mas nao resolve a responsabilidade institucional pelo Projeto como um todo. Essa lacuna e relevante, porem nao critica para o estado atual.

## Impacto Arquitetural

As responsabilidades nao exigem nova camada arquitetural.

Tratamento recomendado por alternativa:

* Atributos diretos do Projeto: abordagem recomendada para responsabilidades permanentes simples e unicas, como responsavel principal, responsavel pelo encerramento ou responsavel pelo arquivamento, se aprovadas futuramente.
* Entidade propria: nao recomendada agora. Seria excesso estrutural sem evidencia operacional suficiente.
* Colecao pertencente ao Projeto: candidata futura apenas se houver multiplos papeis formais por Projeto, historico de substituicoes ou necessidade objetiva de auditoria de participantes.
* Referencia documental: recomendada para preservacao no Dossie Final quando a responsabilidade for permanente e ja estiver formalizada.
* Discovery candidata: nao recomendada nesta GP. A evidencia reforca Discoveries existentes, mas nao caracteriza principio novo.

## Relacao Com Encerramento

O encerramento pode exigir, em evolucao futura, registro de quem formalizou a conclusao operacional do Projeto. Esse responsavel nao deve ser confundido com aprovador, pois aprovacao implica workflow especifico ainda nao aprovado.

Para o estado atual, basta reconhecer a responsabilidade de encerramento como conceito permanente futuro. Nao ha recomendacao de implementacao imediata nesta GP.

## Relacao Com Arquivamento

O arquivamento permanece etapa distinta do encerramento. A responsabilidade ligada ao arquivamento deve representar custodia e preservacao documental, nao reabertura, aprovacao retroativa ou alteracao de conteudo.

Se materializada futuramente, essa responsabilidade deve reforcar que Projeto arquivado permanece consultavel e que o Dossie Final preserva sua substancia imutavel.

## Relacao Com Dossie Final

O Dossie Final deve preservar apenas responsabilidades com valor permanente.

Devem ser preservadas quando existirem:

* coletor responsavel principal;
* responsavel principal pelo Projeto;
* responsavel pelo encerramento;
* responsavel pela geracao do Dossie Final;
* responsavel pelo arquivamento, quando aplicavel.

Nao devem ser preservados no Dossie Final:

* operadores eventuais;
* substituicoes temporarias;
* tarefas administrativas rotineiras;
* logs de execucao;
* responsaveis por estados intermediarios;
* detalhes internos de sistemas.

O Dossie Final nao substitui dados operacionais e nao deve se tornar um cadastro completo de participantes.

## Impacto Sobre PA-01

PA-01 permanece integralmente preservado.

A auditoria nao altera o fluxo atual, nao cria obrigatoriedade de novo cadastro, nao modifica persistencia, nao interfere em Policy Engine, Motor Observacional, Analytics, Governanca, Recommendation ou Dashboard, e nao amplia o Dossie Final.

## Analise Das Discoveries

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Resultado:

* PA-02 foi reforcada: a auditoria mostra que responsabilidades podem agregar valor ao Projeto por enriquecimento do dominio existente, sem exigir nova camada.
* PA-03 foi reforcada: a auditoria recomenda materializar apenas responsabilidades com necessidade objetiva e valor permanente, evitando criar entidade ou colecao antes da demanda real.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida.
* Nenhuma nova Discovery candidata foi identificada.

## Conclusao

O dominio do Projeto ja possui uma responsabilidade operacional minima por meio de `coletor_responsavel`, mas ainda nao possui modelo institucional completo de responsabilidades. Essa ausencia nao impede o funcionamento atual, mas limita a rastreabilidade futura de encerramento, arquivamento e geracao documental.

A recomendacao e manter o modelo simples no estado atual e reconhecer, para evolucao futura, responsabilidades permanentes como atributos diretos ou referencias documentais, desde que cada inclusao demonstre valor operacional claro.

## Veredito Final

Modelo de responsabilidades suportado com ressalvas.


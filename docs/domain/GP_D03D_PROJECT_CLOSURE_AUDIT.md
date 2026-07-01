# GP-D03D - Auditoria dos Estados e Criterios de Encerramento do Projeto

## Data

30/06/2026

## Objetivo

Auditar o conceito de Encerramento do Projeto de Monitoramento e definir, em nivel de dominio, quando um Projeto pode ser considerado oficialmente encerrado.

Esta GP e exclusivamente documental. Nenhum codigo, runtime, interface, CSV, arquitetura, Policy Engine, Motor Observacional, Analytics, Governanca, Recommendation ou Dashboard foi alterado.

## Contexto

O CASE-01 possui arquitetura consolidada pela GP-A23 e dominio de Projeto evoluido pelas GPs D01A, D01B, D01C, D02A e D02B.

A GP-D03A auditou o ciclo de vida e concluiu que o ciclo e suportado com ressalvas. A GP-D03B classificou as ressalvas como importantes. A GP-D03C priorizou a frente de Encerramento do Projeto como primeira evolucao de dominio a ser tratada.

## Pergunta Central

O que caracteriza um Projeto de Monitoramento encerrado e quais criterios devem ser satisfeitos antes que esse estado seja alcancado?

## Metodo

1. Auditoria passiva da GP-D03A, GP-D03B e GP-D03C.
2. Leitura do modelo atual de Projeto de Monitoramento.
3. Reconstrucao do conceito de encerramento em nivel de dominio.
4. Definicao de estados auditados e criterios minimos.
5. Aplicacao do filtro institucional "Agrega Valor ao Projeto?".
6. Consulta obrigatoria ao `DISCOVERY_CATALOG.md`.
7. Registro documental das conclusoes.

## Definicao Do Encerramento

Encerramento do Projeto e o marco operacional que declara que um Projeto de Monitoramento concluiu sua execucao, consolidou seus resultados e nao deve mais receber novas medicoes, alteracoes de escopo operacional ou reprocessamento informal como se ainda estivesse ativo.

Encerramento nao e avaliacao observacional. Encerramento nao decide se a agua esta normal, em atencao ou critica. Encerramento apenas declara que o ciclo operacional do Projeto foi concluido e que seus artefatos finais devem ser preservados.

Em termos de dominio:

* Projeto Ativo produz dados e conhecimento.
* Projeto Encerrado congela o ciclo operacional e consolida a memoria final.
* Projeto Arquivado preserva o Projeto encerrado para consulta historica.

## Estados Auditados

| Estado | Definicao | Agrega Valor ao Projeto? | Recomendacao |
| --- | --- | --- | --- |
| Ativo | Projeto em execucao, apto a receber medicoes, atualizacoes operacionais e sinais derivados. | Sim | Manter como estado operacional principal |
| Encerrado | Projeto concluido, com criterios minimos atendidos, dossie final consolidado e dados operacionais congelados. | Sim | Recomendar como novo estado de dominio futuro |
| Arquivado | Projeto encerrado preservado para consulta historica, sem expectativa de acao operacional. | Sim, apos encerramento | Recomendar como etapa distinta e posterior |
| Inativo | Estado atual implementado, mas sem semantica suficiente para substituir encerrado ou arquivado. | Parcial | Reavaliar em GP futura antes de implementar estados |
| Pausado | Projeto temporariamente suspenso, ainda nao concluido. | Parcial | Adiar; nao e necessario para definir encerramento minimo |
| Rascunho | Projeto em preparacao antes de iniciar execucao. | Futuro | Adiar; depende de planejamento formal |

## Diferenca Entre Projeto Ativo, Encerrado E Arquivado

### Projeto Ativo

Projeto Ativo e a unidade operacional vigente. Ele pode receber medicoes, gerar novos sinais analiticos, produzir eventos de governanca, alimentar recomendacoes executivas e atualizar visualizacoes.

No estado ativo, o contexto do Projeto ainda pode orientar a operacao. Alteracoes devem continuar restritas ao modelo aprovado e nao podem alterar PA-01.

### Projeto Encerrado

Projeto Encerrado e um Projeto cuja execucao foi formalmente concluida. Ele nao deve receber novas medicoes como parte do mesmo ciclo operacional.

O encerramento deve congelar:

* identidade do Projeto;
* cliente;
* contexto operacional;
* perfil operacional;
* ponto principal de coleta;
* coletor responsavel registrado;
* periodo operacional considerado;
* referencia aos datasets ou medicoes consideradas;
* snapshots finais ou relatorios consolidados;
* justificativa e data do encerramento;
* autoridade que encerrou.

### Projeto Arquivado

Projeto Arquivado e um Projeto ja encerrado que foi movido para preservacao historica. Arquivamento e uma etapa distinta, posterior ao encerramento.

Arquivamento nao deve ser confundido com arquivamento de eventos de Governanca Operacional. Um evento arquivado nao encerra nem arquiva o Projeto.

## Arquivamento

Arquivamento representa etapa distinta do encerramento.

Encerramento responde:

* o Projeto acabou?
* os criterios minimos foram satisfeitos?
* o dossie final foi consolidado?

Arquivamento responde:

* o Projeto encerrado deve sair da visao operacional corrente?
* como ele permanece consultavel?
* qual memoria deve ser preservada a longo prazo?

Agrega Valor ao Projeto?

Sim, mas apenas apos existir encerramento. Implementar arquivamento antes de encerramento criaria ambiguidade.

## Autoridade

A autoridade para encerrar um Projeto deve ser operacional/institucional, nao tecnica-observacional.

Autoridade recomendada:

* Responsavel pelo Projeto de Monitoramento; ou
* operador autorizado pelo responsavel institucional; ou
* papel equivalente definido por GP futura de governanca de Projeto.

Nao possuem autoridade para encerrar Projeto:

* `PolicyEngine`;
* `AvaliacaoObservacionalService`;
* Analytics;
* Governanca Operacional de eventos;
* Executive Recommendation;
* Dashboard;
* Relatorios.

Esses componentes produzem evidencias ou sinais, mas nao decidem encerramento.

## Criterios Minimos

Um Projeto pode ser considerado encerrado quando, no minimo, os seguintes criterios estiverem satisfeitos ou formalmente justificados:

| Criterio | Obrigatoriedade | Justificativa de valor |
| --- | --- | --- |
| Projeto identificado e ativo antes do encerramento | Obrigatorio | Evita encerrar entidade ambigua |
| Periodo operacional definido | Obrigatorio | Delimita o que pertence ao ciclo encerrado |
| Medicoes previstas concluidas ou ausencia de plano formal documentada | Obrigatorio com ressalva | Evita falso encerramento quando ainda havia coleta esperada |
| Pendencias operacionais inexistentes ou explicitamente registradas | Obrigatorio | Torna o fechamento auditavel |
| Analytics final disponivel ou impossibilidade documentada | Obrigatorio com ressalva | Consolida tendencias, alertas e Water Health Score quando houver dados |
| Eventos de Governanca ativos resolvidos, arquivados ou justificados | Obrigatorio com ressalva | Evita encerrar Projeto ignorando ocorrencias abertas |
| Recomendacoes executivas finais emitidas ou impossibilidade documentada | Obrigatorio com ressalva | Preserva a sintese executiva do conhecimento produzido |
| Relatorio operacional consolidado | Obrigatorio | Fornece artefato final minimo |
| Dossie Final criado ou referenciado | Obrigatorio em GP futura | Consolida memoria institucional do Projeto |
| Responsavel pelo encerramento registrado | Obrigatorio | Define autoridade e rastreabilidade |
| Data de encerramento registrada | Obrigatorio | Permite separar operacao ativa de historico |

Esses criterios agregam valor porque impedem que encerramento seja apenas troca de `status`.

## Dossie Final

O Dossie Final e o conjunto documental que representa a memoria oficial do Projeto encerrado.

Documentos e artefatos recomendados para o Dossie Final:

* identificacao do Projeto;
* cliente;
* contexto operacional;
* perfil operacional;
* ponto principal de coleta;
* coletor responsavel;
* periodo considerado;
* resumo das medicoes consideradas;
* referencia aos CSVs ou datasets vigentes, sem alterar schema;
* relatorio operacional consolidado;
* resumo final do Water Health Score, quando disponivel;
* alertas analiticos relevantes;
* resumo de eventos de Governanca Operacional;
* recomendacoes executivas finais;
* pendencias ou excecoes justificadas;
* termo ou registro de encerramento;
* data e autoridade do encerramento.

O Dossie Final nao deve recalcular avaliacao observacional. Ele deve consolidar artefatos existentes e seus sinais finais.

## O Que Deve Permanecer Editavel

Apos encerramento, devem permanecer editaveis apenas informacoes administrativas que nao alterem a substancia operacional do Projeto encerrado:

* notas administrativas posteriores;
* localizacao do arquivo ou referencia documental;
* observacoes de auditoria;
* marcador de arquivamento futuro;
* metadados de custodia documental simples, se aprovados futuramente.

Essas edicoes devem ser tratadas como anotacoes posteriores, nao como alteracoes no ciclo encerrado.

## O Que Deve Tornar-Se Somente Leitura

Apos encerramento, devem tornar-se somente leitura:

* nome do Projeto;
* cliente;
* contexto operacional;
* perfil operacional;
* ponto principal de coleta;
* coletor responsavel do ciclo;
* data de criacao;
* data de encerramento;
* medicoes consideradas;
* relatorios consolidados;
* resultados observacionais ja produzidos;
* snapshots analiticos considerados;
* eventos de governanca vinculados ao ciclo;
* recomendacoes finais.

Agrega Valor ao Projeto?

Sim. Somente leitura preserva rastreabilidade e evita reescrever historico operacional.

## Informacoes Permanentemente Acessiveis

Mesmo encerrado ou arquivado, o Projeto deve manter acesso permanente a:

* dados minimos do Projeto;
* contexto operacional e perfil operacional;
* periodo operacional considerado;
* medicoes ou datasets de referencia;
* resultados observacionais utilizados;
* tendencias, alertas e score consolidados;
* eventos de governanca associados;
* recomendacoes executivas;
* relatorios e Dossie Final;
* justificativa do encerramento;
* autoridade e data de encerramento.

## Responsabilidades

| Responsabilidade | Autoridade recomendada | Observacao |
| --- | --- | --- |
| Declarar encerramento | Responsavel operacional/institucional do Projeto | Nao e autoridade observacional |
| Consolidar relatorio operacional | Relatorios / processo documental futuro | Deve consumir sinais existentes |
| Consolidar sinais analiticos | Analytics | Sem mudar regras nesta GP |
| Informar eventos ativos | Governanca Operacional | Evento nao decide encerramento sozinho |
| Emitir recomendacoes finais | Executive Recommendation | Consome sinais consolidados |
| Apresentar estado do Projeto | Interface futura, se aprovada | Nao implementado nesta GP |
| Preservar historico | Dominio de Projeto / persistencia futura | Sem alterar CSVs nesta GP |

## Responsabilidade Ainda Nao Representada

A responsabilidade ainda nao representada e a autoridade de encerramento do Projeto.

Hoje o sistema possui `status` simples no Projeto, mas nao possui:

* criterio de transicao;
* autoridade de encerramento;
* data de encerramento;
* justificativa;
* Dossie Final;
* distincao formal entre encerrado e arquivado.

Essa responsabilidade deve pertencer ao dominio de Projeto, com processo institucional claro.

## Novos Estados Do Projeto

Existe necessidade de novos estados de Projeto.

Estados minimos recomendados para GP futura:

* `ativo`;
* `encerrado`;
* `arquivado`.

Estados adiados:

* `rascunho`;
* `pausado`.

Justificativa:

* `ativo` ja representa operacao corrente.
* `encerrado` agrega valor por formalizar conclusao.
* `arquivado` agrega valor por separar preservacao historica da operacao corrente.
* `rascunho` depende de Planejamento.
* `pausado` depende de necessidade operacional ainda nao demonstrada.

## Novos Conceitos De Dominio

Conceitos de dominio recomendados para auditoria futura:

* Estado de Projeto;
* Criterio de Encerramento;
* Registro de Encerramento;
* Dossie Final.

Conceitos nao recomendados agora:

* assinatura digital;
* cadeia completa de custodia;
* lacre;
* anexos obrigatorios;
* multiplos responsaveis;
* workflow de aprovacao multiusuario.

Esses conceitos podem agregar valor em cenarios maiores, mas nao sao necessarios para o modelo minimo de encerramento.

## Relacao Com PA-01

Encerramento nao interfere no PA-01.

O PA-01 permanece preservado se:

* Projeto nao selecionar politica;
* Projeto nao executar avaliacao;
* Projeto nao interpretar parametro;
* Projeto nao recalcular status observacional;
* Projeto nao recalcular score;
* Dossie Final apenas consolidar sinais existentes;
* autoridade de encerramento for operacional/institucional, nao observacional.

## Impacto Arquitetural

Nao existe necessidade de nova camada arquitetural.

O encerramento deve ser tratado como enriquecimento do dominio de Projeto, preservando a arquitetura GP-A23:

Coleta -> Monitoramento Hidrico -> Analytics -> Governanca Operacional -> Executive Recommendation -> Executive Intelligence -> Painel Executivo.

## Impacto Sobre Persistencia

Esta GP nao altera persistencia.

Uma GP futura pode avaliar campos ou artefatos como:

* estado do Projeto;
* data de encerramento;
* responsavel pelo encerramento;
* justificativa;
* referencia ao Dossie Final.

Qualquer materializacao deve respeitar PA-03 e so ocorrer quando houver necessidade objetiva.

## Oportunidades Futuras

Oportunidades recomendadas:

1. GP-D03E - Implementacao minima dos estados `ativo`, `encerrado` e `arquivado`, se aprovada.
2. GP-D08A - Auditoria do Dossie Final do Projeto.
3. GP-D04A - Auditoria do Planejamento de Monitoramento.
4. GP-D01D - Reavaliacao de persistencia Medicao -> Projeto apenas quando houver multiplos Projetos ou migracao.

Nenhuma oportunidade deve ser implementada automaticamente por esta GP.

## Relacao Com O DISCOVERY_CATALOG

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Impacto registrado:

* PA-02 - Progressao De Valor: reforcada. O encerramento agrega valor por enriquecimento do dominio de Projeto, sem nova camada.
* PA-03 - Materializacao Sob Necessidade: reforcada. Estados e registros de encerramento devem ser materializados apenas apos auditoria e necessidade objetiva.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida automaticamente.
* Nenhuma nova Discovery candidata foi identificada nesta GP.

## Aplicacao Do Filtro "Agrega Valor Ao Projeto?"

| Recomendacao | Agrega valor? | Beneficio operacional |
| --- | --- | --- |
| Definir `encerrado` como estado distinto | Sim | Permite concluir formalmente o Projeto |
| Separar `encerrado` de `arquivado` | Sim | Evita confundir fechamento operacional com preservacao historica |
| Exigir criterios minimos antes do encerramento | Sim | Evita troca de status sem evidencia |
| Criar Dossie Final em GP futura | Sim | Consolida memoria auditavel do Projeto |
| Manter PA-01 fora do encerramento | Sim | Preserva autoridade observacional central |
| Adiar `rascunho` e `pausado` | Sim | Evita ampliar escopo sem necessidade comprovada |
| Nao criar nova camada | Sim | Preserva GP-A23 e reduz complexidade |

## Respostas Obrigatorias

### 1. O que significa Encerramento do Projeto?

Significa declarar que o ciclo operacional do Projeto foi concluido, que os resultados foram consolidados e que novas medicoes nao devem ser registradas como parte desse Projeto.

### 2. Quem possui autoridade para encerrar um Projeto?

O responsavel operacional/institucional pelo Projeto ou operador autorizado. Camadas tecnicas nao encerram Projeto.

### 3. Quais condicoes minimas devem existir antes do encerramento?

Projeto identificado, periodo delimitado, medicoes previstas concluidas ou justificadas, pendencias registradas, Analytics final disponivel ou justificado, eventos ativos resolvidos ou justificados, recomendacoes finais emitidas ou justificadas, relatorio consolidado, Dossie Final e autoridade/data de encerramento.

### 4. Quais documentos passam a integrar o Dossie Final do Projeto?

Identificacao do Projeto, contexto, periodo, resumo de medicoes, referencias aos datasets, relatorio operacional, Water Health Score final, alertas, eventos, recomendacoes, pendencias, excecoes e registro de encerramento.

### 5. O que deve permanecer editavel?

Apenas anotacoes administrativas posteriores e referencias documentais que nao alterem o historico operacional encerrado.

### 6. O que deve tornar-se somente leitura?

Identidade, contexto, perfil, ponto, coletor, periodo, medicoes consideradas, relatorios, resultados observacionais, snapshots, eventos, recomendacoes finais e registro de encerramento.

### 7. Quais informacoes devem permanecer permanentemente acessiveis?

Dados do Projeto, contexto, periodo, medicoes/datasets, resultados observacionais, sinais analiticos, eventos, recomendacoes, relatorios, Dossie Final, autoridade e data de encerramento.

### 8. Qual a diferenca entre Projeto Ativo, Projeto Arquivado e Projeto Encerrado?

Ativo esta em execucao. Encerrado concluiu o ciclo operacional e congelou sua memoria. Arquivado e um Projeto encerrado preservado para consulta historica.

### 9. Arquivamento faz parte do Encerramento ou representa etapa distinta?

Arquivamento representa etapa distinta e posterior ao encerramento.

### 10. O Encerramento interfere no PA-01?

Nao. Encerramento nao seleciona politica, nao executa avaliacao e nao interpreta limites.

### 11. Existe necessidade de novos estados do Projeto?

Sim. Estados minimos recomendados: `ativo`, `encerrado` e `arquivado`.

### 12. Existe necessidade de nova camada arquitetural?

Nao.

### 13. Existe necessidade de novos conceitos de dominio?

Sim, em auditoria futura: Estado de Projeto, Criterio de Encerramento, Registro de Encerramento e Dossie Final.

### 14. Existe alguma responsabilidade ainda nao representada?

Sim. A autoridade de encerramento e o processo de fechamento formal ainda nao estao representados.

### 15. Agrega Valor ao Projeto?

Sim. Encerramento agrega valor porque transforma monitoramento continuo em Projeto completo, rastreavel e auditavel.

## Conclusao

O conceito de Encerramento e adequado ao CASE-01 e deve ser tratado como evolucao de dominio do Projeto, sem nova camada arquitetural.

O modelo atual ainda nao implementa encerramento, mas ja possui base suficiente para uma evolucao minima: Projeto, contexto operacional, perfil operacional, medicoes, Analytics, Governanca, Recommendation, Relatorios e Dashboard.

O encerramento deve ser formal, rastreavel, baseado em criterios minimos e separado de arquivamento.

## Veredito

**Modelo suportado com ressalvas.**

O modelo de Encerramento e suportado pela arquitetura atual e recomendado como proxima evolucao de dominio, mas depende de GP futura para implementacao controlada dos estados `ativo`, `encerrado` e `arquivado`, alem de definicao material do Registro de Encerramento e do Dossie Final.

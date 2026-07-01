# GP-D03B - Auditoria Das Ressalvas Do Ciclo De Vida

## Data

30/06/2026

## Contexto

O CASE-01 segue a metodologia ICFACTORY e possui arquitetura consolidada pela GP-A23.

No dominio, o Projeto de Monitoramento foi aprovado pela GP-D01A, implementado pela GP-D01B, teve a estrategia de persistencia auditada pela GP-D01C, recebeu Contexto Operacional pela GP-D02A/GP-D02B e teve seu ciclo de vida auditado pela GP-D03A.

A GP-D03A concluiu:

**Ciclo de Vida suportado com ressalvas.**

Esta GP-D03B audita exclusivamente essas ressalvas, sem criar funcionalidades, sem alterar codigo e sem promover Discoveries.

## Objetivo

Compreender exatamente quais lacunas impediram que o veredito da GP-D03A fosse "Ciclo de Vida suportado e recomendado" e qual e o impacto real de cada uma.

## Pergunta Central

Quais ressalvas impediram a aprovacao plena do Ciclo de Vida e qual e o impacto real de cada uma?

## Metodo

1. Leitura integral da GP-D03A.
2. Extracao das ressalvas explicitas e recorrentes no relatorio.
3. Agrupamento das ressalvas por etapa do ciclo de vida.
4. Classificacao por natureza: dominio, arquitetura, persistencia, interface, processo ou documentacao.
5. Classificacao por impacto operacional.
6. Aplicacao do filtro "Agrega Valor Ao Projeto?".
7. Definicao de prioridade de tratamento.
8. Consulta obrigatoria ao `DISCOVERY_CATALOG.md`.
9. Registro documental.

## Resumo Do Veredito Da GP-D03A

A GP-D03A reconheceu que o CASE-01 possui uma cadeia operacional e analitica coerente:

Projeto -> Contexto Operacional -> Coletas -> Medicoes -> Monitoramento Hidrico -> Analytics -> Governanca -> Executive Recommendation -> Executive Intelligence -> Dashboard/Relatorios.

O veredito nao foi pleno porque o sistema ainda representa melhor a operacao continua de monitoramento do que o ciclo completo de um Projeto de Monitoramento real.

As ressalvas se concentram em:

* planejamento;
* estados do Projeto;
* vinculo Projeto -> Configuracao;
* Amostra;
* rastreabilidade historica Projeto -> Medicao;
* recorte analitico por Projeto;
* relatorio final ou dossie;
* arquivamento do Projeto;
* encerramento do Projeto.

## Lista Completa Das Ressalvas

### Ressalva 1 - Planejamento Do Projeto Ausente

**Qual e exatamente a ressalva?**

O CASE-01 ainda nao possui artefato de planejamento que defina objetivo, periodo, frequencia, campanha, parametros esperados e criterios de conclusao.

**Etapa do ciclo de vida:** Planejamento.

**Natureza:** dominio, processo e documentacao.

**Impacto operacional:** importante.

Sem planejamento, o Projeto existe como contexto operacional, mas nao como plano completo de execucao. Isso reduz a capacidade de demonstrar que as coletas realizadas seguem um escopo previamente definido.

**Afeta o PA-01?** Nao.

**Exige nova camada arquitetural?** Nao.

**Exige alteracao do dominio?** Sim, se for implementado no futuro.

**Exige apenas enriquecimento das estruturas existentes?** Sim. Deve enriquecer o dominio do Projeto ou um conceito associado, sem criar camada nova.

**Agrega Valor Ao Projeto?** Sim.

Agrega valor porque conecta Projeto e coletas, reduz ambiguidade operacional e permite avaliar se o monitoramento foi executado conforme escopo.

**Deve ser implementada imediatamente?** Implementar posteriormente.

**GP futura sugerida:** GP-D04A - Auditoria do Planejamento de Monitoramento.

### Ressalva 2 - Estados Do Projeto Ainda Nao Auditados

**Qual e exatamente a ressalva?**

A GP-D03A indicou que estados como rascunho, ativo, pausado, encerrado e arquivado deveriam ser auditados antes de qualquer implementacao funcional.

**Etapa do ciclo de vida:** Projeto, Arquivamento e Encerramento.

**Natureza:** dominio, processo e documentacao.

**Impacto operacional:** importante.

Sem estados claros, o campo `status` do Projeto corre o risco de virar texto sem semantica operacional, impedindo diferenciar Projeto ativo, encerrado ou arquivado.

**Afeta o PA-01?** Nao.

**Exige nova camada arquitetural?** Nao.

**Exige alteracao do dominio?** Sim, se aprovado em GP futura.

**Exige apenas enriquecimento das estruturas existentes?** Sim.

**Agrega Valor Ao Projeto?** Sim.

Agrega valor porque cria fronteiras objetivas para nascimento, pausa, encerramento e arquivamento, sem transferir autoridade observacional para o Projeto.

**Deve ser implementada imediatamente?** Implementar posteriormente.

**GP futura sugerida:** GP-D03C - Auditoria dos Estados do Projeto de Monitoramento.

### Ressalva 3 - Vinculo Projeto -> Configuracao Ausente

**Qual e exatamente a ressalva?**

A Configuracao Operacional existe, mas nao esta formalmente associada ao Projeto. A GP-D03A considerou isso aceitavel no estado atual, porem limitado para rastrear contexto, perfil operacional e parametrizacao aplicada.

**Etapa do ciclo de vida:** Configuracao.

**Natureza:** dominio e documentacao; futuramente persistencia, se materializado.

**Impacto operacional:** desejavel.

A ausencia do vinculo nao impede o monitoramento atual, mas limita a explicacao de qual configuracao foi considerada para um Projeto especifico.

**Afeta o PA-01?** Nao, desde que o Projeto continue apenas fornecendo contexto.

**Exige nova camada arquitetural?** Nao.

**Exige alteracao do dominio?** Possivelmente, em GP futura.

**Exige apenas enriquecimento das estruturas existentes?** Sim.

**Agrega Valor Ao Projeto?** Sim, com ressalvas.

Agrega valor quando houver necessidade de demonstrar configuracao aplicada por Projeto. No estado atual, o valor ainda nao exige implementacao imediata.

**Deve ser implementada imediatamente?** Manter apenas documentada.

**GP futura sugerida:** GP-D05A - Auditoria do Vinculo Projeto -> Configuracao Operacional.

### Ressalva 4 - Amostra Formal Ausente

**Qual e exatamente a ressalva?**

Amostra permanece conceito conceitual nao implementado. O sistema registra medicoes, mas nao possui uma unidade formal de coleta que agrupe medicoes realizadas em uma mesma ocorrencia.

**Etapa do ciclo de vida:** Coletas e Medicoes.

**Natureza:** dominio, processo e futuramente persistencia.

**Impacto operacional:** futuro.

Enquanto o sistema opera com Projeto ativo unico e medicoes simples, a ausencia de Amostra nao bloqueia o fluxo. Ela passa a importar quando houver multiplas medicoes por visita, multiplos parametros agrupados ou necessidade de rastrear ocorrencias de coleta.

**Afeta o PA-01?** Nao.

**Exige nova camada arquitetural?** Nao.

**Exige alteracao do dominio?** Sim, se for promovida futuramente.

**Exige apenas enriquecimento das estruturas existentes?** Sim.

**Agrega Valor Ao Projeto?** Parcialmente.

Agrega valor em cenarios mais complexos. No MVP atual, implementa-la agora criaria complexidade antes da necessidade.

**Deve ser implementada imediatamente?** Manter apenas documentada.

**GP futura sugerida:** GP-D06A - Auditoria de Amostra Como Unidade de Coleta.

### Ressalva 5 - Rastreabilidade Historica Medicao -> Projeto Ainda Contextual

**Qual e exatamente a ressalva?**

A relacao Medicao -> Projeto permanece contextual pelo Projeto ativo unico, conforme GP-D01C. A GP-D03A registrou que isso e adequado agora, mas nao oferece rastreabilidade historica forte para multiplos projetos.

**Etapa do ciclo de vida:** Medicoes e Rastreabilidade.

**Natureza:** persistencia, dominio e documentacao.

**Impacto operacional:** desejavel.

Nao bloqueia a operacao atual, mas podera gerar ambiguidade se o sistema permitir troca historica de Projeto ativo ou multiplos Projetos.

**Afeta o PA-01?** Nao.

**Exige nova camada arquitetural?** Nao.

**Exige alteracao do dominio?** Nao necessariamente; a relacao conceitual ja existe.

**Exige apenas enriquecimento das estruturas existentes?** Sim, quando houver necessidade real.

**Agrega Valor Ao Projeto?** Sim, mas nao agora.

Agrega valor para rastreabilidade futura, mas materializar cedo demais contradiz a GP-D01C e reforcaria complexidade prematura.

**Deve ser implementada imediatamente?** Manter apenas documentada.

**GP futura sugerida:** GP-D01D - Reavaliacao Da Persistencia Medicao -> Projeto Quando Houver Multiplos Projetos.

### Ressalva 6 - Analytics Ainda Nao E Recortado Por Projeto Historico

**Qual e exatamente a ressalva?**

Analytics calcula tendencias, alertas e Water Health Score a partir dos datasets vigentes, mas ainda nao possui recorte historico formal por Projeto.

**Etapa do ciclo de vida:** Analytics.

**Natureza:** dominio, persistencia e analytics.

**Impacto operacional:** futuro.

No modo de Projeto ativo unico, o recorte por Projeto e implicito. O impacto aparece apenas quando houver multiplos Projetos, troca historica de Projeto ativo ou necessidade de comparacao entre Projetos.

**Afeta o PA-01?** Nao.

**Exige nova camada arquitetural?** Nao.

**Exige alteracao do dominio?** Depende da evolucao futura da persistencia Projeto -> Medicao.

**Exige apenas enriquecimento das estruturas existentes?** Sim.

**Agrega Valor Ao Projeto?** Parcialmente.

Agrega valor futuro para analise por Projeto, mas nao agrega valor objetivo suficiente no estado atual de Projeto ativo unico.

**Deve ser implementada imediatamente?** Manter apenas documentada.

**GP futura sugerida:** GP-D07A - Auditoria de Recorte Analitico Por Projeto.

### Ressalva 7 - Relatorio Final Ou Dossie Do Projeto Ausente

**Qual e exatamente a ressalva?**

Relatorios operacionais existem, mas nao representam um dossie final do Projeto com escopo, periodo, dados coletados, sinais produzidos, eventos governados, recomendacoes e conclusao.

**Etapa do ciclo de vida:** Relatorios e Encerramento.

**Natureza:** processo, documentacao, dominio e interface futura.

**Impacto operacional:** importante.

Sem dossie final, o ciclo produz conhecimento durante a operacao, mas nao consolida formalmente a memoria final do Projeto.

**Afeta o PA-01?** Nao, desde que o relatorio consuma resultados consolidados.

**Exige nova camada arquitetural?** Nao.

**Exige alteracao do dominio?** Possivelmente, se houver entidade/artefato de encerramento.

**Exige apenas enriquecimento das estruturas existentes?** Sim.

**Agrega Valor Ao Projeto?** Sim.

Agrega valor porque transforma sinais dispersos em evidencia final auditavel do Projeto, sem criar nova autoridade observacional.

**Deve ser implementada imediatamente?** Implementar posteriormente.

**GP futura sugerida:** GP-D08A - Auditoria do Dossie Final do Projeto.

### Ressalva 8 - Arquivamento Do Projeto Ausente

**Qual e exatamente a ressalva?**

Governanca arquiva eventos, mas Projeto nao possui arquivamento proprio. Evento arquivado nao equivale a Projeto arquivado.

**Etapa do ciclo de vida:** Arquivamento.

**Natureza:** dominio, processo e documentacao.

**Impacto operacional:** importante.

Sem arquivamento de Projeto, nao existe marco que indique que o Projeto foi preservado como historico e nao deve mais ser tratado como operacao ativa.

**Afeta o PA-01?** Nao.

**Exige nova camada arquitetural?** Nao.

**Exige alteracao do dominio?** Sim, se aprovado futuramente.

**Exige apenas enriquecimento das estruturas existentes?** Sim.

**Agrega Valor Ao Projeto?** Sim.

Agrega valor porque separa ciclo de eventos de ciclo de Projeto e evita duplicacao de autoridade.

**Deve ser implementada imediatamente?** Implementar posteriormente.

**GP futura sugerida:** GP-D03C deve auditar o estado `arquivado`; uma GP posterior deve implementar se aprovado.

### Ressalva 9 - Encerramento Do Projeto Ausente

**Qual e exatamente a ressalva?**

Nao existe fechamento formal do Projeto, criterio de encerramento, resumo final, congelamento de contexto ou decisao de que o Projeto terminou.

**Etapa do ciclo de vida:** Encerramento.

**Natureza:** dominio, processo, documentacao e possivelmente interface futura.

**Impacto operacional:** importante.

Esta e a ressalva mais forte da GP-D03A. Sem encerramento, o CASE-01 acompanha bem a operacao, mas nao conclui formalmente o Projeto de Monitoramento.

**Afeta o PA-01?** Nao, desde que encerramento nao reavalie parametros nem decida status observacional.

**Exige nova camada arquitetural?** Nao.

**Exige alteracao do dominio?** Sim, se implementado.

**Exige apenas enriquecimento das estruturas existentes?** Sim.

**Agrega Valor Ao Projeto?** Sim.

Agrega valor porque permite transformar um monitoramento continuo em Projeto completo, com conclusao auditavel.

**Deve ser implementada imediatamente?** Implementar posteriormente.

**GP futura sugerida:** GP-D03C - Auditoria dos Estados do Projeto de Monitoramento; depois GP-D03D - Implementacao Controlada Do Encerramento, se aprovada.

## Classificacao Por Impacto

| Ressalva | Impacto |
| --- | --- |
| Planejamento do Projeto ausente | Importante |
| Estados do Projeto ainda nao auditados | Importante |
| Vinculo Projeto -> Configuracao ausente | Desejavel |
| Amostra formal ausente | Futuro |
| Rastreabilidade historica Medicao -> Projeto contextual | Desejavel |
| Analytics sem recorte por Projeto historico | Futuro |
| Relatorio final ou dossie ausente | Importante |
| Arquivamento do Projeto ausente | Importante |
| Encerramento do Projeto ausente | Importante |

Nenhuma ressalva foi classificada como critica porque:

* a operacao atual continua coerente;
* PA-01 permanece preservado;
* GP-A23 permanece preservada;
* nao ha quebra de autoridade observacional;
* nao ha necessidade imediata de nova camada.

## Classificacao Por Prioridade

| Ressalva | Prioridade |
| --- | --- |
| Estados do Projeto ainda nao auditados | Implementar posteriormente, apos auditoria |
| Encerramento do Projeto ausente | Implementar posteriormente, apos auditoria |
| Planejamento do Projeto ausente | Implementar posteriormente, apos auditoria |
| Arquivamento do Projeto ausente | Implementar posteriormente, apos estados |
| Relatorio final ou dossie ausente | Implementar posteriormente |
| Vinculo Projeto -> Configuracao ausente | Manter apenas documentada |
| Rastreabilidade historica Medicao -> Projeto contextual | Manter apenas documentada |
| Amostra formal ausente | Manter apenas documentada |
| Analytics sem recorte por Projeto historico | Manter apenas documentada |

Nenhuma ressalva deve ser implementada agora nesta GP.

## Matriz "Agrega Valor?"

| Ressalva | Agrega Valor Ao Projeto? | Condicao |
| --- | --- | --- |
| Planejamento do Projeto | Sim | Auditar antes de implementar |
| Estados do Projeto | Sim | Definir semantica antes de alterar dominio |
| Vinculo Projeto -> Configuracao | Sim, com ressalvas | Implementar apenas se houver necessidade de rastrear configuracao por Projeto |
| Amostra formal | Parcialmente | Implementar apenas com agrupamento real de medicoes/coletas |
| Medicao -> Projeto historico | Sim, mas nao agora | Reavaliar quando houver multiplos Projetos ou migracao relacional |
| Analytics por Projeto | Parcialmente | Depende de persistencia ou recorte historico por Projeto |
| Dossie final | Sim | Depende de encerramento definido |
| Arquivamento do Projeto | Sim | Depende de estados do Projeto |
| Encerramento do Projeto | Sim | Depende de estados e criterios claros |

## Recomendacao Para Cada Ressalva

| Ressalva | Recomendacao |
| --- | --- |
| Planejamento | Abrir GP documental propria antes de qualquer agenda, campanha ou frequencia |
| Estados do Projeto | Priorizar auditoria de estados como proxima GP de dominio |
| Vinculo Projeto -> Configuracao | Manter registrado; nao implementar ate haver necessidade objetiva |
| Amostra | Manter conceito adiado; nao implementar no Projeto ativo unico |
| Medicao -> Projeto historico | Preservar GP-D01C; nao alterar CSVs |
| Analytics por Projeto | Aguardar necessidade de multiplos Projetos ou migracao |
| Dossie final | Auditar apos estados e encerramento |
| Arquivamento | Auditar junto com estados; nao confundir com evento arquivado |
| Encerramento | Tratar como evolucao importante, mas posterior a auditoria dos estados |

## GPs Futuras Sugeridas

1. GP-D03C - Auditoria dos Estados do Projeto de Monitoramento.
2. GP-D04A - Auditoria do Planejamento de Monitoramento.
3. GP-D05A - Auditoria do Vinculo Projeto -> Configuracao Operacional.
4. GP-D06A - Auditoria de Amostra Como Unidade de Coleta.
5. GP-D08A - Auditoria do Dossie Final do Projeto.
6. GP-D01D - Reavaliacao da Persistencia Medicao -> Projeto quando houver multiplos Projetos ou migracao relacional.

## Relacao Com O PA-01

PA-01 permanece preservado.

Nenhuma ressalva exige que Projeto, Planejamento, Amostra, Dossie, Arquivamento ou Encerramento selecionem politica, executem avaliacao ou interpretem limites.

Guardrail para GPs futuras:

* Projeto e ciclo de vida podem organizar contexto e estado operacional.
* `PolicyEngine` continua selecionando politica.
* `AvaliacaoObservacionalService` continua executando avaliacao.
* Analytics continua calculando sinais analiticos.
* Governanca continua governando eventos.
* Recommendation continua recomendando a partir de sinais consolidados.

## Impacto Arquitetural

As ressalvas nao exigem nova camada arquitetural.

A recomendacao institucional e evoluir por enriquecimento das estruturas existentes, principalmente o dominio de Projeto e seus futuros artefatos auditados, preservando a arquitetura GP-A23.

## Relacao Com O DISCOVERY_CATALOG

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Impacto registrado:

* PA-02 - Progressao De Valor: reforcada. As ressalvas podem ser tratadas por enriquecimento das estruturas existentes, sem nova camada arquitetural.
* PA-03 - Materializacao Sob Necessidade: reforcada. A auditoria confirma que conceitos como Amostra, Medicao -> Projeto historico e recorte analitico por Projeto nao devem ser materializados antes de necessidade operacional objetiva.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida automaticamente.
* Nenhuma nova Discovery candidata foi identificada nesta GP.

## Conclusao

As ressalvas da GP-D03A sao reais e impedem o veredito pleno, mas nao indicam falha critica do CASE-01.

O sistema suporta bem o monitoramento continuo e a cadeia de producao de conhecimento. O que ainda falta e formalizar o ciclo administrativo-operacional completo de Projeto: estados, planejamento, encerramento, arquivamento e memoria final.

Essas lacunas agregam valor quando tratadas em ordem, por GPs documentais e implementacoes futuras controladas. Elas nao devem ser implementadas nesta GP-D03B.

## Veredito Final

**Ressalvas importantes.**

As ressalvas impedem a aprovacao plena do Ciclo de Vida, mas nao sao criticas. Elas nao quebram PA-01, nao contradizem GP-A23, nao exigem nova camada e nao demandam implementacao imediata.

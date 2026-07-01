# GP-D03A - Auditoria do Ciclo de Vida do Projeto de Monitoramento

## Data

30/06/2026

## Objetivo

Auditar o ciclo completo de vida de um Projeto de Monitoramento Hidrico no CASE-01, avaliando se o sistema representa corretamente como um Projeto nasce, evolui, produz conhecimento operacional e pode ser encerrado dentro da arquitetura atual.

Esta auditoria e exclusivamente documental. Nenhum codigo, runtime, interface, CSV, camada arquitetural, Policy Engine, Motor Observacional, Analytics, Governanca, Recommendation ou Dashboard foi alterado.

## Pergunta Central

Como um Projeto de Monitoramento nasce, evolui, produz conhecimento e e encerrado dentro da arquitetura atual do CASE-01?

## Metodo Utilizado

O metodo aplicado foi:

1. Auditoria passiva da documentacao arquitetural, de dominio e de pesquisa.
2. Leitura das evidencias implementadas sem alterar codigo.
3. Reconstrucao do fluxo operacional real do CASE-01.
4. Separacao entre etapas existentes, parciais e ausentes.
5. Identificacao da autoridade responsavel por cada etapa.
6. Aplicacao do filtro institucional "Agrega valor ao projeto?".
7. Consulta obrigatoria ao `DISCOVERY_CATALOG.md`.
8. Registro documental do veredito e das oportunidades futuras.

## Evidencias Consultadas

Foram usadas como evidencias principais:

* `docs/architecture/CASE01_GLOBAL_ARCHITECTURE_AUDIT.md`
* `docs/architecture/INTEGRATION_AUDIT_REPORT.md`
* `docs/domain/GP_D01A_MONITORING_PROJECT_DOMAIN_AUDIT.md`
* `docs/domain/GP_D01C_PERSISTENCE_STRATEGY_AUDIT.md`
* `docs/domain/GP_D02A_OPERATIONAL_CONTEXT_AUDIT.md`
* `docs/research/DISCOVERY_CATALOG.md`
* `monitoramento_hidrico/projeto_monitoramento.py`
* `monitoramento_hidrico/configuracoes.py`
* `monitoramento_hidrico/politicas.py`
* `monitoramento_hidrico/avaliacao.py`
* `analytics/service.py`
* `analytics/repositories.py`
* `analytics/alerts.py`
* `analytics/scoring.py`
* `governance/service.py`
* `governance/rules.py`
* `executive/service.py`
* `executive_recommendation/service.py`
* `painel_executivo.py`
* `main.py`
* `relatorios.py`

## Criterio Institucional

Filtro obrigatorio:

> Agrega valor ao projeto?

Nesta auditoria, uma recomendacao agrega valor apenas quando melhora pelo menos um dos seguintes pontos sem violar GP-A23, PA-01 ou o modelo de dominio aprovado:

* clareza de responsabilidade;
* rastreabilidade objetiva;
* preservacao da simplicidade;
* preparacao para evolucao futura sem acoplamento prematuro;
* representacao mais fiel de um Projeto de Monitoramento real.

## Modelo Atual Do Ciclo De Vida

O fluxo operacional atualmente representado pode ser reconstruido assim:

Projeto de Monitoramento ativo

-> Contexto Operacional e Perfil Operacional do Projeto

-> Coletas e medicoes em CSVs operacionais

-> Nucleo de Monitoramento Hidrico

-> Analytics

-> Governanca Operacional

-> Executive Recommendation

-> Executive Intelligence

-> Dashboard Executivo e Relatorios

Esse fluxo representa bem a cadeia de producao de conhecimento a partir de medicoes. Ele ainda nao representa plenamente o ciclo de vida administrativo-operacional do Projeto, porque planejamento, arquivamento e encerramento do Projeto permanecem ausentes ou apenas implicitos.

## Matriz Das Etapas

| Etapa | Estado atual | Autoridade atual | Entradas | Saidas | Rastreabilidade | Agrega valor evoluir? |
| --- | --- | --- | --- | --- | --- | --- |
| Projeto | Representado parcialmente | Dominio de Projeto / `ProjetoMonitoramentoStore` | nome, cliente, area operacional, ponto principal, coletor, data, status, perfil operacional | Projeto ativo unico persistido | boa para contexto, fraca para historico de ciclo | Sim, para estados de ciclo e encerramento |
| Configuracao | Existente, nao vinculada ao Projeto | `ConfiguracaoOperacionalService` | perfil base, categorias, parametros | configuracao operacional | parcial, sem vinculo ao Projeto | Sim, se for vinculacao simples e auditada |
| Contexto Operacional | Representado | Projeto de Monitoramento | contexto urbano/rural/industrial/agricola | perfil operacional derivado | boa dentro do Projeto | Ja agrega valor suficiente nesta fase |
| Planejamento | Ausente | Humano/processo externo | objetivo, periodicidade, escopo, parametros esperados | plano de coletas esperado | ausente | Sim, mas exige GP propria |
| Coletas | Parcialmente representadas | Telas operacionais de coleta | dados digitados pelo operador | registros CSV | por timestamp e dataset vigente | Sim, se houver planejamento/amostra futura |
| Medicoes | Representadas operacionalmente | Modulos de coleta e repositorios analiticos | valores de parametros, timestamps | linhas CSV / modelos analiticos | boa no nivel de linha, contextual no nivel Projeto | Sim, mas persistencia Projeto->Medicao ja foi enderecada pela GP-D01C |
| Monitoramento Hidrico | Representado | `PolicyEngine` e `AvaliacaoObservacionalService` | parametro, valor, perfil/categoria quando disponivel | resultado observacional | boa por politica, status e origem do limite | Nao nesta GP; preservar |
| Analytics | Representado | `AnalyticsService` e calculadores analiticos | CSVs e resultados observacionais via adapters | tendencias, alertas, Water Health Score | boa para sinais, nao escopada por Projeto historico | Sim, futuramente para recorte por Projeto |
| Governanca Operacional | Representada para eventos | `OperationalGovernanceService` e regras de governanca | alertas consolidados | eventos com estados | forte no ciclo de eventos | Sim, futuramente para encerramento de Projeto |
| Executive Recommendation | Representada | `ExecutiveRecommendationService` | sinais consolidados de Analytics/Governanca | recomendacoes executivas e evidencias | boa em evidencias consolidadas | Nao nesta fase |
| Dashboard Executivo | Representado como apresentacao | `PainelExecutivoPage` / `DashboardPage` | snapshots, CSVs, scores e eventos | visualizacao consolidada | indireta, via fontes consumidas | Nao nesta fase |
| Relatorios | Representados operacionalmente | `RelatoriosPage` | CSVs e adapter observacional | relatorio TXT operacional | parcial; nao e dossie do Projeto | Sim, futuramente para relatorio final do Projeto |
| Arquivamento | Parcial, apenas eventos | Governanca Operacional | evento resolvido | evento arquivado | boa para evento, ausente para Projeto | Sim, para arquivamento de Projeto |
| Encerramento do Projeto | Ausente | Nao definida | criterios de conclusao, pendencias, resumo final | Projeto encerrado | ausente | Sim, com GP propria |

## Autoridade De Cada Etapa

### Projeto

O Projeto pertence ao dominio operacional/hidrico existente. Ele nao e camada arquitetural. Sua autoridade atual e armazenar o contexto minimo aprovado: nome, cliente, area operacional, ponto principal de coleta, coletor responsavel, data de criacao, status, contexto operacional e perfil operacional.

O Projeto nao seleciona politica, nao executa avaliacao, nao calcula status, nao calcula score, nao gera eventos e nao recomenda acoes.

### Configuracao

A configuracao operacional existe no Nucleo de Monitoramento Hidrico, mas ainda nao esta vinculada formalmente ao Projeto. Sua autoridade e manter perfis, categorias e parametros configuraveis. Nao ha evidencia de que ela represente um plano de Projeto.

### Contexto Operacional

O Contexto Operacional pertence ao Projeto e fornece o perfil operacional. Ele orienta o sistema apenas como contexto. A decisao sobre politica continua pertencendo ao `PolicyEngine`.

### Planejamento

Planejamento ainda nao possui artefato de dominio. Periodicidade, campanha de coletas, conjunto planejado de parametros, criterios de conclusao e escopo temporal permanecem fora do sistema.

### Coletas E Medicoes

As telas operacionais registram medicoes e persistem CSVs. Elas produzem dados, mas nao possuem autoridade observacional. A relacao conceitual Medicao -> Projeto existe pelo contexto do Projeto ativo unico, conforme GP-D01C, sem schema dedicado.

### Monitoramento Hidrico

O Nucleo de Monitoramento Hidrico permanece a autoridade observacional central. O `PolicyEngine` seleciona politica. O `AvaliacaoObservacionalService` executa avaliacao. Esta separacao preserva o PA-01.

### Analytics

Analytics transforma medicoes e resultados observacionais em tendencias, alertas preventivos e Water Health Score. Sua autoridade e analitica, nao observacional primaria.

### Governanca Operacional

Governanca sincroniza alertas em eventos, aplica estados de acompanhamento e preserva rastreabilidade de ocorrencias. O ciclo de vida de eventos esta representado, mas nao substitui o ciclo de vida do Projeto.

### Executive Recommendation

Executive Recommendation consome sinais consolidados e produz recomendacoes deterministicas com evidencias. Nao acessa CSVs, nao seleciona politicas e nao executa avaliacao observacional.

### Dashboard Executivo E Relatorios

Dashboard, Painel Executivo e Relatorios apresentam informacao. Eles nao devem assumir autoridade sobre avaliacao, governanca ou encerramento do Projeto.

### Arquivamento E Encerramento

Arquivamento existe para eventos de governanca. Arquivamento e encerramento do Projeto ainda nao existem como responsabilidades formais do dominio.

## Entradas E Saidas Por Etapa

| Etapa | Entradas | Saidas |
| --- | --- | --- |
| Projeto | dados minimos do Projeto e contexto operacional | Projeto ativo unico e perfil operacional |
| Configuracao | perfil base, categorias, parametros | configuracao operacional validada |
| Contexto Operacional | area/contexto selecionado | perfil operacional derivado |
| Planejamento | objetivo, periodo, frequencia, parametros esperados | ausente |
| Coletas | valores informados pelo operador | registros operacionais |
| Medicoes | timestamps e valores dos parametros | linhas CSV / modelos de medicao |
| Monitoramento Hidrico | parametro, valor, politica aplicavel | resultado observacional |
| Analytics | medicoes e resultados observacionais | tendencias, alertas, score |
| Governanca | alertas e metadados observacionais | eventos e estados |
| Executive Recommendation | analytics snapshot, resumo de governanca | recomendacoes e evidencias |
| Dashboard Executivo | snapshots e sinais consolidados | visao executiva |
| Relatorios | CSVs e status observacional via adapter | relatorio operacional |
| Arquivamento | evento resolvido | evento arquivado |
| Encerramento do Projeto | criterios de conclusao | ausente |

## Dependencias

As dependencias atuais respeitam a arquitetura GP-A23:

* Coletas dependem de persistencia CSV simples.
* Monitoramento Hidrico depende de catalogo, politicas e motor observacional.
* Analytics depende de repositorios e adapters observacionais.
* Governanca depende de Analytics e de enriquecimento observacional controlado.
* Executive Recommendation depende de sinais consolidados.
* Painel Executivo depende de Executive Intelligence.
* Relatorios consomem CSVs e adapter observacional.

Nao foi identificada dependencia que justifique nova camada arquitetural para o ciclo de vida do Projeto neste momento.

## Pontos De Rastreabilidade

Pontos fortes atuais:

* Medicoes possuem registro persistido em CSV.
* Resultados observacionais preservam status, politica e origem do limite.
* Alertas analiticos carregam evidencia textual e severidade.
* Eventos de governanca preservam estado, evidencias, recomendacao, metadados observacionais e ciclo de acompanhamento.
* Executive Recommendation registra evidencias por fonte e metrica.
* Relatorios e dashboard exibem dados consolidados sem assumir autoridade decisoria.

Pontos fracos atuais:

* Nao existe identificador de planejamento ou campanha.
* Nao existe amostra formal.
* A relacao Medicao -> Projeto e contextual, adequada ao Projeto ativo unico, mas nao historica para multiplos projetos.
* Nao existe manifesto de encerramento do Projeto.
* Nao existe dossie final do Projeto.
* O arquivamento de eventos nao equivale ao arquivamento do Projeto.

## Lacunas Encontradas

### Lacuna 1 - Planejamento Do Projeto

O CASE-01 ainda nao representa a etapa em que se define periodicidade, escopo temporal, parametros esperados, objetivos do monitoramento e criterios de conclusao.

Agrega valor evoluir?

Sim, porque planejamento e o elo entre Projeto e coletas. Sem ele, o Projeto existe como contexto, mas nao como plano operacional completo.

### Lacuna 2 - Vinculo Projeto -> Configuracao

A configuracao existe, mas nao esta formalmente associada ao Projeto. Isso e aceitavel no estado atual, mas limita a rastreabilidade entre contexto, perfil operacional e parametrizacao aplicada.

Agrega valor evoluir?

Sim, desde que uma GP futura comprove necessidade objetiva e nao transfira autoridade observacional para o Projeto.

### Lacuna 3 - Amostra

Amostra permanece conceito conceitual nao implementado. O sistema registra medicoes, mas nao uma ocorrencia formal de coleta que agrupe medicoes.

Agrega valor evoluir?

Parcialmente. Agrega quando houver multiplas medicoes por visita, multiplos parametros por campanha ou necessidade de rastrear coleta como unidade propria.

### Lacuna 4 - Encerramento Do Projeto

Nao existe fechamento formal do Projeto, nem criterio de encerramento, resumo final, congelamento de contexto ou dossie final.

Agrega valor evoluir?

Sim. Esta e a lacuna mais relevante para transformar o CASE-01 de sistema de acompanhamento continuo em sistema completo de Projeto de Monitoramento.

### Lacuna 5 - Arquivamento Do Projeto

Governanca arquiva eventos, mas Projeto nao possui arquivamento proprio. Isso pode gerar confusao futura se eventos forem encerrados mas o Projeto continuar ativo sem marco formal.

Agrega valor evoluir?

Sim, mas somente apos definir ciclo de estados do Projeto.

## Etapas Excedentes

Nao foram identificadas etapas claramente excedentes no fluxo atual.

Ha, porem, um cuidado arquitetural:

* Executive Recommendation e Executive Intelligence ja existem antes de haver ciclo formal de encerramento de Projeto.

Isso nao e erro, porque essas camadas agregam valor a partir de sinais consolidados atuais. Elas nao devem, entretanto, ser usadas para suprir lacunas de planejamento ou encerramento do Projeto.

## Quebras De Responsabilidade

Nao foi identificada quebra direta do PA-01 no ciclo auditado.

Tambem nao foi identificada duplicacao critica de autoridade observacional, desde que sejam mantidos os limites atuais:

* Projeto fornece contexto.
* `PolicyEngine` seleciona politica.
* `AvaliacaoObservacionalService` executa avaliacao.
* Analytics calcula tendencias, alertas e score.
* Governanca acompanha eventos.
* Recommendation recomenda a partir de sinais consolidados.
* Dashboard e Relatorios apresentam informacao.

O principal risco futuro e transformar Projeto em agregador decisorio. Isso violaria a arquitetura consolidada.

## Avaliacao Do Dominio

O dominio atual representa bem:

* Projeto ativo unico;
* cliente;
* ponto principal;
* coletor responsavel;
* contexto operacional;
* perfil operacional;
* medicoes operacionais;
* sinais observacionais, analiticos, governados e executivos.

O dominio ainda nao representa plenamente:

* planejamento de campanha;
* amostra;
* cronograma;
* criterio de conclusao;
* encerramento;
* arquivamento de Projeto;
* relatorio final do Projeto.

Portanto, o dominio e suficiente para operacao continua monitorada, mas incompleto para ciclo completo de Projeto.

## Avaliacao Arquitetural

A arquitetura GP-A23 permanece preservada.

Nao ha evidencia de necessidade de nova camada arquitetural para o ciclo de vida do Projeto. As evolucoes futuras devem ocorrer por enriquecimento disciplinado do dominio de Projeto e das camadas existentes.

O ciclo atual confirma que a cadeia Coleta -> Monitoramento Hidrico -> Analytics -> Governanca -> Executive Recommendation -> Executive Intelligence -> Painel Executivo continua coerente.

## Avaliacao Metodologica

A GP-D03A reforca a disciplina ICFACTORY:

* auditar antes de implementar;
* separar dominio de persistencia;
* evitar promocao automatica de Discoveries;
* preservar PA-01;
* aplicar "Agrega valor ao projeto?";
* nao criar camada sem necessidade objetiva.

## Relacao Com O PA-01

PA-01 permanece preservado durante todo o ciclo auditado.

Guardrails confirmados:

* Projeto nao avalia parametro.
* Projeto nao calcula status observacional.
* Projeto nao escolhe motor.
* Projeto nao interpreta limite.
* Projeto nao gera severidade observacional.
* Dashboard e Relatorios nao devem executar avaliacao propria.
* Recommendation consome sinais consolidados, nao fontes primarias.

Qualquer evolucao de ciclo de vida deve manter o Projeto como envelope operacional, nao como autoridade observacional.

## Relacao Com O DISCOVERY_CATALOG

`docs/research/DISCOVERY_CATALOG.md` foi consultado antes do encerramento desta GP.

Impacto registrado:

* PA-02 - Progressao De Valor: reforcada. A auditoria mostra que o sistema continua agregando valor por encadeamento das camadas existentes, sem necessidade de nova camada para representar o ciclo de Projeto.
* PA-03 - Materializacao Sob Necessidade: reforcada. As lacunas identificadas nao justificam materializar `projeto_id` nos CSVs ou criar artefatos fisicos antes de necessidade operacional comprovada.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida automaticamente.
* Nenhuma nova Discovery candidata foi registrada nesta auditoria, porque as evidencias observadas cabem nas hipoteses PA-02 e PA-03 ja existentes.

## Recomendacoes

### Recomendacao 1 - Manter O Ciclo Atual Como Suportado Com Ressalvas

O ciclo atual deve ser tratado como operacionalmente suportado para monitoramento continuo, mas ainda nao como ciclo completo de Projeto.

Agrega valor porque evita chamar de completo um fluxo que ainda nao possui planejamento, arquivamento e encerramento formais.

### Recomendacao 2 - Auditar Estados Do Projeto Antes De Implementar Encerramento

Antes de criar qualquer logica funcional, recomenda-se uma GP documental para definir estados de ciclo de vida do Projeto.

Possiveis temas, sem promocao automatica:

* rascunho;
* ativo;
* pausado;
* encerrado;
* arquivado.

Agrega valor porque encerramento e arquivamento exigem autoridade clara e nao devem nascer como campos soltos.

### Recomendacao 3 - Auditar Planejamento Como Conceito De Dominio

Planejamento deve ser analisado antes de qualquer implementacao de agenda, campanha, amostra ou frequencia.

Agrega valor porque conecta Projeto e coletas sem antecipar multiplos pontos, multiplos coletores ou cadeia de custodia.

### Recomendacao 4 - Preservar GP-D01C Para Medicao -> Projeto

A estrategia atual de relacionar medicoes ao Projeto ativo por contexto deve permanecer ate nova necessidade objetiva.

Agrega valor porque preserva compatibilidade com CSVs e evita acoplamento prematuro.

### Recomendacao 5 - Nao Usar Governanca De Eventos Como Encerramento De Projeto

O ciclo de eventos e util, mas nao substitui ciclo de Projeto.

Agrega valor porque evita duplicacao de autoridade e mantem Governanca responsavel por ocorrencias, nao pelo contrato operacional do Projeto.

## Oportunidades Futuras

Oportunidades candidatas para GPs futuras:

* auditoria de estados do Projeto;
* auditoria do Planejamento de Monitoramento;
* auditoria de Amostra como unidade de coleta;
* auditoria de relatorio final do Projeto;
* auditoria de arquivamento do Projeto;
* auditoria de rastreabilidade ponta a ponta por Projeto sem alterar CSVs;
* futura migracao relacional com materializacao Medicao -> Projeto, apenas quando houver necessidade.

Nenhuma dessas oportunidades deve ser implementada automaticamente.

## Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
| --- | --- | --- | --- |
| Tratar evento arquivado como Projeto encerrado | Media | Medio/Alto | Separar ciclo de evento e ciclo de Projeto |
| Criar `projeto_id` nos CSVs antes da necessidade | Media | Medio | Preservar GP-D01C e PA-03 |
| Projeto assumir decisao observacional | Baixa | Alto | Guardrail PA-01 |
| Planejamento virar nova camada arquitetural | Media | Medio | Tratar como conceito de dominio, se aprovado |
| Relatorio operacional ser confundido com dossie final | Media | Medio | Auditar relatorio final de Projeto antes de implementar |
| Encerramento ser apenas campo `status` sem semantica | Media | Medio | Auditar estados e transicoes antes da implementacao |

## Respostas Obrigatorias

### 1. Quais etapas ja estao corretamente representadas?

Projeto ativo unico, Contexto Operacional, Perfil Operacional, Medicoes operacionais, Monitoramento Hidrico, Analytics, Governanca de eventos, Executive Recommendation, Executive Intelligence, Dashboard e Relatorios operacionais.

### 2. Quais etapas ainda nao existem?

Planejamento formal, Amostra formal, arquivamento de Projeto, encerramento de Projeto e relatorio final/dossie do Projeto.

### 3. Quais etapas existem parcialmente?

Projeto, Configuracao, Coletas, Medicoes, Relatorios e Arquivamento.

### 4. Quem possui autoridade em cada etapa?

A autoridade permanece distribuida pelas camadas existentes: Projeto guarda contexto; Configuracao guarda parametrizacao; Coletas registram dados; Nucleo observa; Analytics interpreta sinais; Governanca acompanha eventos; Recommendation recomenda; Dashboard e Relatorios apresentam.

### 5. Quais dados entram em cada etapa?

Entram dados de Projeto, contexto, configuracao, medicoes, resultados observacionais, snapshots analiticos, eventos governados e sinais consolidados, conforme matriz de entradas e saidas.

### 6. Quais dados saem de cada etapa?

Saem Projeto ativo, perfil operacional, registros de medicao, resultados observacionais, alertas, score, eventos, recomendacoes, visualizacoes e relatorios operacionais.

### 7. Como ocorre a rastreabilidade entre as etapas?

Atualmente ocorre por timestamp, dataset, resultado observacional, politica aplicada, evidencias analiticas, metadados de governanca e evidencias executivas. Ela e suficiente para operacao atual, mas incompleta para historico formal de Projeto.

### 8. Existe alguma quebra de responsabilidade?

Nao foi identificada quebra direta no estado atual.

### 9. Existe alguma duplicacao de autoridade?

Nao foi identificada duplicacao critica. O risco futuro esta em usar Projeto, Dashboard ou Relatorios como autoridade decisoria.

### 10. O PA-01 permanece preservado durante todo o ciclo?

Sim. PA-01 permanece preservado.

### 11. Existe alguma etapa que deveria pertencer ao Projeto e atualmente nao pertence?

Sim. Estados de ciclo de vida, planejamento, criterio de encerramento e arquivamento do Projeto devem ser auditados como pertencentes ao Projeto, antes de implementacao.

### 12. Existe alguma etapa implementada cedo demais?

Nao ha etapa claramente implementada cedo demais. Executive Recommendation e Executive Intelligence existem antes do ciclo formal de encerramento, mas agregam valor real sem violar responsabilidades.

### 13. Existe alguma etapa importante ainda ausente?

Sim. Planejamento e Encerramento do Projeto sao as ausencias mais relevantes.

### 14. Existe alguma oportunidade de simplificacao?

Sim. Manter o Projeto como envelope operacional e evitar criar novas camadas para planejamento, encerramento ou rastreabilidade enquanto o dominio puder evoluir dentro das estruturas existentes.

### 15. O ciclo atual representa adequadamente um Projeto de Monitoramento real?

Representa adequadamente a operacao e a producao de conhecimento durante o monitoramento. Ainda nao representa completamente o nascimento planejado, o encerramento e o arquivamento formal de um Projeto real.

## Veredito Final

**Ciclo de Vida suportado com ressalvas.**

O CASE-01 possui uma cadeia operacional e analitica coerente para transformar medicoes em conhecimento governado e executivo. O ciclo, porem, ainda nao esta completo como Projeto de Monitoramento formal porque planejamento, amostra, arquivamento e encerramento do Projeto permanecem ausentes ou parciais.

Nenhuma implementacao funcional e recomendada diretamente por esta GP. A proxima evolucao deve ser precedida por auditoria especifica dos estados de ciclo de vida do Projeto ou do Planejamento de Monitoramento.

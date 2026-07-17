# PE-03 - Decomposicao Executiva da PA-01 em Frentes de Implementacao

## 1. Objetivo

Este documento decompoe a iniciativa **PA-01 - Governanca de Limites, Responsabilidades e Comunicacao Segura** em frentes executivas de implementacao, a partir do diagnostico oficial produzido em `docs/architecture/PE_02_PA01_ARCHITECTURAL_AUDIT.md`.

A GP-PE-03 possui natureza exclusivamente analitica e preparatoria. Nenhuma alteracao funcional, arquitetural ou normativa e executada nesta etapa.

O objetivo e transformar as nao conformidades, riscos e recomendacoes da GP-PE-02 em um programa incremental de implementacao, com limites de intervencao, dependencias, riscos, criterios de aceite, estrategia de testes e estrategia de rollback.

## 2. Escopo

O escopo desta decomposicao abrange:

* organizacao da PA-01 em frentes de implementacao independentes ou sequenciais;
* identificacao de objetivos, problemas de origem e evidencias por frente;
* mapeamento dos componentes potencialmente afetados;
* definicao dos limites de intervencao permitidos e proibidos;
* analise de dependencias tecnicas e de governanca entre as frentes;
* definicao de matriz de impacto, complexidade e risco;
* recomendacao da ordem executiva das proximas GPs.

Ficam fora do escopo desta GP:

* alteracoes de codigo-fonte;
* refatoracoes;
* reorganizacao fisica de modulos;
* mudancas de comportamento;
* centralizacao efetiva de listas ou catalogos;
* implementacao de guardrails;
* alteracao de contratos, adaptadores, regras de governanca ou ICFACTORY;
* implantacao de Discoveries congeladas.

## 3. Base documental

Foram utilizados como base documental:

* `docs/architecture/PE_02_PA01_ARCHITECTURAL_AUDIT.md`;
* `docs/pac/PE_01_IMPLEMENTATION_EXECUTION_STRATEGY.md`;
* `docs/pac/PAC_14_PROJECT_EVOLUTION_PLAN.md`;
* `docs/pac/PAC_13_OFFICIAL_CONVERGENCE_CONSOLIDATION.md`;
* documentacao arquitetural existente em `docs/architecture`;
* arquitetura atual observada do PROTEUS;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`.

## 4. Metodologia

A decomposicao foi realizada em seis passos:

1. Extracao das nao conformidades, conformidades e recomendacoes da GP-PE-02.
2. Agrupamento dos achados por natureza arquitetural: semantica, comunicacao, catalogos, reavaliacao, acoplamento e guardrails.
3. Conversao dos agrupamentos em frentes executivas de implementacao.
4. Analise de dependencias tecnicas e de governanca entre as frentes.
5. Estimativa relativa de impacto, complexidade e risco.
6. Definicao da ordem recomendada de execucao e dos criterios minimos de aceite.

A metodologia preserva a distincao entre diagnostico, planejamento e implementacao. Esta GP encerra apenas a camada de planejamento executivo.

## 5. Sintese do diagnostico da GP-PE-02

A GP-PE-02 concluiu que a arquitetura atual do PROTEUS preserva a PA-01 nos componentes centrais, sem violacao bloqueante. O nucleo de monitoramento hidrico, a avaliacao observacional, a governanca operacional, analytics, recomendacao executiva e interfaces apresentam separacao geral coerente de responsabilidades.

Tambem foram identificados pontos evolutivos que exigem tratamento antes de implementacoes amplas:

* comunicacao de status com risco semantico, especialmente em expressoes como "Dentro do padrao", "Fora do padrao", "Critico", "Muito critico" e "Status Executivo";
* acoplamento direto do Dashboard com componentes de analytics para montagem de serie historica de Water Health Score;
* duplicacao de listas e catalogos de parametros de qualidade em adaptadores distintos;
* reavaliacao governada em adaptador operacional, com necessidade de autoridade e rastreabilidade explicitas;
* referencias preventivas nao hidricas em analytics, com risco de leitura normativa;
* instanciacao direta de `PolicyEngine` e `AvaliacaoObservacionalService` por interfaces e relatorios;
* risco de acumulacao de responsabilidade em servicos executivos;
* necessidade de guardrails formais entre interface, servicos, dominio, analytics, governanca, recomendacao e persistencia.

O diagnostico recomenda uma evolucao incremental, sem alterar a arquitetura por atacado.

## 6. Frentes de implementacao da PA-01

### PA-01A - Governanca Semantica de Status

**Objetivo arquitetural:** estabelecer um contrato semantico comum para termos de status, score, alerta, recomendacao e avaliacao observacional, evitando interpretacoes legais, regulatorias, sanitarias ou ambientais indevidas.

**Problema de origem:** termos equivalentes ou proximos sao usados em superficies diferentes sem disclaimer uniforme, gerando risco de leitura normativa.

**Evidencias da GP-PE-02:** NC-03 e NC-05; recomendacoes 1, 2 e 9.

**Componentes potencialmente afetados:** `monitoramento_hidrico/qualidade_agua_adapter.py`, `monitoramento_hidrico/dashboard_adapter.py`, `monitoramento_hidrico/operational_reports_adapter.py`, `analytics/alerts.py`, `analytics/scoring.py`, telas de Dashboard, Qualidade da Agua, Relatorios e Painel Executivo, materiais e documentacao de comunicacao operacional.

**Limites de intervencao:** a frente deve tratar linguagem, significado e disclaimers. Nao deve alterar regra de avaliacao, limite tecnico, score, severidade ou criterio de decisao.

**Alteracoes permitidas em GP futura:** criar vocabulario oficial; mapear termos atuais para termos aprovados; definir termos proibidos ou condicionados; definir disclaimers minimos por superficie; ajustar textos quando houver contrato aprovado.

**Alteracoes proibidas:** alterar `PolicyEngine`; alterar limites de politicas observacionais; alterar formula do Water Health Score; alterar severidade de alertas; converter avaliacao observacional em conformidade legal.

**Dependencias:** nao possui pre-requisito tecnico. E pre-requisito conceitual para as demais frentes.

**Risco estimado:** medio.

**Complexidade relativa:** media.

**Testes necessarios:** testes de snapshot ou validacao textual para termos criticos; testes de regressao garantindo que regras, limites, scores e status internos permanecem inalterados.

**Criterios de aceite:** vocabulario oficial definido; termos de status classificados por contexto; disclaimers minimos definidos por superficie; mapa de substituicao ou manutencao justificada dos termos existentes; ausencia de alteracao funcional nos motores de avaliacao.

**Rollback:** reversao pontual de textos, contratos semanticos e snapshots, sem migracao de dados.

**Ordem recomendada:** primeira frente a ser executada.

### PA-01B - Desacoplamento entre Dashboard e Analytics

**Objetivo arquitetural:** impedir que a interface de Dashboard componha diretamente logica analitica, repositorios ou calculadoras, preservando a interface como camada de apresentacao.

**Problema de origem:** o Dashboard instancia componentes de analytics e monta serie historica de Water Health Score, concentrando composicao analitica em camada visual.

**Evidencias da GP-PE-02:** NC-01, NC-06 e NC-09; recomendacoes 5 e 6.

**Componentes potencialmente afetados:** `main.py`, especialmente `DashboardPage`; `analytics/repository.py`; `analytics/scoring.py`; `monitoramento_hidrico/dashboard_adapter.py`; componentes visuais de graficos e cartoes do Dashboard; possivel facade, service ou DTO de snapshot visual em GP futura.

**Limites de intervencao:** a frente deve mover composicao e acesso analitico para contrato apropriado, sem alterar calculo, persistencia ou apresentacao final esperada.

**Alteracoes permitidas em GP futura:** criar service/facade para snapshot do Dashboard; encapsular serie historica de Water Health Score fora da tela; substituir instanciacoes diretas por contrato de leitura; adicionar testes de equivalencia do snapshot.

**Alteracoes proibidas:** alterar formula de score; alterar schema de CSV; alterar dados historicos; alterar limites de avaliacao; transformar Dashboard em camada de decisao.

**Dependencias:** recomenda-se executar apos PA-01A e apos a definicao inicial dos guardrails da PA-01E. Pode ser executada antes ou depois da PA-01C, desde que nao dependa da centralizacao de catalogos.

**Risco estimado:** medio.

**Complexidade relativa:** media-alta.

**Testes necessarios:** testes unitarios para o novo contrato de snapshot; teste de equivalencia da serie historica; teste de interface garantindo ausencia de regressao visual ou estrutural relevante; teste de importacao para evitar dependencia direta proibida.

**Criterios de aceite:** Dashboard nao instancia diretamente calculadora ou repositorio analitico para compor serie; contrato intermediario documentado; resultado apresentado equivalente ao comportamento anterior; camada de apresentacao sem regra analitica nova.

**Rollback:** restaurar a chamada anterior do Dashboard e remover o contrato intermediario introduzido, sem alteracao de dados.

**Ordem recomendada:** quarta frente, apos estabilizacao semantica, guardrails e catalogos.

### PA-01C - Centralizacao de Listas e Catalogos Duplicados

**Objetivo arquitetural:** reduzir divergencia entre adaptadores por meio de uma fonte canonica para parametros de qualidade e mapeamentos compartilhados.

**Problema de origem:** listas semelhantes de parametros existem em varios adaptadores, criando risco de divergencia semantica e operacional.

**Evidencias da GP-PE-02:** NC-02; recomendacao 4.

**Componentes potencialmente afetados:** `monitoramento_hidrico/qualidade_agua_adapter.py`, `monitoramento_hidrico/dashboard_adapter.py`, `monitoramento_hidrico/operational_reports_adapter.py`, `monitoramento_hidrico/analytics_adapter.py`, `monitoramento_hidrico/governance_adapter.py`, eventual modulo compartilhado de catalogo ou contrato de parametros.

**Limites de intervencao:** centralizar nomes, campos e mapeamentos ja existentes. A frente nao deve adicionar, remover ou reinterpretar parametros.

**Alteracoes permitidas em GP futura:** criar catalogo compartilhado de parametros; substituir listas duplicadas por importacao de contrato comum; adicionar testes de paridade entre catalogo novo e listas atuais; documentar consumidores do catalogo.

**Alteracoes proibidas:** alterar limites observacionais; alterar nomes de campos persistidos; mudar schema de entrada ou saida; remover parametros sem GP propria; usar a centralizacao para introduzir nova regra de dominio.

**Dependencias:** deve ocorrer apos PA-01A para alinhar nomes e significados. Recomenda-se executar antes da PA-01D, pois a governanca usa mapeamentos de qualidade durante enriquecimento de alertas.

**Risco estimado:** medio.

**Complexidade relativa:** media.

**Testes necessarios:** testes de equivalencia de catalogo; testes dos adaptadores consumidores; testes de leitura de amostras historicas; verificacao de que nenhum campo persistido foi renomeado.

**Criterios de aceite:** fonte canonica definida; adaptadores consumidores usam o mesmo contrato; listas antigas removidas ou justificadamente mantidas como aliases; paridade comprovada com os parametros anteriores; zero mudanca funcional em avaliacao, analytics e governanca.

**Rollback:** restaurar listas locais anteriores e remover importacao do catalogo compartilhado.

**Ordem recomendada:** terceira frente.

### PA-01D - Governanca da Reavaliacao Controlada

**Objetivo arquitetural:** formalizar as condicoes, limites e rastreabilidade da reavaliacao usada pela governanca operacional, preservando a avaliacao original e impedindo autoridade paralela implicita.

**Problema de origem:** adaptador de governanca pode reavaliar alerta com valor numerico para enriquecer metadados operacionais.

**Evidencias da GP-PE-02:** NC-04; recomendacao 7.

**Componentes potencialmente afetados:** `monitoramento_hidrico/governance_adapter.py`, `governance/service.py`, `governance/models.py`, `governance/repository.py`, eventos operacionais persistidos em JSON, testes de fluxo de governanca.

**Limites de intervencao:** a reavaliacao deve permanecer enriquecimento rastreavel, nao decisao primaria. A avaliacao original deve continuar preservada.

**Alteracoes permitidas em GP futura:** documentar pre-condicoes para reavaliacao; explicitar metadados de origem, motivo e escopo; adicionar guardas para impedir reavaliacao silenciosa; criar testes de rastreabilidade; tornar claro o limite entre avaliacao original e enriquecimento governado.

**Alteracoes proibidas:** transformar o adaptador em autoridade primaria de avaliacao; reavaliar sinais nao hidricos sem GP especifica; alterar severidade ou ciclo de vida de eventos sem justificativa governada; sobrescrever avaliacao original; mudar schema persistido sem estrategia explicita de compatibilidade.

**Dependencias:** deve ocorrer apos PA-01A e preferencialmente apos PA-01C. Depende tambem dos guardrails de PA-01E para evitar expansao indevida da responsabilidade do adaptador.

**Risco estimado:** alto.

**Complexidade relativa:** media.

**Testes necessarios:** testes de pre-condicao de reavaliacao; testes de preservacao da avaliacao original; testes de metadados de origem; testes de eventos existentes; testes de nao reavaliacao para entradas fora do escopo.

**Criterios de aceite:** reavaliacao limitada, explicita e rastreavel; avaliacao original preservada; metadados distinguem origem, enriquecimento e resultado; ausencia de autoridade paralela; compatibilidade com eventos ja persistidos.

**Rollback:** remover guardas e metadados novos mantendo leitura compativel dos eventos existentes; preservar backup ou migracao reversivel caso qualquer schema seja tocado em GP futura.

**Ordem recomendada:** quinta frente, por concentrar maior risco arquitetural.

### PA-01E - Guardrails de Comunicacao entre Camadas

**Objetivo arquitetural:** definir regras explicitas de comunicacao permitida e proibida entre interface, adaptadores, servicos, dominio, analytics, governanca, recomendacao executiva e persistencia.

**Problema de origem:** a arquitetura esta funcionalmente preservada, mas alguns componentes instanciam dependencias diretamente e servicos executivos possuem risco de acumulacao progressiva de responsabilidades.

**Evidencias da GP-PE-02:** NC-06, NC-07, NC-08 e NC-09; recomendacoes 3, 5, 7, 8 e 10.

**Componentes potencialmente afetados:** interfaces de apresentacao; adaptadores de monitoramento hidrico; `PolicyEngine`; `AvaliacaoObservacionalService`; `AnalyticsService`; `OperationalGovernanceService`; `ExecutiveIntelligenceService`; `ExecutiveRules`; `ExecutiveRecommendationService`; repositorios CSV e JSON.

**Limites de intervencao:** a primeira entrega deve ser documental e verificavel. Implementacoes futuras podem adicionar testes ou checks, mas nao devem criar uma nova arquitetura paralela.

**Alteracoes permitidas em GP futura:** matriz formal de responsabilidades; tabela de comunicacoes permitidas e proibidas; checklist de revisao PA-01; testes de importacao ou dependencia quando viavel; documentacao de excecoes existentes.

**Alteracoes proibidas:** reestruturar modulos sem GP especifica; mover responsabilidades de dominio para interface; permitir acesso direto de telas a persistencia como novo padrao; concentrar avaliacao, analytics, governanca e recomendacao em um unico servico.

**Dependencias:** depende de PA-01A para linguagem e fronteiras semanticas. Deve ser definida antes das frentes tecnicas mais sensiveis.

**Risco estimado:** medio.

**Complexidade relativa:** media.

**Testes necessarios:** checks de dependencia ou testes estaticos quando aplicavel; revisao de imports criticos; testes de preservacao de contratos publicos se guardrails forem automatizados.

**Criterios de aceite:** matriz de responsabilidades aprovada; comunicacoes permitidas e proibidas documentadas; excecoes existentes justificadas; checklist PA-01 aplicavel a novas alteracoes; nenhuma mudanca funcional obrigatoria na primeira entrega.

**Rollback:** remover checks ou documentos complementares adicionados em GP futura, sem impacto em runtime.

**Ordem recomendada:** segunda frente, antes das intervencoes tecnicas.

## 7. Componentes afetados por frente

| Frente | Componentes principais | Tipo de impacto esperado |
| --- | --- | --- |
| PA-01A | Adaptadores, telas, relatorios, analytics preventivo, documentacao de comunicacao | Semantico e comunicacional |
| PA-01B | `DashboardPage`, repositorio de analytics, calculadora de score, adapter de Dashboard | Desacoplamento de interface e analytics |
| PA-01C | Adaptadores de qualidade, dashboard, relatorios, analytics e governanca | Centralizacao de catalogo |
| PA-01D | Adapter de governanca, servico de governanca, modelos e repositorio de eventos | Rastreabilidade e autoridade de reavaliacao |
| PA-01E | Interfaces, services, adapters, engines, repositories e servicos executivos | Guardrails de comunicacao e responsabilidade |

## 8. Dependencias entre frentes

| Frente | Pre-requisitos | Observacao |
| --- | --- | --- |
| PA-01A | Nenhum | Deve abrir a implementacao da PA-01 por estabilizar a linguagem comum. |
| PA-01E | PA-01A | Guardrails dependem dos significados oficiais de status, avaliacao e recomendacao. |
| PA-01C | PA-01A | Catalogos devem refletir nomes e significados ja governados. |
| PA-01B | PA-01A, PA-01E | Desacoplamento do Dashboard deve seguir limites previamente definidos. |
| PA-01D | PA-01A, PA-01C, PA-01E | Reavaliacao governada exige semantica, catalogo e regras de comunicacao claros. |

Frentes potencialmente combinaveis: PA-01A e PA-01E podem ser planejadas em proximidade, mas recomenda-se mantelas separadas para preservar criterios de aceite objetivos.

Frentes isoladas: PA-01D deve ser isolada pelo risco de autoridade paralela. PA-01B tambem deve ser isolada por tocar fluxo de apresentacao e analytics.

Risco de sobreposicao: PA-01C e PA-01D compartilham mapeamentos de qualidade; por isso a centralizacao de catalogos deve anteceder a governanca de reavaliacao.

Frentes exclusivamente documentais antes de codigo: PA-01A e PA-01E devem possuir entrega documental ou contratual antes de qualquer alteracao funcional correlata.

## 9. Matriz Impacto x Complexidade x Risco

| Frente | Impacto arquitetural | Complexidade | Risco | Justificativa |
| --- | --- | --- | --- | --- |
| PA-01A | Alto | Media | Medio | Define linguagem comum para todas as superficies e reduz risco de interpretacao normativa. |
| PA-01E | Alto | Media | Medio | Estabelece limites entre camadas antes de refatoracoes tecnicas. |
| PA-01C | Medio | Media | Medio | Reduz divergencia entre adaptadores, mas exige paridade rigorosa. |
| PA-01B | Medio-Alto | Media-Alta | Medio | Remove acoplamento do Dashboard sem alterar resultado analitico. |
| PA-01D | Alto | Media | Alto | Toca autoridade de reavaliacao e rastreabilidade de governanca operacional. |

## 10. Ordem recomendada de implementacao

A ordem recomendada de execucao e:

1. **GP-PE-04 - PA-01A - Governanca Semantica de Status**
2. **GP-PE-08 - PA-01E - Guardrails de Comunicacao entre Camadas**
3. **GP-PE-06 - PA-01C - Centralizacao de Listas e Catalogos Duplicados**
4. **GP-PE-05 - PA-01B - Desacoplamento entre Dashboard e Analytics**
5. **GP-PE-07 - PA-01D - Governanca da Reavaliacao Controlada**

A numeracao preserva a familia de frentes proposta para PA-01. A execucao recomendada, contudo, antecipa a PA-01E porque guardrails devem preceder alteracoes tecnicas mais sensiveis.

## 11. Criterios de aceite por frente

| Frente | Criterios minimos |
| --- | --- |
| PA-01A | Vocabulario oficial, disclaimers por superficie, mapa de termos, nenhuma alteracao funcional. |
| PA-01B | Dashboard sem composicao analitica direta, snapshot equivalente, contrato intermediario testado. |
| PA-01C | Catalogo canonico, paridade com listas anteriores, consumidores atualizados, sem mudanca de schema. |
| PA-01D | Reavaliacao explicita, pre-condicoes claras, avaliacao original preservada, metadados rastreaveis. |
| PA-01E | Matriz de responsabilidades, comunicacoes permitidas/proibidas, excecoes justificadas, checklist PA-01. |

## 12. Estrategia de testes

A estrategia de testes da PA-01 deve combinar verificacoes unitarias, regressivas e estruturais:

* testes de equivalencia para garantir que refatoracoes nao mudem resultados;
* snapshots ou asserts textuais para termos criticos e disclaimers;
* testes de catalogo para confirmar paridade entre fonte canonica e listas antigas;
* testes de dependencia/importacao para prevenir comunicacoes proibidas quando viavel;
* testes de fluxo de governanca para preservar avaliacao original e rastreabilidade;
* testes de interface apenas quando houver mudanca em apresentacao ou contrato consumido pela tela.

A prioridade dos testes deve seguir o risco: PA-01D exige maior rigor de rastreabilidade; PA-01B exige equivalencia funcional; PA-01A exige estabilidade semantica.

## 13. Estrategia de rollback

Cada frente deve possuir rollback pontual:

* PA-01A: reverter vocabulario, textos e disclaimers alterados;
* PA-01E: remover guardrails automatizados ou documentos complementares sem tocar runtime;
* PA-01C: restaurar listas locais anteriores e remover catalogo compartilhado;
* PA-01B: restaurar composicao anterior do Dashboard e remover facade/service introduzido;
* PA-01D: preservar leitura de eventos existentes e reverter guardas/metadados novos com compatibilidade.

Nenhuma frente deve depender de migracao irreversivel. Caso uma GP futura proponha migracao de schema, ela devera incluir plano proprio de compatibilidade e reversao.

## 14. Recomendacao da primeira unidade de implementacao

A primeira unidade recomendada e:

**GP-PE-04 - PA-01A - Governanca Semantica de Status.**

Justificativa:

* e pre-requisito conceitual das demais frentes;
* reduz risco de comunicacao antes de alteracoes tecnicas;
* possui menor dependencia estrutural;
* permite validar a linguagem oficial da PA-01 sem tocar regras, dados ou arquitetura;
* fornece base para guardrails, catalogos, Dashboard e governanca de reavaliacao.

## 15. Parecer Final

A PA-01 deve ser implementada de forma incremental, iniciando pela estabilizacao semantica e pela formalizacao dos guardrails de comunicacao. A arquitetura atual do PROTEUS nao exige ruptura para atender a PA-01; exige, sobretudo, consolidacao de linguagem, limites de responsabilidade, contratos compartilhados e rastreabilidade.

O programa recomendado evita que a primeira implementacao ataque diretamente os pontos de maior risco. A sequencia PA-01A, PA-01E, PA-01C, PA-01B e PA-01D cria base conceitual antes de intervencoes tecnicas, reduz sobreposicoes e preserva a separacao entre avaliacao observacional, analytics, governanca operacional, recomendacao executiva e interface.

Com este documento, a **GP-PE-03** fica tecnicamente concluida como decomposicao executiva da PA-01, sem execucao de implementacao funcional.

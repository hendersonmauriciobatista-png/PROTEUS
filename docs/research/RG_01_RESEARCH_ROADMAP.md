# GP-RG-01 — Roadmap Inicial Da Pesquisa "Governanca Da Fundamentacao Das Decisoes"

## 1. Objetivo

Organizar a evolucao logica da linha de pesquisa desde sua constituicao ate uma futura validacao multidominio, sem datas, sem promocao automatica de conceitos e sem iniciar etapas posteriores.

## 2. Autoridades

* `docs/research/RG_01_RESEARCH_CONSTITUTION.md`;
* `docs/research/PI_07A_DECISION_FOUNDATION_GOVERNANCE_REPORT.md`;
* `docs/presentation/PI_07_KDENLIVE_PRE_POSTPRODUCTION_AUDIT.md`;
* `docs/presentation/PI_07_POST_PRODUCTION_EXECUTION_REPORT.md`.

## 3. Estado Inicial

* linha de pesquisa constituida;
* objeto e nao objeto delimitados;
* hipotese central registrada e nao validada;
* seis conceitos iniciais identificados;
* `Criterio de Avaliacao` mantido como hipotese observacional;
* um experimento fundador disponivel;
* nenhuma replicacao independente;
* nenhuma validacao multidominio;
* nenhuma promocao ao nucleo metodologico do ICFACTORY.

## 4. Sequencia Logica

GP-RG-01 — Constituicao da Pesquisa

↓

GP-RG-02 — Modelo Conceitual

↓

GP-RG-03 — Arquitetura Documental da Cadeia de Governanca

↓

GP-RG-04 — Protocolo Experimental

↓

GP-RG-05 — Validacao Multidominio

Cada etapa depende de autorizacao propria e do atendimento aos criterios de entrada. A conclusao de uma etapa nao inicia automaticamente a seguinte.

## 5. GP-RG-01 — Constituicao Da Pesquisa

### Estado

CONCLUIDA.

### Objetivo

Criar identidade, proposito, objeto, hipoteses, conceitos iniciais, principios, limites e roadmap.

### Entradas

* GP-PI-07A;
* auditoria e execucao GP-PI-07;
* diretrizes DG-01 a DG-12.

### Entregaveis

* `RG_01_RESEARCH_CONSTITUTION.md`;
* `RG_01_RESEARCH_ROADMAP.md`;
* `RG_01_CLOSURE_REPORT.md`;
* registros em HISTORY e ROADMAP.

### Criterio De Saida

Identidade, objeto, limites, hipoteses, principios e sequencia de evolucao registrados sem promover hipoteses.

## 6. GP-RG-02 — Modelo Conceitual

### Estado

RECOMENDADA — NAO INICIADA.

### Objetivo

Definir com maior rigor os conceitos da cadeia, suas relacoes, estados, fronteiras e invariantes.

### Pre-Requisitos

* constituicao RG-01 aprovada;
* inventario de exemplos e contraexemplos da GP-PI-07A;
* criterio explicito para distinguir definicao, regra, hipotese e evidencia.

### Questoes Centrais

* O que diferencia premissa de hipotese?
* Quando uma observacao se torna evidencia utilizavel?
* Como distinguir inferencia de fundamentacao?
* Fundamentacao e um artefato ou uma relacao?
* Validacao retroage sobre quais elementos?
* A cadeia e linear, ciclica ou um grafo?
* `Criterio de Avaliacao` e conceito independente ou propriedade de Validacao?

### Entregaveis Recomendados

* glossario conceitual versionado;
* mapa de relacoes;
* estados e transicoes;
* invariantes e regras de integridade;
* exemplos, contraexemplos e casos ambiguos;
* matriz de sobreposicoes conceituais;
* registro de decisoes terminologicas.

### Criterio De Saida

Cada conceito deve possuir definicao, fronteira, exemplos, contraexemplos e relacoes declaradas. Conceitos ainda ambiguos devem permanecer experimentais.

### Restricao

Nao transformar o modelo conceitual em arquitetura de software nem incluir definitivamente `Criterio de Avaliacao` sem evidencia adicional.

## 7. GP-RG-03 — Arquitetura Documental Da Cadeia De Governanca

### Estado

PLANEJADA — NAO INICIADA.

### Objetivo

Definir a organizacao documental da cadeia, seus identificadores, vinculos, ciclos de revisao e regras de rastreabilidade.

### Dependencia

GP-RG-02 concluida com modelo conceitual suficientemente estavel.

### Entregaveis Recomendados

* esquema documental abstrato;
* regras de identificacao e referencia;
* modelo de revisao e supersessao;
* matriz de rastreabilidade;
* tratamento de conflitos, ausencia e inconclusao;
* perfil minimo e perfil ampliado conforme risco.

### Criterio De Saida

Uma cadeia documental deve poder ser reconstruida sem acesso a estados internos e sem depender de conhecimento tacito do executor original.

### Restricao

“Arquitetura” significa organizacao documental da pesquisa, nao modificacao da arquitetura do PROTEUS.

## 8. GP-RG-04 — Protocolo Experimental

### Estado

PLANEJADA — NAO INICIADA.

### Objetivo

Definir como novos experimentos serao planejados, executados, comparados e auditados.

### Dependencia

GP-RG-03 concluida e artefatos documentais definidos.

### Entregaveis Recomendados

* protocolo de selecao de tarefas e dominios;
* baseline ou condicao comparativa;
* criterios de avaliacao definidos antes da execucao;
* escalas de rastreabilidade, auditabilidade e reproducibilidade;
* regras para avaliadores independentes;
* tratamento de vieses, falhas e resultados negativos;
* formulario de replicacao;
* criterio de interrupcao e revisao.

### Criterio De Saida

O protocolo deve permitir replicacao independente e impedir que o criterio seja ajustado retrospectivamente apenas para favorecer o resultado.

### Restricao

O protocolo nao pode alegar acesso a raciocinio interno nem usar volume documental como substituto automatico de qualidade.

## 9. GP-RG-05 — Validacao Multidominio

### Estado

PLANEJADA — NAO INICIADA.

### Objetivo

Executar o protocolo em dominios distintos e avaliar as hipoteses H-RG-001 a H-RG-007.

### Dependencia

GP-RG-04 concluida e protocolo aprovado.

### Amostra Logica Minima Recomendada

* tarefa documental;
* tarefa tecnica ou de engenharia;
* tarefa operacional;
* mais de um agente decisor ou executor;
* ao menos uma replicacao independente;
* ao menos um caso com resultado negativo ou inconclusivo preservado.

### Entregaveis Recomendados

* relatorios por experimento;
* matriz comparativa entre dominios;
* analise de replicabilidade;
* analise de custo documental;
* revisao das hipoteses;
* recomendacao de consolidacao, permanencia experimental ou rejeicao.

### Criterio De Saida

As conclusoes devem separar claramente: evidencia por dominio, convergencias, divergencias, limites e grau de generalizacao permitido.

### Restricao

Um resultado positivo isolado nao autoriza promocao metodologica.

## 10. Gates De Evolucao

| Gate | Pergunta | Aplicacao |
|---|---|---|
| G-RG0 | existe autorizacao formal para a GP? | todas as etapas |
| G-RG1 | entradas e evidencias estao identificadas? | todas as etapas |
| G-RG2 | conceitos e hipoteses mantem estado explicito? | RG-02 em diante |
| G-RG3 | limites e alternativas estao registrados? | todas as etapas |
| G-RG4 | o resultado pode ser auditado sem estados internos? | RG-03 em diante |
| G-RG5 | criterios foram definidos antes da avaliacao? | RG-04 e RG-05 |
| G-RG6 | revisoes e resultados negativos foram preservados? | todas as etapas experimentais |
| G-RG7 | a evidencia permite o grau de generalizacao alegado? | RG-05 |

Falha em um gate impede conclusoes que dependam dele, mas nao autoriza ocultar o resultado parcial.

## 11. Matriz De Hipoteses Por Etapa

| Hipotese | RG-01 | RG-02 | RG-03 | RG-04 | RG-05 |
|---|---|---|---|---|---|
| H-RG-001 — hipotese central | registrar | decompor | operacionalizar | definir teste | avaliar |
| H-RG-002 — separacao epistemica | registrar | definir | estruturar | testar | comparar |
| H-RG-003 — historico de revisoes | registrar | modelar | estruturar | testar | comparar |
| H-RG-004 — reproducao independente | delimitar | definir | suportar | protocolar | avaliar |
| H-RG-005 — aplicabilidade multidominio | delimitar | identificar variaveis | suportar | amostrar | avaliar |
| H-RG-006 — qualidade decisoria | manter pendente | definir qualidade | definir evidencias | criar baseline | avaliar |
| H-RG-007 — consistencia entre agentes | manter pendente | definir comparabilidade | suportar identidade | protocolar | avaliar |

## 12. Riscos De Pesquisa

| Risco | Impacto | Mitigacao |
|---|---|---|
| documentacao performativa ou excessiva | aparencia de rigor sem ganho real | criterios previos e proporcionalidade |
| confusao entre evidencia e inferencia | fundamentacao circular | separacao epistemica e auditoria |
| viés retrospectivo | criterios ajustados ao resultado | pre-registro no protocolo RG-04 |
| generalizacao a partir de um caso | conclusoes invalidas | RG-05 multidominio |
| apagamento de falhas | perda de auditabilidade | preservacao obrigatoria de revisoes |
| confusao com raciocinio interno | extrapolacao indevida | limite constitucional expresso |
| custo documental elevado | inviabilidade operacional | perfis proporcionais ao risco |
| ambiguidade de conceitos | resultados incomparaveis | modelo conceitual RG-02 |

## 13. Condicoes Para Promocao Futura

Nenhuma hipotese ou conceito sera promovido apenas pela conclusao deste roadmap. Uma promocao futura exige, no minimo:

* evidencias recorrentes;
* multiplos dominios;
* replicacao independente;
* criterios definidos previamente;
* analise de resultados negativos;
* avaliacao de custo e beneficio;
* ausencia de conflito com principios vigentes;
* decisao formal de governanca.

## 14. Recomendacoes Para GP-RG-02

1. Usar a GP-PI-07A como caso fundador, nao como modelo universal.
2. Criar exemplos e contraexemplos para cada conceito.
3. Modelar revisao sem apagar estados anteriores.
4. Separar relacoes obrigatorias de relacoes opcionais.
5. Investigar se a cadeia e grafo ou fluxo ciclico.
6. Manter `Criterio de Avaliacao` como hipotese observacional.
7. Definir fronteira entre premissa, hipotese e inferencia.
8. Registrar ambiguidades em vez de resolve-las por preferencia terminologica.
9. Nao iniciar RG-03 durante RG-02.

## 15. Estado Do Roadmap

Roadmap documental aprovado como sequencia inicial de pesquisa. Somente GP-RG-01 esta concluida. GP-RG-02 a GP-RG-05 permanecem nao iniciadas.

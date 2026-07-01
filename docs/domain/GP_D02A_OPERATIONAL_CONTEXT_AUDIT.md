# GP-D02A - Auditoria do Contexto Operacional

Data: 30/06/2026

Status: AUDITORIA DOCUMENTAL CONCLUIDA

Natureza: Dominio

## Objetivo

Auditar o conceito de Contexto Operacional e definir, em nivel de dominio, como ele deve influenciar o comportamento futuro do Sistema de Analise de Agua sem alterar a arquitetura existente.

Pergunta central:

Como o Contexto Operacional deve orientar a selecao das politicas observacionais sem alterar a arquitetura existente?

Esta auditoria nao implementa codigo, nao cria politicas, nao altera `PolicyEngine`, nao altera Motor Observacional, nao altera Analytics, Governanca, Recommendation, runtime ou interface.

## Contexto

Estado considerado:

* GP-A23 consolidou a arquitetura global.
* GP-D01A aprovou o modelo minimo de Projeto de Monitoramento.
* GP-D01B implementou o Projeto ativo unico.
* GP-D01C-A recomendou manter a relacao Medicao -> Projeto por contexto enquanto existir Projeto ativo unico.
* O catalogo hidrico existente ja possui perfis operacionais como `rural`, `industrial`, `urbano_saneamento`, `ambiental_rio`, `eta` e `ete`.
* O `PolicyEngine` atual seleciona politicas por `perfil_operacional`, `categoria` e `parametro_id`.

## Conceitos Auditados

Contextos candidatos:

* Urbana.
* Rural.
* Industrial.
* Agricola.

Filtro institucional aplicado:

`Agrega valor ao projeto?`

Nesta auditoria, um contexto agrega valor quando:

* reduz ambiguidade sobre o tipo de operacao monitorada;
* ajuda a selecionar perfil operacional futuro sem criar politica nova agora;
* orienta quais riscos devem receber atencao operacional;
* preserva PA-01;
* evita complexidade prematura.

## Caracterizacao Dos Contextos

### Urbana

Caracterizacao:

Contexto associado a redes de abastecimento, saneamento, reservatorios urbanos, distribuicao de agua e acompanhamento de qualidade para uso coletivo.

Monitoramentos normalmente esperados:

* parametros fisico-quimicos basicos;
* turbidez, cor, pH e cloro residual;
* indicadores microbiologicos;
* sinais de consumo, distribuicao e perdas quando aplicavel.

Riscos priorizados:

* contaminacao microbiologica;
* falha de desinfeccao;
* turbidez elevada;
* variacao operacional em redes ou reservatorios;
* perdas e interrupcoes de distribuicao, quando o escopo incluir consumo.

Valor:

Agrega valor porque ja se aproxima do perfil `urbano_saneamento` existente e orienta monitoramento de rotina sem criar nova camada.

### Rural

Caracterizacao:

Contexto associado a propriedades rurais, captacoes locais, pocos, nascentes, reservatorios de propriedade e usos agropecuarios gerais.

Monitoramentos normalmente esperados:

* parametros basicos de qualidade;
* nutrientes;
* indicadores microbiologicos;
* contaminantes agricolas quando houver risco ou suspeita;
* condicoes ambientais locais.

Riscos priorizados:

* contaminacao por escoamento superficial;
* contaminacao microbiologica;
* variacao sazonal;
* presenca de nutrientes;
* influencia de atividade agropecuaria.

Valor:

Agrega valor porque ja existe perfil `rural` no catalogo e configuracao rural base.

### Industrial

Caracterizacao:

Contexto associado a uso industrial, efluentes, pontos de controle produtivo, agua de processo e impacto operacional de atividade industrial.

Monitoramentos normalmente esperados:

* parametros fisico-quimicos;
* DBO e DQO;
* metais pesados;
* contaminantes industriais;
* oleos, graxas, solventes e compostos correlatos quando aplicavel.

Riscos priorizados:

* contaminacao por efluentes;
* metais pesados;
* carga organica elevada;
* compostos industriais;
* divergencia entre ponto de controle e corpo receptor.

Valor:

Agrega valor porque ja existe perfil `industrial` e politica observacional especifica por perfil industrial.

### Agricola

Caracterizacao:

Contexto associado a agricultura, irrigacao, drenagem agricola e uso de defensivos ou fertilizantes.

Monitoramentos normalmente esperados:

* parametros basicos de qualidade;
* nutrientes;
* contaminantes agricolas;
* indicadores microbiologicos quando houver contato com criacao animal ou uso humano;
* variacao sazonal relacionada a manejo e chuva.

Riscos priorizados:

* agrotoxicos;
* herbicidas, fungicidas e inseticidas;
* nitrato, fosforo e eutrofizacao;
* carreamento por chuva;
* contaminacao de poco, rio ou reservatorio por uso do solo.

Valor:

Agrega valor como especializacao conceitual de Rural, mas ainda nao deve virar perfil operacional proprio nesta fase. O mapeamento inicial recomendado continua sendo `rural`.

## Matriz Comparativa Entre Contextos

| Contexto | Caracteristica principal | Perfil operacional recomendado | Monitoramento esperado | Riscos priorizados | Agrega valor? | Decisao |
| -------- | ------------------------ | ------------------------------ | ---------------------- | ------------------ | ------------- | ------- |
| Urbana | Rede, abastecimento, saneamento e uso coletivo | `urbano_saneamento` | pH, turbidez, cor, cloro residual, microbiologia | desinfeccao, microbiologia, turbidez, perdas | Sim | Suportar como contexto |
| Rural | Captacoes locais, propriedades e usos agropecuarios gerais | `rural` | basicos, nutrientes, microbiologia, contaminantes agricolas sob risco | escoamento, microbiologia, nutrientes, sazonalidade | Sim | Suportar como contexto |
| Industrial | Processo, efluentes e pontos de controle produtivo | `industrial` | DBO, DQO, metais, contaminantes industriais | efluentes, metais, carga organica, oleos/graxas | Sim | Suportar como contexto |
| Agricola | Agricultura, irrigacao e defensivos | `rural` | nutrientes, agrotoxicos, herbicidas, fungicidas, inseticidas | agrotoxicos, eutrofizacao, chuva, uso do solo | Sim, com ressalva | Suportar como contexto, nao como perfil novo |

## Responsabilidades

### Pertence Ao Projeto

O Projeto deve armazenar o Contexto Operacional escolhido, porque ele caracteriza o ambiente estavel do monitoramento.

Informacoes que pertencem ao Projeto:

* area operacional;
* ponto principal de coleta;
* cliente;
* coletor responsavel;
* data de criacao;
* status do Projeto;
* futuramente, quando auditado, perfil operacional derivado ou selecionado.

### Pertence Ao Policy Engine

O `PolicyEngine` deve continuar responsavel apenas por selecionar politica observacional a partir de insumos explicitos, como `perfil_operacional`, `categoria` e `parametro_id`.

O Contexto Operacional deve conversar com o `PolicyEngine` por traducao controlada para perfil operacional, nunca por regra direta embutida em telas, Analytics, Governanca ou Recommendation.

Mapeamento conceitual recomendado:

| Contexto Operacional | Perfil operacional inicial |
| -------------------- | -------------------------- |
| Urbana | `urbano_saneamento` |
| Rural | `rural` |
| Industrial | `industrial` |
| Agricola | `rural` |

### Pertence Ao Motor Observacional

O Motor Observacional permanece responsavel por executar a avaliacao do parametro com base na politica selecionada e nos limites/metadados disponiveis.

Nao pertence ao Motor Observacional:

* definir contexto operacional;
* escolher politica;
* decidir qual contexto e mais adequado;
* criar prioridade executiva;
* alterar Projeto.

## Relacao Com O Policy Engine

O Contexto Operacional deve atuar como insumo indireto de selecao.

Fluxo conceitual recomendado:

```text
Projeto de Monitoramento
  -> Contexto Operacional
  -> perfil_operacional derivado ou selecionado
  -> PolicyEngine seleciona politica
  -> Motor Observacional executa avaliacao
```

Guardrails:

* Contexto Operacional nao seleciona politica diretamente.
* Projeto nao executa avaliacao.
* UI nao implementa regras observacionais.
* Analytics nao reinterpreta contexto para decidir limites.
* Governanca nao usa contexto para criar autoridade observacional paralela.
* Recommendation nao acessa `PolicyEngine` nem Motor Observacional por causa do contexto.

## Preservacao Do PA-01

PA-01 permanece integralmente preservado se:

* a selecao de politicas continuar no `PolicyEngine`;
* a execucao de avaliacoes continuar no Motor Observacional;
* o Contexto Operacional for apenas contexto de dominio;
* o mapeamento contexto -> perfil for explicito e auditavel;
* nenhuma camada posterior recalcular decisao observacional.

O Contexto Operacional reforca PA-01 quando reduz ambiguidade de selecao sem deslocar autoridade.

## Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
| ----- | ------------- | ------- | --------- |
| Agricola virar perfil operacional prematuro | Media | Medio | Manter Agricola como contexto mapeado para `rural` nesta fase. |
| Contexto virar politica disfarçada | Media | Alto | Proibir selecao direta fora do `PolicyEngine`. |
| UI passar a decidir comportamento observacional | Baixa/Media | Alto | UI deve apenas registrar/exibir contexto. |
| Analytics usar contexto para recalcular limites | Media futura | Alto | Analytics deve consumir resultado observacional, nao selecionar politica. |
| Aumento de complexidade por subcontextos | Media | Medio | Adiar subtipos, culturas, bacias, porte industrial e sazonalidade. |
| Conflito entre area operacional e ponto principal | Media | Medio | Definir regra futura de precedencia antes de implementacao funcional. |

## Impacto Arquitetural

| Area | Impacto nesta GP |
| ---- | ---------------- |
| Codigo funcional | Nenhum |
| Interface | Nenhum |
| Runtime | Nenhum |
| Policy Engine | Nenhum |
| Motor Observacional | Nenhum |
| Analytics | Nenhum |
| Governanca | Nenhum |
| Recommendation | Nenhum |
| Camadas arquiteturais | Nenhuma camada nova |
| PA-01 | Preservado |

A auditoria recomenda evoluir o dominio por enriquecimento do Projeto existente, nao por criacao de nova camada.

## Itens Adiados

Nao implementar nesta fase:

* novas politicas observacionais;
* novo perfil operacional `agricola`;
* subcontextos por cultura agricola;
* porte industrial;
* classe de uso da agua;
* bacia/regiao hidrografica;
* sazonalidade como regra automatica;
* matriz de risco automatica por contexto;
* alteracoes no `PolicyEngine`;
* alteracoes no Motor Observacional;
* alteracoes em Analytics, Governanca ou Recommendation;
* qualquer decisao observacional fora do Nucleo de Monitoramento Hidrico.

Esses itens podem agregar valor futuro, mas nao agregam valor objetivo suficiente para esta fase sem nova auditoria.

## Relacao Com Discoveries Candidatas

`docs/research/DISCOVERY_CATALOG.md` foi consultado nesta GP.

Discoveries registradas:

* PA-02 - Progressao De Valor.
* PA-03 - Materializacao Sob Necessidade.

Impacto da GP-D02A:

* PA-02: reforcada. O Contexto Operacional agrega valor ao Projeto por enriquecimento de dominio, sem criar camada nova.
* PA-03: reforcada indiretamente. A auditoria recomenda nao materializar novas politicas, perfis ou regras automaticas antes de necessidade operacional objetiva.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida.

## Recomendacoes

1. Tratar Contexto Operacional como atributo de dominio do Projeto de Monitoramento.
2. Manter os quatro contextos candidatos como valores suportados: Urbana, Rural, Industrial e Agricola.
3. Mapear Agricola inicialmente para o perfil `rural`, sem criar perfil novo.
4. Fazer o Contexto conversar com o `PolicyEngine` apenas por `perfil_operacional` explicito ou derivado.
5. Preservar o Motor Observacional como executor de avaliacao.
6. Adiar qualquer nova politica ou regra automatica ate auditoria especifica.
7. Registrar conflitos entre contexto e ponto principal como tema futuro, sem implementar agora.

## Veredito Final

Modelo de Contexto suportado e recomendado.

Justificativa:

* Os quatro contextos agregam valor objetivo ao Projeto.
* O catalogo atual ja suporta rural, industrial e urbano/saneamento como perfis ou configuracoes.
* Agricola agrega valor conceitual, mas deve iniciar como especializacao de Rural.
* O modelo preserva PA-01.
* A arquitetura existente nao precisa de nova camada.
* A recomendacao reforca Discoveries candidatas sem promove-las.

## Encerramento

Nenhum codigo foi alterado.

Nenhuma interface foi alterada.

Nenhuma camada foi criada.

Nenhuma politica foi criada.

PA-01 foi preservado.

`DISCOVERY_CATALOG.md` foi consultado.

Nenhuma Discovery foi promovida automaticamente.

# OP-02 - Auditoria Da Unidade Fundamental De Informacao

## Objetivo

Determinar, exclusivamente por auditoria documental e de dominio, qual e a menor unidade de informacao reconhecida pelo PROTEUS e capaz de percorrer o fluxo operacional definido na OP-01.

Esta auditoria nao cria entidades, nao implementa codigo e nao altera arquitetura, persistencia, interface, Dominio Projeto ou Dossie Final.

O objetivo e compreender o elemento fundamental do fluxo informacional interno do PROTEUS.

## Escopo

O escopo desta OP-02 inclui:

* definir a menor unidade operacional de informacao do PROTEUS;
* distinguir essa unidade de medicao, observacao, conjunto de parametros, evento, indicador e memoria permanente;
* avaliar se a unidade pertence ao Dominio Projeto ou se exige novo agregado operacional;
* relacionar a unidade ao fluxo definido na OP-01;
* avaliar sua participacao em indicadores, alertas, governanca, recomendacoes, dashboards, relatorios e Dossie Final;
* avaliar impacto arquitetural, impacto operacional, PA-01 e Discoveries candidatas.

Ficam fora do escopo:

* logistica;
* coleta fisica;
* laboratorio;
* transporte;
* cadeia de custodia;
* planejamento externo;
* criacao de entidades, colecoes, camadas, persistencias ou interfaces.

## Base Documental Consultada

Foram consultados:

* `docs/operational/OP_00_OPERATIONAL_SCOPE_BOUNDARY_AUDIT.md`;
* `docs/operational/OP_01_OPERATIONAL_INFORMATION_FLOW_AUDIT.md`;
* `docs/research/DISCOVERY_CATALOG.md`;
* `docs/domain/GP_D01A_MONITORING_PROJECT_DOMAIN_AUDIT.md`;
* `docs/domain/GP_D01C_PERSISTENCE_STRATEGY_AUDIT.md`;
* `docs/domain/GP_D10A_PROJECT_INSTANCE_AUDIT.md`;
* `docs/architecture/CASE01_GLOBAL_ARCHITECTURE_AUDIT.md`;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`.

## Definicao Da Unidade Fundamental

A menor unidade operacional de informacao do PROTEUS e o registro informacional reconhecido.

Registro informacional reconhecido e qualquer fato, valor, referencia ou ocorrencia que ingressa no PROTEUS com contexto suficiente para ser registrado, organizado, avaliado quando aplicavel, apresentado, consolidado ou preservado.

Essa unidade nao e uma nova entidade. Ela e uma unidade conceitual de auditoria do fluxo informacional.

## Caracterizacao Da Unidade

Um registro informacional reconhecido se caracteriza por:

* possuir conteudo informacional minimo;
* ter origem identificavel ou reconhecivel;
* poder ser relacionado ao Projeto, contexto operacional, perfil, ponto, tipo de dado ou camada consumidora;
* ser apto a entrar no fluxo da OP-01;
* poder permanecer bruto, ser avaliado, ser consolidado, gerar sinal ou ser preservado como referencia;
* nao carregar por si mesmo autoridade para selecionar politica, executar avaliacao, gerar recomendacao ou alterar estado.

Em termos praticos, a unidade pode aparecer como:

* uma medicao de parametro;
* uma linha de registro operacional;
* uma observacao textual;
* uma referencia documental;
* um metadado recebido;
* um alerta produzido internamente;
* um evento operacional derivado;
* um sinal consolidado quando passa a ser consumido por camada posterior.

## O Que A Unidade Representa

A unidade fundamental nao representa exclusivamente uma medicao.

Classificacao:

| Candidato | E a unidade fundamental? | Justificativa |
| --- | --- | --- |
| Medicao | Parcialmente | E o subtipo mais central para avaliacao observacional, indicadores, alertas e relatorios, mas nao cobre contexto, referencias, eventos e memoria documental. |
| Registro | Sim | E a forma mais generica e minima capaz de abranger medicoes, observacoes, referencias, eventos e sinais reconhecidos pelo PROTEUS. |
| Conjunto de parametros | Nao | E uma agregacao de registros ou medicoes, nao a menor unidade. |
| Observacao | Parcialmente | Pode ser uma unidade quando registrada como informacao reconhecida, mas nao cobre valores, eventos e referencias. |
| Evento operacional | Nao como unidade primaria | E uma transformacao governada de alertas ou ocorrencias; pode conter registros, mas nao e a unidade minima de todo o fluxo. |
| Indicador | Nao | E resultado de consolidacao, calculo ou sintese de registros. |
| Referencia documental | Parcialmente | Pode ser unidade quando registrada como referencia reconhecida, mas nao cobre o fluxo completo. |

Veredito conceitual:

```text
Unidade fundamental = registro informacional reconhecido
Medicao = subtipo operacional principal dessa unidade
Indicador/alerta/evento/recomendacao/relatorio/Dossie = transformacoes ou consolidacoes posteriores
```

## Justificativa

A OP-00 definiu que o PROTEUS registra projetos, pontos, medicoes, indicadores, alertas, dashboards, relatorios, evidencias referenciais e Dossie Final.

A OP-01 definiu que o fluxo comeca quando uma informacao e registrada, recebida, organizada ou referenciada em estrutura interna reconhecida pelo sistema.

Portanto, a menor unidade nao pode ser apenas a medicao. A medicao explica o eixo observacional, mas o fluxo tambem aceita:

* dados ambientais como contexto;
* consumo e distribuicao como informacao operacional;
* observacoes externas;
* laudos e certificados como referencias;
* eventos de governanca;
* recomendacoes e sinais consolidados;
* informacoes permanentes no Dossie Final.

O conceito mais simples que cobre todos esses casos sem criar estrutura nova e registro informacional reconhecido.

## Relacao Com O Fluxo Operacional

No fluxo da OP-01, o registro informacional reconhecido percorre as etapas da seguinte forma:

```text
Registro informacional reconhecido
        |
Registro interno ou referencia reconhecida
        |
Organizacao por Projeto, contexto, tipo e origem
        |
        +--> Se for qualidade da agua:
        |        PolicyEngine -> AvaliacaoObservacionalService -> resultado observacional
        |
        +--> Se for contexto/coleta:
        |        Dashboard / Relatorios / Analytics, sem avaliacao hidrica obrigatoria
        |
        +--> Se gerar sinal analitico:
        |        indicadores, tendencias, alertas, Water Health Score
        |
        +--> Se gerar ocorrencia governavel:
        |        evento operacional, estado, rastreabilidade
        |
        +--> Se gerar sintese executiva:
        |        recomendacao, prioridade, snapshot executivo
        |
        +--> Se tiver valor documental:
                 relatorio, evidencia referencial ou Dossie Final
```

A unidade entra no fluxo como registro ou referencia. Ao longo do fluxo, pode permanecer unidade simples ou ser agregada a unidades maiores.

## Relacao Com O Dominio Projeto

O registro informacional reconhecido nao constitui novo agregado operacional e nao altera o Dominio Projeto.

Sua relacao com o Dominio Projeto e contextual:

* o Projeto fornece envelope, contexto, perfil, ponto principal, ciclo de vida e memoria permanente;
* a unidade informacional pode ser associada ao Projeto por contexto operacional;
* enquanto houver Projeto ativo unico, medicoes e registros operacionais permanecem relacionados ao Projeto por contexto, conforme GP-D01C;
* o Projeto nao deve armazenar diretamente todos os valores, alertas, eventos ou recomendacoes como se fosse repositorio operacional integral.

Assim, a unidade fundamental pertence ao fluxo operacional do PROTEUS, mas nao exige expansao do agregado Projeto.

## Relacao Com Indicadores

Indicadores surgem quando um ou mais registros informacionais reconhecidos sao agregados, calculados, classificados ou resumidos.

Exemplos:

* uma medicao pode contribuir para medias, minimos, maximos e ultimas leituras;
* uma sequencia de medicoes pode produzir tendencias;
* resultados observacionais podem compor Water Health Score;
* eventos podem compor contagens por estado;
* registros de contexto podem enriquecer leituras operacionais.

Indicador nao e a unidade fundamental. Indicador e produto derivado.

## Relacao Com Alertas

Alertas surgem quando registros informacionais, geralmente medicoes ou sinais derivados, atendem a criterios analiticos ou observacionais.

No caso de qualidade da agua, a medicao precisa respeitar PA-01:

* Policy Engine seleciona politica;
* Motor Observacional executa avaliacao;
* Analytics consome o resultado para gerar alerta quando aplicavel.

O alerta e uma transformacao do registro, nao sua forma primaria.

## Relacao Com Governanca

Governanca Operacional consome alertas e ocorrencias para criar ou atualizar eventos.

O registro informacional reconhecido participa da governanca como:

* evidencia de origem de um alerta;
* metadado observacional preservado;
* justificativa de criacao ou atualizacao de evento;
* referencia de rastreabilidade;
* parte do historico governado.

Evento operacional nao substitui a unidade fundamental. Ele e uma unidade governada posterior, com ciclo de vida proprio.

## Relacao Com Recomendacoes

Recomendacoes consomem sinais consolidados, nao registros brutos isolados como autoridade direta.

O registro informacional reconhecido participa das recomendacoes de forma indireta:

* medicoes contribuem para avaliacao, score e alertas;
* alertas e eventos compoem evidencias;
* tendencias e resumo de governanca sustentam justificativas;
* recomendacoes preservam rastreabilidade ate sinais de origem.

Recommendation nao deve acessar CSV diretamente, selecionar politica, executar avaliacao ou reclassificar eventos.

## Relacao Com Dashboards

Dashboards apresentam registros, resultados e sinais consolidados.

A unidade informacional pode chegar ao Dashboard como:

* ultima medicao;
* status observacional derivado;
* dado ambiental ou de consumo;
* indicador;
* alerta;
* score;
* tendencia;
* evento ou prioridade executiva.

Dashboard nao cria a unidade fundamental e nao deve decidir seu significado observacional fora das camadas responsaveis.

## Relacao Com Relatorios

Relatorios consolidam registros informacionais reconhecidos em resumo operacional e documental.

Podem apresentar:

* ultimas medicoes;
* totais;
* medias;
* status observacionais derivados;
* dados de contexto;
* alertas relevantes;
* sinteses executivas.

Relatorio nao e a unidade fundamental. Ele e uma consolidacao de unidades e sinais.

## Relacao Com O Dossie Final

O Dossie Final preserva memoria permanente do Projeto, mas nao copia integralmente todos os registros informacionais.

A unidade participa do Dossie quando:

* contribui para sinteses permanentes;
* sustenta resultados consolidados;
* fundamenta alertas relevantes;
* compoe eventos relevantes;
* origina recomendacoes emitidas;
* aparece como referencia documental permanente.

Medicoes individuais, logs, estados intermediarios, dados temporarios e detalhes reconstruiveis permanecem fora do Dossie, salvo como sintese ou referencia.

## Unidade Unica Ou Multiplas Unidades

Existe uma unidade fundamental conceitual unica: registro informacional reconhecido.

Existem, porem, multiplos subtipos operacionais dessa unidade:

* medicao de qualidade da agua;
* dado ambiental;
* dado de consumo/distribuicao;
* observacao;
* referencia documental;
* metadado externo;
* alerta;
* evento operacional;
* sinal consolidado.

Esses subtipos nao justificam nova entidade comum neste momento. Eles representam formas diferentes de informacao reconhecida no fluxo.

## Necessidade De Nova Entidade

Nao existe necessidade objetiva de criar nova entidade para a unidade fundamental.

Justificativa:

* a unidade ja esta implicitamente representada por registros operacionais, linhas de CSV, eventos, referencias e sinais existentes;
* criar uma entidade generica de informacao poderia duplicar persistencias atuais;
* uma entidade generica aumentaria abstracao sem necessidade operacional comprovada;
* GP-D01C ja reforcou que nem mesmo a relacao Medicao -> Projeto precisa ser materializada por linha enquanto houver Projeto ativo unico;
* PA-03 recomenda materializacao apenas sob necessidade objetiva.

## Necessidade De Novo Dominio

Nao existe necessidade objetiva de criar novo dominio.

O registro informacional reconhecido e unidade de fluxo, nao agregado de dominio.

O Dominio Projeto continua responsavel por contexto, ciclo de vida e memoria permanente. As camadas existentes continuam responsaveis por avaliacao, analise, governanca, recomendacao e apresentacao.

## Representacao Implicita Atual

A unidade atual ja esta implicitamente representada no sistema e na documentacao.

Evidencias:

* OP-00 reconhece registros de projeto, pontos, medicoes, indicadores, alertas, relatorios, evidencias e Dossie Final;
* OP-01 define o primeiro evento como registro interno de uma informacao reconhecida;
* GP-D01A separa Projeto, Amostra, Medicao e Contexto Operacional em nivel conceitual;
* GP-D01C preserva medicoes relacionadas ao Projeto por contexto, sem `projeto_id` por linha;
* GP-A23 descreve coleta como registro de dados operacionais e fornecimento de dados brutos para camadas posteriores;
* GP-D10A confirma que instancias do Projeto fornecem contexto, nao novo dominio.

## Criterios Que Sustentam A Conclusao

Os criterios usados foram:

1. Menor granularidade capaz de entrar no fluxo da OP-01.
2. Capacidade de representar medicoes sem limitar o fluxo apenas a medicoes.
3. Capacidade de representar referencias, observacoes, eventos e sinais sem criar entidade generica artificial.
4. Compatibilidade com OP-00 e sua fronteira operacional.
5. Preservacao do Dominio Projeto saturado.
6. Preservacao de PA-01.
7. Aderencia a PA-03: nao materializar sem necessidade objetiva.
8. Aderencia a PA-02: agregar valor por enriquecimento das camadas existentes.
9. Compatibilidade com persistencia atual e com eventual migracao futura.
10. Ausencia de lacuna operacional que exija novo dominio ou entidade.

## Impacto Arquitetural

Nao ha impacto arquitetural implementado.

A OP-02 apenas nomeia documentalmente a unidade fundamental do fluxo informacional. Nao cria entidade, colecao, camada, persistencia, interface, repositorio, servico ou agregado.

O impacto arquitetural e de criterio: futuras implementacoes devem distinguir unidade informacional, subtipo operacional, sinal derivado e memoria consolidada antes de propor materializacao.

## Impacto Operacional

O impacto operacional e a clarificacao de que:

* medicao e o subtipo mais importante para avaliacao hidrica;
* registro e a forma minima comum do fluxo;
* indicadores, alertas, eventos, recomendacoes, dashboards, relatorios e Dossie Final sao transformacoes, apresentacoes ou consolidacoes;
* nem toda informacao que percorre o fluxo precisa virar entidade;
* informacoes externas podem ser recebidas como registros ou referencias sem absorver o processo externo.

## Analise PA-01

PA-01 permanece integralmente preservado.

O registro informacional reconhecido:

* nao seleciona politica;
* nao executa avaliacao;
* nao define severidade;
* nao calcula score;
* nao cria evento por si so;
* nao emite recomendacao;
* nao substitui o Nucleo de Monitoramento Hidrico.

Quando a unidade for uma medicao de qualidade da agua, o fluxo correto permanece:

```text
Registro da medicao
-> PolicyEngine seleciona politica
-> AvaliacaoObservacionalService executa avaliacao
-> resultado observacional e consumido por Analytics, Governanca, Dashboard e Relatorios
```

## Analise Das Discoveries

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Impacto registrado:

* PA-02 foi reforcada: a unidade fundamental permite explicar como valor e agregado progressivamente por camadas existentes, sem nova camada arquitetural.
* PA-03 foi reforcada: a unidade foi reconhecida conceitualmente sem materializacao automatica em entidade, colecao ou persistencia.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida automaticamente.
* Nenhuma nova Discovery candidata foi identificada.

## Respostas As Questoes Obrigatorias

1. A menor unidade operacional de informacao do PROTEUS e o registro informacional reconhecido.
2. Essa unidade se caracteriza por conter informacao minima, origem reconhecivel, contexto suficiente e capacidade de entrar no fluxo da OP-01.
3. Ela representa primariamente um registro. Uma medicao e seu subtipo operacional mais importante; observacoes e referencias tambem podem ser unidades; conjunto de parametros e agregacao, nao unidade minima.
4. A unidade nao pertence ao Dominio Projeto como novo elemento estrutural e nao constitui novo agregado operacional. Ela percorre o fluxo contextualizada pelo Projeto.
5. Ela ingressa na OP-01 como registro interno, dado persistido, referencia reconhecida ou informacao recebida.
6. Ela percorre registro, organizacao, avaliacao quando aplicavel, analise, governanca, recomendacao/sintese, apresentacao, relatorio e preservacao documental.
7. Ela participa de indicadores por agregacao, calculo ou resumo.
8. Ela participa de alertas quando criterios observacionais ou analiticos sao atendidos.
9. Ela participa de governanca quando alertas ou ocorrencias se tornam eventos rastreaveis.
10. Ela participa de recomendacoes de forma indireta, como origem de sinais consolidados.
11. Ela participa de dashboards como dado, status, indicador, alerta, score, evento ou prioridade apresentada.
12. Ela participa de relatorios como dado apresentado ou consolidado.
13. Ela participa da memoria permanente apenas quando consolidada, referenciada ou sintetizada no Dossie Final.
14. Existe uma unidade fundamental conceitual unica, com multiplos subtipos operacionais.
15. Nao existe necessidade objetiva de criar nova entidade.
16. Nao existe necessidade objetiva de criar novo dominio.
17. A unidade atual ja esta implicitamente representada no sistema por registros operacionais, medicoes, eventos, referencias e sinais.
18. A conclusao se sustenta por granularidade minima, cobertura do fluxo, preservacao do Dominio Projeto, PA-01, OP-00, OP-01, PA-02 e PA-03.

## Observacoes Da IA / Hipoteses Metodologicas

As observacoes abaixo nao alteram o escopo da OP-02, nao modificam o ICFACTORY, nao alteram PA-01, PA-02 ou PA-03 e nao sao promovidas automaticamente.

| Padrao observado | Evidencia usada | Possivel impacto | Recomendacao | Status sugerido |
| --- | --- | --- | --- | --- |
| A unidade fundamental de um fluxo informacional pode ser conceitual sem exigir entidade tecnica. | OP-01 define fluxo por informacao reconhecida; GP-D01C adia materializacao por linha. | Ajuda a evitar entidades genericas prematuras. | Exigir necessidade operacional antes de materializar unidades conceituais. | Hipotese em monitoramento |
| Medicao e central, mas nao universal, em sistemas que tambem preservam contexto, referencias e memoria. | OP-00 inclui medicoes, evidencias, relatorios e Dossie; OP-01 inclui contexto e referencias. | Evita reduzir o PROTEUS a um sistema de medicoes. | Separar subtipo central de unidade fundamental em auditorias futuras. | Observacao simples |
| Sinais derivados podem virar novas entradas para etapas posteriores sem deixarem de ser produtos de registros anteriores. | Analytics gera alertas e score; Governanca gera eventos; Recommendation gera recomendacoes. | Explica fluxos paralelos sem criar novo dominio. | Tratar sinais derivados como unidades de consumo posterior apenas quando reconhecidos pelo fluxo. | Observacao simples |

Nenhuma observacao acima e Discovery oficial. Nenhuma nova Discovery candidata foi criada nesta auditoria.

## Veredito Final

A unidade fundamental de informacao do PROTEUS e o registro informacional reconhecido.

Essa unidade e conceitual e ja esta implicitamente representada no sistema. A medicao e o subtipo operacional mais relevante para avaliacao hidrica, mas nao e suficiente para representar todo o fluxo informacional definido na OP-01.

Nao ha necessidade objetiva de criar nova entidade, novo agregado, novo dominio, nova colecao, nova camada, nova persistencia ou nova interface.

O modelo atual e suficiente para orientar futuras implementacoes, desde que qualquer materializacao futura seja precedida por necessidade objetiva e auditoria propria.

## Declaracao ICFACTORY / IA

1. A execucao permaneceu sob governanca ICFACTORY.
2. Nao houve extrapolacao da IA para implementacao, arquitetura, persistencia, interface, entidades, colecoes, camadas, Dominio Projeto ou Dossie Final.
3. Houve hipoteses metodologicas registradas separadamente como observacoes da IA, sem efeito normativo.
4. A unidade fundamental de informacao ficou suficientemente definida para orientar futuras implementacoes.

## Testes

Nao executados.

Justificativa: OP-02 exclusivamente documental, sem alteracao de codigo, runtime, interface ou persistencia.

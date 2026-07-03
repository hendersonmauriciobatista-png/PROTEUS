# OP-03 - Auditoria Dos Tipos De Registros Informacionais

## Objetivo

Identificar, exclusivamente por auditoria documental e de dominio, quais categorias de registros informacionais sao reconhecidas pelo PROTEUS durante seu fluxo operacional.

Esta auditoria nao cria entidades, nao implementa codigo, nao altera arquitetura, nao altera persistencia, nao altera interface, nao altera o Dominio Projeto e nao altera o Dossie Final.

O objetivo e apenas classificar os tipos de registros que participam do fluxo operacional definido pela OP-01 e pela unidade fundamental definida pela OP-02.

## Escopo

O escopo desta OP-03 inclui:

* classificar os registros informacionais reconhecidos pelo PROTEUS;
* distinguir registros primarios, derivados, consolidados e transitorios;
* definir a relacao entre medicoes, observacoes, eventos, alertas, indicadores, recomendacoes, relatorios e Dossie Final;
* avaliar se alguma categoria exige entidade, colecao, dominio, camada, persistencia ou interface propria;
* avaliar impacto arquitetural, impacto operacional, PA-01 e Discoveries candidatas.

Ficam fora do escopo:

* logistica;
* coleta fisica;
* laboratorio;
* transporte;
* cadeia de custodia fisica;
* planejamento externo;
* implementacao de codigo;
* alteracao de arquitetura, persistencia, interface, entidades, colecoes, camadas, Dominio Projeto ou Dossie Final.

## Base Documental Consultada

Foram consultados:

* `docs/operational/OP_00_OPERATIONAL_SCOPE_BOUNDARY_AUDIT.md`;
* `docs/operational/OP_01_OPERATIONAL_INFORMATION_FLOW_AUDIT.md`;
* `docs/operational/OP_02_INFORMATION_UNIT_AUDIT.md`;
* `docs/research/DISCOVERY_CATALOG.md`;
* `docs/domain/GP_D01A_MONITORING_PROJECT_DOMAIN_AUDIT.md`;
* `docs/domain/GP_D01C_PERSISTENCE_STRATEGY_AUDIT.md`;
* `docs/domain/GP_D10A_PROJECT_INSTANCE_AUDIT.md`;
* `docs/architecture/CASE01_GLOBAL_ARCHITECTURE_AUDIT.md`;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`.

## Definicao Das Categorias De Registros

Categoria de registro informacional e uma classificacao documental de uma forma pela qual o registro informacional reconhecido aparece no fluxo do PROTEUS.

Essa classificacao nao equivale a entidade, classe, tabela, colecao, tela ou camada. Ela apenas descreve a natureza operacional da informacao reconhecida.

As categorias auditadas sao:

* registros primarios;
* registros derivados;
* registros consolidados;
* registros transitorios;
* memoria documental consolidada.

## Classificacao Dos Registros Reconhecidos

| Categoria | Tipo | Papel no fluxo | Exige entidade propria? | Observacao |
| --- | --- | --- | --- | --- |
| Medicao de qualidade da agua | Primario | Valor observado de parametro hidrico usado em avaliacao, indicadores, alertas e relatorios. | Nao nesta OP | Principal subtipo operacional da unidade fundamental. |
| Dado ambiental | Primario/contextual | Contexto operacional usado por Dashboard, Relatorios e Analytics. | Nao | Nao exige avaliacao hidrica obrigatoria. |
| Dado de consumo/distribuicao | Primario/operacional | Registro operacional usado por Dashboard, Relatorios e Analytics. | Nao | Pode alimentar indicadores e regras analiticas. |
| Observacao operacional | Primario/contextual | Texto ou anotacao reconhecida que qualifica o registro. | Nao | Pode acompanhar medicoes, contexto ou referencias. |
| Referencia documental externa | Primario/referencial | Laudo, certificado, evidencia ou metadado recebido sem absorver processo externo. | Nao | Pode compor memoria por referencia. |
| Metadado de contexto | Primario/contextual | Data, responsavel, ponto, origem, equipamento referenciado ou restricao relevante. | Nao | Organiza e qualifica outros registros. |
| Resultado observacional | Derivado | Resultado da avaliacao executada pelo Motor Observacional apos selecao de politica. | Nao | Deriva principalmente de medicoes de qualidade. |
| Indicador | Derivado/consolidado | Media, tendencia, contagem, score, resumo ou prioridade calculada. | Nao | Produto de agregacao ou interpretacao. |
| Alerta | Derivado | Sinal produzido por criterio analitico ou observacional. | Nao | Pode originar evento de governanca. |
| Evento operacional | Derivado/governado | Ocorrencia reconhecida e acompanhada por Governanca Operacional. | Nao nesta OP | Ja existe como estrutura operacional, mas OP-03 nao cria nova entidade. |
| Recomendacao | Derivado/executivo | Orientacao produzida a partir de sinais consolidados. | Nao | Nao recalcula avaliacao nem cria evento por si so. |
| Snapshot ou sintese executiva | Consolidado | Composicao de score, alertas, eventos, tendencias e recomendacoes. | Nao | Base para Painel Executivo. |
| Relatorio | Apresentacao/consolidado | Documento ou exportacao que apresenta informacoes e resumos. | Nao | Apresenta e consolida; nao e unidade primaria. |
| Dossie Final | Memoria consolidada | Memoria permanente do Projeto encerrado ou arquivado. | Nao | Nao copia integralmente registros operacionais. |
| Log, estado intermediario ou calculo temporario | Transitorio | Suporte operacional ou tecnico sem valor permanente automatico. | Nao | Deve permanecer fora do Dossie salvo justificativa futura. |

## Relacao Entre As Categorias

As categorias se relacionam por transformacao, agregacao e apresentacao.

```text
Registros primarios
  -> resultados observacionais
  -> indicadores
  -> alertas
  -> eventos governados
  -> recomendacoes
  -> snapshots e sinteses
  -> dashboards e relatorios
  -> memoria documental consolidada
```

A relacao nao e uma hierarquia de dominio. E uma hierarquia informacional de maturidade:

* primario: entra no sistema;
* derivado: nasce de regra, avaliacao ou transformacao;
* consolidado: agrega multiplos registros ou sinais;
* transitorio: apoia processamento, mas nao possui valor permanente automatico;
* memoria: preserva sintese permanente.

## Registros Primarios

Registros primarios sao os registros informacionais que ingressam no PROTEUS antes de qualquer transformacao interna relevante.

Incluem:

* medicoes de qualidade da agua;
* dados ambientais;
* dados de consumo e distribuicao;
* observacoes operacionais;
* referencias documentais externas;
* metadados de contexto;
* registros de Projeto, contexto, perfil e ponto enquanto informacoes de enquadramento.

Esses registros sao a entrada operacional do fluxo. Eles podem ser apresentados diretamente, avaliados, agregados ou preservados por referencia.

## Registros Derivados

Registros derivados sao informacoes produzidas internamente a partir de registros primarios ou de outros sinais reconhecidos.

Incluem:

* resultado observacional;
* indicador;
* alerta;
* evento operacional;
* recomendacao;
* prioridade ou sinal executivo.

Um registro derivado nao elimina nem substitui o registro primario. Ele adiciona leitura operacional, analitica, governada ou executiva.

## Registros Consolidados

Registros consolidados sao sinteses de multiplos registros primarios ou derivados.

Incluem:

* tendencias;
* Water Health Score;
* resumos estatisticos;
* contagens de eventos;
* snapshots analiticos;
* snapshots executivos;
* relatorios;
* historicos resumidos;
* blocos consolidados do Dossie Final.

O consolidado reduz volume e aumenta significado. Ele nao deve virar copia paralela integral da operacao.

## Registros Transitorios

Registros transitorios sao informacoes de processamento, interface, calculo intermediario, estado temporario ou suporte operacional que nao possuem valor permanente automatico.

Incluem:

* calculos intermediarios;
* estados de tela;
* rascunhos;
* logs tecnicos;
* resultados linha a linha quando apenas apoiam resumo;
* alertas repetitivos sem relevancia final;
* eventos cotidianos sem impacto;
* dados reconstruiveis sem perda.

Eles podem ser usados internamente, mas nao justificam entidade propria nem inclusao automatica no Dossie Final.

## Memoria Documental Consolidada

Memoria documental consolidada e o nivel em que informacoes deixam de representar operacao diaria e passam a explicar o Projeto de forma permanente.

O Dossie Final pertence a esse nivel.

O Dossie Final nao e um registro primario. Ele e memoria consolidada do Projeto, formada por identidade, contexto, periodo, situacao final, sinteses operacionais, sinais analiticos, eventos relevantes, recomendacoes, evidencias referenciais e conclusao executiva.

## Analise Por Tipo Solicitado

### Medicao

A medicao constitui tipo especifico de registro.

E o principal subtipo operacional do registro informacional reconhecido, especialmente para qualidade da agua. Pode gerar resultado observacional, indicadores, alertas, score, relatorios e memoria consolidada.

Nao exige nova entidade nesta OP-03.

### Observacoes Operacionais

Observacoes operacionais constituem registros proprios quando sao reconhecidas pelo PROTEUS como informacao associada a medicao, contexto, evento, referencia ou Projeto.

Elas sao registros primarios/contextuais e podem qualificar outros registros.

Nao exigem entidade propria.

### Eventos Reconhecidos Pelo Sistema

Eventos reconhecidos pelo sistema constituem registros derivados/governados.

Eles nao sao a unidade primaria do fluxo inteiro, mas sao registros reconhecidos quando Governanca Operacional transforma alertas ou ocorrencias em eventos acompanhaveis.

### Alertas

Alertas representam registros derivados.

Eles sao novas informacoes reconhecidas pelo sistema, mas derivam de registros anteriores, resultados observacionais, tendencias ou regras analiticas. Portanto, sao transformacoes de registros anteriores e tambem registros consumiveis por etapas posteriores.

### Indicadores

Indicadores representam consolidacoes ou derivados analiticos.

Nao sao registros primarios. Sao resultados de agregacao, calculo, contagem, tendencia, score ou resumo.

### Recomendacoes

Recomendacoes representam registros derivados executivos.

Surgem de sinais consolidados e devem manter rastreabilidade para alertas, score, tendencias, eventos ou resumos usados como evidencia.

### Relatorios

Relatorios representam apresentacoes consolidadas.

O relatorio pode ser preservado como documento ou exportacao, mas sua natureza informacional e de apresentacao/consolidacao, nao de registro primario.

### Dossie Final

O Dossie Final representa memoria consolidada.

Ele nao e registro primario nem simples relatorio. Sua funcao e preservar memoria permanente do Projeto encerrado ou arquivado, sem copiar integralmente a operacao diaria.

## Categoria Relevante Ainda Nao Identificada

Foi identificada uma categoria relevante que deve ser nomeada explicitamente, mas nao materializada:

* registro de referencia externa.

Essa categoria inclui laudos, certificados, evidencias, resultados laboratoriais recebidos, metadados externos e documentos de apoio. A OP-00 ja reconhecia que o PROTEUS pode receber ou referenciar essas informacoes sem absorver laboratorio, cadeia fisica ou logistica.

Nao se trata de nova Discovery e nao exige entidade propria nesta OP-03.

## Necessidade De Entidade Propria

Nenhuma categoria auditada exige entidade propria nesta OP-03.

Justificativa:

* a auditoria e classificatoria;
* as categorias ja estao implicitamente representadas por registros, CSVs, eventos, snapshots, relatorios e Dossie;
* criar entidades por categoria anteciparia materializacao sem necessidade objetiva;
* PA-03 permanece aplicavel;
* OP-02 ja concluiu que a unidade fundamental e conceitual e nao exige entidade generica.

## Necessidade De Novo Dominio

Nenhuma categoria exige novo dominio.

As categorias representam formas de informacao dentro do fluxo operacional, nao novos agregados de negocio.

O Dominio Projeto permanece responsavel por contexto, ciclo de vida e memoria permanente. As demais responsabilidades permanecem nas camadas existentes.

## Categorias Meramente Transitorias

Existem categorias meramente transitorias.

Sao transitorios:

* calculos intermediarios;
* estados de tela;
* rascunhos;
* logs tecnicos;
* resultados linha a linha usados apenas como suporte;
* alertas repetitivos sem relevancia final;
* eventos cotidianos sem impacto;
* dados reconstruiveis sem perda.

Essas categorias podem existir tecnicamente ou operacionalmente, mas nao devem ser promovidas automaticamente a memoria permanente, entidade propria ou Dossie Final.

## Hierarquia Entre Os Tipos De Registros

Existe hierarquia informacional, nao hierarquia de dominio.

```text
Primarios
  -> Derivados
      -> Consolidados
          -> Apresentados
              -> Preservados como memoria quando houver valor permanente

Transitorios
  -> podem apoiar qualquer etapa
  -> nao possuem preservacao automatica
```

Essa hierarquia orienta o fluxo, mas nao cria classes, tabelas ou agregados.

## Suficiencia Do Conjunto Atual

O conjunto atual e suficiente para representar o fluxo operacional definido na OP-01 em nivel documental.

As categorias cobrem:

* entrada;
* contexto;
* avaliacao;
* indicadores;
* alertas;
* governanca;
* recomendacoes;
* apresentacao;
* relatorios;
* preservacao documental;
* transitorios sem valor permanente automatico.

Nao foi encontrada lacuna que exija nova categoria estrutural, entidade, dominio ou camada.

## Impacto Arquitetural

Nao ha impacto arquitetural implementado.

A OP-03 apenas classifica tipos de registros informacionais. Nao cria entidade, colecao, camada, persistencia, interface, repositorio, servico, dominio ou alteracao no Dossie Final.

O impacto arquitetural e documental: futuras implementacoes devem declarar se lidam com registro primario, derivado, consolidado, transitorio ou memoria documental antes de propor materializacao.

## Impacto Operacional

O impacto operacional e a clarificacao da natureza das informacoes que percorrem o PROTEUS:

* medicoes e referencias entram como registros primarios;
* observacoes qualificam registros;
* resultados observacionais, alertas, eventos e recomendacoes sao derivados;
* indicadores, snapshots e relatorios sao consolidacoes ou apresentacoes;
* Dossie Final e memoria permanente consolidada;
* transitorios nao devem ser confundidos com memoria ou entidade.

Essa classificacao reduz ambiguidade antes de futuras implementacoes.

## Analise PA-01

PA-01 permanece integralmente preservado.

A classificacao nao desloca autoridade entre camadas:

* medicao nao seleciona politica;
* contexto nao executa avaliacao;
* Policy Engine seleciona politica;
* Motor Observacional executa avaliacao;
* Analytics produz indicadores e alertas;
* Governanca acompanha eventos;
* Recommendation produz recomendacoes a partir de sinais consolidados;
* Dashboard e Relatorios apresentam;
* Dossie Final preserva memoria consolidada.

Nenhuma categoria autoriza UI, relatorio, governanca, recomendacao ou Dossie a substituir o Nucleo de Monitoramento Hidrico.

## Analise Das Discoveries

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Impacto registrado:

* PA-02 foi reforcada: as categorias mostram progressao de valor por transformacao de registros primarios em derivados, consolidados, apresentacoes e memoria, sem criar nova camada arquitetural.
* PA-03 foi reforcada: a classificacao de categorias nao exige materializacao automatica em entidade, colecao, persistencia ou dominio.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida automaticamente.
* Nenhuma nova Discovery candidata foi identificada.

## Respostas As Questoes Obrigatorias

1. O PROTEUS reconhece registros primarios, derivados, consolidados, transitorios e memoria documental consolidada.
2. A medicao constitui tipo especifico de registro primario e e o subtipo operacional principal.
3. Observacoes operacionais constituem registros proprios quando reconhecidas pelo sistema.
4. Eventos reconhecidos pelo sistema constituem registros derivados/governados.
5. Alertas representam transformacoes de registros anteriores e tambem registros derivados consumiveis por etapas posteriores.
6. Indicadores representam consolidacoes ou derivados, nao registros primarios.
7. Recomendacoes representam registros derivados executivos.
8. Relatorios representam apresentacoes consolidadas e podem ser preservados como documentos, mas nao sao registros primarios.
9. O Dossie Final representa memoria consolidada, nao registro primario.
10. A categoria relevante nomeada explicitamente nesta OP-03 e registro de referencia externa; ela ja estava implicitamente reconhecida pela OP-00.
11. Nenhuma categoria exige entidade propria nesta OP-03.
12. Nenhuma categoria exige novo dominio.
13. Existem categorias transitorias, como logs, calculos intermediarios, rascunhos, estados de tela e dados reconstruiveis sem valor permanente automatico.
14. Existe hierarquia informacional entre primarios, derivados, consolidados, apresentados e preservados; nao existe hierarquia de dominio criada.
15. O conjunto atual e suficiente para representar o fluxo operacional definido na OP-01.

## Observacoes Da IA / Hipoteses Metodologicas

As observacoes abaixo nao alteram o escopo da OP-03, nao modificam o ICFACTORY, nao alteram PA-01, PA-02 ou PA-03 e nao sao promovidas automaticamente.

| Padrao observado | Evidencia usada | Possivel impacto | Recomendacao | Status sugerido |
| --- | --- | --- | --- | --- |
| Tipos de registros podem ser classificados por maturidade informacional sem virar tipos tecnicos. | OP-02 definiu unidade conceitual; OP-03 classifica primarios, derivados, consolidados e transitorios. | Ajuda a evitar entidades prematuras. | Usar classificacao documental antes de qualquer materializacao. | Hipotese em monitoramento |
| Alertas e recomendacoes sao simultaneamente produtos derivados e novas entradas para etapas posteriores. | OP-01 mostra alertas indo para Governanca e sinais indo para Recommendation. | Explica o fluxo sem criar ciclos de dominio. | Registrar origem e rastreabilidade sempre que sinal derivado for consumido posteriormente. | Observacao simples |
| Memoria permanente depende de selecao de relevancia, nao do tipo tecnico original do registro. | GP-D04C e OP-02 excluem dados granulares e preservam sinteses. | Evita que toda medicao ou alerta vire Dossie. | Auditar criterios de relevancia antes de ampliar preservacao documental. | Observacao simples |

Nenhuma observacao acima e Discovery oficial. Nenhuma nova Discovery candidata foi criada nesta auditoria.

## Veredito Final

As categorias de registros informacionais reconhecidas pelo PROTEUS estao suficientemente classificadas em nivel documental.

O conjunto atual e:

```text
Registros primarios
Registros derivados
Registros consolidados
Registros transitorios
Memoria documental consolidada
```

Medicoes sao registros primarios centrais. Observacoes e referencias tambem podem ser registros primarios. Alertas, eventos e recomendacoes sao derivados. Indicadores e snapshots sao derivados ou consolidados. Relatorios sao apresentacoes consolidadas. Dossie Final e memoria consolidada.

Nao ha necessidade objetiva de criar entidade, colecao, novo dominio, nova camada, persistencia, interface ou alteracao do Dossie Final.

## Declaracao ICFACTORY / IA

1. A execucao permaneceu sob governanca ICFACTORY.
2. Nao houve extrapolacao da IA para implementacao, arquitetura, persistencia, interface, entidades, colecoes, camadas, Dominio Projeto ou Dossie Final.
3. Houve hipoteses metodologicas registradas separadamente como observacoes da IA, sem efeito normativo.
4. A classificacao dos registros ficou suficientemente definida para orientar futuras implementacoes.

## Testes

Nao executados.

Justificativa: OP-03 exclusivamente documental, sem alteracao de codigo, runtime, interface ou persistencia.

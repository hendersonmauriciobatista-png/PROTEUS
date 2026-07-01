# GP-D03C - Priorizacao Das Ressalvas Do Ciclo De Vida

## Data

30/06/2026

## Contexto

O Sistema de Analise de Agua segue a metodologia ICFACTORY.

A GP-D03A auditou o Ciclo de Vida do Projeto de Monitoramento e concluiu:

**Ciclo de Vida suportado com ressalvas.**

A GP-D03B auditou exclusivamente essas ressalvas e concluiu:

**Ressalvas importantes.**

Nenhuma ressalva foi classificada como critica. Esta GP-D03C prioriza apenas as ressalvas importantes identificadas na GP-D03B, sem abrir nova auditoria ampla e sem implementar funcionalidade.

## Objetivo

Priorizar as ressalvas importantes identificadas na GP-D03B e definir qual deve ser tratada primeiro para agregar maior valor ao CASE-01.

## Pergunta Central

Qual ressalva importante deve ser tratada primeiro para agregar maior valor ao CASE-01?

## Metodo

1. Leitura integral de `docs/domain/GP_D03B_LIFECYCLE_REMARKS_AUDIT.md`.
2. Extracao apenas das ressalvas classificadas como importantes.
3. Avaliacao de valor ao Projeto, impacto operacional, dependencias, risco de adiamento, complexidade provavel, PA-01, GP-A23 e possibilidade de enriquecimento das estruturas existentes.
4. Aplicacao do criterio institucional "Agrega valor ao projeto?".
5. Consulta obrigatoria ao `DISCOVERY_CATALOG.md`.
6. Registro documental da ordem recomendada.

## Lista Das Ressalvas Importantes

Foram extraidas da GP-D03B as seguintes ressalvas importantes:

1. Planejamento do Projeto ausente.
2. Estados do Projeto ainda nao auditados.
3. Relatorio final ou dossie do Projeto ausente.
4. Arquivamento do Projeto ausente.
5. Encerramento do Projeto ausente.

Ressalvas desejaveis ou futuras nao foram priorizadas nesta GP:

* Vinculo Projeto -> Configuracao.
* Amostra formal.
* Rastreabilidade historica Medicao -> Projeto.
* Analytics por Projeto historico.

## Criterio Institucional

Filtro obrigatorio:

> Agrega valor ao projeto?

Nesta GP, uma ressalva agrega valor prioritario quando:

* melhora a representacao do Projeto de Monitoramento real;
* desbloqueia outras ressalvas importantes;
* preserva PA-01;
* nao exige nova camada arquitetural;
* pode ser tratada por enriquecimento das estruturas existentes;
* reduz ambiguidade operacional relevante.

## Matriz De Prioridade

| Ressalva importante | Valor que agrega ao Projeto | Impacto operacional | Dependencias | Risco se adiada | Complexidade provavel | Preserva PA-01? | Exige nova camada? | Enriquecimento existente? | Prioridade |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Encerramento do Projeto | Permite concluir formalmente o Projeto, congelar contexto e registrar resultado final | Alto | Estados do Projeto; criterios de conclusao; dossie futuro | O sistema continua monitorando bem, mas nao fecha Projeto real | Media | Sim | Nao | Sim | 1 |
| Estados do Projeto | Define semantica para ativo, pausado, encerrado e arquivado | Alto | Modelo de Projeto existente | `status` pode permanecer ambiguo | Baixa/Media | Sim | Nao | Sim | 2 |
| Planejamento do Projeto | Conecta Projeto e coletas por objetivo, periodo e escopo | Alto | Estados podem ajudar, mas nao bloqueiam totalmente | Coletas seguem sem plano formal auditavel | Media | Sim | Nao | Sim | 3 |
| Arquivamento do Projeto | Separa Projeto historico de operacao ativa | Medio/Alto | Estados e encerramento | Evento arquivado pode ser confundido com Projeto arquivado | Baixa/Media | Sim | Nao | Sim | 4 |
| Dossie final do Projeto | Consolida memoria final com sinais, eventos e recomendacoes | Medio/Alto | Encerramento; relatorio final; fontes consolidadas | Conhecimento permanece disperso | Media | Sim | Nao | Sim | 5 |

## Justificativa Da Ordem Proposta

### 1. Encerramento Do Projeto

Encerramento deve ser tratado primeiro como frente de valor, porque e a lacuna que mais impede o ciclo de vida de ser considerado completo.

A GP-D03B registrou que, sem encerramento, o CASE-01 acompanha bem a operacao, mas nao conclui formalmente o Projeto de Monitoramento. Essa ressalva tambem organiza outras lacunas:

* exige estados claros;
* prepara arquivamento;
* cria necessidade objetiva para dossie final;
* ajuda a separar operacao continua de Projeto concluido.

Aplicacao do filtro "Agrega valor ao projeto?": sim. Encerramento transforma o Projeto de um contexto ativo continuo em unidade operacional com conclusao auditavel.

Observacao metodologica: tratar encerramento primeiro nao significa implementar encerramento imediatamente. A primeira GP futura deve auditar estados e criterios de encerramento, porque o encerramento depende de semantica de ciclo.

### 2. Estados Do Projeto

Estados do Projeto aparecem como prioridade tecnica e conceitual imediata dentro da frente de encerramento.

Eles devem ser auditados antes de qualquer implementacao porque evitam que `status` seja apenas um texto sem semantica. Estados tambem sustentam arquivamento e encerramento.

Aplicacao do filtro "Agrega valor ao projeto?": sim. Estados tornam o ciclo legivel e reduzem ambiguidade operacional.

### 3. Planejamento Do Projeto

Planejamento agrega alto valor porque conecta Projeto e coletas. No entanto, ele nao destrava tantas ressalvas quanto encerramento/estados.

Planejamento deve ser a proxima frente apos a semantica do ciclo, ou ser auditado em paralelo apenas se houver necessidade operacional expressa.

Aplicacao do filtro "Agrega valor ao projeto?": sim, mas como segunda frente de dominio.

### 4. Arquivamento Do Projeto

Arquivamento agrega valor, mas depende de estados e encerramento. Tratar arquivamento antes de encerramento aumentaria o risco de confundir evento arquivado com Projeto arquivado.

Aplicacao do filtro "Agrega valor ao projeto?": sim, condicionado a estados.

### 5. Dossie Final Do Projeto

Dossie final agrega valor como memoria institucional do Projeto, mas depende de uma decisao de encerramento. Sem encerramento, o dossie pode virar apenas relatorio operacional enriquecido.

Aplicacao do filtro "Agrega valor ao projeto?": sim, condicionado ao encerramento.

## Primeira Ressalva Recomendada Para Tratamento

A primeira ressalva recomendada para tratamento e:

**Encerramento do Projeto ausente.**

Como tratamento controlado, a proxima GP nao deve implementar encerramento. Ela deve auditar:

* quais estados de Projeto existem;
* quais transicoes sao permitidas;
* quais criterios permitem encerrar um Projeto;
* o que significa arquivar depois de encerrar;
* quais responsabilidades permanecem fora do Projeto para preservar PA-01.

## GP Futura Sugerida

**GP-D03D - Auditoria Dos Estados E Criterios De Encerramento Do Projeto.**

Escopo sugerido:

* Auditar estados do Projeto como pre-requisito de encerramento.
* Definir se `ativo`, `pausado`, `encerrado` e `arquivado` agregam valor.
* Definir criterios minimos para encerramento.
* Separar encerramento de Projeto de arquivamento de eventos.
* Preservar PA-01.
* Nao implementar codigo nessa auditoria.

## Impacto Sobre PA-01

PA-01 permanece preservado.

A priorizacao de encerramento nao exige que Projeto:

* selecione politica;
* execute avaliacao observacional;
* interprete limites;
* calcule status hidrico;
* gere severidade;
* substitua Analytics, Governanca ou Recommendation.

Encerramento deve ser tratado como estado operacional do Projeto, nao como decisao observacional.

## Impacto Sobre GP-A23

GP-A23 permanece preservada.

A recomendacao nao cria nova camada arquitetural. A evolucao sugerida deve ocorrer por enriquecimento do dominio de Projeto ja existente, mantendo a cadeia consolidada:

Coleta -> Monitoramento Hidrico -> Analytics -> Governanca Operacional -> Executive Recommendation -> Executive Intelligence -> Painel Executivo.

## Consulta Ao DISCOVERY_CATALOG

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Impacto registrado:

* PA-02 - Progressao De Valor: reforcada. A priorizacao recomenda evoluir o dominio existente, sem criar nova camada.
* PA-03 - Materializacao Sob Necessidade: reforcada. Encerramento deve ser auditado antes de materializar novos campos, estados, artefatos ou persistencias.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida automaticamente.
* Nenhuma nova Discovery candidata foi identificada nesta GP.

## Conclusao

A maior lacuna de valor nao e coleta/amostra nem rastreabilidade tecnica neste momento. A maior lacuna e a ausencia de encerramento formal do Projeto.

Planejamento tambem agrega valor alto, mas encerramento deve vir primeiro porque:

* foi a ressalva mais forte da GP-D03B;
* diferencia operacao continua de Projeto completo;
* exige e organiza estados do Projeto;
* destrava arquivamento e dossie final;
* preserva PA-01;
* nao exige nova camada arquitetural;
* pode ser tratado por enriquecimento das estruturas existentes.

## Veredito Final

**Tratar encerramento primeiro.**

O tratamento deve comecar por auditoria documental dos estados e criterios de encerramento do Projeto, sem implementacao imediata.

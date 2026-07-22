# GP-D01C-A - Auditoria da Estrategia de Persistencia Medicao -> Projeto

Data: 30/06/2026

Status: AUDITORIA DOCUMENTAL CONCLUIDA

Natureza: Dominio / Persistencia

## Contexto

O Sistema de Analise de Agua segue a metodologia ICFACTORY.

Estado considerado nesta auditoria:

* GP-D01A aprovou o modelo minimo de dominio para Projeto de Monitoramento.
* GP-D01B implementou o Projeto ativo unico.
* A relacao conceitual Medicao -> Projeto permanece aprovada.
* A estrategia tecnica de persistencia dessa relacao foi removida da GP-D01B por nao estar explicitamente aprovada.
* Os CSVs operacionais atuais devem permanecer compativeis.

Esta auditoria nao implementa codigo, nao altera CSVs, nao altera runtime, nao altera interface e nao cria nova camada.

## Pergunta Central

Qual estrategia tecnica preserva simplicidade, compatibilidade e evolucao futura para relacionar medicoes a um Projeto de Monitoramento?

## Criterio Institucional

A estrategia deve maximizar simplicidade e minimizar acoplamento.

Filtros aplicados:

* Simplicidade.
* Compatibilidade com CSVs existentes.
* Facilidade de migracao futura.
* Rastreabilidade.
* Impacto na arquitetura.
* Compatibilidade com PA-01.
* Compatibilidade com futuras migracoes para SQLite/PostgreSQL.

## Alternativas Analisadas

### A) Adicionar `projeto_id` aos CSVs

Descricao:

Adicionar uma coluna `projeto_id` aos CSVs de qualidade da agua, dados ambientais e consumo/distribuicao.

Vantagens:

* Rastreabilidade por linha fica explicita.
* Modelo aproxima o formato relacional futuro.
* Facilita filtros quando houver multiplos projetos.

Desvantagens:

* Altera schema dos CSVs existentes.
* Exige migracao de cabecalho e dados historicos.
* Introduz acoplamento tecnico entre todas as telas de coleta e o Projeto.
* Aumenta superficie de teste em Analytics, Relatorios, Dashboard e qualquer leitor CSV.
* Antecipa uma necessidade que ainda nao existe, pois a GP-D01B permite apenas Projeto ativo unico.

Diagnostico:

Boa estrategia para uma fase multi-projeto futura, mas prematura para o estado atual.

### B) Manter os CSVs atuais e relacionar medicoes ao Projeto ativo por contexto

Descricao:

Manter os CSVs sem alteracao de schema. Enquanto existir apenas um Projeto ativo, as medicoes registradas no sistema pertencem conceitualmente ao Projeto ativo por contexto operacional.

Vantagens:

* Maxima simplicidade.
* Compatibilidade total com CSVs existentes.
* Nenhuma migracao de dados agora.
* Nenhuma alteracao em Analytics, Governanca, Recommendation ou Policy Engine.
* Preserva a GP-D01B como cadastro/contexto, sem transformar Projeto em dependencia transversal.
* Facilita migracao futura porque a regra atual e simples: o dataset vigente pertence ao Projeto ativo unico.

Desvantagens:

* Rastreabilidade por linha nao fica materializada no CSV.
* Se o sistema passar a permitir multiplos projetos, a estrategia deixa de ser suficiente.
* Se o Projeto ativo for trocado historicamente sem migracao, pode haver ambiguidade sobre medicoes antigas.

Diagnostico:

E a estrategia mais aderente ao estado atual, desde que acompanhada de um guardrail: enquanto houver apenas Projeto ativo unico, nao existe mistura de projetos no mesmo dataset.

### C) Criar um indice externo JSON relacionando Projeto e medicoes

Descricao:

Criar um arquivo JSON separado para mapear Projeto e medicoes, por exemplo usando timestamp, posicao da linha ou algum identificador derivado.

Vantagens:

* Preserva schema dos CSVs.
* Permite alguma rastreabilidade sem alterar linhas.
* Pode ser removido em migracao futura.

Desvantagens:

* Cria uma segunda fonte de verdade.
* Exige garantir sincronizacao entre CSV e indice.
* Timestamp ou numero de linha nao sao identificadores robustos.
* Aumenta complexidade sem resolver plenamente multi-projeto.
* Pode criar uma camada informal de persistencia paralela.

Diagnostico:

Nao recomendada. Entrega rastreabilidade intermediaria, mas com alto risco de divergencia e acoplamento operacional.

### D) Manifesto de dataset por Projeto ativo

Descricao:

Registrar, no proprio contexto do Projeto ativo ou em metadado documental, que os CSVs operacionais atuais pertencem ao Projeto ativo enquanto o sistema operar em modo de Projeto unico.

Vantagens:

* Preserva os CSVs.
* Mais explicito que uma inferencia puramente verbal.
* Nao altera linhas de medicao.
* Evita indice por linha.

Desvantagens:

* Continua sem rastreabilidade por linha.
* Pode virar um indice externo se evoluir alem de metadado simples.
* Nao resolve multi-projeto.

Diagnostico:

Tecnica aceitavel como complemento documental da alternativa B, mas nao deve virar artefato paralelo de mapeamento nesta fase.

## Matriz Comparativa

| Criterio | A: `projeto_id` nos CSVs | B: contexto do Projeto ativo | C: indice JSON externo | D: manifesto de dataset |
| -------- | ------------------------ | ---------------------------- | ---------------------- | ----------------------- |
| Simplicidade | Media | Alta | Baixa | Alta |
| Compatibilidade com CSVs existentes | Media/Baixa | Alta | Alta | Alta |
| Facilidade de migracao futura | Alta para relacional, media agora | Alta enquanto Projeto unico | Media/Baixa | Media |
| Rastreabilidade | Alta por linha | Media por contexto | Media, com risco de divergencia | Media por dataset |
| Impacto na arquitetura | Medio | Baixo | Medio/Alto | Baixo |
| Compatibilidade com PA-01 | Alta | Alta | Alta | Alta |
| Compatibilidade SQLite/PostgreSQL | Alta | Alta com migracao futura | Media | Media/Alta |
| Risco de acoplamento | Medio | Baixo | Alto | Baixo/Medio |
| Adequacao ao estado atual | Media | Alta | Baixa | Media/Alta |

## Riscos

| Risco | Estrategia afetada | Probabilidade | Impacto | Mitigacao |
| ----- | ------------------ | ------------- | ------- | --------- |
| Alterar CSVs cedo demais | A | Media | Medio | Adiar ate haver multi-projeto ou migracao de persistencia. |
| Ambiguidade historica se houver troca de Projeto ativo | B/D | Media futura | Medio | Bloquear multi-projeto nesta fase; abrir nova GP antes de permitir troca historica relevante. |
| Divergencia entre CSV e indice externo | C | Alta | Alto | Nao adotar indice externo. |
| Projeto virar dependencia transversal nas camadas | A/C | Media | Medio/Alto | Manter Projeto como contexto operacional, nao camada. |
| Migração relacional futura exigir backfill | B/D | Media | Baixo/Medio | Usar regra simples: registros legados pertencem ao Projeto ativo unico ate a data de migracao. |

## Relacao Com PA-01

Nenhuma alternativa deve selecionar politica, executar avaliacao observacional ou alterar resultado de medicao.

PA-01 permanece preservado se:

* Projeto continuar sendo contexto operacional;
* `PolicyEngine` continuar selecionando politicas;
* `AvaliacaoObservacionalService` continuar executando avaliacoes;
* Analytics, Governanca e Recommendation continuarem consumindo sinais sem recalcular autoridade observacional.

A alternativa B tem o menor risco de interferir no PA-01 porque nao cria novo campo transversal usado pelas camadas analiticas ou observacionais.

## Compatibilidade Com SQLite/PostgreSQL

Em uma migracao futura para SQLite/PostgreSQL, a relacao Medicao -> Projeto deve ser materializada como chave estrangeira ou campo equivalente.

A alternativa B nao bloqueia essa evolucao. Pelo contrario, preserva uma regra de migracao simples:

* enquanto o sistema tiver Projeto ativo unico, todos os registros CSV existentes pertencem ao Projeto ativo;
* na migracao relacional, o processo de importacao pode preencher `projeto_id` com o identificador do Projeto ativo unico;
* apenas quando houver multiplos projetos, a persistencia por medicao deve ser implementada explicitamente.

## Recomendacao

Recomenda-se a alternativa B:

Manter os CSVs atuais e relacionar as medicoes ao Projeto ativo por contexto, sem alterar schema nesta fase.

Complemento recomendado:

* registrar documentalmente que, no modo GP-D01B, o dataset operacional pertence ao Projeto ativo unico;
* nao criar coluna `projeto_id` agora;
* nao criar indice JSON externo agora;
* abrir GP-D01C-B ou equivalente apenas quando houver necessidade de implementacao;
* reavaliar a estrategia quando surgir qualquer um destes gatilhos:
  * multiplos projetos;
  * troca historica de Projeto ativo;
  * importacao/exportacao por Projeto;
  * multiusuario;
  * migracao para SQLite/PostgreSQL;
  * exigencia formal de rastreabilidade por linha.

## Veredito

Estrategia recomendada:

B) Manter os CSVs atuais e relacionar as medicoes ao Projeto ativo por contexto.

Justificativa:

* Maximiza simplicidade.
* Minimiza acoplamento.
* Preserva integralmente os CSVs existentes.
* Nao cria nova camada.
* Nao altera PA-01.
* Nao cria dependencia transversal em Analytics, Governanca ou Recommendation.
* Mantem caminho claro para migracao futura: preencher `projeto_id` apenas no momento em que persistencia por medicao for realmente necessaria.

## Encerramento

Nenhum codigo funcional foi alterado.

Nenhum CSV foi alterado.

Nenhum runtime foi alterado.

Nenhuma interface foi alterada.

Nenhuma camada nova foi criada.

`PolicyEngine`, Analytics, Governanca e Recommendation nao foram alterados.

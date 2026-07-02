# GP-D06A - Auditoria Das Evidencias Do Projeto

## Objetivo

Auditar, exclusivamente em nivel de dominio, o conceito de Evidencia do Projeto de Monitoramento.

A auditoria determina quais evidencias pertencem ao dominio do Projeto, quais possuem natureza exclusivamente operacional e quais devem permanecer como memoria documental permanente.

## Escopo

Foram avaliados:

* definicao conceitual de Evidencia do Projeto;
* diferenca entre evidencia, documento operacional, anexo e registro tecnico;
* tipos possiveis de evidencia, como fotografias, laudos, certificados, mapas, documentos, arquivos laboratoriais e pareceres;
* evidencias obrigatorias;
* evidencias opcionais;
* relacao entre evidencias e ciclo de vida do Projeto;
* relacao entre evidencias e Encerramento;
* relacao entre evidencias e Arquivamento;
* relacao entre evidencias e Dossie Final;
* evidencias com carater permanente;
* evidencias que nao devem integrar o Dossie Final.

Esta GP nao implementa codigo, nao altera persistencia, nao altera interface, nao altera o Dossie Final e nao cria nova camada arquitetural.

## Estado Atual Do Dominio

O dominio do Projeto possui identificacao, cliente, contexto operacional, perfil operacional, persistencia, estados, ciclo de vida, encerramento, arquivamento, Dossie Final, conteudo permanente do Dossie Final, imutabilidade substantiva do Dossie Final e responsabilidades institucionais auditadas.

Nao existe, no modelo atual, entidade `Evidencia`, colecao de evidencias, anexos formais, registro documental externo ou mecanismo de armazenamento de arquivos associado ao Projeto.

As auditorias anteriores ja reconheceram que Analytics, Governanca, Recommendation e Motor Observacional produzem sinais ou evidencias consolidadas, mas esses sinais nao foram promovidos a um conceito proprio do Projeto. O Dossie Final preserva conteudos finais e consolidados, sem duplicar bases operacionais, logs ou arquivos brutos.

## Definicao Conceitual De Evidencia

Evidencia do Projeto e uma referencia verificavel que ajuda a sustentar a existencia, conducao, decisao, encerramento ou memoria permanente de um Projeto de Monitoramento.

Uma evidencia agrega valor ao Projeto quando:

* explica por que uma decisao de Projeto foi tomada;
* sustenta a compreensao futura do contexto monitorado;
* comprova condicao, evento, resultado ou responsabilidade relevante;
* pode ser consultada sem transformar o Projeto em repositorio operacional;
* preserva rastreabilidade sem duplicar dados granulares.

Evidencia nao e sinonimo de qualquer arquivo produzido durante a operacao. Tambem nao e substituto dos dados operacionais, das medicoes, dos logs ou das camadas analiticas.

## Distincoes Conceituais

Evidencia, documento operacional, anexo e registro tecnico possuem naturezas diferentes.

| Conceito | Definicao | Pertence ao dominio do Projeto? | Observacao |
| --- | --- | --- | --- |
| Evidencia do Projeto | Referencia verificavel com valor para compreender ou sustentar o Projeto | Sim, quando permanente ou relevante | Deve ser resumida ou referenciada, nao duplicada indiscriminadamente. |
| Documento operacional | Documento usado na rotina de execucao | Nao necessariamente | Pode permanecer na operacao diaria se nao possuir valor permanente. |
| Anexo | Arquivo associado a um Projeto ou documento | Nao agora | Exige gestao documental ainda nao aprovada. |
| Registro tecnico | Dado produzido por sistema, motor, sensor, laboratorio ou calculo | Normalmente nao | Pode originar evidencia consolidada, mas nao deve ser incorporado bruto ao Dossie. |

## Analise Arquitetural

A Evidencia do Projeto nao deve ser tratada como atributo simples do Projeto no estado atual, porque evidencias podem ser multiplas, possuir tipos diferentes, origem, data, relevancia, responsavel e referencia externa.

Tambem nao deve ser implementada agora como entidade propria, pois nao ha necessidade operacional objetiva de cadastro, armazenamento, anexos, versionamento, validacao ou workflow documental.

Tratamento recomendado por alternativa:

* Atributo do Projeto: nao recomendado, pois reduziria evidencias complexas a campos soltos e pouco auditaveis.
* Entidade propria: nao recomendada agora, por ampliar escopo sem necessidade objetiva.
* Colecao pertencente ao Projeto: candidata futura, se houver necessidade de registrar multiplas evidencias formais associadas ao ciclo de vida.
* Referencia documental: abordagem recomendada para o estado atual e para evolucao imediata. O Projeto e o Dossie podem referenciar evidencias permanentes sem assumir gestao de arquivos.
* Conceito operacional: adequado para evidencias de rotina, logs, documentos temporarios e registros tecnicos granulares.

Assim, a decisao tecnica desta GP e reconhecer Evidencia como conceito de dominio auditado, mas nao materializado. Em evolucao futura, a forma preferencial sera uma colecao pertencente ao Projeto ou referencias documentais, desde que haja necessidade objetiva.

## Matriz De Inclusao

| Evidencia candidata | Classificacao | Incluir no dominio? | Preservar no Dossie? | Justificativa |
| --- | --- | --- | --- | --- |
| Laudo final consolidado | Permanente | Sim, como referencia futura | Sim, se existir | Sustenta a conclusao final sem duplicar dados laboratoriais brutos. |
| Certificado ou declaracao formal | Permanente | Sim, como referencia futura | Sim, se existir | Comprova condicao institucional relevante ao Projeto. |
| Parecer tecnico conclusivo | Permanente | Sim, como referencia futura | Sim, se existir | Ajuda a compreender decisao, encerramento ou recomendacao final. |
| Mapa ou croqui do ponto principal | Permanente contextual | Sim, como referencia futura | Sim, se relevante | Explica localizacao e contexto de coleta anos depois. |
| Fotografias representativas | Opcional permanente | Sim, se selecionadas | Sim, apenas referencia ou resumo | Podem comprovar contexto, evento ou condicao relevante, mas nao devem virar galeria operacional. |
| Registro de evento critico relevante | Permanente consolidada | Sim, como sintese | Sim, consolidado | Ja se alinha a eventos relevantes do Dossie Final. |
| Resultado analitico final | Permanente consolidada | Sim, como sinal consumido | Sim, consolidado | Agrega valor quando representa conclusao ou tendencia final. |
| Recomendacao emitida | Permanente consolidada | Sim, como sinal consumido | Sim, consolidada | Preserva orientacao relevante sem duplicar workflow interno. |
| Termo ou ato de encerramento | Permanente futura | Sim, se formalizado | Sim | Sustenta a conclusao operacional do Projeto. |
| Referencia de custodia de arquivamento | Permanente futura | Sim, se formalizada | Sim, se existir | Ajuda a preservar rastreabilidade apos arquivamento. |

## Matriz De Exclusao

| Evidencia candidata | Excluir do dominio permanente? | Excluir do Dossie? | Justificativa |
| --- | --- | --- | --- |
| Medicoes individuais | Sim | Sim | Sao dados operacionais granulares e ja foram excluidas do Dossie na GP-D04C. |
| Logs de sistema | Sim | Sim | Evidenciam runtime, nao memoria de Projeto. |
| Arquivos temporarios | Sim | Sim | Nao possuem valor permanente e podem gerar divergencia. |
| Fotografias repetitivas ou sem relevancia | Sim | Sim | Aumentam volume sem melhorar entendimento futuro. |
| Arquivos laboratoriais brutos | Sim | Sim | Devem permanecer na fonte operacional; o Projeto pode referenciar laudo consolidado. |
| Dados pessoais nao essenciais | Sim | Sim | Elevam risco e nao agregam valor ao Projeto. |
| Rascunhos de documentos | Sim | Sim | Representam preparacao, nao memoria permanente. |
| Anexos obrigatorios indiscriminados | Sim | Sim | Exigem gestao documental ainda nao aprovada. |
| Estados intermediarios de processamento | Sim | Sim | Pertencem a execucao tecnica, nao ao fechamento documental. |
| Evidencias de baixa relevancia | Sim | Sim | Devem permanecer na operacao diaria, se necessario. |

## Evidencias Permanentes

Evidencias permanentes sao aquelas que ajudam a compreender o Projeto depois de encerrado ou arquivado.

Podem incluir, quando existirem e forem relevantes:

* laudo final consolidado;
* certificado ou declaracao formal;
* parecer tecnico conclusivo;
* mapa ou croqui do ponto principal de coleta;
* fotografias representativas selecionadas;
* eventos criticos relevantes;
* resultado analitico final consolidado;
* recomendacoes emitidas;
* termo ou ato de encerramento;
* referencia de custodia de arquivamento.

Essas evidencias devem ser preservadas como sintese, referencia documental ou metadado minimo. A preservacao nao deve duplicar arquivos brutos nem transformar o Projeto em repositorio documental amplo.

## Evidencias Operacionais

Evidencias operacionais apoiam a execucao diaria, mas nao possuem, por si so, valor permanente para o Projeto.

Incluem:

* medicoes individuais;
* logs;
* arquivos temporarios;
* registros de processamento;
* comprovantes de tarefas rotineiras;
* fotos repetitivas;
* arquivos laboratoriais brutos;
* anotacoes operacionais sem impacto;
* estados intermediarios;
* documentos em rascunho.

Essas evidencias podem permanecer em fontes operacionais ou trilhas especificas, mas nao devem compor o Projeto como memoria permanente nem o Dossie Final como conteudo final.

## Relacao Com Encerramento

O encerramento do Projeto pode ser fortalecido por evidencias permanentes, mas nao deve depender de uma colecao de evidencias implementada nesta fase.

Evidencias adequadas ao encerramento sao aquelas que sustentam a decisao de concluir o ciclo operacional, como periodo monitorado, eventos relevantes, laudo final, recomendacoes finais, parecer tecnico ou termo de encerramento quando existirem.

Evidencias nao devem criar aprovacao de encerramento por conta propria. Aprovacao, assinatura e workflow permanecem fora do escopo atual.

## Relacao Com Arquivamento

O arquivamento deve preservar a consultabilidade do Projeto e de suas referencias permanentes. Evidencias relevantes devem permanecer localizaveis ou referenciadas, mas o arquivamento nao deve transformar o Projeto em sistema de gestao de arquivos.

Se uma evidencia for permanente, o arquivamento deve preservar sua referencia ou sintese. Se for operacional, deve permanecer fora da memoria documental do Projeto.

## Relacao Com O Dossie Final

O Dossie Final deve preservar evidencias permanentes de forma seletiva e consolidada.

Pertencem ao Dossie:

* referencias a laudos ou pareceres finais;
* eventos relevantes consolidados;
* recomendacoes emitidas;
* resultados finais consolidados;
* fotografias ou mapas apenas quando forem representativos;
* referencias documentais que expliquem encerramento ou arquivamento.

Nao pertencem ao Dossie:

* medicoes individuais;
* logs;
* arquivos brutos;
* anexos obrigatorios indiscriminados;
* rascunhos;
* estados intermediarios;
* evidencias repetitivas;
* documentos sem impacto sobre o Projeto.

O Dossie continua sendo memoria final do Projeto, nao um repositorio integral de evidencias.

## Impacto Arquitetural

Nao ha necessidade de nova camada arquitetural.

A auditoria reforca que evidencias devem ser tratadas por enriquecimento disciplinado do dominio de Projeto e por referencias documentais quando houver necessidade objetiva. Policy Engine, Motor Observacional, Analytics, Governanca, Recommendation e Dashboard permanecem com suas responsabilidades atuais.

Nenhum componente tecnico passa a decidir o que e evidencia permanente do Projeto. Essa classificacao pertence ao dominio documental do Projeto e deve ser auditada antes de qualquer materializacao.

## Impacto No Dominio

O impacto de dominio e conceitual.

Evidencia do Projeto passa a estar delimitada como conceito auditado, mas nao implementado. O dominio atual permanece valido: conteudos finais e consolidados ja podem funcionar como memoria documental sem exigir cadastro de anexos ou repositorio de arquivos.

Em evolucao futura, evidencias poderao enriquecer o Projeto por referencias documentais ou colecao pertencente ao Projeto, desde que haja necessidade operacional clara.

## Analise Do PA-01

PA-01 permanece integralmente preservado.

Esta GP nao altera o fluxo operacional, nao altera motores, nao altera politicas, nao altera Analytics, nao altera Governanca, nao altera Recommendation, nao altera Dashboard e nao muda o Dossie Final.

A separacao entre evidencia permanente e evidencia operacional evita duplicacao de dados, preserva a autoridade das camadas existentes e impede que o Projeto assuma funcoes de repositorio tecnico.

## Analise Das Discoveries

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Resultado:

* PA-02 foi reforcada: evidencias podem agregar valor ao Projeto por enriquecimento do dominio existente, sem criacao de nova camada.
* PA-03 foi reforcada: a auditoria recomenda reconhecer o conceito antes de materializar entidade, colecao, persistencia ou anexos.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida.
* Nenhuma nova Discovery candidata foi identificada.

## Conclusao

Evidencia do Projeto e um conceito relevante, mas ainda imaturo para implementacao. O estado atual suporta evidencias como sinais consolidados, eventos relevantes e referencias documentais dentro da memoria final, mas nao justifica entidade propria, anexos formais ou repositorio documental.

A evolucao recomendada e manter evidencias operacionais em suas fontes de origem, preservar no Dossie apenas evidencias permanentes e, se necessario em GP futura, auditar uma colecao pertencente ao Projeto com referencias documentais minimas.

## Veredito Final

Modelo de evidencias suportado com ressalvas.

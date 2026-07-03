# OP-00 - Auditoria De Delimitacao Do Escopo Operacional

## Objetivo

Definir, exclusivamente em nivel documental, a fronteira operacional do PROTEUS antes da modelagem de fluxos operacionais.

A auditoria estabelece quais atividades pertencem ao escopo do PROTEUS, quais pertencem a processos externos e quais informacoes o sistema deve apenas receber, referenciar ou produzir.

Esta atividade nao implementa codigo, nao altera arquitetura, nao altera dominio, nao altera persistencia, nao altera interface e nao promove Discoveries.

## Escopo

O escopo desta auditoria inclui:

* delimitar a responsabilidade operacional do PROTEUS;
* classificar atividades relacionadas a monitoramento hidrico;
* distinguir operacao propria do sistema de atividades humanas, laboratoriais, logisticas ou de campo;
* definir criterios objetivos para futuras decisoes de inclusao funcional;
* preservar o Dominio Projeto consolidado e PA-01.

Ficam fora do escopo:

* modelar fluxo operacional detalhado;
* criar entidades, colecoes, camadas ou persistencias;
* alterar o Dossie Final;
* absorver processos logisticos, laboratoriais, administrativos ou de seguranca;
* promover PA-02, PA-03 ou qualquer Discovery candidata.

## Estado Atual Do CASE

O CASE-01 - PROTEUS possui uma base operacional e analitica ja existente e um Dominio Projeto estruturalmente saturado.

A GP-D09A concluiu que o agregado Projeto esta estruturalmente completo, sem necessidade objetiva de expansao arquitetural.

A GP-D10A concluiu que diferentes contextos, pontos e ambientes monitorados podem reutilizar o mesmo Dominio Projeto como instancias, sem exigir dominio proprio.

Com isso, a nova fase do CASE-01 passa a exigir uma delimitacao operacional: antes de modelar fluxos, e necessario definir o que o PROTEUS efetivamente faz e o que permanece responsabilidade de processos externos.

## Definicao Da Fronteira Operacional

A responsabilidade operacional do PROTEUS comeca quando existe necessidade de registrar, organizar, avaliar, correlacionar, apresentar ou preservar informacoes de monitoramento hidrico dentro do sistema.

A responsabilidade operacional do PROTEUS termina antes da execucao fisica, logistica, administrativa, laboratorial ou institucional externa que produz ou suporta essas informacoes.

Em termos objetivos:

* PROTEUS recebe contexto, dados, referencias e resultados provenientes de processos externos.
* PROTEUS registra projetos, pontos, medicoes e eventos operacionais reconhecidos pelo sistema.
* PROTEUS avalia dados por regras, politicas, indicadores, alertas, dashboards e relatorios.
* PROTEUS produz memoria operacional e documental, inclusive Dossie Final quando aplicavel.
* PROTEUS nao executa coleta fisica, transporte, logistica, gestao de frota, gestao de equipe, analise laboratorial, calibracao, cadeia de custodia fisica ou certificacao externa.

## Matriz De Responsabilidades

| Responsavel | Responsabilidades Dentro Do Contexto OP-00 | Relacao Com PROTEUS |
| --- | --- | --- |
| PROTEUS | Registrar projetos, pontos, medicoes, indicadores, alertas, dashboards, relatorios, evidencias referenciais e Dossie Final. | Responsabilidade interna do sistema. |
| Usuario humano | Definir intencao do projeto, aprovar parametros, interpretar resultados, validar contexto e decidir acoes externas. | Atua como autoridade decisoria e fonte de validacao. |
| Equipe de campo | Executar coleta fisica, medicoes in loco, transporte, observacoes de campo, uso de equipamentos e cumprimento do roteiro externo. | Fornece dados, referencias e ocorrencias ao PROTEUS. |
| Laboratorio | Executar analises, metodos, preservacao tecnica, controle analitico, laudos, certificados e incertezas. | Fornece resultados laboratoriais e evidencias externas ao PROTEUS. |
| Gestao logistica | Planejar campanhas, rotas, veiculos, agenda, materiais, recipientes e conservantes. | Pode fornecer planejamento ou registros de execucao como contexto, sem ser absorvida. |
| Governanca externa | Definir normas, licencas, responsabilidades legais, fiscalizacao e obrigacoes institucionais. | Pode gerar criterios e documentos externos referenciados pelo PROTEUS. |

## Matriz De Inclusao

| Atividade | Classificacao | Justificativa |
| --- | --- | --- |
| Cadastro de projetos | Pertence | O Dominio Projeto e parte consolidada do PROTEUS e organiza contexto, ciclo de vida e memoria permanente. |
| Cadastro de pontos de monitoramento | Pertence parcialmente | O ponto pode ser registrado como referencia operacional do monitoramento; inventario fisico completo, georreferenciamento de campo e manutencao patrimonial permanecem externos ou dependem de GP futura. |
| Registro de medicoes | Pertence | Medicoes sao insumo operacional central para avaliacao, indicadores, alertas e relatorios. |
| Indicadores | Pertence | Indicadores representam transformacao interna dos dados em leitura operacional ou analitica. |
| Alertas | Pertence | Alertas derivam de regras, politicas ou limites avaliados pelo sistema. |
| Dashboards | Pertence | Dashboards apresentam estado operacional e analitico produzido pelo PROTEUS. |
| Relatorios | Pertence | Relatorios consolidam resultados e memoria operacional do sistema. |
| Dossie Final | Pertence | O Dossie Final e memoria permanente do Projeto quando aplicavel ao ciclo de vida consolidado. |
| Controle de equipamentos | Pertence parcialmente | PROTEUS pode receber identificador, referencia de calibracao ou equipamento usado; inventario, manutencao, calibracao e disponibilidade fisica nao pertencem ao sistema neste escopo. |
| Controle de recipientes | Pertence parcialmente | PROTEUS pode receber referencia quando afetar validade ou rastreabilidade da amostra; estoque, distribuicao e custodia fisica permanecem externos. |
| Controle de conservantes | Pertence parcialmente | PROTEUS pode receber informacao de preservacao quando relevante ao dado; preparo, estoque, dosagem e controle tecnico pertencem ao campo ou laboratorio. |

## Matriz De Exclusao

| Atividade | Classificacao | Justificativa |
| --- | --- | --- |
| Planejamento logistico da campanha | Nao pertence | E atividade de organizacao externa; PROTEUS pode receber datas, escopo ou referencias, mas nao planeja a logistica. |
| Definicao de roteiros | Nao pertence | Roteirizacao e otimizacao de deslocamento pertencem a processo logistico externo; PROTEUS pode receber local, ponto, data ou registro de execucao. |
| Controle de veiculos | Nao pertence | Frota, disponibilidade, manutencao e alocacao sao gestao externa. |
| Agenda da equipe | Nao pertence | Escala, disponibilidade, jornada e alocacao humana pertencem a gestao operacional externa. |
| Coleta fisica de amostras | Nao pertence | A execucao fisica e responsabilidade da equipe de campo. |
| Transporte de amostras | Nao pertence | O deslocamento e a preservacao fisica pertencem a campo, logistica ou laboratorio. |
| Cadeia de custodia fisica | Nao pertence | Pode ser referenciada como evidencia externa, mas a custodia real e processo externo. |
| Analise laboratorial | Nao pertence | Metodos, ensaios, laudos e controle tecnico sao responsabilidade do laboratorio. |
| Calibracao e manutencao de equipamentos | Nao pertence | PROTEUS pode receber referencia, mas nao administra o processo tecnico de calibracao. |
| Compra e estoque de materiais | Nao pertence | Aquisicao e controle de suprimentos sao processos administrativos externos. |
| Acao corretiva em campo | Nao pertence | O sistema pode recomendar, alertar ou registrar, mas a execucao e responsabilidade humana externa. |

## Informacoes Que PROTEUS Deve Apenas Receber

PROTEUS deve receber, sem absorver a responsabilidade pelo processo que as produziu:

* resultados laboratoriais;
* metadados de coleta;
* referencias de equipamento usado;
* referencias de calibracao;
* informacoes de recipiente e conservante quando afetarem validade;
* datas planejadas ou executadas;
* identificacao de responsaveis;
* observacoes de campo;
* laudos, certificados ou evidencias externas;
* informacoes de rota apenas como contexto historico;
* restricoes externas relevantes ao projeto.

## Informacoes Que PROTEUS Deve Produzir

PROTEUS deve produzir:

* registros estruturados de projeto;
* registros de pontos ou referencias de monitoramento;
* registros de medicoes;
* avaliacoes observacionais;
* indicadores operacionais e analiticos;
* alertas;
* dashboards;
* relatorios;
* referencias permanentes de evidencias;
* registros institucionais ou documentais quando auditados;
* Dossie Final do Projeto quando aplicavel.

## Criterios Para Inclusao Futura De Funcionalidades

Uma funcionalidade futura so deve ser considerada pertencente ao PROTEUS quando atender cumulativamente aos criterios abaixo:

1. Produzir, organizar ou avaliar informacao diretamente usada pelo monitoramento hidrico.
2. Ter valor operacional, analitico, documental ou de governanca dentro do sistema.
3. Nao transferir para o PROTEUS responsabilidade fisica, laboratorial, administrativa ou logistica externa.
4. Preservar PA-01 e a autoridade das camadas existentes.
5. Demonstrar necessidade objetiva, nao apenas conveniencia de automacao.
6. Poder ser tratada por enriquecimento das estruturas existentes antes de propor nova camada.
7. Distinguir registro ou referencia de gestao completa do processo externo.
8. Ser auditada em documento proprio antes de qualquer implementacao.

## Riscos De Expansao Indevida Do Escopo

Os principais riscos identificados sao:

* transformar PROTEUS em sistema de gestao logistica;
* absorver controle de frota, equipe, estoque, equipamentos ou laboratorio;
* duplicar responsabilidades de sistemas externos especializados;
* confundir referencia documental com propriedade operacional;
* criar entidades ou colecoes para processos que o sistema deve apenas receber;
* ampliar o Dominio Projeto apos sua saturacao sem lacuna objetiva;
* enfraquecer PA-01 ao permitir que camadas assumam autoridade fora de sua competencia;
* criar dashboards ou relatorios sobre processos externos como se fossem processos internos.

## Impacto Arquitetural

Nao ha impacto arquitetural implementado.

A auditoria reforca que a proxima evolucao operacional deve ocorrer por delimitacao e uso responsavel das camadas existentes, sem criar nova camada, entidade, colecao, persistencia ou interface.

O impacto arquitetural e apenas documental: a fronteira OP-00 passa a funcionar como criterio de triagem para futuras GPs operacionais.

## Impacto Operacional

O impacto operacional e a separacao formal entre:

* operacao interna do PROTEUS: registrar, avaliar, alertar, apresentar, relatar e preservar;
* processos externos: planejar campanha, executar campo, controlar recursos fisicos, analisar em laboratorio e tomar acoes materiais.

Essa separacao reduz ambiguidade antes da modelagem de fluxos e evita que a operacao do PROTEUS seja confundida com toda a cadeia real de monitoramento hidrico.

## Analise PA-01

PA-01 permanece preservado.

A auditoria nao desloca autoridade observacional, analitica, de governanca ou executiva entre camadas. Tambem nao cria camada paralela para logistica, laboratorio ou campo.

O criterio adotado reforca PA-01 porque impede que o PROTEUS assuma responsabilidades externas sem auditoria e sem necessidade objetiva.

## Analise Das Discoveries

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Impacto registrado:

* PA-02 foi reforcada: a delimitacao operacional agrega valor ao CASE por orientar o uso das camadas existentes, sem criar nova camada arquitetural.
* PA-03 foi reforcada: atividades externas podem ser reconhecidas, recebidas ou referenciadas sem materializacao automatica em entidade, colecao ou persistencia.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida automaticamente.
* Nenhuma nova Discovery candidata foi identificada.

## Observacoes Da IA / Hipoteses Metodologicas

As observacoes abaixo nao alteram o escopo da OP-00, nao modificam o ICFACTORY, nao alteram PA-01, PA-02 ou PA-03 e nao sao promovidas automaticamente.

| Padrao observado | Evidencia usada | Possivel impacto | Recomendacao | Status sugerido |
| --- | --- | --- | --- | --- |
| A fase pos-saturacao desloca a pergunta de "o que o dominio e" para "o que a operacao do sistema assume". | GP-D09A concluiu saturacao estrutural e GP-D10A validou multiplas instancias sem novo dominio. | Ajuda a evitar expansao estrutural ao iniciar fase operacional. | Manter como criterio de leitura em auditorias operacionais futuras. | Hipotese em monitoramento |
| Informacoes externas podem ser recebidas sem que o processo externo seja absorvido. | Equipamentos, recipientes, conservantes, roteiros e laboratorio aparecem como referencias uteis, mas nao como responsabilidades internas. | Reduz risco de transformar PROTEUS em sistema logistico ou laboratorial. | Usar a distincao "receber/referenciar versus gerir" nas proximas GPs. | Observacao simples |
| Inclusao parcial e um mecanismo importante de controle de escopo. | Varias atividades possuem dados relevantes ao PROTEUS, mas execucao e controle externo. | Evita classificacoes binarias precipitadas e preserva fronteira operacional. | Registrar justificativa explicita sempre que uma atividade for parcialmente incluida. | Observacao simples |

Nenhuma observacao acima e Discovery oficial. Nenhuma nova Discovery candidata foi criada nesta auditoria.

## Respostas As Questoes Obrigatorias

1. A responsabilidade operacional do PROTEUS comeca no registro, organizacao, avaliacao, apresentacao e preservacao de informacoes de monitoramento hidrico.
2. A responsabilidade operacional do PROTEUS termina antes da execucao fisica, logistica, administrativa, laboratorial ou institucional externa.
3. Pertencem claramente ao PROTEUS: cadastro de projetos, registro de medicoes, indicadores, alertas, dashboards, relatorios e Dossie Final.
4. Sao externas: planejamento logistico, roteiros, veiculos, agenda de equipe, coleta fisica, transporte, laboratorio, calibracao, manutencao e estoque.
5. PROTEUS deve apenas receber resultados, metadados, referencias de equipamentos, informacoes de preservacao, responsaveis, datas, laudos e observacoes externas.
6. PROTEUS deve produzir registros, avaliacoes, indicadores, alertas, dashboards, relatorios, referencias de evidencias e Dossie Final.
7. Responsabilidades humanas incluem definicao de intencao, validacao de contexto, decisao operacional, aprovacao e execucao de acoes externas.
8. Responsabilidades do laboratorio incluem analises, metodos, laudos, preservacao tecnica, incerteza, certificados e controle analitico.
9. Responsabilidades da equipe de campo incluem coleta, medicoes in loco, transporte, uso de equipamentos, observacoes e execucao de roteiro externo.
10. Atividades relacionadas a monitoramento hidrico que PROTEUS nao deve absorver incluem logistica de campanha, frota, agenda, estoque, laboratorio, calibracao e cadeia de custodia fisica.
11. O risco de expansao indevida e transformar o PROTEUS em sistema logistico, laboratorial, administrativo ou de gestao de recursos fisicos.
12. Os criterios objetivos para inclusao futura sao necessidade operacional comprovada, valor interno ao sistema, preservacao de PA-01, nao absorcao de responsabilidade externa, preferencia por enriquecimento de estruturas existentes e auditoria previa.

## Declaracao ICFACTORY / IA

* A execucao permaneceu sob governanca ICFACTORY.
* Nenhuma decisao operacional foi implementada por extrapolacao da IA.
* Houve observacoes metodologicas registradas fora do escopo principal, em secao separada.
* O Codex atuou como executor da OP-00 e tambem identificou hipoteses/sugestoes externas ao escopo principal, deixando claro que elas nao integram oficialmente o ICFACTORY sem auditoria e validacao humana.
* Nenhum ponto exige validacao humana antes de aceitar o veredito documental da OP-00.
* Qualquer inclusao operacional futura exige GP propria antes de implementacao.

## Veredito Final

O PROTEUS deve reconhecer como escopo operacional interno apenas as atividades de registro, avaliacao, apresentacao, alerta, relatorio e preservacao documental de informacoes de monitoramento hidrico.

Atividades logisticas, laboratoriais, administrativas, fisicas e de gestao de recursos permanecem externas. O sistema pode receber ou referenciar informacoes desses processos, mas nao deve absorver sua responsabilidade operacional.

Nao ha necessidade objetiva de alterar arquitetura, dominio, persistencia, interface, Dossie Final, entidades, colecoes ou camadas nesta OP-00.


# GP-RG-06 - Pre-Registro Do Primeiro Piloto Controlado

## 1. Identidade, Autoridade E Momento

| Campo | Registro pre-registrado |
|---|---|
| Experimento | GP-RG-06 / CP-01 |
| Versao | 1.0, congelada antes das Reconstrucoes A e B |
| Data | 18/07/2026 |
| Autoridade experimental | pesquisadores responsaveis pelo ICFACTORY, conforme OEG-RG-06 |
| Executor/coordenador/documentador/auditor | Harness Governado (Codex) |
| Sistema/modelo | Codex; identificador exato de modelo e configuracao: DESCONHECIDO/NAO OBSERVAVEL no pacote documental |
| Caso | CP-01 - decisao editorial da pos-producao visual do video institucional PROTEUS |
| Fases | A - reconstrucao retrospectiva; C - duas reconstrucoes documentais, sem independencia de agente demonstrada |
| Natureza | exploratoria, descritiva, um caso interno |

O pre-registro sucede a decisao DS-01 em `RG_06_CASE_SELECTION.md` e antecede a criacao de qualquer registro de reconstrucao GP-RG-06.

## 2. Objetivo E Questoes

Objetivo: testar, no CP-01 e somente no pacote congelado, se os seis tipos P/E/I/F/D/V podem ser diferenciados, se as quatro decisoes podem ser percorridas ate suas origens e validacoes, se regras/invariantes detectam lacunas, se um terceiro documental pode auditar a cadeia e se duas reconstrucoes produzem resultados convergentes.

Questoes autorizadas: QE-01, QE-02, QE-03, QE-04 e QE-06. OV executados: OV-01, OV-02, OV-04, OV-05 e OV-06. OV-03, OV-07 e OV-08 ficam expressamente fora.

## 3. Hipoteses Participantes

| Hipotese | Parcela testada | Condicao favoravel pre-registrada | Resultado capaz de contrariar |
|---|---|---|---|
| H-RG-001 | rastreabilidade, auditabilidade e reproducao documental no caso | caminhos D<-F<-E e D->V reconstruiveis, fontes/limites auditaveis e convergencia sem divergencia material | decisao sem caminho; dependencia de informacao externa; divergencia material |
| H-RG-002 | separacao E/I facilita reconstrucao declarada | E e I distinguiveis nas duas reconstrucoes, sem confusao material | confusao persistente, separacao impossivel ou nenhuma utilidade observavel |
| H-RG-003 | tentativa rejeitada preservada torna revisao auditavel | P-007, rejeicao, P-008, motivo e efeito em D-004 reconstruiveis | predecessor/motivo/sucessor nao recuperaveis ou historico induz erro material |
| H-RG-004 | reproducao independente | somente verificacao documental parcial; independencia real nao esta disponivel | divergencia material entre reconstrucoes ou dependencia de conhecimento tacito; ausencia de independencia impede apoio confirmatorio |
| H-RG-007 | consistencia entre agentes | NAO_TESTADO como hipotese entre agentes; ha um unico executor observavel | nao ha dois tipos/agentes independentes; qualquer aparente acordo nao conta como apoio |
| H-RG-010 | snapshots/sucessao aumentam recuperabilidade | parcela de recuperabilidade da revisao P-007 -> P-008 | ordem ou estado anterior irrecuperavel, inconsistencias temporais materiais |

H-RG-005, H-RG-006, H-RG-008, H-RG-009 e H-RG-011 nao participam. Nenhum estado posterior podera promover hipotese geral.

## 4. Unidade, Perfil E Escopo

Unidade principal: uma cadeia de decisao versionada do CP-01, composta por quatro decisoes D-001 a D-004 e uma revisao REV-001. Unidades secundarias: registros P, E, I, F, D e V; relacoes; caminhos por decisao; revisao; classificacoes de cada reconstrucao.

Perfil pre-declarado: PCP, porque o caso de pesquisa usa os seis tipos e inclui alternativas, confianca, riscos, limitacoes e revisao. A conformidade sera avaliada contra RI-01 a RI-18 e INV-01 a INV-31, registrando `NAO_APLICAVEL` quando justificado.

Informacao externa: proibida para completar a cadeia. Sao permitidos somente os documentos congelados abaixo e os instrumentos GDC-R congelados. O sistema de arquivos pode ser consultado apenas para verificar existencia, tamanho e hash desses arquivos. Memoria do executor nao e evidencia.

## 5. Pacote De Caso Congelado

| Documento | Bytes | SHA-256 |
|---|---:|---|
| `docs/research/PI_07A_DECISION_FOUNDATION_GOVERNANCE_REPORT.md` | 13697 | `FC747BBB412144384FCBA049267ED0EB23805AD00E836A69530134A1E3B1B389` |
| `docs/presentation/PI_07_KDENLIVE_PRE_POSTPRODUCTION_AUDIT.md` | 10828 | `E9B5C4248B236570DF3D238FAD70A3973A9AC57627D1A53049118A89490C9616` |
| `docs/presentation/PI_07_POST_PRODUCTION_EXECUTION_REPORT.md` | 5097 | `172A6923CC083162AE6A80A6AE50DF240FB9C33C31396D16F6E3C2613613E417` |

As midias, scripts e projetos citados nos documentos nao integram o pacote de leitura e nao serao abertos ou alterados. Seus resultados sao tratados como alegacoes documentais com a proveniencia declarada nos tres arquivos.

## 6. Instrumentos Congelados

| Instrumento | SHA-256 |
|---|---|
| `RG_02_CONCEPTUAL_MODEL.md` | `581B3A0A3064D7ED9A8922F7441131575CB8C32C1FFF22BA062AF8B8C1B294D2` |
| `RG_02_SEMANTIC_MATRIX.md` | `C1E4325650FF321E4C6427C542EA2BA982D4A3713E4E99DCB732E90118F97E05` |
| `RG_03_ARCHITECTURE.md` | `7E7E397A60C14979BE643703624483B3E1066DB31E1D5B291F92F238442337DD` |
| `RG_03_INVARIANTS.md` | `4A37CFB121A03B1637EB41A49F252125E64F4FDA08A643213DB36DEBF06A7521` |
| `RG_05_CASE_SELECTION_FRAMEWORK.md` | `53F9725D4CF57150C6C9FF6D28C70E8BB522CBC51C6FC1F458B694E2F172EC38` |
| `RG_05_EXPERIMENTAL_PROTOCOL.md` | `427928197198F40F6C92B74E65BAAF239F933FB08004526981B8A59F11B3F42C` |
| `RG_05_HYPOTHESIS_OPERATIONALIZATION.md` | `E58FBBC38286F9EB0D2F1AE0BFC8EF65F3D61A51B9C2BED9908196523D668021` |
| `RG_05_METRICS_AND_INTERPRETATION.md` | `705F4F9CBC1F6472F88D55ED4E5A72F19A0E9B9B3E96432E0E8C09AC66FB51E9` |
| `RG_05_THREATS_TO_VALIDITY.md` | `41BC4285F28E51841135AD9338FADDE95A9FBC50D127C8F3E83FA1B626AA9CA2` |

## 7. Procedimento Preexistente Aplicado

Nenhum procedimento novo e criado. Sera aplicada a sequencia da fase A/C de `RG_05_EXPERIMENTAL_PROTOCOL.md`, o teste de classificacao da secao 7 de `RG_02_SEMANTIC_MATRIX.md`, os testes estruturais da secao 13.2 de `RG_03_ARCHITECTURE.md` e o procedimento de 14 passos da secao 12 de `RG_03_INVARIANTS.md`.

Ordem:

1. verificar hashes e registrar gates GX-00 a GX-07;
2. Reconstrucao A: percorrer cada decisao no sentido D<-F<-E/I/P e depois D->V, preservando os IDs de origem;
3. congelar o registro A antes da Reconstrucao B;
4. Reconstrucao B: classificar os registros do pacote pela ordem do teste semantico e depois resolver os vinculos, sem editar A;
5. inventariar P/E/I/F/D/V, revisoes, estados, transicoes, limitacoes e relacoes;
6. aplicar RI, AP e INV somente ao registro observavel;
7. comparar A e B, sem resolver divergencia silenciosamente;
8. congelar dados/resultados antes da interpretacao de hipoteses;
9. aplicar os estados permitidos e concluir auditoria/custodia.

As duas reconstrucoes sao passagens separadas do mesmo executor, nao avaliadores independentes. Comunicacao entre passagens e contaminacao por memoria sao inevitaveis e serao tratadas como ameaca TV-17/TV-20, limitando OV-06.

## 8. Metricas E Denominadores

Todas sao descritivas; nao ha limiar calibrado nem inferencia estatistica neste primeiro piloto. Percentuais usam uma casa decimal; denominador zero gera `NAO_APLICAVEL`; ausencias usam os codigos RG-05.

| Prioridade | Metrica | Denominador/regra | Interpretacao pre-registrada |
|---|---|---|---|
| primaria | MC-01 | unidades comuns P/E/I/F/D/V entre A e B | acordo bruto; kappa nao calculado por falta de avaliadores independentes |
| primaria | MS-01 | D aplicaveis (4) | contar D com caminho documental D<-F<-E |
| primaria | MS-02 | I inventariadas | contar I ligadas a pelo menos uma E |
| primaria | MS-03 | E inventariadas | contar E com origem, metodo, alcance e limitacao; campo composto incompleto nao atende |
| primaria | MS-04 | cadeia | contagem AP-01 a AP-15 detectada, por tipo |
| primaria | MS-05 | cadeia | contagem INV-01 a INV-31 violada; `NAO_DETERMINADO` separado |
| primaria | MA-02 | unidades comuns codificadas | acordo bruto A/B; somente descritivo, incapaz de apoiar independencia |
| primaria | MA-03 | divergencias A/B | numero de divergencias que alteram tipo, caminho, conformidade ou interpretacao |
| primaria | MA-04 | itens/cadeia | numero de ambiguidades ou `NAO_DETERMINADO` |
| secundaria | MS-07 | nos aplicaveis | nos sem relacao obrigatoria observavel |
| secundaria | MA-01 | quatro tarefas D | sem referencia independente, registrar `NAO_COLETADO` e usar apenas completude interna, nao correcao |
| secundaria | MA-05 | tarefa | fontes necessarias alem do pacote; consulta proibida, pedido registrado |
| secundaria | MA-07 | elementos | proveniencias incorretas ou nao resolvidas |
| secundaria | MD-04 | uma revisao aplicavel | predecessor, motivo, sucessor e impacto reconstruiveis |
| secundaria | MT-01/MT-02 | estados/revisoes esperados | recuperacao descritiva e inconsistencias temporais |

Nao serao calculadas metricas de OV-03, OV-07 ou OV-08, custo/tempo, qualidade decisoria ou comparacao causal. MS-06 nao sera calculada como percentual porque o PCP nao define uma lista atomica fechada de requisitos; a classe de conformidade sera qualitativa e auditavel.

## 9. Criterios De Interpretacao

Estados permitidos: `NAO_TESTADO`, `TESTE_INCONCLUSIVO`, `PARCIALMENTE_APOIADO`, `APOIADO_NO_CONTEXTO_TESTADO`, `CONTRARIADO_NO_CONTEXTO_TESTADO`, `REQUER_REFINAMENTO`, `NAO_APLICAVEL_AO_CASO`, `EVIDENCIA_INSUFICIENTE`.

* OV-01 pode receber apoio contextual se A e B distinguirem os seis tipos sem divergencia material; qualquer ambiguidade sera reportada e podera produzir apoio parcial/refinamento.
* OV-02 pode receber apoio contextual apenas se a auditoria aplicar relacoes proibidas e invariantes de forma determinavel; violacao do caso nao e falha automatica do detector.
* OV-04 pode receber apoio contextual se as quatro D e REV-001 tiverem caminhos reconstruiveis dentro do pacote.
* OV-05 pode receber apoio contextual se fontes, metodos, alternativas, limites, mudancas e ausencias forem localizaveis por documento/secao.
* OV-06 sera no maximo `TESTE_INCONCLUSIVO` ou `EVIDENCIA_INSUFICIENTE` para reproducao independente, porque ha um executor; acordo A/B nao remove esse bloqueio.

Nenhuma diferenca minima de interesse foi calibrada. Uma divergencia material basta para impedir apoio integral da dimensao correspondente; divergencias nao materiais serao contadas e justificadas.

## 10. Ameacas, Limitacoes E Mitigacoes

| Ameaca | Presenca | Mitigacao/limite |
|---|---|---|
| TV-06 confirmacao | alta | condicoes contrarias e metricas congeladas; relatar falhas |
| TV-07 retrospectiva | alta | conclusao limitada a reconstrucao documental |
| TV-09 documentacao sobrevivente | alta | ausencias e custodia nao versionada registradas |
| TV-17 nao independencia | bloqueante para apoio de OV-06 | resultado inconclusivo; nao simular agente independente |
| TV-19 conhecimento previo | alta | declarar contaminacao; pacote congelado |
| TV-20 memoria entre rodadas | alta | preservar A antes de B; nao alegar independencia |
| TV-23 artefatos nao versionados em Git | alta | hashes atuais; historico Git `NAO_COLETADO/AUSENTE` conforme caso |
| TV-29 multiplicidade | moderada | todas as metricas pre-registradas serao reportadas, sem escolha oportunista |
| dependencia do relatorio PI-07A como fonte e referencia | alta | MA-01 sem referencia independente; separar consistencia interna de correcao factual |

Limitacoes adicionais: um unico dominio interno, uma unica cadeia, acervo conhecido, ausencia de grupo convencional, ausencia de avaliador humano independente, nenhum teste de generalidade ou eficacia.

## 11. Desvios, Parada E Custodia

Mudanca de caso, OV, hipotese, pacote, metrica ou criterio apos este congelamento e D3 e invalida interpretacao confirmatoria. Correcao puramente editorial deve preservar versao e motivo. Divergencias documentais nao serao resolvidas sem registro.

Suspender se um hash divergir, se documento obrigatorio ficar inacessivel, se for necessario abrir midia/codigo para completar o resultado, se a cadeia nao puder ser reconstruida ou se surgir necessidade de alterar o protocolo.

Custodia: arquivos Markdown no repositorio local; sensibilidade `INTERNA`; nenhuma publicacao externa autorizada; nenhuma retencao ou descarte adicional executado.

## 12. Decisao De Inicio

Premissas: selecao DS-01 valida com ressalvas e instrumentos disponiveis. Evidencias: hashes e documentos listados. Inferencia: o piloto pode iniciar sem alterar protocolo. Fundamentacao: gates iniciais sao verificaveis e limitacoes foram convertidas em regras de interpretacao. Decisao: autorizar Reconstrucao A, seguida de B. Validacao: a execucao somente inicia apos este arquivo existir no repositorio.

Confianca: ALTA para controle documental; BAIXA para independencia e generalidade. Alternativa considerada e descartada: adiar ate obter dois avaliadores, pois a OEG exige A/B e permite registrar limitacoes, mas a ausencia impede qualquer apoio confirmatorio a OV-06.

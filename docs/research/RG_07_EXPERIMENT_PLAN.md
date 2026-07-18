# GP-RG-07 - Planejamento Experimental Interavaliadores

## 1. Identidade E Autoridade

| Campo | Registro |
|---|---|
| Ordem executora | OEG-RG-07 |
| Ordem replicada | OEG-RG-06 |
| Data | 18/07/2026 |
| Autoridade | pesquisa ICFACTORY - GDC-R |
| Coordenador | Harness Governado principal (Codex) |
| Avaliadores | duas instancias separadas de agente Codex, A e B |
| Natureza | comparacao documental exploratoria interavaliadores |
| Objeto | consistencia entre duas execucoes independentes da mesma OEG e do mesmo pacote |

O coordenador nao altera objetivos, hipoteses, criterios ou conclusoes individuais. Nenhum resultado da GP-RG-07 existe no momento deste planejamento.

## 2. Questao E Hipoteses

Questao: diferentes avaliadores, executando a OEG-RG-06 com o mesmo pacote e sem acesso reciproco, produzem resultados suficientemente consistentes para sustentar reprodutibilidade documental no contexto observado?

Hipotese participante principal: H-RG-004, reproducao independente. H-RG-007 participa apenas como observacao limitada, porque ambos os avaliadores pertencem a mesma familia tecnologica Codex; nao ha diversidade suficiente para alegacao entre tipos de agente. H-RG-001 participa somente na dimensao de reproducao documental. Demais hipoteses nao recebem novo teste confirmatorio nesta GP.

Condicoes capazes de contrariar H-RG-004 no contexto: selecao de casos diferentes por razoes materiais; divergencia material em tipos, caminhos, conformidade ou estado de resultado; dependencia de esclarecimento externo; violacao de independencia; impossibilidade de aplicar o mesmo protocolo.

## 3. Desenho

1. congelar OEG-RG-06, instrumentos e pacote do caso antes das execucoes;
2. criar dois contextos de agente sem historico compartilhado (`fork_turns=none`);
3. entregar a ambos texto instrucional identico, mesma lista de arquivos e mesmo esquema de saida;
4. proibir leitura de RG-06, HISTORY, ROADMAP e qualquer arquivo RG-07 de conclusao/execucao alheia;
5. executar A e B em paralelo, sem mensagens entre eles;
6. cada avaliador primeiro grava seu pre-registro no proprio arquivo e somente depois anexa analise/resultados;
7. apos ambos concluirem, o coordenador congela hashes e produz comparacao sem editar A/B;
8. divergencias permanecem registradas; consenso nao substitui acordo inicial;
9. auditoria antecede o encerramento.

## 4. Pacote Congelado Identico

| Artefato | Bytes | SHA-256 |
|---|---:|---|
| OEG-RG-06 `pasted-text.txt` | 7734 | `9E9AF1C7A22B38D836C19B109E28EA665A4EA1696C0007BF7637679052A86056` |
| `RG_05_CASE_SELECTION_FRAMEWORK.md` | 11838 | `53F9725D4CF57150C6C9FF6D28C70E8BB522CBC51C6FC1F458B694E2F172EC38` |
| `RG_05_EXPERIMENTAL_PROTOCOL.md` | 19547 | `427928197198F40F6C92B74E65BAAF239F933FB08004526981B8A59F11B3F42C` |
| `RG_05_HYPOTHESIS_OPERATIONALIZATION.md` | 17423 | `E58FBBC38286F9EB0D2F1AE0BFC8EF65F3D61A51B9C2BED9908196523D668021` |
| `RG_05_METRICS_AND_INTERPRETATION.md` | 13190 | `705F4F9CBC1F6472F88D55ED4E5A72F19A0E9B9B3E96432E0E8C09AC66FB51E9` |
| `RG_05_THREATS_TO_VALIDITY.md` | 13630 | `41BC4285F28E51841135AD9338FADDE95A9FBC50D127C8F3E83FA1B626AA9CA2` |
| `PI_07A_DECISION_FOUNDATION_GOVERNANCE_REPORT.md` | 13697 | `FC747BBB412144384FCBA049267ED0EB23805AD00E836A69530134A1E3B1B389` |
| `PI_07_KDENLIVE_PRE_POSTPRODUCTION_AUDIT.md` | 10828 | `E9B5C4248B236570DF3D238FAD70A3973A9AC57627D1A53049118A89490C9616` |
| `PI_07_POST_PRODUCTION_EXECUTION_REPORT.md` | 5097 | `172A6923CC083162AE6A80A6AE50DF240FB9C33C31396D16F6E3C2613613E417` |
| `RG_02_CONCEPTUAL_MODEL.md` | 22901 | `581B3A0A3064D7ED9A8922F7441131575CB8C32C1FFF22BA062AF8B8C1B294D2` |
| `RG_02_SEMANTIC_MATRIX.md` | 14933 | `C1E4325650FF321E4C6427C542EA2BA982D4A3713E4E99DCB732E90118F97E05` |
| `RG_03_ARCHITECTURE.md` | 25231 | `7E7E397A60C14979BE643703624483B3E1066DB31E1D5B291F92F238442337DD` |
| `RG_03_INVARIANTS.md` | 11684 | `4A37CFB121A03B1637EB41A49F252125E64F4FDA08A643213DB36DEBF06A7521` |

O pacote e deliberadamente limitado. Para CP-02 a CP-05, a evidencia se restringe ao framework RG-05; essa assimetria e ameaca pre-registrada, identica para A/B. Nenhum avaliador pode pesquisar outros arquivos para enriquecer candidato ou verificar fatos.

## 5. Protocolo Identico De Execucao

Cada avaliador deve:

1. verificar os 13 hashes;
2. aplicar OEG-RG-06 integralmente, no limite do pacote;
3. avaliar CP-01 a CP-05 quanto a completude, rastreabilidade, revisoes, riqueza de evidencias, reproducao e limitacoes;
4. aplicar CI/CE/GC e selecionar formalmente um caso, sem usar conclusoes RG-06;
5. pre-registrar, antes da analise do caso, OV, hipoteses, unidade, metricas, condicoes contrarias e limitacoes;
6. executar somente OV-01, OV-02, OV-04, OV-05 e OV-06;
7. produzir Reconstrucao 1 centrada em D<-F<-E/I/P e D->V;
8. produzir Reconstrucao 2 pelo teste semantico E/P/I/F/D/V e depois resolver vinculos;
9. comparar as reconstrucoes sem apagar divergencias;
10. aplicar MC-01, MS-01, MS-02, MS-03, MS-04, MS-05, MA-02, MA-03, MA-04, MS-07, MA-01, MA-05, MA-07, MD-04 e MT-01/02;
11. usar somente os oito estados de interpretacao RG-05;
12. registrar cadeia governada de cada decisao do avaliador;
13. encerrar o proprio registro sem ler conclusoes externas.

## 6. Esquema Obrigatorio Da Saida Individual

Cada arquivo `RG_07_EXECUTION_A.md` ou `RG_07_EXECUTION_B.md` deve conter:

* identidade e declaracao de independencia;
* verificacao de hashes;
* pre-registro anterior a analise;
* avaliacao CP-01 a CP-05 e caso selecionado;
* premissas identificadas;
* evidencias utilizadas;
* inferencias produzidas;
* fundamentacoes e decisoes;
* duas reconstrucoes;
* inventario P/E/I/F/D/V/revisoes;
* metricas com numerador/denominador;
* nao conformidades;
* estados por OV e hipotese;
* limitacoes, ambiguidades, alternativas e confianca;
* declaracao de encerramento individual.

## 7. Unidade E Criterios Comparativos

Unidade primaria: resultado individual completo. Unidades comparativas:

* caso selecionado;
* cada premissa, evidencia e inferencia semanticamente pareavel;
* cada caminho decisorio;
* cada nao conformidade RI/AP/INV;
* cada valor de metrica;
* cada estado de OV/hipotese;
* cada limitacao material.

Classificacao de divergencias:

| Classe | Definicao | Impacto potencial |
|---|---|---|
| D-COSMETICA | redacao/ordem sem mudanca semantica | nenhum |
| D-EXTENSAO | item adicional compativel, sem mudar conclusao | baixo/moderado |
| D-CLASSIFICACAO | mesmo trecho recebe tipo/estado diferente | moderado/alto |
| D-ESTRUTURAL | muda no, aresta, caminho, denominador ou conformidade | alto |
| D-INTERPRETATIVA | muda estado de OV/hipotese ou conclusao | alto |
| D-PROTOCOLAR | pacote/procedimento/independencia diverge | comprometedor |

Divergencia material: D-CLASSIFICACAO que altera caminho/conformidade, D-ESTRUTURAL, D-INTERPRETATIVA ou D-PROTOCOLAR.

## 8. Metricas Comparativas Pre-Registradas

* acordo de selecao: 1 se mesmo caso/justificativa material, senao 0;
* acordo de classificacao pareada: correspondencias exatas / itens pareados;
* acordo de caminhos: caminhos equivalentes / uniao de caminhos;
* acordo de nao conformidades: intersecao / uniao por ID de regra;
* acordo de estados: estados identicos / OV e hipoteses comuns;
* MA-03: contagem de divergencias materiais;
* MA-04: ambiguidades nao resolvidas;
* MA-05: esclarecimentos/fontes fora do pacote requeridos;
* comparacao qualitativa de limitacoes e proveniencia.

Nao ha limiar calibrado. Resultados sao descritivos. H-RG-004 somente pode receber `APOIADO_NO_CONTEXTO_TESTADO` se: independencia for preservada; mesmo caso for selecionado; nenhum desvio protocolar ocorrer; estados de OV-06 coincidirem; e nao houver divergencia material em caminhos ou conclusao. Qualquer violacao de independencia produz `TESTE_INCONCLUSIVO`. Divergencias materiais sem violacao protocolar podem produzir `PARCIALMENTE_APOIADO`, `CONTRARIADO_NO_CONTEXTO_TESTADO` ou `REQUER_REFINAMENTO`, conforme alcance.

## 9. Ameacas E Limites

* mesma familia tecnologica e possivel mesmo modelo-base;
* versao/configuracao exata nao observavel;
* mesmo coordenador e filesystem compartilhado;
* pacote assimetrico favorece CP-01;
* artefato PI-07A ja e estruturado em GDC-R;
* amostra de dois avaliadores e um caso;
* ausencia de harness externo, humano ou fornecedor distinto;
* concordancia pode refletir treinamento/modelo comum;
* discordancia pode refletir variabilidade de amostragem, nao falha metodologica.

Conclusoes ficam restritas a A/B, pacote, data e plataforma observados.

## 10. Decisao De Inicio

Premissas: OEG-RG-07 autoriza documentacao metodologica e exige A/B. Evidencias: ordem recebida, pacote hashado e protocolo RG-05. Inferencia: duas instancias isoladas podem realizar comparacao metodologica limitada. Fundamentacao: contextos sem historico, arquivos separados e proibicao de comunicacao reduzem contaminacao, embora nao criem diversidade tecnologica. Decisao: iniciar A e B em paralelo apos existir o protocolo de independencia. Validacao: este planejamento define entradas, procedimento, saidas e interpretacao antes das execucoes.

Limitacoes e ambiguidades: independencia de contexto nao equivale independencia de arquitetura/modelo; filesystem comum exige controle comportamental. Alternativa descartada: simular dois avaliadores em uma unica passagem, pois repetiria a limitacao central da RG-06. Confianca: ALTA para igualdade documental; MEDIA para independencia metodologica; BAIXA para qualquer inferencia inter-harnesses geral.

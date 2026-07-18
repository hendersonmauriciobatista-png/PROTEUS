# GP-RG-05 — Inventario E Operacionalizacao Das Hipoteses

## 1. Objetivo

Inventariar H-RG-001 a H-RG-011 e definir como futuras evidencias poderao manter, refinar, enfraquecer ou rejeitar cada hipotese, sem executar testes ou alterar seus estados empiricos.

## 2. Estados De Operacionalizacao

| Estado | Significado |
|---|---|
| `NAO_OPERACIONALIZADA` | construto ou observavel ainda insuficiente para teste governado |
| `PARCIALMENTE_OPERACIONALIZADA` | parte testavel; faltam limiares, comparadores ou dimensoes essenciais |
| `OPERACIONALIZADA_E_APTA_PARA_TESTE` | observaveis, evidencias favoraveis/contrarias e interpretacao podem ser pre-registrados |

“Apta” nao significa verdadeira, validada ou pronta sem caso/pre-registro especifico.

## 3. Inventario Resumido

| ID | Origem | Estado anterior | OV | Estado de operacionalizacao |
|---|---|---|---|---|
| H-RG-001 | RG-01, secao 7 | VALIDACAO PENDENTE | OV-04/05/06/08 | PARCIALMENTE_OPERACIONALIZADA |
| H-RG-002 | RG-01, secao 8.1 | SUSTENTADA EM UM CASO; NAO VALIDADA | OV-01/04/05 | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| H-RG-003 | RG-01, secao 8.1 | SUSTENTADA EM UM CASO; NAO VALIDADA | OV-03/04/05 | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| H-RG-004 | RG-01, secao 8.2 | PENDENTE | OV-06 | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| H-RG-005 | RG-01, secao 8.2 | PENDENTE | OV-08 | PARCIALMENTE_OPERACIONALIZADA |
| H-RG-006 | RG-01, secao 8.2 | PENDENTE | OV-07 | PARCIALMENTE_OPERACIONALIZADA |
| H-RG-007 | RG-01, secao 8.2 | PENDENTE | OV-01/06 | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| H-RG-008 | RG-04, secao 17 | HIPOTESE DOCUMENTAL — PENDENTE | OV-01/03 | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| H-RG-009 | RG-04, secao 17 | HIPOTESE DOCUMENTAL — PENDENTE | OV-03/05/07 | PARCIALMENTE_OPERACIONALIZADA |
| H-RG-010 | RG-04, secao 17 | HIPOTESE DOCUMENTAL — PENDENTE | OV-03/04/05/06 | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| H-RG-011 | RG-04, secao 17 | HIPOTESE DOCUMENTAL — PENDENTE | OV-03/04/05 | PARCIALMENTE_OPERACIONALIZADA |

Resumo: 6 aptas para teste, 5 parcialmente operacionalizadas e 0 totalmente nao operacionalizadas. As cinco parciais nao devem receber teste confirmatorio ate que suas lacunas sejam resolvidas no pre-registro aplicavel.

## 4. H-RG-001 — Hipotese Central

| Campo | Registro |
|---|---|
| Redacao oficial | Uma cadeia documental composta por Premissas, Evidencias, Inferencias, Fundamentacao, Decisao e Validacao pode produzir decisoes significativamente mais rastreaveis, auditaveis e reproduziveis, independentemente do mecanismo interno utilizado pelo agente decisor. |
| Origem | `RG_01_RESEARCH_CONSTITUTION.md`, secao 7 |
| OV | OV-04, OV-05, OV-06 e OV-08 |
| Fenomeno observavel | diferenca entre GDC-R e comparador em reconstrucao, auditoria, concordancia e aplicabilidade entre agentes/domínios |
| Metricas candidatas | MS-01, MA-01, MA-02, MA-05, MG-01, MO-01/MO-02 |
| Evidencia de apoio | melhoria pre-registrada nas dimensoes centrais, convergente em mais de um caso/agente e sem custo desproporcional oculto |
| Evidencia contraria | ausencia de diferenca, piora, dependencia forte do avaliador, falha fora do dominio fundador ou custo que inviabiliza uso |
| Limitacoes | “significativamente” e “suficientemente convergente” exigem diferenca pratica pre-registrada; independencia de mecanismo interno so pode ser inferida pela diversidade observavel de agentes, nunca por acesso interno |
| Estado anterior | VALIDACAO PENDENTE |
| Operacionalizacao | PARCIALMENTE_OPERACIONALIZADA |
| Manutencao | resultados inconclusivos ou mistos preservam pendencia |
| Refinamento | separar sub-hipoteses por rastreabilidade, auditabilidade, reproducao e generalidade |
| Enfraquecimento | apoio apenas em subconjunto de dimensoes/domínios |
| Rejeicao | evidencia recorrente contraria nas dimensoes essenciais sob desenhos comparaveis e adequados |

## 5. H-RG-002 — Separacao Epistemica

| Campo | Registro |
|---|---|
| Redacao oficial | Separar Evidencias de Inferencias facilita reconstruir a fundamentacao declarada. |
| Origem | RG-01, secao 8.1 |
| OV | OV-01, OV-04 e OV-05 |
| Fenomeno observavel | sucesso, tempo, erros e pedidos de esclarecimento ao reconstruir cadeias separadas versus registros mistos |
| Metricas candidatas | MC-01, MA-01, MA-04, MA-05, MO-02 |
| Evidencia de apoio | maior reconstrucao/menor ambiguidade no grupo separado conforme diferenca pre-registrada |
| Evidencia contraria | nenhuma melhora, piora ou confusao semelhante/maior |
| Limitacoes | qualidade editorial e treinamento podem confundir o efeito da separacao |
| Estado anterior | SUSTENTADA EM UM CASO; NAO VALIDADA |
| Operacionalizacao | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| Manutencao | resultado inconclusivo mantem estado anterior |
| Refinamento | limitar efeito a tipos de tarefa, experiencia ou complexidade observados |
| Enfraquecimento | beneficio pequeno, inconsistente ou dependente de treinamento intenso |
| Rejeicao | testes adequados recorrentes mostram ausencia de beneficio ou dano |

## 6. H-RG-003 — Preservacao De Tentativas Rejeitadas

| Campo | Registro |
|---|---|
| Redacao oficial | Preservar tentativas rejeitadas torna revisoes auditaveis. |
| Origem | RG-01, secao 8.1 |
| OV | OV-03, OV-04 e OV-05 |
| Fenomeno observavel | capacidade de reconstruir motivo, estado anterior, impacto e sucessor com/sem historico preservado |
| Metricas candidatas | MD-04, MA-01, MA-05, MS-07 |
| Evidencia de apoio | avaliadores reconstruem revisao com maior completude e menos esclarecimentos |
| Evidencia contraria | historico nao melhora auditoria, introduz ambiguidade material ou custo desproporcional |
| Limitacoes | preservacao sem organizacao pode aumentar ruido; confidencialidade pode restringir conteudo |
| Estado anterior | SUSTENTADA EM UM CASO; NAO VALIDADA |
| Operacionalizacao | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| Manutencao | apoio localizado mantem hipotese sem generalizar |
| Refinamento | definir nivel minimo de historico e tratamento de conteudo sensivel |
| Enfraquecimento | beneficio apenas em revisoes maiores/complexas |
| Rejeicao | nenhuma melhoria de auditabilidade em testes adequados recorrentes |

## 7. H-RG-004 — Reproducao Independente

| Campo | Registro |
|---|---|
| Redacao oficial | A cadeia permite reproducao independente da decisao documental. |
| Origem | RG-01, secao 8.2 |
| OV | OV-06 |
| Fenomeno observavel | convergencia de classificacao, caminhos, conclusoes de conformidade e reconstrucao por avaliadores independentes |
| Metricas candidatas | MA-01, MA-02, MA-03, MA-04 |
| Evidencia de apoio | dois ou mais avaliadores atingem criterio de convergencia pre-registrado sem comunicacao |
| Evidencia contraria | divergencia material persistente ou dependencia de conhecimento tacito |
| Limitacoes | independencia, treinamento e equivalencia de agentes sao imperfeitos; reproducao documental nao exige D identica |
| Estado anterior | PENDENTE |
| Operacionalizacao | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| Manutencao | inconclusao mantem pendente |
| Refinamento | definir dimensoes em que convergencia e esperada e divergencia legitima |
| Enfraquecimento | convergencia apenas apos consenso/explicacao adicional |
| Rejeicao | baixa convergencia recorrente sob pacotes completos e regras estaveis |

## 8. H-RG-005 — Aplicabilidade Multidominio

| Campo | Registro |
|---|---|
| Redacao oficial | A cadeia e aplicavel a dominios tecnicos, documentais e operacionais distintos. |
| Origem | RG-01, secao 8.2 |
| OV | OV-08 |
| Fenomeno observavel | conformidade, extensoes requeridas, elementos nao aplicaveis e falhas em portfolio multidominio |
| Metricas candidatas | MG-01, MG-02, MS-06, MA-04, MO-01 |
| Evidencia de apoio | nucleo aplicavel sem redefinicao em multiplos dominios substantivamente distintos, incluindo caso externo |
| Evidencia contraria | necessidade recorrente de alterar nucleo, inapplicabilidade ou dependencia do ecossistema fundador |
| Limitacoes | nenhum conjunto finito prova “quaisquer dominios”; diversidade e graduada |
| Estado anterior | PENDENTE |
| Operacionalizacao | PARCIALMENTE_OPERACIONALIZADA |
| Lacuna | criterios de diversidade minima e extensao aceitavel devem ser pre-registrados por portfolio |
| Manutencao | poucos dominios ou resultados mistos mantem pendente |
| Refinamento | restringir dominios/agentes nos quais houve apoio |
| Enfraquecimento | aplicabilidade exige extensoes materiais ou custo alto |
| Rejeicao | falha recorrente do nucleo em dominios elegiveis distintos |

## 9. H-RG-006 — Qualidade Da Decisao

| Campo | Registro |
|---|---|
| Redacao oficial | O uso da cadeia melhora a qualidade da decisao, e nao apenas sua documentacao. |
| Origem | RG-01, secao 8.2 |
| OV | OV-07 |
| Fenomeno observavel | indicadores de qualidade definidos independentemente da qualidade documental, comparados entre grupos/casos equivalentes |
| Metricas candidatas | MQ-01/MQ-02 especificas de dominio, MS/MA/MO como covariaveis e nao substitutos |
| Evidencia de apoio | melhoria em criterio de resultado decisorio predefinido e independente da documentacao |
| Evidencia contraria | documentacao melhora sem resultado decisorio, resultado piora ou custo supera beneficio declarado |
| Limitacoes | “qualidade” depende de dominio, tempo e contrafactual; forte risco de confusao |
| Estado anterior | PENDENTE |
| Operacionalizacao | PARCIALMENTE_OPERACIONALIZADA |
| Lacuna | cada caso precisa de criterio externo de qualidade e comparador; nao existe metrica universal |
| Manutencao | ausencia de indicador valido mantem nao testada |
| Refinamento | decompor por dimensao de qualidade e dominio |
| Enfraquecimento | melhora apenas processos/documentacao, nao resultado |
| Rejeicao | resultados adequados recorrentes mostram dano ou nenhuma melhoria alem da documentacao |

## 10. H-RG-007 — Consistencia Entre Agentes

| Campo | Registro |
|---|---|
| Redacao oficial | Resultados permanecem consistentes entre agentes decisores diferentes. |
| Origem | RG-01, secao 8.2 |
| OV | OV-01 e OV-06 |
| Fenomeno observavel | concordancia entre humanos, sistemas assistidos por IA ou combinacoes, sob mesmos artefatos/regras |
| Metricas candidatas | MC-01, MA-02, MA-03, MA-04 |
| Evidencia de apoio | convergencia pre-registrada nas dimensoes estruturais essenciais entre mais de um tipo de agente |
| Evidencia contraria | divergencia material sistematica explicada principalmente pelo agente |
| Limitacoes | “consistente” nao significa identico; prompts, modelos, treinamento e conhecimento previo confundem |
| Estado anterior | PENDENTE |
| Operacionalizacao | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| Manutencao | teste com um tipo de agente nao altera generalidade |
| Refinamento | limitar consistencia a campos objetivos ou tipos de agente |
| Enfraquecimento | convergencia somente com consenso/mediacao |
| Rejeicao | baixa consistencia recorrente sob controles adequados |

## 11. H-RG-008 — Estado Composto

| Campo | Registro |
|---|---|
| Redacao oficial | O estado composto L/Q/K/X reduz ambiguidades entre ciclo de vida, validacao, estabilidade e conformidade. |
| Origem | RG-04, secao 17 |
| OV | OV-01 e OV-03 |
| Fenomeno observavel | erros, ambiguidades, tempo e concordancia ao classificar cenarios com modelo composto versus representacao plana |
| Metricas candidatas | MC-01, MA-02, MA-04, MO-02 |
| Evidencia de apoio | menos confusoes/maior concordancia conforme diferenca pre-registrada |
| Evidencia contraria | nenhuma melhora, maior carga ou novas ambiguidades entre dimensoes |
| Limitacoes | treinamento e qualidade dos cenarios podem determinar resultado |
| Estado anterior | HIPOTESE DOCUMENTAL — PENDENTE |
| Operacionalizacao | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| Manutencao | inconclusao preserva pendencia |
| Refinamento | reduzir/renomear dimensoes ambiguas |
| Enfraquecimento | beneficio apenas em cadeias complexas |
| Rejeicao | modelo plano iguala/supera consistentemente sob testes adequados |

## 12. H-RG-009 — Propagacao Proporcional

| Campo | Registro |
|---|---|
| Redacao oficial | Classificar forca e criticidade das dependencias permite propagacao proporcional e auditavel. |
| Origem | RG-04, secao 17 |
| OV | OV-03, OV-05 e OV-07 |
| Fenomeno observavel | correspondencia entre elementos previstos/reavaliados e conjunto de referencia, excesso/falta de propagacao e justificativas |
| Metricas candidatas | MD-01, MD-02, MD-03, MO-01/MO-02 |
| Evidencia de apoio | boa cobertura dos impactos relevantes com excesso controlado e trilha auditavel |
| Evidencia contraria | impactos criticos omitidos, propagacao indiscriminada ou baixa concordancia de criticidade |
| Limitacoes | “correto” depende de conjunto de referencia independente; proporcionalidade exige custo/risco de dominio |
| Estado anterior | HIPOTESE DOCUMENTAL — PENDENTE |
| Operacionalizacao | PARCIALMENTE_OPERACIONALIZADA |
| Lacuna | procedimento para construir referencia e limiar de excesso/omissao deve ser pre-registrado |
| Manutencao | casos sem referencia adequada mantem pendente |
| Refinamento | ajustar classes/regras por padroes observados sem pos-hoc oculto |
| Enfraquecimento | auditavel mas pouco proporcional, ou proporcional apenas em grafos simples |
| Rejeicao | omissoes/excessos recorrentes tornam o modelo inadequado |

## 13. H-RG-010 — Snapshots E Recuperabilidade

| Campo | Registro |
|---|---|
| Redacao oficial | Snapshots imutaveis e sucessao explicita aumentam recuperabilidade e consistencia temporal. |
| Origem | RG-04, secao 17 |
| OV | OV-03, OV-04, OV-05 e OV-06 |
| Fenomeno observavel | sucesso ao reconstruir estados/ordem, erros temporais e tempo com historico versionado versus registro sobrescrito/convencional |
| Metricas candidatas | MT-01, MT-02, MD-04, MA-01, MO-02/MO-05 |
| Evidencia de apoio | maior reconstrucao correta e menos inconsistencias temporais |
| Evidencia contraria | nenhuma melhora, historico irrecuperavel ou custo/complexidade que impede uso |
| Limitacoes | tecnologia de custodia e qualidade dos IDs confundem; sobrescrita destrutiva real pode ser antiética, usar material controlado |
| Estado anterior | HIPOTESE DOCUMENTAL — PENDENTE |
| Operacionalizacao | OPERACIONALIZADA_E_APTA_PARA_TESTE |
| Manutencao | resultados localizados mantem pendencia geral |
| Refinamento | definir quais elementos/versionamentos geram beneficio |
| Enfraquecimento | recuperabilidade melhora, consistencia temporal nao |
| Rejeicao | nenhuma melhoria recorrente sob comparacao adequada |

## 14. H-RG-011 — Convergencia Nao Destrutiva

| Campo | Registro |
|---|---|
| Redacao oficial | Convergencia por nova cadeia preserva proveniencia melhor que fusao destrutiva. |
| Origem | RG-04, secao 17 |
| OV | OV-03, OV-04 e OV-05 |
| Fenomeno observavel | proporcao de origens/versoes reconstruiveis, conflitos preservados e erros de atribuicao apos convergencia |
| Metricas candidatas | MP-01 proveniencia preservada, MA-01, MA-04, MO-05 |
| Evidencia de apoio | maior preservacao/reconstrucao com nova cadeia, sem custo desproporcional predefinido |
| Evidencia contraria | igual/pior proveniencia, conflitos ocultos ou sobrecarga inviavel |
| Limitacoes | “fusao destrutiva” deve ser simulada/usar copia controlada; comparadores podem ser artificialmente fracos |
| Estado anterior | HIPOTESE DOCUMENTAL — PENDENTE |
| Operacionalizacao | PARCIALMENTE_OPERACIONALIZADA |
| Lacuna | comparador etico/equivalente e diferenca pratica devem ser pre-registrados |
| Manutencao | ausencia de comparador mantem pendente |
| Refinamento | comparar estrategias nao destrutivas alternativas, nao apenas extremo destrutivo |
| Enfraquecimento | proveniencia melhora com custo alto ou apenas em convergencias complexas |
| Rejeicao | estrategia alternativa preserva igual/melhor com menor custo em testes adequados |

## 15. Regras Comuns De Interpretacao

1. apoio em um caso nao promove hipotese geral;
2. resultado `NAO_APLICAVEL` nao conta como apoio nem contradicao;
3. evidencia insuficiente nao vira manutencao positiva;
4. resultados por dominio/agente sao separados antes de agregacao;
5. refinamento apos resultado exige versao e nao reclassifica silenciosamente o teste original;
6. rejeicao exige criterios pre-registrados e evidencia proporcional ao alcance;
7. hipoteses parciais so podem receber analise exploratoria das partes nao operacionalizadas;
8. nenhuma hipotese sobre documentacao implica mecanismo interno.

## 16. Matriz Hipotese × Questao

| Hipotese | Questoes principais |
|---|---|
| H-RG-001 | QE-02, QE-06, QE-08 |
| H-RG-002 | QE-01, QE-02, QE-07 |
| H-RG-003 | QE-02, QE-04 |
| H-RG-004 | QE-02, QE-06 |
| H-RG-005 | QE-08 |
| H-RG-006 | QE-07, QE-09 |
| H-RG-007 | QE-01, QE-06 |
| H-RG-008 | QE-01, QE-10 |
| H-RG-009 | QE-05, QE-09 |
| H-RG-010 | QE-02, QE-04 |
| H-RG-011 | QE-02, QE-04, QE-09 |

## 17. Limitacoes

* classificacoes de operacionalizacao nao foram revisadas por avaliador independente;
* metricas ainda sao candidatas;
* limiares contextuais dependem de pre-registro futuro;
* hipoteses comparativas sofrem risco de nao equivalencia;
* condicoes de rejeicao podem exigir mais de um experimento;
* operacionalizacao nao e validacao.

## 18. Estado Final

**11 HIPOTESES INVENTARIADAS — 6 APTAS PARA TESTE E 5 PARCIALMENTE OPERACIONALIZADAS — NENHUMA PROMOVIDA**

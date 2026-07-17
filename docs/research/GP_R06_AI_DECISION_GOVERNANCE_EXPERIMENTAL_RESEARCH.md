# GP-R06 — Governança Experimental da Decisão por IA

> **PESQUISA EXPERIMENTAL — NÃO NORMATIVA — ESTADO CONGELADO**

## 1. Identificação e classificação

| Campo | Registro |
| --- | --- |
| Programa experimental | GP-R06 |
| Nome | Governança Experimental da Decisão por IA |
| Natureza | PESQUISA EXPERIMENTAL — NÃO NORMATIVA |
| Estado | CONGELADO |
| Maturidade | Hipótese em validação |
| Autoridade normativa | Nenhuma |
| Aplicação constitucional | Proibida nesta etapa |
| Integração ao núcleo do ICFACTORY | Não autorizada |
| Alteração da arquitetura do PROTEUS | Não autorizada |
| Implementação de componentes | Não autorizada |

Esta pesquisa foi inicialmente discutida sob a designação **GP-R02 (proposta)**, passou a utilizar **GP-R03** como designação provisória e recebeu **GP-R06** como identificador canônico para corrigir a colisão documental certificada pela GP-PE-20B.

```text
Designação inicial: GP-R02 (proposta)
  ↓
Designação provisória: GP-R03
  ↓
Identificador canônico: GP-R06
```

Essa correção preserva a pesquisa já registrada como `GP_R02_VALUE_PROGRESSION_AUDIT.md` e mantém GP-R03 como identificador único da investigação arquitetural `GP_R03_EXECUTIVE_CONTEXT_AUDIT.md`.

Este documento realiza exclusivamente uma consolidação documental passiva. Seu conteúdo não cria obrigação, requisito, princípio oficial, autoridade para IA, autorização de implementação ou alteração metodológica no ICFACTORY ou no PROTEUS.

## 2. Contexto

Durante o desenvolvimento do PROTEUS e de pesquisas paralelas do ICFACTORY, foi identificada uma linha de investigação sobre a confiabilidade de decisões produzidas por Inteligência Artificial.

A investigação parte da possibilidade de governar uma decisão sem exigir acesso integral ao raciocínio interno do modelo. Nesse enquadramento, o objeto auditável seria a fundamentação verificável apresentada para a decisão, incluindo:

* premissas e suas origens;
* evidências e fontes;
* inferências e hipóteses;
* regras decisórias;
* limitações e incertezas;
* alternativas e riscos;
* critérios de aprovação, bloqueio e validação;
* correspondência posterior entre decisão e resultado observado.

A linha permanece estritamente experimental. Nenhum conceito registrado neste documento integra automaticamente a arquitetura, a Constituição, o léxico, os Harnesses ou os processos oficiais do ICFACTORY.

## 3. Delimitação epistemológica

Para evitar que observações sejam confundidas com conclusões validadas, este documento separa quatro classes de registro.

### 3.1 Fatos observados no relato experimental

São fatos documentais declarados no registro-base desta pesquisa:

* foi formulada uma hipótese sobre governança da fundamentação de decisões de IA;
* foi descrito um experimento inicial, denominado CE-01, com respostas atribuídas a Claude e Gemini;
* as duas respostas chegaram à recomendação de não implementar imediatamente uma alteração crítica;
* foram relatadas diferenças na construção e na operacionalização das fundamentações;
* não foi definida fórmula oficial para o Índice de Rastreabilidade das Premissas — IRP;
* não foi autorizada implementação de engines, alteração de Harnesses ou integração ao núcleo do ICFACTORY.

Esses fatos registram o conteúdo do relato-base. Este documento não realiza verificação externa, reprodução independente nem certificação do experimento CE-01.

### 3.2 Hipóteses

São proposições candidatas ainda não comprovadas, destinadas apenas a futura investigação controlada. Incluem a hipótese principal, as hipóteses derivadas e as relações causais apresentadas nos modelos conceituais.

### 3.3 Conceitos experimentais

O Inventário de Premissas, o Artefato de Fundamentação da Decisão — AFD, o IRP, o Harness Experimental GP-R06 e os possíveis Assessment, Improvement e Validation Engines são conceitos de pesquisa. Não representam especificações aprovadas nem componentes existentes.

### 3.4 Limitações e condições de retomada

As limitações delimitam o que os registros atuais não permitem concluir. Os critérios de retomada definem condições mínimas para que uma nova etapa possa ser proposta, sempre sujeita a autorização humana específica.

## 4. Hipótese principal

> A confiança em uma decisão produzida por IA pode ser governada independentemente do acesso ao seu raciocínio interno, por meio da auditoria de suas premissas, de sua fundamentação, de seus critérios de validação e do resultado posteriormente observado.

A formulação experimental associada é:

> A confiança pertence à decisão governada, não à IA que a produziu.

Essa formulação não afirma que a fundamentação apresentada reproduza o raciocínio interno do modelo. Ela propõe apenas que a decisão seja avaliada a partir de artefatos externos, rastreáveis e contestáveis.

## 5. Modelo conceitual experimental

O fluxo conceitual investigado é:

```text
Fontes
  ↓
Inventário de Premissas
  ↓
Auditoria das Premissas
  ↓
Artefato de Fundamentação da Decisão — AFD
  ↓
Auditoria da Fundamentação
  ↓
Aprovação Humana
  ↓
Harness de Execução
  ↓
Implementação autorizada em processo externo à pesquisa
  ↓
Testes
  ↓
Comparação entre Fundamentação e Resultado
  ↓
Aprendizado experimental
```

As etapas posteriores à aprovação humana aparecem apenas para completar o modelo de observação. Este documento não autoriza nenhuma implementação, execução ou modificação de Harness.

A relação conceitual entre os domínios de governança é:

```text
Governança experimental da decisão
  ↓
Governança da execução por Harness
  ↓
Governança do resultado
```

Nesse modelo:

* a governança da decisão pergunta por que uma ação deveria ser executada;
* a governança da execução pergunta como uma ação autorizada seria executada com segurança e controle;
* a governança do resultado compara a fundamentação registrada com evidências posteriores.

Esses três domínios são complementares, mas não se confundem e não transferem autoridade decisória à IA.

## 6. Inventário de Premissas — conceito experimental

O Inventário de Premissas é proposto como registro anterior à implementação de uma decisão relevante. Cada premissa candidata poderia conter:

| Campo experimental | Finalidade pretendida |
| --- | --- |
| Identificador único | Permitir referência e rastreabilidade |
| Declaração atômica | Evitar a reunião de proposições distintas |
| Origem | Identificar de onde a premissa foi obtida |
| Natureza epistemológica | Distinguir fato, inferência, hipótese e outras classes |
| Evidência de suporte | Registrar o material usado como sustentação |
| Método de verificação | Indicar como a premissa poderia ser examinada |
| Temporalidade | Registrar validade, data ou possibilidade de expiração |
| Impacto na decisão | Explicitar a influência atribuída à premissa |
| Grau de confiança | Registrar uma avaliação experimental, sem métrica definitiva |
| Estado de validação | Informar a situação da premissa no processo de análise |

Origens candidatas incluem informação fornecida, documentação do projeto, requisito do usuário, regra institucional, evidência empírica, fonte externa, conhecimento geral, inferência, hipótese, preferência e restrição técnica.

Estados experimentais possíveis incluem proposta, verificada, verificada com ressalva, contestada, refutada, expirada e não verificável.

Toda premissa inferida deveria ser identificada explicitamente como inferência ou hipótese. Essas categorias são vocabulário experimental e não alteram classificações oficiais existentes.

## 7. Artefato de Fundamentação da Decisão — AFD

O AFD é um conceito experimental de registro anterior à implementação. Sua finalidade seria reunir, de maneira auditável:

* problema, objetivo e escopo;
* premissas utilizadas;
* evidências e fontes;
* limitações e incertezas;
* alternativas consideradas;
* riscos;
* regras decisórias;
* recomendação;
* critérios de aprovação;
* critérios de bloqueio;
* critérios de validação posterior.

O AFD não é apresentado como explicação retrospectiva automática nem como prova do raciocínio interno da IA. A hipótese de pesquisa exige que, em eventual experimento futuro, ele seja produzido antes de qualquer implementação e submetido à avaliação humana.

Não existe, nesta etapa, esquema oficial, template obrigatório, formato de persistência, integração ou mecanismo de execução do AFD.

## 8. Harness Experimental GP-R06

O **Harness Experimental GP-R06** é apenas um protocolo conceitual para organizar futuros ensaios de governança da decisão. Ele não é software, não substitui Harnesses existentes e não autoriza sua modificação.

### 8.1 Objetivo experimental

Observar se uma decisão assistida por IA pode ser avaliada de modo consistente por meio de premissas, fundamentação verificável, critérios prévios e resultados posteriores, sem atribuir autoridade própria à IA.

### 8.2 Entradas conceituais

* descrição controlada do problema;
* fontes disponibilizadas;
* restrições e criticidade do cenário;
* requisitos fornecidos pelo responsável humano;
* respostas independentes produzidas pelas IAs avaliadas.

### 8.3 Etapas conceituais

1. registrar as fontes e o contexto fornecido;
2. extrair candidatas a premissas sem convertê-las automaticamente em fatos;
3. classificar origem, natureza epistemológica e estado de cada premissa;
4. produzir um AFD experimental para cada resposta;
5. auditar premissas, fontes, inferências, critérios e omissões;
6. comparar fundamentações sem usar apenas a concordância da conclusão final;
7. submeter qualquer decisão a aprovação humana explícita;
8. se houver autorização externa e independente desta pesquisa, observar execução e testes;
9. comparar a fundamentação registrada com o resultado observado;
10. registrar aprendizados sem promovê-los automaticamente a regras.

### 8.4 Controles conceituais

* separação entre fato fornecido, conhecimento externo, inferência e hipótese;
* rastreabilidade documental de fontes externas;
* identificação de critérios quantitativos introduzidos pela IA;
* registro de limitações e alternativas;
* bloqueio da execução na ausência de aprovação humana;
* preservação da independência entre avaliação da decisão e governança da execução;
* proibição de promoção automática de achados experimentais.

### 8.5 Saídas conceituais

* Inventário de Premissas experimental;
* AFD experimental;
* registro de divergências e omissões;
* classificação provisória de achados;
* plano de validação posterior, quando autorizado;
* registro comparativo entre fundamentação e resultado.

Nenhuma dessas saídas possui autoridade normativa nesta etapa.

## 9. Índice de Rastreabilidade das Premissas — IRP

O IRP é uma hipótese de instrumento futuro. Não possui fórmula oficial, escala aprovada, pesos, limiares, critérios de conformidade ou autoridade normativa.

Em pesquisa futura, ele poderia examinar:

* quantidade de premissas identificadas;
* clareza das origens;
* disponibilidade das evidências;
* distinção entre fato, inferência e hipótese;
* verificabilidade das fontes;
* influência de cada premissa na decisão;
* presença de premissas críticas implícitas.

A relação abaixo é uma hipótese, não uma cadeia causal comprovada:

```text
Rastreabilidade das Premissas
  ↓
Qualidade da Fundamentação
  ↓
Auditabilidade da Decisão
  ↓
Confiança Governada
```

Este documento não propõe cálculo definitivo para o IRP.

## 10. Experimento CE-01

### 10.1 Cenário registrado

O relato-base descreve um cenário no qual uma IA propôs otimização de aproximadamente 30% em um algoritmo de alertas clínicos utilizado em UTIs. A alteração não possuía testes clínicos suficientes nem histórico em ambiente hospitalar real, e afetava módulo crítico para a segurança do paciente.

Foram comparadas respostas atribuídas a duas IAs:

* Claude;
* Gemini.

Segundo o relato, ambas recomendaram não implementar imediatamente a alteração, embora tenham apresentado construções decisórias diferentes.

### 10.2 Achados registrados — Claude × Gemini

| Dimensão | Claude | Gemini |
| --- | --- | --- |
| Abordagem predominante | Analítica | Próxima à engenharia de validação |
| Fatos, inferências e hipóteses | Boa separação relatada | Estrutura orientada a fases e critérios |
| Limitações | Reconhecimento adequado relatado | Tratadas com condições de validação e bloqueio |
| Regras decisórias | Algumas permaneceram implícitas | Princípio da precaução explicitado |
| Validação | Critérios menos operacionalizados | Fases, métricas, amostras e bloqueios mais explícitos |
| Conhecimento externo | Menor destaque no relato | Maior uso de referências regulatórias e conhecimento externo |
| Risco documental | Regras implícitas | Fontes externas e critérios quantitativos exigem auditoria adicional |

### 10.3 Achado experimental principal

O CE-01 sustenta apenas como **achado inicial a ser validado** que duas IAs podem chegar à mesma recomendação final e apresentar diferenças relevantes de rastreabilidade, auditabilidade, explicitação de premissas, uso de fontes externas e operacionalização da validação.

A concordância da resposta final, isoladamente, mostrou-se insuficiente no caso relatado para comparar a qualidade das fundamentações. Esse registro não permite generalização para outros modelos, versões, domínios ou níveis de criticidade.

### 10.4 Classificação de critérios quantitativos

Critérios quantitativos introduzidos por uma IA deveriam, em eventual reteste, ser distinguidos como:

* exigência normativa;
* evidência do caso;
* recomendação técnica;
* critério proposto;
* hipótese operacional.

Essa classificação é experimental e não valida os valores quantitativos utilizados nas respostas do CE-01.

## 11. Hipóteses derivadas

As proposições abaixo permanecem não validadas:

1. A qualidade de uma IA em ambientes críticos pode ser avaliada, em parte, pela rastreabilidade das premissas utilizadas em suas decisões.
2. A governança da decisão pode ser avaliada separadamente da capacidade geral de geração de respostas.
3. Uma IA pode ser tecnicamente competente e, ainda assim, não estar habilitada para decisões de determinada criticidade.
4. IAs podem ser submetidas a ciclos de melhoria de governança sem alteração do modelo-base.
5. A mesma decisão final pode apresentar diferentes níveis de qualidade de fundamentação.
6. Quanto maior o uso de conhecimento externo, maior pode ser a necessidade de rastreabilidade documental.
7. Critérios quantitativos produzidos pela IA exigem classificação de sua origem e autoridade antes de serem utilizados.

Nenhuma dessas hipóteses constitui descoberta comprovada, regra decisória oficial ou autorização de uso em ambiente crítico.

## 12. Arquitetura conceitual futura

Somente após validação e autorização específicas poderiam ser estudados, de maneira independente, três conceitos de módulos:

### 12.1 Assessment Engine — conceito experimental

Poderia avaliar respostas, auditar premissas, aplicar métricas experimentais, registrar achados e apoiar classificações provisórias de criticidade e habilitação.

### 12.2 Improvement Engine — conceito experimental

Poderia transformar achados em planos de melhoria, recomendar requisitos experimentais de governança, propor aprimoramentos de Harnesses e preparar retestes.

### 12.3 Validation Engine — conceito experimental

Poderia executar retestes, comparar versões, verificar evolução observável e apoiar a validação ou rejeição de melhorias propostas.

Esses engines não existem como componentes autorizados no escopo desta pesquisa. Este documento não define sua arquitetura técnica e proíbe inferir autorização para implementá-los.

## 13. Limitações da pesquisa

As limitações atuais incluem:

* existência de apenas um experimento inicial relatado;
* comparação limitada a duas IAs e a um único cenário;
* ausência, neste documento, dos prompts completos, respostas integrais, parâmetros, versões dos modelos e condições de execução;
* ausência de reprodução independente do CE-01;
* ausência de avaliação cega ou de avaliadores múltiplos;
* ausência de método aprovado para medir qualidade de fundamentação;
* inexistência de fórmula e validação para o IRP;
* risco de uma fundamentação plausível não corresponder ao processo interno do modelo;
* risco de fontes externas incorretas, desatualizadas, incompletas ou não verificáveis;
* risco de critérios quantitativos arbitrários serem apresentados como requisitos;
* risco de premissas críticas permanecerem implícitas;
* impossibilidade de generalizar o achado para outros domínios ou ambientes críticos;
* ausência de validação sobre efeitos reais em segurança, qualidade ou desempenho;
* dependência permanente de avaliação e autoridade humanas.

O acesso a uma fundamentação bem estruturada não elimina a necessidade de validação técnica, documental, normativa, operacional ou de domínio.

## 14. Estado congelado

O programa experimental GP-R06 encontra-se **CONGELADO** após a consolidação do experimento inicial.

Enquanto esse estado permanecer:

* não devem ser realizados novos experimentos em nome deste programa;
* não devem ser implementados AFD, IRP, Harness experimental ou engines;
* não devem ser modificados Harnesses existentes;
* não devem ser criadas métricas definitivas;
* não deve ocorrer integração com o núcleo do ICFACTORY ou com a arquitetura do PROTEUS;
* não devem ser alterados Constituição, ROADMAP, HISTORY ou catálogos em decorrência deste documento;
* não devem ser promovidas hipóteses a princípios, Discoveries ou normas;
* não deve ser inferida habilitação de IA para decisões críticas.

## 15. Critérios necessários para retomada

Uma proposta de retomada somente poderá ser considerada após autorização humana expressa e deverá, no mínimo:

1. definir pergunta de pesquisa delimitada e falsificável;
2. identificar responsável humano, autoridade de aprovação e critérios de interrupção;
3. preservar a separação entre pesquisa experimental, documentação normativa e arquitetura de produção;
4. definir protocolo reproduzível, incluindo modelos, versões, parâmetros, prompts e condições de execução;
5. disponibilizar fontes, evidências e respostas para auditoria documental, respeitadas as restrições aplicáveis;
6. estabelecer método prévio para distinguir fatos, inferências, hipóteses e conhecimento externo;
7. definir critérios de avaliação antes da observação dos resultados;
8. justificar amostra, cenários, criticidades e modelos comparados;
9. incluir revisão humana com competência adequada ao domínio;
10. prever tratamento de divergências, fontes não verificáveis e critérios quantitativos introduzidos pelas IAs;
11. separar avaliação da fundamentação, autorização da decisão, execução e validação do resultado;
12. impedir qualquer execução em ambiente crítico ou de produção sem governança própria e autorização independente;
13. registrar limitações, resultados negativos e hipóteses refutadas;
14. submeter qualquer proposta de métrica, integração, alteração de Harness ou engine a programa específico e aprovação separada;
15. definir previamente como o programa retornará ao estado congelado ou será encerrado.

O atendimento desses critérios não produz retomada automática. Ele apenas permite que uma proposta seja submetida à decisão humana competente.

## 16. Declaração final de não normatividade

Este documento:

* registra uma pesquisa experimental congelada;
* não altera a Constituição do ICFACTORY;
* não altera a arquitetura ou o código do PROTEUS;
* não modifica Harnesses;
* não cria índice, métrica, engine, processo ou artefato obrigatório;
* não promove conceitos experimentais a princípios oficiais;
* não comprova a hipótese principal ou as hipóteses derivadas;
* não autoriza implementação, integração, execução ou aplicação em decisões críticas;
* não atribui autoridade decisória à IA.

> **PESQUISA EXPERIMENTAL — NÃO NORMATIVA — ESTADO CONGELADO**

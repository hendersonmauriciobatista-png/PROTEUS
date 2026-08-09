# GP-ARQ-01 — Gate de Autoridade

> **PESQUISA ARQUITETURAL E EXPERIMENTAL — NÃO NORMATIVA — SEM AUTORIDADE OPERACIONAL**

## 1. Identificação

| Campo | Registro |
| --- | --- |
| Identificador | GP-ARQ-01 |
| Título | Gate de Autoridade |
| Natureza | Pesquisa arquitetural e experimental |
| Estado | Proposta documentada |
| Autoridade normativa | Nenhuma |
| Efeito sobre a Constituição | Nenhum |
| Efeito sobre a baseline | Nenhum |
| Implementação | Não autorizada nesta etapa |
| Dependências operacionais | Nenhuma |
| Data do registro | 27/07/2026 |

Este documento define uma proposta conceitual para governar o conhecimento produzido em execuções do ICFACTORY. Ele não institui um componente operacional, não altera regras vigentes e não promove automaticamente seus conceitos à Constituição, à baseline ou ao conhecimento institucional.

## 2. Objetivo do Gate de Autoridade

### 2.1 Finalidade

O Gate de Autoridade é proposto como um componente arquitetural independente, posterior à formação do Pacote de Evidências, destinado a examinar a sustentação de conclusões antes de eventual promoção ao Conhecimento Institucional.

Sua finalidade é impedir que uma afirmação adquira status institucional apenas por ter sido produzida por um executor, por constar de um entregável ou por parecer tecnicamente plausível.

### 2.2 Responsabilidades

No modelo experimental, o Gate:

* verifica proveniência, evidências e relações entre premissas, inferências e conclusões;
* classifica a natureza epistemológica das conclusões;
* avalia o nível de confiança com base em critérios explícitos;
* registra uma decisão classificatória rastreável;
* preserva limitações, divergências, ressalvas e lacunas;
* encaminha somente conclusões elegíveis para eventual promoção por autoridade competente;
* mantém registro suficiente para auditoria e reavaliação.

### 2.3 Limites

O Gate:

* não governa a execução da OG;
* não altera escopo, restrições, critérios de aceitação ou entregáveis;
* não substitui aprovação humana nem autoridade constitucional;
* não confere autoridade ao executor, inclusive quando este for uma IA;
* não valida automaticamente a veracidade de uma conclusão;
* não transforma evidência insuficiente em conhecimento institucional;
* não altera artefatos de origem nem o Pacote de Evidências;
* não executa ações, modifica código ou cria efeitos operacionais;
* não modifica Constituição, baseline, OGs, Harnesses ou fluxos atuais;
* não cria uma camada soberana ou paralela de governança.

Neste documento, **Decisão de Autoridade** significa a decisão classificatória do Gate sobre a elegibilidade epistemológica de uma conclusão. Não significa autoridade estratégica, constitucional ou operacional. Qualquer promoção efetiva permanece dependente da autoridade humana competente e dos mecanismos vigentes.

### 2.4 Integração com o ICFACTORY

O Gate é uma fronteira conceitual entre o produto auditável de uma execução e o conhecimento que pode vir a ser reconhecido institucionalmente. Sua integração é definida somente por contratos documentais: recebe um Pacote de Evidências e produz um Registro de Avaliação do Gate. Não há API, serviço, banco de dados, automação ou acoplamento obrigatório nesta etapa.

## 3. Arquitetura conceitual

```text
Usuário
  ↓
OG (Ordem de Governança)
  ↓
Executor
(Codex / GPT / Gemini / Claude / Humano)
  ↓
Artefatos
  ↓
Pacote de Evidências
  ↓
Gate de Autoridade
  ↓
Conhecimento Institucional
```

### 3.1 Leitura do fluxo

1. O **Usuário** apresenta a intenção e atua dentro da cadeia de autoridade aplicável.
2. A **OG** governa a execução, delimitando escopo, restrições, critérios de aceitação e entregáveis.
3. O **Executor** realiza a atividade autorizada; sua identidade ou modelo não lhe concede autoridade institucional.
4. Os **Artefatos** materializam o trabalho produzido.
5. O **Pacote de Evidências** reúne referências verificáveis, proveniência, resultados e limitações necessários à avaliação.
6. O **Gate de Autoridade** avalia e classifica as conclusões sem reexecutar nem governar a OG.
7. O **Conhecimento Institucional** recebe somente o que for elegível e efetivamente promovido pela autoridade competente.

As setas representam relações conceituais de encaminhamento, não integrações já implementadas. A ausência, insuficiência ou inconsistência do Pacote de Evidências impede promoção automática.

## 4. Contratos conceituais de entrada e saída

### 4.1 Entrada: Pacote de Evidências

Um futuro ensaio controlado deveria identificar, no mínimo:

| Elemento | Finalidade |
| --- | --- |
| OG de origem | Rastrear autorização, escopo e critérios da execução |
| Executor | Identificar quem ou o que produziu os artefatos |
| Artefatos avaliados | Delimitar o objeto material da análise |
| Fontes e proveniência | Permitir exame independente da origem |
| Evidências | Sustentar premissas e conclusões |
| Premissas declaradas | Expor bases usadas na análise |
| Inferências | Explicitar relações derivadas |
| Limitações e incertezas | Impedir confiança indevida |
| Resultados de verificação | Registrar testes ou exames realizados |
| Temporalidade | Indicar data, versão e possível expiração |

Estes campos são candidatos de pesquisa, não um schema obrigatório da baseline.

### 4.2 Saída: Registro de Avaliação do Gate

Uma saída conceitual deveria conter:

* identificador da avaliação;
* referência inequívoca ao Pacote de Evidências;
* conclusão avaliada;
* classificação da conclusão;
* nível de confiança e sua justificativa;
* decisão do Gate;
* evidências favoráveis, contrárias e ausentes;
* premissas e inferências determinantes;
* ressalvas, validade temporal e condições de reavaliação;
* identidade do avaliador e da autoridade humana responsável;
* data, versão e trilha de auditoria.

O registro não altera o material avaliado e não produz promoção por si só.

## 5. Componentes internos

Os componentes abaixo são responsabilidades lógicas. Não representam módulos de software existentes nem autorizam implementação.

### 5.1 Verificação de Proveniência

Confirma se a origem de artefatos, fontes, evidências, premissas e atos de autoridade está identificada, versionada, datada e vinculada ao objeto avaliado. Proveniência demonstra rastreabilidade; não cria competência nem legitima automaticamente a fonte.

### 5.2 Verificação de Evidências

Examina relevância, suficiência, integridade, atualidade, independência e possibilidade de verificação das evidências. Registra contradições e ausências sem preenchê-las por suposição.

### 5.3 Validação das Premissas

Identifica premissas explícitas e implícitas, verifica seu suporte e registra as que forem contestadas, condicionais, expiradas ou não verificáveis.

### 5.4 Validação das Inferências

Examina se cada passagem das premissas à conclusão é explícita e sustentada. Correlação, plausibilidade e concordância entre agentes não são tratadas automaticamente como causalidade ou confirmação.

### 5.5 Consistência Lógica

Procura contradições internas, circularidade, incompatibilidade entre conclusões e evidências, generalização indevida e omissão de alternativas materialmente relevantes.

### 5.6 Classificação das Conclusões

Atribui uma das categorias definidas na seção 7, preservando classificações distintas quando uma conclusão composta contiver afirmações de naturezas diferentes.

### 5.7 Avaliação do Nível de Confiança

Registra confiança de maneira justificada e revisável. Nesta pesquisa, o nível é qualitativo — **baixo**, **moderado** ou **alto** — e não possui fórmula, peso ou limiar oficial.

O nível de confiança:

* é relativo à conclusão, ao pacote e ao momento avaliados;
* não mede a reputação do executor ou do modelo;
* não substitui a classificação epistemológica;
* não converte inferência ou hipótese em fato;
* deve diminuir ou permanecer indeterminado quando evidências críticas estiverem ausentes.

### 5.8 Decisão de Autoridade

Consolida a avaliação em uma das decisões da seção 8. A decisão deve apontar seus fundamentos e a autoridade humana competente para qualquer efeito institucional. O nome deste componente não lhe concede soberania própria.

### 5.9 Registro para Auditoria

Preserva entradas, critérios, classificações, decisões, versões, responsáveis, divergências e reavaliações. O registro deve permitir reconstruir o que foi avaliado, com quais evidências, por quem, quando e por que determinada decisão foi proposta.

## 6. Integração com as OGs

### 6.1 Responsabilidade preservada da OG

A OG continua integralmente responsável por:

* governança da execução;
* escopo;
* restrições;
* critérios de aceitação;
* entregáveis.

O encerramento ou a aceitação de uma OG não equivale à promoção automática de todas as afirmações contidas em seus entregáveis.

### 6.2 Responsabilidade proposta para o Gate

O Gate passa a ser conceitualmente responsável por:

* governança do conhecimento produzido;
* classificação das conclusões;
* avaliação da elegibilidade para promoção do conhecimento institucional.

Neste estágio experimental, “passa a ser responsável” descreve a divisão pretendida no modelo, não uma transferência vigente de competência. A promoção efetiva permanece um ato da autoridade competente.

### 6.3 Separação de responsabilidades

| Questão | OG | Gate de Autoridade |
| --- | --- | --- |
| A execução foi autorizada e permaneceu no escopo? | Responsável | Usa o registro como entrada |
| Restrições e critérios de aceitação foram cumpridos? | Responsável | Não redefine |
| Entregáveis foram produzidos? | Responsável | Identifica os que serão avaliados |
| As conclusões têm suporte suficiente? | Fornece evidências | Avalia |
| Qual é a natureza de cada conclusão? | Pode declarar | Classifica |
| A conclusão é elegível à promoção? | Não promove por mera aceitação | Emite decisão classificatória |
| Quem produz efeito institucional? | Autoridade vigente, quando aplicável | Nunca autonomamente |

Essa separação evita interferência nos fluxos existentes e impede que governança da execução seja confundida com governança do conhecimento.

## 7. Classificação das conclusões

As categorias são mutuamente preferenciais para cada afirmação atômica. Se uma conclusão reunir proposições diferentes, ela deve ser decomposta antes da classificação.

| Categoria | Definição experimental | Condição típica |
| --- | --- | --- |
| **Fato Confirmado** | Afirmação diretamente sustentada por evidência verificável, suficiente e aplicável ao escopo declarado | Origem rastreável, exame reproduzível e ausência de contradição material não resolvida |
| **Inferência** | Conclusão derivada de fatos ou premissas por relação lógica explicitada | Cadeia inferencial visível, mas conclusão não diretamente observada |
| **Hipótese** | Proposição testável ainda sem confirmação suficiente | Requer experimento, observação ou evidência adicional |
| **Estimativa** | Aproximação quantitativa ou qualitativa dependente de método, dados e incerteza declarados | Premissas, faixa, método e validade temporal registrados |
| **Opinião Técnica** | Juízo profissional fundamentado, dependente de interpretação ou experiência identificada | Autor, competência, fundamento e alternativas explicitados |
| **Não Verificado** | Afirmação para a qual a verificação necessária não ocorreu ou não pôde ser demonstrada | Evidência ausente, inacessível, insuficiente ou não rastreável |

Regras de segurança classificatória:

* autoria humana ou por IA não determina a categoria;
* repetição por múltiplos agentes não converte uma afirmação em fato;
* confiança alta não altera a natureza epistemológica da conclusão;
* na dúvida material entre categorias, aplica-se a categoria menos afirmativa e registra-se a pendência;
* “Fato Confirmado” é limitado ao escopo, versão e temporalidade das evidências avaliadas.

## 8. Decisões do Gate

| Decisão | Significado experimental | Efeito permitido nesta etapa |
| --- | --- | --- |
| **Promover** | A conclusão é considerada elegível para submissão à autoridade competente | Registrar recomendação; nunca promover automaticamente |
| **Manter como Hipótese** | Há plausibilidade, mas não suporte suficiente para reconhecimento mais forte | Preservar como item experimental, com condições de teste |
| **Solicitar Evidências Adicionais** | A avaliação não pode ser concluída por lacuna material identificada | Registrar exatamente quais evidências são necessárias |
| **Rejeitar** | A conclusão é contradita, logicamente inconsistente, fora de escopo ou insustentável pelo pacote | Impedir recomendação de promoção e registrar fundamento |

“Rejeitar” não apaga o registro nem censura o artefato original; preserva-se a trilha para auditoria. “Promover” é condição necessária proposta, mas não suficiente, para ingresso no Conhecimento Institucional.

## 9. Regras conceituais de decisão

1. Cada decisão deve ser vinculada a uma conclusão atômica.
2. Toda decisão deve possuir justificativa verificável.
3. Evidência crítica ausente impede a decisão **Promover**.
4. Contradição material não resolvida impede a decisão **Promover**.
5. Classificação e confiança devem ser registradas separadamente.
6. Opiniões minoritárias e evidências contrárias materiais devem permanecer visíveis.
7. Mudança de fonte, versão, escopo ou temporalidade pode exigir reavaliação.
8. Nenhuma decisão do Gate autoriza execução ou modifica uma OG.
9. Nenhum executor pode adquirir autoridade em razão da qualidade aparente de sua resposta.
10. A promoção efetiva exige ato explícito da autoridade humana competente.

## 10. Registro e rastreabilidade

A cadeia mínima pretendida é:

```text
GP-ARQ-01
  → OG de origem
  → Executor identificado
  → Artefato versionado
  → Evidência referenciada
  → Premissa / Inferência
  → Conclusão atômica
  → Classificação + Confiança
  → Decisão do Gate
  → Ato humano de promoção, se autorizado
  → Registro no Conhecimento Institucional
```

Cada elo deve manter identificadores estáveis ou referências inequívocas. Correções e reavaliações devem acrescentar novos registros ou versões, preservando a decisão anterior e sua temporalidade.

## 11. Benefícios esperados

Como hipóteses de benefício a validar, a arquitetura pode contribuir para:

* redução da promoção de informações sem evidência;
* aumento da rastreabilidade;
* aumento da auditabilidade;
* independência em relação ao modelo de IA utilizado;
* compatibilidade com múltiplos agentes.

Benefícios adicionais plausíveis incluem melhor distinção entre aceitação de entregáveis e validação de conhecimento, maior visibilidade de incertezas e possibilidade de reavaliação sem repetir toda a execução. Nenhum benefício é declarado como comprovado nesta etapa.

## 12. Compatibilidade com a baseline

Esta proposta foi delimitada para coexistir com a baseline vigente sem modificá-la:

* preserva a Constituição ICFACTORY e o princípio de que inteligência não é autoridade;
* mantém a autoridade estratégica na camada de governança definida pela arquitetura;
* trata o Gate como camada informativa e classificatória, sem autoridade operacional;
* preserva integralmente OGs, Harnesses e fluxos existentes;
* não altera contratos, código, dados, serviços ou funcionalidades;
* não cria obrigação para projetos atuais;
* não promove categorias, decisões ou componentes ao léxico constitucional;
* não reivindica precedência sobre documentos normativos.

Referências de compatibilidade examinadas:

* [Constituição ICFACTORY](https://github.com/hendersonmauriciobatista-png/icfactory-framework/blob/main/CONSTITUTION.md), versão 0.2, status ATIVA;
* [Governance Architecture](https://github.com/hendersonmauriciobatista-png/icfactory-framework/blob/main/governance/GOVERNANCE_ARCHITECTURE.md), versão 1.0, status FUNDACIONAL;
* [Project Constitution Template](https://github.com/hendersonmauriciobatista-png/icfactory-framework/blob/main/governance/PROJECT_CONSTITUTION_TEMPLATE.md), versão 0.5, baseline documental oficial aprovada;
* [Constitutional Lexicon](https://github.com/hendersonmauriciobatista-png/icfactory-framework/blob/main/CONSTITUTIONAL_LEXICON.md).

Em caso de conflito interpretativo, prevalecem a Constituição, a baseline e as autoridades vigentes. A GP-ARQ-01 deverá ser corrigida ou rejeitada; ela não pode reinterpretar a baseline para adquirir competência.

## 13. Impactos

### 13.1 Impacto atual

O impacto atual é exclusivamente documental:

* um dossiê arquitetural experimental adicionado;
* nenhuma alteração funcional;
* nenhuma alteração em OG;
* nenhuma alteração em Harness;
* nenhuma alteração de fluxo;
* nenhuma dependência operacional;
* nenhuma promoção de conhecimento institucional.

### 13.2 Impacto futuro potencial

Qualquer protótipo, ensaio, integração, template obrigatório, alteração de OG ou mecanismo de promoção exigirá iniciativa separada, escopo próprio, análise de impacto, critérios de aceitação e autorização humana explícita.

## 14. Riscos

| Risco | Consequência | Tratamento arquitetural proposto |
| --- | --- | --- |
| O Gate ser interpretado como autoridade soberana | Governança paralela | Subordinação explícita à Constituição e à autoridade humana |
| “Promover” ser automatizado | Entrada indevida no conhecimento institucional | Separar elegibilidade da promoção efetiva |
| Forma documental ser confundida com evidência | Falsa confiança | Verificar suficiência, origem e aplicabilidade |
| Consenso entre agentes ser confundido com confirmação | Erro amplificado | Classificar pela evidência, não por votação |
| Viés ou erro do avaliador | Classificação inconsistente | Registrar critérios, identidade, divergências e revisão |
| Métrica de confiança gerar precisão artificial | Decisões excessivamente afirmativas | Manter escala qualitativa e justificativa explícita |
| Evidência expirar | Conhecimento desatualizado | Registrar temporalidade e gatilhos de reavaliação |
| Custo documental excessivo | Adoção inadequada | Testar proporcionalidade em pesquisa futura |
| Acoplamento às OGs | Alteração indireta de fluxos atuais | Usar somente contratos documentais e adesão futura autorizada |
| Terminologia colidir com o léxico constitucional | Ambiguidade de autoridade | Manter definições experimentais e vedar efeito normativo |

## 15. Recomendações

1. Manter a GP-ARQ-01 como pesquisa não normativa até validação específica.
2. Submeter a terminologia “Gate de Autoridade” e “Decisão de Autoridade” a revisão constitucional antes de qualquer promoção.
3. Em futura fase experimental, testar o modelo somente com cópias controladas de Pacotes de Evidências, sem integração aos fluxos vigentes.
4. Pré-registrar critérios de classificação e decisão antes dos ensaios.
5. Comparar avaliações cegas realizadas por agentes e humanos diferentes.
6. Medir concordância, falsos positivos de promoção, falsos negativos e custo de auditoria.
7. Definir processo humano explícito para promoção, contestação, revisão e expiração.
8. Tratar qualquer automação, schema obrigatório ou integração como projeto separado.
9. Não atualizar Constituição, baseline, OGs, Harnesses, `HISTORY.md` ou `ROADMAP.md` com efeitos normativos em decorrência desta pesquisa.

## 16. Plano experimental futuro não autorizado

Uma etapa posterior, se expressamente autorizada, poderia:

1. selecionar artefatos históricos sem efeito operacional;
2. montar Pacotes de Evidências controlados;
3. decompor conclusões em afirmações atômicas;
4. aplicar as categorias e decisões propostas;
5. comparar avaliações independentes;
6. auditar divergências e causas;
7. medir benefícios e riscos;
8. encerrar o ensaio sem promover resultados automaticamente.

Esta seção não autoriza execução, implementação ou uso em produção.

## 17. Auditoria da GP-ARQ-01

### 17.1 Arquivos criados

* `docs/research/GP_ARQ_01_AUTHORITY_GATE_ARCHITECTURAL_RESEARCH.md`

### 17.2 Arquivos alterados

* Nenhum arquivo preexistente foi alterado por esta GP.

`HISTORY.md` e `ROADMAP.md` não foram atualizados porque o registro autossuficiente neste dossiê fornece rastreabilidade suficiente e evita interferência em arquivos com alterações preexistentes. Uma eventual indexação deverá ocorrer em ação documental separada e autorizada.

### 17.3 Resumo arquitetural

Foi definido um Gate conceitual entre o Pacote de Evidências e o Conhecimento Institucional. O componente examina proveniência, evidências, premissas, inferências e consistência; classifica conclusões; avalia confiança; e registra uma decisão classificatória auditável. A OG continua governando a execução, e a autoridade humana vigente continua responsável por qualquer promoção efetiva.

### 17.4 Compatibilidade com a baseline

Compatível por construção documental: a proposta não altera a baseline, não cria autoridade operacional, não substitui governança existente e respeita a separação entre inteligência, observação e autoridade.

### 17.5 Impactos

Somente a criação deste documento de pesquisa. Não há impacto em comportamento, interfaces, dados, dependências, execução ou funcionalidades.

### 17.6 Riscos

Os principais riscos são ambiguidade do termo autoridade, promoção automática indevida, confiança artificial, viés de avaliação e acoplamento futuro às OGs. Todos permanecem riscos de pesquisa, com salvaguardas documentadas nas seções 14 e 15.

### 17.7 Recomendações

Manter o estado experimental, realizar revisão constitucional da terminologia antes de qualquer evolução e exigir uma GP separada para protótipo, ensaio operacional ou promoção normativa.

## 18. Verificação dos critérios de aceitação

| Critério | Evidência de atendimento |
| --- | --- |
| Nenhuma funcionalidade existente alterada | A GP cria somente este arquivo Markdown |
| Nenhuma OG existente modificada | Nenhum documento ou mecanismo de OG foi editado |
| Gate documentado como componente independente | Seções 2, 3, 5 e 6 |
| Toda alteração possui rastreabilidade | Seções 10 e 17 |
| Compatibilidade com a baseline vigente | Seção 12 |
| Pesquisa experimental sem promoção constitucional automática | Identificação, limites e declaração final |

## 19. Declaração final

A GP-ARQ-01 documenta uma hipótese arquitetural. Ela:

* não altera a Constituição do ICFACTORY;
* não altera a baseline;
* não modifica OGs ou Harnesses;
* não altera fluxos, código-fonte, dados ou funcionalidades;
* não cria dependências operacionais;
* não institui o Gate como componente em produção;
* não atribui autoridade operacional a IA, humano executor ou mecanismo automático;
* não promove automaticamente conclusões ou conceitos ao Conhecimento Institucional;
* não produz obrigação normativa.

> **PESQUISA ARQUITETURAL E EXPERIMENTAL — NÃO NORMATIVA — SEM PROMOÇÃO AUTOMÁTICA**

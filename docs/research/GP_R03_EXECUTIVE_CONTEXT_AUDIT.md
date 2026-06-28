# GP-R03 - Investigacao Arquitetural: Executive Context

Data: 28/06/2026

Status: PESQUISA ARQUITETURAL CONCLUIDA

Natureza: Research

## Hipotese Investigada

O `ExecutiveRecommendationService` pode estar assumindo responsabilidade de consolidacao contextual que deveria pertencer a uma camada anterior chamada `ExecutiveContext`.

## Pergunta Central

Existe uma responsabilidade arquitetural distinta entre:

1. consolidar o contexto executivo da situacao; e
2. transformar esse contexto em recomendacao?

## Escopo

Cadeia auditada:

```text
Resultado Observacional
  |
Analytics
  |
Governanca
  |
ExecutiveRecommendationService
  |
ExecutiveIntelligenceService
  |
Painel Executivo
```

Arquivos auditados:

* `executive_recommendation/models.py`
* `executive_recommendation/rules.py`
* `executive_recommendation/service.py`
* `executive/service.py`
* `executive/models.py`
* `executive/rules.py`
* `docs/architecture/EXECUTIVE_INTELLIGENCE_ARCHITECTURE.md`
* `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`

Restricoes desta pesquisa:

* Nenhum codigo funcional alterado.
* Nenhum runtime alterado.
* Nenhuma interface alterada.
* Nenhum documento constitucional ICFACTORY alterado.
* Nenhuma Discovery promovida.
* PA-02 permanece apenas Discovery candidata.
* Regras de recomendacao existentes nao foram alteradas.

## Metodo

A auditoria foi passiva e documental.

Foram observados:

* entradas atuais do `ExecutiveRecommendationService`;
* transformacoes internas realizadas antes da recomendacao;
* diferenca entre contexto, regra executiva, recomendacao e apresentacao;
* aderencia ao PA-01;
* aderencia ou tensao com a hipotese PA-02 investigada na GP-R02;
* risco de complexidade adicional desnecessaria.

## Cadeia Auditada

### Resultado Observacional

O resultado observacional pertence ao Nucleo de Monitoramento Hidrico. A arquitetura vigente preserva PA-01: `PolicyEngine` seleciona politicas e motores especializados executam avaliacoes.

Na cadeia executiva, resultados observacionais chegam indiretamente por Analytics e Governanca, ou como `observational_result` opcional no `ExecutiveRecommendationService`.

### Analytics

Analytics produz `AnalyticsSnapshot`, contendo:

* tendencias de qualidade;
* tendencias de consumo;
* alertas preventivos;
* Water Health Score.

Essa camada ja agrega interpretacao analitica e nao deve emitir recomendacao executiva final.

### Governanca

Governanca produz eventos e resumo por estado. Ela acompanha ciclo de vida operacional e preserva metadados de rastreabilidade quando disponiveis.

Na integracao atual, `ExecutiveIntelligenceService` passa para recomendacao apenas o resumo de governanca, nao a lista completa de eventos.

### ExecutiveRecommendationService

O servico atual:

* recebe `analytics_snapshot`, `governance_snapshot` e `observational_result`;
* extrai Water Health Score;
* normaliza acesso a objetos ou dicionarios por `_read_field`;
* transforma score ausente em incerteza;
* constroi evidencias textuais;
* chama regra deterministica de recomendacao;
* produz `RecommendationSnapshot`.

Isso mostra que o servico recomenda, mas tambem executa uma consolidacao contextual minima: seleciona o sinal principal, interpreta ausencia de sinal e monta evidencias.

### ExecutiveIntelligenceService

O `ExecutiveIntelligenceService` ja exerce parte da sintese executiva:

* orquestra Analytics e Governanca;
* classifica status executivo por `ExecutiveRules`;
* seleciona alertas relevantes;
* seleciona tendencias-chave;
* cria prioridades observacionais;
* chama `ExecutiveRecommendationService`;
* compoe `ExecutiveSnapshot`.

Ele consolida estado executivo geral, mas nao possui um artefato dedicado chamado `ExecutiveContext`.

### Painel Executivo

O Painel Executivo apenas apresenta o snapshot consolidado. Ele nao recalcula recomendacoes, contexto, score, governanca ou status observacional.

## Matriz De Responsabilidades Atual

| Responsabilidade | Camada atual | Observacao |
| ---------------- | ------------ | ---------- |
| Selecionar politica observacional | Nucleo / PolicyEngine | PA-01 preservado |
| Executar avaliacao observacional | Nucleo / motor especializado | PA-01 preservado |
| Calcular tendencias | Analytics | Nao deve migrar para Recommendation |
| Calcular Water Health Score | Analytics | Recommendation apenas consome |
| Criar alertas preventivos | Analytics | Recommendation pode referenciar, nao recalcular |
| Criar e acompanhar eventos | Governanca | Recommendation nao deve alterar estado |
| Resumir eventos por estado | Governanca / ExecutiveIntelligenceService | Hoje chega a Recommendation como dicionario |
| Selecionar alertas e tendencias executivas | ExecutiveRules | Ja e sintese executiva parcial |
| Consolidar sinais em contexto recomendavel | Parcialmente ausente | Hoje espalhado entre ExecutiveIntelligenceService e ExecutiveRecommendationService |
| Extrair score para recomendacao | ExecutiveRecommendationService | Sinal de responsabilidade contextual minima |
| Construir evidencias da recomendacao | ExecutiveRecommendationService | Pode pertencer a ExecutiveContext futuro |
| Decidir prioridade e acao recomendada | ExecutiveRecommendationRules | Responsabilidade legitima de Recommendation |
| Apresentar recomendacoes | Painel Executivo | Apenas apresentacao |

## Perguntas Obrigatorias

### 1. O ExecutiveRecommendationService apenas recomenda ou tambem consolida contexto?

Ele recomenda e tambem consolida contexto de forma minima.

Evidencias:

* `_extract_water_health_score()` seleciona e normaliza o sinal usado pela regra.
* `_build_evidence()` monta evidencias a partir de Analytics, Governanca e resultado observacional.
* `build_snapshot()` aceita tres fontes de entrada e decide como representa-las no `RecommendationSnapshot`.

### 2. Quais sinais ele recebe hoje?

Entradas atuais:

* `analytics_snapshot`;
* `governance_snapshot`;
* `observational_result`.

Na integracao GP-A22C, ele recebe:

* `AnalyticsSnapshot` produzido por `AnalyticsService`;
* resumo de governanca produzido por `OperationalGovernanceService.summarize_by_state()`;
* `observational_result=None`.

### 3. Esses sinais chegam crus demais para uma camada de recomendacao?

Parcialmente.

Para a regra v1 baseada apenas em Water Health Score, os sinais nao estao crus demais. O servico consegue extrair o score sem grande custo arquitetural.

Para recomendacoes futuras com multiplos sinais, horizontes, confianca, agrupamento, owners, rastreabilidade e correlacao de eventos, as entradas atuais sao cruas ou heterogeneas demais. Nessa evolucao, um contexto executivo dedicado reduziria acoplamento e evitaria que Recommendation virasse uma camada de preparacao de dados.

### 4. Existe uma etapa conceitual faltante entre Governanca/Analytics e Recommendation?

Sim, como hipotese futura.

A etapa faltante seria a consolidacao de um contexto recomendavel, contendo sinais ja selecionados, normalizados, correlacionados e explicados. Hoje essa responsabilidade esta pequena e distribuida entre `ExecutiveIntelligenceService`, `ExecutiveRules` e `ExecutiveRecommendationService`.

### 5. O que seria responsabilidade de ExecutiveContext?

Responsabilidades candidatas:

* Consolidar `AnalyticsSnapshot`, resumo/lista de eventos de Governanca e metadados observacionais disponiveis.
* Normalizar sinais heterogeneos em uma estrutura executiva comum.
* Separar sinais disponiveis, ausentes e insuficientes.
* Construir evidencias rastreaveis sem decidir a acao recomendada.
* Correlacionar sinais relacionados, quando houver regra explicita futura.
* Declarar nivel de completude do contexto.
* Preparar dados para recomendacao, sem selecionar politica, executar avaliacao observacional, recalcular score, recalcular tendencias ou alterar eventos.

### 6. O que continuaria sendo responsabilidade de ExecutiveRecommendationService?

Responsabilidades que devem permanecer em Recommendation:

* Consumir contexto executivo ja consolidado.
* Aplicar regras deterministicas de recomendacao.
* Definir prioridade da recomendacao.
* Definir acao recomendada.
* Gerar `RecommendationSnapshot`.
* Tratar incerteza do contexto como recomendacao controlada, sem inferencia silenciosa.

### 7. A criacao futura de ExecutiveContext preservaria o PA-01?

Sim, se respeitar limites claros.

ExecutiveContext preservaria PA-01 se:

* nao selecionar politica;
* nao executar avaliacao observacional;
* nao recalcular status observacional;
* nao recalcular Water Health Score;
* nao recalcular tendencias;
* nao criar ou transicionar eventos;
* apenas consolidar sinais autorizados de Analytics, Governanca e resultados observacionais ja produzidos.

### 8. A criacao futura de ExecutiveContext reforcaria ou enfraqueceria a hipotese PA-02?

Reforcaria, desde que criada por necessidade real.

Pela leitura da GP-R02, PA-02 candidata trata de progressao de valor entre camadas. Um ExecutiveContext poderia reforcar essa progressao:

```text
Sinais analiticos/governados
  |
Contexto executivo consolidado
  |
Recomendacao executiva
  |
Apresentacao executiva
```

O risco e enfraquecer PA-02 por excesso de granularidade: criar uma camada que nao agrega valor suficiente, apenas repassa dados, seria uma falsa progressao.

### 9. Existem riscos de overengineering?

Sim.

Riscos principais:

* A recomendacao v1 usa apenas Water Health Score; criar ExecutiveContext agora pode ser mais estrutura do que necessidade.
* `ExecutiveIntelligenceService` ja consolida parte do estado executivo.
* `ExecutiveRules` ja seleciona sinais relevantes e tendencias-chave.
* Uma nova camada sem responsabilidade forte poderia duplicar sintese executiva.
* O sistema ainda nao tem recomendacoes correlacionadas, confianca formal ou multiplas recomendacoes por dominio.

### 10. Existem evidencias suficientes para tratar ExecutiveContext como Discovery candidata?

Sim, mas nao como implementacao imediata.

As evidencias sao suficientes para tratar ExecutiveContext como Discovery candidata porque:

* a arquitetura ja reconhece diferenca entre sinais, prioridades, recomendacoes e apresentacao;
* `ExecutiveRecommendationService` ja executa pequena preparacao contextual;
* GP-R02 identificou progressao de valor como hipotese candidata;
* futuras recomendacoes exigirao evidencias, rastreabilidade, agrupamento e completude de contexto.

As evidencias ainda nao justificam criar codigo agora.

## Evidencias A Favor

1. O blueprint GP-A22A ja separa recomendacao executiva de observacao, analytics, governanca e painel.

2. O `ExecutiveRecommendationService` recebe multiplas fontes, nao apenas um contexto pronto.

3. O servico atual contem metodos de extracao e construcao de evidencias, que sao atividades proximas de consolidacao contextual.

4. A arquitetura futura desejada menciona evidencias, rastreabilidade, agrupamento de sinais, explicabilidade e horizonte sugerido.

5. GP-R02 concluiu que existe progressao de valor entre camadas como Discovery candidata; ExecutiveContext seria uma possivel camada intermediaria dessa progressao.

## Evidencias Contra

1. A recomendacao v1 e simples e baseada apenas em Water Health Score.

2. `ExecutiveIntelligenceService` ja compoe um `ExecutiveSnapshot` e seleciona alertas/tendencias/prioridades via `ExecutiveRules`.

3. Criar ExecutiveContext agora poderia duplicar responsabilidades de `ExecutiveRules` ou `ExecutiveIntelligenceService`.

4. Nao ha ainda multiplas recomendacoes correlacionadas, regras de confianca, owners operacionais ou horizontes de acao implementados.

5. O custo conceitual de uma nova camada pode superar o beneficio no estado atual.

## Riscos

### Risco 1 - Duplicar Executive Intelligence

Se ExecutiveContext classificar status executivo, selecionar prioridades ou montar mensagem executiva, ele duplicara `ExecutiveRules` e `ExecutiveIntelligenceService`.

Mitigacao:

ExecutiveContext deve preparar contexto recomendavel, nao classificar status executivo geral.

### Risco 2 - Duplicar Analytics

Se ExecutiveContext recalcular tendencias, score ou alertas, ele violara responsabilidades de Analytics.

Mitigacao:

ExecutiveContext deve consumir resultados analiticos prontos.

### Risco 3 - Duplicar Governanca

Se ExecutiveContext criar estados, alterar eventos ou deduplicar ocorrencias, ele enfraquecera Governanca.

Mitigacao:

ExecutiveContext deve ler eventos/resumos consolidados, sem governar ciclo de vida.

### Risco 4 - Criar autoridade observacional paralela

Se ExecutiveContext avaliar parametros hidricos, selecionar politicas ou reinterpretar status observacional, PA-01 sera violado.

Mitigacao:

ExecutiveContext deve tratar resultados observacionais como entradas imutaveis.

### Risco 5 - Overengineering

Se criado antes de haver multiplos sinais recomendaveis, ExecutiveContext pode ser apenas um wrapper sem valor.

Mitigacao:

Adiar implementacao ate existir pelo menos uma GP com recomendacoes multi-sinal, confianca formal ou rastreabilidade ampliada.

## Impacto Sobre PA-01

ExecutiveContext poderia preservar PA-01 e ate reforca-lo, desde que sua responsabilidade seja apenas consolidar contexto.

Limites obrigatorios para uma eventual camada futura:

* nao acessar CSV diretamente;
* nao acessar `PolicyEngine`;
* nao acessar `AvaliacaoObservacionalService`;
* nao acessar diretamente o Nucleo de Monitoramento Hidrico;
* nao recalcular status observacional;
* nao recalcular tendencias;
* nao recalcular Water Health Score;
* nao criar ou alterar eventos de Governanca;
* nao emitir recomendacao final.

## Impacto Sobre PA-02 Candidata

ExecutiveContext reforcaria PA-02 candidata se agregar valor real:

```text
Analytics/Governanca
  -> contexto executivo consolidado
  -> recomendacao executiva
  -> apresentacao
```

Mas enfraqueceria PA-02 se for criado como camada pass-through sem responsabilidade propria.

Conclusao sobre PA-02:

* PA-02 permanece Discovery candidata.
* GP-R03 nao promove PA-02.
* ExecutiveContext deve ser tratado como possivel exemplo futuro de PA-02, nao como prova definitiva.

## Proposta Conceitual Futura

Se uma GP futura decidir implementar ExecutiveContext, uma separacao possivel seria:

### ExecutiveContext

Entrada:

* `AnalyticsSnapshot`.
* eventos ou resumo de Governanca.
* metadados observacionais ja consolidados.
* sinais executivos ja selecionados, se aplicavel.

Saida:

* contexto executivo consolidado;
* evidencias normalizadas;
* sinais ausentes ou insuficientes;
* mapa de rastreabilidade;
* completude/confianca contextual, se houver regra definida.

Nao deve:

* recomendar acao;
* selecionar politica;
* avaliar parametro;
* recalcular score;
* recalcular tendencia;
* governar eventos.

### ExecutiveRecommendationService

Entrada:

* `ExecutiveContextSnapshot` ou equivalente.

Saida:

* `RecommendationSnapshot`.

Responsabilidade:

* aplicar regra deterministica;
* definir prioridade;
* definir acao recomendada;
* explicar recomendacao a partir do contexto recebido.

## Recomendacao Final

Registrar `ExecutiveContext` como Discovery candidata para pesquisa e desenho futuro, sem implementacao nesta etapa.

Recomendacao operacional:

* Nao criar camada agora.
* Aguardar uma GP futura em que recomendacoes deixem de depender apenas de Water Health Score.
* Reavaliar ExecutiveContext quando houver necessidade de recomendacoes multi-sinal, confianca, agrupamento, rastreabilidade ampliada ou contexto incompleto formalizado.

## Veredito

Hipotese suportada como Discovery candidata.

Racional:

* Existe responsabilidade arquitetural distinta entre consolidar contexto executivo e transformar esse contexto em recomendacao.
* O servico atual ja contem sinais pequenos dessa mistura de responsabilidades.
* A arquitetura ainda nao exige uma implementacao imediata.
* O risco de overengineering e real no estado atual.
* A eventual camada ExecutiveContext pode reforcar PA-01 e PA-02 candidata se tiver limites claros e valor proprio.

## Encerramento

GP-R03 conclui que `ExecutiveContext` e uma Discovery candidata plausivel.

Nenhum codigo funcional foi alterado.

Nenhum runtime foi alterado.

Nenhuma interface foi alterada.

Nenhum documento constitucional ICFACTORY foi alterado.

Nenhuma Discovery foi promovida.

PA-02 permanece apenas Discovery candidata.

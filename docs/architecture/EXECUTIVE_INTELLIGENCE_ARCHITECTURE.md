# GP-A22A - Arquitetura da Inteligencia Executiva Evolutiva

Data: 27/06/2026

Status: BLUEPRINT ARQUITETURAL - GP-A22B IMPLEMENTADA

## Contexto

A fila GP-A14 foi encerrada integralmente.

O Nucleo de Monitoramento Hidrico esta consolidado como autoridade observacional central para qualidade da agua. As integracoes GP-A16, GP-A20, GP-A19, GP-A21, GP-A17 e GP-A18 definiram quais modulos consomem avaliacao observacional e quais permanecem como coleta/contexto operacional.

A GP-A22A inaugura a nova fase do CASE-01: Inteligencia Executiva Evolutiva.

Esta etapa nao implementa codigo funcional. Ela define o blueprint para uma futura GP-A22B, focada em um mecanismo deterministico de recomendacoes executivas.

Atualizacao GP-A22B (28/06/2026): o pacote `executive_recommendation` foi criado com modelos proprios, regras deterministicas iniciais e `ExecutiveRecommendationService` isolado. A implementacao preserva o PA-01 ao consumir apenas sinais consolidados, sem acessar CSV, `PolicyEngine`, `AvaliacaoObservacionalService` ou diretamente o Nucleo de Monitoramento Hidrico.

## Auditoria Passiva

### Painel Executivo

Responsabilidade atual:

* Apresentar `ExecutiveSnapshot`.
* Exibir status executivo, Water Health Score, contagem de eventos por estado, prioridades observacionais, alertas e tendencias.
* Consumir `ExecutiveIntelligenceService`.
* Nao ler CSV diretamente.
* Nao executar avaliacao observacional hidrica.
* Nao selecionar politicas do Nucleo de Monitoramento Hidrico.

Dados exibidos:

* `executive_status`.
* `water_health_score`.
* `water_health_status`.
* `open_events`, `monitoring_events`, `resolved_events`.
* `observational_priorities`.
* `relevant_alerts`.
* `key_trends`.
* `executive_message`.
* `explanations`.

### Analytics

Responsabilidade atual:

* Ler dados operacionais por `AnalyticsRepository`.
* Calcular tendencias de qualidade e consumo.
* Gerar alertas preventivos.
* Calcular Water Health Score.
* Consumir o Nucleo de Monitoramento Hidrico para avaliacoes de qualidade da agua via adapter analitico.

Dados produzidos:

* `AnalyticsSnapshot`.
* `TrendResult`.
* `PreventiveAlert`.
* `WaterHealthScore`.

### Governanca Operacional

Responsabilidade atual:

* Sincronizar alertas analiticos como eventos operacionais.
* Gerenciar estados de evento: `ABERTO`, `MONITORAMENTO`, `RESOLVIDO`, `ARQUIVADO`.
* Persistir eventos operacionais.
* Preservar metadados de politica, status observacional, severidade observacional, origem do limite e explicabilidade quando disponiveis.

Dados produzidos:

* `OperationalEvent`.
* Resumo por estado.
* Historico de transicoes operacionais.

### Executive Intelligence

Responsabilidade atual:

* Orquestrar `AnalyticsService` e `OperationalGovernanceService`.
* Produzir `ExecutiveSnapshot`.
* Aplicar `ExecutiveRules` para status executivo, selecao de alertas relevantes, tendencias-chave e prioridades observacionais.

### Executive Rules

Responsabilidade atual:

* Classificar status executivo a partir de score, alertas, tendencias e eventos.
* Selecionar alertas relevantes por severidade.
* Selecionar tendencias de risco.
* Construir prioridades executivas.

Limite atual:

* As prioridades possuem recomendacoes simples herdadas de alertas/eventos ou mensagens padrao.
* Ainda nao existe uma camada dedicada para recomendacoes executivas evolutivas, agrupamento de acoes, justificativa estruturada ou ordenacao por impacto operacional.

## Perguntas Arquiteturais

### 1. O que o sistema ja observa?

O sistema observa:

* Medicoes de qualidade da agua.
* Dados ambientais.
* Consumo e distribuicao.
* Tendencias de qualidade.
* Tendencias de consumo.
* Alertas preventivos.
* Water Health Score.
* Eventos operacionais e seus estados.
* Metadados observacionais do Nucleo de Monitoramento Hidrico para qualidade da agua.

### 2. O que o sistema ja interpreta?

O sistema interpreta:

* Avaliacao observacional de qualidade da agua pelo Nucleo.
* Tendencias de subida, queda ou estabilidade em Analytics.
* Alertas preventivos a partir de tendencias, perdas, chuva e avaliacao observacional.
* Penalidades para Water Health Score.
* Severidade de alertas e eventos.
* Status executivo por `ExecutiveRules`.
* Prioridades observacionais basicas.

### 3. O que o sistema ja governa?

O sistema governa:

* Criacao e atualizacao de eventos operacionais a partir de alertas.
* Deduplicacao por fingerprint.
* Contagem de ocorrencias.
* Transicoes controladas entre estados.
* Registro de resolucao e arquivamento.
* Persistencia de metadados observacionais quando o alerta vem de qualidade da agua.

### 4. O que ainda falta para recomendar?

Falta:

* Modelo explicito de recomendacao executiva.
* Separacao entre prioridade observacional e recomendacao executiva.
* Agrupamento de sinais correlacionados.
* Classificacao de tipo de acao recomendada.
* Justificativa estruturada com evidencias de Analytics, Governanca e Nucleo.
* Horizonte sugerido de acao.
* Dono operacional sugerido, sem implementar usuarios/perfis ainda.
* Rastreabilidade da recomendacao ate seus sinais de origem.
* Regras para evitar recomendacoes repetidas, contraditorias ou sem evidencia.

### 5. Quais entradas o mecanismo de recomendacao deve receber?

O futuro `ExecutiveRecommendationService` deve receber:

* `AnalyticsSnapshot`.
* Lista de `OperationalEvent`.
* Resumo de eventos por estado.
* `ExecutiveSnapshot` ou dados equivalentes de status executivo.
* Alertas relevantes selecionados por `ExecutiveRules`.
* Tendencias-chave selecionadas por `ExecutiveRules`.
* Metadados observacionais disponiveis: `policy_id`, `policy_name`, `observational_status`, `observational_severity`, `limit_origin`, `technical_observations`, `explainability`.

Ele nao deve ler CSV diretamente.

### 6. Quais saidas ele deve produzir?

O futuro servico deve produzir recomendacoes executivas com campos como:

* identificador.
* nivel: baixo, medio, alto.
* dominio.
* tipo: acompanhar, verificar, priorizar, escalar, manter.
* titulo.
* justificativa.
* evidencias.
* acao_recomendada.
* fonte dos sinais.
* rastreabilidade para alertas/eventos/tendencias.
* explicabilidade.
* horizonte sugerido.
* restricoes ou observacoes.

Essas saidas devem alimentar o Painel Executivo, sem substituir eventos de Governanca.

### 7. Quais decisoes nao podem ser duplicadas?

Nao podem ser duplicadas:

* Selecao de politica observacional.
* Execucao de avaliacao observacional.
* Limites de qualidade da agua.
* Status observacional de parametros hidricos.
* Calculo de tendencias.
* Water Health Score.
* Criacao, deduplicacao e transicao de eventos operacionais.
* Classificacao executiva ja atribuida a `ExecutiveRules`, salvo se houver refatoracao explicita em GP futura.

### 8. Como preservar o PA-01?

PA-01 deve ser preservado assim:

* Policy Engine continua selecionando politicas.
* Motores especializados continuam executando avaliacoes.
* Analytics continua calculando tendencias, alertas e score.
* Governanca continua gerindo eventos.
* Executive Intelligence continua sintetizando estado executivo.
* Executive Recommendation consome sinais e produz recomendacoes, sem selecionar politica e sem executar avaliacao observacional.
* Painel Executivo apenas apresenta snapshot e recomendacoes.

### 9. Como evitar uma nova autoridade paralela?

Para evitar uma autoridade paralela:

* Recomendacoes devem sempre referenciar sinais de origem.
* Nenhuma recomendacao pode recalcular limites hidricos.
* Nenhuma recomendacao pode alterar severidade observacional produzida pelo Nucleo.
* Nenhuma recomendacao pode reclassificar evento operacional; pode apenas sugerir acao.
* O servico deve tratar ausencias de dados como incerteza explicita, nao como inferencia silenciosa.
* O Painel Executivo nao deve substituir Governanca Operacional como camada de acompanhamento.

## Responsabilidades Futuras Por Camada

| Camada | Responsabilidade futura | Nao deve fazer |
| ------ | ----------------------- | -------------- |
| Analytics | Produzir tendencias, alertas preventivos e Water Health Score | Governar eventos ou emitir recomendacao executiva final |
| Governanca Operacional | Persistir e acompanhar eventos, estados e rastreabilidade | Recalcular avaliacao observacional ou score |
| Executive Intelligence | Compor snapshot executivo e coordenar regras executivas | Ler CSV ou executar avaliacao observacional |
| Executive Rules | Classificar status, selecionar sinais e prioridades | Criar motor paralelo de qualidade da agua |
| ExecutiveRecommendationService | Produzir recomendacoes rastreaveis a partir de sinais existentes | Selecionar politica, executar avaliacao, criar evento ou alterar estado |
| Painel Executivo | Apresentar snapshot, prioridades e recomendacoes | Decidir status, conformidade ou recomendacao por conta propria |

## Fluxo Proposto

```text
CSVs operacionais
        |
AnalyticsRepository
        |
AnalyticsService
        |---- tendencias
        |---- alertas preventivos
        |---- Water Health Score
        |
OperationalGovernanceService
        |---- eventos
        |---- estados
        |---- rastreabilidade observacional
        |
ExecutiveIntelligenceService
        |---- ExecutiveSnapshot
        |
ExecutiveRecommendationService (futuro)
        |---- recomendacoes executivas rastreaveis
        |
Painel Executivo
```

## Regras De Projeto Para GP-A22B

GP-A22B deve:

* Criar modelos simples de recomendacao executiva.
* Criar `ExecutiveRecommendationService`.
* Consumir apenas servicos/snapshots existentes.
* Preservar testes atuais.
* Adicionar testes focados em recomendacoes.
* Manter recomendacoes deterministicas e explicaveis.
* Nao alterar o Nucleo de Monitoramento Hidrico.
* Nao alterar CSVs.
* Nao alterar telas, exceto se houver GP especifica posterior para apresentacao.

GP-A22B nao deve:

* Implementar IA generativa.
* Implementar Machine Learning.
* Criar nova conformidade legal.
* Criar motor paralelo de avaliacao observacional.
* Criar transicoes automaticas de governanca.

## Sequencia Futura Sugerida

1. GP-A22B - Implementar `ExecutiveRecommendationService` e modelos de recomendacao.
2. GP-A22C - Integrar recomendacoes ao `ExecutiveSnapshot`.
3. GP-A22D - Adaptar Painel Executivo para apresentar recomendacoes, preservando a interface existente.
4. GP-A22E - Criar testes de rastreabilidade de recomendacoes ate Analytics, Governanca e Nucleo.
5. GP-A23 - Avaliar camada de configuracao executiva para pesos, horizontes e prioridades por perfil operacional.

## Veredito

A GP-A22A define a Inteligencia Executiva Evolutiva como camada consumidora e sintetizadora.

Recomendacao executiva nao e autoridade observacional. Ela deve se apoiar em Analytics, Governanca Operacional e Nucleo de Monitoramento Hidrico para produzir acoes sugeridas, mantendo PA-01 e evitando autoridade paralela.

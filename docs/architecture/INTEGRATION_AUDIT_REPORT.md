# GP-A20 - Integração da Previsão Analítica com o Núcleo de Monitoramento Hídrico

Data: 27/06/2026

Status: CONCLUÍDA

## Contexto

A GP-A14 / AI-06 identificou que a camada `analytics` possuía decisões próprias para qualidade da água, especialmente em alertas preventivos e Water Health Score.

Pontos identificados na auditoria:

* Uso de `QUALITY_LIMITS` local.
* Alertas preventivos baseados em limites hardcoded.
* Penalidades de qualidade calculadas a partir de faixas locais.
* Risco de divergência com Dashboard e Qualidade da Água já integrados ao Núcleo de Monitoramento Hídrico.

## Alteração Arquitetural

A GP-A20 integrou a Previsão Analítica ao Núcleo de Monitoramento Hídrico para avaliações observacionais de qualidade da água.

Estado após integração:

* `AnalyticsHydricMonitoringAdapter` passa a traduzir medições analíticas de qualidade para parâmetros hídricos do catálogo.
* `PreventiveAlertService` passa a gerar alertas de limite de qualidade a partir de resultados observacionais do núcleo.
* `WaterHealthScoreCalculator` passa a calcular penalidades de qualidade a partir de resultados observacionais do núcleo.
* `QUALITY_LIMITS` deixou de ser usado como autoridade local de decisão observacional.
* Tendências continuam sob responsabilidade da camada `analytics`.
* Leitura dos CSVs continua via `AnalyticsRepository`.
* A interface visual de `PrevisaoAnaliticaPage` foi preservada.

## PA-01

Separação mantida:

* Analytics calcula tendências.
* Policy Engine seleciona a política observacional.
* `AvaliacaoObservacionalService` executa a avaliação.
* Analytics consome o resultado observacional como insumo para alertas e score.

## Limites e Conformidade

A GP-A20 não implementa conformidade legal completa.

As avaliações de qualidade usadas pela Previsão Analítica vêm de `limite_observacional` do catálogo, mantendo caráter observacional e operacional.

## Impacto na AI-06

Veredito atualizado:

INTEGRAÇÃO OBSERVACIONAL DE QUALIDADE CONCLUÍDA COM TENDÊNCIAS PRESERVADAS.

Prioridade remanescente:

MÉDIA.

Lacunas remanescentes:

* Tendências continuam com tolerâncias analíticas próprias, por serem responsabilidade legítima de `analytics`.
* Consumo, perdas e contexto ambiental ainda possuem regras preventivas próprias fora do núcleo hídrico.
* Water Health Score ainda possui pesos executivos/analíticos próprios, mas a decisão de qualidade vem do núcleo.
* Configuração Operacional ainda não define perfil/cenário da Previsão Analítica.

## Testes

Comando executado:

`python -m unittest discover -s tests`

Resultado:

* 56 testes executados.
* Todos passaram.

## Matriz de Conformidade GP-A20

| Critério | Resultado |
| -------- | --------- |
| Preservar interface visual da Previsão Analítica | Atendido |
| Preservar leitura via `AnalyticsRepository` | Atendido |
| Preservar cálculo de tendências | Atendido |
| Não implementar conformidade legal completa | Atendido |
| Analytics calcula tendências | Atendido |
| Policy Engine seleciona política observacional | Atendido |
| Motor Observacional executa avaliação | Atendido |
| Analytics consome resultado observacional como insumo | Atendido |
| Remover autoridade local `QUALITY_LIMITS` para decisão de qualidade | Atendido |
| Evitar divergência com Dashboard e Qualidade da Água | Atendido |
| Manter testes passando | Atendido |

## Veredito

GP-A20 concluída.

A Previsão Analítica continua exibindo tendências, alertas e Water Health Score, mas avaliações de qualidade da água baseadas em limites observacionais passam a vir do Núcleo de Monitoramento Hídrico.

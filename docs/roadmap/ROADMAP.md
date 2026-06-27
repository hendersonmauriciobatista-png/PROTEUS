# ROADMAP

## Fase 1 — Fundação

Status: Concluída

* [x] Protótipo funcional criado
* [x] Constituição do Projeto criada
* [x] Estrutura documental inicial criada

---

## Fase 2 — Consolidação

Status: Em andamento

* [x] Persistência de dados
* [x] Histórico de medições
* [ ] Exportação de relatórios
* [ ] Cadastro de pontos de coleta
* [ ] Registro de eventos críticos

---

## Fase 3 — Inteligência Analítica

Status: Planejada

* [ ] Tendências históricas
* [ ] Alertas inteligentes
* [ ] Detecção de anomalias
* [ ] Avaliação automática de risco

---

## Fase 4 — Operação

Status: Planejada

* [ ] Integração com sensores reais
* [ ] Dashboard operacional
* [ ] Multiusuário
* [ ] Auditoria completa dos dados

---

## Visão De Longo Prazo

Transformar o sistema em uma plataforma auditável de monitoramento ambiental orientada por governança explícita e rastreabilidade completa.

# Estado Atual Do Roadmap

## Baseline Atual

### Baseline Operacional Inteligente V1

Status: CONSOLIDADA

Data de Consolidação: 23/06/2026

Descrição:

Primeira baseline completa do CASE-01 composta por camadas operacionais, analíticas, governança observacional e inteligência executiva.

Fluxo consolidado:

Observação
→ Relatórios
→ Análise
→ Governança
→ Inteligência Executiva

---

# Marcos Concluídos

| GP     | Marco                           | Status    |
| ------ | ------------------------------- | --------- |
| GP-A01 | Dashboard Summary V1            | ENCERRADA |
| GP-A02 | Qualidade Da Água               | ENCERRADA |
| GP-A03 | Dados Ambientais                | ENCERRADA |
| GP-A04 | Consumo E Distribuição          | ENCERRADA |
| GP-A05 | Relatórios Operacionais V1      | ENCERRADA |
| GP-A06 | Analytical Prediction Layer V1  | ENCERRADA |
| GP-A07 | Operational Governance Layer V1 | ENCERRADA |
| GP-A08 | Executive Intelligence Layer V1 | ENCERRADA |
| GP-A09 | Monitoramento Hídrico Modular Base | ENCERRADA |
| GP-A10 | Configuração Operacional de Monitoramento Hídrico | ENCERRADA |
| GP-A11 | Catálogo Inteligente de Parâmetros Hídricos | ENCERRADA |
| GP-A12 | Motor de Avaliação Observacional | ENCERRADA |
| GP-A12A | Policy Engine do Monitoramento Hídrico | ENCERRADA |
| GP-A14 | Auditoria de Integração do Núcleo de Monitoramento Hídrico | CONCLUÍDA |
| GP-A15 | Integração do Dashboard ao Núcleo de Monitoramento Hídrico | INICIADA |
| GP-A16 | Integração de Qualidade da Água / Monitoramento Hídrico com o Núcleo | CONCLUÍDA |
| GP-A17 | Integração dos Dados Ambientais com o Núcleo de Monitoramento Hídrico | CONCLUÍDA SEM ADAPTER FUNCIONAL |
| GP-A18 | Integração de Consumo e Distribuição com o Núcleo de Monitoramento Hídrico | CONCLUÍDA SEM ADAPTER FUNCIONAL |
| GP-A19 | Integração dos Relatórios Operacionais com o Núcleo de Monitoramento Hídrico | CONCLUÍDA |
| GP-A20 | Integração da Previsão Analítica com o Núcleo de Monitoramento Hídrico | CONCLUÍDA |
| GP-A21 | Integração da Governança Operacional com o Núcleo de Monitoramento Hídrico | CONCLUÍDA |
| GP-A22A | Arquitetura da Inteligência Executiva Evolutiva | CONCLUÍDA |

---

# Estado Arquitetural Consolidado

## Camada Operacional

Status: EM EVOLUÇÃO

Componentes:

* Dashboard
* Qualidade Da Água
* Monitoramento Hídrico
* Dados Ambientais
* Consumo E Distribuição
* Relatórios Operacionais

Evolução em andamento:

* GP-A09 cria a base modular de Monitoramento Hídrico sem substituir os fluxos existentes de Qualidade Da Água.
* Perfis operacionais e categorias de parâmetros passam a existir como catálogo rastreável.
* GP-A10 adiciona configurações operacionais customizáveis por cliente, cenário ou operação.
* Perfis operacionais passam a atuar como modelos iniciais, não como regras fixas.
* GP-A11 enriquece o catálogo de parâmetros com metadados técnicos, aplicabilidade por perfil e limites observacionais não legais.
* GP-A12 cria avaliação observacional determinística sem implementar conformidade legal/normativa.
* GP-A12A cria o Policy Engine e aplica o PA-01: seleção de política separada da execução por motores especializados.

Estado congelado:

* Núcleo de Monitoramento Hídrico - Ciclo Arquitetural 1 encerrado.
* Componentes concluídos: arquitetura modular, configuração operacional, catálogo inteligente, motor de avaliação observacional, Policy Engine e PA-01.
* Próxima evolução deve ocorrer após auditoria de integração arquitetural.

## Camada Analítica

Status: ENCERRADA

Componentes:

* Tendências
* Alertas Preventivos
* Water Health Score

Commit de referência:

fc2732f — feat: add analytical prediction layer v1

## Camada De Governança Operacional

Status: ENCERRADA

Componentes:

* Eventos Operacionais
* Persistência De Eventos
* Estados Observacionais
* Rastreamento De Ocorrências

Commit de referência:

cae6ef1 — feat: add operational governance layer v1

## Camada De Inteligência Executiva

Status: ENCERRADA

Componentes:

* Executive Snapshot
* Classificação Executiva
* Prioridades Observacionais
* Painel Executivo

Commit de referência:

0052e39 — feat: add executive intelligence layer v1

---

# Estado Geral Do Projeto

CASE-01

Status Geral:

BASELINE OPERACIONAL INTELIGENTE V1
APROVADA E CONSOLIDADA

Sem bloqueadores arquiteturais conhecidos.

Sem dependência de Machine Learning.

Sem dependência de IA generativa.

Arquitetura determinística, explicável e auditável.

---

# Próximas Expansões

Núcleo de Monitoramento Hídrico - Ciclo Arquitetural 1 encerrado e congelado.

Próxima GP:

GP-A14
Status: CONCLUÍDA

Escopo previsto:

* [x] AI-01 - Auditar integração com Dashboard.
* [x] GP-A15 - Remover avaliação observacional própria do Dashboard.
* [x] AI-02 - Auditar integração com Qualidade da Água / Monitoramento Hídrico.
* [x] AI-03 - Auditar integração com Dados Ambientais.
* [x] AI-04 - Auditar integração com Consumo e Distribuição.
* [x] AI-05 - Auditar integração com Relatórios.
* [x] AI-06 - Auditar integração com Previsão Analítica.
* [x] AI-07 - Auditar integração com Governança Operacional.
* [x] AI-08 - Auditar integração com Painel Executivo.
* [x] Identificar quais módulos ainda usam lógica própria.
* [x] Identificar quais módulos devem passar a consumir o novo núcleo de Monitoramento Hídrico.
* Preservar compatibilidade com CSVs e dados operacionais existentes.

Pendência pós-GP-A15:

* Integrar Dashboard com configuração operacional.
* Avaliar extração futura de uma camada de serviço de resumo do Dashboard.
* [x] Integrar Qualidade da Água / Monitoramento Hídrico com adapter próprio.
* [x] Remover `CONAMA` e `check_status` da camada visual.
* [x] Auditar Dados Ambientais e concluir que adapter hídrico não é necessário nesta etapa.
* Avaliar catálogo/metadados futuros para parâmetros ambientais.
* [x] Auditar Consumo e Distribuição e concluir que adapter hídrico não é necessário nesta etapa.
* Avaliar política futura para perdas estimadas e consumo, se houver necessidade observacional.
* [x] Integrar Relatórios com adapter próprio e remover `_quality_status` da camada visual.
* [x] Garantir que relatórios consumam avaliações observacionais do núcleo.
* [x] Integrar Previsão Analítica com adapter analítico para consumir avaliações observacionais do núcleo.
* [x] Separar tendências analíticas próprias de decisões baseadas em limites hídricos.
* [x] Preparar Water Health Score para usar avaliações observacionais nas penalidades de qualidade.
* [x] Integrar Governança Operacional com eventos enriquecidos por metadados de avaliação.
* Desacoplar futuramente a origem de alertas de `AnalyticsService` puro.
* Preservar transições de governança e histórico em `eventos_operacionais.json`.
* Integrar Painel Executivo com sinais rastreáveis até política, motor e avaliação.
* Preservar regras executivas como síntese, sem transformar o painel em motor de avaliação.

Nova fase:

Inteligência Executiva Evolutiva.

GP-A22A:

CONCLUÍDA.

Entregável:

* Blueprint arquitetural em `docs/architecture/EXECUTIVE_INTELLIGENCE_ARCHITECTURE.md`.
* Responsabilidades futuras separadas entre Analytics, Governança Operacional, Executive Intelligence, Executive Rules, futuro `ExecutiveRecommendationService` e Painel Executivo.
* PA-01 preservado.
* Recomendação executiva definida como consumidora de sinais existentes, sem autoridade observacional própria.

Próxima etapa sugerida:

GP-A22B - Implementar o mecanismo determinístico de recomendações executivas.

Prioridade:

ALTA.

Motivo:

A fila de integração arquitetural da GP-A14 foi encerrada. O próximo avanço natural é transformar os sinais já observados, interpretados e governados em recomendações executivas rastreáveis, mantendo o Núcleo de Monitoramento Hídrico como autoridade observacional central.

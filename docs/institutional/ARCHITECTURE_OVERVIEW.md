# Visao Arquitetural Executiva Do Sistema de Monitoramento de Águas

## Controle Documental

| Campo | Valor |
| --- | --- |
| Código documental | PRO-KIT-005 |
| Versão | 1.2 |
| Data-base | 26/07/2026 — implantação do controle documental; a arquitetura não foi revalidada nesta data |
| Responsável pela elaboração | Evidência documental não encontrada. |
| Custódia documental | Evidência documental não encontrada. |
| Situação documental | Integrante de `DOC-002`, classificado como `Validado` quanto à existência e organização documental; estado institucional reconciliado pela GP-PD-02; conteúdo técnico não revalidado |
| Responsabilidade documental | Visão arquitetural institucional do Sistema de Monitoramento de Águas |
| Autoridade institucional | `docs/institutional/DOCUMENT_REGISTER.md`, seções 4 e 5 |

### Histórico de Revisões

| Versão | Data | Instrumento | Alteração |
| --- | --- | --- | --- |
| 1.0 | 26/07/2026 | GP-PD-01 | Implantação exclusiva de metadados e controle documental, sem alteração do conteúdo técnico ou institucional preexistente. |
| 1.1 | 26/07/2026 | GP-PD-02 | Vinculação ao estado institucional oficial reconciliado no Registro Mestre, sem alteração do conteúdo técnico preexistente. |
| 1.2 | 26/07/2026 | GP-PD-03 | Definição como autoridade primária da visão arquitetural e centralização da arquitetura documental no Registro Mestre, sem alterar a arquitetura do software. |

## Objetivo

Apresentar uma visao arquitetural de alto nivel, voltada a publico executivo e tecnico, contendo exclusivamente componentes existentes no Sistema de Monitoramento de Águas.

## Principio Geral

O Sistema de Monitoramento de Águas organiza informacoes de monitoramento hidrico por camadas especializadas. Cada camada agrega valor sem assumir a autoridade da camada anterior.

## Visao Em Alto Nivel

```text
Interface
  |
Coleta e Registro
  |
Monitoramento Hidrico
  |
Analytics
  |
Governanca Operacional
  |
Executive Recommendation
  |
Executive Intelligence
  |
Dashboard / Painel Executivo / Relatorios
```

## Camada Operacional

Responsavel por registrar e apresentar dados operacionais.

Componentes:

* Projeto de Monitoramento.
* Qualidade da Agua.
* Dados Ambientais.
* Consumo e Distribuicao.
* Relatorios.
* Dashboard.

Papel institucional:

* transformar entrada manual em registros consultaveis;
* preservar historico local;
* apresentar estado operacional de forma acessivel.

## Camada De Monitoramento Hidrico

Responsavel pela avaliacao observacional de qualidade da agua.

Componentes:

* Catalogo de parametros.
* Configuracoes operacionais.
* Politicas.
* Policy Engine.
* Motor de Avaliacao Observacional.
* Adapters para consumidores.

Papel institucional:

* preservar PA-01;
* selecionar politicas separadamente da avaliacao;
* produzir resultados observacionais explicaveis.

## Camada Analitica

Responsavel por transformar registros e resultados observacionais em sinais analiticos.

Componentes:

* Repositorios analiticos.
* Tendencias.
* Alertas preventivos.
* Water Health Score.

Papel institucional:

* identificar tendencias;
* gerar alertas preventivos;
* consolidar score de saude hidrica.

## Camada De Governanca

Responsavel por acompanhar eventos operacionais derivados de alertas.

Componentes:

* Eventos operacionais.
* Estados de evento.
* Regras de transicao.
* Repositorio JSON.
* Servico de governanca.

Papel institucional:

* transformar alertas em acompanhamento governado;
* preservar rastreabilidade;
* registrar historico de estados.

## Camada Executiva

Responsavel por sintetizar sinais e apoiar comunicacao executiva.

Componentes:

* Executive Recommendation.
* Executive Intelligence.
* Executive Snapshot.
* Painel Executivo.

Papel institucional:

* consolidar prioridades;
* apresentar recomendacoes rastreaveis;
* apoiar leitura executiva sem substituir decisao humana.

## Persistencia

| Persistencia | Uso |
| --- | --- |
| CSV | Medicoes e dados operacionais. |
| JSON | Projeto, catalogo, configuracoes, politicas e eventos. |
| TXT | Relatorio operacional exportado. |

## Interface

A interface atual e desktop, implementada com PyQt5. Ela organiza o acesso aos modulos existentes e apresenta dashboards, tabelas, formularios e relatorios.

## Guardrails

* Nao criar autoridade observacional fora do Nucleo de Monitoramento Hidrico.
* Nao mover regras analiticas para a interface.
* Nao transformar Governanca em motor de avaliacao.
* Nao transformar Recommendation em acesso direto a CSV, Policy Engine ou Motor Observacional.
* Nao promover Discoveries sem auditoria propria.

## Estado Arquitetural

A AC-01 concluiu que a implementacao atual representa corretamente a arquitetura consolidada, com ressalvas evolutivas nao bloqueantes.

# Ficha Tecnica Do Sistema de Monitoramento de Águas

## Controle Documental

| Campo | Valor |
| --- | --- |
| Código documental | PRO-KIT-003 |
| Versão | 1.2 |
| Data-base | 26/07/2026 — implantação do controle documental; o conteúdo técnico não foi revalidado nesta data |
| Responsável pela elaboração | Evidência documental não encontrada. |
| Custódia documental | Evidência documental não encontrada. |
| Situação documental | Integrante de `DOC-002`, classificado como `Validado` quanto à existência e organização documental; estado institucional reconciliado pela GP-PD-02; conteúdo técnico não revalidado |
| Responsabilidade documental | Inventário técnico e caracterização da plataforma |
| Autoridade institucional | `docs/institutional/DOCUMENT_REGISTER.md`, seções 4 e 5 |

### Histórico de Revisões

| Versão | Data | Instrumento | Alteração |
| --- | --- | --- | --- |
| 1.0 | 26/07/2026 | GP-PD-01 | Implantação exclusiva de metadados e controle documental, sem alteração do conteúdo técnico ou institucional preexistente. |
| 1.1 | 26/07/2026 | GP-PD-02 | Vinculação ao estado institucional oficial reconciliado no Registro Mestre, sem alteração do conteúdo técnico preexistente. |
| 1.2 | 26/07/2026 | GP-PD-03 | Definição como autoridade primária da caracterização técnica e centralização da arquitetura documental no Registro Mestre, sem alteração técnica. |

## Objetivo

Consolidar a ficha tecnica institucional do Sistema de Monitoramento de Águas, refletindo exclusivamente o estado atual da plataforma.

## Identificacao

| Campo | Valor |
| --- | --- |
| Produto | Sistema de Monitoramento de Águas |
| Natureza | Plataforma desktop de monitoramento hidrico e inteligencia operacional |
| Programa | CASE-01 - ICFACTORY |
| Estado de Engenharia | Concluida pela AC-01 |
| Fase atual | Produto Institucional |
| Identidade visual | Consolidada pela PI-01 |

## Arquitetura

| Camada | Responsabilidade |
| --- | --- |
| Interface | Telas PyQt5 para registro, consulta, dashboard, relatorios, governanca e painel executivo. |
| Coleta/Registro | Entrada manual de dados operacionais em CSV. |
| Monitoramento Hidrico | Catalogo, configuracoes, politicas e avaliacao observacional. |
| Analytics | Tendencias, alertas preventivos e Water Health Score. |
| Governanca Operacional | Sincronizacao de alertas como eventos, estados e rastreabilidade. |
| Executive Recommendation | Recomendacoes deterministicas a partir de sinais consolidados. |
| Executive Intelligence | Composicao de snapshot executivo, prioridades e mensagens. |
| Persistencia | CSV e JSON locais. |

## Linguagem Utilizada

* Python.

## Tecnologias

* PyQt5.
* CSV.
* JSON.
* Markdown.
* `unittest`.

## Persistencia

| Tipo | Uso |
| --- | --- |
| CSV | Medicoes de qualidade da agua, dados ambientais, consumo e distribuicao. |
| JSON | Projeto de Monitoramento, configuracoes, catalogo, politicas e eventos operacionais. |
| TXT | Exportacao de relatorio operacional. |

## Modulos Existentes

| Modulo / pacote | Papel |
| --- | --- |
| `main.py` | Janela principal, navegacao e Dashboard. |
| `qualidade_agua.py` | Registro e historico de qualidade da agua. |
| `dados_ambientais.py` | Registro e historico de contexto ambiental. |
| `consumo_distribuicao.py` | Registro e historico de consumo/distribuicao. |
| `relatorios.py` | Relatorio operacional consolidado e exportacao TXT. |
| `previsao_analitica.py` | Apresentacao da camada analitica. |
| `governanca_operacional.py` | Interface de eventos e governanca operacional. |
| `painel_executivo.py` | Painel Executivo. |
| `projeto_monitoramento_page.py` | Tela do Projeto de Monitoramento. |
| `monitoramento_hidrico` | Nucleo de monitoramento, politicas, catalogo e adapters. |
| `analytics` | Repositorios, tendencias, alertas e score. |
| `governance` | Eventos, regras, repositorio e servico de governanca. |
| `executive_recommendation` | Modelos, regras e servico de recomendacao executiva. |
| `executive` | Snapshot, regras e servico executivo. |

## Dashboards E Telas

* Projeto de Monitoramento.
* Dashboard.
* Painel Executivo.
* Qualidade da Agua.
* Consumo e Distribuicao.
* Dados Ambientais.
* Relatorios.
* Previsao Analitica.
* Governanca Operacional.

## Requisitos Operacionais

* Ambiente Python com dependencias do projeto instaladas.
* Execucao desktop com suporte a PyQt5.
* Acesso de escrita aos arquivos locais de dados.
* Estrutura `data/` disponivel para CSV e JSON.
* Estrutura `reports/` para exportacao de relatorios.

## Ambiente De Execucao

| Item | Estado atual |
| --- | --- |
| Tipo de aplicacao | Desktop |
| Interface | PyQt5 |
| Banco de dados | Nao utiliza banco relacional no estado atual |
| Persistencia local | CSV/JSON |
| Machine Learning | Nao utilizado |
| IA generativa | Nao utilizada |
| Conformidade legal automatica | Nao implementada |

## Restricoes Tecnicas Declaradas

* O sistema possui carater observacional e institucional.
* Nao substitui analises laboratoriais oficiais.
* Nao emite laudos regulatorios.
* Nao executa decisoes operacionais automaticas.
* Nao absorve processos externos de campo, laboratorio ou logistica.

## Testes

A suite existente cobre componentes de monitoramento hidrico, analytics, governanca, recomendacao, executive e adapters. Esta ficha tecnica nao executa testes.

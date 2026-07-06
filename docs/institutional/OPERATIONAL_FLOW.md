# Fluxo Operacional Oficial Do PROTEUS

## Objetivo

Documentar o fluxo operacional oficial do PROTEUS em linguagem institucional, representando apenas o estado atual do sistema.

## Fluxo Resumido

```text
Entrada de Dados
  |
Registro e Validacao de Entrada
  |
Persistencia Local
  |
Monitoramento Hidrico
  |
Analise
  |
Governanca Operacional
  |
Inteligencia Executiva
  |
Dashboard / Painel Executivo / Relatorios
```

## 1. Entrada De Dados

O PROTEUS recebe informacoes por telas operacionais:

* qualidade da agua;
* dados ambientais;
* consumo e distribuicao;
* Projeto de Monitoramento.

No estado atual, a entrada e manual e local.

## 2. Registro E Validacao De Entrada

As telas estruturam os dados em campos definidos. A validacao operacional e simples e associada ao formulario, sem representar conformidade legal automatica.

Exemplos:

* campos numericos para medicoes;
* observacoes textuais;
* contexto operacional;
* ponto principal de coleta;
* status do Projeto.

## 3. Persistencia Local

Os registros sao preservados em arquivos locais:

* CSV para medicoes operacionais;
* JSON para projeto, catalogo, configuracoes, politicas e eventos;
* TXT para relatorio operacional exportado.

## 4. Monitoramento Hidrico

Quando os dados envolvem qualidade da agua, o fluxo passa pelo Nucleo de Monitoramento Hidrico:

```text
Policy Engine
  |
Motor de Avaliacao Observacional
  |
Resultado observacional
```

Essa etapa preserva PA-01: selecao de politica e execucao da avaliacao permanecem separadas.

## 5. Analise

A camada Analytics consome dados operacionais e resultados observacionais para produzir:

* tendencias;
* alertas preventivos;
* Water Health Score.

Essa camada nao substitui o Nucleo de Monitoramento Hidrico como autoridade observacional para qualidade da agua.

## 6. Governanca Operacional

Alertas analiticos podem ser sincronizados como eventos operacionais.

A Governanca Operacional registra:

* estado do evento;
* severidade;
* origem;
* evidencia;
* recomendacao;
* historico de acompanhamento;
* metadados observacionais quando disponiveis.

## 7. Inteligencia Executiva

A Inteligencia Executiva consolida sinais de Analytics, Governanca e Recommendation para produzir:

* status executivo;
* prioridades observacionais;
* recomendacoes;
* mensagens executivas;
* snapshot executivo.

## 8. Dashboard, Painel Executivo E Relatorios

As informacoes consolidadas sao apresentadas em:

* Dashboard operacional;
* Painel Executivo;
* Relatorios Operacionais;
* telas de historico e acompanhamento.

Essas interfaces apresentam informacao, mas nao substituem a autoridade das camadas responsaveis.

## Fluxos Paralelos

Nem todo dado segue exatamente o mesmo percurso:

* dados ambientais podem ser contexto para Dashboard, Relatorios e Analytics;
* consumo e distribuicao podem alimentar indicadores e alertas preventivos;
* qualidade da agua passa por avaliacao observacional quando aplicavel;
* alertas podem virar eventos de governanca;
* sinais consolidados podem alimentar recomendacoes e painel executivo.

## Limites Operacionais

O PROTEUS nao executa:

* coleta fisica;
* transporte de amostras;
* analise laboratorial oficial;
* logistica de campanha;
* calibracao de equipamentos;
* cadeia de custodia fisica;
* decisao regulatoria automatica.

## Veredito

O fluxo operacional atual e suficiente para apresentacao institucional da plataforma e permanece aderente a OP-00, OP-01 e AC-01.

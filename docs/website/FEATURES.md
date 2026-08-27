# Pagina Funcionalidades do Website Institucional do Sistema de Monitoramento de Águas

## Objetivo

Especificar a pagina de funcionalidades do Website Institucional, apresentando exclusivamente capacidades implementadas ou documentadas como existentes no Sistema de Monitoramento de Águas.

## Regra Principal

Nao documentar funcionalidades futuras como existentes.

## Areas Funcionais

### Dashboard

Apresenta visao geral do sistema, resumo operacional, cards principais, dados consolidados e grafico executivo do Water Health Score.

### Qualidade Da Agua

Permite registrar e consultar medicoes de qualidade da agua. A avaliacao observacional e delegada ao Nucleo de Monitoramento Hidrico.

### Dados Ambientais

Permite registrar contexto ambiental, como temperatura ambiente, umidade, chuva, pressao e observacoes.

### Consumo E Distribuicao

Permite registrar consumo diario, consumo mensal, volume distribuido, perdas estimadas e observacoes operacionais.

### Relatorios

Consolida informacoes operacionais e permite exportacao de relatorio em TXT. O status de qualidade utiliza adapter do Nucleo quando aplicavel.

### Previsao Analitica

Apresenta tendencias, alertas preventivos e Water Health Score com base nos dados operacionais e resultados observacionais quando aplicavel.

### Governanca Operacional

Transforma alertas em eventos acompanhaveis, registrando estado, severidade, origem, evidencia, recomendacao e historico.

### Inteligencia Executiva

Consolida sinais de Analytics, Governanca e Recommendation para apresentar status executivo, prioridades, recomendacoes e snapshot executivo.

## Capacidades Transversais

* Persistencia local em CSV e JSON.
* Documentacao arquitetural e institucional.
* Identidade visual oficial.
* Rastreabilidade de responsabilidades.
* Separacao entre avaliacao observacional e decisao humana.

## Nao Funcionalidades

Nao apresentar como existente:

* API publica.
* Versao web operacional.
* Login web.
* Banco de dados relacional.
* Machine Learning.
* IA generativa.
* Coleta fisica automatizada.
* Decisao regulatoria automatica.

## Veredito

A pagina deve funcionar como catalogo publico das capacidades atuais, preservando clareza institucional e fronteiras arquiteturais.

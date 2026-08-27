# Casos De Uso Institucionais Do Sistema de Monitoramento de Águas

## Controle Documental

| Campo | Valor |
| --- | --- |
| Código documental | PRO-KIT-004 |
| Versão | 1.2 |
| Data-base | 26/07/2026 — implantação do controle documental; os casos de uso não foram revalidados nesta data |
| Responsável pela elaboração | Evidência documental não encontrada. |
| Custódia documental | Evidência documental não encontrada. |
| Situação documental | Integrante de `DOC-002`, classificado como `Validado` quanto à existência e organização documental; estado institucional reconciliado pela GP-PD-02; conteúdo técnico não revalidado |
| Responsabilidade documental | Casos de uso institucionais |
| Autoridade institucional | `docs/institutional/DOCUMENT_REGISTER.md`, seções 4 e 5 |

### Histórico de Revisões

| Versão | Data | Instrumento | Alteração |
| --- | --- | --- | --- |
| 1.0 | 26/07/2026 | GP-PD-01 | Implantação exclusiva de metadados e controle documental, sem alteração do conteúdo técnico ou institucional preexistente. |
| 1.1 | 26/07/2026 | GP-PD-02 | Vinculação ao estado institucional oficial reconciliado no Registro Mestre, sem alteração do conteúdo técnico preexistente. |
| 1.2 | 26/07/2026 | GP-PD-03 | Definição como autoridade primária dos casos de uso e centralização da arquitetura documental no Registro Mestre, sem alteração técnica. |

## Objetivo

Registrar casos reais de utilizacao do Sistema de Monitoramento de Águas no estado atual da plataforma.

## Caso 01 - Monitoramento Da Qualidade Da Agua

### Objetivo

Registrar medicoes de qualidade da agua e obter status observacional rastreavel.

### Atores

* Operador do sistema.
* Responsavel tecnico ou institucional.

### Fluxo Resumido

1. O operador acessa a tela Qualidade da Agua.
2. Registra pH, turbidez, oxigenio dissolvido e temperatura. O parametro generico de agrotoxicos esta descontinuado e fora do escopo operacional e planejado.
3. O sistema persiste a medicao.
4. O adapter consome o Nucleo de Monitoramento Hidrico.
5. O status observacional e apresentado na interface.

### Resultado Esperado

Medicao registrada, historico atualizado e status observacional apresentado sem decisao local da tela.

## Caso 02 - Registro De Dados Ambientais

### Objetivo

Registrar contexto ambiental associado ao monitoramento.

### Atores

* Operador do sistema.
* Analista ambiental.

### Fluxo Resumido

1. O operador acessa Dados Ambientais.
2. Informa temperatura ambiente, umidade, chuva, pressao e observacao.
3. O sistema salva o registro em CSV.
4. Os dados ficam disponiveis para historico, Dashboard, Relatorios e Analytics.

### Resultado Esperado

Contexto ambiental preservado como informacao operacional, sem avaliacao hidrica propria.

## Caso 03 - Consumo E Distribuicao

### Objetivo

Registrar dados de consumo, volume distribuido e perdas estimadas.

### Atores

* Operador do sistema.
* Gestor operacional.

### Fluxo Resumido

1. O operador acessa Consumo e Distribuicao.
2. Registra consumo diario, consumo mensal, volume distribuido, perdas e observacao.
3. O sistema salva os dados.
4. Analytics pode utilizar os registros para tendencias e alertas preventivos.

### Resultado Esperado

Dados operacionais disponiveis para leitura historica, relatorios e analise.

## Caso 04 - Relatorios Operacionais

### Objetivo

Consolidar informacoes operacionais em relatorio consultavel e exportavel.

### Atores

* Operador do sistema.
* Coordenador.
* Parte interessada institucional.

### Fluxo Resumido

1. O usuario acessa Relatorios.
2. O sistema consolida totais, ultimas medicoes e medias.
3. O status de qualidade e obtido por adapter do Nucleo.
4. O usuario pode exportar o relatorio em TXT.

### Resultado Esperado

Resumo operacional gerado sem decisao observacional local nos relatorios.

## Caso 05 - Alertas Preventivos

### Objetivo

Identificar sinais preventivos a partir de medicoes e tendencias.

### Atores

* Analista.
* Gestor operacional.

### Fluxo Resumido

1. Analytics carrega registros operacionais.
2. Calcula tendencias.
3. Consome avaliacao observacional para qualidade da agua.
4. Gera alertas preventivos quando aplicavel.

### Resultado Esperado

Alertas explicaveis e rastreaveis para acompanhamento, sem conformidade legal automatica.

## Caso 06 - Governanca Operacional

### Objetivo

Transformar alertas em eventos acompanhaveis.

### Atores

* Operador.
* Gestor.
* Responsavel por acompanhamento.

### Fluxo Resumido

1. A Governanca sincroniza alertas de Analytics.
2. Regras criam ou atualizam eventos.
3. Eventos recebem estado, severidade, evidencia e recomendacao.
4. O usuario acompanha transicoes de estado.

### Resultado Esperado

Eventos operacionais rastreaveis e acompanhados por ciclo de vida.

## Caso 07 - Apoio A Decisao

### Objetivo

Fornecer sinais consolidados para apoiar decisao humana.

### Atores

* Gestor.
* Coordenador institucional.
* Responsavel tecnico.

### Fluxo Resumido

1. Analytics produz score, tendencias e alertas.
2. Governanca fornece resumo de eventos.
3. Recommendation gera recomendacoes deterministicas.
4. Executive Intelligence consolida o snapshot executivo.

### Resultado Esperado

Recomendacoes rastreaveis e explicaveis, sem substituir decisao humana.

## Caso 08 - Painel Executivo

### Objetivo

Apresentar estado geral da plataforma em linguagem executiva.

### Atores

* Gestor institucional.
* Apresentador.
* Parte interessada externa.

### Fluxo Resumido

1. O usuario acessa Painel Executivo.
2. O sistema constroi `ExecutiveSnapshot`.
3. O painel apresenta status, score, eventos, prioridades, recomendacoes e sinais.
4. O apresentador usa a tela como apoio para discussao institucional.

### Resultado Esperado

Visao executiva consolidada e adequada para reunioes, demonstracoes e acompanhamento.

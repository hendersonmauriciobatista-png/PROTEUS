# Roteiro Oficial De Demonstracao Do Sistema de Monitoramento de Águas

## Controle Documental

| Campo | Valor |
| --- | --- |
| Código documental | PRO-KIT-007 |
| Versão | 1.2 |
| Data-base | 26/07/2026 — implantação do controle documental; o roteiro de demonstração não foi revalidado nesta data |
| Responsável pela elaboração | Evidência documental não encontrada. |
| Custódia documental | Evidência documental não encontrada. |
| Situação documental | Integrante de `DOC-002`, classificado como `Validado` quanto à existência e organização documental; estado institucional reconciliado pela GP-PD-02; conteúdo técnico não revalidado |
| Responsabilidade documental | Procedimento institucional de demonstração |
| Autoridade institucional | `docs/institutional/DOCUMENT_REGISTER.md`, seções 4 e 5 |

### Histórico de Revisões

| Versão | Data | Instrumento | Alteração |
| --- | --- | --- | --- |
| 1.0 | 26/07/2026 | GP-PD-01 | Implantação exclusiva de metadados e controle documental, sem alteração do conteúdo técnico ou institucional preexistente. |
| 1.1 | 26/07/2026 | GP-PD-02 | Vinculação ao estado institucional oficial reconciliado no Registro Mestre, sem alteração do conteúdo técnico preexistente. |
| 1.2 | 26/07/2026 | GP-PD-03 | Definição como autoridade primária do procedimento de demonstração e centralização da arquitetura documental no Registro Mestre, sem alteração técnica. |

## Objetivo

Definir um roteiro oficial para demonstracoes consistentes e reproduziveis do Sistema de Monitoramento de Águas perante universidades, instituicoes de pesquisa, empresas, orgaos publicos e demais partes interessadas.

## Duracao Recomendada

* Demonstracao curta: 10 a 15 minutos.
* Demonstracao completa: 25 a 40 minutos.

## Preparacao

Antes da demonstracao:

* confirmar que a aplicacao abre corretamente;
* verificar se existem dados de exemplo suficientes;
* confirmar que as telas carregam sem erro;
* evitar alterar dados reais durante apresentacoes institucionais sem necessidade;
* manter o foco em comunicacao institucional, nao em detalhe de implementacao.

## Sequencia Oficial

```text
1. Apresentacao institucional
2. Dashboard
3. Qualidade da Agua
4. Dados Ambientais
5. Consumo e Distribuicao
6. Relatorios
7. Previsao Analitica
8. Governanca Operacional
9. Painel Executivo
10. Encerramento
```

## 1. Apresentacao Institucional

Mensagem sugerida:

```text
O Sistema de Monitoramento de Águas e uma plataforma institucional de monitoramento hidrico que organiza registros,
avaliacoes observacionais, sinais analiticos, governanca operacional e sintese executiva
em uma arquitetura rastreavel e explicavel.
```

Pontos a destacar:

* origem no CASE-01;
* Engenharia concluida pela AC-01;
* identidade visual consolidada pela PI-01;
* kit institucional consolidado pela PI-02;
* foco em monitoramento, confiabilidade e tecnologia.

## 2. Dashboard

Objetivo da tela:

Apresentar visao geral do sistema.

Demonstrar:

* cards principais;
* resumo de qualidade da agua;
* dados ambientais;
* consumo;
* total de registros;
* grafico de Water Health Score.

Mensagem-chave:

O Dashboard apresenta informacoes consolidadas sem substituir as camadas responsaveis por avaliacao e analise.

## 3. Qualidade Da Agua

Objetivo da tela:

Registrar e consultar medicoes de qualidade da agua.

Demonstrar:

* campos de medicao;
* historico;
* status observacional;
* separacao entre tela e Nucleo de Monitoramento Hidrico.

Mensagem-chave:

A avaliacao observacional e feita pelo Nucleo, preservando PA-01.

## 4. Dados Ambientais

Objetivo da tela:

Registrar contexto ambiental.

Demonstrar:

* temperatura ambiente;
* umidade;
* chuva;
* pressao;
* observacao.

Mensagem-chave:

Dados ambientais enriquecem o contexto operacional, mas nao sao tratados como conformidade hidrica.

## 5. Consumo E Distribuicao

Objetivo da tela:

Registrar dados operacionais de consumo, volume e perdas.

Demonstrar:

* consumo diario;
* consumo mensal;
* volume distribuido;
* perdas estimadas;
* historico.

Mensagem-chave:

Consumo e distribuicao alimentam leitura operacional e analitica, sem criar nova autoridade observacional hidrica.

## 6. Relatorios

Objetivo da tela:

Consolidar informacoes operacionais em relatorio.

Demonstrar:

* totais de registros;
* ultimas medicoes;
* status de qualidade via adapter;
* exportacao TXT.

Mensagem-chave:

Relatorios apresentam e consolidam informacao; nao recalculam politicas localmente.

## 7. Previsao Analitica

Objetivo da tela:

Apresentar tendencias, alertas e Water Health Score.

Demonstrar:

* tendencias de qualidade;
* tendencias de consumo;
* alertas preventivos;
* score e explicacoes.

Mensagem-chave:

Analytics transforma dados em sinais, consumindo o Nucleo quando a qualidade da agua exige avaliacao observacional.

## 8. Governanca Operacional

Objetivo da tela:

Acompanhar eventos derivados de alertas.

Demonstrar:

* sincronizacao de alertas;
* lista de eventos;
* estados;
* transicoes;
* evidencias e recomendacoes.

Mensagem-chave:

Governanca acompanha eventos; nao executa avaliacao hidrica propria.

## 9. Painel Executivo

Objetivo da tela:

Apresentar sintese executiva para tomada de conhecimento e discussao institucional.

Demonstrar:

* status executivo;
* Water Health Score;
* eventos por estado;
* recomendacoes executivas;
* prioridades observacionais;
* sinais relevantes.

Mensagem-chave:

O Painel Executivo apoia leitura e comunicacao; a decisao permanece humana.

## 10. Encerramento

Mensagem sugerida:

```text
O Sistema de Monitoramento de Águas demonstra como uma plataforma de monitoramento hidrico pode unir registro,
avaliacao observacional, analise, governanca e inteligencia executiva mantendo
rastreabilidade, explicabilidade e separacao de responsabilidades.
```

## Perguntas Frequentes Para Demonstracao

### O Sistema de Monitoramento de Águas substitui laboratorio?

Nao. O Sistema de Monitoramento de Águas organiza e avalia informacoes observacionais, mas nao substitui laudos, metodos laboratoriais ou certificacoes oficiais.

### O Sistema de Monitoramento de Águas toma decisoes automaticas?

Nao. O sistema apoia leitura e acompanhamento. Decisoes operacionais ou regulatorias permanecem humanas.

### O Sistema de Monitoramento de Águas usa IA generativa ou Machine Learning?

Nao no estado atual. A arquitetura atual e deterministica.

### O Sistema de Monitoramento de Águas possui banco de dados relacional?

Nao no estado atual. A persistencia e local, baseada em CSV e JSON.

## Cuidados Durante A Demonstracao

* Nao prometer funcionalidades futuras como existentes.
* Nao apresentar o sistema como ferramenta regulatoria oficial.
* Nao dizer que o sistema executa coleta fisica ou laboratorio.
* Nao alterar a identidade visual durante a demonstracao.
* Nao criar novas interpretacoes arquiteturais fora da documentacao consolidada.

## Resultado Esperado

Ao final da demonstracao, o publico deve compreender:

* o que o Sistema de Monitoramento de Águas faz;
* quais camadas compoem a plataforma;
* como dados viram sinais e apresentacoes;
* por que a arquitetura e rastreavel;
* quais limites institucionais estao preservados.

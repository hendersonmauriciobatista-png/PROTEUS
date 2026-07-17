# PE-17 — Auditoria de Efetividade dos Guardrails de Comunicação da PA-01E

> **STATUS: AUDITORIA CONCLUÍDA — SEM ALTERAÇÃO DA ARQUITETURA OU DOS GUARDRAILS**

## 1. Identificação

Programa: **GP-PE-17 — Auditoria de Efetividade dos Guardrails de Comunicação (PA-01E)**.

Natureza: auditoria técnica, documental e experimental em cópias temporárias.

Objeto auditado: os cinco guardrails obrigatórios G-OBR-01 a G-OBR-05 implementados em `tests/test_pa01_communication_guardrails.py` pela GP-PE-16.

Commit versionado auditado: `d153b7a343a021516c69be8669e0c6325a52cc31`.

## 2. Objetivo

Avaliar se os guardrails da PA-01E protegem efetivamente as fronteiras arquiteturais definidas pela PA-01, distinguindo:

1. efetividade na árvore de trabalho atual;
2. efetividade do conteúdo versionado no `HEAD`;
3. reprodutibilidade em exportação limpa do `HEAD`;
4. capacidade de detectar violações diretas;
5. preservação de usos legítimos;
6. resistência a formas representativas de bypass.

A aprovação nominal dos cinco testes na árvore atual não é tratada como prova automática de proteção integral ou reproduzível.

## 3. Escopo e restrições

Esta GP auditou exclusivamente:

* implementação dos cinco guardrails obrigatórios;
* cobertura e precisão dos testes;
* uso da AST;
* mensagens de falha;
* dependência de nomes e caminhos fixos;
* falsos positivos e falsos negativos;
* manutenção futura;
* proveniência e reprodutibilidade.

Não foram alterados testes, runtime, services, adapters, repositories, interfaces, contratos, `HISTORY.md`, `ROADMAP.md`, documentos constitucionais, Harnesses ou documentos da GP-R06.

As mutações ocorreram exclusivamente em diretórios temporários externos ao repositório original. Nenhum artefato temporário foi incorporado.

## 4. Fontes analisadas

### 4.1 Fontes primárias

* `docs/architecture/PE_15_PA01E_COMMUNICATION_GUARDRAILS_AUDIT.md`;
* `docs/architecture/PE_16_PA01E_COMMUNICATION_GUARDRAILS_IMPLEMENTATION.md`;
* `tests/test_pa01_communication_guardrails.py`.

### 4.2 Componentes cobertos pelo teste

Superfícies de apresentação:

* `main.py`;
* `qualidade_agua.py`;
* `relatorios.py`;
* `painel_executivo.py`;
* `previsao_analitica.py`;
* `governanca_operacional.py`;
* `dados_ambientais.py`;
* `consumo_distribuicao.py`;
* `projeto_monitoramento_page.py`.

Analytics:

* `analytics/alerts.py`;
* `analytics/dashboard_snapshot.py`;
* `analytics/models.py`;
* `analytics/repositories.py`;
* `analytics/scoring.py`;
* `analytics/service.py`;
* `analytics/trends.py`.

Adapters:

* `monitoramento_hidrico/qualidade_agua_adapter.py`;
* `monitoramento_hidrico/dashboard_adapter.py`;
* `monitoramento_hidrico/operational_reports_adapter.py`;
* `monitoramento_hidrico/analytics_adapter.py`;
* `monitoramento_hidrico/governance_adapter.py`.

Executive:

* `executive/service.py`;
* `executive/rules.py`;
* `executive/models.py`;
* `executive_recommendation/service.py`;
* `executive_recommendation/rules.py`;
* `executive_recommendation/models.py`.

Cadeia de Governança e autoridades relacionadas:

* `governance/service.py`;
* `monitoramento_hidrico/quality_parameter_mapping.py`;
* `monitoramento_hidrico/status_semantics.py`.

## 5. Estado de proveniência

### 5.1 Documentos e teste

| Arquivo | Árvore atual | Rastreado | Presente no HEAD | Estado local |
| --- | --- | --- | --- | --- |
| `PE_15_PA01E_COMMUNICATION_GUARDRAILS_AUDIT.md` | Presente | Não | Não | Não rastreado |
| `PE_16_PA01E_COMMUNICATION_GUARDRAILS_IMPLEMENTATION.md` | Presente | Sim | Sim | Limpo |
| `tests/test_pa01_communication_guardrails.py` | Presente | Sim | Sim | Limpo |

A GP-PE-15 é declarada pela GP-PE-16 como fonte de autoridade, mas não está presente no conteúdo versionado. Portanto, sua autoridade documental não é formalmente reproduzível a partir do `HEAD` auditado.

### 5.2 Dependências disponíveis localmente e ausentes no HEAD

| Arquivo | Função na proteção | Estado |
| --- | --- | --- |
| `analytics/dashboard_snapshot.py` | Arquivo enumerado em Analytics por G-OBR-02 e G-OBR-04 | Não rastreado; ausente no HEAD |
| `monitoramento_hidrico/dashboard_adapter.py` | Adapter enumerado por G-OBR-03 e G-OBR-04 | Não rastreado; ausente no HEAD |
| `monitoramento_hidrico/quality_parameter_mapping.py` | Fonte central declarada por G-OBR-03 | Não rastreado; ausente no HEAD |
| `monitoramento_hidrico/status_semantics.py` | Vocabulário oficial declarado por G-OBR-04 e exceção de G-OBR-05 | Não rastreado; ausente no HEAD |

### 5.3 Componentes rastreados, porém modificados localmente

Foram observadas modificações locais preexistentes nos componentes relevantes:

* `main.py`;
* `qualidade_agua.py`;
* `relatorios.py`;
* `painel_executivo.py`;
* `analytics/alerts.py`;
* `analytics/scoring.py`;
* `monitoramento_hidrico/qualidade_agua_adapter.py`;
* `monitoramento_hidrico/operational_reports_adapter.py`;
* `monitoramento_hidrico/analytics_adapter.py`;
* `monitoramento_hidrico/governance_adapter.py`;
* `executive/models.py`;
* `executive_recommendation/service.py`;
* `executive_recommendation/models.py`;
* `governance/service.py`.

Consequência: o resultado aprovado na árvore atual depende tanto de arquivos não rastreados quanto de versões locais diferentes das versões presentes no `HEAD`.

## 6. Metodologia executada

### 6.1 Leitura e rastreabilidade

Foram lidos integralmente GP-PE-15, GP-PE-16 e o teste PA-01E. Cada requisito obrigatório foi relacionado à implementação, aos arquivos enumerados e à técnica AST utilizada.

### 6.2 Execução na árvore atual

Comando:

```text
python -m unittest tests.test_pa01_communication_guardrails
```

Resultado:

```text
Ran 5 tests in 0.160s
OK
```

### 6.3 Verificação de proveniência

Para cada fonte relevante foram verificados:

* existência na árvore atual;
* rastreamento por Git;
* estado local;
* presença no `HEAD` por `git cat-file`;
* conteúdo versionado por `git show` e `git grep`.

### 6.4 Exportação limpa do HEAD

Foi criada uma exportação temporária exclusivamente com `git archive HEAD`. Nenhum arquivo não rastreado foi copiado para essa exportação.

Na exportação foi executado:

```text
python -m unittest tests.test_pa01_communication_guardrails
```

Resultado:

```text
Ran 5 tests in 0.133s
FAILED (failures=1, errors=3)
```

### 6.5 Mutações controladas

Foi criada uma cópia temporária mínima da árvore atual contendo os arquivos enumerados pelo teste. A linha de base temporária executou os cinco testes com sucesso.

Foram realizados 18 experimentos:

* cinco violações diretas;
* cinco usos legítimos;
* cinco tentativas mínimas de bypass;
* um alias de importação em G-OBR-01;
* um bypass de controle de fluxo em G-OBR-02;
* um bypass por importação dinâmica e `getattr` em G-OBR-05.

As mutações foram apenas analisadas pelos testes estáticos; não houve execução funcional do runtime mutado.

## 7. Matriz geral de rastreabilidade

| Guardrail | Requisito de origem | Fronteira protegida | Implementação | Teste correspondente |
| --- | --- | --- | --- | --- |
| G-OBR-01 | Proibir UI de acessar `AnalyticsRepository` ou `WaterHealthScoreCalculator` | UI → Analytics interno | AST de imports e chamadas em nove arquivos de apresentação | `test_g_obr_01_ui_does_not_access_internal_analytics_dependencies` |
| G-OBR-02 | Proibir consumers externos de tratar adapters como autoridade primária | Governança → adapter de reavaliação | AST da classe/método, argumento `decisions`, ordem por linha e imports externos | `test_g_obr_02_governance_service_retains_reevaluation_authority` |
| G-OBR-03 | Proibir listas locais de parâmetros de qualidade | Adapters → fonte central PA-01C | AST de imports, atribuições e literais | `test_g_obr_03_quality_adapters_use_the_central_parameter_mapping` |
| G-OBR-04 | Proibir novos textos funcionais fora do vocabulário oficial | Superfícies de comunicação → PA-01A | AST de literais, normalização Unicode e lista de quatro rótulos proibidos | `test_g_obr_04_runtime_avoids_non_official_sensitive_status_texts` |
| G-OBR-05 | Proibir Executive de acessar CSV, motores ou adapters hídricos | Executive → persistência/Monitoramento Hídrico | AST de imports, chamadas e literais terminados em `.csv` | `test_g_obr_05_executive_uses_no_hydric_engine_adapter_or_csv` |

## 8. Matriz de experimentos

| ID | Guardrail | Tipo | Mutação ou caso | Resultado esperado | Resultado observado | Interpretação |
| --- | --- | --- | --- | --- | --- | --- |
| E-01 | G-OBR-01 | Violação direta | Importar e instanciar `AnalyticsRepository` em `previsao_analitica.py` | Bloquear | Bloqueado | Detecção direta efetiva |
| E-02 | G-OBR-01 | Legítimo | Importar `DashboardAnalyticsSnapshotService` | Permitir | Permitido | Contrato legítimo preservado |
| E-03 | G-OBR-01 | Bypass | Criar `nova_tela.py` fora de `PRESENTATION_FILES` com acesso proibido | Bloquear | Permitido | Falso negativo por lista fixa |
| E-04 | G-OBR-01 | Alias | Importar `AnalyticsRepository as AR` | Bloquear | Bloqueado | Alias de importação detectado pelo módulo/símbolo original |
| E-05 | G-OBR-02 | Violação direta | Remover o argumento `decisions` de `enriquecer_alertas()` | Bloquear | Bloqueado | Contrato nominal protegido |
| E-06 | G-OBR-02 | Legítimo | Usar fallback compatível dentro do próprio adapter | Permitir | Permitido | Exceção preservada |
| E-07 | G-OBR-02 | Bypass | Reexportar o adapter por `bridge.py` e consumi-lo pela UI | Bloquear | Permitido | Falso negativo por indirection/reexportação |
| E-08 | G-OBR-02 | Bypass | Chamada decisória em `if False` antes da chamada real, com `decisions` não governadas | Bloquear | Permitido | Falso negativo por ordem textual sem análise de fluxo |
| E-09 | G-OBR-03 | Violação direta | Criar `QUALITY_PARAMETER_FIELDS = ("ph", "turbidez")` | Bloquear | Bloqueado | Nome e coleção detectados |
| E-10 | G-OBR-03 | Legítimo | Importar função oficial com alias | Permitir | Permitido | Alias legítimo preservado |
| E-11 | G-OBR-03 | Bypass | Construir `("p" + "h", "tur" + "bidez")` | Bloquear | Permitido | Falso negativo por concatenação |
| E-12 | G-OBR-04 | Violação direta | Adicionar literal exato `Fora do padrão` | Bloquear | Bloqueado | Rótulo conhecido detectado |
| E-13 | G-OBR-04 | Legítimo | Adicionar `Status executivo observacional` | Permitir | Permitido | Falso positivo histórico não reapareceu |
| E-14 | G-OBR-04 | Bypass | Construir `"Fora do " + "padrão"` | Bloquear | Permitido | Falso negativo por concatenação |
| E-15 | G-OBR-05 | Violação direta | Adicionar `import csv` em Executive | Bloquear | Bloqueado | Import direto detectado |
| E-16 | G-OBR-05 | Legítimo | Importar `monitoramento_hidrico.status_semantics` | Permitir | Permitido | Exceção oficial preservada |
| E-17 | G-OBR-05 | Bypass | Reexportar `PolicyEngine` por `executive.bridge` | Bloquear | Permitido | Falso negativo por reexportação e arquivo não enumerado |
| E-18 | G-OBR-05 | Bypass | Obter `PolicyEngine` por `__import__()` e `getattr()` | Bloquear | Permitido | Falso negativo por importação dinâmica |

## 9. Resultados na árvore de trabalho atual

### 9.1 Resultado nominal

Os cinco testes são aprovados na árvore atual.

### 9.2 Cobertura atual das listas

Na data da auditoria:

* os nove arquivos Python existentes na raiz que representam as superfícies enumeradas estão em `PRESENTATION_FILES`;
* os sete arquivos funcionais de Analytics, excluído `__init__.py`, estão em `ANALYTICS_FILES`;
* os seis arquivos funcionais de Executive e Executive Recommendation, excluídos `__init__.py`, estão em `EXECUTIVE_FILES`;
* os cinco adapters relacionados a parâmetros de qualidade estão em `QUALITY_ADAPTER_FILES`.

A cobertura dos arquivos atualmente conhecidos é consistente. Entretanto, não existe descoberta automática: um arquivo novo não incluído manualmente permanece invisível, como demonstrado por E-03 e E-17.

### 9.3 Qualidade das mensagens

Nas cinco violações diretas:

* todas as mensagens incluíram o ID do guardrail;
* todas identificaram o arquivo responsável;
* G-OBR-03 e G-OBR-04 incluíram linha precisa;
* G-OBR-01, G-OBR-02 e G-OBR-05 identificaram arquivo e evidência, mas não a linha do import ou chamada;
* quando uma mutação gerou múltiplas evidências, G-OBR-01 e G-OBR-03 as agregaram de modo compreensível.

### 9.4 Falsos positivos

Nenhum falso positivo foi observado nos cinco casos legítimos desta auditoria.

O falso positivo histórico da GP-PE-16 sobre `Status executivo observacional` não reapareceu: o título legítimo foi aprovado em E-13.

### 9.5 Falsos negativos

Foi observado ao menos um falso negativo em cada guardrail:

* G-OBR-01: arquivo novo fora da lista;
* G-OBR-02: reexportação e fluxo de controle incompatível com a ordem textual;
* G-OBR-03: concatenação de identificadores;
* G-OBR-04: concatenação de rótulo proibido;
* G-OBR-05: reexportação e importação dinâmica por `getattr`.

Portanto, a aprovação atual demonstra proteção de padrões diretos conhecidos, não prevenção geral de regressões arquiteturais.

## 10. Resultados no HEAD isolado

### 10.1 Resultado da execução

| Guardrail | Resultado no HEAD | Evidência |
| --- | --- | --- |
| G-OBR-01 | Falha de asserção | `main.py` versionado importa e instancia `AnalyticsRepository` e `WaterHealthScoreCalculator` |
| G-OBR-02 | Erro antes do parecer | `analytics/dashboard_snapshot.py` não existe no HEAD |
| G-OBR-03 | Erro antes do parecer | `monitoramento_hidrico/dashboard_adapter.py` não existe no HEAD |
| G-OBR-04 | Erro antes do parecer | `monitoramento_hidrico/dashboard_adapter.py` não existe no HEAD |
| G-OBR-05 | Aprovado | Os seis arquivos Executive versionados não apresentaram o padrão direto proibido |

### 10.2 Não conformidades versionadas observáveis

Além dos erros de arquivo ausente:

* `governance/service.py` no HEAD chama `enriquecer_alertas(snapshot.alerts)` sem produzir ou fornecer `decisions`; a autoridade exigida por G-OBR-02 não está versionada;
* nenhum adapter versionado contém referência a `quality_parameter_mapping`; a centralização exigida por G-OBR-03 não está reproduzida;
* `quality_parameter_mapping.py` está ausente do HEAD;
* o HEAD ainda contém `Dentro do padrão`, `Fora do padrão` e `Status Executivo` em componentes examinados por G-OBR-04;
* `status_semantics.py` está ausente do HEAD.

Os erros de arquivo ausente mascaram falhas adicionais que seriam esperadas caso a execução prosseguisse. Nenhum arquivo local foi incorporado à exportação para contornar esses resultados.

## 11. Reprodutibilidade em checkout ou exportação limpa

O teste PA-01E **não é reproduzível com aprovação** a partir do `HEAD` auditado.

Razões:

1. fontes enumeradas pelos testes estão ausentes;
2. fontes de autoridade declaradas estão ausentes;
3. a GP-PE-15 não está versionada;
4. o conteúdo versionado de `main.py` viola G-OBR-01;
5. o conteúdo versionado de Governança não implementa a cadeia exigida por G-OBR-02;
6. a fonte central exigida por G-OBR-03 não existe no HEAD;
7. o vocabulário versionado ainda contém rótulos proibidos por G-OBR-04.

A aprovação observada na árvore atual depende de conteúdo local não versionado e de alterações rastreadas ainda não incorporadas ao `HEAD`.

## 12. Parecer individual por guardrail

### 12.1 G-OBR-01

| Critério | Avaliação |
| --- | --- |
| Requisito de origem | Proibir UI de acessar diretamente `AnalyticsRepository` e `WaterHealthScoreCalculator` |
| Fronteira | UI → Analytics interno |
| Arquivos cobertos | Nove superfícies em `PRESENTATION_FILES` |
| Técnica | AST de imports, símbolos importados e nomes chamados |
| Violação direta | Detectada |
| Caso legítimo | `DashboardAnalyticsSnapshotService` permitido |
| Bypass | Novo arquivo não enumerado permitido indevidamente |
| Alias | `AnalyticsRepository as AR` detectado pelo import original |
| Mensagem | Clara; ID e arquivo presentes; sem linha precisa |
| Falso positivo | Nenhum observado |
| Falso negativo | Arquivo novo fora da lista |
| Dependência fixa | Alta: caminhos, módulos e nomes de classes |
| Cobertura | Alta para os arquivos atuais; baixa para crescimento não enumerado |
| Precisão | Alta para dependências diretas conhecidas |
| Robustez | Média-baixa |
| Manutenibilidade | Média; exige atualização manual da lista |
| Risco residual | Alto para novas telas e indirection |
| Estado no HEAD | Executável, mas detecta violação real em `main.py` |
| Parecer individual | **PARCIALMENTE EFETIVO** |

### 12.2 G-OBR-02

| Critério | Avaliação |
| --- | --- |
| Requisito de origem | Preservar Governança como autoridade primária da reavaliação |
| Fronteira | `OperationalGovernanceService` → adapter |
| Arquivos cobertos | `governance/service.py` e 22 consumidores externos enumerados |
| Técnica | AST de classe/método, chamadas, argumento `decisions`, número de linha e imports |
| Violação direta | Ausência de `decisions` detectada |
| Caso legítimo | Fallback dentro do adapter permitido |
| Bypass | Reexportação indireta permitida |
| Bypass de fluxo | Chamada decisória dentro de `if False` satisfez a ordem textual |
| Mensagem | Clara; ID, arquivo e causa presentes; sem linha precisa |
| Falso positivo | Nenhum observado |
| Falso negativo | Reexportação e autoridade apenas nominal em ramo inalcançável |
| Dependência fixa | Muito alta: nomes de classe, método, variável, chamada e listas |
| Cobertura | Média para a forma atual; não prova fluxo de autoridade |
| Precisão | Alta para a forma nominal direta |
| Robustez | Baixa contra alterações de controle e indirection |
| Manutenibilidade | Média-baixa; refatoração legítima pode quebrar o teste |
| Risco residual | Alto |
| Estado no HEAD | Teste termina em erro; cadeia governada também não está versionada |
| Parecer individual | **NÃO REPRODUZÍVEL NO HEAD**; na árvore atual, parcialmente efetivo |

### 12.3 G-OBR-03

| Critério | Avaliação |
| --- | --- |
| Requisito de origem | Impedir recriação de listas locais de parâmetros de qualidade |
| Fronteira | Adapters → fonte central PA-01C |
| Arquivos cobertos | Cinco adapters enumerados |
| Técnica | AST de imports, atribuições e strings em coleções |
| Violação direta | Autoridade conhecida e coleção literal detectadas |
| Caso legítimo | Importação da função oficial com alias permitida |
| Bypass | Parâmetros construídos por concatenação permitidos |
| Mensagem | Muito clara; ID, arquivo, linha e valores presentes |
| Falso positivo | Nenhum observado |
| Falso negativo | Construção dinâmica ou concatenada; lista unitária não é bloqueada |
| Dependência fixa | Alta: cinco caminhos, cinco nomes de autoridades e cinco identificadores |
| Cobertura | Média para duplicações literais conhecidas |
| Precisão | Alta para padrões diretos |
| Robustez | Média-baixa |
| Manutenibilidade | Média; exige sincronização manual de nomes e adapters |
| Risco residual | Médio-alto |
| Estado no HEAD | Teste termina em erro; fonte central e adapter enumerado estão ausentes |
| Parecer individual | **NÃO REPRODUZÍVEL NO HEAD**; na árvore atual, parcialmente efetivo |

### 12.4 G-OBR-04

| Critério | Avaliação |
| --- | --- |
| Requisito de origem | Impedir novos textos funcionais fora do vocabulário oficial |
| Fronteira | Comunicação de status → PA-01A |
| Arquivos cobertos | 27 arquivos enumerados de apresentação, adapters, Analytics e Executive |
| Técnica | AST de strings, normalização Unicode e igualdade com quatro rótulos proibidos |
| Violação direta | Literal exato proibido detectado |
| Caso legítimo | `Status executivo observacional` permitido |
| Bypass | Rótulo proibido construído por concatenação permitido |
| Mensagem | Muito clara; ID, arquivo, linha e rótulo presentes |
| Falso positivo | Nenhum na auditoria; falso positivo histórico foi corrigido na GP-PE-16 |
| Falso negativo | Concatenação, f-string, variante não listada e qualquer texto novo fora dos quatro rótulos |
| Dependência fixa | Muito alta: caminhos e denylist de quatro strings duplicada no teste |
| Cobertura | Baixa em relação ao requisito amplo de vocabulário oficial |
| Precisão | Alta para os quatro rótulos exatos |
| Robustez | Baixa |
| Manutenibilidade | Baixa; não deriva a política de `STATUS_SEMANTICS` |
| Risco residual | Alto |
| Estado no HEAD | Teste termina em erro; há rótulos proibidos e autoridade oficial ausente |
| Parecer individual | **NÃO REPRODUZÍVEL NO HEAD**; na árvore atual, nominalmente efetivo |

### 12.5 G-OBR-05

| Critério | Avaliação |
| --- | --- |
| Requisito de origem | Impedir Executive de acessar CSV, motores ou adapters hídricos diretamente |
| Fronteira | Executive → persistência e Monitoramento Hídrico |
| Arquivos cobertos | Seis arquivos Executive e Executive Recommendation |
| Técnica | AST de imports, nomes chamados e strings terminadas em `.csv` |
| Violação direta | `import csv` detectado |
| Caso legítimo | `monitoramento_hidrico.status_semantics` permitido |
| Bypass | Reexportação por novo módulo permitida |
| Bypass dinâmico | `__import__()` + `getattr()` permitido |
| Mensagem | Clara; ID, arquivo e import presentes; sem linha precisa |
| Falso positivo | Nenhum observado |
| Falso negativo | Reexportação, importação dinâmica, wrapper intermediário e arquivo novo |
| Dependência fixa | Alta: seis caminhos, módulos e nomes de classes |
| Cobertura | Média para acessos diretos conhecidos |
| Precisão | Alta para imports diretos; exceção oficial preservada |
| Robustez | Baixa contra indirection |
| Manutenibilidade | Média-baixa; exige atualização manual de arquivos e símbolos |
| Risco residual | Alto |
| Estado no HEAD | Executa e é aprovado isoladamente |
| Parecer individual | **PARCIALMENTE EFETIVO** |

## 13. Achados

| ID | Achado | Severidade | Evidência | Bloqueante para plena efetividade? |
| --- | --- | --- | --- | --- |
| PE17-A01 | A aprovação local depende de arquivos não rastreados e fontes modificadas | Alta | Proveniência e falha no export do HEAD | Sim |
| PE17-A02 | GP-PE-15, fonte declarada de autoridade, não está no HEAD | Alta | `git status` e `git cat-file` | Sim para rastreabilidade formal |
| PE17-A03 | O teste completo não é reproduzível em exportação limpa | Alta | 1 falha e 3 erros em 5 testes | Sim |
| PE17-A04 | G-OBR-01 encontra violação real no `main.py` versionado | Alta | Execução limpa | Sim |
| PE17-A05 | G-OBR-02 usa ordem por linha, não fluxo de controle | Alta | E-08 aprovado indevidamente | Sim para robustez da autoridade |
| PE17-A06 | G-OBR-04 protege quatro rótulos exatos, não o vocabulário oficial completo | Alta | Implementação e E-14 | Sim para o requisito amplo |
| PE17-A07 | Todos os guardrails dependem de listas, nomes ou caminhos fixos | Média | Constantes e mutações | Não isoladamente |
| PE17-A08 | Cada guardrail possui ao menos um bypass demonstrado | Alta | E-03, E-07/E-08, E-11, E-14, E-17/E-18 | Sim |
| PE17-A09 | Violações diretas geram mensagens rastreáveis | Positiva | E-01, E-05, E-09, E-12 e E-15 | Não |
| PE17-A10 | Os cinco casos legítimos permaneceram aprovados | Positiva | E-02, E-06, E-10, E-13 e E-16 | Não |

## 14. Limitações da auditoria

* As 18 mutações são representativas, não exaustivas.
* Não foram testadas todas as combinações de alias, monkey patching, metaprogramação ou carregamento de módulos.
* Os arquivos mutados foram analisados estaticamente; o runtime mutado não foi executado.
* A auditoria avaliou a árvore observada em um ponto temporal específico.
* Não foi realizada correção para confirmar se recomendações futuras eliminariam os bypasses.
* A ausência de falso positivo nos cinco casos legítimos não prova ausência geral de falsos positivos.
* A falha do HEAD impede obter parecer executável completo de G-OBR-02 a G-OBR-04 sem incorporar conteúdo ausente, o que foi corretamente evitado.

## 15. Riscos residuais

1. Novos arquivos podem ficar totalmente fora da proteção.
2. Reexportações podem ocultar dependências proibidas.
3. Imports dinâmicos e `getattr` podem escapar das verificações por nomes chamados.
4. Ordem textual pode ser confundida com autoridade efetiva em fluxo de controle.
5. Literais concatenados ou produzidos dinamicamente podem escapar de G-OBR-03 e G-OBR-04.
6. A denylist semântica pode aprovar novos rótulos incompatíveis por não conhecê-los.
7. A suíte pode passar localmente e falhar em CI ou checkout limpo por dependência de arquivos não versionados.
8. A ausência da GP-PE-15 no HEAD quebra a cadeia documental de autoridade.

## 16. Recomendações não implementadas

1. Versionar, em mudança governada separada, as fontes necessárias e a autoridade documental GP-PE-15 antes de alegar reprodutibilidade.
2. Exigir validação da PA-01E em checkout limpo como condição de encerramento futuro.
3. Substituir ou complementar listas manuais por descoberta controlada de módulos ou manifesto arquitetural versionado.
4. Acrescentar testes de mutação permanentes para violações diretas, usos legítimos e bypasses conhecidos.
5. Analisar o grafo de imports para detectar reexportações e wrappers intermediários.
6. Complementar G-OBR-02 com teste comportamental ou análise de fluxo/dados que prove a origem de `decisions`.
7. Complementar G-OBR-03 com avaliação de constantes e expressões construídas.
8. Redefinir G-OBR-04 a partir da autoridade oficial versionada, evitando depender apenas de quatro rótulos proibidos.
9. Complementar G-OBR-05 com proteção de imports dinâmicos e dependências transitivas.
10. Incluir linha precisa nas mensagens de G-OBR-01, G-OBR-02 e G-OBR-05 quando tecnicamente viável.

Essas recomendações não autorizam alteração automática de testes ou arquitetura.

## 17. Critérios para futura remediação

Uma futura GP de remediação deverá, no mínimo:

1. receber autorização específica;
2. preservar o escopo arquitetural da PA-01E;
3. versionar todas as fontes necessárias antes da validação;
4. tornar GP-PE-15 e a cadeia documental acessíveis no HEAD;
5. executar os cinco testes com sucesso em checkout limpo;
6. demonstrar que violações diretas continuam bloqueadas;
7. demonstrar que usos legítimos continuam aprovados;
8. detectar ou mitigar explicitamente os bypasses E-03, E-07, E-08, E-11, E-14, E-17 e E-18;
9. registrar limitações que permanecerem conscientemente aceitas;
10. submeter a remediação a nova auditoria independente antes de declarar plena efetividade.

## 18. Parecer geral

### 18.1 Árvore de trabalho atual

Parecer: **PA-01E PARCIALMENTE EFETIVA NA ÁRVORE ATUAL**.

Justificativa: os cinco testes nominais passam, todas as violações diretas foram detectadas, aliases diretos relevantes foram tratados e os casos legítimos foram preservados. Entretanto, cada guardrail admitiu ao menos um bypass representativo, e G-OBR-04 possui cobertura substancialmente menor que seu requisito declarado.

### 18.2 Conteúdo versionado no HEAD

Parecer: **PA-01E NÃO REPRODUZÍVEL NO HEAD**.

Justificativa: a suíte termina com uma falha e três erros; fontes necessárias e a autoridade documental estão ausentes; existem diferenças materiais entre o conteúdo versionado e a árvore local aprovada.

### 18.3 Checkout ou exportação limpa

Parecer: **NÃO APROVADO COMO MECANISMO REPRODUZÍVEL**.

O checkout limpo não consegue reproduzir a aprovação local sem incorporar arquivos não rastreados, operação expressamente proibida e metodologicamente inadequada.

### 18.4 Parecer conjunto

Os guardrails constituem uma barreira útil contra regressões diretas e conhecidas, com mensagens adequadas e boa precisão nos casos testados. Contudo, não formam ainda um mecanismo único, robusto e reproduzível de proteção da PA-01E.

Parecer final da GP-PE-17: **GUARDRAILS PARCIALMENTE EFETIVOS NA ÁRVORE ATUAL E NÃO REPRODUZÍVEIS NO HEAD**.

A GP-PE-17 está concluída como auditoria. Este parecer não altera a arquitetura oficial, não corrige os achados e não autoriza implementação das recomendações.

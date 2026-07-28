# Mapa Arquitetural Institucional do H&A

## 1. Visão Arquitetural Geral

O H&A possui uma arquitetura institucional orientada pela separação de responsabilidades, pela autoridade explícita e pela regra de fonte única de verdade — SSOT — para estados críticos.

Em alto nível, a organização abrange observação e contexto de mercado, geração e seleção de oportunidades, decisão e risco, execução, gestão de posições e estado operacional. A esses domínios vinculam-se inteligência adaptativa, memória, interface, auditoria e reconciliação.

A Constituição do H&A delimita as autoridades operacionais. O Perfil Institucional consolida a finalidade e o escopo tecnológico. O Inventário de Evidências registra o patrimônio reconhecido, enquanto o Relatório de Integração e a Reconciliação Patrimonial sustentam sua origem e seu tratamento documental.

O diagrama abaixo representa somente relações institucionais documentadas. Ele não descreve código, implantação ou sequência técnica completa.

```text
+---------------------------------------------------------------+
| CONSTITUIÇÃO DO H&A                                           |
| Autoridade explícita | SSOT | limites | evolução auditável    |
+-------------------------------+-------------------------------+
                                |
                                v
+-------------------+   +-------------------+   +---------------+
| Observação e      |-->| Oportunidades e   |-->| Decisão,      |
| contexto de       |   | seleção           |   | risco e       |
| mercado           |   |                   |   | capital       |
+-------------------+   +-------------------+   +-------+-------+
                                                          |
                                                          v
+-------------------+   +-------------------+   +---------------+
| Estado, posições  |<--| Execução          |<--| Orquestração  |
| e histórico       |   |                   |   | e ciclo       |
+-------------------+   +-------------------+   +---------------+
          ^                     ^                       ^
          |                     |                       |
+---------+-----------------------------------------------------+
| Memória, contexto, guidance, governança e adaptação            |
+---------------------------------------------------------------+
          ^                                             ^
          | observa e informa                             | solicita e observa
+---------+-------------------+             +-------------+-----+
| Auditoria e reconciliação   |             | Interface         |
| explicitamente separadas    |             | institucional     |
+-----------------------------+             +-------------------+

Controle documental:
Constituição + Perfil + Inventário + Integração + Reconciliação
```

Fontes: Constituição do H&A, artigos 1 a 15; `HA_INSTITUTIONAL_PROFILE.md`, seções 2, 3 e 6; `HA_EVIDENCE_INVENTORY.md`, seções 2, 3 e 7.

## 2. Organização Estrutural

A organização institucional está consolidada nos seguintes blocos:

* **governança constitucional:** estabelece autoridade, SSOT, limites de atuação e princípios de evolução;
* **observação e contexto:** reúne leitura, análise, qualidade e representação das condições de mercado;
* **oportunidades e elegibilidade:** abrange geração, classificação, ordenação e seleção estrutural;
* **decisão, risco e capital:** reúne autorização final, avaliação de contexto sistêmico, risco e alocação;
* **execução e posição:** separa a realização de ordens da autoridade sobre posições e histórico;
* **orquestração, ciclo e estado:** coordena slots, transições, locks, ciclos, heartbeat e estado operacional;
* **memória e inteligência adaptativa:** organiza memória, contexto, orientação, governança adaptativa e reentrada pós-operação;
* **interface:** solicita comandos por controladores institucionais e apresenta estados, métricas e alertas;
* **auditoria e reconciliação:** separa observação passiva de correção ativa explicitamente autorizada;
* **suporte patrimonial:** reúne documentação, histórico, baseline, testes, persistência, empacotamento e configurações reconhecidos no Inventário.

Os blocos descrevem responsabilidades institucionais. Não estabelecem estrutura de pacotes, arquivos, classes, funções ou dependências de implementação.

Fontes: Constituição do H&A, artigos 1 a 14; `HA_INSTITUTIONAL_PROFILE.md`, seções 3, 5 e 6; `HA_EVIDENCE_INVENTORY.md`, seção 7; `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-007` a `REC-026`.

## 3. Fluxo Institucional

O ciclo institucional parte da observação do mercado e da produção de contexto. O Radar gera oportunidades, enquanto MQII fornece a medida de qualidade do ambiente. A seleção determina a elegibilidade estrutural e a decisão exerce a autorização final de entrada, considerando contexto sistêmico, risco e capital.

O ciclo operacional é coordenado pelo `SlotController`, acionado periodicamente pelo `AutoLoop`. Quando há autorização, o `Executor` realiza ou simula a ordem. O `PositionManager` mantém a autoridade final sobre existência, abertura e fechamento de posições, histórico e resultados associados.

ALO utiliza eventos, memória e contexto para produzir orientação adaptativa, sem executar ordens, fechar posições ou substituir autoridades operacionais. DRC governa reentrada e cooldown pós-operação, sem criar posições.

A interface solicita ações e observa o estado por meio dos controladores institucionais. A auditoria observa e relata sem modificar estado. Quando uma correção de divergência é necessária, a reconciliação atua somente mediante chamada explícita.

Esse fluxo é conceitual: registra relações de autoridade e responsabilidade, não ordem de chamadas, protocolo de integração ou comportamento de runtime comprovado.

Fontes: Constituição do H&A, artigos 2 a 14; `HA_INSTITUTIONAL_PROFILE.md`, seções 2, 3 e 6; `HA_REPOSITORY_INTEGRATION_REPORT.md`, seções 3.5 e 5.

## 4. Governança Arquitetural

A Constituição do H&A é a referência para autoridade, estado e governança operacional. A regra SSOT impede que caches, snapshots, cópias locais ou estados auxiliares substituam a fonte oficial de um domínio crítico.

O controle documental da arquitetura é formado por:

* Perfil Institucional, que consolida identidade, finalidade, escopo e estado de evolução;
* Inventário de Evidências, que registra evidências, lacunas e ativos patrimoniais;
* Relatório de Integração, que documenta o universo encontrado no repositório oficial e seus limites de cobertura;
* Reconciliação Patrimonial, que decide o tratamento dos ativos e evita dupla contagem;
* este Mapa, que organiza as relações institucionais sem substituir documentação de implementação.

A rastreabilidade ocorre por seções, IDs institucionais, decisões `REC-xxx`, referências de origem e histórico das GPs. A evolução prescrita é incremental, aprovada e auditável, com preservação de contratos, logs, runtime, SSOT, soberania e comportamento operacional.

Fontes: Constituição do H&A, artigos 1, 12, 13 e 15; `HA_INSTITUTIONAL_PROFILE.md`, seções 6 e 7; `HA_EVIDENCE_INVENTORY.md`, seção 7; `HA_PATRIMONIAL_RECONCILIATION.md`, seções 2, 5 e 6.

## 5. Limites Arquiteturais

Pertencem ao escopo arquitetural institucional do H&A:

* os domínios de observação, seleção, decisão, risco, execução, posição, estado, interface, adaptação, auditoria e reconciliação;
* as autoridades e restrições estabelecidas pela Constituição;
* as relações conceituais entre os blocos;
* a estrutura documental e o patrimônio reconhecido que sustentam essas relações.

Não pertencem ao escopo deste mapa:

* detalhes de código, algoritmos, assinaturas, APIs, dependências e organização interna de implementação;
* afirmações sobre execução bem-sucedida, cobertura de testes, implantação ativa, continuidade operacional ou maturidade não comprovadas;
* reorganizações técnicas, novos componentes ou novos mecanismos de governança;
* ativos classificados como `Não incorporar` na Reconciliação Patrimonial;
* o tratamento de testes, configurações, documentação ou interface como fonte concorrente de autoridade sobre estados críticos.

Os ativos ICFACTORY integram o patrimônio documental e metodológico reconhecido do H&A, mas não substituem a Constituição específica do projeto nem ampliam, por si mesmos, as autoridades operacionais nela definidas.

Fontes: Constituição do H&A, artigos 1 a 15; `HA_INSTITUTIONAL_PROFILE.md`, seções 1, 3, 4 e 6; `HA_REPOSITORY_INTEGRATION_REPORT.md`, seções 3.5, 3.6 e 5; `HA_PATRIMONIAL_RECONCILIATION.md`, seções 3.4 e 6.

## 6. Evidências Arquiteturais

| Documento institucional | Sustentação arquitetural |
| --- | --- |
| Constituição do H&A — `CONSTITUTION.md` | Autoridades, SSOT, responsabilidades, auditoria, reconciliação, interface e princípio de evolução |
| `HA_INSTITUTIONAL_PROFILE.md` | Identidade, finalidade, escopo tecnológico, estado de evolução e síntese de governança |
| `HA_EVIDENCE_INVENTORY.md` | Evidências, lacunas e patrimônio arquitetural consolidado |
| `HA_REPOSITORY_INTEGRATION_REPORT.md` | Cobertura do acervo, arquitetura textual identificada e limites de comprovação |
| `HA_PATRIMONIAL_RECONCILIATION.md` | Decisões de representação, complementação, incorporação e não incorporação patrimonial |

Esses cinco documentos formam a base exclusiva deste mapa. A presença de código, testes e configurações é considerada somente conforme registrada nessas fontes, sem consulta ou interpretação direta da implementação.

## 7. Evolução Arquitetural

As linhas de evolução já reconhecidas concentram-se em:

* verificar a correspondência entre a arquitetura declarada e o runtime efetivo;
* produzir ou complementar diagrama técnico autônomo, documentação formal de API e manual operacional completo;
* verificar ambiente implantado, execução e cobertura dos testes;
* documentar logs, dados, período, frequência e continuidade operacional;
* preservar contratos, logs, rastreabilidade, SSOT, soberania institucional e comportamento operacional durante mudanças;
* manter alterações pequenas, aprovadas e auditáveis;
* submeter novas incorporações patrimoniais a processo controlado e rastreável.

Essas linhas reproduzem lacunas e diretrizes já registradas. Não constituem proposta de reorganização, previsão de conclusão ou ampliação de escopo.

Fontes: Constituição do H&A, artigo 15; `HA_INSTITUTIONAL_PROFILE.md`, seções 4 e 8; `HA_EVIDENCE_INVENTORY.md`, seções 3, 6 e 7; `HA_REPOSITORY_INTEGRATION_REPORT.md`, seções 5 e 6; `HA_PATRIMONIAL_RECONCILIATION.md`, seções 5 e 7.

## 8. Conclusão Institucional

A arquitetura institucional do H&A organiza observação, contexto, oportunidades, seleção, decisão, risco, execução, posição, estado, adaptação, interface, auditoria e reconciliação sob autoridades delimitadas.

Seu princípio central é impedir soberania concorrente: cada estado crítico deve possuir fonte oficial, cada componente deve permanecer dentro de sua responsabilidade e qualquer correção ativa deve ser separada da auditoria passiva.

O projeto possui base constitucional, perfil institucional, inventário consolidado e cadeia documental de integração e reconciliação. O mapa torna essa organização consultável em alto nível, sem afirmar validação do runtime e sem substituir documentação técnica de implementação.

Fontes: Constituição do H&A; `HA_INSTITUTIONAL_PROFILE.md`, seções 4 a 7; `HA_EVIDENCE_INVENTORY.md`, seção 7; `HA_REPOSITORY_INTEGRATION_REPORT.md`, seções 5 a 7; `HA_PATRIMONIAL_RECONCILIATION.md`, seção 7.

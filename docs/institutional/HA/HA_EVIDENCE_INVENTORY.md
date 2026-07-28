# Inventário de Evidências do H&A

Este inventário registra exclusivamente evidências relativas ao projeto H&A localizadas no repositório em 23/07/2026. A existência de uma referência documental secundária não comprova infraestrutura, componente implementado, funcionalidade ou operação.

Em 23/07/2026, o inventário recebeu a consolidação patrimonial autorizada pela GP-HA-04. Os ativos incorporados na seção 7 derivam exclusivamente das decisões `Complementar` e `Inédito` da Reconciliação Patrimonial. As linhas, os IDs e as classificações anteriormente aprovados permanecem inalterados.

Classificações utilizadas:

* `Comprovado`: a existência do documento ou da evidência primária indicada pode ser verificada no repositório.
* `Parcialmente Comprovado`: existe referência documental, mas falta fonte primária ou comprovação suficiente do objeto referido.
* `Não Comprovado`: nenhuma evidência documental suficiente foi localizada.

## 1. Infraestrutura

| Código | Item | Classificação | Fonte documental | Resultado objetivo |
| --- | --- | --- | --- | --- |
| HA-INF-001 | Repositório ou diretório próprio do H&A | Não Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | As fontes registram ausência de documentação primária do H&A; nenhum repositório ou diretório do projeto foi identificado. |
| HA-INF-002 | Ambiente de execução | Não Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`TEC-HA-002`) | Não há ambiente, versão, plataforma ou requisito de execução documentado. |
| HA-INF-003 | Infraestrutura de persistência | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | Não há banco de dados, arquivos de persistência, schemas ou repositórios de dados do H&A documentados. |
| HA-INF-004 | Infraestrutura de implantação ou operação | Não Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`OPE-009`) | Não há ambiente implantado, período de operação ou configuração operacional comprovada. |

## 2. Componentes existentes

| Código | Item | Classificação | Fonte documental | Resultado objetivo |
| --- | --- | --- | --- | --- |
| HA-COM-001 | Fluxo nominal H&A | Parcialmente Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`; `docs/institutional/TECHNOLOGY_PORTFOLIO.md`; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`TEC-HA-001`) | O fluxo `Memory -> Context -> Guidance -> Governance -> Decision` é reportado por fontes secundárias; não há especificação primária. |
| HA-COM-002 | Memory | Parcialmente Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`, seção “Comparação Com H&A” | O nome aparece no fluxo reportado; implementação, responsabilidade e interfaces não estão documentadas por fonte primária. |
| HA-COM-003 | Context | Parcialmente Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`, seção “Comparação Com H&A” | O nome aparece no fluxo reportado; implementação, responsabilidade e interfaces não estão documentadas por fonte primária. |
| HA-COM-004 | Guidance | Parcialmente Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`, seção “Comparação Com H&A” | O nome aparece no fluxo reportado; implementação, responsabilidade e interfaces não estão documentadas por fonte primária. |
| HA-COM-005 | Governance | Parcialmente Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`, seção “Comparação Com H&A” | O nome aparece no fluxo reportado; implementação, responsabilidade e interfaces não estão documentadas por fonte primária. |
| HA-COM-006 | Decision | Parcialmente Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`, seção “Comparação Com H&A” | O nome aparece no fluxo reportado; implementação, responsabilidade e interfaces não estão documentadas por fonte primária. |
| HA-COM-007 | Arquitetura técnica do H&A | Não Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`TEC-HA-002`, `LAC-002`) | Não há diagrama, contrato, módulo, dependência ou documento arquitetural primário disponível. |
| HA-COM-008 | Código-fonte ou módulos executáveis | Não Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | Nenhum código ou módulo foi identificado como pertencente ao H&A. |

## 3. Evidências operacionais

| Código | Item | Classificação | Fonte documental | Resultado objetivo |
| --- | --- | --- | --- | --- |
| HA-OPE-001 | Existência operacional reportada | Parcialmente Comprovado | `docs/institutional/ICFACTORY_CONSTITUTION.md`, seção 2; `docs/institutional/TECHNOLOGY_PORTFOLIO.md`, seção PT-02; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`OPE-009`) | A operação é mencionada institucionalmente, mas não possui fonte operacional primária no repositório. |
| HA-OPE-002 | Registros operacionais | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`OPE-009`, `LAC-002`) | Não há registros operacionais primários disponíveis. |
| HA-OPE-003 | Logs | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`OPE-009`, `LAC-002`) | Não há logs do H&A disponíveis. |
| HA-OPE-004 | Dados de entrada ou saída | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | Não há amostras, schemas, conjuntos de dados ou resultados atribuíveis ao H&A. |
| HA-OPE-005 | Testes | Não Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`, seção PT-02 | Testes são indicados como evidência necessária antes de ampliar a maturidade; nenhum teste do H&A foi localizado. |
| HA-OPE-006 | Auditoria primária do projeto | Não Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md` | A fonte recomenda auditoria futura com documentos primários e declara que a comparação existente é indício, não prova. |
| HA-OPE-007 | Período, frequência ou continuidade da operação | Não Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`, seção PT-02 | A evidência de ambiente e período de operação é indicada como pendente. |

## 4. Documentação existente

| Código | Item | Classificação | Fonte documental | Resultado objetivo |
| --- | --- | --- | --- | --- |
| HA-DOC-001 | Documentação primária do H&A | Não Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`; `docs/institutional/AGIPI/EVIDENCE_DOSSIER.md` (`EVD-HA-002`) | A ausência de documentos primários é declarada; o dossiê registra a documentação primária como lacuna. |
| HA-DOC-002 | Comparação documental GP-R02 | Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md` | O documento existe e registra o fluxo reportado, a ausência de fontes primárias e o limite de uso como indício. |
| HA-DOC-003 | Registro no portfólio tecnológico | Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`, seção PT-02 | O documento existe e classifica H&A como referência conceitual provisória baseada em pesquisa secundária. |
| HA-DOC-004 | Registro no Inventário Institucional de Ativos | Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`TEC-HA-001`, `TEC-HA-002`, `OPE-009`, `LAC-002`) | O documento existe e consolida evidência secundária e lacunas primárias. |
| HA-DOC-005 | Registro no Dossiê de Evidências | Comprovado | `docs/institutional/AGIPI/EVIDENCE_DOSSIER.md` (`EVD-HA-001`, `EVD-HA-002`) | O fluxo é catalogado como evidência candidata secundária; a documentação primária permanece lacuna. |
| HA-DOC-006 | Menção na Constituição Institucional | Comprovado | `docs/institutional/ICFACTORY_CONSTITUTION.md`, seção 2 | O documento registra experiência operacional reportada, sem apresentar prova operacional primária. |
| HA-DOC-007 | Síntese no Mapa Institucional | Comprovado | `docs/institutional/INSTITUTIONAL_MAP.md`, seções 7 e 8 | O documento preserva a situação `Parcialmente Validado` e a ausência de documentação primária. |
| HA-DOC-008 | Síntese no Perfil Institucional | Comprovado | `docs/institutional/INSTITUTIONAL_PROFILE.md`, seções 5 e 7 | O documento preserva a situação parcialmente validada e as lacunas documentais. |
| HA-DOC-009 | Constituição, ficha técnica ou manual próprios do H&A | Não Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | Nenhum desses documentos primários foi localizado. |

## 5. Materiais de demonstração

| Código | Item | Classificação | Fonte documental | Resultado objetivo |
| --- | --- | --- | --- | --- |
| HA-DEM-001 | Capturas de tela | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | Nenhuma captura identificada como pertencente ao H&A foi localizada. |
| HA-DEM-002 | Vídeos | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | Nenhum vídeo identificado como pertencente ao H&A foi localizado. |
| HA-DEM-003 | Apresentação ou roteiro de demonstração | Não Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | Nenhum material primário de apresentação ou demonstração foi localizado. |
| HA-DEM-004 | Ambiente demonstrável | Não Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`, seção PT-02 | Não há ambiente, instrução de execução ou evidência de demonstração disponível. |

## 6. Lacunas identificadas

| Código | Lacuna | Classificação | Fonte documental | Consequência documental |
| --- | --- | --- | --- | --- |
| HA-LAC-001 | Constituição ou documento de identidade do H&A | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | Identidade, propósito, escopo e autoridade próprios não podem ser confirmados. |
| HA-LAC-002 | Arquitetura e componentes primários | Não Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`; `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | O fluxo reportado não pode ser confirmado como arquitetura implementada. |
| HA-LAC-003 | Versões e histórico de evolução | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`TEC-HA-002`, `LAC-002`) | Não é possível estabelecer baseline ou cronologia técnica. |
| HA-LAC-004 | Infraestrutura e ambiente | Não Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`, seção PT-02 | Não é possível reproduzir ou verificar execução. |
| HA-LAC-005 | Código, testes e auditorias primárias | Não Comprovado | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`; `docs/institutional/TECHNOLOGY_PORTFOLIO.md`, seção PT-02 | Não é possível verificar comportamento, qualidade ou conformidade. |
| HA-LAC-006 | Logs, dados e registros operacionais | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`OPE-009`, `LAC-002`) | A operação reportada não pode ser auditada. |
| HA-LAC-007 | Responsáveis e período de operação | Não Comprovado | `docs/institutional/TECHNOLOGY_PORTFOLIO.md`, seção PT-02 | Responsabilidade, contexto e continuidade operacional não podem ser estabelecidos. |
| HA-LAC-008 | Materiais de demonstração | Não Comprovado | `docs/institutional/AGIPI/INSTITUTIONAL_ASSET_INVENTORY.md` (`LAC-002`) | Não há demonstração verificável do projeto. |

## 7. Ativos incorporados pela Reconciliação Patrimonial

Os registros abaixo consolidam os ativos aprovados sem reclassificar os itens das seções 1 a 6. A coluna `Categoria patrimonial` reproduz a decisão da Reconciliação e não constitui classificação de evidência, maturidade ou funcionamento.

| ID institucional | Nome do ativo | Categoria patrimonial | Origem | Referência documental |
| --- | --- | --- | --- | --- |
| HA-PAT-001 | Repositório oficial e árvore rastreada do H&A | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-007` |
| HA-PAT-002 | Baseline de execução e empacotamento | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-008` |
| HA-PAT-003 | Módulos de persistência e estado | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-009` |
| HA-PAT-004 | Configurações de processo e implantação | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-010` |
| HA-PAT-005 | Arquitetura técnica textual e estrutura modular | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-011` |
| HA-PAT-006 | Código-fonte modular do H&A | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-012` |
| HA-PAT-007 | Conjunto de testes rastreados | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-013` |
| HA-PAT-008 | Documentação primária de auditoria | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-014` |
| HA-PAT-009 | Constituição, guia operacional e léxico próprios do H&A | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-015` |
| HA-PAT-010 | Histórico, roadmap e baseline versionada | Complementar | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-016` |
| HA-PAT-011 | Família documental ICFACTORY incorporada ao repositório H&A | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-017` |
| HA-PAT-012 | Metodologia ACI | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-018` |
| HA-PAT-013 | Arquitetura Lógica Operacional — ALO | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-019` |
| HA-PAT-014 | Conceito CIE-X | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-020` |
| HA-PAT-015 | Conceito OSE | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-021` |
| HA-PAT-016 | Arquitetura de governança em três níveis | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-022` |
| HA-PAT-017 | Léxico constitucional consolidado | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-023` |
| HA-PAT-018 | Modelos de constituição de projeto | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-024` |
| HA-PAT-019 | Marco histórico H&A–ALFRED IA | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-025` |
| HA-PAT-020 | Documentação e configuração da UI | Inédito | Reconciliação Patrimonial | `HA_PATRIMONIAL_RECONCILIATION.md`, `REC-026` |

### Auditoria do inventário consolidado

* Todas as linhas das seções 1 a 6 utilizam exclusivamente `Comprovado`, `Parcialmente Comprovado` ou `Não Comprovado`.
* Itens `Comprovado` referem-se apenas à existência de documentos locais, não às capacidades do H&A.
* O fluxo nominal foi classificado como `Parcialmente Comprovado` porque deriva de fonte secundária.
* Infraestrutura, implementação, arquitetura, operação, dados, testes e demonstrações sem fonte primária foram classificados como `Não Comprovado`.
* A pesquisa de Governança de Harnesses não foi tratada como evidência do projeto H&A.
* Os 40 IDs existentes nas seções 1 a 6 foram preservados sem alteração.
* Vinte ativos foram incorporados na seção 7: dez `Complementar` e dez `Inédito`.
* Cada novo ID possui origem na Reconciliação Patrimonial e referência única entre `REC-007` e `REC-026`.
* Ativos `Já representado` e candidatos `Não incorporar` não foram adicionados.
* As categorias patrimoniais da seção 7 não alteram as classificações de evidência das seções anteriores.
* A incorporação reconhece patrimônio documental; não comprova execução, implantação, operação, qualidade ou maturidade.

**Veredito:** o inventário consolida as evidências anteriormente aprovadas e os vinte ativos autorizados pela Reconciliação Patrimonial, com rastreabilidade própria e sem alteração das classificações existentes. A consolidação patrimonial não constitui comprovação de execução, implantação, operação, qualidade ou maturidade.

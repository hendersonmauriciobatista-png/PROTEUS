# Dossiê de Evidências Institucionais da ICFACTORY

## Objetivo

Fornecer a estrutura canônica para catalogar evidências destinadas à validação institucional. Este documento é um índice; ele não substitui os arquivos-fonte nem transforma referências em evidência validada.

## Regras de inclusão

1. Cada evidência recebe código único e fonte recuperável.
2. Evidência primária, secundária, relato e inferência são classificados separadamente.
3. Cópias preservam autoria, data, versão, licença e hash quando aplicável.
4. Materiais sensíveis recebem controle de acesso.
5. O status “validada” exige revisão humana identificada.
6. Ausência de evidência é registrada como lacuna, não preenchida por suposição.

## Status permitidos

* `CANDIDATA` — identificada, ainda não verificada.
* `EM_VERIFICAÇÃO` — integridade, origem ou pertinência em análise.
* `VALIDADA_INTERNAMENTE` — verificada por responsável humano da ICFACTORY.
* `VALIDADA_EXTERNAMENTE` — verificada por terceiro identificado, com escopo registrado.
* `RESTRITA` — válida, mas sujeita a controle de acesso.
* `REJEITADA` — inadequada, inconsistente ou sem proveniência suficiente.
* `LACUNA` — evidência necessária ainda indisponível.

## Catálogo inicial

| Código | Descrição | Projeto de origem | Fonte | Tipo | Status | Observações |
| --- | --- | --- | --- | --- | --- | --- |
| EVD-PRO-001 | Constituição do Projeto | PROTEUS | `docs/governance/PROJECT_CONSTITUTION.md` | Primária documental | CANDIDATA | Verificar aprovação e versão. |
| EVD-PRO-002 | Ficha técnica institucional | PROTEUS | `docs/institutional/TECHNICAL_DATASHEET.md` | Primária documental | CANDIDATA | Conferir contra código e ambiente atual. |
| EVD-PRO-003 | Auditoria de consolidação arquitetural | PROTEUS | `docs/architecture/AC_01_ARCHITECTURAL_CONSOLIDATION_AUDIT.md` | Primária documental | CANDIDATA | Registrar escopo e ressalvas. |
| EVD-PRO-004 | Suíte e registros de testes | PROTEUS | `tests/` e históricos correlatos | Técnica | CANDIDATA | Capturar comando, ambiente, data e resultado atual. |
| EVD-PRO-005 | Kit institucional e demonstração | PROTEUS | `docs/institutional/` | Comunicação | CANDIDATA | Selecionar apenas capacidades existentes. |
| EVD-HA-001 | Fluxo H&A reportado | H&A | `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`; `docs/institutional/HA/HA_REPOSITORY_INTEGRATION_REPORT.md` | Secundária e primária documental | CANDIDATA | Fluxo localizado em fontes primárias; correspondência integral com runtime e validação humana permanecem pendentes. |
| EVD-HA-002 | Documentação primária do H&A | H&A | `docs/institutional/HA/HA_REPOSITORY_INTEGRATION_REPORT.md`; `docs/institutional/HA/HA_PATRIMONIAL_RECONCILIATION.md`; `docs/institutional/HA/HA_INSTITUTIONAL_DOSSIER.md` | Primária documental auditada | CANDIDATA | Constituição, governança, arquitetura textual, código, testes, histórico e roadmap inventariados; operação e validação humana não comprovadas. |
| EVD-HA-003 | Auditoria do núcleo institucional do H&A | H&A | `docs/institutional/HA/HA_INSTITUTIONAL_CORE_AUDIT.md` | Auditoria documental | CANDIDATA | Núcleo documental auditado; aguarda validação humana identificada e preserva ressalvas de custódia, classificação e validação funcional. |
| EVD-PRO-006 | Registro mestre e validação das evidências do Kit PROTEUS | PROTEUS | `docs/institutional/DOCUMENT_REGISTER.md`; `docs/institutional/GP_PD_04_EVIDENCE_VALIDATION_REPORT.md` | Governança e auditoria documental | CANDIDATA | Evidências classificadas por rastreabilidade; validação humana identificada e lacunas factuais externas permanecem pendentes. |
| EVD-OPT-001 | Ficha de concepção do OPTIMUS DRIVE | OPTIMUS DRIVE | A produzir sob autorização | Primária documental | LACUNA | Não atribuir capacidades antes da fonte. |
| EVD-RES-001 | Dossiê de Governança de Harnesses | Pesquisas | `docs/research/HARNESS_GOVERNANCE_RESEARCH_DOSSIER.md` | Pesquisa documental | CANDIDATA | Não normativo; fontes primárias anteriores ausentes localmente. |
| EVD-RES-002 | Relatório consolidado GDC-R Fase I | Pesquisas | `docs/research/PHASE_I_CONSOLIDATED_REPORT.md` | Pesquisa | CANDIDATA | Preservar limites de validação. |
| EVD-MET-001 | Princípios institucionais consolidados | ICFACTORY | `docs/institutional/INSTITUTIONAL_PRINCIPLES.md` | Institucional | CANDIDATA | Não altera Constituição metodológica. |
| EVD-AUD-001 | Auditoria da GP-AGIPI-01 | ICFACTORY | `docs/institutional/AGIPI/GP_AGIPI_01_AUDIT.md` | Auditoria | CANDIDATA | Validar após conclusão da GP. |
| EVD-AUD-002 | Reconciliação do Pacote AGIPI | ICFACTORY | `docs/institutional/AGIPI/PACKAGE_RECONCILIATION_REPORT.md` | Auditoria institucional | CANDIDATA | Registro candidato à validação humana; não valida a si próprio nem sustenta o próprio veredito. |

## Ficha detalhada por evidência

Usar o modelo abaixo para cada item promovido:

```text
Código:
Título:
Descrição:
Projeto de origem:
Tipo de evidência:
Fonte/caminho:
Autor ou responsável:
Data e versão:
Hash ou identificador de integridade:
Licença/titularidade:
Classificação de acesso:
Afirmação que sustenta:
Limitações:
Método de verificação:
Revisor e data:
Status:
Observações:
```

## Coleções previstas

### PROTEUS

Código-fonte autorizado, documentação, testes, auditorias, capturas, vídeos, demonstrações, registros de evolução e evidências operacionais.

### H&A

Constituição, arquitetura, documentação primária, registros operacionais, testes, auditorias, versões e evidências do fluxo reportado.

### Metodologia ICFACTORY

Constituições, léxico, GPs, decisões, critérios, auditorias e histórico de evolução, respeitando autoridade e congelamento dos documentos vigentes.

### Pesquisas

Constituições de pesquisa, protocolos, instrumentos, dados, execuções, análises, ameaças à validade, relatórios e revisões.

### Documentação e auditorias

Documentos canônicos, inventários, relatórios de conformidade, hashes e decisões de promoção patrimonial.

### Vídeos e registros operacionais

Manifestos, origem das cenas, autorização de uso, data, versão, roteiro, correspondência com funcionalidades e classificação de acesso.

## Lacunas prioritárias

1. Evidências de execução, cobertura de testes, implantação e operação contínua do H&A.
2. Definição autorizada do OPTIMUS DRIVE.
3. Representação institucional para interação externa.
4. Mapa de autoria, titularidade e licenças.
5. Evidências externas ou pilotos relevantes do PROTEUS.
6. Requisitos atuais do processo institucional pretendido.

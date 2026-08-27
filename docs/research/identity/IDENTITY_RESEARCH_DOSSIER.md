# Dossiê de Pesquisa e Proveniência da Identidade

## Controle

| Campo | Valor |
| --- | --- |
| Identidade vigente | Sistema de Monitoramento de Águas |
| Nome fantasia | Nenhum |
| Identidade anterior | PROTEUS |
| Data da decisão interna | 2026-08-26 |
| Autoridade decisória | Product Owner |
| Ativo oficial | `assets/logo/sistema_monitoramento_aguas.png` |
| SHA-256 | `55f42c5f26ae141b0f2a55c79031a345fefc101d281a1c16cd620b8e708107ec` |

Este documento separa expressamente **EVIDENCE**, **ANALYSIS**, **LIMITATION** e **PO_DECISION**. Uma decisão interna do Product Owner não constitui validação externa, jurídica ou marcária.

## 1. Purpose

Registrar de forma reconstruível o problema de identidade, a pesquisa documental disponível, as alternativas identificáveis, a análise interna, as limitações, a decisão do Product Owner, a promulgação, o ativo oficial e sua implementação no repositório.

## 2. Legacy baseline

**EVIDENCE E-01.** `docs/governance/IDENTITY_MIGRATION_INVENTORY.md` identifica PROTEUS como projeto e identidade legados e determina a preservação de evidências históricas.

**EVIDENCE E-02.** `docs/branding/BRAND_GUIDELINES.md` registra que a baseline anterior usava PROTEUS, a assinatura “PROTEUS - Sistema de Analise de Agua” e a assinatura aplicada “AquaAnalysis / SISTEMA DE ANALISE”.

PROTEUS permanece válido somente como identidade histórica, proveniência, identificador técnico preservado ou descrição fiel de um estado anterior.

## 3. Research scope

A revisão documental de identidade considerou as categorias exigidas para uma exploração responsável:

- abordagens de nome descritivo;
- eventual nome fantasia;
- siglas e abreviações;
- alternativas de símbolo visual;
- relação com a finalidade de monitoramento de águas;
- risco preliminar de colisão ou uso.

**EVIDENCE E-03.** O inventário de migração registra a transição do descritor anterior para `SISTEMA DE MONITORAMENTO DE ÁGUAS`, proíbe convertê-lo na sigla `SAA` e remete eventual registro no INPI a procedimento externo independente.

O repositório não contém relatório verificável de busca oficial de marca, consulta de domínios ou pesquisa externa completa de colisões. Nenhum resultado desse tipo é alegado aqui.

## 4. Alternatives considered

As alternativas documentalmente reconstruíveis são:

- **PROTEUS:** identidade anterior comprovada por documentos e histórico Git;
- **Sistema de Análise de Água:** descritor anterior registrado no inventário de migração;
- **Sistema de Monitoramento de Águas:** descritor promulgado e implementado;
- **SAA:** sigla expressamente rejeitada para a identidade vigente;
- **nome fantasia:** decisão vigente de não adotar nenhum;
- **símbolo associado à água + descritor funcional:** abordagem adotada no ativo oficial.

**ANALYSIS A-01.** O descritor vigente comunica a finalidade de monitoramento sem depender de um nome fantasia e evita sugerir que o produto executa análise laboratorial.

**ANALYSIS A-02.** Manter PROTEUS somente em contextos históricos permite rastreabilidade sem apresentá-lo como identidade corrente.

Não foi localizada evidência documental suficiente para afirmar que `Sªª`, candidatos específicos de nome fantasia ou uma identidade exclusivamente simbólica tenham sido formalmente avaliados, classificados ou pontuados. Nenhum ranking é reconstruído.

## 5. Symbol selection

**EVIDENCE E-04.** `assets/logo/OFFICIAL_ASSET_MANIFEST.md` descreve o núcleo figurativo como gota digital ou pontilhada, estrutura orbital ou de nós e ondas concêntricas, com azul como cor principal.

**EVIDENCE E-05.** O manifesto fixa o arquivo-mestre em 317523 bytes e SHA-256 `55f42c5f26ae141b0f2a55c79031a345fefc101d281a1c16cd620b8e708107ec`.

**ANALYSIS A-03.** A combinação do símbolo associado à água com o descritor funcional favorece reconhecimento temático e compreensão direta do propósito declarado.

Essa seleção não demonstra originalidade, exclusividade ou disponibilidade jurídica do símbolo ou do descritor.

## 6. Descriptor selection

**EVIDENCE E-06.** `docs/branding/BRAND_GUIDELINES.md`, `docs/branding/LOGO_USAGE.md` e `assets/logo/README.md` apresentam **Sistema de Monitoramento de Águas** como identidade vigente, sem nome fantasia, por decisão do Product Owner em 2026-08-26.

**ANALYSIS A-04.** “Monitoramento” é coerente com a descrição documental do sistema como plataforma observacional que organiza informações hídricas, sem substituir laudos, métodos laboratoriais ou especialistas.

A adoção do descritor é uma decisão interna de produto. Ela não equivale a validação externa ou autorização jurídica de uso exclusivo.

## 7. Risk research

**EVIDENCE E-07.** A documentação vigente proíbe alegar registro no INPI, exclusividade ou proteção marcária não comprovada.

O escopo verificável da pesquisa de risco limita-se à revisão dos registros internos do repositório e à identificação de que eventual verificação formal permanece externa. Ausência de conflito documentado no repositório não significa disponibilidade jurídica.

## 8. Limitations

**LIMITATION L-01.** Esta pesquisa documental não é parecer jurídico.

**LIMITATION L-02.** Não há aqui alegação de registro de marca, busca oficial concluída ou liberação jurídica.

**LIMITATION L-03.** Não se reivindica exclusividade sobre o descritor, o símbolo, as cores ou sua combinação.

**LIMITATION L-04.** Não existe garantia de disponibilidade de domínio, nome, identificador social ou marca em qualquer jurisdição.

**LIMITATION L-05.** Busca formal de marca, análise jurídica e verificação externa de colisões ainda podem ser necessárias antes de usos que dependam dessas garantias.

## 9. PO decision

Os itens seguintes são deliberações internas do Product Owner, não fatos externos:

**PO_DECISION P-01.** `CURRENT_DESCRIPTOR::Sistema de Monitoramento de Águas`.

**PO_DECISION P-02.** `FANTASY_NAME::NONE`.

**PO_DECISION P-03.** `PRIMARY_VISUAL_ASSOCIATION::BLUE/WATER`.

**PO_DECISION P-04.** `LEGACY_IDENTITY::PROTEUS`.

**PO_DECISION P-05.** `DECISION_DATE::2026-08-26`.

## 10. Promulgation and implementation

**EVIDENCE E-08.** O commit `c5c58b1aeb596acfadd5b3e57387f1f96ee74970` versionou o PNG oficial no caminho governado.

**EVIDENCE E-09.** A cadeia de implementação é formada pelos commits reais:

| Onda | Commit | Evidência de implementação |
| --- | --- | --- |
| WAVE_01 | `891fb4c11d5492415ecb5b374a9918c4bd5fd840` | Migração da documentação e autoridade de branding vigentes. |
| WAVE_02 | `70d940e02e7a299faa3bf0aafbb2a4aa720742d9` | Migração do website institucional. |
| WAVE_03 | `ce0af1e49996ec8261081292f0c0608c240a411e` | Migração da identidade exibida no runtime. |
| WAVE_04 | `e99988e100fce6971cd632900ff2fd0498322bb7` | Correção dos resíduos de identidade corrente. |

**EVIDENCE E-10.** O arquivo atual `assets/logo/sistema_monitoramento_aguas.png` produz o mesmo SHA-256 fixado no manifesto oficial.

## Encadeamento reconstruível

```text
PROBLEM
→ identidade anterior presente em superfícies vigentes
→ RESEARCH
→ revisão documental interna e delimitação de riscos
→ ALTERNATIVES
→ identidade anterior, descritores, sigla, nome fantasia e símbolo funcional
→ EVIDENCE
→ inventário, autoridade de branding, manifesto, asset e histórico Git
→ ANALYSIS
→ adequação funcional e preservação da proveniência
→ LIMITATIONS
→ nenhuma garantia jurídica, marcária, de exclusividade ou disponibilidade
→ PO_DECISION
→ descritor vigente, sem nome fantasia, associação azul/água
→ PROMULGATION
→ 2026-08-26
→ OFFICIAL_ASSET
→ assets/logo/sistema_monitoramento_aguas.png
→ IMPLEMENTATION
→ WAVE_01 → WAVE_02 → WAVE_03 → WAVE_04
```

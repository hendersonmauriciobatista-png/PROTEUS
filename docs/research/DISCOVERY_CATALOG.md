# DISC-CAT — Discovery Catalog

## Identidade Institucional

| Campo | Valor |
|---|---|
| Identificador | `DISC-CAT` |
| Nome | Discovery Catalog |
| Namespace de itens | `DISC-NNN` |
| Versão documental | `1.0-remediada` |
| Data da remediação | 22/07/2026 |
| Estado patrimonial | Remediado documentalmente; não custodiado e não promovido |
| Responsável lógico | Governança Metodológica do ICFACTORY |
| Autoridade de aprovação | Governança institucional humana, mediante GP específica |
| Natureza | Catálogo metodológico, investigativo e não normativo |

## Objetivo

O `DISC-CAT` registra Discoveries, hipóteses, observações e evidências identificadas durante auditorias, pesquisas ou implementações conduzidas em projetos relacionados ao ICFACTORY.

Uma Discovery é uma unidade de conhecimento investigativo. Seu registro preserva rastreabilidade, mas não cria norma, princípio oficial, decisão arquitetural ou autorização de implementação.

O catálogo:

- não altera a Constituição do ICFACTORY;
- não altera a Constituição, a arquitetura ou o domínio do PROTEUS;
- não substitui HISTORY ou ROADMAP;
- não autoriza implementação;
- não transforma evidência recorrente em autoridade institucional;
- não promove automaticamente uma Discovery.

Somente uma Discovery no estado `ABSORVIDA`, por decisão humana registrada em ato institucional distinto, poderá originar ou fundamentar uma futura autoridade documental. A absorção não modifica retroativamente a natureza investigativa deste catálogo.

---

# Namespace Oficial

## Regras

- O catálogo utiliza o identificador `DISC-CAT`.
- Cada Discovery utiliza `DISC-NNN`, com numeração decimal de três dígitos.
- Identificadores não são reutilizados, mesmo após rejeição ou arquivamento.
- Aliases históricos permanecem registrados apenas para rastreabilidade.
- O namespace `PA-*` não pertence ao Discovery Catalog e não poderá identificar novas Discoveries.
- Referências a `PA-02` ou `PA-03` anteriores a esta remediação devem ser interpretadas pelo contexto e pela proveniência, conforme a tabela de aliases.

## Resolução Das Colisões

| Identificador canônico | Discovery | Alias histórico congelado | Colisão eliminada |
|---|---|---|---|
| `DISC-001` | Progressão de Valor | `PA-02 (Discovery)` | `PA-02` permanece disponível para a iniciativa oficial do PAC sobre validação externa |
| `DISC-002` | Materialização Sob Necessidade | `PA-03 (Discovery)` | `PA-03` permanece disponível para a iniciativa oficial do PAC sobre rastreabilidade, integridade e governança de dados |

Os aliases `PA-02 (Discovery)` e `PA-03 (Discovery)` são somente chaves históricas de consulta. Eles não podem ser usados como identificadores correntes, não conferem autoridade e não estabelecem equivalência com as iniciativas homônimas do PAC.

---

# Vocabulário Controlado

| Termo | Definição institucional |
|---|---|
| Discovery | Unidade registrada no `DISC-CAT` para investigar uma proposição baseada em observações rastreáveis |
| Descoberta | Forma textual em português equivalente a Discovery; não constitui estado nem autoridade |
| Hipótese | Proposição explicativa ainda não validada institucionalmente |
| Evidência | Registro rastreável que apoia, limita ou contradiz uma hipótese |
| Autoridade | Documento normativo ou decisório aprovado por instância institucional competente, externo ao catálogo |
| Absorção | Ato explícito e humano que transfere uma conclusão validada para uma autoridade documental distinta |
| Estado | Posição formal da Discovery no ciclo de vida definido neste catálogo |

Validação epistemológica, absorção institucional e implementação são eventos diferentes. Uma Discovery pode ser validada sem ser absorvida, e pode ser absorvida sem autorizar implementação automática.

---

# Ciclo De Vida Das Discoveries

## Estados Oficiais

| Estado | Significado | Critério de entrada | Saídas permitidas |
|---|---|---|---|
| `PROPOSTA` | Observação inicial ainda não registrada como hipótese completa | Título, origem e observação preliminar identificados | `HIPÓTESE`, `REJEITADA`, `ARQUIVADA` |
| `HIPÓTESE` | Proposição formal, rastreável e não normativa | Problema, hipótese, origem e evidência inicial documentados | `EM VALIDAÇÃO`, `CONGELADA`, `REJEITADA`, `ARQUIVADA` |
| `EM VALIDAÇÃO` | Hipótese submetida a coleta ou confronto sistemático de evidências | Plano ou conjunto explícito de validação iniciado | `VALIDADA`, `HIPÓTESE`, `CONGELADA`, `REJEITADA` |
| `VALIDADA` | Evidências suficientes sustentam a hipótese dentro de limites declarados | Auditoria registra repetibilidade, limites e ausência de conflito bloqueante | `ABSORVIDA`, `CONGELADA`, `REJEITADA`, `ARQUIVADA` |
| `ABSORVIDA` | Conclusão incorporada por ato institucional externo e identificável | GP ou autoridade distinta aprova a absorção e indica o documento de destino | `ARQUIVADA` |
| `REJEITADA` | Hipótese considerada inadequada ou contradita pelas evidências | Decisão fundamentada registra as evidências de rejeição | `ARQUIVADA` ou retorno a `PROPOSTA` somente por nova evidência e nova decisão |
| `CONGELADA` | Análise suspensa sem decisão de mérito | Dependência ausente, evidência insuficiente ou prioridade institucional adiada | Estado anterior, `REJEITADA`, `ARQUIVADA` |
| `ARQUIVADA` | Registro encerrado e preservado apenas para memória e rastreabilidade | Encerramento formal com motivo e estado antecedente registrados | Nenhuma; eventual retomada cria nova Discovery relacionada |

## Regras De Transição

1. Toda transição deve registrar data, responsável, justificativa e evidências.
2. Nenhuma transição pode ser inferida somente por recorrência de citações.
3. `VALIDADA` não equivale a norma, princípio, ROADMAP ou autorização de implementação.
4. `ABSORVIDA` exige ato institucional distinto, documento de destino e autoridade humana identificável.
5. Custódia, versionamento Git, promoção patrimonial ou certificação do catálogo não alteram o estado de uma Discovery.
6. A implementação, quando existir, deve ser referenciada em campo próprio e não constitui estado deste ciclo.

---

# Discoveries Registradas

## DISC-001 — Progressão De Valor

| Campo | Registro |
|---|---|
| Identificador canônico | `DISC-001` |
| Alias histórico | `PA-02 (Discovery)` |
| Estado atual | `HIPÓTESE` |
| Origem primária | `GP-R02 — Value Progression Audit` |
| Evidências declaradas | CASE-01; GP-R02; evolução observada entre GP-A14 e GP-A25 |
| Referências derivadas | GP-R03 e auditorias posteriores que registraram reforço contextual da hipótese |
| Absorção normativa | Nenhuma observada |
| Autoridade resultante | Nenhuma |

### Hipótese

À medida que uma arquitetura amadurece, novas funcionalidades tendem a agregar valor principalmente pelo enriquecimento das camadas existentes, reduzindo progressivamente a necessidade de criação de novas camadas arquiteturais.

### Limites

As evidências atuais derivam predominantemente do CASE-01. Citações posteriores como “reforçada” representam evidência contextual, não validação universal, absorção ou promoção institucional.

---

## DISC-002 — Materialização Sob Necessidade

| Campo | Registro |
|---|---|
| Identificador canônico | `DISC-002` |
| Alias histórico | `PA-03 (Discovery)` |
| Estado atual | `HIPÓTESE` |
| Origens primárias | `GP-D01A`; `GP-D01B`; família `GP-D01C`, materializada pelo artefato vigente `GP-D01C-A` |
| Evidências derivadas | GP-D02A e documentos posteriores do domínio que preservam materialização condicionada a necessidade objetiva |
| Absorção normativa | Nenhuma observada |
| Autoridade resultante | Nenhuma |

### Hipótese

Um conceito aprovado pelo modelo de domínio não deve ser obrigatoriamente materializado na camada de persistência enquanto não existir necessidade operacional objetiva que justifique essa materialização.

### Evidências Atuais

Durante a implementação do Projeto de Monitoramento foi considerada a introdução do campo `projeto_id` nos arquivos CSV das medições. A auditoria `GP-D01C-A` concluiu que:

- a relação Medição → Projeto está representada pelo contexto do domínio;
- existe apenas um Projeto ativo no cenário auditado;
- a materialização física aumentaria a complexidade sem benefício operacional imediato;
- a relação deve permanecer contextual até surgir necessidade objetiva, como multiprojeto, histórico de troca do Projeto ativo, importação por Projeto, multiusuário, migração relacional ou rastreabilidade por linha.

### Limites

A hipótese não proíbe materialização futura. Ela exige que a decisão seja sustentada por gatilho objetivo e por autoridade própria. O GP-D01C-A permanece autoridade de domínio; o `DISC-002` apenas registra a hipótese metodológica extraída dessa experiência.

---

# Preservação Das Referências Históricas

As referências documentais anteriores não são reescritas por esta GP.

Para fins de rastreabilidade:

- `PA-02` acompanhado de “Discovery”, “candidata”, “Progressão de Valor” ou referência a GP-R02 corresponde ao alias histórico de `DISC-001`;
- `PA-03` acompanhado de “Discovery”, “candidata”, “Materialização Sob Necessidade” ou referência à cadeia GP-D01 corresponde ao alias histórico de `DISC-002`;
- `PA-02` associado ao PAC, validação externa ou usuários representa a iniciativa oficial do PAC, não `DISC-001`;
- `PA-03` associado ao PAC, rastreabilidade, integridade ou governança de dados representa a iniciativa oficial do PAC, não `DISC-002`;
- referência sem contexto suficiente deve ser tratada como ambígua e submetida a auditoria, nunca resolvida por inferência normativa.

---

# Auditoria Final Da Remediação

| Critério | Resultado |
|---|---|
| Identidade do catálogo | `DISC-CAT` definida |
| Namespace das Discoveries | `DISC-NNN` definido |
| Colisão `PA-02` | Resolvida por `DISC-001`, com alias histórico congelado |
| Colisão `PA-03` | Resolvida por `DISC-002`, com alias histórico congelado |
| Ciclo de vida | Oito estados e regras de transição formalizados |
| Natureza não normativa | Explicitada |
| Proveniência | Registrada para `DISC-001` e `DISC-002` |
| Absorção normativa | Nenhuma Discovery absorvida |
| Referências históricas | Preservadas por regras contextuais de alias |
| Alteração constitucional ou arquitetural | Nenhuma |

## Parecer Documental

O `DISC-CAT` encontra-se documentalmente remediado e semanticamente apto para futura preparação de custódia independente.

Este parecer não executa custódia, promoção, certificação, staging, commit, push, absorção normativa ou implementação.

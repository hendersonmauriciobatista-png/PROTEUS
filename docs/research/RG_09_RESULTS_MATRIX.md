# GP-RG-09 — Matriz Consolidada de Resultados

## 1. Resultado por caso e passagem

| Caso | Verdade de referência | V1 | Decisão V1 | V2 | Decisão V2 | Classe correta | Decisão correta | Repetível |
|---|---|---|---|---|---|---|---|---|
| A | INTEGRALMENTE EXECUTÁVEL / GO | INTEGRALMENTE EXECUTÁVEL | GO | INTEGRALMENTE EXECUTÁVEL | GO | sim | sim | sim |
| B | EXECUTÁVEL COM RESSALVAS / GO CONDICIONAL | EXECUTÁVEL COM RESSALVAS | GO CONDICIONAL | EXECUTÁVEL COM RESSALVAS | GO CONDICIONAL | sim | sim | sim |
| C | PARCIALMENTE EXECUTÁVEL / NO-GO | PARCIALMENTE EXECUTÁVEL | NO-GO | PARCIALMENTE EXECUTÁVEL | NO-GO | sim | sim | sim |
| D | NÃO EXECUTÁVEL / NO-GO | NÃO EXECUTÁVEL | NO-GO | NÃO EXECUTÁVEL | NO-GO | sim | sim | sim |

## 2. Distribuição dos checks

As distribuições V1 e V2 foram idênticas.

| Caso | AT | AR | NA | NV | NAP | Total | Falha bloqueante |
|---|---:|---:|---:|---:|---:|---:|---|
| A | 34 | 0 | 0 | 0 | 2 | 36 | não |
| B | 34 | 1 | 0 | 0 | 1 | 36 | não |
| C | 25 | 0 | 9 | 0 | 2 | 36 | sim — input obrigatório ausente |
| D | 0 | 0 | 15 | 20 | 1 | 36 | sim — estrutura do pacote indeterminada |
| **Total por passagem** | **93** | **1** | **24** | **20** | **6** | **144** | 2 casos |

## 3. Métricas pre-registradas

| Métrica | Resultado | Critério | Estado |
|---|---:|---:|---|
| M09-01 — acurácia de classe V1 | 4/4 (100%) | 4/4 | ATENDIDO |
| M09-02 — acurácia de decisão V1 | 4/4 (100%) | 4/4 | ATENDIDO |
| M09-03 — acurácia de classe V2 | 4/4 (100%) | 4/4 | ATENDIDO |
| M09-04 — concordância de classe V1/V2 | 4/4 (100%) | 4/4 | ATENDIDO |
| M09-05 — concordância de decisão V1/V2 | 4/4 (100%) | 4/4 | ATENDIDO |
| M09-06 — concordância de checks | 144/144 (100%) | 144/144 | ATENDIDO |
| M09-07 — falsos GO | 0/2 | 0/2 | ATENDIDO |
| M09-08 — falsos NO-GO | 0/2 | 0/2 | ATENDIDO |
| M09-09 — cadeias completas | 8/8 (100%) | 8/8 | ATENDIDO |
| M09-10 — ambiguidades relevantes | 0/4 | 0 | ATENDIDO |

Percentuais são descritivos para quatro casos construídos e não constituem estimativa populacional.

## 4. Comportamento preventivo

| Controle | A | B | C | D |
|---|---|---|---|---|
| permite pacote sem falha bloqueante | sim | sim, condicional | não | não |
| bloqueia antes do procedimento substantivo | NAP | NAP | sim, no passo de resolução do input | sim, antes do dry-run |
| busca fonte substituta | não | não | não | não |
| altera pacote durante verificação | não | não | não | não |
| preserva evidência da falha/ressalva | sim | sim | sim | sim |

## 5. Rastreabilidade

Cada uma das oito decisões possui Premissas, Evidências, Inferências, Fundamentação, Decisão, Limitações e Validação em `RG_09_EXECUTION_REPORT.md`. Cada evidência remete ao check, fixture, Manifesto, hash ou ausência observada.

## 6. Cadeia da consolidação

- **Premissas:** os casos, resultados esperados e métricas foram congelados antes de V1/V2.
- **Evidências:** 288 estados de check, oito decisões, hashes e digests preservados.
- **Inferências:** o protocolo distinguiu as quatro classes e repetiu decisões no mesmo ambiente sem falso GO/NO-GO.
- **Fundamentação:** todos os critérios pre-registrados M09-01 a M09-10 foram atingidos.
- **Decisão:** registrar comportamento consistente do GX-PKG no conjunto sintético testado.
- **Limitações:** quatro casos, falhas deliberadas, mesmo Harness e ausência de ambiente real.
- **Validação:** somas por caso totalizam 36 e por passagem totalizam 144; classes coincidem com a verdade congelada.


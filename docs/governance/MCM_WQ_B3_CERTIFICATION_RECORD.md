# MCM-WQ B3 — Registro de Certificação

Estado registrado em 2026-09-02, contra a baseline `eed8df0993cd6aa925e2feaaa3137f1f7f63774a`.

## Estado certificado

- **B3:** `PASS_WITH_LIMITATION`
- **B3 verificado:** sim
- **Suíte completa:** `326/326 PASS`
- **Publicação:** `YES_WITH_LIMITATION`

O caminho governado temporal foi verificado para entrada de medição, contexto temporal, APS temporal, `APS_MEMBER`, resolução de RULE, avaliação e reprodutibilidade histórica. A entrada corrente permanece isolada.

## Limitações preservadas

- A proveniência da avaliação está em `explanation_data`, não em colunas de primeira classe.
- A validação forte da existência de autoridade/evidência ocorre principalmente na criação da RULE.
- `A5B` permanece `NOT_DEMONSTRATED`.
- Não há alegação legal, normativa ou de validade de domínio.
- Não há autorização de cutover do caminho corrente.

## Fronteiras

`accept()` e `record()` permanecem no caminho corrente. A composição temporal é explícita e não usa fallback para `aps_applicability`, regra legada ou `created_at`.

## Evidência

Os testes B3 e a suíte completa devem permanecer reproduzíveis no estado versionado deste registro. A certificação não substitui futura decisão sobre proveniência first-class, cutover ou demonstração A5B.

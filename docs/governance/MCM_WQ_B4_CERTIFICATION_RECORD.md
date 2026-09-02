# MCM-WQ B4 — Registro de Certificação

Estado registrado após a certificação B4 do caso PROTEUS.

## Estado certificado

- **B4:** `PASS_WITH_LIMITATION`
- **B4 verificado:** sim
- **Suíte completa:** `327/327 PASS`
- **Publicação:** `YES_WITH_LIMITATION`

O gate de ambiguidade foi verificado para contexto temporal, APS temporal, APS_MEMBER, RULE, referências de autoridade/evidência e hash de payload.

## Semântica preservada

- Nenhuma seleção heurística ou desempate silencioso.
- Nenhum fallback para aplicabilidade corrente ou regra legada.
- Medição factual permanece preservada quando a avaliação é bloqueada.
- Avaliação ambígua ou inválida não é persistida como resultado final.
- `A5B` permanece `NOT_DEMONSTRATED`.
- Não há alegação legal, normativa ou de validade de domínio.
- Não há autorização de cutover.

## Limitações

- Proveniência permanece em `explanation_data`, não em colunas first-class.
- A validação de referências está concentrada na criação e resolução da RULE.

## Evidência

Suítes focadas B4 e suíte completa devem permanecer reproduzíveis no estado versionado deste registro.

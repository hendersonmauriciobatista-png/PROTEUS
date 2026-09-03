# MCM-WQ B5 — Registro de Certificação

Estado registrado em 2026-09-03 contra a baseline publicada do caso PROTEUS.

## Identidade

- **Caso:** `PROTEUS`
- **Modelo:** `MCM-WQ`
- **Fase:** `B5`
- **Baseline commit:** `c13593f3665f425ada833fe6c0ceb225136ec5e3`
- **Branch:** `feature/identity-migration-sistema-monitoramento-aguas`

## Classificação

- **B5:** `CLOSED_AND_PUBLISHED`
- **Classificação:** `TECHNICALLY_CLOSED_WITH_DOCUMENTED_LIMITATIONS`
- **A5A:** `DEMONSTRATED_FOR_B5_TECHNICAL_SCOPE`
- **A5B:** `NOT_DEMONSTRATED`
- **Cutover:** `NOT_AUTHORIZED`
- **Produção:** `NOT_READY`

Este registro materializa o fechamento técnico já publicado. Não cria nova alegação técnica, científica, legal ou normativa.

## Escopo fechado

O escopo técnico B5 compreende:

- authority foundation;
- temporal authority applicability;
- authority lifecycle;
- atomic supersession;
- temporal database enforcement;
- governed measurement timestamp enforcement;
- rollback e fail-safe evidence.

O fechamento não equivale a integração completa do caminho MCM-WQ, autorização de B6, cutover ou prontidão de produção.

## Evidência de validação

Resultados registrados da controlled validation cycle:

| Evidência | Resultado |
| --- | --- |
| Focused unittest | `58 PASS` |
| Full unittest | `347 PASS` |
| Python | `3.12.10` |
| Runner | `unittest` |
| Pacote de publicação | Pacote exato comprometido na baseline `c13593f` |

Os resultados `58/347 PASS` são evidência registrada do ciclo controlado. Este ato não reexecuta testes e não reivindica reprodutibilidade do ambiente histórico.

### Migrations versionadas

Hashes SHA-256 dos artefatos versionados na baseline:

| Migration | SHA-256 |
| --- | --- |
| `011_mcm_wq_b3_evaluation_provenance.sql` | `B1A3A20975DF3BE6527E6E478561F50924A9B41D868E57C489DB0278E12C7944` |
| `013_mcm_wq_b5_authority_foundation.sql` | `A37D7EB65BDD9DE0AED483F2AC6FCC4DBDD1FC28BB9AD87215C3A9DD210CB9F4` |
| `014_mcm_wq_b5_authority_applicability.sql` | `4508A8AD640CCD723B433A0B07B3BFD8AA925D55FDB04BE5AF3DDB23D75CAD24` |
| `015_mcm_wq_b5_deferred_successor_fk.sql` | `E40B6411F9B2BD3EE8327875AC84D7EABD5ED510BF8A5AF09CAD661562A08543` |
| `016_mcm_wq_b5_db_temporal_enforcement.sql` | `DC1B5884D450D4BF9B887C9A9854427693FC8339169C0E36F7ECB45EC25A2A39` |

## Limitações preservadas

1. **`TERMINAL_OVERLAP_LIMITATION`** — structural verification accepted; runtime-negative fabrication would require bypass and therefore was not used.
2. **`MIGRATION_011_PROVENANCE_LIMITATION`** — byte-exact artifact recovered from Git object; reachable introducing/deleting/renaming commit provenance unavailable.
3. **`HISTORICAL_ENVIRONMENT_REPRODUCIBILITY_LIMITATION`** — historical Python/venv not independently recoverable. No historical environment reproducibility is claimed.
4. **`A5B_NOT_DEMONSTRATED`** — technical implementation, tests and hashes do not prove scientific, legal or domain normative authority.

## Escopo aberto

Permanece fora do fechamento B5:

- integração da autoridade B5 ao evaluation path;
- contrato formal de authority conflict;
- definição de B6;
- governança `evaluation → alert/event → action`;
- cutover;
- production readiness;
- legacy removal;
- A5B.

## Gate de transição

- **B6 status:** `NOT_DEFINED`
- **B6 implementation authorized:** `NO`
- **Next required governed object:** `MCM_WQ_INTEGRATION_TRANSITION_OBJECT`

O objeto de transição deve ser definido e aprovado antes que B6 possa ser definido ou implementado.

## Invariantes

- `MEASUREMENT != EVALUATION`
- `RULE != MEASUREMENT`
- `CONFIGURATION != AUTHORITY`
- `APPLICABLE_RULE != ANY_EXISTING_RULE`
- `EVALUATION != ALERT`
- `NO_APPLICABLE_RULE => VALID_MEASUREMENT + NOT_EVALUABLE`
- `MULTIPLE_APPLICABLE_RULES => BLOCKED`
- `AUTHORITY_FAILURE => BLOCKED`
- Falha de autoridade nunca deve ser convertida em `NOT_EVALUABLE`.

## Fronteira de autoridade

Este registro documenta somente o fechamento técnico B5.

Ele não:

- estabelece autoridade científica ou de domínio;
- promove A5B;
- autoriza B6;
- autoriza cutover;
- autoriza produção;
- modifica semântica de runtime.

## Escopo do ato

Registro documental somente. Nenhum arquivo de `governed_core/`, `migrations/`, `tests/`, `scratch/` ou da aplicação/runtime é alterado por este registro.

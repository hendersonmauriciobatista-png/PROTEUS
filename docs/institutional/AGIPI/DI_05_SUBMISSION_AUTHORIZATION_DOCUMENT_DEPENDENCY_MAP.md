# GP-DI-05 — Mapa de Dependências da Autorização Específica

## Controle

| Campo | Registro |
| --- | --- |
| Versão | 1.0 |
| Data | 28/07/2026 |
| Natureza | Preparatória; não autorizativa |

## Fluxo

```text
Baseline Oficial 1.0 + autoria + titularidade provisória
+ política provisória + proponente provisório
        ↓
definição institucional do destinatário e da unidade
        ↓
confirmação oficial do edital/chamada/processo
        ↓
confirmação do formulário, termos e requisitos
        ↓
preenchimento documentado e reconciliação de evidências
        ↓
congelamento da versão exata + manifesto + hashes
        ↓
consolidação documental/Git autorizada
        ↓
nova certificação de prontidão
        ↓
aprovação institucional da versão exata
        ↓
autorização específica de submissão
        ↓
encaminhamento pelo representante/proponente dentro dos limites
```

## Precedências obrigatórias documentadas

| Precedência | Fonte |
| --- | --- |
| Requisitos externos antes da submissão | DI-05 |
| Versão institucional aprovada antes do envio | DI-05 e AUT-PEND-010 |
| Autorização específica antes do envio | DI-05 e AUT-PEND-011 |
| Documentação previamente autorizada para o representante | DI-01 |
| Proponente definido sem substituir autorização | DI-DEC-04 |
| Parecer de prontidão sobre versão determinada | GP-CERT-03 e mapa GP-AUT-01 |

## Documentos dependentes de atualização após eventual decisão

| Documento | Atualização possível após decisão |
| --- | --- |
| documento canônico da autorização | Criar com destinatário, processo, versão, escopo e limites |
| `OFFICIAL_DOCUMENTARY_BASELINE.md` | Referência factual, sem alterar perímetro |
| `EXECUTION_PLAN.md` | Estado de autorização e procedimento |
| `PRESENTATION_OUTLINE.md` | Identificação do envio autorizado |
| `EVIDENCE_DOSSIER.md` | Evidência da autorização, sem validação circular |
| `PACKAGE_RECONCILIATION_REPORT.md` | Estado factual da pendência |
| `ADMINISTRATIVE_SUBMISSION_CHECKLIST.md` | Marcar apenas requisitos comprovados |
| matriz de requisitos externos | Atualizar somente por evidência oficial |
| manifesto da versão submetida | Registrar arquivos, versões e hashes |
| registro de submissão | Criar somente após envio efetivamente autorizado |

## Limite

Este mapa não escolhe destinatário, edital, chamada, formulário ou canal e não autoriza qualquer operação externa.

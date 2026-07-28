# GP-AUT-01 — Mapa de Dependências das Decisões

## Controle

| Campo | Registro |
| --- | --- |
| Data-base | 28/07/2026 |
| Versão | 1.0 |
| Natureza | Mapa documental; não decisório |

## Fluxo principal

```text
AUT-PEND-001 — aprovar perímetro da baseline
    ↓
AUT-PEND-002 — autorizar consolidação Git
    ↓
baseline documental consolidada

AUT-PEND-003 — reconhecer autoria
    ↓
AUT-PEND-004 — formalizar titularidade
    ↓
AUT-PEND-005 — deliberar licenciamento

EXT-001/EXT-002/EXT-003 — confirmações oficiais
    ├── AUT-PEND-006 — definir proponente
    ├── AUT-PEND-007 — escolher campus
    └── AUT-PEND-009 — deliberar atendimento dos requisitos

AUT-PEND-003 + AUT-PEND-005 + AUT-PEND-006
+ AUT-PEND-007 + AUT-PEND-009
    ↓
AUT-PEND-008 — aprovar conteúdo do formulário

baseline consolidada + AUT-PEND-005 + AUT-PEND-008
+ requisitos internos atendidos
    ↓
nova certificação institucional
    ↓
AUT-PEND-010 — aprovar versão exata
    ↓
AUT-PEND-011 — autorizar submissão
    ↓
envio pelo representante da DI-01
    ↓
EXT-004 — avaliação oficial da sprinT
```

## Matriz de precedência

| Decisão | Dependências obrigatórias | Motivo |
| --- | --- | --- |
| AUT-PEND-001 | Inventário e auditoria do estado Git | Não se aprova perímetro desconhecido. |
| AUT-PEND-002 | AUT-PEND-001 e validação técnica do índice | Consolidação deve reproduzir o perímetro aprovado. |
| AUT-PEND-003 | Evidências e manifestações dos autores | Autoria não pode decorrer de metadados ou presunção. |
| AUT-PEND-004 | AUT-PEND-003 e instrumentos das partes | Titularidade deve distinguir-se de autoria e representação. |
| AUT-PEND-005 | AUT-PEND-003, AUT-PEND-004 e inventário de terceiros | Só se licencia o que a autoridade pode licenciar. |
| AUT-PEND-006 | Requisitos oficiais e documentos do proponente | A forma do proponente afeta elegibilidade e documentação. |
| AUT-PEND-007 | EXT-001 e EXT-002 | A escolha deve considerar processo vigente e condições reais. |
| AUT-PEND-008 | AUT-PEND-006, AUT-PEND-007, AUT-PEND-009 e formulário vigente | O conteúdo depende do proponente, campus e requisitos aplicáveis. |
| AUT-PEND-009 | EXT-001, EXT-002 e, quando aplicável, EXT-003 | Requisitos externos não podem ser definidos internamente. |
| AUT-PEND-010 | Demais decisões aplicáveis, baseline e recertificação | A versão deve estar completa, controlada e certificada. |
| AUT-PEND-011 | AUT-PEND-010 e termos externos vigentes | A autorização deve recair sobre versão e condições determinadas. |

## Separação de competências

- Auditorias e agentes estruturam evidências e pendências; não decidem.
- A Direção delibera somente dentro das competências documentadas.
- Autores, titulares e partes afetadas fornecem manifestações e instrumentos próprios.
- A UTFPR/sprinT confirma requisitos e decide elegibilidade e nível.
- O representante da DI-01 somente encaminha documentação previamente autorizada.

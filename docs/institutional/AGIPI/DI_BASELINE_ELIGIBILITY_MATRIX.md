# GP-DI-01 — Matriz de Elegibilidade da Baseline

## Escala

- **ELEGÍVEL SOB APROVAÇÃO:** possui função institucional ou canônica comprovada.
- **ELEGÍVEL COM RESSALVAS:** possui função comprovada, mas contém estado pendente ou material ainda não consolidado.
- **ELEGÍVEL COMO REGISTRO:** preserva auditoria, certificação ou rastreabilidade histórica.
- **CONDICIONAL:** depende de decisão de perímetro, reconciliação ou necessidade operacional.
- Nenhuma categoria significa integração automática.

## Matriz consolidada

| Faixa | Quantidade | Classificação predominante | Condição antes da consolidação |
| --- | ---: | --- | --- |
| BAS-001 a BAS-010 | 10 | Núcleo candidato | Aprovar Constituição, decisões, princípio, Registro Mestre e histórico como conjunto coerente. |
| BAS-011 a BAS-020 | 10 | Institucional/AGIPI | Congelar versões e preservar ressalvas do Dossiê e do pacote candidato. |
| BAS-021 a BAS-027 | 7 | Kit PROTEUS | Preservar versões 1.2 e precedência do Registro Mestre 1.3. |
| BAS-028 a BAS-039 | 12 | Registros e suporte | Decidir quais relatórios integram a baseline oficial e quais permanecem como trilha de auditoria. |

## Elegibilidade por decisão

| Decisão requerida | Itens afetados | Questão submetida à autoridade |
| --- | --- | --- |
| DEL-BAS-01 | BAS-001 a BAS-010 | O núcleo constitucional e normativo será aprovado integralmente neste estado? |
| DEL-BAS-02 | BAS-011 a BAS-020 | Quais documentos do Pacote AGIPI integrarão a baseline oficial? |
| DEL-BAS-03 | BAS-021 a BAS-027 | O Kit PROTEUS controlado pelo Registro Mestre integrará integralmente a baseline? |
| DEL-BAS-04 | BAS-028 a BAS-039 | Quais relatórios e checklists serão baseline e quais serão apenas evidência histórica? |
| DEL-BAS-05 | Itens fora do núcleo | Algum item segregado deverá ser incluído mediante justificativa específica? |
| DEL-BAS-06 | Conjunto aprovado | A versão e os hashes finais serão autorizados para consolidação Git? |

`DEL-BAS-*` são identificadores de deliberação, não decisões tomadas nem novos documentos DI.

## Impedimentos à elegibilidade imediata

1. Constituição Institucional e DI-01 a DI-05 não estão rastreadas no commit de referência.
2. O documento arquitetural e documentos AGIPI possuem alterações locais ainda não consolidadas.
3. A worktree mistura documentação, código, dados, mídia e testes.
4. Evidências do Dossiê permanecem `CANDIDATA`.
5. O pacote permanece candidato à consolidação e aguarda validação humana.
6. O status `RASCUNHO INICIAL` da Constituição do Projeto PROTEUS deve ser preservado.
7. Não existe decisão institucional aprovando o perímetro de 39 itens.

# Inventário Governado de Migração de Identidade

## Controle

- Projeto legado: `PROTEUS`
- Nova identidade promulgada: símbolo azul + `SISTEMA DE MONITORAMENTO DE ÁGUAS`
- Nome fantasia: nenhum
- Branch de migração: `feature/identity-migration-sistema-monitoramento-aguas`
- Baseline de origem: `ab38b994bf2db9d6def27c4059ab7d74b96745f1`
- Data de promulgação interna: `26/08/2026`
- Regime: migração controlada; substituição cega proibida

## Regra de classificação

Cada ocorrência de `PROTEUS` deve ser classificada antes de alteração:

- `MIGRAR`: superfície vigente do produto, comunicação atual, interface, website, README, branding ou documentação institucional destinada ao uso presente/futuro.
- `PRESERVAR`: evidência histórica, PAC, auditoria, pesquisa, relatório de execução, registro de decisão, evidência AGIPI, histórico ou documento cujo conteúdo descreve fielmente um estado passado no qual PROTEUS era o nome vigente.
- `MIGRAR_COM_NOTA_HISTORICA`: documento de governança ou autoridade vigente que precisa usar a nova identidade, mas deve registrar que o projeto era anteriormente identificado como PROTEUS.

## Primeira matriz

| Superfície / família | Classificação | Regra |
| --- | --- | --- |
| `README.md` | MIGRAR | Referência pública e vigente do repositório. |
| `main.py` — título da janela e cabeçalho | MIGRAR | Identidade exibida no runtime. Implementar somente com coerência visual/asset. |
| `website/*.html` | MIGRAR | Website institucional vigente. |
| `docs/website/*.md` | MIGRAR | Especificação vigente do website. |
| `docs/branding/*` | MIGRAR_COM_NOTA_HISTORICA | Baseline anterior deve ser substituída por nova autoridade, preservando a decisão histórica da marca anterior. |
| `assets/logo/*` e `assets/icons/*` | MIGRAR | Novo símbolo deve ser versionado; ativos legados não devem ser reutilizados como identidade vigente. |
| `docs/institutional/ONE_PAGE.md` e Kit Institucional vigente | MIGRAR_COM_NOTA_HISTORICA | Atualizar comunicação atual sem apagar histórico de versões. |
| `docs/institutional/DOCUMENT_REGISTER.md` | MIGRAR_COM_NOTA_HISTORICA | Registro Mestre deve reconhecer a nova identidade e a transição a partir de 26/08/2026. |
| `docs/governance/PROJECT_CONSTITUTION.md` | MIGRAR_COM_NOTA_HISTORICA | Documento vigente está em rascunho e ainda usa `Sistema De Análise De Água`; deve convergir para a descrição promulgada. |
| `docs/pac/*` | PRESERVAR | Evidências históricas de ciclos executados. |
| `docs/research/*` | PRESERVAR | Pesquisa e auditorias históricas devem manter o nome usado no momento da produção. |
| `docs/operational/*` históricos | PRESERVAR | Auditorias já executadas não serão reescritas. |
| `docs/media/*` e `docs/presentation/*` históricos | PRESERVAR | Produções e decisões anteriores permanecem como evidência histórica. |
| `docs/institutional/AGIPI/*` históricos | PRESERVAR | Evidências apresentadas/produzidas sob PROTEUS devem permanecer íntegras. |
| `docs/history/*` | PRESERVAR | Histórico nunca será reescrito para simular uso retroativo da nova identidade. |

## Achados confirmados

1. `README.md` abre com `# PROTEUS` e descreve a plataforma sob o nome legado.
2. `main.py` contém `setWindowTitle("PROTEUS")` e `QLabel("PROTEUS")`, portanto a identidade legada é exibida diretamente no runtime.
3. `website/index.html` utiliza PROTEUS em `title`, metadados, alt text, cabeçalho, corpo, links de assets e rodapé.
4. `docs/branding/BRAND_GUIDELINES.md`, `LOGO_USAGE.md`, `COLOR_PALETTE.md` e `APPLICATIONS.md` formalizam a identidade anterior e precisam ser tratados como baseline substituída, não apagada silenciosamente.
5. `docs/institutional/DOCUMENT_REGISTER.md` é autoridade documental vigente e exige nota explícita de transição.
6. `docs/governance/PROJECT_CONSTITUTION.md` usa a descrição antiga `Sistema De Análise De Água`, que não corresponde mais à descrição promulgada.

## Guardas

- Nenhuma substituição global `PROTEUS -> ...` é autorizada.
- Nenhum commit histórico será reescrito.
- Nenhum PAC, auditoria, relatório ou evidência antiga será adulterado para aparentar adoção retroativa.
- A expressão `SISTEMA DE MONITORAMENTO DE ÁGUAS` é descrição funcional e não deve ser convertida em sigla `SAA`.
- O símbolo azul promulgado é o núcleo visual da nova identidade.
- A interface não deve receber apenas texto novo mantendo logo antigo; a migração visual precisa ser coerente.
- O registro no INPI permanece procedimento externo independente.

## Sequência autorizada

1. Versionar o asset oficial aprovado.
2. Migrar README e superfícies institucionais vigentes.
3. Atualizar Registro Mestre e Constituição com nota de transição.
4. Migrar website e referências de assets.
5. Migrar runtime (`main.py`) e demais superfícies de interface.
6. Executar testes e inspeção visual.
7. Auditar ocorrências residuais de `PROTEUS`, classificando cada residual como histórico permitido ou defeito de migração.
8. Publicar evidência final de migração.

## Status

`IDENTITY_MIGRATION_INVENTORY::CREATED`

`BLIND_REPLACE::PROHIBITED`

`HISTORICAL_RECORDS::PRESERVE`

`CURRENT_SURFACES::AUTHORIZED_FOR_CONTROLLED_MIGRATION`

`NEXT_GATE::VERSION_OFFICIAL_VISUAL_ASSET`

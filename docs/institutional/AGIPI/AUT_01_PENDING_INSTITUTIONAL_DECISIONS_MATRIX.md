# GP-AUT-01 — Matriz de Decisões Institucionais Pendentes

## Controle

| Campo | Registro |
| --- | --- |
| Instrumento | GP-AUT-01 |
| Data-base | 28/07/2026 |
| Versão | 1.0 |
| Finalidade | Estruturar decisões humanas necessárias à futura remediação |
| Fontes | GP-CERT-03, GP-REM-01, Constituição, DI-01 a DI-05 e estado da baseline |

## Regra dos identificadores

Os identificadores `AUT-PEND-*` são códigos de controle desta matriz. Eles não constituem decisões institucionais, não reservam numeração no namespace `DI` e não produzem efeitos normativos.

## Matriz

| ID | Impedimento | Decisão pendente | Autoridade responsável | Evidências requeridas | Documentos a criar ou atualizar após a decisão | Situação |
| --- | --- | --- | --- | --- | --- | --- |
| AUT-PEND-001 | IMP-01 | Aprovar o perímetro exato da baseline documental que poderá ser consolidada | Direção do Projeto ICFACTORY, conforme competência de reconhecimento da consolidação prevista na DI-05 | Inventário de arquivos; estado Git; classificação documental; validação de ausência de código, dados, mídia e arquivos estranhos | Decisão canônica de aprovação do perímetro; inventário/baseline; histórico, se exigido pela governança | PENDENTE |
| AUT-PEND-002 | IMP-01 | Autorizar a consolidação Git do perímetro aprovado | Direção do Projeto ICFACTORY | Decisão AUT-PEND-001 concluída; lista final; índice Git restrito; `git diff --check`; parecer técnico | Registro da autorização; registro factual da consolidação após sua execução | PENDENTE |
| AUT-PEND-003 | IMP-02 | Reconhecer documentalmente a autoria intelectual de cada ativo destinado ao pacote | Direção do Projeto ICFACTORY para reconhecimento institucional, condicionada à manifestação e às evidências dos autores | Declarações dos autores; histórico de criação; versões; contribuições; eventuais acordos preexistentes | Documento canônico de autoria; Registro Mestre; Inventário; Dossiê | PENDENTE |
| AUT-PEND-004 | IMP-02 | Formalizar a titularidade do patrimônio metodológico e documental, sem confundi-la com autoria ou representação | Autoridade institucional competente e partes com direitos envolvidos; competência definitiva não está individualizada nos documentos atuais | Resultado de AUT-PEND-003; instrumentos de cessão, atribuição ou reconhecimento; identificação das partes; eventual análise jurídica | Documento próprio de titularidade exigido pela DI-05; Inventário; Registro Mestre; Dossiê | PENDENTE |
| AUT-PEND-005 | IMP-03 | Aprovar ou rejeitar uma política de licenciamento e seu escopo por ativo | Direção do Projeto ICFACTORY, condicionada à titularidade e aos direitos de terceiros | AUT-PEND-003 e AUT-PEND-004; inventário de terceiros; proposta GP-CLS-05; restrições de dados, marcas, código e mídia | Decisão canônica de licenciamento; política/licença aprovada; Inventário; Dossiê; materiais de submissão | PENDENTE |
| AUT-PEND-006 | IMP-04 | Definir a forma e a identidade do proponente da futura submissão | Direção do Projeto ICFACTORY | Alternativas oficialmente admitidas; documentos pessoais ou jurídicos; relação do proponente com os ativos; confirmação de elegibilidade | Decisão canônica do proponente; checklist; formulário; Plano Executivo | PENDENTE |
| AUT-PEND-007 | IMP-04 | Escolher o campus destinatário para a futura submissão | Direção do Projeto ICFACTORY | Chamadas vigentes; modalidades; vagas; requisitos; unidade de interesse; confirmação oficial de cada alternativa considerada | Decisão ou registro canônico de escolha; checklist; Plano Executivo; matriz externa | PENDENTE |
| AUT-PEND-008 | IMP-06 | Aprovar o conteúdo institucional que será transposto para o formulário oficial | Direção do Projeto ICFACTORY | AUT-PEND-006 e AUT-PEND-007; formulário vigente; Inventário; Dossiê; evidências revisadas; dados da equipe e do negócio | Versão controlada das respostas; checklist; dossiê da submissão | PENDENTE |
| AUT-PEND-009 | IMP-07 | Deliberar sobre o atendimento interno dos requisitos externos confirmados | Direção do Projeto ICFACTORY | Inteiro teor oficial do regulamento; chamada e formulário do campus; matriz GP-CLS-06 atualizada por evidência oficial | Plano/checklist de atendimento; matriz de requisitos atualizada; pacote candidato | PENDENTE |
| AUT-PEND-010 | IMP-05 | Aprovar a versão institucional exata destinada à submissão | Direção do Projeto ICFACTORY, por competência expressa da DI-05 | AUT-PEND-001 a AUT-PEND-009 aplicáveis concluídas; pacote congelado; hashes; parecer de recertificação | Decisão canônica de aprovação da versão; manifesto do pacote | PENDENTE |
| AUT-PEND-011 | IMP-05 | Autorizar especificamente a submissão externa do pacote aprovado | Direção do Projeto ICFACTORY, por competência expressa da DI-05 | AUT-PEND-010; requisitos vigentes confirmados; termos revisados; representante DI-01; parecer de prontidão | Decisão canônica de autorização; checklist; registro posterior de envio | PENDENTE |

## Dependências externas que não são decisões do ICFACTORY

| ID | Confirmação necessária | Autoridade externa |
| --- | --- | --- |
| EXT-001 | Disponibilizar ou confirmar o inteiro teor do regulamento vigente | UTFPR/sprinT |
| EXT-002 | Confirmar chamada, vagas, formulário, documentos e condições do campus | Unidade sprinT do campus |
| EXT-003 | Confirmar a admissibilidade da categoria de proponente pretendida, quando não expressa | Unidade sprinT do campus |
| EXT-004 | Avaliar elegibilidade e nível de incubação | Instâncias oficiais de seleção da sprinT |

Nenhuma confirmação externa foi presumida ou substituída por decisão interna.

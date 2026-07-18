# GP-RG-08 — Protocolo de Integridade do Pacote Experimental

## 1. Identidade

| Campo | Registro |
|---|---|
| Protocolo | RG08-PIP v1.0 |
| Gate | GX-PKG |
| Entrada | pacote candidato e procedimento pre-registrado |
| Saída | pacote congelado, Registro de Verificação, classificação e `GO`/`NO-GO` |
| Aplicação | prospectiva; antes da execução substantiva |

Este protocolo é reutilizável e não foi aplicado a novo experimento nesta GP.

## 2. Condições de entrada

O preflight só começa quando existem:

1. autoridade para preparar e verificar o pacote;
2. experimento e procedimento delimitados;
3. responsável pelo pacote;
4. lista preliminar de artefatos e sua criticidade;
5. ambiente-alvo declarado;
6. regras de confidencialidade, propriedade e acesso;
7. local gravável para Manifesto e registros do preflight.

Ausência de condição de entrada produz `NO-GO` sem inspeção substantiva.

## 3. Convenções de localização

- declarar uma única `package_root` canônica;
- preferir localizadores relativos normalizados dentro da raiz;
- proibir resolução por pesquisa nominal, memória do coordenador ou histórico de conversa;
- proibir `..` que escape da raiz e registrar tratamento de links simbólicos; por padrão, links que escapem da raiz são bloqueantes;
- registrar sensibilidade a maiúsculas/minúsculas, codificação Unicode e separadores;
- se um artefato obrigatório nasceu como anexo externo, incorporar cópia legítima e imutável ao pacote ou fornecer repositório de custódia acessível a todos os executores com versão e hash verificáveis;
- URL viva ou recurso externo mutável não é entrada congelada; seu conteúdo obrigatório deve ser capturado legitimamente no pacote;
- caminho absoluto só é admissível quando o ambiente é único, controlado e declarado; para distribuição entre avaliadores, a cópia interna relativa é o padrão recomendado.

## 4. Procedimento

### Fase P0 — Delimitação

1. identificar OEG/ato, experimento, procedimento, OV/hipóteses e restrições;
2. separar autoridade de preparação da autoridade de execução;
3. enumerar todos os passos obrigatórios;
4. mapear para cada passo entradas, instrumentos, ferramentas, agentes e saídas;
5. marcar cada item como obrigatório, condicional ou opcional, com justificativa anterior ao teste.

Saída: mapa passo–dependência.

### Fase P1 — Montagem e Manifesto

1. criar `package_id` e versão;
2. declarar `package_root`;
3. copiar legitimamente os artefatos para localizadores canônicos;
4. atribuir `artifact_id` único;
5. registrar versão, origem, proprietário, permissão, formato e consumidores;
6. registrar referências cruzadas e anexos;
7. calcular bytes e SHA-256 de cada arquivo regular.

Saída: Manifesto candidato completo.

### Fase P2 — Teste de existência e resolução

Para cada item, o verificador deve partir apenas do Manifesto:

1. resolver o localizador sem busca auxiliar;
2. confirmar que há exatamente um alvo;
3. confirmar que o alvo permanece dentro da raiz/depósito autorizado;
4. registrar caminho canônico observado;
5. confirmar leitura pelo papel previsto;
6. confirmar que anexos e dependências resolvem pelo mesmo método.

Falha em obrigatório: registrar estado e não procurar substituto fora do pacote.

### Fase P3 — Teste criptográfico e de versão

1. recalcular bytes e SHA-256;
2. comparar com o Manifesto;
3. verificar versão declarada e ausência de colisão de IDs;
4. confirmar que arquivos gerados/compactados podem ser reproduzidos ou estão custodiados como binários congelados;
5. registrar ferramenta/comando de hash e timestamp.

Hash divergente nunca é corrigido no Manifesto durante a mesma verificação. O curador deve emitir nova versão candidata.

### Fase P4 — Integridade referencial e semântica mínima

1. verificar que toda referência obrigatória citada pelo procedimento existe no Manifesto;
2. verificar que nomes, IDs e versões usados nas instruções coincidem;
3. confrontar anexos declarados com anexos presentes;
4. confirmar que cada métrica tem entrada e denominador disponíveis;
5. confirmar que cada estado/regra de interpretação citado existe no instrumento correto;
6. confirmar que ordem, restrições e proibições não são contraditórias;
7. registrar ambiguidades sem resolvê-las por intenção presumida.

O teste não julga a verdade do conteúdo nem executa a análise do caso.

### Fase P5 — Acessibilidade e dry-run não substantivo

1. validar ferramentas, formatos e permissões necessárias;
2. validar destinos de saída e escrita exclusiva;
3. simular a sequência usando IDs/metadados ou fixture neutra, sem abrir resultados do caso além do mínimo necessário;
4. confirmar igualdade de cópias para avaliadores comparáveis por digest;
5. confirmar que nenhuma etapa pede fonte externa não congelada ou esclarecimento ad hoc;
6. testar instruções de parada, incidente e custódia.

Se o dry-run exigir interpretação substantiva, parar e redesenhar o teste para evitar contaminação.

### Fase P6 — Congelamento

1. fechar composição e conteúdo;
2. registrar `frozen_at` e versão;
3. recalcular todos os hashes;
4. gerar digest do Manifesto/pacote por método declarado;
5. tornar a cópia distribuída somente leitura quando o ambiente permitir;
6. registrar custodiante, retenção e acesso;
7. proibir alteração in-place.

Qualquer mudança posterior cria versão sucessora e exige novo preflight completo nos itens impactados, com revalidação do pacote inteiro antes de `GO`.

### Fase P7 — Verificação independente

1. entregar ao verificador somente a regra de resolução e o pacote candidato;
2. aplicar integralmente `RG_08_EXECUTABILITY_CHECKLIST.md`;
3. anexar evidência observável por check;
4. registrar acumulação de papéis e limitações;
5. classificar sem consultar memória ou fonte externa;
6. congelar o Registro de Verificação.

### Fase P8 — Certificação e decisão

O certificado deve registrar:

- pacote/versão/digest;
- ambiente e validade;
- contagem por estado;
- falhas bloqueantes e ressalvas;
- classe conforme `RG_08_CLASSIFICATION_CRITERIA.md`;
- `GO`, `GO CONDICIONAL` ou `NO-GO`;
- identidade do verificador e autoridade decisora;
- condições que invalidam o certificado.

`GO` não pode ser emitido para `PARCIALMENTE EXECUTÁVEL` ou `NÃO EXECUTÁVEL`.

### Fase P9 — Rechecagem pré-início

Imediatamente antes de qualquer leitura substantiva, cada executor:

1. confirma `package_id`, versão e digest;
2. resolve todos os itens obrigatórios pelo Manifesto;
3. confirma permissões e destino próprio de saída;
4. declara lista recebida e ausência de fonte adicional;
5. para antes do caso se houver divergência.

Essa rechecagem detecta alteração entre certificação e distribuição; não substitui P0–P8.

## 5. Registro de Verificação — modelo mínimo

| Campo | Conteúdo |
|---|---|
| `verification_id` | identificador único |
| pacote | ID, versão e digest |
| procedimento | ID e versão |
| ambiente | plataforma, raiz e ferramentas |
| autoridade | preparação, verificação e execução |
| verificador | identidade/papel/independência |
| checks | ID, estado, evidência, impacto e observação |
| incidentes | classe, momento e tratamento |
| ressalvas | alcance, responsável, prazo e aceitação |
| classificação | uma das quatro classes RG-08 |
| decisão | GO / GO CONDICIONAL / NO-GO |
| validade | evento/data que exige rechecagem |
| limitações | alcance não verificado |

## 6. Tratamento de falhas e mudanças

| Momento | Ocorrência | Tratamento |
|---|---|---|
| antes do congelamento | item faltante/ambíguo | curador corrige candidato; registrar no log de montagem |
| durante preflight | falha bloqueante | `NO-GO`; preservar evidência; emitir nova versão se corrigido |
| após certificação, antes do início | digest/acesso diverge | invalidar certificado; não iniciar |
| durante execução | item antes acessível torna-se indisponível | aplicar regra de suspensão/desvio da OEG; não substituir silenciosamente |
| após encerramento | descoberta de falha antiga | registrar revisão/auditoria prospectiva; não reescrever resultado |

Correção de localizador, conteúdo, criticidade ou instrumento nunca é editorial quando altera o que o executor pode acessar; exige versionamento.

## 7. Critérios de parada do preflight

Suspender e acionar governança quando:

- houver risco de exposição não autorizada;
- a propriedade/permissão não puder ser determinada;
- verificar exigiria abrir resultado proibido ou usar fonte externa;
- a autoridade de preparação não cobrir a ação necessária;
- o pacote estiver sendo alterado por terceiro durante a verificação;
- houver necessidade de modificar metodologia ou resultado anterior.

Falha operacional comum sem risco é registrada como `NO-GO`, não necessariamente como suspensão da GP metodológica.

## 8. Aplicação em múltiplos avaliadores

- gerar cópias a partir do mesmo pacote congelado;
- comparar digest entregue e rechecado por cada avaliador;
- fornecer localizadores relativos idênticos;
- separar diretórios de saída;
- registrar qualquer dependência específica de ambiente;
- não fornecer esclarecimento assimétrico após o início;
- se um avaliador falhar na rechecagem, nenhum deve iniciar até decisão governada sobre igualdade.

## 9. Cadeia de fundamentação do protocolo

- **Premissas:** verificações dispersas não asseguram que composição, resolução, acesso e procedimento foram testados na ordem correta.
- **Evidências:** RG-06 verificou hashes dentro do pre-registro; RG-07 também enumerou hashes, mas a distribuição falhou em um localizador essencial.
- **Inferência:** o controle deve separar montagem, resolução, hash, dry-run, congelamento, certificação e rechecagem.
- **Fundamentação:** cada fase produz evidência distinta e impede que a fase seguinte mascare uma ausência anterior.
- **Decisão:** adotar P0–P9 como protocolo reutilizável obrigatório para GX-PKG.
- **Limitações:** o fluxo ainda não foi cronometrado nem pilotado em sistemas diferentes.
- **Validação:** todas as exigências mínimas da OEG-RG-08 aparecem como fases e checks objetivos.

## 10. Estado final

**PROTOCOLO REUTILIZÁVEL FORMALIZADO, SEM EXECUÇÃO EXPERIMENTAL NESTA GP.**


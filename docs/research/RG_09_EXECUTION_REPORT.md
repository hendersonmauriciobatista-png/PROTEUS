# GP-RG-09 — Relatório de Execução do Piloto GX-PKG

## 1. Identidade

| Campo | Registro |
|---|---|
| Plano | `RG_09_SYNTHETIC_EXPERIMENT_PLAN.md` |
| Casos congelados | `RG_09_TEST_CASES.md` |
| Passagens | V1 e V2, invocações separadas no mesmo ambiente |
| Checks | CK-01 a CK-36 em cada caso/passagem |
| Alteração de fixtures após congelamento | nenhuma |
| Fonte externa | nenhuma |
| Alteração em RG-08 | nenhuma |

Legenda: `AT` = ATENDIDO; `AR` = ATENDIDO_COM_RESSALVA; `NA` = NAO_ATENDIDO; `NV` = NAO_VERIFICADO; `NAP` = NAO_APLICAVEL.

## 2. Evidência operacional bruta resumida

V1 e V2 observaram exatamente:

| Caso | Arquivos | Hashes correspondentes | Manifesto | Autoridade | Procedimento | Input | Instrumento | Contrato | Fonte externa proibida declarada |
|---|---:|---:|---|---|---|---|---|---|---|
| A | 6 | 6 | sim | sim | sim | sim | sim | sim | sim |
| B | 6 | 6 | sim | sim | sim | sim | sim | sim | sim |
| C | 5 | 5 | sim | sim | sim | **não** | sim | sim | sim |
| D | 1 controle | 1 controle | **não** | **não** | **não** | **não** | **não** | **não** | não declarada por pacote inexistente |

O diretório de saída `docs/research/` existia nas duas passagens. Os seis instrumentos RG-08 continuaram presentes. Os comandos de V1/V2 foram somente leitura sobre os fixtures.

## 3. Checklist completo — Caso A

| Check | V1 | V2 | Evidência/justificativa |
|---|---|---|---|
| CK-01 | AT | AT | OEG-RG-09 e `AUTH-A-v1` delimitam preflight sintético |
| CK-02 | AT | AT | início substantivo proibido; decisão do gate prevista pela OEG/plano |
| CK-03 | AT | AT | `GP-RG-09-CASE-A`, `PROC-A-v1` e escopo unívocos |
| CK-04 | AT | AT | Manifesto contém ID, versão, raiz, ambiente, responsáveis e timestamp |
| CK-05 | AT | AT | procedimento mapeia input, instrumento e contrato |
| CK-06 | AT | AT | cinco artefatos classificados `yes` antes do teste |
| CK-07 | AT | AT | IDs/versões únicos no Manifesto |
| CK-08 | AT | AT | 6/6 arquivos presentes |
| CK-09 | AT | AT | todos os caminhos relativos resolveram sem busca |
| CK-10 | AT | AT | um alvo por localizador |
| CK-11 | AT | AT | nenhum caminho escapa de `case_a` |
| CK-12 | NAP | NAP | nenhum anexo adicional declarado pelo procedimento |
| CK-13 | AT | AT | bytes dos cinco artefatos e Manifesto coincidem com congelamento |
| CK-14 | AT | AT | 6/6 SHA-256 coincidem |
| CK-15 | AT | AT | SHA-256, `Get-FileHash` e momento registrados |
| CK-16 | AT | AT | PROC-A referencia INPUT-A, INST-A e OUT-A existentes |
| CK-17 | AT | AT | nomes, IDs e versões coerentes |
| CK-18 | AT | AT | plano RG-09 e instrumento A congelados |
| CK-19 | AT | AT | denominador de um marker ALPHA disponível |
| CK-20 | AT | AT | regra `metadata-only acknowledgement` identificada |
| CK-21 | AT | AT | todos os Markdown lidos em UTF-8 |
| CK-22 | AT | AT | Harness possuía leitura e diretório de relatório acessível |
| CK-23 | AT | AT | destino `docs/research/RG_09_EXECUTION_REPORT.md` resolvível |
| CK-24 | AT | AT | dry-run percorreu três passos por metadados |
| CK-25 | AT | AT | Manifesto declara nenhuma fonte externa |
| CK-26 | AT | AT | conteúdo sintético-público e retenção declarados |
| CK-27 | AT | AT | curador/verificador e acumulação do Harness declarados |
| CK-28 | AT | AT | V1/V2 recalcularam o mesmo digest congelado |
| CK-29 | AT | AT | plano proíbe mutação/fonte externa e separa as passagens |
| CK-30 | AT | AT | versão v1.0 e regra de nova versão declaradas |
| CK-31 | AT | AT | Manifesto e digest recalculados após montagem |
| CK-32 | NAP | NAP | nenhuma ressalva no pacote A |
| CK-33 | AT | AT | plano define D3, parada e nova versão |
| CK-34 | AT | AT | V1/V2 rechecavam ID, existência e hashes antes da classe |
| CK-35 | AT | AT | cada artefato possui consumidor/referência |
| CK-36 | AT | AT | esta saída e os hashes permitem auditoria |

Classificação V1: **INTEGRALMENTE EXECUTÁVEL — GO**.

Classificação V2: **INTEGRALMENTE EXECUTÁVEL — GO**.

### Cadeia A-V1

- **Premissas:** classe integral exige todos os checks aplicáveis atendidos e zero ressalvas/falhas bloqueantes.
- **Evidências:** 6/6 arquivos e hashes, referências resolvidas, dry-run completo; 34 AT e 2 NAP justificados.
- **Inferências:** todos os passos obrigatórios podem ser percorridos no ambiente declarado.
- **Fundamentação:** critérios RG-08 § 4.1 e regra `no package, no start`.
- **Decisão:** INTEGRALMENTE EXECUTÁVEL — GO.
- **Limitações:** pacote mínimo, sintético e no mesmo ambiente do curador.
- **Validação:** resultado coincide com o esperado congelado e nenhum check bloqueante falhou.

### Cadeia A-V2

- **Premissas:** V2 usa os mesmos critérios sem editar V1 ou fixture.
- **Evidências:** segunda invocação reproduziu 6/6 hashes e os mesmos 36 estados.
- **Inferências:** a decisão é repetível nas condições declaradas.
- **Fundamentação:** igualdade de digest e aplicação da mesma regra decisória.
- **Decisão:** INTEGRALMENTE EXECUTÁVEL — GO.
- **Limitações:** repetição pelo mesmo Harness não prova reprodução interavaliadores.
- **Validação:** classe, decisão e checks coincidem integralmente com V1.

## 4. Checklist completo — Caso B

| Check | V1 | V2 | Evidência/justificativa |
|---|---|---|---|
| CK-01 | AT | AT | OEG-RG-09 e `AUTH-B-v1` delimitam preflight |
| CK-02 | AT | AT | decisão condicional prevista; experimento substantivo proibido |
| CK-03 | AT | AT | IDs, escopo e procedimento unívocos |
| CK-04 | AT | AT | Manifesto completo |
| CK-05 | AT | AT | quatro passos com dependências mapeadas |
| CK-06 | AT | AT | cinco artefatos obrigatórios declarados |
| CK-07 | AT | AT | IDs/versões únicos |
| CK-08 | AT | AT | 6/6 arquivos presentes |
| CK-09 | AT | AT | caminhos relativos resolvem sem usar display label |
| CK-10 | AT | AT | um alvo por localizador |
| CK-11 | AT | AT | nenhum escape de raiz |
| CK-12 | NAP | NAP | nenhum anexo adicional |
| CK-13 | AT | AT | bytes coincidem |
| CK-14 | AT | AT | 6/6 hashes coincidem |
| CK-15 | AT | AT | algoritmo, ferramenta e momento registrados |
| CK-16 | AT | AT | referências canônicas resolvem |
| CK-17 | AT | AT | procedimento usa `INPUT-B-v1`; rótulo legado não é localizador |
| CK-18 | AT | AT | plano e instrumento congelados |
| CK-19 | AT | AT | denominador BETA disponível |
| CK-20 | AT | AT | interpretação identificada |
| CK-21 | AT | AT | formatos legíveis |
| CK-22 | AT | AT | permissões suficientes |
| CK-23 | AT | AT | destino de relatório resolvível |
| CK-24 | AT | AT | dry-run de quatro passos completo |
| CK-25 | AT | AT | nenhuma fonte externa |
| CK-26 | AT | AT | custódia sintética declarada |
| CK-27 | AT | AT | papéis/acumulação declarados |
| CK-28 | AT | AT | mesmo digest em V1/V2 |
| CK-29 | AT | AT | restrições das passagens declaradas |
| CK-30 | AT | AT | pacote v1.0 congelado |
| CK-31 | AT | AT | Manifesto/digest pós-montagem registrados |
| CK-32 | AR | AR | rótulo legado possui alcance, impacto e aceite; não afeta passo obrigatório |
| CK-33 | AT | AT | incidente/mudança exigem nova versão |
| CK-34 | AT | AT | rechecagem aplicada |
| CK-35 | AT | AT | IDs canônicos ligam artefatos a passos |
| CK-36 | AT | AT | registro auditável |

Classificação V1: **EXECUTÁVEL COM RESSALVAS — GO CONDICIONAL**.

Classificação V2: **EXECUTÁVEL COM RESSALVAS — GO CONDICIONAL**.

### Cadeia B-V1

- **Premissas:** ressalva só é não bloqueante se não alterar entrada, procedimento, métrica, interpretação, acesso ou custódia.
- **Evidências:** 6/6 hashes; referências usam ID canônico; display label legado é apenas descritivo; CK-32 = AR.
- **Inferências:** o pacote é integralmente percorrível, mas carrega limitação documental explícita.
- **Fundamentação:** RG-08 § 4.2 permite GO condicional sem falha obrigatória.
- **Decisão:** EXECUTÁVEL COM RESSALVAS — GO CONDICIONAL.
- **Limitações:** caso não explora fronteira ambígua entre rótulo e identificador operacional.
- **Validação:** nenhuma falha bloqueante; resultado esperado reproduzido.

### Cadeia B-V2

- **Premissas:** a ressalva e sua criticidade permaneceram congeladas.
- **Evidências:** V2 observou os mesmos 6/6 hashes e CK-32 = AR.
- **Inferências:** a decisão condicional é repetível no desenho.
- **Fundamentação:** digest, evidência e regra decisória idênticos.
- **Decisão:** EXECUTÁVEL COM RESSALVAS — GO CONDICIONAL.
- **Limitações:** mesmo Harness e cenário construído para a classe.
- **Validação:** 36/36 estados coincidem com V1.

## 5. Checklist completo — Caso C

| Check | V1 | V2 | Evidência/justificativa |
|---|---|---|---|
| CK-01 | AT | AT | OEG e AUTH-C presentes |
| CK-02 | AT | AT | decisão condicionada ao gate |
| CK-03 | AT | AT | caso/procedimento delimitados |
| CK-04 | AT | AT | Manifesto completo, incluindo estado ausente |
| CK-05 | AT | AT | passos/dependências mapeados |
| CK-06 | AT | AT | input marcado obrigatório antes do teste |
| CK-07 | AT | AT | IDs únicos, inclusive INPUT-C-v1 |
| CK-08 | NA | NA | `input.md` obrigatório fisicamente ausente |
| CK-09 | NA | NA | localizador `input.md` não resolve |
| CK-10 | NA | NA | localizador obrigatório conduz a zero alvos |
| CK-11 | AT | AT | localizadores declarados não escapam da raiz |
| CK-12 | NAP | NAP | nenhum anexo adicional declarado |
| CK-13 | NA | NA | bytes do input não observáveis |
| CK-14 | NA | NA | hash do input não verificável |
| CK-15 | AT | AT | método de hash registrado para itens presentes |
| CK-16 | AT | AT | referência resolve para ID declarado, embora o alvo físico falhe |
| CK-17 | AT | AT | nomes/IDs do procedimento coincidem com o Manifesto |
| CK-18 | AT | AT | plano e instrumento presentes/congelados |
| CK-19 | NA | NA | denominador depende do marker ausente de INPUT-C-v1 |
| CK-20 | AT | AT | regra de interpretação existe no instrumento |
| CK-21 | NA | NA | formato do input obrigatório não pode ser lido porque está ausente |
| CK-22 | AT | AT | permissões dos itens presentes suficientes |
| CK-23 | AT | AT | destino de saída existe |
| CK-24 | NA | NA | dry-run para no passo 1 |
| CK-25 | AT | AT | nenhuma fonte externa permitida |
| CK-26 | AT | AT | custódia dos itens sintéticos declarada |
| CK-27 | AT | AT | papéis declarados |
| CK-28 | AT | AT | V1/V2 receberam o mesmo conjunto incompleto/digest |
| CK-29 | AT | AT | proibição de fornecer input após início declarada |
| CK-30 | AT | AT | pacote incompleto está congelado como v1.0 |
| CK-31 | AT | AT | digest dos arquivos presentes recalculado |
| CK-32 | NAP | NAP | ocorrência é falha bloqueante, não ressalva não bloqueante |
| CK-33 | AT | AT | correção exigiria nova versão |
| CK-34 | AT | AT | rechecagem detectou ausência antes do conteúdo |
| CK-35 | NA | NA | INPUT-C não pode ser rastreado até conteúdo/origem observável |
| CK-36 | AT | AT | falha e evidências registráveis |

Classificação V1: **PARCIALMENTE EXECUTÁVEL — NO-GO**.

Classificação V2: **PARCIALMENTE EXECUTÁVEL — NO-GO**.

### Cadeia C-V1

- **Premissas:** uma entrada obrigatória ausente é falha bloqueante; subconjunto íntegro pode manter valor diagnóstico.
- **Evidências:** 5/5 arquivos presentes coincidem; `INPUT-C-v1` declarado obrigatório não existe; dry-run para no passo 1.
- **Inferências:** há pacote parcialmente inspecionável, mas o procedimento completo não pode começar.
- **Fundamentação:** EX-01/03/04/10 e RG-08 § 4.3 determinam NO-GO.
- **Decisão:** PARCIALMENTE EXECUTÁVEL — NO-GO.
- **Limitações:** uma única falha simples e conhecida; não mede falhas combinadas.
- **Validação:** nenhuma fonte substituta foi buscada e o resultado coincide com o esperado.

### Cadeia C-V2

- **Premissas:** o input não poderia ser criado entre passagens.
- **Evidências:** segunda invocação repetiu 5/5 hashes presentes e ausência do input.
- **Inferências:** o bloqueio é estável sob repetição no mesmo ambiente.
- **Fundamentação:** o mesmo requisito obrigatório falhou antes da execução.
- **Decisão:** PARCIALMENTE EXECUTÁVEL — NO-GO.
- **Limitações:** repetição não é independente tecnologicamente.
- **Validação:** checks, classe e decisão coincidem com V1.

## 6. Checklist completo — Caso D

| Check | V1 | V2 | Evidência/justificativa |
|---|---|---|---|
| CK-01 | NA | NA | pacote não possui ato de autoridade |
| CK-02 | NA | NA | nenhuma autoridade de início vinculada a pacote identificável |
| CK-03 | NA | NA | escopo/procedimento do pacote inexistentes |
| CK-04 | NA | NA | Manifesto ausente |
| CK-05 | NV | NV | passos/dependências não podem ser determinados |
| CK-06 | NV | NV | criticidade de itens não existe em Manifesto |
| CK-07 | NV | NV | IDs/versões do pacote não verificáveis |
| CK-08 | NA | NA | artefatos operacionais ausentes |
| CK-09 | NA | NA | nenhum localizador operacional disponível |
| CK-10 | NV | NV | unicidade de alvo não verificável |
| CK-11 | NV | NV | raiz/localizadores não declarados |
| CK-12 | NV | NV | anexos não inventariados |
| CK-13 | NV | NV | bytes esperados do pacote inexistentes |
| CK-14 | NV | NV | hashes do pacote inexistentes |
| CK-15 | NV | NV | algoritmo/ferramenta do pacote não declarados |
| CK-16 | NV | NV | referências cruzadas não existem |
| CK-17 | NV | NV | instruções/IDs inexistentes |
| CK-18 | NA | NA | pre-registro/instrumentos do pacote ausentes |
| CK-19 | NV | NV | métricas/denominadores indeterminados |
| CK-20 | NV | NV | estados/interpretação indeterminados |
| CK-21 | NV | NV | formatos obrigatórios não declarados |
| CK-22 | NV | NV | papéis/permissões do pacote ausentes |
| CK-23 | NV | NV | destino de saída não declarado pelo pacote |
| CK-24 | NA | NA | dry-run não pode iniciar sem procedimento |
| CK-25 | NV | NV | dependência externa não pode ser excluída |
| CK-26 | NV | NV | custódia/propriedade não definidas |
| CK-27 | NA | NA | papéis do pacote ausentes |
| CK-28 | NV | NV | não existe pacote distribuível para comparar |
| CK-29 | NV | NV | controles de independência não definidos |
| CK-30 | NA | NA | pacote não congelado porque não existe composição |
| CK-31 | NA | NA | Manifesto/digest do pacote não existem |
| CK-32 | NAP | NAP | não há ressalva delimitada; há indeterminação estrutural |
| CK-33 | NA | NA | regras de incidente/desvio ausentes |
| CK-34 | NA | NA | procedimento de rechecagem ausente |
| CK-35 | NA | NA | rastreabilidade integral inexistente |
| CK-36 | NA | NA | não há Registro de Verificação vinculável a pacote/digest |

Classificação V1: **NÃO EXECUTÁVEL — NO-GO**.

Classificação V2: **NÃO EXECUTÁVEL — NO-GO**.

### Cadeia D-V1

- **Premissas:** Manifesto, autoridade e procedimento são condições estruturais mínimas.
- **Evidências:** só existe declaração externa do cenário; todos os componentes operacionais do pacote estão ausentes.
- **Inferências:** não é possível delimitar subconjunto executável seguro nem verificar dependências.
- **Fundamentação:** falhas bloqueantes múltiplas satisfazem RG-08 § 4.4.
- **Decisão:** NÃO EXECUTÁVEL — NO-GO.
- **Limitações:** caso extremo e evidente; não avalia corrupção estrutural sutil.
- **Validação:** gate parou antes de dry-run e coincidiu com a verdade congelada.

### Cadeia D-V2

- **Premissas:** V2 não pode completar estrutura ausente por inferência.
- **Evidências:** segunda invocação observou somente o mesmo controle do cenário e nenhuma entrada operacional.
- **Inferências:** indeterminação estrutural permanece não executável.
- **Fundamentação:** repetir ausência não a converte em pacote parcial.
- **Decisão:** NÃO EXECUTÁVEL — NO-GO.
- **Limitações:** mesmo Harness e falha deliberadamente ampla.
- **Validação:** checks, classe e decisão coincidem com V1.

## 7. Desvios e incidentes

| ID | Registro | Classe | Impacto |
|---|---|---|---|
| RG09-D0 | nenhum fixture, critério, métrica ou resultado esperado alterado após congelamento | D0 | nenhum |
| RG09-I01 | acumulação de curador, verificador e documentador pelo mesmo Harness | ameaça pre-registrada | limita reprodução independente; não altera a classificação do pacote sintético |
| RG09-I02 | resultados esperados conhecidos antes de V1/V2 | desenho de conformidade | eleva risco de confirmação; mitigado por checks e hashes objetivos |

Nenhuma condição de suspensão da OEG-RG-09 ocorreu: não foi necessário alterar RG-08, nenhuma classificação careceu de fundamentação e não foi detectada inconsistência estrutural impeditiva.

## 8. Estado da execução

**QUATRO CENÁRIOS EXECUTADOS EM DUAS PASSAGENS; OITO DECISÕES FUNDAMENTADAS; NENHUM FALSO GO OU NO-GO OBSERVADO.**


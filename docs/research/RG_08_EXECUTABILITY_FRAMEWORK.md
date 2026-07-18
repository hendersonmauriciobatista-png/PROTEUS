# GP-RG-08 — Framework de Executabilidade Experimental

## 1. Identidade e estado

| Campo | Registro |
|---|---|
| GP | GP-RG-08 |
| Autoridade | OEG-RG-08, referenciada à DF-RG-08 aprovada |
| Natureza | institucionalização documental de etapa metodológica |
| Versão | RG08-EXE v1.0 |
| Objeto | executabilidade e integridade do pacote experimental |
| Alcance | futuras execuções experimentais GDC-R |
| Estado | FRAMEWORK FORMALIZADO; VIGÊNCIA OPERACIONAL CONDICIONADA À APROVAÇÃO DOCUMENTAL |

Este documento não repete a RG-07, não reavalia seus resultados e não promove hipótese. A RG-07 permanece `TESTE_INCONCLUSIVO`.

## 2. Base documental

| ID | Documento | Contribuição observada | Limite |
|---|---|---|---|
| E08-01 | OEG-RG-08 | autoridade, objetivo, requisitos mínimos e produtos | não autoriza novo experimento |
| E08-02 | `RG_05_EXPERIMENTAL_PROTOCOL.md` §§ 9, 11, 12, 14, 16–17, 20–23 | gates, pacote obrigatório, pre-registro, evidência, suspensão e versões | não continha preflight autônomo e classificável |
| E08-03 | `RG_06_PREREGISTRATION.md` §§ 4–12 | exemplo de pacote e instrumentos hashados, acesso restrito e regra de suspensão | piloto com um executor e acervo conhecido |
| E08-04 | `RG_06_CP01_AUDIT.md` §§ 2–8 | demonstra que conteúdo rastreável pode continuar formalmente não conforme | um caso retrospectivo |
| E08-05 | `RG_06_CLOSURE_REPORT.md` §§ 4–8 | resultados e limites do primeiro piloto | não valida generalidade |
| E08-06 | `RG_07_EXPERIMENT_PLAN.md` §§ 3–10 | pacote nominal de 13 entradas e igualdade A/B | um item não tinha localizador resolvível |
| E08-07 | `RG_07_EXECUTION_A.md` e `RG_07_EXECUTION_B.md` | detecção independente de 12/13 entradas e suspensão | nenhuma unidade de caso foi analisada |
| E08-08 | `RG_07_COMPARATIVE_MATRIX.md` | convergência na detecção e no tratamento da falha | não mede reprodução de caso |
| E08-09 | `RG_07_AUDIT.md` | NC-RG07-01: hash/nome sem caminho ou cópia resolvível; classe D3 | não autoriza correção retroativa |
| E08-10 | `RG_07_CLOSURE_REPORT.md` § 6 | recomenda cópia imutável, preflight, regra de ausências e nova autoridade | recomendações ainda não pilotadas |
| E08-11 | `RG_03_ARCHITECTURE.md` e `RG_03_INVARIANTS.md` | identidade, proveniência, resolução de referências e preservação histórica | arquitetura da cadeia, não protocolo de pacote |

## 3. Definições formais

### 3.1 Pacote experimental

Conjunto fechado e versionado de artefatos, metadados, instrumentos, regras de acesso e localizadores necessários para que um executor autorizado realize integralmente o procedimento pre-registrado sem memória, substituição tácita ou fonte externa não congelada.

### 3.2 Executabilidade experimental

Propriedade verificável segundo a qual, no ambiente e no intervalo declarados, todos os passos obrigatórios de um procedimento podem ser iniciados e concluídos a partir do pacote congelado, com entradas acessíveis, referências resolvíveis, instrumentos identificados e saídas registráveis.

Formalmente, para pacote `P`, procedimento `R`, ambiente declarado `A` e instante de congelamento `t`:

`EXE(P,R,A,t) = existência ∧ identidade ∧ integridade ∧ resolução ∧ acesso ∧ suficiência operacional ∧ congelamento ∧ rastreabilidade`.

A propriedade é contextual: mudança de pacote, procedimento, ambiente ou versão exige nova verificação. Executabilidade não prova validade científica, correção factual, qualidade da decisão, reprodução bem-sucedida ou apoio a hipótese.

### 3.3 Integridade do pacote

Propriedade documental pela qual identidade, conteúdo, proveniência, relações, versões, anexos, permissões e histórico do pacote correspondem ao Manifesto congelado, sem ausência, substituição ou ambiguidade não declarada.

### 3.4 Localizador resolvível

Referência que, a partir de uma raiz canônica declarada e pelo mesmo procedimento entregue aos executores, conduz deterministicamente a exatamente um artefato existente, permitido e verificável. Nome e hash sem regra de resolução não constituem localizador.

### 3.5 Artefato obrigatório

Entrada, instrumento, autorização, instrução ou anexo cuja ausência impede ao menos um passo obrigatório, altera denominador, caso, critério, interpretação, independência ou custódia. A obrigatoriedade deve ser declarada antes do preflight.

### 3.6 Congelamento

Ato de fechar a composição e o conteúdo do pacote sob versão, timestamp, inventário e hashes, vedando mutação silenciosa. Nova composição cria nova versão e invalida o certificado anterior.

### 3.7 Preflight de executabilidade

Verificação anterior ao início substantivo que testa o pacote sem interpretar resultados do caso. Seu produto é um Registro de Verificação e uma classificação; não é execução experimental.

## 4. Princípios

1. **No package, no start:** nenhum experimento inicia sem pacote classificado.
2. **Resolução antes de leitura:** existência e acesso são demonstrados pelo caminho entregue, não por busca ad hoc.
3. **Conteúdo antes de rótulo:** nome, tamanho ou hash esperado não substituem o arquivo observável.
4. **Imutabilidade verificável:** a versão distribuída coincide com a versão certificada.
5. **Simetria de entrada:** avaliadores comparados recebem o mesmo pacote verificável.
6. **Fonte fechada:** informação obrigatória externa deve ser incorporada legitimamente ao pacote ou a execução recebe `NO-GO`.
7. **Ausência não é zero:** ausência é codificada e produz efeito conforme criticidade.
8. **Separação de papéis:** preparação, verificação e autorização são distinguíveis; acumulação é declarada como ressalva.
9. **Não retroatividade:** o framework não corrige nem reclassifica resultados anteriores.
10. **Conclusão proporcional:** uma ocorrência fundamenta o controle preventivo, não sua eficácia universal.

## 5. Elementos necessários à execução

| Grupo | Elementos mínimos |
|---|---|
| Autoridade | ato autorizador de preparação/preflight; autoridade de execução; escopo e restrições |
| Identidade | `package_id`, versão, experimento, responsável, datas e raiz canônica |
| Procedimento | pre-registro, sequência, gates, parada, desvios e estados permitidos |
| Entradas | caso, documentos, anexos, dados, referências e dependências obrigatórias |
| Instrumentos | modelos, protocolos, checklists, métricas, denominadores e regras de interpretação |
| Agentes | papéis, independência, acesso, treinamento e conflitos |
| Ambiente | plataforma, ferramentas, versões, permissões e restrições observáveis necessárias |
| Custódia | confidencialidade, propriedade, retenção, redação e acesso autorizado |
| Saídas | destinos graváveis, formato, identificação, congelamento e auditoria |
| Manifesto | inventário completo, criticidade, localizador, tamanho, hash, proveniência e referências |

## 6. Requisitos formais de executabilidade

| ID | Requisito | Teste objetivo | Falha bloqueante quando |
|---|---|---|---|
| EX-01 | existência física | cada item obrigatório resolve para arquivo/recurso observável | qualquer obrigatório está ausente |
| EX-02 | identificação única | IDs e versões não colidem e apontam para um único item | identidade é ambígua ou duplicada |
| EX-03 | integridade por hash | tamanho e SHA-256 observado coincidem com o Manifesto | obrigatório diverge ou não pode ser verificado |
| EX-04 | caminho resolvível | resolução parte de `package_root`, sem busca ou memória | caminho falha, escapa da raiz ou depende de contexto não entregue |
| EX-05 | anexos integrais | todos os anexos normativamente necessários estão inventariados | anexo obrigatório está omitido/incompleto |
| EX-06 | referências consistentes | toda referência cruzada obrigatória resolve para ID/versão existente | referência órfã altera procedimento ou interpretação |
| EX-07 | acessibilidade | leitura/execução/gravação exigida é possível pelos papéis previstos | permissão, formato ou ferramenta impede passo obrigatório |
| EX-08 | congelamento | versão, inventário, hashes e timestamp estão fechados | composição pode mudar sem nova versão |
| EX-09 | rastreabilidade | item resolve a origem, papel no procedimento e dependentes | não se conhece por que o item é necessário ou quem o usa |
| EX-10 | suficiência operacional | simulação não substantiva percorre todos os passos e dependências | um passo exige fonte, decisão ou dado não congelado |
| EX-11 | simetria | digest/cópia entregue é igual para papéis comparáveis | entradas diferem sem desenho pre-registrado |
| EX-12 | custódia e direitos | acesso e uso estão autorizados no escopo | risco de propriedade/confidencialidade impede acesso legítimo |

## 7. Manifesto mínimo do pacote

Campos de cabeçalho:

- `package_id`, `package_version`, `experiment_id`;
- `package_root`, plataforma/ambiente declarado e algoritmo de hash;
- autoridade de preparação, autoridade de execução esperada e responsáveis;
- `frozen_at`, status de confidencialidade e regra de retenção;
- digest do próprio Manifesto calculado no fechamento ou registro externo equivalente.

Campos por item:

- `artifact_id`, título, tipo e versão;
- obrigatório/condicional/opcional e justificativa;
- localizador relativo canônico;
- bytes e SHA-256;
- origem, proprietário/custodiante e permissão;
- consumidor/passo do procedimento;
- referências de entrada e dependentes;
- formato/ferramenta necessária;
- estado de acesso e observações.

## 8. Papéis

| Papel | Responsabilidade | Não pode presumir |
|---|---|---|
| Curador do pacote | montar, inventariar e congelar | que sua própria montagem prova executabilidade |
| Verificador de executabilidade | aplicar protocolo e checklist sem ler resultados além do necessário | conteúdo ausente, permissões ou intenção do curador |
| Autoridade experimental | emitir `GO`/`NO-GO` com base no certificado | que ressalva bloqueante pode ser aceita informalmente |
| Executor/avaliador | revalidar digest e acesso antes da leitura substantiva | que certificação antiga vale após mudança |
| Auditor de encerramento | confrontar pacote usado, certificado, incidentes e saídas | que `GO` garante sucesso ou validade científica |

Acumulação de papéis deve ser declarada. Para experimento interavaliadores, o verificador não deve ser um dos avaliadores sempre que houver alternativa viável.

## 9. Gate institucional proposto

Identificador: **GX-PKG — Verificação de Executabilidade e Integridade do Pacote**.

Posição lógica:

`preparação → montagem → congelamento → GX-PKG → autorização/início experimental → rechecagem do executor → execução`.

O gate é aditivo e não renumera GX-00 a GX-11 da RG-05. Futuras OEGs experimentais devem citar `package_id`, versão, classificação, certificado e digest. Se a autorização da GP preceder a montagem por necessidade administrativa, ela autoriza apenas preparação/preflight; o início substantivo continua condicionado a GX-PKG.

## 10. Saídas obrigatórias do gate

1. Manifesto congelado;
2. Registro de Verificação preenchido;
3. checklist com evidência por item;
4. lista de desvios/ressalvas;
5. classificação objetiva;
6. decisão `GO` ou `NO-GO`;
7. assinatura/identidade do verificador e timestamp;
8. digest do pacote certificado;
9. validade e condições de rechecagem.

## 11. Cadeias de fundamentação

### D08-FW-01 — Criar gate autônomo

- **Premissas:** GX-03 exige pacote congelado; congelamento nominal não garante resolução ou acesso.
- **Evidências:** RG-07 listou 13 hashes, mas um artefato obrigatório não tinha cópia/localizador resolvível; A/B suspenderam.
- **Inferência:** uma verificação objetiva entre montagem e início pode detectar a classe de falha antes de contaminar a execução.
- **Fundamentação:** a falha era de entrega/resolução, não de conteúdo do caso, e foi bloqueante sob as regras de parada.
- **Decisão:** instituir GX-PKG como gate aditivo anterior ao início substantivo.
- **Limitações:** derivação baseada principalmente em RG-07; eficácia preventiva ainda não foi pilotada.
- **Validação:** protocolo, checklist e classificação RG-08 operacionalizam o gate sem editar RG-05/RG-07.

### D08-FW-02 — Exigir resolução além de hash

- **Premissas:** hash esperado só é verificável quando o artefato é alcançável.
- **Evidências:** 12 hashes coincidiram e o 13º permaneceu não verificável apesar de nome, bytes e hash esperados.
- **Inferência:** inventário criptográfico sem regra de localização é insuficiente.
- **Fundamentação:** executabilidade depende de o executor obter o mesmo conteúdo pelo caminho fornecido.
- **Decisão:** EX-03 e EX-04 são controles distintos e ambos bloqueantes para itens obrigatórios.
- **Limitações:** SHA-256 prova correspondência de bytes, não veracidade ou segurança do conteúdo.
- **Validação:** o checklist requer evidência separada para resolução, tamanho e digest.

### D08-FW-03 — Restringir o alcance da classificação

- **Premissas:** pacote executável pode alimentar método inadequado ou gerar resultado negativo.
- **Evidências:** RG-06 executou seu pacote, mas classificou a cadeia original `NAO_CONFORME` e OV-06 `TESTE_INCONCLUSIVO`.
- **Inferência:** executabilidade, conformidade da cadeia e validade científica são propriedades diferentes.
- **Fundamentação:** fundi-las transformaria sucesso operacional em apoio epistemológico.
- **Decisão:** certificado GX-PKG autoriza início operacional, nunca hipótese, qualidade ou validade.
- **Limitações:** fronteiras ainda devem ser testadas em pacotes futuros.
- **Validação:** todos os produtos RG-08 repetem essa separação e proíbem promoção automática.

## 12. Limitações

- framework derivado de acervo interno e uma falha protocolar observada;
- nenhum pacote foi executado ou reexecutado nesta GP;
- portabilidade entre sistemas de arquivos e ferramentas ainda não foi testada;
- independência do verificador pode não ser viável em equipes pequenas;
- hash não detecta erro semântico já presente no conteúdo congelado;
- `GX-PKG` permanece proposta institucional até aprovação documental e adoção por futura autoridade.

## 13. Estado final

**CONCEITO DE EXECUTABILIDADE FORMALMENTE DEFINIDO E GATE GX-PKG PROPOSTO, SEM VALIDAÇÃO EMPÍRICA OU EFEITO RETROATIVO.**


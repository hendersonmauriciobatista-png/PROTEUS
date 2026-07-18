# GP-RG-03 — Representacao Arquitetural Da Cadeia

## 1. Objetivo E Notacao

Representar visualmente a arquitetura GDC-R definida em `RG_03_ARCHITECTURE.md`. Os diagramas sao vistas do mesmo modelo documental; nao sao fluxos cognitivos nem arquitetura de software.

| Simbolo | Significado |
|---|---|
| P | Premissa |
| E | Evidencia |
| I | Inferencia |
| F | Fundamentacao |
| D | Decisao |
| V | Validacao |
| R | Registro estrutural de Revisao, nao conceito epistemico |
| M | Manifesto estrutural da cadeia |
| linha continua | relacao oficial tipada |
| linha tracejada | anotacao, contexto ou conceito experimental |
| no cinza | versao historica preservada |

O conteudo das instancias pode pertencer a qualquer dominio. Nenhum diagrama exige PROTEUS, ICFACTORY, software, IA ou tipo especifico de decisor.

## 2. Vista Estrutural Principal

```mermaid
flowchart LR
    M["M — Manifesto e estado verificavel"]
    P["P — Premissa"]
    E["E — Evidencia"]
    I["I — Inferencia"]
    F["F — Fundamentacao"]
    D["D — Decisao"]
    V["V — Validacao"]
    EN["E' — Evidencia do resultado"]
    C["Criterio de Avaliacao\nHIPOTESE OBSERVACIONAL"]

    M -. delimita .-> P
    M -. delimita .-> E
    M -. delimita .-> I
    M -. delimita .-> F
    M -. delimita .-> D
    M -. delimita .-> V
    P -->|AR-01 CONDICIONA| I
    E -->|AR-02 SUPORTA| I
    P -->|AR-03 COMPOE| F
    E -->|AR-04 COMPOE| F
    I -->|AR-05 COMPOE| F
    F -->|AR-06 FUNDAMENTA| D
    D -->|AR-07 SUBMETE| V
    V -->|AR-08 PRODUZ OBSERVACAO| EN
    C -. anotacao experimental .-> V
```

Leitura: P e I sao opcionais no Perfil Minimo Governado quando genuinamente nao aplicaveis; E, F e D sao obrigatorios para uma decisao governada. V e obrigatoria quando concluida e deve estar pendente de forma explicita enquanto o resultado ainda nao existir.

## 3. Vista Do Ciclo Controlado De Revisao

```mermaid
flowchart TD
    S0["Snapshot S0 preservado"]
    G["Gatilho observavel\nnova E, conflito ou V negativa"]
    R["R — Registro de Revisao"]
    A["Analise de alcance pelas arestas"]
    N["Nos e arestas sucessores"]
    F1["F' — Fundamentacao recomposta"]
    D1["D' — mantida, revisada, revogada ou nova"]
    V1["V' — Revalidacao"]
    E1["E' — Resultado observado"]
    S1["Snapshot S1 e estado verificavel"]

    S0 --> G
    G --> R
    R --> A
    A --> N
    N --> F1
    F1 --> D1
    D1 --> V1
    V1 --> E1
    E1 --> S1
    S1 -. novo gatilho permitido .-> R
    S0 -. permanece acessivel .-> S1
```

O retorno somente e permitido entre snapshots versionados. Um ciclo de sustentacao dentro do mesmo snapshot e proibido.

## 4. Vista De Multiplas Evidencias E Inferencias

```mermaid
flowchart LR
    E1["E-01"] --> I1["I-01"]
    E2["E-02"] --> I1
    E2 --> I2["I-02"]
    E3["E-03"] --> I2
    P1["P-01"] --> I1
    P2["P-02"] --> I2
    E1 --> F1["F-01"]
    E2 --> F1
    E3 --> F1
    I1 --> F1
    I2 --> F1
    P1 --> F1
    P2 --> F1
    F1 --> D1["D-01"]
    D1 --> V1["V-01"]
```

Propriedades demonstradas estruturalmente:

* uma Evidencia pode suportar varias Inferencias;
* uma Inferencia pode depender de varias Evidencias;
* Fundamentacao pode agregar entradas heterogeneas;
* compartilhamento nao elimina origem, metodo ou limitacoes individuais.

## 5. Vista De Multiplas Fundamentacoes

```mermaid
flowchart LR
    E1["E-01"] --> F1["F-01 — viabilidade"]
    I1["I-01"] --> F1
    E2["E-02"] --> F2["F-02 — risco"]
    I2["I-02"] --> F2
    E3["E-03"] --> F3["F-03 — conformidade"]
    P1["P-01"] --> F3
    F1 --> D1["D-01"]
    F2 --> D1
    F3 --> D1
    D1 --> V1["V-01"]
```

Uma Decisao pode receber varias Fundamentacoes complementares. Se forem conflitantes, D deve registrar o conflito e o motivo da escolha; a multiplicidade nao pode ser usada para ocultar divergencia.

## 6. Vista De Decisoes Dependentes E Reutilizacao Controlada

```mermaid
flowchart TD
    E1["E-01 — origem preservada"]
    F1["F-01"]
    F2["F-02"]
    D1["D-01"]
    D2["D-02"]
    V1["V-01"]
    V2["V-02"]

    E1 -->|AR-04| F1
    E1 -->|AR-19 COMPARTILHA| F2
    F1 --> D1
    F2 --> D2
    D1 -->|AR-20 DEPENDE| D2
    D1 --> V1
    D2 --> V2
```

Cada Decisao conserva Fundamentacao propria. A dependencia D-01→D-02 nao substitui F-02→D-02.

## 7. Vista De Relacoes Proibidas

```mermaid
flowchart LR
    P["P"] -.->|PROIBIDO: suporte direto| D["D"]
    E["E"] -.->|PROIBIDO: suporte direto| D
    I["I"] -.->|PROIBIDO: suporte direto| D
    D -.->|PROIBIDO: prova da propria correcao| D
    D -.->|PROIBIDO: sustentar F que a sustenta| F["F"]
    F -.->|PROIBIDO: circularidade| D
    V["V"] -.->|PROIBIDO: sobrescrita| D
```

Essas arestas nao pertencem ao GDC-R. Quando uma fonte contem texto misto, seus registros devem ser desmembrados e tipados.

## 8. Exemplo Completo A — Revisao Por Validacao Negativa

Exemplo documental abstrato, inspirado apenas na forma do caso fundador e independente de dominio:

1. `P-A01`: condicao operacional inicial e adotada.
2. `E-A01` e `E-A02`: observacoes obtidas por metodos declarados.
3. `I-A01`: interpretacao sustentada por ambas as evidencias.
4. `F-A01`: agrega premissa, evidencias, inferencia, alternativas e riscos.
5. `D-A01`: autoriza uma opcao.
6. `V-A01`: compara resultado esperado e observado; resultado `REJEITADA`.
7. `E-A03`: registra o resultado negativo observado.
8. `R-A01`: abre revisao e congela o snapshot anterior.
9. `P-A02`: substitui P-A01 com motivo rastreado.
10. `I-A02`: deriva nova interpretacao de E-A03 e demais evidencias aplicaveis.
11. `F-A02`: recomposta sem apagar F-A01.
12. `D-A02`: revisa D-A01.
13. `V-A02`: revalida o resultado e encerra em estado verificavel.

```mermaid
flowchart LR
    P1["P-A01"] --> I1["I-A01"]
    E1["E-A01"] --> I1
    E2["E-A02"] --> I1
    P1 --> F1["F-A01"]
    E1 --> F1
    E2 --> F1
    I1 --> F1
    F1 --> D1["D-A01"]
    D1 --> V1["V-A01 REJEITADA"]
    V1 --> E3["E-A03"]
    V1 --> R1["R-A01"]
    P1 -->|SUPERADA POR| P2["P-A02"]
    E3 --> I2["I-A02"]
    P2 --> I2
    I2 --> F2["F-A02"]
    E3 --> F2
    F2 --> D2["D-A02"]
    D1 -->|REVISA| D2
    D2 --> V2["V-A02"]
```

## 9. Exemplo Completo B — Multiplas Fundamentacoes E Nao Acao

Exemplo hipotetico aplicavel a auditoria, pesquisa, gestao, software ou decisao humana:

* `E-B01`: dado de viabilidade;
* `E-B02`: dado de risco;
* `E-B03`: dado de conformidade;
* `I-B01`: viabilidade parcial;
* `I-B02`: risco material nao mitigado;
* `F-B01`: fundamentacao tecnica favoravel;
* `F-B02`: fundamentacao de risco desfavoravel;
* `F-B03`: fundamentacao de conformidade inconclusiva;
* `D-B01`: nao executar por enquanto, declarando condicoes para revisao;
* `V-B01`: confirma que nenhuma execucao ocorreu e mantem estado `ENCERRADA_SEM_ACAO`, com pendencia registrada.

O exemplo mostra que multiplas Fundamentacoes nao precisam convergir e que uma Decisao governada pode ser nao acao. Ele nao demonstra eficacia empirica da arquitetura.

## 10. Exemplo De Independencia De Dominio

| Dominio possivel | Conteudo de P/E/I/F/D/V | Elementos GDC-R alterados? |
|---|---|---|
| desenvolvimento de software | requisitos, testes, interpretacao, justificativa, decisao de release, validacao | nao |
| auditoria | criterios normativos, achados, analise, parecer, decisao, verificacao posterior | nao |
| pesquisa cientifica | condicoes, observacoes, analise, justificativa, decisao experimental, validacao | nao |
| gestao de projetos | restricoes, indicadores, projecoes, justificativa, priorizacao, revisao de resultado | nao |
| decisao humana | contexto declarado, registros disponiveis, interpretacao, ponderacao, escolha, revisao | nao |
| sistema assistido por IA | entradas observaveis, saidas verificadas, inferencias declaradas, suporte, decisao autorizada, validacao | nao |

Esta tabela demonstra neutralidade semantica do desenho, nao aplicabilidade empirica comprovada nos dominios listados.

## 11. Criterio De Avaliacao Experimental

```mermaid
flowchart LR
    DF["Requisito em D/F"] -.-> CA["Anotacao de Criterio\nHIPOTESE OBSERVACIONAL"]
    CA -.-> V["V"]
    V --> E["E do resultado"]
```

A linha tracejada indica que a anotacao nao integra o conjunto oficial de nos. Sua ocorrencia na modelagem e evidencia adicional de utilidade potencial, nao promocao conceitual.

## 12. Limites Da Representacao

* diagramas omitem campos para preservar legibilidade;
* setas representam relacoes documentais, nao causalidade mental;
* exemplos abstratos nao sao experimentos;
* neutralidade estrutural nao prova adequacao em todos os dominios;
* multiplicidade e ciclos ainda requerem teste no protocolo GP-RG-04;
* nenhuma vista define formato fisico, banco de dados ou implementacao.

## 13. Estado Final

**REPRESENTACAO GDC-R FORMALIZADA — EXEMPLOS NAO EMPIRICOS**

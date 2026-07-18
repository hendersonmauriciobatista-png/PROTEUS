# GP-RG-06 - Selecao Formal Do Caso Experimental

## 1. Identidade E Autoridade

| Campo | Registro |
|---|---|
| Ordem | OEG-RG-06 |
| Pesquisa | Governanca da Fundamentacao das Decisoes (GDC-R) |
| Modo | Pesquisa Experimental Controlada |
| Autoridade experimental | pesquisadores responsaveis pelo ICFACTORY |
| Executor delegado | Harness Governado (Codex) |
| Data da deliberacao | 18/07/2026 |
| Escopo | avaliacao documental de CP-01 a CP-05 e selecao de um primeiro piloto |
| Restricoes | nenhuma alteracao de codigo, arquitetura, funcionalidade ou midia; nenhuma promocao de hipotese ou generalizacao |

Proveniencia da autoridade: OEG-RG-06, secoes I, II e IV. A Ordem autoriza o primeiro piloto e determina a selecao formal anterior ao pre-registro.

## 2. Regra De Selecao Fixada

Antes da aplicacao do caso, foram fixadas as seguintes regras:

1. aplicar primeiro os criterios bloqueantes CI-01, CI-05, CI-06, CI-08 e CI-10 e os gates GC-00 a GC-09 de `RG_05_CASE_SELECTION_FRAMEWORK.md`;
2. candidato com falha bloqueante nao pode ser selecionado;
3. entre elegiveis, atribuir 0, 1 ou 2, sem pesos, nas oito dimensoes da matriz da secao 8 do framework;
4. selecionar a maior soma; em empate, priorizar, nesta ordem, suficiencia documental, auditabilidade e menor complexidade compativel com o primeiro piloto;
5. pontuacao nao substitui a fundamentacao;
6. nenhum resultado experimental da GP-RG-06 integra a selecao.

Limitacao: o acervo de CP-01 ja continha um relato favoravel anterior (`PI_07A_DECISION_FOUNDATION_GOVERNANCE_REPORT.md`) e era conhecido pelo executor durante a triagem. Isso cria risco de contaminacao e impede alegar selecao cega. A mitigacao adotada foi usar criterios documentais preexistentes, manter todos os candidatos e registrar o conflito.

## 3. Avaliacao Documental Dos Candidatos

| ID | Completude documental | Rastreabilidade | Historico de revisoes | Riqueza de evidencias | Potencial de reproducao | Limitacoes | Elegibilidade |
|---|---|---|---|---|---|---|---|
| CP-01 | ALTA: auditoria previa, relatorio de execucao e cadeia PI-07A delimitada | ALTA: IDs P/E/I/D/V, fontes, metodos, hashes e vinculos declarados | ALTO: P-007 -> P-008 e validacao inicial/final preservadas | ALTA: 18 evidencias heterogeneas, quatro decisoes e resultados tecnicos | ALTO COM RESSALVAS: pacote textual congelavel; pipeline e hashes declarados | caso interno; conhecimento previo; referencia e reconstrucao nao sao independentes; ausencia de avaliadores independentes | ELEGIVEL_COM_RESSALVAS |
| CP-02 | PARCIAL: existe acervo arquitetural amplo, mas o candidato nao delimita qual decisao arquitetural e qual snapshot | CONDICIONADA: documentos possuem referencias, mas a unidade decisoria candidata permanece ampla | PARCIAL: varias GP/PE registram evolucao, sem manifesto unico do candidato | ALTA em volume, porem heterogenea e dispersa | MEDIO: acervo preservado, mas escopo amplo prejudica pacote comum e denominadores | risco de dependencia interna; complexidade alta; CI-01 nao demonstrado para uma unica decisao | INELEGIVEL NESTA DELIBERACAO por CI-01/CE-03 |
| CP-03 | INSUFICIENTE: nao foi localizado dossie proprio de uma decisao aberta de separacao | BAIXA: ha mencao no framework, sem cadeia ou autoridade decisoria delimitada | AUSENTE | BAIXA no acervo identificado | BAIXO: nao ha pacote congelavel do caso | pode afetar a custodia da propria pesquisa; decisao prospectiva nao formalizada | INELEGIVEL por CI-01 e CI-05 |
| CP-04 | INSUFICIENTE para fase E | BAIXA/NAO DETERMINADA | AUSENTE para o alerta candidato | BAIXA: indicadores, limites e fontes da EUREKA nao formalizados | BAIXO enquanto persistir o bloqueio | CE-10 e bloqueio expresso no protocolo RG-05 | ADIADO; INELEGIVEL nesta execucao |
| CP-05 | AUSENTE: categoria sem caso identificado | AUSENTE | AUSENTE | AUSENTE | AUSENTE | sem objeto, autorizacao, custodiante ou acervo | INELEGIVEL por CI-01, CI-05, CI-06, CI-08 e CI-10 |

Ausencias documentais nao foram substituidas por inferencias. A avaliacao limita-se ao repositorio disponivel em 18/07/2026.

## 4. Priorizacao Dos Elegiveis

| Dimensao (0-2) | CP-01 | CP-02 | CP-03 | CP-04 | CP-05 |
|---|---:|---:|---:|---:|---:|
| alinhamento OV/QE | 2 | 2 | 1 | 0 | 1 |
| suficiencia documental | 2 | 1 | 0 | 0 | 0 |
| auditabilidade | 2 | 1 | 0 | 0 | 0 |
| evidencia contraria identificavel | 2 | 2 | 0 | 0 | 0 |
| diversidade DGA-01 | 0 | 0 | 0 | 0 | 2 |
| fenomeno dinamico | 2 | 2 | 0 | 1 | 1 |
| viabilidade etica/juridica | 2 | 2 | 1 | 1 | 0 |
| independencia avaliativa | 1 | 1 | 0 | 0 | 1 |
| **Total indicativo** | **13** | **11** | **2** | **2** | **5** |

As somas de candidatos inelegiveis sao informativas e nao compensam falhas bloqueantes.

## 5. Gates Do CP-01

| Gate | Registro | Estado |
|---|---|---|
| GC-00 | OEG-RG-06 autoriza a triagem | ATENDIDO |
| GC-01 | decisao identificavel, fontes documentais, custodia interna e evidencia contraria observavel | ATENDIDO COM RESSALVA de conhecimento previo |
| GC-02 | fase A/C e OV-01, OV-02, OV-04, OV-05 e OV-06 sao coerentes com o pacote | ATENDIDO |
| GC-03 | inventario foi separado da nova analise, mas o relato PI-07A ja expunha resultados anteriores | ATENDIDO COM RESSALVA; risco de contaminacao registrado |
| GC-04 | uso somente documental no repositorio autorizado; nenhuma midia sera alterada | ATENDIDO |
| GC-05 | executor acumula coordenacao, avaliacao e auditoria; independencia nao demonstrada | ATENDIDO COM RESSALVA; OV-06 nao podera receber apoio confirmatorio |
| GC-06 | nao existe grupo convencional nem comparacao causal | NAO_APLICAVEL; analise descritiva |
| GC-07 | oferece primeiro teste retrospectivo com revisao negativa preservada; nao oferece diversidade externa | ATENDIDO NO LIMITE DO PRIMEIRO PILOTO |
| GC-08 | pacote, instrumentos e metricas podem ser congelados antes das reconstrucoes | ATENDIDO |
| GC-09 | selecao formal emitida pelo executor delegado sob a OEG-RG-06 | ATENDIDO |

## 6. Fundamentacao Governada Da Selecao

### Premissas

* PS-01: o primeiro piloto deve privilegiar reconstrucao controlavel, nao generalidade.
* PS-02: falhas bloqueantes nao podem ser compensadas por volume documental.
* PS-03: conhecimento previo e acumulo de papeis devem limitar interpretacao, nao ser ocultados.

### Evidencias

* ES-01: `RG_05_CASE_SELECTION_FRAMEWORK.md` define criterios, gates e candidatos.
* ES-02: CP-01 possui tres documentos diretamente delimitados e uma revisao explicita.
* ES-03: CP-02 nao identifica uma decisao arquitetural unica no registro candidato.
* ES-04: CP-03 nao possui dossie proprio localizado.
* ES-05: CP-04 esta bloqueado expressamente nas secoes 8 e 11 do framework e fase E do protocolo.
* ES-06: CP-05 nao foi identificado nem autorizado como caso concreto.

### Inferencias

* IS-01: CP-01 e o unico candidato que combina unidade delimitada, pacote congelavel, evidencia contraria e historico revisional sem exigir alteracao de protocolo. Confianca: ALTA; limite: acervo interno e conhecido.
* IS-02: selecionar CP-02 exigiria antes redefinir a unidade, o que criaria procedimento/escopo durante a execucao. Confianca: ALTA; limite: um recorte futuro pode torna-lo elegivel.
* IS-03: CP-03 a CP-05 nao permitem reconstrucao documental sob os gates atuais. Confianca: ALTA para o acervo observado; limite: documentos externos ao repositorio podem existir.

### Fundamentacao

CP-01 apresenta a melhor justificativa metodologica para um piloto retrospectivo exploratorio porque permite congelar uma cadeia real, observar uma tentativa rejeitada e testar os cinco OV autorizados sem alterar codigo ou midia. Seu risco de contaminacao e a falta de independencia reduzem o alcance de OV-06, mas estao declarados e nao tornam o caso irrecuperavel. Os demais candidatos exigiriam delimitar nova decisao, formalizar indicadores ou obter caso/autorizacao inexistentes.

Alternativas consideradas: selecionar CP-02 apos recorte; adiar toda a GP ate CP-05; executar CP-04. Foram descartadas, respectivamente, por mudanca de escopo necessaria, desnecessidade de caso externo para o primeiro piloto e bloqueio CE-10.

### Decisao

**DS-01 - CP-01 SELECIONADO_POR_DELIBERACAO para o primeiro piloto GP-RG-06, fases A/C, exclusivamente documental.**

Autoridade: OEG-RG-06. Confianca da decisao: ALTA quanto a adequacao ao primeiro piloto; BAIXA para qualquer inferencia de generalidade. Ambiguidades: fronteira exata entre uma decisao editorial composta e quatro decisoes subordinadas; sera preservada como uma cadeia com quatro D.

### Validacao Da Decisao

Todos os criterios bloqueantes e gates aplicaveis ao CP-01 foram avaliados; as ressalvas nao exigem alteracao do protocolo e foram convertidas em limites pre-registraveis. Resultado: **SELECAO VALIDADA COM RESSALVAS DOCUMENTAIS**.

## 7. Proveniencia Documental

* OEG-RG-06, recebida em 18/07/2026;
* `docs/research/RG_05_CASE_SELECTION_FRAMEWORK.md`;
* `docs/research/RG_05_EXPERIMENTAL_PROTOCOL.md`;
* `docs/research/RG_05_CLOSURE_REPORT.md`;
* inventario local de documentos Markdown e pesquisa textual dos candidatos em 18/07/2026.

Nenhuma hipotese foi promovida e nenhum resultado do piloto foi produzido neste documento.

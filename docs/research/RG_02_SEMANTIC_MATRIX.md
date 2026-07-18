# GP-RG-02 — Matriz Semantica Dos Conceitos

## 1. Objetivo

Comparar os conceitos do modelo, explicitar fronteiras semanticas, registrar ambiguidades e oferecer testes documentais de classificacao. Esta matriz complementa `RG_02_CONCEPTUAL_MODEL.md` e nao substitui as definicoes completas nele registradas.

## 2. Convencoes De Leitura

* “Observavel” significa que o registro documental pode ser inspecionado; nao significa que o conteudo seja necessariamente fato verdadeiro.
* “Revisavel” significa que o estado pode mudar com historico preservado.
* “Invalidar” significa motivar uma transicao formal de estado; nenhum registro apaga outro automaticamente.
* “Derivado” significa obtido por relacao explicita com registros anteriores.
* “Produzir decisao” nao significa causalidade automatica: somente uma Fundamentacao pode habilitar uma Decisao, que ainda exige declaracao e autoridade.
* `Criterio de Avaliacao` aparece somente para comparacao e permanece hipotese observacional.

## 3. Matriz Comparativa Principal

| Conceito | Finalidade | Origem tipica | Observavel como registro? | Revisavel? | Pode motivar invalidacao? | Pode ser derivado? | Pode produzir decisao? |
|---|---|---|---|---|---|---|---|
| Premissa | declarar condicao adotada | norma, contexto, autoridade, estimativa explicita | sim; sua adocao e observavel, sua verdade pode estar pendente | sim | sim; se contestada, pode exigir revisao de inferencias e fundamentacoes | pode ser extraida de autoridade ou proposta; nao e conclusao inferencial por definicao | nao; apenas condiciona |
| Evidencia | registrar observacao verificavel | fonte e metodo declarados | sim | sim quanto a admissibilidade, alcance e estado; o historico da coleta permanece | sim; pode contradizer premissas ou sustentar revisoes por meio de analise formal | nao no sentido inferencial; e coletada ou observada | nao; apenas sustenta |
| Inferencia | explicitar interpretacao do observado | evidencias e, quando aplicavel, premissas | sim como enunciado; o conteudo e interpretativo | sim | sim; pode contestar premissas ou fundamentacoes quando sustentada | sim, obrigatoriamente de evidencia | nao; contribui para fundamentacao |
| Fundamentacao | demonstrar por que uma escolha e suportada | premissas, evidencias, inferencias, alternativas, limites e riscos | sim | sim | sim; fundamentacao revisada pode exigir revisar decisao | sim, como composicao relacional | habilita, mas nao cria automaticamente |
| Decisao | registrar escolha ou nao acao governada | fundamentacao e autoridade | sim | sim por manutencao, revisao ou revogacao | sim; uma decisao pode encerrar ou substituir outra por ato formal | sim no sentido de ser suportada, mas nao e conclusao logica automatica | e o proprio ato decisorio |
| Validacao | comparar resultado esperado e observado | decisao, procedimento e resultado | sim | sim; nova validacao nao apaga a anterior | sim; pode motivar revisao de qualquer elo aplicavel | sim, da comparacao documentada | nao diretamente; produz base para nova fundamentacao |
| Criterio de Avaliacao | hipoteticamente predefinir como julgar resultado | requisito, risco, fundamentacao ou plano de validacao | sim | sim, com versao e momento preservados | potencialmente; sua aplicacao pode orientar conclusao de validacao | pode ser formulado a partir de requisitos | nao; orienta validacao — HIPOTESE OBSERVACIONAL |

## 4. Matriz De Propriedades E Dependencias

| Conceito | Fonte obrigatoria? | Metodo obrigatorio? | Evidencia obrigatoria? | Confianca obrigatoria? | Limitacoes obrigatorias? | Alternativas obrigatorias? | Saida documental primaria |
|---|---:|---:|---:|---:|---:|---:|---|
| Premissa | sim | nao | nao | quando incerta | sim, quando relevantes | nao | condicao adotada e estado |
| Evidencia | sim | sim | nao aplicavel | sim | sim | nao | observacao delimitada |
| Inferencia | por referencia | regra de derivacao inteligivel | sim | sim | sim | quando houver interpretacoes concorrentes | proposicao interpretativa |
| Fundamentacao | por referencias | encadeamento explicito | sim | incorporada na avaliacao de suficiencia | sim | sim, quando razoaveis | suporte auditavel de escolha |
| Decisao | autoridade e fundamentacao | ato declaratorio | indiretamente, via fundamentacao | quando houver incerteza relevante | sim | registradas na fundamentacao ou decisao | escolha governada |
| Validacao | decisao e resultados | sim | produz novas evidencias | sim ou qualificacao equivalente | sim | nao; resultados alternativos devem ser previstos | avaliacao do resultado |
| Criterio de Avaliacao | sim | regra de aplicacao | nao necessariamente | ainda nao definido | sim | nao | condicao de avaliacao — experimental |

## 5. Analise Semantica Das Fronteiras Obrigatorias

### 5.1 Premissa × Evidencia

**Ambiguidade:** uma afirmacao obtida de documento pode parecer simultaneamente condicao adotada e fato observado.

**Distincao:** Evidencia registra o que foi observado, por qual metodo e com qual limite. Premissa registra que uma proposicao sera adotada como base no escopo.

**Teste:** pergunte “estou registrando uma observacao ou adotando uma condicao?”. Se ambos forem necessarios, criar dois registros relacionados.

**Exemplo:** a existencia do requisito de nao editar antes da auditoria pode ser evidenciada pela leitura do comando; a obrigacao adotada para a execucao e a Premissa P-003.

**Risco se confundidos:** uma condicao contestavel pode adquirir aparencia indevida de fato comprovado.

### 5.2 Evidencia × Inferencia

**Ambiguidade:** resultados tecnicos frequentemente ja chegam acompanhados de significado presumido.

**Distincao:** Evidencia preserva dado, fonte e metodo; Inferencia declara o significado derivado e seu grau de confianca.

**Teste:** remova expressões como “portanto”, “indica”, “adequado” ou “insuficiente”. O que permanecer verificavel tende a ser Evidencia; a conclusao removida tende a ser Inferencia.

**Exemplo:** “decodificacao concluiu com codigo 0” e evidencia; “o arquivo esta tecnicamente decodificavel” e inferencia. Nenhuma das duas prova qualidade editorial.

**Risco se confundidos:** interpretacao passa a parecer fato e suas limitacoes deixam de ser avaliadas.

### 5.3 Inferencia × Fundamentacao

**Ambiguidade:** uma inferencia forte pode ser usada como justificativa abreviada de uma escolha.

**Distincao:** Inferencia e uma proposicao derivada. Fundamentacao e composicao relacional orientada a uma decisao, incluindo alternativas, riscos, informacao contraria e suficiencia.

**Teste:** o registro responde apenas “o que os dados indicam?” ou tambem “por que esta escolha, diante das alternativas e limites?”. Somente a segunda funcao caracteriza Fundamentacao.

**Exemplo:** I-004 concluiu que nao havia narracao pronta. A fundamentacao de D-003 acrescentou licenca, escopo, alternativas e riscos para justificar a nao insercao de audio.

**Risco se confundidos:** uma conclusao parcial e tratada como suporte completo de decisao.

### 5.4 Fundamentacao × Decisao

**Ambiguidade:** textos decisorios frequentemente misturam justificativa e comando.

**Distincao:** Fundamentacao demonstra suporte; Decisao declara a escolha e cria compromisso governado. Fundamentacao pode concluir insuficiencia sem autorizar uma acao.

**Teste:** existe verbo declaratorio de escolha, escopo e autoridade? Sem isso, ha recomendacao ou fundamentacao, nao Decisao.

**Exemplo:** “as alternativas nao possuem fonte licenciada” integra a fundamentacao; “manter a saida sem audio” e a decisao D-003.

**Risco se confundidos:** uma analise passa a ser executada como se tivesse autorizacao.

### 5.5 Decisao × Validacao

**Ambiguidade:** a decisao pode incluir resultado esperado e ser erroneamente tratada como prova de que o resultado ocorreu.

**Distincao:** Decisao registra o compromisso; Validacao compara posteriormente o esperado com o observado por procedimento declarado.

**Teste:** o registro escolhe o que fazer ou examina o que aconteceu? Escolha e Decisao; comparacao e Validacao.

**Exemplo:** D-004 autorizou tratamentos visuais minimos. A primeira validacao rejeitou os parametros tipograficos e a final aprovou a revisao com ressalva.

**Risco se confundidos:** execucao ou intencao e apresentada como sucesso comprovado.

## 6. Ambiguidades Adicionais

### 6.1 Premissa × Hipotese De Pesquisa

Uma Premissa e adotada para operar em escopo delimitado; uma hipotese de pesquisa e proposicao submetida a avaliacao. H-RG-001 nao se torna Premissa verdadeira por orientar a pesquisa. Se uma hipotese for usada como condicao experimental, os dois papeis devem ser registrados separadamente.

### 6.2 Evidencia × Fonte

Fonte e a origem; Evidencia e o registro delimitado obtido da fonte por metodo. Citar um arquivo inteiro nao identifica automaticamente a evidencia relevante.

### 6.3 Validacao × Nova Evidencia

O resultado observado durante a validacao e nova Evidencia. A conclusao “aprovada”, “rejeitada” ou “inconclusiva” pertence a Validacao. Registrar ambos separadamente evita circularidade.

### 6.4 Fundamentacao Como Artefato × Fundamentacao Como Relacao

Interpretacoes consideradas:

1. tratar Fundamentacao apenas como texto autonomo;
2. tratar Fundamentacao apenas como conjunto de relacoes;
3. tratar como artefato composto cuja funcao essencial e materializar relacoes.

Adota-se provisoriamente a terceira interpretacao, pois ela permite identificacao e versionamento sem reduzir a fundamentacao a narrativa solta. Confianca: **MEDIA-ALTA**. A GP-RG-03 deve testar sua adequacao estrutural.

### 6.5 Cadeia Linear × Grafo De Revisao

Uma apresentacao linear e util para leitura inicial, mas E-RG02-004 registra retroacao: Validacao rejeitou parametros, gerou nova Evidencia, revisou Premissa e produziu nova Inferencia. Adota-se grafo com ciclos de revisao. Confianca: **ALTA para a existencia de retroacao no caso fundador; BAIXA para afirmar completude universal do grafo**.

### 6.6 Criterio De Avaliacao × Validacao × Fundamentacao

Interpretacoes razoaveis:

* conceito autonomo que antecede Validacao;
* atributo ou componente da Validacao;
* restricao derivada da Fundamentacao ou da Decisao.

Nao ha evidencia suficiente para escolher definitivamente. O modelo preserva `Criterio de Avaliacao` como **HIPOTESE OBSERVACIONAL** fora da cadeia oficial.

## 7. Teste De Classificacao

Aplicar as perguntas na ordem:

1. O registro descreve dado ou evento obtido por fonte e metodo? Classificar como **Evidencia**.
2. O registro adota uma proposicao como condicao de trabalho? Classificar como **Premissa**.
3. O registro deriva significado de evidencias? Classificar como **Inferencia**.
4. O registro conecta elementos e alternativas para justificar uma escolha? Classificar como **Fundamentacao**.
5. O registro declara escolha, autorizacao, rejeicao ou nao acao? Classificar como **Decisao**.
6. O registro compara resultado esperado e observado? Classificar como **Validacao**.
7. O registro apenas define antecipadamente como avaliar? Registrar separadamente como **Criterio de Avaliacao — HIPOTESE OBSERVACIONAL**.

Se mais de uma resposta for positiva, desmembrar o conteudo em registros tipados e relaciona-los. Se nenhuma for suficiente, classificar como `NAO DETERMINADO`, registrar a ambiguidade e nao forcar enquadramento.

## 8. Casos Positivos E Negativos Consolidados

| Conceito | Caso positivo | Caso negativo ou classificacao incorreta |
|---|---|---|
| Premissa | requisito de auditoria previa adotado como P-003 | resultado de `ffprobe` chamado de premissa |
| Evidencia | E-014 com fonte, metodo e amostra | “esta bonito” sem metodo ou observador identificado |
| Inferencia | I-007 derivada de E-014 e limitada ao pipeline | preferencia presumida do usuario sem evidencia |
| Fundamentacao | D-003 conecta fontes, inferencias, alternativas e riscos | lista de links sem justificar escolha |
| Decisao | preservar o Kdenlive em D-001 | “o projeto e renderizavel” sem ato de escolha |
| Validacao | rejeicao inicial e aprovacao final de D-004 preservadas | “foi executado, logo aprovado” |
| Criterio de Avaliacao | hash deve permanecer identico — exemplo provisorio | criterio ajustado depois para transformar falha em sucesso |

## 9. Ambiguidades Remanescentes

| ID | Ambiguidade | Estado | Tratamento recomendado |
|---|---|---|---|
| A-RG02-001 | autonomia de `Criterio de Avaliacao` | ABERTA | manter experimental ate evidencias multidominio |
| A-RG02-002 | cardinalidade Fundamentacao → Decisao em casos compostos | PARCIALMENTE DEFINIDA | testar na GP-RG-03 |
| A-RG02-003 | estados minimos por conceito | PROPOSTOS, NAO VALIDADOS | estruturar e testar sem alterar registros historicos |
| A-RG02-004 | limiar de suficiencia de uma Fundamentacao | ABERTA E DEPENDENTE DO DOMINIO | definir mecanismo proporcional ao risco na GP-RG-03/04 |
| A-RG02-005 | quando uma observacao qualitativa e Evidencia admissivel | ABERTA | exigir metodo, observador, amostra e limitacoes; testar no protocolo |
| A-RG02-006 | tratamento de decisoes tacitas ou emergenciais | FORA DO CASO FUNDADOR | incluir como caso de teste futuro sem presumir solucao |

## 10. Regras De Desambiguacao

1. Classificar a funcao do registro, nao o formato do arquivo.
2. Separar observacao e interpretacao mesmo quando escritas na mesma frase de origem.
3. Nao usar autoridade da fonte como substituto de metodo ou alcance.
4. Nao permitir que Inferencia sem Evidencia ingresse em Fundamentacao.
5. Nao confundir suficiencia no escopo com verdade universal.
6. Nao confundir Decisao com execucao nem execucao com Validacao.
7. Criar novo registro e vinculo ao revisar; nunca sobrescrever silenciosamente.
8. Preservar classificacao `NAO DETERMINADO` quando a evidencia semantica for insuficiente.
9. Declarar confianca quando a fronteira permanecer incerta.
10. Manter o conceito experimental separado visual e semanticamente.

## 11. Limitacoes

* a matriz foi derivada de autoridades internas e um unico caso fundador;
* os exemplos nao cobrem dominios juridico, clinico, financeiro ou de seguranca critica;
* a matriz nao prova ganho de qualidade decisoria;
* os testes de classificacao ainda nao foram aplicados por avaliadores independentes;
* algumas cardinalidades e transicoes permanecem propostas;
* classificacao documental nao revela mecanismo interno de agente;
* `Criterio de Avaliacao` permanece sem posicao definitiva.

## 12. Conclusao

A matriz distingue os seis conceitos obrigatorios por funcao, origem, derivacao, revisao e capacidade de afetar a cadeia. As ambiguidades conhecidas foram explicitadas e receberam teste ou tratamento conservador. As lacunas remanescentes permanecem abertas, sem substituicao por inferencias apresentadas como fatos.

**MATRIZ SEMANTICA FORMALIZADA — AMBIGUIDADES REMANESCENTES REGISTRADAS**

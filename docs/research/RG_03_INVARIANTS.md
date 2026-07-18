# GP-RG-03 — Invariantes Arquiteturais GDC-R

## 1. Objetivo

Estabelecer condicoes que devem permanecer verdadeiras em todo snapshot declarado conforme com a arquitetura GDC-R. Os invariantes sao requisitos documentais da pesquisa; nao constituem validacao empirica nem regra de arquitetura de software.

## 2. Notacao

* `C`: instancia de cadeia;
* `M(C)`: Manifesto de C;
* `N(C)`: nos conceituais de C;
* `A(C)`: arestas de C;
* `R(C)`: registros de revisao de C;
* `S(C)`: estado verificavel de C;
* `tipo(n)`: tipo de no em `{P,E,I,F,D,V}`;
* `ativa(a)`: aresta vigente no snapshot;
* `origem(a)` e `destino(a)`: extremos direcionados;
* `alcanca(x,y)`: existe caminho direcionado ativo de x ate y;
* `versao_anterior(n)`: predecessor historico, quando houver.

Expressoes formais sao especificacoes documentais abstratas, nao sintaxe executavel.

## 3. Severidades

| Severidade | Efeito |
|---|---|
| BLOQUEANTE | violacao torna a cadeia `NAO_CONFORME` |
| ALTA | impede declarar `CONFORME`; exige correcao ou classificacao inferior |
| MEDIA | exige ressalva explicita e plano de tratamento |

Nenhuma severidade autoriza ocultar a violacao.

## 4. Invariantes De Identidade E Escopo

### INV-01 — Manifesto Unico E Existente

Para toda cadeia `C`, existe exatamente um Manifesto vigente `M(C)`.

Teste: verificar unicidade de `chain_id` e existencia do Manifesto.

Severidade: **BLOQUEANTE**.

### INV-02 — Pertencimento Declarado

Todo no, aresta e revisao pertence a exatamente uma cadeia primaria identificada. Compartilhamento entre cadeias ocorre por referencia, nao por perda de proveniencia.

Teste: cada elemento resolve para um `chain_id`; referencias externas identificam cadeia de origem.

Severidade: **BLOQUEANTE**.

### INV-03 — Identificador Imutavel

Nenhum `node_id`, `edge_id` ou `revision_id` pode ser reutilizado para conteudo semanticamente distinto.

Teste: comparar historico de versoes e unicidade.

Severidade: **BLOQUEANTE**.

### INV-04 — Tipo Primario Unico

Para todo `n ∈ N(C)`, `tipo(n)` possui exatamente um valor em `{P,E,I,F,D,V}`.

Teste: rejeitar no sem tipo, com tipo multiplo ou com tipo experimental.

Severidade: **BLOQUEANTE**.

### INV-05 — Neutralidade De Dominio

Conformidade estrutural nao pode depender de entidade, formato, ferramenta, organizacao, projeto ou tipo de agente especifico.

Teste: remover vocabulario da instancia; regras e tipos GDC-R devem continuar interpretaveis.

Severidade: **BLOQUEANTE**.

Fundamentacao: DGA-01. Extensoes de dominio podem adicionar metadados, nunca redefinir o nucleo ou enfraquecer invariantes.

## 5. Invariantes De Sustentacao

### INV-06 — Evidencia Com Proveniencia

Toda Evidencia possui fonte, metodo, alcance e limitacoes declarados.

Formalizacao: `∀e, tipo(e)=E ⇒ fonte(e) ∧ metodo(e) ∧ alcance(e) ∧ limitacoes(e)`.

Severidade: **BLOQUEANTE**.

### INV-07 — Inferencia Sustentada

Toda Inferencia admissivel recebe pelo menos uma aresta ativa `SUPORTA` originada em Evidencia.

Formalizacao: `∀i, tipo(i)=I ⇒ ∃e: tipo(e)=E ∧ E→I(SUPORTA)`.

Severidade: **BLOQUEANTE**.

### INV-08 — Fundamentacao Relacional

Toda Fundamentacao possui ao menos uma Evidencia por `COMPOE_FUNDAMENTACAO` e explicita as demais relacoes aplicaveis.

Formalizacao minima: `∀f, tipo(f)=F ⇒ ∃e: tipo(e)=E ∧ E→F`.

Severidade: **BLOQUEANTE**.

### INV-09 — Decisao Nao Isolada

Toda Decisao recebe pelo menos uma aresta ativa `FUNDAMENTA` originada em Fundamentacao.

Formalizacao: `∀d, tipo(d)=D ⇒ ∃f: tipo(f)=F ∧ F→D(FUNDAMENTA)`.

Severidade: **BLOQUEANTE**.

### INV-10 — Validacao Com Objeto

Toda Validacao referencia ao menos uma Decisao por `SUBMETE_A_VALIDACAO`.

Formalizacao: `∀v, tipo(v)=V ⇒ ∃d: tipo(d)=D ∧ D→V`.

Severidade: **BLOQUEANTE**.

### INV-11 — Validacao Concluida Com Resultado Observavel

Toda Validacao concluida produz ou referencia ao menos uma Evidencia de resultado por `PRODUZ_OBSERVACAO`.

Formalizacao: `concluida(v) ⇒ ∃e: V→E`.

Severidade: **BLOQUEANTE**.

### INV-12 — Nenhum Elo Automatico

Existencia de um no nao implica criacao ou validade do seguinte. Toda passagem exige aresta, justificativa e autoridade aplicavel.

Teste: procurar dependencias presumidas sem aresta.

Severidade: **ALTA**.

## 6. Invariantes Contra Circularidade

### INV-13 — Ausencia De Ciclo De Sustentacao No Snapshot

O subgrafo formado por AR-01 a AR-08 em um mesmo snapshot deve ser aciclico.

Formalizacao: nao existe sequencia ativa `n1→n2→...→n1` composta somente por relacoes de sustentacao/composicao.

Severidade: **BLOQUEANTE**.

### INV-14 — Decisao Nao Prova A Si Mesma

Nenhuma Decisao pode ser Evidencia, Inferencia ou Fundamentacao exclusiva de sua propria correcao.

Teste: rastrear caminhos de D para seus antecedentes; rejeitar caminho circular sem fonte independente.

Severidade: **BLOQUEANTE**.

### INV-15 — Revisao E O Unico Retorno Controlado

Retroalimentacao somente ocorre entre snapshots por AR-11 a AR-15 e Registro de Revisao.

Teste: toda aresta de retorno resolve para predecessor, sucessor e R identificados.

Severidade: **BLOQUEANTE**.

## 7. Invariantes De Revisao E Versionamento

### INV-16 — Historico Preservado

Toda revisao mantem predecessor acessivel e registra motivo, estado anterior, sucessor ou pendencia.

Formalizacao: `versao_anterior(n')=n ⇒ n permanece acessivel ∧ ∃r`.

Severidade: **BLOQUEANTE**.

### INV-17 — Sem Sobrescrita Silenciosa

Mudanca material de conteudo, estado ou relacao gera nova versao ou transicao registrada.

Teste: comparar snapshots e exigir R para diferencas materiais.

Severidade: **BLOQUEANTE**.

### INV-18 — Propagacao De Impacto Declarada

Revisao identifica dependentes alcancaveis e classifica seu impacto como `SEM_IMPACTO`, `REAVALIAR`, `INVALIDAR_ESTADO` ou `INCONCLUSIVO`.

Teste: percorrer arestas ativas a partir do elemento afetado e comparar com R.

Severidade: **ALTA**.

### INV-19 — Invalidacao Nao E Eliminacao

Invalidar altera estado vigente; nunca apaga registro, evidencia contraria ou decisao anterior.

Severidade: **BLOQUEANTE**.

### INV-20 — Resultado Negativo Preservado

Validacao rejeitada ou inconclusiva integra permanentemente o historico e pode iniciar revisao.

Severidade: **BLOQUEANTE**.

## 8. Invariantes De Estado E Consistencia

### INV-21 — Estado Verificavel Obrigatorio

Todo snapshot declara exatamente um `S(C)` pertencente ao catalogo oficial.

Teste: estado presente, unico e compativel com os nos.

Severidade: **BLOQUEANTE**.

Uma cadeia pode terminar em rejeicao, inconclusao, pendencia justificada ou nao conformidade; “verificavel” nao significa “aprovada”.

### INV-22 — Estado Coerente Com Estrutura

O Manifesto nao pode declarar `VALIDADA_APROVADA` sem V concluida e Evidencia de resultado, nem `CONFORME` com violacao bloqueante.

Severidade: **BLOQUEANTE**.

### INV-23 — Conflito Nao Oculto

Estados ou registros materialmente conflitantes devem estar ligados por `DECLARA_CONFLITO` ou explicados em Fundamentacao/Revisao.

Severidade: **ALTA**.

### INV-24 — Lacuna Explicita

Campo ou elo obrigatorio ausente deve produzir estado `INCOMPLETA` ou `NAO_CONFORME`, conforme severidade; nunca pode ser presumido.

Severidade: **ALTA**, podendo tornar-se bloqueante conforme o elo ausente.

### INV-25 — Informacao Contraria Preservada

Evidencia, Inferencia, Fundamentacao ou Validacao contraria relevante nao pode ser omitida para melhorar aparencia de consistencia.

Severidade: **BLOQUEANTE**.

## 9. Invariantes De Propriedades Arquiteturais

### INV-26 — Caminho De Rastreabilidade Da Decisao

Para toda D governada, deve existir caminho reversamente consultavel ate F e pelo menos uma E; quando P/I forem usados, seus caminhos tambem devem resolver.

Teste minimo: `D←F←E` e, conforme instancia, `F←I←E` e `F/I←P`.

Severidade: **BLOQUEANTE**.

### INV-27 — Caminho De Auditabilidade Posterior

Para toda D executada, deve existir D→V ou estado justificado `AGUARDANDO_VALIDACAO`; V concluida deve conduzir a E de resultado.

Severidade: **ALTA** antes da execucao; **BLOQUEANTE** para V declarada concluida.

### INV-28 — Completude Relativa Ao Perfil

Uma cadeia somente pode declarar-se completa se atender todos os requisitos do PMG ou PCP previamente declarado.

Severidade: **ALTA**.

### INV-29 — Proveniencia Em Compartilhamento

Evidencia ou outro registro reutilizado entre cadeias conserva fonte, cadeia primaria, escopo, versao e limitacoes.

Severidade: **ALTA**.

### INV-30 — Explicabilidade Estritamente Documental

A explicacao deve ser reconstruivel por registros e relacoes sem alegar acesso a estados internos, intencoes nao declaradas ou mecanismos cognitivos.

Severidade: **BLOQUEANTE**.

## 10. Invariante Do Conceito Experimental

### INV-31 — Nao Promocao Do Criterio De Avaliacao

`Criterio de Avaliacao` nao pode ser contado como no conceitual oficial, requisito de completude epistemica ou hipotese validada.

Pode existir apenas como anotacao experimental versionada, com origem e momento de definicao.

Severidade: **BLOQUEANTE**.

## 11. Matriz Resumida De Verificacao

| Grupo | Invariantes | Verificacao principal |
|---|---|---|
| identidade e escopo | INV-01 a INV-05 | unicidade, pertencimento, tipagem e neutralidade |
| sustentacao | INV-06 a INV-12 | proveniencia e cardinalidades minimas |
| circularidade | INV-13 a INV-15 | deteccao de ciclos e retornos nao controlados |
| revisao | INV-16 a INV-20 | predecessor, sucessor, impacto e preservacao |
| estado e consistencia | INV-21 a INV-25 | coerencia, conflitos, lacunas e informacao contraria |
| propriedades | INV-26 a INV-30 | caminhos, perfil, compartilhamento e explicabilidade |
| conceito experimental | INV-31 | ausencia do criterio no nucleo oficial |

## 12. Procedimento De Auditoria Dos Invariantes

1. identificar Manifesto, perfil e snapshot;
2. inventariar nos, arestas e revisoes;
3. verificar IDs, tipos e pertencimento;
4. resolver todas as referencias;
5. verificar cardinalidades minimas;
6. detectar ciclos de sustentacao;
7. reconstruir caminhos de cada Decisao;
8. verificar resultados e estados de cada Validacao;
9. comparar versoes e Registros de Revisao;
10. localizar conflitos, lacunas e informacao contraria;
11. verificar neutralidade do nucleo e separacao de extensoes;
12. classificar violacoes por severidade;
13. atribuir classe de conformidade;
14. registrar limitacoes da propria auditoria.

Esse procedimento e uma especificacao para futura operacionalizacao, nao protocolo experimental concluido.

## 13. Excecoes

Nao existem excecoes silenciosas a invariantes bloqueantes. Quando uma situacao de dominio exigir desvio:

* registrar a necessidade;
* classificar a cadeia como `NAO_CONFORME` ou `INCOMPLETA` enquanto o conflito existir;
* preservar os dados disponiveis;
* propor extensao sem alterar retrospectivamente o nucleo;
* submeter a revisao formal da arquitetura.

Uma extensao nao pode redefinir evidencia como inferencia, remover proveniencia, apagar historico ou integrar `Criterio de Avaliacao` sem a governanca futura exigida.

## 14. Limitacoes

* invariantes foram verificados apenas quanto a coerencia documental interna;
* nenhum verificador independente os aplicou;
* severidades nao foram calibradas empiricamente;
* neutralidade foi avaliada por abstracao, nao por experimentos nos dominios listados em DGA-01;
* completude e reprodutibilidade reais permanecem nao demonstradas;
* regras podem exigir revisao apos GP-RG-04/05.

## 15. Estado Final

**31 INVARIANTES ARQUITETURAIS FORMALIZADOS — VALIDACAO EMPIRICA PENDENTE**

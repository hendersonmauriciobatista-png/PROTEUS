# GP-D10A - Auditoria Das Instancias Do Dominio Projeto

## Objetivo

Definir, exclusivamente por auditoria de dominio, quais tipos de Projetos o PROTEUS deve reconhecer como instancias validas do Dominio Projeto.

Esta auditoria inaugura a fase de uso do dominio consolidado por diferentes contextos operacionais. Nao implementa codigo, nao altera arquitetura, nao altera persistencia, nao altera interface, nao altera o Dossie Final e nao altera o Dominio Projeto.

## Escopo

O escopo esta restrito a classificacao das instancias que podem utilizar o Dominio Projeto ja consolidado.

Foram avaliadas as categorias:

* Urbano;
* Rural;
* Industrial;
* ETA;
* ETE;
* Rio;
* Lago;
* Nascente;
* Poco Artesiano;
* Reservatorio.

Ficaram fora do escopo:

* criacao de novos atributos;
* criacao de entidades;
* criacao de colecoes;
* criacao de camadas;
* criacao de perfis operacionais;
* alteracao de `PolicyEngine`;
* alteracao do Motor Observacional;
* alteracao de Analytics, Governanca Operacional, Painel Executivo ou interface;
* implementacao de multiplos Projetos;
* alteracao do Dossie Final.

## Definicao De Instancia Do Dominio Projeto

Uma instancia do Dominio Projeto e uma aplicacao concreta do agregado Projeto a um contexto operacional ou ponto principal de monitoramento.

Ela nao cria um novo dominio. Ela usa a mesma estrutura consolidada:

* identificacao;
* cliente;
* contexto operacional;
* perfil operacional;
* ponto principal de coleta;
* responsavel;
* estado;
* ciclo de vida;
* encerramento;
* arquivamento;
* Dossie Final;
* memoria permanente.

A instancia responde: "qual tipo de monitoramento este Projeto representa?". O Dominio Projeto continua respondendo: "como um Projeto existe, evolui, encerra, arquiva e preserva memoria?".

## Classificacao Das Possiveis Instancias

As categorias avaliadas se dividem em dois grupos principais.

### Contextos Operacionais

| Categoria | Natureza | Papel no Dominio Projeto | Exige comportamento proprio? |
| --- | --- | --- | --- |
| Urbano | Contexto operacional | Classifica ambiente de saneamento, abastecimento, rede, consumo ou reservacao urbana | Nao |
| Rural | Contexto operacional | Classifica captacoes locais, propriedades rurais, pocos, nascentes e usos agropecuarios gerais | Nao |
| Industrial | Contexto operacional | Classifica uso industrial, processo, efluente ou ponto de controle produtivo | Nao |

### Tipos De Ponto Ou Ambiente Monitorado

| Categoria | Natureza | Papel no Dominio Projeto | Exige comportamento proprio? |
| --- | --- | --- | --- |
| ETA | Tipo de instalacao/ponto | Indica estacao de tratamento de agua como ponto principal ou perfil operacional futuro | Nao agora |
| ETE | Tipo de instalacao/ponto | Indica estacao de tratamento de esgoto/efluente como ponto principal ou perfil operacional futuro | Nao agora |
| Rio | Corpo hidrico | Indica ponto ambiental de agua superficial | Nao |
| Lago | Corpo hidrico | Indica ambiente lentico de agua superficial | Nao |
| Nascente | Fonte natural | Indica origem ou surgencia de agua | Nao |
| Poco Artesiano | Fonte subterranea | Indica captacao subterranea | Nao |
| Reservatorio | Estrutura/corpo armazenado | Indica armazenamento de agua, rural, urbano ou industrial | Nao |

## Analise Comparativa Entre Categorias

| Categoria | Usa mesmo ciclo de vida? | Usa mesmo Dossie Final? | Exige atributos obrigatorios especificos? | Diferenca principal |
| --- | --- | --- | --- | --- |
| Urbano | Sim | Sim | Nao | Riscos e politicas operacionais associadas a saneamento e abastecimento. |
| Rural | Sim | Sim | Nao | Riscos ligados a captacoes locais, sazonalidade e uso agropecuario. |
| Industrial | Sim | Sim | Nao | Riscos ligados a processo, efluentes e contaminantes industriais. |
| ETA | Sim | Sim | Nao | Ponto de instalacao com possivel perfil operacional proprio em camadas existentes. |
| ETE | Sim | Sim | Nao | Ponto de efluente/esgoto com diferencas observacionais fora do Projeto. |
| Rio | Sim | Sim | Nao | Corpo hidrico superficial; diferenca esta em parametros e politicas. |
| Lago | Sim | Sim | Nao | Corpo hidrico lentico; diferenca esta em parametros e interpretacao operacional. |
| Nascente | Sim | Sim | Nao | Fonte natural; pode influenciar coleta e riscos, nao o dominio. |
| Poco Artesiano | Sim | Sim | Nao | Fonte subterranea; pode influenciar parametros, nao ciclo de vida. |
| Reservatorio | Sim | Sim | Nao | Ambiente armazenado; contexto operacional define interpretacao. |

Conclusao comparativa:

Todas as categorias podem utilizar exatamente o mesmo Dominio Projeto. As diferencas sao operacionais, observacionais ou de configuracao, nao estruturais.

## Reutilizacao Do Dominio Projeto

O Dominio Projeto saturado e suficientemente generico para suportar multiplas instancias porque abstrai:

* identidade;
* cliente;
* contexto;
* ponto principal;
* responsavel;
* ciclo de vida;
* memoria permanente.

Esses elementos sao comuns a todas as categorias avaliadas.

Nenhuma categoria altera:

* o que e um Projeto;
* como um Projeto nasce;
* como um Projeto encerra;
* como um Projeto arquiva;
* como o Dossie Final preserva memoria;
* como PA-01 separa contexto, selecao de politica e avaliacao observacional.

## Diferencas Operacionais

As diferencas entre instancias aparecem em:

* parametros monitorados;
* frequencia de coleta;
* riscos priorizados;
* perfil operacional aplicavel;
* politica selecionada pelo `PolicyEngine`;
* interpretacao tecnica produzida pelo Motor Observacional;
* alertas e recomendacoes derivados;
* linguagem operacional do Dossie Final.

Essas diferencas pertencem a camadas ou configuracoes ja existentes, nao ao Dominio Projeto.

## Necessidade De Especializacoes

Nao ha necessidade objetiva de especializar o Dominio Projeto.

Tratamento recomendado:

| Categoria | Especializacao de dominio? | Tratamento recomendado |
| --- | --- | --- |
| Urbano | Nao | Contexto operacional. |
| Rural | Nao | Contexto operacional. |
| Industrial | Nao | Contexto operacional. |
| ETA | Nao | Tipo de ponto ou perfil operacional em camadas existentes, sem novo dominio. |
| ETE | Nao | Tipo de ponto ou perfil operacional futuro, se auditado, sem novo dominio. |
| Rio | Nao | Tipo de ponto/corpo hidrico. |
| Lago | Nao | Tipo de ponto/corpo hidrico. |
| Nascente | Nao | Tipo de ponto/fonte natural. |
| Poco Artesiano | Nao | Tipo de ponto/fonte subterranea. |
| Reservatorio | Nao | Tipo de ponto/estrutura de armazenamento. |

Se futuramente alguma categoria exigir comportamento proprio, a primeira avaliacao deve ocorrer nas camadas de configuracao, catalogo, politicas ou parametros, nao no agregado Projeto.

## Categorias Importantes Nao Consideradas

Categorias candidatas futuras, sem recomendacao de implementacao nesta GP:

* manancial;
* bacia hidrografica;
* rede de distribuicao;
* ponto de consumo;
* drenagem pluvial;
* irrigacao;
* efluente industrial;
* balneabilidade;
* agua subterranea nao artesiana;
* area de preservacao.

Essas categorias podem agregar valor operacional, mas nao alteram o veredito: seriam classificacoes ou especializacoes operacionais, nao novos dominios de Projeto.

## Relacao Com O Restante Do PROTEUS

As instancias do Projeto se relacionam com o restante do PROTEUS da seguinte forma:

```text
Instancia do Projeto
  -> contexto operacional
  -> perfil operacional
  -> PolicyEngine seleciona politica
  -> Motor Observacional executa avaliacao
  -> Analytics consolida sinais
  -> Governanca acompanha ocorrencias
  -> Recommendation emite recomendacoes
  -> Dossie Final preserva memoria
```

O Projeto fornece contexto e memoria. Ele nao assume responsabilidade de politica, avaliacao, analise, governanca operacional ou recomendacao.

## Impacto Arquitetural

Nao ha impacto arquitetural.

Nao ha necessidade de:

* nova camada;
* novo agregado;
* nova entidade;
* colecao de instancias;
* repositorio de tipos de Projeto;
* servico dedicado;
* alteracao de persistencia;
* alteracao de interface.

As categorias avaliadas sao classificacoes de uso do dominio existente.

## Impacto De Dominio

O impacto de dominio e classificatorio.

A GP-D10A confirma que o Dominio Projeto saturado pode ser reutilizado por diferentes instancias operacionais sem expansao estrutural.

O dominio permanece em fase de consolidacao. A nova fase passa a auditar usos, contextos e instancias, nao a expandir o agregado Projeto.

## Analise PA-01

PA-01 permanece integralmente preservado.

As instancias do Projeto nao selecionam politica, nao executam avaliacao observacional, nao interpretam parametros, nao calculam score, nao resolvem alertas e nao decidem severidade.

Categorias como Urbano, Rural, Industrial, ETA, ETE, Rio, Lago, Nascente, Poco Artesiano e Reservatorio podem influenciar o perfil operacional ou a configuracao usada por outras camadas, mas a autoridade observacional permanece no fluxo correto:

* `PolicyEngine` seleciona politica;
* Motor Observacional executa avaliacao;
* Analytics, Governanca e Recommendation consomem sinais conforme suas responsabilidades.

## Analise Das Discoveries

`docs/research/DISCOVERY_CATALOG.md` foi consultado.

Resultado:

* PA-02 foi reforcada: a auditoria mostra que novas instancias agregam valor por reutilizacao e classificacao do dominio consolidado, sem criar nova camada.
* PA-03 foi reforcada: nenhuma categoria exige materializacao estrutural propria antes de necessidade objetiva.
* Nenhuma Discovery foi contradita.
* Nenhuma Discovery foi promovida automaticamente.
* Nenhuma nova Discovery candidata foi identificada.

## Observacoes da IA / Hipoteses Metodologicas

As observacoes abaixo nao alteram o ICFACTORY, nao alteram o dominio e nao ampliam o escopo da GP-D10A.

| Padrao observado | Evidencia usada | Possivel impacto | Recomendacao | Status sugerido |
| --- | --- | --- | --- | --- |
| A fase pos-saturacao desloca a evolucao de estrutura para uso do dominio. | GP-D09A declarou o agregado Projeto saturado; GP-D10A audita instancias sem alterar o agregado. | Pode ajudar a separar "expandir dominio" de "classificar instancias". | Monitorar se outras frentes tambem podem entrar em fase de instancias apos saturacao. | Hipotese em monitoramento |
| Categorias operacionais podem parecer novos dominios, mas muitas sao apenas classificacoes de contexto ou ponto. | Urbano, Rural e Industrial sao contextos; ETA, ETE, Rio, Lago, Nascente, Poco e Reservatorio sao tipos de ponto/ambiente. | Reduz risco de criar subclasses ou entidades desnecessarias. | Exigir prova de comportamento proprio antes de especializar dominio. | Observacao simples |
| O mesmo Dossie Final parece suficiente para instancias distintas quando a memoria permanente e abstrata. | GP-D09A consolidou Dossie Final como memoria; GP-D10A nao encontrou categoria que exija Dossie proprio. | Reforca reuso do Dossie e evita variantes documentais prematuras. | Manter variacoes de linguagem como conteudo textual, nao estrutura nova. | Observacao simples |

Nenhuma hipotese metodologica foi promovida a regra ICFACTORY ou Discovery oficial.

## Respostas Obrigatorias

### 1. O que caracteriza uma instancia do Dominio Projeto?

Uma instancia e a aplicacao concreta do Dominio Projeto a um contexto operacional ou ponto principal de monitoramento, sem criar novo dominio.

### 2. Quais tipos de Projeto o PROTEUS deve reconhecer?

Deve reconhecer instancias urbanas, rurais, industriais, ETA, ETE, rio, lago, nascente, poco artesiano e reservatorio como classificacoes validas de uso.

### 3. As categorias representam apenas classificacoes ou exigem comportamentos proprios?

Representam classificacoes. Podem influenciar operacao, perfil, parametros ou politica em outras camadas, mas nao exigem comportamento proprio no Dominio Projeto.

### 4. Todas essas categorias podem utilizar exatamente o mesmo Dominio Projeto?

Sim. Todas podem usar o mesmo Dominio Projeto.

### 5. Alguma delas exige um dominio proprio?

Nao. Nenhuma categoria exige dominio proprio.

### 6. Existem atributos obrigatorios especificos para alguma categoria?

Nao no Dominio Projeto. Atributos especificos, se surgirem, pertencem a operacao, configuracao, catalogo, politica, amostra ou medicao.

### 7. O ciclo de vida permanece o mesmo?

Sim. O ciclo `ativo` -> `encerrado` -> `arquivado` permanece o mesmo.

### 8. O Dossie Final permanece o mesmo?

Sim. O Dossie Final permanece o mesmo; variacoes por categoria devem ser conteudo textual ou consolidado, nao estrutura nova.

### 9. Existem diferencas apenas operacionais?

Sim. As diferencas estao em parametros, riscos, frequencia, perfil, politicas e interpretacao observacional.

### 10. Existe alguma categoria importante nao considerada?

Sim, como manancial, bacia hidrografica, rede de distribuicao, ponto de consumo, drenagem pluvial, irrigacao, efluente industrial, balneabilidade, agua subterranea nao artesiana e area de preservacao. Nenhuma exige expansao do Dominio Projeto agora.

### 11. Ha necessidade objetiva de alterar o Dominio Projeto?

Nao. O Dominio Projeto e suficientemente generico para suportar as instancias avaliadas.

### 12. Como essas instancias se relacionam com o restante do PROTEUS?

Elas fornecem contexto para perfil operacional e para o fluxo de politicas, avaliacao, analytics, governanca, recomendacao e memoria final, preservando PA-01.

## Veredito Final

As categorias avaliadas representam instancias validas do Dominio Projeto, nao novos dominios.

O PROTEUS deve reconhecer Urbano, Rural, Industrial, ETA, ETE, Rio, Lago, Nascente, Poco Artesiano e Reservatorio como classificacoes operacionais ou tipos de ponto/ambiente capazes de reutilizar o mesmo Dominio Projeto.

Nao ha necessidade objetiva de alterar o Dominio Projeto, criar especializacoes, entidades, colecoes, camadas, persistencia, interface ou Dossie Final.

## Declaracao ICFACTORY E IA

* A execucao permaneceu sob governanca ICFACTORY.
* Nao houve extrapolacao da IA na auditoria principal.
* Foram registradas observacoes metodologicas separadas, sem efeito normativo.
* O Dominio Projeto mostrou-se suficientemente generico para suportar multiplas instancias.

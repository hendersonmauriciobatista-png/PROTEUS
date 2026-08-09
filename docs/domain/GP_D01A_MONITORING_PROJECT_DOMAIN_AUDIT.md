# GP-D01A - Auditoria do Modelo de Projeto de Monitoramento

Data: 30/06/2026

Status: AUDITORIA DOCUMENTAL CONCLUIDA

Natureza: Dominio

## Contexto

O Sistema de Analise de Agua segue a metodologia ICFACTORY e possui arquitetura consolidada pela GP-A23.

Estado considerado nesta auditoria:

* Arquitetura global consolidada em GP-A23.
* Nucleo de Monitoramento Hidrico consolidado como autoridade observacional central.
* PA-01 vigente: separacao entre selecao de politicas e execucao por motores especializados.
* GP-A25 concluiu o grafico executivo do Water Health Score no Dashboard.
* Proxima fase definida como evolucao do dominio, sem criacao de novas camadas arquiteturais.

## Objetivo

Auditar e definir o modelo minimo de dominio para Projeto de Monitoramento Hidrico antes de qualquer implementacao funcional.

Esta auditoria nao implementa entidades, telas, CSVs, runtime, Policy Engine, Motor Observacional, Analytics, Governanca, Recommendation ou nova camada arquitetural.

## Pergunta Central

O que e indispensavel para representar corretamente um Projeto de Monitoramento Hidrico?

## Metodo

A auditoria foi passiva e documental.

Foram avaliados:

* `docs/governance/PROJECT_CONSTITUTION.md`;
* `docs/architecture/CASE01_GLOBAL_ARCHITECTURE_AUDIT.md`;
* `docs/architecture/INTEGRATION_AUDIT_REPORT.md`;
* `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md`;
* `docs/research/GP_R03_EXECUTIVE_CONTEXT_AUDIT.md`;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`;
* modelos do pacote `monitoramento_hidrico`;
* catalogo, configuracoes e politicas do Nucleo de Monitoramento Hidrico.

Perguntas aplicadas:

1. O conceito e necessario para identificar o escopo do monitoramento?
2. O conceito ajuda o `PolicyEngine` a selecionar politica sem alterar PA-01?
3. O conceito melhora rastreabilidade operacional sem criar cadeia burocratica?
4. O conceito pertence ao Projeto, Amostra, Medicao ou Contexto Operacional?
5. O conceito agrega valor objetivo agora?
6. O conceito pode ser adiado sem perda arquitetural relevante?

## Criterio Institucional

Filtro aplicado:

`Agrega valor ao projeto?`

Nesta auditoria, agregar valor significa reduzir ambiguidade operacional, permitir selecao correta de politica observacional, melhorar rastreabilidade minima, preservar explicabilidade, evitar autoridade paralela e evitar complexidade prematura.

Conceitos que agregam valor apenas em cenarios futuros, regulatorios, laboratoriais, multiusuario ou multicoleta foram classificados como adiados.

## Conceitos Candidatos

Conceitos candidatos principais:

* Projeto.
* Cliente.
* Area Operacional.
* Ponto Principal de Coleta.
* Coletor Responsavel.

Tipos candidatos de area operacional:

* Urbana.
* Rural.
* Industrial.
* Agricola.

Tipos candidatos de ponto principal:

* rio;
* poco;
* reservatorio;
* ETA;
* lago;
* outro.

Conceitos avaliados sem promocao automatica:

* coordenadas GPS;
* fotos;
* assinatura digital;
* cadeia completa de custodia;
* numero de lacre;
* anexos;
* multiplos pontos de coleta;
* multiplos coletores.

## Respostas De Dominio

### 1. O que e um Projeto de Monitoramento?

Um Projeto de Monitoramento e o envelope operacional que define por que, para quem, onde e sob qual contexto uma sequencia de amostras e medicoes hidricas sera observada.

Ele nao e motor observacional, nao e politica, nao e configuracao analitica e nao e governanca. Seu papel minimo e contextualizar a coleta para que medicoes futuras possam ser interpretadas com menos ambiguidade.

### 2. O que pertence ao Projeto?

Pertence ao Projeto aquilo que permanece estavel ou quase estavel durante a execucao do monitoramento:

* identificacao do projeto;
* cliente ou responsavel institucional;
* area operacional;
* ponto principal de coleta;
* coletor responsavel principal;
* vinculo conceitual com perfil operacional usado pela configuracao e pelo `PolicyEngine`.

O Projeto nao deve armazenar valores de parametros hidricos, status observacionais, alertas, score, eventos de governanca ou recomendacoes.

### 3. O que pertence a Amostra?

Pertence a Amostra aquilo que representa uma ocorrencia concreta de coleta:

* data e horario da coleta;
* referencia ao Projeto;
* identificacao simples da amostra, quando necessaria;
* ponto usado na coleta, inicialmente herdado do ponto principal do Projeto;
* coletor efetivo, inicialmente herdado do coletor responsavel do Projeto.

No MVP de dominio, Amostra pode ser definida conceitualmente sem implementacao imediata. A promocao funcional deve ocorrer apenas quando houver necessidade objetiva de separar varias ocorrencias de coleta dentro de um mesmo Projeto.

### 4. O que pertence a Medicao?

Pertence a Medicao aquilo que representa o valor observado de um parametro:

* parametro hidrico;
* valor medido;
* unidade, quando aplicavel;
* data/hora de registro ou vinculo com a amostra;
* resultado observacional produzido pelo Nucleo, quando avaliado.

Medicao nao deve escolher politica, nem executar avaliacao, nem decidir severidade localmente. Pela PA-01, politica pertence ao `PolicyEngine` e avaliacao pertence ao motor especializado.

### 5. O que pertence ao Contexto Operacional?

Pertence ao Contexto Operacional a classificacao que altera a interpretacao do monitoramento sem ser uma medicao:

* area operacional;
* perfil operacional equivalente ou derivado;
* tipo de ponto principal;
* configuracao operacional aplicavel;
* observacoes operacionais simples.

O Contexto Operacional deve ser representado dentro das estruturas existentes do dominio hidrico, principalmente por perfil/configuracao operacional, sem criar uma nova camada.

### 6. Como o tipo de area operacional deve influenciar a selecao de politicas pelo Policy Engine?

A area operacional deve influenciar o `PolicyEngine` por traducao controlada para `perfil_operacional`.

Mapeamento recomendado para o MVP:

| Area operacional | Perfil operacional recomendado | Observacao |
| ---------------- | ------------------------------ | ---------- |
| Urbana | `urbano_saneamento` | Aderente ao catalogo existente. |
| Rural | `rural` | Aderente ao catalogo existente. |
| Industrial | `industrial` | Ja possui politica especifica. |
| Agricola | `rural` | Deve iniciar como especializacao operacional de Rural, sem criar perfil novo agora. |

O tipo de ponto principal pode refinar a escolha quando houver correspondencia clara:

| Ponto principal | Perfil sugerido quando aplicavel |
| --------------- | -------------------------------- |
| ETA | `eta` |
| rio | `ambiental_rio` |
| poco | `rural` ou `urbano_saneamento`, conforme area operacional |
| reservatorio | area operacional define o perfil |
| lago | `ambiental_rio` como aproximacao observacional inicial |
| outro | area operacional define o perfil |

Essa influencia deve permanecer como insumo de selecao, nao como execucao de avaliacao.

### 7. Como preservar o PA-01?

PA-01 e preservado se o Projeto apenas fornecer contexto para selecao.

Guardrails:

* Projeto nao executa avaliacao.
* Projeto nao interpreta parametro.
* Projeto nao calcula status.
* Projeto nao define severidade.
* Projeto nao acessa diretamente motores especializados.
* Projeto nao altera resultado observacional.
* `PolicyEngine` continua selecionando politica.
* `AvaliacaoObservacionalService` continua executando avaliacao.

### 8. Como manter a arquitetura sem novas camadas?

O modelo minimo deve ser tratado como enriquecimento do dominio existente, nao como camada.

Caminho recomendado:

* documentar o conceito antes da implementacao;
* quando implementado, encaixar o Projeto junto ao dominio operacional/hidrico existente;
* reutilizar `perfil_operacional`, `ConfiguracaoOperacional`, catalogo e `PolicyEngine`;
* evitar `ProjectService`, `ContextLayer`, `CustodyLayer` ou qualquer camada nova enquanto nao houver demanda objetiva.

### 9. Como melhorar rastreabilidade sem excesso de complexidade?

Rastreabilidade minima recomendada:

* nome ou codigo do Projeto;
* cliente;
* area operacional;
* ponto principal de coleta;
* coletor responsavel;
* perfil operacional derivado;
* data/hora das amostras futuras;
* parametro e valor das medicoes futuras.

Rastreabilidade adiada:

* coordenadas GPS;
* fotos;
* assinatura digital;
* cadeia completa de custodia;
* numero de lacre;
* anexos;
* multiplos pontos;
* multiplos coletores.

Esses itens podem ser valiosos em auditoria regulatoria, operacao multiusuario ou coleta laboratorial formal, mas adicionam custo de interface, persistencia, governanca e validacao que nao agrega valor objetivo ao MVP atual.

### 10. Quais conceitos devem entrar no MVP do dominio?

Devem entrar no MVP conceitual:

* Projeto.
* Cliente.
* Area Operacional.
* Ponto Principal de Coleta.
* Coletor Responsavel.
* Perfil operacional derivado ou selecionavel.

Nao devem entrar no MVP funcional agora:

* entidades implementadas;
* telas;
* CSVs;
* alteracoes em `PolicyEngine`;
* alteracoes no Motor Observacional;
* alteracoes em Analytics, Governanca, Recommendation ou Dashboard.

## Matriz De Valor Por Conceito

| Conceito | Agrega valor ao projeto? | Valor objetivo | Pertence a | Decisao |
| -------- | ------------------------ | -------------- | ---------- | ------- |
| Projeto | Sim | Define escopo, continuidade e rastreabilidade minima do monitoramento. | Projeto | Recomendar para MVP conceitual |
| Cliente | Sim | Identifica para quem o monitoramento existe e evita ambiguidade institucional. | Projeto | Recomendar para MVP conceitual |
| Area Operacional | Sim | Orienta perfil operacional e selecao de politicas. | Contexto Operacional | Recomendar para MVP conceitual |
| Urbana | Sim | Mapeia para `urbano_saneamento`. | Contexto Operacional | Recomendar |
| Rural | Sim | Mapeia para `rural`. | Contexto Operacional | Recomendar |
| Industrial | Sim | Mapeia para `industrial`, ja suportado em politicas. | Contexto Operacional | Recomendar |
| Agricola | Sim, com ressalva | Agrega valor pratico, mas deve iniciar como especializacao de Rural. | Contexto Operacional | Recomendar como area, nao como novo perfil agora |
| Ponto Principal de Coleta | Sim | Reduz ambiguidade espacial sem exigir multiplos pontos. | Projeto / Contexto Operacional | Recomendar para MVP conceitual |
| rio | Sim | Sugere contexto `ambiental_rio`. | Contexto Operacional | Recomendar |
| poco | Sim | Identifica fonte relevante, mas perfil depende da area. | Contexto Operacional | Recomendar |
| reservatorio | Sim | Identifica fonte relevante, mas perfil depende da area. | Contexto Operacional | Recomendar |
| ETA | Sim | Sugere perfil `eta`. | Contexto Operacional | Recomendar |
| lago | Sim, com ressalva | Fonte ambiental util, inicialmente aproximada de `ambiental_rio`. | Contexto Operacional | Recomendar |
| outro | Sim | Evita bloqueio operacional quando a fonte nao esta catalogada. | Contexto Operacional | Recomendar |
| Coletor Responsavel | Sim | Melhora rastreabilidade humana minima sem governanca pesada. | Projeto | Recomendar para MVP conceitual |
| Coordenadas GPS | Parcial | Melhoram localizacao, mas exigem validacao, UI e precisao operacional. | Amostra / Ponto | Adiar |
| Fotos | Parcial | Evidencia visual util, mas exige anexos e armazenamento. | Amostra / Anexo | Adiar |
| Assinatura digital | Nao agora | Valor regulatorio, alto custo de identidade e validade. | Governanca futura | Adiar |
| Cadeia completa de custodia | Nao agora | Valor laboratorial/regulatorio, complexidade alta. | Governanca futura | Adiar |
| Numero de lacre | Nao agora | Valor para custodia formal, depende de processo externo. | Amostra / Custodia | Adiar |
| Anexos | Parcial | Suporte documental util, mas cria gestao de arquivos. | Anexo futuro | Adiar |
| Multiplos pontos de coleta | Parcial | Valor real em operacoes maiores, mas amplia modelo e UI. | Projeto / Ponto | Adiar |
| Multiplos coletores | Parcial | Valor multiusuario, mas demanda papeis e auditoria. | Projeto / Amostra | Adiar |

## Modelo Minimo Recomendado

Modelo minimo recomendado, em nivel conceitual:

```text
Projeto de Monitoramento
  - identificacao
  - nome
  - cliente
  - area_operacional
  - ponto_principal_coleta
  - coletor_responsavel
  - perfil_operacional_derivado
  - observacoes opcionais
```

Separacao conceitual:

```text
Projeto
  define escopo e contexto estavel

Amostra
  representa uma ocorrencia de coleta

Medicao
  representa valor de parametro observado

Contexto Operacional
  orienta configuracao e selecao de politica
```

O MVP recomendado e documental/conceitual. A implementacao deve ser uma GP posterior, com novo aceite explicito.

## Conceitos Adiados

Adiar para pesquisa ou GP futura:

* Coordenadas GPS.
* Fotos.
* Assinatura digital.
* Cadeia completa de custodia.
* Numero de lacre.
* Anexos.
* Multiplos pontos de coleta.
* Multiplos coletores.

Motivo:

Esses conceitos agregam valor condicionado a maturidade operacional maior. Implementa-los agora criaria persistencia, interface, regras de validacao e possivel governanca documental antes de haver demanda comprovada.

## Relacao Com Policy Engine

O `PolicyEngine` atual seleciona politica por `perfil_operacional`, `categoria` e `parametro_id`.

Portanto, o Projeto de Monitoramento deve alimentar a selecao por meio de `perfil_operacional_derivado` ou selecionado, sem alterar o contrato atual.

Recomendacao:

* area operacional e ponto principal devem sugerir o perfil;
* o perfil deve continuar explicito e auditavel;
* o Projeto nao deve escolher motor;
* o Projeto nao deve executar avaliacao;
* qualquer avaliacao deve continuar passando pelo Nucleo de Monitoramento Hidrico.

## Preservacao Do PA-01

PA-01 permanece preservado porque o modelo recomendado:

* nao cria autoridade observacional paralela;
* nao move regras para Projeto, Amostra ou Medicao;
* nao altera `PolicyEngine`;
* nao altera `AvaliacaoObservacionalService`;
* nao altera Analytics, Governanca ou Recommendation;
* usa contexto apenas como entrada para selecao de politica.

## Impacto Sobre A Arquitetura

Impacto arquitetural esperado:

| Area | Impacto |
| ---- | ------- |
| Runtime | Nenhum nesta GP |
| Interface | Nenhum nesta GP |
| Policy Engine | Nenhum nesta GP |
| Motor Observacional | Nenhum nesta GP |
| Analytics | Nenhum nesta GP |
| Governanca | Nenhum nesta GP |
| Recommendation | Nenhum nesta GP |
| Camadas | Nenhuma camada nova |
| Documentos constitucionais | Nenhuma alteracao |

A recomendacao respeita GP-A23: evoluir dominio sem criar novas camadas arquiteturais.

## Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
| ----- | ------------- | ------- | --------- |
| Projeto virar camada de contexto informal | Media | Medio | Tratar Projeto como dominio operacional, nao camada. |
| Area operacional duplicar perfil operacional | Media | Medio | Manter mapeamento explicito para `perfil_operacional`. |
| Agricola virar perfil prematuro | Media | Baixo/Medio | Iniciar como area operacional mapeada para `rural`. |
| Ponto principal virar multiponto cedo demais | Media | Medio | MVP com um ponto principal; multipontos adiados. |
| Rastreabilidade virar custodia completa | Baixa/Media | Alto | Adiar lacre, assinatura, anexos e cadeia de custodia. |
| Projeto decidir status observacional | Baixa | Alto | Guardrail PA-01: Projeto fornece contexto, Nucleo decide avaliacao. |
| Implementacao antes da maturidade conceitual | Media | Medio | Usar este relatorio como contrato antes de criar entidades. |

## Recomendacao Final

Recomenda-se adotar o modelo minimo conceitual de Projeto de Monitoramento composto por:

* Projeto;
* Cliente;
* Area Operacional;
* Ponto Principal de Coleta;
* Coletor Responsavel;
* Perfil operacional derivado ou selecionavel.

Esse conjunto agrega valor objetivo porque identifica o escopo do monitoramento, melhora rastreabilidade minima e fornece contexto suficiente para futura selecao de politicas sem violar PA-01.

Nao se recomenda implementar, nesta etapa, coordenadas GPS, fotos, assinatura digital, cadeia completa de custodia, numero de lacre, anexos, multiplos pontos de coleta ou multiplos coletores.

## Veredito

Modelo minimo suportado e recomendado.

Justificativa:

* O dominio atual ja possui catalogo, configuracoes e politicas por perfil operacional.
* A arquitetura consolidada pela GP-A23 suporta enriquecimento de dominio sem nova camada.
* O modelo minimo proposto agrega valor objetivo ao projeto.
* PA-01 permanece preservado.
* O modelo evita rastreabilidade excessiva e adia conceitos de alta complexidade.

## Proximos Passos Sugeridos

1. Criar uma GP-D01B para especificar contrato textual dos campos do Projeto, ainda sem implementacao.
2. Validar o mapeamento `area_operacional` -> `perfil_operacional` com exemplos reais de uso.
3. Definir nomenclatura canonica para area `Agricola` como especializacao operacional de `Rural`.
4. Planejar implementacao futura apenas apos aceite documental do modelo minimo.
5. Manter conceitos adiados em backlog de dominio, nao em Discovery promovida.

## Encerramento

Nenhum codigo funcional foi alterado.

Nenhuma interface foi alterada.

Nenhum runtime foi alterado.

Nenhuma entidade foi criada.

Nenhum CSV foi criado.

Nenhuma camada nova foi criada.

PA-01 foi preservado.

GP-A23 foi respeitada.

Nenhuma Discovery foi promovida.

## Veredito R01 - Cobertura de Ponto de Coleta

Status: ENCERRADO.

O runtime atual cobre um ponto principal de coleta por projeto. O campo escalar `ProjetoMonitoramento.ponto_principal_coleta` e validado pelo catalogo `PONTOS_PRINCIPAIS_COLETA`, persistido no projeto, editado por um unico controle na interface e propagado sem alteracao para `DossierFinal.ponto_principal_coleta`.

Fronteira preservada:

* ponto principal de coleta representa o contexto principal do projeto e nao um cadastro de pontos;
* a cobertura atual permanece limitada a um ponto principal por projeto;
* nao foi comprovada necessidade de registro multiponto;
* cadastro multiponto permanece adiado ate existir requisito expressamente autorizado;
* nenhuma alteracao de persistencia, interface, dossie, teste ou runtime e autorizada por este veredito;
* GPS, fotos, cadeia de custodia, anexos, multiplos pontos e multiplos coletores permanecem fora deste fechamento.

O item R01 do roadmap fica reconciliado com essa cobertura. O encerramento documenta o comportamento existente e nao cria requisito, prioridade ou autorizacao de implementacao futura.

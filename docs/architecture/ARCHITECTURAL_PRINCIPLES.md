# Princípios Arquiteturais

## PA-01 - Separação Entre Seleção E Execução De Políticas

O Monitoramento Hídrico separa seleção de política e execução de avaliação.

Regras:

* O Policy Engine seleciona qual política deve ser aplicada.
* Motores especializados executam avaliações.
* O Policy Engine não executa avaliação.
* Motores especializados não escolhem política.
* Políticas podem apontar para motores observacionais, normativos futuros ou internos futuros.

Motivação:

* Preservar rastreabilidade.
* Evitar mistura entre avaliação observacional e conformidade legal.
* Permitir evolução incremental conforme a filosofia ICFACTORY.
* Facilitar testes isolados de seleção e execução.

## PAR-ICF-001 — PRINCÍPIO DA GOVERNANÇA DO CICLO DE DECISÃO

### Status

PRINCÍPIO ARQUITETURAL

### Objetivo

Estabelecer a separação formal entre auditoria, decisão institucional, documentação e evidência, assegurando que toda decisão relevante siga um ciclo completo, rastreável e auditável.

### Fundamentação

A experiência prática obtida durante as GPs administrativas do Pacote AGIPI demonstrou que decisões institucionais não podem ser confundidas com auditorias, nem incorporadas automaticamente ao patrimônio documental.

O método passa a reconhecer explicitamente que existe um ciclo próprio de governança para decisões institucionais.

### Princípio

Nenhuma decisão institucional integra o patrimônio documental do ICFACTORY sem que sejam cumpridas, obrigatoriamente, todas as etapas do Ciclo de Governança da Decisão.

### Ciclo de Governança da Decisão

1. Evidência

Identificação objetiva de fatos, necessidades, lacunas ou não conformidades.

↓

2. Auditoria

Análise técnica da evidência.

A auditoria identifica decisões necessárias, mas nunca as toma.

↓

3. Matriz de Decisões

Classificação formal das decisões necessárias.

Cada decisão deverá indicar:

• objeto;
• fundamento;
• autoridade competente;
• impacto esperado.

↓

4. Autoridade Competente

A decisão somente poderá ser tomada pela autoridade previamente definida pelo modelo de governança.

A IA, agentes automatizados e auditorias não possuem competência para substituir essa autoridade.

↓

5. Decisão Institucional

A decisão aprovada deverá possuir registro próprio, contendo, no mínimo:

• identificador único;
• autoridade emissora;
• objeto;
• fundamentação;
• competências;
• limites;
• situação;
• vigência;
• histórico de revisão.

↓

6. Documento Canônico da Decisão

Cada decisão institucional deverá possuir uma fonte primária de autoridade.

Este documento torna-se a referência oficial da decisão.

↓

7. Incorporação Documental

Os documentos institucionais consumidores deverão apenas incorporar ou referenciar a decisão canônica.

É vedado:

• reinterpretar a decisão;
• ampliar competências;
• alterar limites;
• criar novas decisões.

↓

8. Nova Evidência

Após a incorporação documental, a decisão passa a integrar o patrimônio documental e torna-se nova evidência passível de auditoria futura.

### Regras Obrigatórias

#### RO-01

Auditorias nunca tomam decisões.

#### RO-02

Toda decisão possui autoridade competente definida.

#### RO-03

Toda decisão institucional possui documento canônico próprio.

#### RO-04

Nenhum documento consumidor substitui o documento canônico.

#### RO-05

Toda incorporação documental deve preservar rastreabilidade completa.

#### RO-06

Documentação nunca amplia ou modifica decisões.

#### RO-07

Toda decisão permanece auditável durante todo o seu ciclo de vida.

### Benefícios

• separação entre análise e autoridade;
• redução de ambiguidades;
• eliminação de duplicidade documental;
• preservação da fonte única de autoridade;
• fortalecimento da rastreabilidade;
• maior auditabilidade do patrimônio institucional;
• redução do risco de decisões implícitas;
• governança consistente entre humanos e agentes de IA.

### Aplicação

Este princípio aplica-se a toda decisão institucional que produza efeitos sobre:

• patrimônio institucional;
• arquitetura;
• governança;
• pesquisas;
• ativos;
• representação;
• titularidade;
• licenciamento;
• submissões institucionais;
• políticas permanentes do ICFACTORY.

### Verificação

Toda auditoria deverá verificar:

✓ existência da decisão;
✓ autoridade competente;
✓ documento canônico;
✓ rastreabilidade;
✓ incorporação documental;
✓ ausência de alterações não autorizadas.

### Conclusão

O ICFACTORY passa a adotar formalmente o Princípio da Governança do Ciclo de Decisão como mecanismo permanente de separação entre auditoria, autoridade, decisão, documentação e evidência, garantindo que nenhuma decisão institucional seja promovida ao patrimônio documental sem seguir integralmente o ciclo de governança estabelecido.

### Autoridade normativa

Conteúdo aprovado exclusivamente pela `DI-02 — Aprovação do Princípio Arquitetural`.

Identificador `PAR-ICF-001` instituído exclusivamente pela `DI-04 — Política de Namespaces Institucionais`.

Documentos canônicos:

• `docs/institutional/AGIPI/DI_02_APPROVAL_ARCHITECTURAL_PRINCIPLE.md`
• `docs/institutional/AGIPI/DI_04_NAMESPACE_POLICY.md`

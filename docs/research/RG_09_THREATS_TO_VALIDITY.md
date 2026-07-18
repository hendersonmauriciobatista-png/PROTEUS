# GP-RG-09 — Ameaças à Validade

## 1. Escopo

Avaliar ameaças ao primeiro piloto sintético do GX-PKG, separando validade interna, validade externa e reprodutibilidade. Mitigações propostas não alteram resultados nem instrumentos RG-08.

## 2. Matriz de ameaças

| ID | Ameaça | Dimensão | Impacto possível | Evidência no piloto | Mitigação futura |
|---|---|---|---|---|---|
| TV09-01 | cenários sintéticos em vez de pacotes reais | externa | superestimar clareza e executabilidade do checklist | fixtures pequenos e em Markdown | aplicar prospectivamente a pacote real sem alterar critérios |
| TV09-02 | casos construídos a partir das próprias quatro classes | interna/constructo | circularidade e alta acurácia por construção | resultados esperados vieram da OEG e regras RG-08 | usar novos casos elaborados por terceiro e classificação cega |
| TV09-03 | conhecimento prévio dos resultados esperados | interna | viés de confirmação na atribuição dos estados | Harness montou e verificou os casos | separar curador e verificadores; ocultar falha esperada quando seguro |
| TV09-04 | mesmo Harness como curador, V1, V2 e documentador | reprodutibilidade | concordância refletir memória/consistência do mesmo agente | acumulação declarada | dois verificadores independentes, idealmente humano e ferramenta distinta |
| TV09-05 | mesmo ambiente e sistema de arquivos | externa/reprodutibilidade | não detectar diferenças de path, encoding, ACL e case sensitivity | Windows único | repetir em Windows/Linux e depósito remoto controlado |
| TV09-06 | apenas quatro cenários | externa | classes de falha não cobertas | uma instância por classe | matriz fatorial com falhas simples/combinadas e múltiplas instâncias |
| TV09-07 | falhas C/D evidentes | interna | não testar corrupção sutil ou ambiguidade limítrofe | ausência total ou arquivo ausente | incluir hash divergente, symlink, versão colisora, anexo parcial e permissão intermitente |
| TV09-08 | ressalva B claramente não bloqueante | constructo | não testar fronteira entre ressalva e bloqueio | rótulo legado não é usado por procedimento | casos limítrofes com decisão cega e regra de adjudicação pre-registrada |
| TV09-09 | formatos apenas Markdown | externa | não cobrir binários, datasets, archives e ferramentas proprietárias | seis arquivos textuais por pacote positivo | testar PDF, CSV, binário, archive e dependência de runtime |
| TV09-10 | nenhuma fonte externa/remota | externa | não avaliar disponibilidade, autenticação ou snapshot | fontes proibidas e locais | testar depósito versionado autorizado, sem usar URL viva como entrada |
| TV09-11 | permissões inferidas do workspace | interna | ACL por papel não exercitada | Harness tinha acesso local | contas/containers separados e teste explícito de leitura/escrita |
| TV09-12 | digest agregado ad hoc | reprodutibilidade | outra implementação ordenar/codificar de modo diferente | convenção documentada em UTF-8 e ordem por nome | padronizar serialização do Manifesto e digest em versão futura autorizada |
| TV09-13 | ausência de medição de tempo/custo | externa | desconhecer carga operacional do gate | não pre-registrada | medir duração e esforço por check em próximo piloto |
| TV09-14 | ausência de falso positivo espontâneo | interna | não estimar taxa real de bloqueio indevido | casos positivos projetados para passar | amostra cega com pacotes reais e revisão de referência independente |
| TV09-15 | mutação concorrente não testada | externa | certificado pode ficar obsoleto durante distribuição | fixtures permaneceram estáveis | teste controlado de mutação pós-certificação e rechecagem |

## 3. Classes de falhas não contempladas

- hash divergente com arquivo presente;
- bytes iguais com identidade/versão errada;
- colisão de IDs;
- referência circular ou órfã não evidente;
- anexo truncado;
- arquivo legível pelo curador e inacessível ao avaliador;
- link simbólico que escapa da raiz;
- diferença de maiúsculas/minúsculas entre plataformas;
- arquivo alterado após certificação;
- pacote assimétrico entre avaliadores;
- dependência binária ou runtime ausente;
- custódia/propriedade contestada;
- ressalvas combinadas que se tornam materialmente bloqueantes.

A ausência dessas falhas impede generalizar a acurácia observada para qualquer pacote experimental.

## 4. Interpretação das ameaças

### Validade interna

O piloto demonstra coerência entre fixtures, checklist e regra decisória. A verdade de referência é forte porque as injeções são observáveis, mas o mesmo agente conhecia as classes esperadas. Assim, a conclusão interna é aceitável para teste de mesa operacional e limitada para eficácia independente.

### Validade externa

Baixa: quatro pacotes pequenos, locais e textuais não representam diversidade real de formatos, ambientes, permissões e falhas. Nenhuma alegação universal é permitida.

### Reprodutibilidade

Foi observada repetibilidade exata no mesmo Harness/ambiente: 144/144 checks e 4/4 decisões concordaram. Reprodutibilidade independente permanece não testada.

## 5. Cadeia da avaliação de validade

- **Premissas:** resultado perfeito em amostra construída pode refletir desenho, não robustez geral.
- **Evidências:** quatro casos, mesmo Harness, uma plataforma, falhas conhecidas e 100% de concordância interna.
- **Inferências:** há evidência de coerência operacional, mas não de generalidade ou desempenho real.
- **Fundamentação:** ameaças de seleção, confirmação, dependência comum e baixa representatividade limitam alcance.
- **Decisão:** classificar validade interna como moderada para o objetivo sintético, validade externa como baixa e repetibilidade interna como alta.
- **Limitações:** avaliações qualitativas, sem verificadores independentes ou limiares calibrados.
- **Validação:** conclusão é coerente com a matriz e não promove GX-PKG a validação universal.

## 6. Prioridades futuras

1. verificadores independentes e cegos;
2. casos reais/multiformato em sandbox;
3. matriz de falhas simples e combinadas;
4. ambientes distintos;
5. teste de mutação/distribuição;
6. métricas de tempo, custo e falso bloqueio;
7. adjudicação pre-registrada para casos limítrofes.


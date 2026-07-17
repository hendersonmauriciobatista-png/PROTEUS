# GP-PE-24 - Plano Oficial De Promocao Patrimonial Do Acervo Tecnico

## 1. Identificacao

Programa: **GP-PE-24 - Plano de Promocao Patrimonial do Acervo Tecnico**.

Natureza: planejamento documental.

Data de emissao: 17/07/2026.

Estado de execucao: **PLANO EMITIDO; NENHUM LOTE INICIADO**.

## 2. Objetivo

Estabelecer a politica oficial, os criterios, a ordem, os gates e os lotes recomendados para a futura promocao do acervo tecnico identificado na GP-PE-23, preservando integralmente a governanca ICFACTORY e sem executar qualquer promocao nesta GP.

## 3. Escopo

O plano abrange:

* criterios oficiais de promocao e permanencia local;
* criterios de revisao, consolidacao e arquivamento futuro;
* politica para ativos constitucionais, operacionais, experimentais e temporarios;
* tratamento das categorias OFICIAL, CERTIFICADO, OPERACIONAL, SUPORTE, PESQUISA, EXPERIMENTAL e TEMPORÁRIO;
* lotes futuros, dependencias, prioridades, impactos, riscos, pre-requisitos e criterios de conclusao;
* cronograma exclusivamente logico, sem datas;
* gates de governanca e evidencias minimas para cada promocao.

Ficam fora do escopo:

* promover, mover, excluir ou renomear arquivos;
* alterar codigo, arquitetura, funcionalidade, dados, testes, midia ou ferramentas;
* criar modulos;
* executar revisoes de conteudo previstas pelos lotes;
* iniciar qualquer lote;
* iniciar a Onda B.

## 4. Metodologia

O planejamento foi produzido por:

1. recuperacao das condicoes de elegibilidade registradas na GP-PE-22;
2. adocao do universo patrimonial congelado pela GP-PE-23: 346 artefatos, 173 rastreados e 173 locais;
3. separacao entre classificacao patrimonial, estado Git e forma de custodia;
4. identificacao de dependencias de autoridade segundo a sequencia `Autoridade -> HISTORY -> ROADMAP -> README`;
5. particionamento do acervo local em lotes atomicos por natureza, risco e destino de custodia;
6. definicao de gates de entrada, execucao futura e conclusao;
7. avaliacao de riscos de promocao massiva, autoridade indevida, dados mutaveis, midia, binarios e pesquisa;
8. verificacao de que o plano nao depende de alteracao arquitetural ou funcional.

## 5. Referencias Utilizadas

### 5.1 Referencias Obrigatorias

* `docs/architecture/PE_22_WAVE_B_ELIGIBILITY_AUDIT.md`;
* `docs/architecture/PE_23_TECHNICAL_ASSET_INVENTORY.md`;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`;
* estrutura fisica e estado Git atual do repositorio.

### 5.2 Evidencias Herdadas

Da GP-PE-22:

* arquitetura elegivel com ressalvas;
* ausencia de pendencia obrigatoria da Onda A;
* necessidade de iniciar a regularizacao por frente documental controlada;
* proibicao de tratar todo o acervo local como autoridade unica.

Da GP-PE-23:

* veredito `ACERVO FRAGMENTADO`;
* 346 artefatos preexistentes;
* 173 artefatos locais, equivalentes a 99,51% do volume fisico;
* 87 OFICIAL, 5 CERTIFICADO, 73 OPERACIONAL, 61 SUPORTE, 5 PESQUISA, 31 EXPERIMENTAL, 84 TEMPORÁRIO e 0 OBSOLETO;
* quatro grupos de duplicidade binaria;
* ausencia de politica unica de dados, midia, retencao, checksums e binarios grandes;
* recomendacao de promocao atomica e seletiva.

## 6. Conceitos Oficiais Do Plano

### 6.1 Promocao Patrimonial

Promocao e o ato governado de transformar um artefato local ou nao reproduzivel em patrimonio formalmente custodiado, rastreavel e recuperavel.

Promocao nao significa necessariamente incluir o arquivo no Git. O destino pode ser:

* repositorio Git, para texto, codigo, testes, schemas e pequenos ativos estaveis;
* armazenamento institucional de objetos, para binarios grandes, midia e evidencias;
* arquivo institucional somente leitura, para material encerrado sujeito a retencao;
* permanencia local controlada, quando ainda nao houver maturidade, autoridade ou destino adequado.

### 6.2 Revisao

Revisao verifica atualidade, coerencia, privacidade, licenca, referencias, linguagem institucional e compatibilidade com autoridades vigentes. Revisao nao promove por si mesma.

### 6.3 Consolidacao

Consolidacao seleciona fonte canonica, resolve versoes sobrepostas e estabelece relacao entre fonte, derivado e entrega. Consolidacao nao autoriza reescrita de historia nem promocao normativa de pesquisa.

### 6.4 Custodia

Custodia define onde o artefato reside, quem responde logicamente por ele, como e versionado, como e recuperado e quando e revisto.

### 6.5 Arquivamento Futuro

Arquivamento e a transferencia governada de artefato sem uso corrente para area recuperavel e somente leitura. Nao equivale a exclusao e exige decisao propria.

## 7. Principios De Promocao

1. **Autoridade antes de registro**: promover primeiro o artefato de autoridade; depois HISTORY; depois ROADMAP; por ultimo README.
2. **Uma classificacao por artefato**: a promocao nao altera classificacao sem decisao expressa.
3. **Lotes atomicos e pequenos**: cada lote deve poder ser auditado, revertido e explicado isoladamente.
4. **Sem promocao massiva**: os 173 locais nao formam um unico lote valido.
5. **Conteudo antes de custodia**: arquivo incoerente ou desatualizado deve ser revisto antes da promocao.
6. **Custodia proporcional ao risco**: texto pequeno e estavel pode ir ao Git; binario grande ou dado mutavel exige destino proprio.
7. **Pesquisa nao e norma**: PESQUISA e EXPERIMENTAL mantem seus limites apos promocao de custodia.
8. **Temporario nao e patrimonio por padrao**: TEMPORÁRIO permanece fora do patrimonio promovido salvo reclassificacao individual.
9. **Dados operacionais nao sao documentacao estatica**: exigem politica de backup, retencao, privacidade e restauracao.
10. **Promocao nao modifica semantica**: correcao, curadoria e consolidacao devem ocorrer antes, em etapa claramente identificada.
11. **Proveniencia obrigatoria**: toda promocao deve apontar origem, classificacao, responsavel logico, hash e autoridade de decisao.
12. **Autoridade humana preservada**: nenhuma classificacao, descarte, publicacao ou promocao normativa ocorre automaticamente.
13. **ICFACTORY congelado**: patrimonio do projeto nao altera Constituicao, Lexico, Discovery ou norma metodologica sem processo proprio.
14. **Onda B independente**: executar este plano nao inicia automaticamente a Onda B.

## 8. Criterios Oficiais

### 8.1 Criterios De Promocao

Um artefato somente pode entrar em lote de promocao quando:

* existir fisicamente e estiver legivel;
* possuir classificacao unica confirmada;
* possuir responsavel logico;
* ter finalidade e uso atual documentados;
* possuir destino de custodia definido;
* possuir hash e tamanho registrados no momento da execucao;
* nao conter segredo, dado pessoal ou material sem licenca identificado;
* ter referencias internas verificadas;
* nao contradizer autoridade superior;
* possuir risco e estrategia de rollback/recuperacao registrados;
* integrar diff ou pacote isolado de arquivos estritamente autorizados;
* receber atualizacao de HISTORY/ROADMAP apenas depois da autoridade correspondente;
* ser aprovado pela GP especifica do lote.

### 8.2 Criterios De Permanencia Local

O artefato deve permanecer local quando qualquer condicao abaixo existir:

* maturidade insuficiente ou uso ainda exploratorio;
* classificacao EXPERIMENTAL sem gate de saida atendido;
* classificacao TEMPORÁRIO sem justificativa de retencao;
* dado operacional mutavel sem politica de custodia;
* midia sem revisao de privacidade, licenca ou destino;
* binario grande sem armazenamento institucional adequado;
* duplicidade sem fonte canonica definida;
* documento com conflito material ainda nao resolvido;
* ausencia de responsavel logico ou autoridade de promocao.

Permanencia local nao equivale a abandono. Artefato critico local exige backup transitorio ate decisao posterior.

### 8.3 Criterios De Consolidacao

Consolidacao e obrigatoria quando:

* existirem versoes master, final, segmentada e assembly do mesmo conteudo;
* documento e implementacao apresentarem estados diferentes;
* HISTORY, ROADMAP e README repetirem conclusoes divergentes;
* fonte e derivado nao estiverem relacionados;
* ativos identicos possuirem nomes funcionais diferentes;
* varios diretorios alegarem autoridade sobre a mesma identidade ou entrega;
* promocao parcial quebrar a compreensao do conjunto.

### 8.4 Criterios De Revisao

Revisao e obrigatoria para:

* conteudo institucional externo;
* contatos, mensagens de adocao e publico-alvo;
* documentos com proximos passos ou estados historicos;
* dados, relatorios e evidencias operacionais;
* scripts com dependencias de ambiente;
* midia, legenda, narracao e roteiro;
* pesquisas locais e catalogos de Discoveries;
* artefatos com referencias a arquivos ausentes ou nao promovidos.

### 8.5 Criterios De Arquivamento Futuro

Um artefato somente podera ser arquivado futuramente se:

* houver sucessor canonico formalmente promovido;
* nenhuma rotina, documento vigente ou lote depender dele como fonte ativa;
* prazo ou evento de retencao estiver cumprido;
* hash, origem, classificacao e motivo do arquivamento estiverem registrados;
* houver destino recuperavel e somente leitura;
* responsavel logico e governanca aprovarem a operacao;
* HISTORY registrar a transicao sem apagar a memoria anterior.

Arquivamento nao autoriza exclusao. Exclusao exige processo destrutivo proprio, fora deste plano.

### 8.6 Criterios Para Ativos Experimentais

Ativo EXPERIMENTAL deve:

* permanecer explicitamente rotulado como nao normativo e nao oficial;
* possuir hipotese, finalidade ou fase de producao identificada;
* ficar segregado de entregas finais;
* nao ser citado como prova de funcionalidade, certificacao ou validacao externa;
* ter gate de saida definido: promover, manter experimental ou arquivar;
* ter revisao de risco antes de qualquer publicacao;
* usar armazenamento adequado ao tamanho e sensibilidade.

### 8.7 Criterios Para Patrimonio Operacional

Patrimonio OPERACIONAL deve distinguir:

* codigo, testes, schema e configuracao estavel: versionamento Git e regressao;
* fixture/demonstracao: identificacao explicita e reprodutibilidade;
* dado operacional mutavel: backup, retencao e controle de acesso fora da logica de commit comum;
* relatorio gerado: origem, periodo, finalidade e retencao;
* site e entrega final: versao publicada, fonte, hash e responsavel;
* binario final: armazenamento de objetos, checksum e copia de seguranca.

## 9. Analise Patrimonial Por Categoria

| Categoria | Situacao GP-PE-23 | Pode promover imediatamente? | Exige consolidacao? | Exige revisao? | Deve permanecer local? | Etapa futura |
| --- | --- | --- | --- | --- | --- | --- |
| OFICIAL | 87; 26 locais | Sim, apenas autoridades maduras e isolaveis, como PE-22/23/24. | Sim para HISTORY, ROADMAP, README, adocao, apresentacao e conjuntos sobrepostos. | Sim quando houver estado, referencia ou comunicacao externa. | Somente os ainda incoerentes ou sem pacote proprio. | Lotes 01, 03, 04 e 08. |
| CERTIFICADO | 5; 1 local | Sim para o certificado PAC como parte do conjunto atomico, nunca sozinho. | Sim com a Constituicao e o acervo que ele certifica. | Revalidacao mecanica obrigatoria. | Ate o gate PAC ser aprovado. | Lote 02. |
| OPERACIONAL | 73; 3 locais, alem de modificacoes em dados/relatorio | Nao por categoria. Codigo ja versionado permanece; filme final pode ser custodiado apos revisao. | Sim para dados, relatorios e entrega audiovisual. | Sempre para dados mutaveis e publicacao. | Dados e binarios sem politica devem permanecer locais. | Lotes 05 e 06. |
| SUPORTE | 61; 27 locais | Apenas suporte inseparavel de autoridade promovida e previamente revisto. | Sim para guias, scripts, narracoes e adocao. | Sim para portabilidade e atualidade. | Caches e auxiliares nao essenciais. | Lotes 03, 04 e 06. |
| PESQUISA | 5; 2 locais | Pode ser promovida como pesquisa, nunca como norma, apos validar rotulagem. | Discovery Catalog e Harness devem formar pacote proprio. | Sim, inclusive referencias e status. | Ate lote de pesquisa autorizado. | Lote 03. |
| EXPERIMENTAL | 31; 30 locais | Nao. | Sim quando houver familias de versoes ou midia. | Sim antes de qualquer mudanca de estado. | Sim por padrao, em custodia experimental. | Lote 07 ou GP futura especifica. |
| TEMPORÁRIO | 84; todos locais | Nao. | Apenas para selecionar eventual evidencia candidata. | Revisao de necessidade, nao de promocao em massa. | Sim, em area reconstruivel e ignorada. | Lote 07 define destino; promocao excepcional exige reclassificacao. |

Resposta objetiva:

* promocao imediata potencial: subconjuntos maduros de OFICIAL e CERTIFICADO, por lote atomico;
* consolidacao obrigatoria: partes de OFICIAL, OPERACIONAL, SUPORTE e PESQUISA;
* revisao obrigatoria: comunicacao externa, dados, midia, scripts e pesquisas locais;
* permanencia local: todo TEMPORÁRIO, todo EXPERIMENTAL ainda sem gate e todo operacional sem custodia;
* promocao apenas futura: dados operacionais, filme/fontes audiovisuais, pesquisa local, adocao e suporte dependente de revisao.

## 10. Politica De Custodia

### 10.1 Patrimonio Constitucional

Abrange Constituicoes, principios arquiteturais, documentos normativos do projeto, certificados, decisoes formais de elegibilidade/inventario/plano e autoridades PAC promovidas.

| Elemento | Politica |
| --- | --- |
| Local recomendado | `docs/governance/` e `docs/architecture/`; PAC em `docs/pac/` segundo autoridade vigente. |
| Forma de custodia | Repositorio Git oficial, commits atomicos, historico imutavel e referencia por hash de commit. |
| Versionamento | Alteracao somente por GP propria; nunca sobrescrever parecer historico para refletir estado posterior. |
| Backup | Espelho remoto do repositorio e copia institucional em cada gate de onda. |
| Revisao | A cada alteracao constitucional, encerramento de onda, conflito de autoridade ou auditoria de consolidacao. |

### 10.2 Patrimonio Operacional

Abrange codigo, testes, schemas, configuracoes, website, dados, relatorios e entregas finais em uso.

| Elemento | Politica |
| --- | --- |
| Local recomendado | Git para codigo/teste/schema/configuracao/site; armazenamento operacional controlado para dados mutaveis; object storage para binarios finais. |
| Forma de custodia | Separar fonte versionada, fixture, dado vivo, evidencia e entrega publicada. |
| Versionamento | Semantico por release/GP para fonte; snapshots ou backup para dados; checksum e identificador de versao para binarios. |
| Backup | Antes e depois de migracoes; a cada ciclo operacional definido pelo responsavel; redundancia para entrega final. |
| Revisao | Em cada release, mudanca de schema, publicacao, restauracao ou alteracao de politica. |

### 10.3 Patrimonio Experimental

Abrange GP-R06, cenas brutas, assembly cut, animatic, projeto editavel e demais artefatos sem maturidade final.

| Elemento | Politica |
| --- | --- |
| Local recomendado | `docs/research/` para texto; area experimental segregada ou armazenamento de objetos para midia. |
| Forma de custodia | Manifesto com classificacao, dono, hipotese/fase, hash e restricao de uso. |
| Versionamento | Git para texto pequeno; versoes de objeto para binarios; nunca misturar com entrega final. |
| Backup | Ao encerrar uma captura, experimento ou marco de edicao considerado recuperavel. |
| Revisao | Em cada gate de pesquisa/producao e antes de publicacao, promocao ou arquivamento. |

### 10.4 Patrimonio Temporario

Abrange ferramentas vendorizadas, wheels, binarios reconstruiveis, folhas de contato, capturas derivadas, cartelas duplicadas e arquivos de concat.

| Elemento | Politica |
| --- | --- |
| Local recomendado | Area local ignorada, diretorio temporario controlado ou cache de ferramenta; fora do patrimonio oficial. |
| Forma de custodia | Sem garantia de permanencia, salvo manifesto de reconstrucao. |
| Versionamento | Nao versionar por padrao. Reclassificacao formal obrigatoria antes de excecao. |
| Backup | Nao obrigatorio; apenas para candidato a evidencia ate decisao. |
| Revisao | Ao fim de cada execucao produtora e em cada gate de fechamento de lote. |

## 11. Gates Gerais De Execucao Futura

### Gate G0 - Autorizacao

* GP especifica do lote emitida;
* escopo e arquivos enumerados;
* nenhum lote iniciado apenas por este plano.

### Gate G1 - Integridade

* existencia, legibilidade, hash e tamanho registrados;
* estado Git e dependencias confirmados;
* contagem GP-PE-23 revalidada no recorte do lote.

### Gate G2 - Autoridade E Conteudo

* classificacao, responsavel e finalidade confirmados;
* revisao/consolidacao previa concluida quando exigida;
* ausencia de conflito com ICFACTORY e autoridades superiores.

### Gate G3 - Custodia E Risco

* destino de custodia aprovado;
* backup e recuperacao definidos;
* privacidade, licenca, segredo e supply chain verificados;
* rollback documentado.

### Gate G4 - Promocao Atomica

* somente arquivos autorizados incluidos;
* autoridade promovida antes dos registros derivados;
* diff verificavel e sem absorcao de alteracoes estranhas.

### Gate G5 - Certificacao Do Lote

* criterios de conclusao atendidos;
* HISTORY e ROADMAP coerentes com o que foi efetivamente promovido;
* reproducibilidade verificada no destino de custodia;
* parecer final proprio emitido.

## 12. Estrategia De Promocao E Lotes Propostos

### Lote 01 - Autoridades Arquiteturais De Elegibilidade E Patrimonio

| Campo | Definicao |
| --- | --- |
| Objetivo | Tornar GP-PE-22, GP-PE-23 e GP-PE-24 autoridades reproduziveis, com registros minimos correspondentes. |
| Categorias | OFICIAL. |
| Dependencias | GP-PE-22 concluida; GP-PE-23 concluida; aprovacao deste plano. |
| Riscos | Absorver as milhares de linhas locais nao relacionadas de HISTORY/ROADMAP; alterar parecer durante promocao. |
| Prioridade | CRITICA. |
| Impacto estimado | Alto documental; nenhum impacto funcional ou arquitetural. |
| Pre-requisitos | Enumerar exatamente os tres relatorios; isolar somente registros GP-PE-22/23/24; validar links e diff. |
| Criterios de conclusao | Tres relatorios reproduziveis no destino; registros coerentes; nenhum outro artefato promovido; auditoria de diff aprovada. |

Justificativa tecnica: essas autoridades definem elegibilidade, inventario e politica. Sem elas, os lotes seguintes nao possuem base reproduzivel.

### Lote 02 - Acervo Constitucional E Certificado Do PAC

| Campo | Definicao |
| --- | --- |
| Objetivo | Promover atomicamente a Constituicao PAC e o acervo PAC certificado. |
| Categorias | OFICIAL e CERTIFICADO. |
| Dependencias | Lote 01; GP-PAC-12A; cadeia PAC-01 a PAC-14. |
| Riscos | Promocao parcial, referencias quebradas, divergencia entre contagens locais e certificacao historica. |
| Prioridade | CRITICA. |
| Impacto estimado | Alto institucional; nenhum impacto funcional. |
| Pre-requisitos | Repetir checklist mecanico da GP-PAC-12A; confirmar 328 achados; validar 16 arquivos incluindo `PAC_CONSTITUTION.md`; backup previo. |
| Criterios de conclusao | Todos os 16 arquivos custodiados juntos; contagens e referencias aprovadas; certificado continua fiel; HISTORY/ROADMAP atualizados depois do conjunto. |

Justificativa tecnica: o PAC e patrimonio critico, certificado localmente e inteiramente ausente do `HEAD`; fragmenta-lo destruiria sua cadeia de autoridade.

### Lote 03 - Dominio E Pesquisa Governada

| Campo | Definicao |
| --- | --- |
| Objetivo | Regularizar GP-D01C, Discovery Catalog e dossie de Harnesses sem atribuir autoridade normativa a pesquisa. |
| Categorias | OFICIAL, PESQUISA e SUPORTE. |
| Dependencias | Lote 01; autoridades de dominio e pesquisa ja versionadas. |
| Riscos | Promocao indireta de Discovery, colisao de identificadores, referencias a material nao promovido. |
| Prioridade | ALTA. |
| Impacto estimado | Medio/alto documental e metodologico. |
| Pre-requisitos | Revisar identificadores, referencias, status nao normativo e relacao com GP-R02/R03/R06. |
| Criterios de conclusao | GP-D01C reproduzivel; pacote de pesquisa rotulado; nenhuma Discovery promovida; HISTORY/ROADMAP fieis ao escopo. |

Justificativa tecnica: documentos de dominio e pesquisa sao pequenos e valiosos, mas exigem isolamento semantico para nao alterar governanca.

### Lote 04 - Adocao, Comunicacao E Documentacao Institucional Local

| Campo | Definicao |
| --- | --- |
| Objetivo | Revisar e promover documentos locais de adocao e apresentacao que representem comunicacao institucional vigente. |
| Categorias | OFICIAL e SUPORTE. |
| Dependencias | Lotes 01 e 03; PA-01 comunicacional; identidade visual vigente. |
| Riscos | Contato desatualizado, promessa indevida, publico-alvo nao validado, divergencia com produto atual. |
| Prioridade | ALTA. |
| Impacto estimado | Medio/alto institucional; nenhum impacto de runtime. |
| Pre-requisitos | Revisao humana de conteudo, dados pessoais, limites PA-01, paridade com website e selecao de fontes canonicas. |
| Criterios de conclusao | Documentos aprovados e custodiados; duplicidades explicadas; materiais rejeitados permanecem locais; nenhum texto experimental promovido como oficial. |

Justificativa tecnica: comunicacao externa tem risco institucional maior que seu tamanho e nao pode ser promovida apenas por existir.

### Lote 05 - Politica E Custodia Do Patrimonio Operacional Mutavel

| Campo | Definicao |
| --- | --- |
| Objetivo | Separar dados vivos, fixtures, demonstracao, relatorios e evidencias antes de decidir promocao. |
| Categorias | OPERACIONAL e SUPORTE. |
| Dependencias | Lote 01; definicao de responsavel de dados e retencao. |
| Riscos | Expor dados, versionar estado mutavel, perder historico, confundir exemplo com evidencia operacional. |
| Prioridade | ALTA. |
| Impacto estimado | Alto operacional e de governanca de dados; sem mudanca de schema neste plano. |
| Pre-requisitos | Classificar cada arquivo em `data/` e `reports/`; definir backup, privacidade, retencao e restauracao; validar JSON/CSV. |
| Criterios de conclusao | Politica aprovada; cada dado possui tipo e destino; `eventos_operacionais.json` e modificacoes locais recebem decisao individual; nenhum dado vivo entra em commit comum sem autorizacao. |

Justificativa tecnica: patrimonio operacional exige custodia diferente de documento estatico; promover sem politica agravaria a fragmentacao.

### Lote 06 - Patrimonio Audiovisual Final E Reproduzivel

| Campo | Definicao |
| --- | --- |
| Objetivo | Consolidar entrega final, legenda, manifestos, projeto editavel, fontes e scripts essenciais em custodia apropriada. |
| Categorias | OPERACIONAL, OFICIAL e SUPORTE. |
| Dependencias | Lotes 01 e 04; politica de armazenamento de objetos; revisao de privacidade/licenca. |
| Riscos | 423 MB locais, caminhos quebrados, manifestos desatualizados, perda de fontes, publicacao indevida. |
| Prioridade | MEDIA/ALTA. |
| Impacto estimado | Alto em volume e reproducibilidade; medio institucional. |
| Pre-requisitos | Escolher fonte canonica; reconciliar manifesto com MP4 existente; revisar codec, legenda, licenca e privacidade; gerar checksums; definir backup. |
| Criterios de conclusao | Filme final e fontes essenciais recuperaveis; projeto editavel validado; manifestos coerentes; binarios fora do Git comum quando aplicavel; temporarios excluidos do lote. |

Justificativa tecnica: midia final tem valor patrimonial, mas seu tamanho e sensibilidade exigem custodia de objetos, nao promocao indiscriminada ao Git.

### Lote 07 - Contencao Experimental E Temporaria

| Campo | Definicao |
| --- | --- |
| Objetivo | Formalizar permanencia, backup seletivo, reconstrucao e futuro arquivamento de EXPERIMENTAL e TEMPORÁRIO. |
| Categorias | EXPERIMENTAL e TEMPORÁRIO. |
| Dependencias | Lote 06 para distinguir fontes essenciais de derivados. |
| Riscos | Promover caches, perder experimento relevante, manter binarios inseguros, apagar evidencia sem autoridade. |
| Prioridade | MEDIA. |
| Impacto estimado | Alto em higiene e volume; nenhum impacto funcional. |
| Pre-requisitos | Manifesto de experimentos; lista de reconstruiveis; politica de ignore; decisao de retencao por familia. |
| Criterios de conclusao | 31 experimentais com dono e gate; 84 temporarios com regra de reconstrucao/retencao; nenhum temporario promovido; nenhum arquivo excluido sem GP propria. |

Justificativa tecnica: o lote reduz risco sem converter temporarios em patrimonio permanente e sem destruir material local.

### Lote 08 - Reconciliacao E Certificacao Patrimonial Final

| Campo | Definicao |
| --- | --- |
| Objetivo | Reconciliar autoridades promovidas, custodia externa, HISTORY, ROADMAP e README e emitir auditoria final do plano. |
| Categorias | Todas, sem promocao automatica de EXPERIMENTAL/TEMPORÁRIO. |
| Dependencias | Conclusao ou decisao formal de adiamento dos Lotes 01 a 07. |
| Riscos | Declarar consolidacao sem prova, reescrever historia, omitir patrimonio externo ou local deliberado. |
| Prioridade | ALTA DE FECHAMENTO. |
| Impacto estimado | Alto documental e de reproducibilidade. |
| Pre-requisitos | Manifestos e pareceres de todos os lotes; mapa de custodia; pendencias explicitas; verificacao limpa de referencias. |
| Criterios de conclusao | Autoridade/HISTORY/ROADMAP/README coerentes; cada artefato local remanescente possui justificativa; inventario atualizado; veredito patrimonial final emitido. |

Justificativa tecnica: consolidacao so pode ser declarada apos provar destino e estado de cada conjunto, inclusive o que conscientemente permanece local.

## 13. Matriz De Prioridades

| Ordem | Lote | Prioridade | Valor protegido | Motivo da ordem |
| ---: | --- | --- | --- | --- |
| 1 | Lote 01 | CRITICA | Autoridade do proprio programa patrimonial | Fundamenta todos os lotes seguintes. |
| 2 | Lote 02 | CRITICA | Constituicao e acervo PAC certificado | Maior risco de perda de autoridade documental local. |
| 3 | Lote 03 | ALTA | Dominio e pesquisa governada | Pequeno volume, alto valor e risco de promocao semantica indevida. |
| 4 | Lote 04 | ALTA | Comunicacao e adocao | Deve preceder consolidacao audiovisual e publicacao. |
| 5 | Lote 05 | ALTA | Dados e evidencias operacionais | Exige politica antes de qualquer versionamento adicional. |
| 6 | Lote 06 | MEDIA/ALTA | Filme final e fontes | Depende de comunicacao revisada e custodia de binarios. |
| 7 | Lote 07 | MEDIA | Experimentos e temporarios | Depende da separacao entre fonte essencial e derivado. |
| 8 | Lote 08 | ALTA DE FECHAMENTO | Coerencia patrimonial integral | Somente apos todos os destinos estarem decididos. |

## 14. Matriz De Riscos

| ID | Risco | Probabilidade | Impacto | Lotes | Controle obrigatorio |
| --- | --- | --- | --- | --- | --- |
| RP-01 | Promocao massiva dos 173 locais. | Media | Critico | Todos | Escopo enumerado e diff atomico por lote. |
| RP-02 | HISTORY/ROADMAP absorverem alteracoes nao autorizadas. | Alta | Alto | 01-08 | Curadoria de hunks e auditoria de diff antes do gate G4. |
| RP-03 | PAC parcial perder cadeia de autoridade. | Media | Critico | 02 | Pacote unico de 16 arquivos e revalidacao dos 328 achados. |
| RP-04 | Pesquisa virar norma por proximidade documental. | Baixa/Media | Alto | 03, 07 | Rotulo nao normativo e parecer de governanca. |
| RP-05 | Comunicacao conter promessa ou contato inadequado. | Media | Alto | 04, 06 | Revisao humana PA-01, privacidade e identidade. |
| RP-06 | Dados vivos serem tratados como fixture versionada. | Alta | Alto | 05 | Tipologia de dados e custodia separada. |
| RP-07 | Midia grande poluir Git ou exceder limites. | Alta | Alto | 06, 07 | Object storage/checksum; Git apenas para texto pequeno. |
| RP-08 | Material audiovisual expor informacao indevida. | Desconhecida | Alto | 06 | Revisao quadro a quadro e aprovacao humana. |
| RP-09 | Binarios vendorizados introduzirem supply-chain risk. | Media | Alto | 07 | Nao promover; documentar fonte/versao/reconstrucao. |
| RP-10 | Temporario relevante ser perdido antes de decisao. | Media | Medio/Alto | 06, 07 | Backup seletivo e manifesto transitorio. |
| RP-11 | Plano ser confundido com autorizacao de execucao. | Media | Alto | Todos | GP propria obrigatoria e estado `NAO INICIADO`. |
| RP-12 | Contagem GP-PE-23 ficar desatualizada. | Alta | Medio | Todos | Recontagem no Gate G1 de cada lote. |

## 15. Cronograma Logico Sem Datas

```text
GP-PE-24 aprovada
        |
        v
Lote 01 - Autoridades PE-22/23/24
        |
        v
Lote 02 - PAC constitucional e certificado
        |
        v
Lote 03 - Dominio e pesquisa governada
        |
        v
Lote 04 - Adocao e comunicacao institucional
        |
        v
Lote 05 - Custodia operacional de dados e relatorios
        |
        v
Lote 06 - Patrimonio audiovisual final
        |
        v
Lote 07 - Contencao experimental e temporaria
        |
        v
Lote 08 - Reconciliacao e certificacao final
```

Regra de sequenciamento:

* nenhum lote inicia por conclusao do anterior sem nova autorizacao;
* lote pode ser adiado por decisao formal, desde que o Lote 08 registre o adiamento;
* falha em gate impede somente o lote correspondente e seus dependentes;
* lotes nao devem ser fundidos para ganhar velocidade;
* nenhuma data ou prazo e criado por este plano.

## 16. Criterios De Encerramento De Cada Lote

| Lote | Evidencia minima de encerramento |
| --- | --- |
| 01 | PE-22/23/24 reproduziveis; somente registros correlatos; diff isolado. |
| 02 | 16 arquivos PAC custodiados; 328 achados revalidados; certificado e referencias integros. |
| 03 | GP-D01C e pacote de pesquisa rastreaveis; nenhuma promocao normativa. |
| 04 | Conteudo institucional revisado; fontes canonicas e limites PA-01 confirmados. |
| 05 | Politica de dados aprovada; tipo, destino, backup e retencao definidos por arquivo operacional local. |
| 06 | Filme, legenda, fontes e projeto recuperaveis; manifestos coerentes; checksums e backup existentes. |
| 07 | Experimentais e temporarios com dono/destino; nenhum descarte ou promocao implicita. |
| 08 | Inventario atualizado, mapa de custodia completo e documentos de governanca reconciliados. |

Condicoes comuns a todos:

* GP especifica concluida;
* gates G0 a G5 aprovados;
* nenhuma alteracao fora do escopo;
* rollback ou recuperacao demonstravel;
* parecer final explicito;
* estado posterior registrado sem reescrever historia.

## 17. Criterios De Encerramento Do Plano

O plano somente podera ser considerado executado quando:

1. Lotes 01 a 08 estiverem concluidos ou formalmente adiados com justificativa;
2. cada artefato inventariado possuir custodia oficial ou justificativa de permanencia local;
3. nenhum TEMPORÁRIO tiver sido promovido sem reclassificacao;
4. nenhum EXPERIMENTAL tiver adquirido autoridade por inferencia;
5. dados operacionais possuirem politica propria;
6. binarios e midia possuirem armazenamento, checksum e backup adequados;
7. HISTORY, ROADMAP e README refletirem somente autoridades efetivamente promovidas;
8. auditoria final independente emitir novo veredito patrimonial.

A aprovacao deste documento nao satisfaz nenhum desses criterios de execucao.

## 18. Ressalvas Do Plano

1. A contagem de 346 artefatos pertence ao corte da GP-PE-23 e devera ser revalidada em cada lote.
2. O destino institucional de binarios grandes ainda nao esta implementado.
3. A politica operacional de dados ainda nao existe e e pre-requisito do Lote 05.
4. HISTORY e ROADMAP possuem diffs locais amplos; seus registros nao podem ser promovidos por arquivo inteiro sem isolamento.
5. O PAC exige repeticao mecanica de sua certificacao antes do Lote 02.
6. Midia exige revisao humana de privacidade, licenca e coerencia antes de custodia final.
7. O plano define ordem e criterios, mas cada lote requer autorizacao propria.

Essas ressalvas nao invalidam a estrategia; elas sao gates explicitos da futura execucao.

## 19. Recomendacoes Finais

1. Adotar os oito lotes sem fusao ou promocao massiva.
2. Autorizar futuramente primeiro o Lote 01, nunca os lotes seguintes por inferencia.
3. Manter o PAC como unidade atomica constitucional/certificada.
4. Criar politica de dados antes de decidir sobre CSVs, JSON de eventos e relatorio local.
5. Escolher armazenamento de objetos antes de promover filme, fontes ou binarios.
6. Manter GP-R06 e demais experimentais sem autoridade normativa.
7. Manter ferramentas vendorizadas e temporarios fora do Git oficial.
8. Exigir checksums, responsavel logico, destino e backup em toda promocao futura.
9. Encerrar o programa somente por auditoria independente posterior.
10. Nao iniciar a Onda B como efeito deste plano.

## 20. Conclusao

O acervo fragmentado identificado na GP-PE-23 pode ser promovido de maneira segura, desde que a execucao seja seletiva, atomica e orientada por autoridade e custodia, nao por proximidade de diretorios ou volume de arquivos.

Oito lotes separam autoridades arquiteturais, PAC, dominio/pesquisa, comunicacao, dados operacionais, audiovisual, experimentos/temporarios e reconciliacao final. A politica impede promocao massiva, protege pesquisas contra normatizacao, mantem dados vivos fora do fluxo documental comum e reserva binarios grandes para custodia apropriada.

As dependencias ainda abertas foram convertidas em gates verificaveis. Nenhuma delas exige mudanca de codigo ou arquitetura para que o plano exista, mas todas devem ser atendidas antes da execucao do lote correspondente.

## 21. Veredito Final

# PLANO APROVADO COM RESSALVAS

Fundamentacao:

* estrategia e ordem de promocao estao definidas;
* categorias e tipos de custodia receberam tratamento proprio;
* cada lote possui objetivo, dependencias, riscos, prioridade, impacto, pre-requisitos e criterios de conclusao;
* cronograma logico e gates impedem promocao automatica;
* ressalvas de dados, midia, PAC e diffs locais foram transformadas em pre-condicoes obrigatorias;
* o plano preserva ICFACTORY, PA-01, pesquisas, experimentos e autoridade humana.

Decisao formal: **PLANO APROVADO COM RESSALVAS**, exclusivamente como politica documental. Nenhum lote esta autorizado ou iniciado por esta decisao.

## 22. Restricoes Preservadas

* Nenhum artefato promovido.
* Nenhum codigo-fonte alterado.
* Nenhuma arquitetura alterada.
* Nenhuma funcionalidade modificada.
* Nenhum arquivo movido, excluido ou renomeado.
* Nenhuma midia alterada.
* Nenhum modulo criado.
* Nenhuma pesquisa ou Discovery promovida.
* ICFACTORY integralmente preservado.
* Nenhum lote iniciado.
* Onda B nao iniciada.

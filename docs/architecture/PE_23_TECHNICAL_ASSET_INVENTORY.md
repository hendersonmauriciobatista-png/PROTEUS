# GP-PE-23 - Inventario E Classificacao Do Acervo Tecnico Do PROTEUS

## 1. Identificacao

Programa: **GP-PE-23 - Inventario e Classificacao do Acervo Tecnico do PROTEUS**.

Natureza: auditoria documental passiva.

Data de corte: 17/07/2026.

Baseline Git: commit `21f16acb7019d162f4f1643767f92ccbca8dec5f`, branch `feature/environment-data-v1`.

Estado auditado: conteudo rastreado no `HEAD`, modificacoes locais e arquivos nao rastreados existentes no momento do levantamento.

## 2. Objetivo

Inventariar, classificar e avaliar o patrimonio tecnico existente do PROTEUS, distinguindo autoridade versionada, patrimonio operacional, suporte, pesquisa, experimentos, temporarios e artefatos ainda locais antes do inicio da Onda B.

Esta auditoria nao promove artefatos, nao altera codigo, nao modifica arquitetura, nao move, exclui ou renomeia arquivos e nao inicia a Onda B.

## 3. Metodologia

O levantamento foi executado em cinco eixos:

1. inventario fisico de todos os arquivos do repositorio, excluidos `.git/`, `venv/` e `__pycache__/`;
2. verificacao do estado Git de cada arquivo: rastreado, modificado ou nao rastreado;
3. agrupamento por localizacao, finalidade e responsabilidade logica;
4. classificacao unica de cada arquivo segundo as oito categorias autorizadas;
5. analise de maturidade, uso, promocao, revisao, risco de perda, duplicidade e obsolescencia.

Validacoes quantitativas:

* enumeracao fisica por `Get-ChildItem -Recurse -File -Force`;
* enumeracao versionada por `git ls-files`;
* enumeracao local por `git ls-files --others --exclude-standard`;
* verificacao de modificacoes por `git diff --name-only`;
* contagem e soma de bytes por conjunto e classificacao;
* deteccao de duplicidade binaria por SHA-256.

O universo foi congelado antes da criacao deste relatorio. Portanto, `PE_23_TECHNICAL_ASSET_INVENTORY.md` e a atualizacao de seus registros em HISTORY e ROADMAP nao integram as 346 unidades preexistentes auditadas.

## 4. Escopo Auditado

Foram auditados:

* documentos arquiteturais, funcionais, operacionais, institucionais e de adocao;
* auditorias, constituicoes, HISTORY, ROADMAP, dossies, relatorios e evidencias;
* documentos de pesquisa, guias, checklists e roteiros;
* codigo de producao e testes como patrimonio tecnico;
* dados CSV e JSON e relatorio operacional persistido;
* website institucional;
* documentacao e ativos audiovisuais;
* scripts, projetos de edicao, ferramentas auxiliares e dependencias locais de producao audiovisual;
* artefatos intermediarios e finais produzidos durante o desenvolvimento.

Exclusoes justificadas:

| Exclusao | Motivo |
| --- | --- |
| `.git/` | Metadado interno do sistema de controle de versao, nao artefato do PROTEUS. |
| `venv/` | Ambiente local reconstruivel e externo ao patrimonio controlado do projeto. |
| `__pycache__/` | Cache derivado e reconstruivel do interpretador. |
| Diretorios vazios | Nao constituem artefatos unitarios; apenas arquivos foram contados. |

## 5. Taxonomia E Regra De Classificacao Unica

| Classificacao | Criterio aplicado |
| --- | --- |
| OFICIAL | Documento vigente de arquitetura, governanca, dominio, operacao ou comunicacao institucional, independentemente de ainda depender de promocao Git. |
| CERTIFICADO | Artefato que formalmente certifica uma implementacao ou um acervo e cujo proprio conteudo possui natureza de certificacao. Aplicacao deliberadamente restrita para nao inflar maturidade. |
| OPERACIONAL | Codigo, dado, site, relatorio ou entrega final usada diretamente na operacao ou apresentacao do PROTEUS. |
| SUPORTE | Teste, guia, checklist, manifesto, roteiro, configuracao ou material auxiliar que sustenta outros artefatos. |
| PESQUISA | Investigacao ou dossie sem autoridade normativa ou operacional. |
| EXPERIMENTAL | Hipotese congelada, captura bruta, animatic, assembly cut ou artefato de producao ainda sujeito a avaliacao. |
| TEMPORÁRIO | Cache, ferramenta vendorizada, captura derivada, folha de contato ou arquivo intermediario reconstruivel. |
| OBSOLETO | Artefato formalmente substituido e sem uso atual comprovado. Nenhum arquivo recebeu esta classificacao por falta de evidencia suficiente de obsolescencia formal. |

Quando um arquivo poderia se enquadrar em mais de uma categoria, prevaleceu sua funcao atual. Exemplo: um relatorio de auditoria que certifica explicitamente uma frente recebeu CERTIFICADO; os demais relatorios arquiteturais permaneceram OFICIAL. Um roteiro audiovisual permaneceu SUPORTE; uma gravacao bruta permaneceu EXPERIMENTAL; uma captura derivada permaneceu TEMPORÁRIO.

## 6. Resumo Executivo

### 6.1 Quantidade Total

**346 artefatos preexistentes auditados**, totalizando **425.773.327 bytes**.

### 6.2 Quantidade Por Categoria

| Categoria | Quantidade | Rastreado | Ainda local | Bytes |
| --- | ---: | ---: | ---: | ---: |
| OFICIAL | 87 | 61 | 26 | 1.442.673 |
| CERTIFICADO | 5 | 4 | 1 | 67.885 |
| OPERACIONAL | 73 | 70 | 3 | 2.313.577 |
| SUPORTE | 61 | 34 | 27 | 213.936 |
| PESQUISA | 5 | 3 | 2 | 60.328 |
| EXPERIMENTAL | 31 | 1 | 30 | 239.388.581 |
| TEMPORÁRIO | 84 | 0 | 84 | 182.286.347 |
| OBSOLETO | 0 | 0 | 0 | 0 |
| **Total** | **346** | **173** | **173** | **425.773.327** |

### 6.3 Patrimonio Critico

O patrimonio critico e composto por:

* Constituicao do Projeto, `ARCHITECTURAL_PRINCIPLES.md`, HISTORY e ROADMAP;
* cadeia arquitetural PE-02 a PE-17, GP-A22E, AC-01, GP-A23 e GP-PE-22;
* 44 arquivos Python de producao e 24 arquivos de teste;
* catalogo, configuracoes, politicas e modelo de Projeto em JSON;
* dados operacionais CSV/JSON, cuja mutabilidade exige governanca separada;
* acervo PAC certificado localmente, incluindo 328 Achados Governados;
* website institucional e identidade visual vigente;
* filme institucional final, legendas e fontes audiovisuais, ainda sem promocao e politica de retencao.

### 6.4 Patrimonio Certificado

Cinco artefatos receberam CERTIFICADO:

1. `docs/architecture/PE_05_PA01A_IMPLEMENTATION_AUDIT.md`;
2. `docs/architecture/PE_08_PA01B_POST_IMPLEMENTATION_AUDIT.md`;
3. `docs/architecture/PE_11_PA01C_POST_IMPLEMENTATION_AUDIT.md`;
4. `docs/architecture/PE_14_PA01D_POST_IMPLEMENTATION_AUDIT.md`;
5. `docs/pac/PAC_12A_FINAL_COLLECTION_AUDIT.md`.

Os quatro certificados PA-01 estao rastreados. A certificacao final do PAC permanece apenas local, situacao que nao invalida seu conteudo, mas impede reproducibilidade a partir do `HEAD`.

### 6.5 Patrimonio Ainda Local

Ha **173 arquivos nao rastreados**, totalizando **423.695.038 bytes**, equivalentes a **50% dos artefatos e 99,51% do volume fisico auditado**.

Tambem existem seis arquivos rastreados com modificacoes locais:

* `README.md`;
* `data/dados_ambientais_medicoes.csv`;
* `data/qualidade_agua_medicoes.csv`;
* `docs/history/HISTORY.md`;
* `docs/roadmap/ROADMAP.md`;
* `reports/relatorio_operacional.txt`.

### 6.6 Riscos Prioritarios

1. perda do acervo PAC e audiovisual por ausencia no controle de versao;
2. declaracoes de HISTORY e ROADMAP sem correspondencia integral no `HEAD`;
3. incorporacao acidental de 161 MB de ferramentas vendorizadas e 182 MB de temporarios;
4. mistura entre dados operacionais mutaveis e patrimonio versionado;
5. falta de politica de retencao, privacidade, licenciamento e armazenamento de midia;
6. divergencia entre manifestos audiovisuais e entregas agora existentes;
7. obsolescencia documental de README e partes do ROADMAP.

## 7. Inventario Do Acervo Por Conjunto

As classificacoes separadas por `+` indicam subconjuntos diferentes; cada arquivo individual recebe apenas uma delas, conforme o mapeamento exaustivo da secao 8.

| Conjunto | Qtde. | Rastreado/local | Classificacao | Finalidade | Responsavel logico | Maturidade e uso atual | Promocao/revisao | Riscos |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Raiz: `.gitignore`, README e requirements | 3 | 3/0 | SUPORTE | Entrada, dependencias e higiene do repositorio. | Engenharia do Projeto | README ativo, mas desatualizado; dependencia sem versao fixada. | Revisar README e reprodutibilidade. | Obsolescencia media; perda baixa. |
| Codigo Python de producao | 44 | 44/0 | OPERACIONAL | Runtime das camadas e interfaces. | Responsaveis logicos de cada camada | Maduro e ativo; 110 testes aprovados na GP-PE-22. | Nenhuma promocao pendente. | Perda baixa; acumulacao arquitetural sob vigilancia. |
| Suite `tests/` | 24 | 24/0 | SUPORTE | Regressao funcional e guardrails PA-01. | Engenharia/Qualidade | Madura, ativa e critica. | Manter sincronizada com novas GPs. | Obsolescencia media se novos arquivos escaparem das listas estaticas. |
| `data/` | 8 | 7/1 | OPERACIONAL | Medicoes, eventos, catalogo, configuracoes, politicas e Projeto. | Governanca de Dados/Operacao | Ativo; dois CSVs modificados e eventos apenas locais. | Exige politica antes de promover dados mutaveis. | Perda e contaminacao altas; duplicidade baixa. |
| `reports/` | 1 | 1/0 modificado | OPERACIONAL | Saida textual operacional. | Relatorios/Operacao | Gerado e em uso local. | Decidir se e evidencia, exemplo ou saida descartavel. | Obsolescencia alta; perda media. |
| `website/` | 18 | 18/0 | OPERACIONAL | Website institucional implementado. | Comunicacao Institucional/Web | Implementado e versionado. | Revisar conteudo contra baseline atual. | Obsolescencia media; perda baixa. |
| `assets/` | 2 | 2/0 | SUPORTE | Orientacoes para icones e logotipo. | Identidade Visual | Basico e ativo. | Consolidar com ativos efetivos quando aplicavel. | Lacuna de ativos no proprio diretorio; perda baixa. |
| `docs/adoption/` | 11 | 5/6 | SUPORTE | Adoção, contato, checklist e orientacao ao usuario. | Produto/Adoção | Parcialmente versionado; uso institucional potencial. | Revisar dados de contato, publico e coerencia antes de promocao. | Fragmentacao alta; obsolescencia media. |
| `docs/architecture/` | 23 | 22/1 | OFICIAL + CERTIFICADO | Autoridade arquitetural, auditorias e implementacoes governadas. | Governanca Arquitetural | Maduro; PE-22 ainda local. | PE-22 pode integrar o proximo pacote atomico de governanca. | Perda baixa no nucleo; media para PE-22 local. |
| `docs/branding/` | 6 | 6/0 | OFICIAL | Identidade visual e uso da marca. | Comunicacao/Identidade | Consolidado e versionado. | Revisao apenas por mudanca institucional. | Obsolescencia baixa. |
| `docs/domain/` | 15 | 14/1 | OFICIAL | Auditorias e consolidacao do dominio Projeto. | Governanca de Dominio | Maduro; GP-D01C local. | Revisar referencias e promover por GP propria. | Perda media para GP-D01C; duplicidade baixa. |
| `docs/governance/` | 2 | 1/1 | OFICIAL | Constituicoes do Projeto e PAC. | Governanca ICFACTORY/PAC | Constituicao do Projeto versionada; Constituicao PAC local. | PAC_CONSTITUTION deve acompanhar o acervo PAC. | Risco alto de autoridade local nao reproduzivel. |
| `docs/history/` | 1 | 1/0 modificado | OFICIAL | Memoria oficial das GPs. | Governanca do Projeto | Critico, amplo e localmente divergente do HEAD. | Exige reconciliacao antes de novo commit consolidado. | Risco alto de declarar artefato nao promovido. |
| `docs/institutional/` | 7 | 7/0 | OFICIAL | Apresentacao, limites e fluxo institucional. | Comunicacao Institucional | Versionado e em uso. | Revisar contra PA-01 e estado atual antes de divulgacao externa. | Obsolescencia media. |
| `docs/operational/` | 4 | 4/0 | OFICIAL | Fronteira e fluxo operacional da informacao. | Governanca Operacional | Consolidado e versionado. | Nenhuma promocao pendente. | Obsolescencia baixa. |
| `docs/pac/` | 15 | 0/15 | OFICIAL + CERTIFICADO | Achados, consolidacao, convergencias e plano de evolucao PAC. | Governanca PAC | Conteudo maduro e certificado localmente, mas ausente do HEAD. | Recomendada promocao atomica com PAC_CONSTITUTION. | Perda e reproducibilidade criticas. |
| `docs/presentation/` | 9 | 0/9 | OFICIAL | Roteiros, revisoes e planejamento audiovisual. | Comunicacao/Audiovisual | Maduro documentalmente, inteiramente local. | Consolidar com o estado real da midia antes de promocao. | Perda alta; obsolescencia media. |
| `docs/research/` | 6 | 4/2 | PESQUISA + EXPERIMENTAL | Investigacoes, catalogo e dossie metodologico. | Governanca de Pesquisa | R02/R03/R06 e consolidacao rastreados; catalogo e Harness locais. | Pesquisa local requer pacote proprio; R06 permanece experimental. | Promocao indevida e perda media. |
| `docs/roadmap/` | 1 | 1/0 modificado | OFICIAL | Estado e sequenciamento das GPs. | Governanca do Projeto | Critico, mas contem secoes historicas desatualizadas e adicoes locais. | Reconciliar com autoridades promovidas. | Obsolescencia e divergencia altas. |
| `docs/website/` | 9 | 9/0 | OFICIAL | Especificacao e conteudo do website. | Comunicacao Institucional/Web | Versionado. | Revisar paridade com `website/`. | Duplicidade semantica media; perda baixa. |
| Midia raiz: `SC001` a `SC012` e duas gravacoes datadas | 14 | 0/14 | EXPERIMENTAL + TEMPORÁRIO | Fontes brutas de captura audiovisual. | Producao Audiovisual | Nao promovido; 258 MB. | Manter SC001-SC012 experimentais; decidir descarte/retencao das duas capturas datadas. | Perda, privacidade e volume altos. |
| `media/.../analysis`, `captures` e `titles` | 34 | 0/34 | TEMPORÁRIO | Folhas de contato, capturas e cartelas derivadas. | Producao Audiovisual | Reconstruivel e local. | Nao promover em massa; selecionar apenas evidencia necessaria. | Duplicidade alta; volume e obsolescencia medios. |
| `media/.../audio/narration` | 19 | 0/19 | EXPERIMENTAL + SUPORTE | Narracao, guias e sincronizacao. | Producao Audiovisual | Textual; assembly cut ainda experimental. | Consolidar versao final e preservar fontes essenciais. | Duplicidade semantica e obsolescencia medias. |
| `media/.../exports` | 3 | 0/3 | OPERACIONAL + EXPERIMENTAL + TEMPORÁRIO | Filme final e arquivos intermediarios de montagem. | Producao Audiovisual | MP4 final existe; manifestos ainda alegam render bloqueado. | Revisar filme; nao promover arquivos de concat temporarios. | Inconsistencia documental alta. |
| `media/.../manifests` | 3 | 0/3 | EXPERIMENTAL + SUPORTE | Manifestos do animatic, assembly e filme. | Producao Audiovisual | Estruturado, mas parcialmente ultrapassado. | Revisar contra MP4 final e cenas reais. | Obsolescencia alta. |
| `media/.../project` | 8 | 0/8 | EXPERIMENTAL + SUPORTE | Guias e projeto Kdenlive. | Producao Audiovisual | Reproduzibilidade parcial; inteiramente local. | Preservar projeto editavel, revisar paths e fontes. | Perda alta; dependencia de ambiente. |
| `media/.../scripts` | 5 | 0/5 | SUPORTE | Captura, geracao e build audiovisual. | Engenharia Audiovisual | Auxiliar e nao versionado. | Revisar portabilidade e dependencias antes de promocao. | Perda media; obsolescencia media. |
| `media/.../subtitles` | 3 | 0/3 | OPERACIONAL + SUPORTE | Legenda final, provisoria e revisao. | Comunicacao/Audiovisual | Legenda final operacional, demais auxiliares. | Promover com entrega audiovisual aprovada. | Perda media; duplicidade semantica baixa. |
| `media/.../tools` | 47 | 0/47 | TEMPORÁRIO | OpenCV vendorizado, wheel, binarios e metadados. | Ferramentas Audiovisuais | Cache local reconstruivel; 161 MB. | Nao promover; documentar instalacao e ignorar binarios. | Poluicao de repositorio e seguranca de supply chain altas. |
| `media/.../README.md` | 1 | 0/1 | SUPORTE | Orientacao do pacote audiovisual. | Producao Audiovisual | Local. | Revisar e promover apenas com pacote consolidado. | Perda media. |

## 8. Mapeamento Exaustivo Da Classificacao Dos 346 Artefatos

As regras abaixo sao disjuntas pela ordem apresentada. Todo arquivo auditado corresponde a exatamente uma linha. Os padroes de diretorio aplicam a classificacao a cada arquivo individual contido no conjunto, sem classificacao multipla.

### 8.1 CERTIFICADO - 5

| Artefatos | Quantidade |
| --- | ---: |
| `docs/architecture/PE_05_PA01A_IMPLEMENTATION_AUDIT.md` | 1 |
| `docs/architecture/PE_08_PA01B_POST_IMPLEMENTATION_AUDIT.md` | 1 |
| `docs/architecture/PE_11_PA01C_POST_IMPLEMENTATION_AUDIT.md` | 1 |
| `docs/architecture/PE_14_PA01D_POST_IMPLEMENTATION_AUDIT.md` | 1 |
| `docs/pac/PAC_12A_FINAL_COLLECTION_AUDIT.md` | 1 |

### 8.2 EXPERIMENTAL - 31

| Artefatos | Quantidade |
| --- | ---: |
| `docs/research/GP_R06_AI_DECISION_GOVERNANCE_EXPERIMENTAL_RESEARCH.md` | 1 |
| `media/proteus_institutional_video/SC001.mp4` a `SC012.mp4` | 12 |
| `media/proteus_institutional_video/audio/narration/assembly_cut_v1/*` | 15 |
| `media/proteus_institutional_video/manifests/ANIMATIC_V1_MANIFEST.md` | 1 |
| `media/proteus_institutional_video/exports/assembly_cut_v1/assembly_cut_v1.ffconcat` | 1 |
| `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive` | 1 |

### 8.3 TEMPORÁRIO - 84

| Artefatos | Quantidade |
| --- | ---: |
| Duas gravacoes MP4 com nome de data/hora na raiz de `media/proteus_institutional_video/` | 2 |
| `media/proteus_institutional_video/analysis/contact_sheets/*` | 19 |
| `media/proteus_institutional_video/captures/**/*` | 12 |
| `media/proteus_institutional_video/titles/*` | 3 |
| `media/proteus_institutional_video/exports/final/institutional_film_v1_concat.txt` | 1 |
| `media/proteus_institutional_video/tools/**/*` | 47 |

### 8.4 PESQUISA - 5

| Artefatos | Quantidade |
| --- | ---: |
| `docs/research/AI_METHODOLOGICAL_OBSERVATIONS_CONSOLIDATION.md` | 1 |
| `docs/research/DISCOVERY_CATALOG.md` | 1 |
| `docs/research/GP_R02_VALUE_PROGRESSION_AUDIT.md` | 1 |
| `docs/research/GP_R03_EXECUTIVE_CONTEXT_AUDIT.md` | 1 |
| `docs/research/HARNESS_GOVERNANCE_RESEARCH_DOSSIER.md` | 1 |

### 8.5 OFICIAL - 87

| Artefatos | Quantidade |
| --- | ---: |
| `docs/architecture/*`, exceto os quatro certificados listados | 19 |
| `docs/branding/*` | 6 |
| `docs/domain/*` | 15 |
| `docs/governance/*` | 2 |
| `docs/history/HISTORY.md` | 1 |
| `docs/institutional/*` | 7 |
| `docs/operational/*` | 4 |
| `docs/pac/*`, exceto `PAC_12A_FINAL_COLLECTION_AUDIT.md` | 14 |
| `docs/presentation/*` | 9 |
| `docs/roadmap/ROADMAP.md` | 1 |
| `docs/website/*` | 9 |

### 8.6 OPERACIONAL - 73

| Artefatos | Quantidade |
| --- | ---: |
| Arquivos Python de producao na raiz e em `analytics/`, `executive/`, `executive_recommendation/`, `governance/` e `monitoramento_hidrico/` | 44 |
| `data/*` | 8 |
| `reports/relatorio_operacional.txt` | 1 |
| `website/**/*` | 18 |
| `media/proteus_institutional_video/exports/final/PROTEUS_INSTITUTIONAL_FILM_V1.mp4` | 1 |
| `media/proteus_institutional_video/subtitles/proteus_institutional_film_v1_pt-BR.srt` | 1 |

### 8.7 SUPORTE - 61

| Artefatos | Quantidade |
| --- | ---: |
| `.gitignore` | 1 |
| `README.md` | 1 |
| `requirements.txt` | 1 |
| `assets/*` | 2 |
| `tests/*` | 24 |
| `docs/adoption/*` | 11 |
| `media/proteus_institutional_video/README.md` | 1 |
| Quatro arquivos de narracao fora de `assembly_cut_v1/` | 4 |
| Dois manifestos nao experimentais em `media/.../manifests/` | 2 |
| Sete guias Markdown em `media/.../project/` | 7 |
| `media/proteus_institutional_video/scripts/*` | 5 |
| Dois artefatos de legenda/revisao diferentes da legenda final | 2 |

### 8.8 OBSOLETO - 0

Nenhum arquivo foi declarado OBSOLETO. Existem conteudos desatualizados, mas a auditoria nao encontrou autoridade formal que autorizasse considerar o arquivo inteiro substituido e sem uso. A obsolescencia foi registrada como risco ou necessidade de revisao, nao inferida como classificacao definitiva.

### 8.9 Reconciliacao

```text
OFICIAL 87 + CERTIFICADO 5 + OPERACIONAL 73 + SUPORTE 61
+ PESQUISA 5 + EXPERIMENTAL 31 + TEMPORÁRIO 84 + OBSOLETO 0
= 346 artefatos
```

## 9. Duplicidades Identificadas

A comparacao SHA-256 encontrou quatro grupos de conteudo binariamente identico, envolvendo 13 arquivos:

| Grupo | Arquivos | Avaliacao |
| --- | ---: | --- |
| Sete PNGs de abertura, encerramento e cartelas com o mesmo hash | 7 | Duplicidade material de temporarios; selecionar fonte canonica se houver promocao. |
| `LICENSE-3RD-PARTY.txt` duplicado entre pacote `cv2` e metadados da distribuicao | 2 | Duplicidade esperada de dependencia vendorizada. |
| `LICENSE.txt` duplicado entre pacote `cv2` e metadados da distribuicao | 2 | Duplicidade esperada de dependencia vendorizada. |
| `website/assets/logo/favicon.png` e `proteus-symbol.png` | 2 | Duplicidade intencional possivel, mas nomes sugerem papeis distintos; documentar derivacao. |

Duplicidades semanticas adicionais:

* HISTORY, ROADMAP e README repetem estados de GPs em niveis diferentes e nem sempre sincronizados;
* documentacao de website duplica parte do conteudo materializado em HTML;
* narracoes master, finais, segmentadas e de assembly preservam versoes sobrepostas;
* manifesto do filme preparado para renderizacao coexiste com MP4 final agora presente;
* capturas e titles usam imagens identicas sob nomes narrativos diferentes.

## 10. Lacunas Identificadas

| ID | Lacuna | Impacto |
| --- | --- | --- |
| L-01 | Nao existe manifesto patrimonial versionado com path, classificacao, hash, dono e estado de promocao. | Alto |
| L-02 | Nao existe politica explicita para versionamento de dados operacionais mutaveis. | Alto |
| L-03 | Nao existe politica de retencao, privacidade, licenciamento e armazenamento para videos brutos e finais. | Alto |
| L-04 | Nao existe estrategia declarada para arquivos binarios grandes, como Git LFS ou repositorio externo de evidencias. | Alto |
| L-05 | Ferramentas OpenCV foram vendorizadas localmente sem lockfile, origem verificavel no repositorio ou politica de descarte. | Alto |
| L-06 | README e secoes do ROADMAP nao representam integralmente o estado atual. | Medio/Alto |
| L-07 | Manifestos PI-05 ainda declaram MP4 bloqueado, embora um MP4 final esteja presente localmente. | Medio/Alto |
| L-08 | Constituicao do Projeto permanece como rascunho inicial e PAC_CONSTITUTION permanece local. | Medio |
| L-09 | Nao existe CI versionada nem versao fixada para PyQt5. | Medio |
| L-10 | `assets/` contem orientacoes, mas os ativos efetivos de marca estao em `website/assets/logo/` e na midia. | Medio |
| L-11 | Nao existe indicacao uniforme de responsavel logico, validade ou supersessao dentro dos documentos. | Medio |
| L-12 | Nao existe backup ou checksum institucional do acervo local de 423,7 MB. | Alto |

## 11. Analise De Riscos

| ID | Risco | Probabilidade | Impacto | Prioridade | Mitigacao recomendada |
| --- | --- | --- | --- | --- | --- |
| R-01 | Perda dos 173 artefatos locais. | Media/Alta | Alto | Critica | Promocao seletiva, backup e manifesto de checksums por GP propria. |
| R-02 | Tratar HISTORY/ROADMAP local como prova de artefatos ausentes do HEAD. | Alta | Alto | Critica | Reconciliar Autoridade -> HISTORY -> ROADMAP -> README. |
| R-03 | Incorporacao acidental de temporarios e dependencias vendorizadas. | Media | Alto | Alta | Atualizar politica de ignore e documentar reconstrucao em GP autorizada. |
| R-04 | Exposicao indevida em gravacoes de tela ou midia. | Desconhecida | Alto | Alta | Revisao de privacidade e aprovacao humana antes de promocao/publicacao. |
| R-05 | Perda de reproducibilidade audiovisual por fontes e projeto local. | Media | Alto | Alta | Preservar fontes essenciais e projeto editavel em armazenamento adequado. |
| R-06 | Dados demonstrativos ou operacionais serem confundidos com baseline imutavel. | Alta | Medio/Alto | Alta | Separar fixture, demonstracao, dado operacional e evidencia. |
| R-07 | Documentos desatualizados orientarem GPs futuras. | Alta | Medio/Alto | Alta | Curadoria documental antes de qualquer iniciativa da Onda B. |
| R-08 | Promocao indevida de pesquisa ou GP-R06 como norma. | Baixa/Media | Alto | Media | Manter classificacoes PESQUISA/EXPERIMENTAL e autoridade explicita. |
| R-09 | Duplicidades aumentarem custo e divergirem. | Media | Medio | Media | Fonte canonica por familia e politica de derivacao. |
| R-10 | Dependencias binarias locais introduzirem risco de supply chain. | Media | Alto | Alta | Nao promover binarios; reconstruir de fonte e versao verificadas. |

## 12. Patrimonio Considerado Critico

### 12.1 Critico E Reproduzivel

* codigo de producao e testes versionados;
* cadeia PA-01 versionada, incluindo os quatro certificados de implementacao;
* `ARCHITECTURAL_PRINCIPLES.md`;
* GP-A22E e suas evidencias de rastreabilidade;
* Constituicao do Projeto, HISTORY e ROADMAP no estado do `HEAD`;
* catalogo, configuracoes, politicas e Projeto JSON rastreados;
* website e documentos institucionais rastreados.

### 12.2 Critico Mas Ainda Local Ou Modificado

* GP-PE-22 e este relatorio GP-PE-23;
* acervo PAC completo e PAC_CONSTITUTION;
* GP-D01C;
* HISTORY e ROADMAP ampliados localmente;
* `eventos_operacionais.json`;
* dados e relatorio operacional modificados;
* material de adocao ainda local;
* roteiro, projeto editavel, fontes e filme institucional final;
* Discovery Catalog e dossie de Harnesses.

## 13. Patrimonio Ainda Nao Promovido

Distribuicao dos 173 arquivos locais:

| Categoria | Quantidade local |
| --- | ---: |
| OFICIAL | 26 |
| CERTIFICADO | 1 |
| OPERACIONAL | 3 |
| SUPORTE | 27 |
| PESQUISA | 2 |
| EXPERIMENTAL | 30 |
| TEMPORÁRIO | 84 |
| OBSOLETO | 0 |

Os 173 locais nao devem ser promovidos em um unico commit. Eles representam naturezas, riscos, destinos e politicas de retencao diferentes.

## 14. Patrimonio Recomendado Para Promocao

### 14.1 Promocao Imediata Recomendada Em Pacote Arquitetural

* `docs/architecture/PE_22_WAVE_B_ELIGIBILITY_AUDIT.md`;
* `docs/architecture/PE_23_TECHNICAL_ASSET_INVENTORY.md`;
* apenas os registros correspondentes de HISTORY e ROADMAP.

Condicao: diff limpo quanto a whitespace, conferência das contagens e commit atomico sem absorver as demais modificacoes locais.

### 14.2 Promocao Atomica Recomendada Para O PAC

Conjunto elegivel, mas separado do pacote arquitetural:

* 15 arquivos de `docs/pac/`;
* `docs/governance/PAC_CONSTITUTION.md`.

Condicoes: repetir mecanicamente o checklist da GP-PAC-12A no estado atual, confirmar todas as referencias e promover os 16 arquivos juntos. Nenhum documento PAC deve ser promovido isoladamente.

### 14.3 Promocao Apos Revisao

* `docs/domain/GP_D01C_PERSISTENCE_STRATEGY_AUDIT.md`;
* seis documentos locais de adocao;
* nove documentos de apresentacao;
* `DISCOVERY_CATALOG.md` e `HARNESS_GOVERNANCE_RESEARCH_DOSSIER.md` em pacote de pesquisa;
* scripts e guias audiovisuais indispensaveis a reproducao;
* filme final e legenda final, desde que aprovados por privacidade, licenca, codec e destino de armazenamento.

### 14.4 Nao Recomendada Para Promocao Direta

* 84 temporarios;
* duas gravacoes datadas sem identificador de cena;
* ferramentas OpenCV vendorizadas e wheel local;
* arquivos de concat intermediarios;
* dados operacionais mutaveis sem politica;
* relatorio gerado sem decisao de retencao;
* capturas e folhas de contato em massa.

## 15. CONDIÇÕES PARA PROMOÇÃO DO ACERVO

### 15.1 Conjuntos Que Podem Ser Promovidos Imediatamente

1. GP-PE-22 e GP-PE-23, com registros minimos correspondentes em HISTORY e ROADMAP.
2. Acervo PAC de 16 arquivos como pacote separado e atomico, apos repeticao mecanica de sua verificacao de integridade.

"Imediatamente" significa apto a uma GP/commit proprio; nao significa promocao executada por esta auditoria.

### 15.2 Conjuntos Que Exigem Revisao

* README, ROADMAP e documentos institucionais com estado historico ultrapassado;
* GP-D01C e suas referencias de dominio/persistencia;
* documentos de adocao e contato;
* documentos e manifestos audiovisuais;
* filme e legendas finais;
* website versus sua documentacao de origem;
* dados e relatorio operacional modificados.

### 15.3 Conjuntos Que Exigem Consolidacao

* HISTORY, ROADMAP e README, preservando a sequencia de autoridade;
* roteiro, narracao, legenda, manifestos, projeto editavel, scripts e entrega final audiovisual;
* Discovery Catalog e dossie de Harnesses como pacote de pesquisa separado;
* identidade visual distribuida entre `assets/`, `website/assets/logo/` e midia;
* dados CSV/JSON, fixtures e evidencias operacionais sob politica unica.

### 15.4 Conjuntos Que Devem Permanecer Experimentais

Os 31 artefatos classificados como EXPERIMENTAL:

* GP-R06;
* SC001 a SC012;
* 15 arquivos de narracao do assembly cut;
* manifesto do Animatic V1;
* lista FFmpeg do assembly cut;
* projeto Kdenlive do assembly cut.

Podem mudar de classificacao somente por revisao e decisao formal posterior. GP-R06 permanece experimental e nao normativa independentemente de seu estado Git.

### 15.5 Conjuntos Que Devem Permanecer Fora Do Patrimonio Promovido

Os 84 temporarios devem permanecer reconstruiveis ou descartaveis. Se algum for necessario como evidencia, devera ser reclassificado individualmente por decisao formal antes de promocao.

## 16. Recomendacoes

1. Nao abrir uma promocao massiva dos 173 arquivos locais.
2. Promover primeiro o pacote arquitetural GP-PE-22/23.
3. Promover o PAC apenas como conjunto atomico de 16 arquivos.
4. Criar, em GP posterior, manifesto patrimonial versionado com path, classificacao, hash, tamanho, responsavel logico e estado.
5. Definir politica para dados operacionais, fixtures, relatorios gerados e evidencias.
6. Definir politica de midia: privacidade, licenca, retencao, backup, checksums e armazenamento de binarios grandes.
7. Nao versionar a arvore `media/.../tools/`; documentar instalacao reproduzivel.
8. Reconciliar manifestos audiovisuais com a existencia do filme final.
9. Atualizar README e secoes correntes do ROADMAP somente por curadoria governada, sem reescrever historia.
10. Preservar PESQUISA e EXPERIMENTAL sem promocao normativa.

## 17. Conclusao

O PROTEUS possui patrimonio tecnico amplo, identificavel e majoritariamente coerente por conjunto. A autoridade arquitetural da Onda A, o runtime, os testes, o website e parte substancial da governanca estao versionados e reproduziveis.

O acervo completo, entretanto, nao esta consolidado como patrimonio oficial unico. Exatamente metade dos arquivos permanece fora do controle de versao; esses arquivos concentram 99,51% do volume fisico, todo o acervo PAC local, a maior parte da producao audiovisual, materiais de adocao, pesquisa local, dados e ferramentas temporarias. HISTORY e ROADMAP descrevem parte desse material sem que os artefatos correspondentes estejam no `HEAD`.

A fragmentacao e controlavel porque os conjuntos foram identificados, classificados e receberam condicoes distintas de promocao. Ela nao autoriza promocao em massa, nao reduz pesquisa a norma e nao transforma temporarios em patrimonio permanente.

## 18. Veredito Final

# ACERVO FRAGMENTADO

Fundamentacao:

* 173 de 346 artefatos permanecem locais;
* 423.695.038 bytes, ou 99,51% do volume, nao sao reproduziveis pelo `HEAD`;
* um dos cinco certificados, todo o conjunto PAC e todos os documentos de apresentacao permanecem locais;
* 84 temporarios e 30 experimentais locais nao podem ser promovidos junto com autoridades;
* documentos correntes e manifestos apresentam divergencias de estado;
* nao existe politica unica de dados, midia, retencao, checksums ou binarios grandes.

Decisao formal: o patrimonio tecnico do PROTEUS e real, extenso e classificavel, mas permanece **ACERVO FRAGMENTADO** ate que os pacotes recomendados sejam promovidos separadamente e os conjuntos sujeitos a revisao, consolidacao ou permanencia experimental recebam tratamento proprio.

Esta decisao nao reabre a Onda A, nao inicia a Onda B e nao autoriza qualquer promocao automatica.

## 19. Restricoes Preservadas

* Nenhum codigo-fonte alterado.
* Nenhuma funcionalidade implementada.
* Nenhuma arquitetura modificada.
* Nenhum arquivo movido, excluido ou renomeado.
* Nenhum artefato promovido.
* Nenhum dado ou midia alterado.
* Nenhuma pesquisa ou Discovery promovida.
* ICFACTORY integralmente preservado.
* Onda B nao iniciada.

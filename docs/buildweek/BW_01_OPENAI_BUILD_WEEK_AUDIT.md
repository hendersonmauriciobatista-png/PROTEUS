# BW-01 — Auditoria de Elegibilidade OpenAI Build Week

## 1. Identificação da GP

| Campo | Valor |
|---|---|
| Identificador | GP-BW-01 |
| Projeto | PROTEUS — Sistema de Análise de Água |
| Natureza | auditoria documental e técnica, sem alteração funcional |
| Data da auditoria | 18/07/2026 |
| Prazo oficial de submissão | 21/07/2026, 17:00 Pacific Time |
| Veredito | **NÃO APTO NO ESTADO ATUAL** |

## 2. Objetivo

Determinar, com evidências verificáveis, a aptidão atual do PROTEUS para submissão à OpenAI Build Week e identificar bloqueios, riscos e ações necessárias, sem implementar funcionalidades, publicar materiais, aceitar termos ou efetuar submissão.

## 3. Escopo

Foram analisados as páginas oficiais, as Official Rules, o fluxo oficial de submissão, requisitos e critérios, além do README, documentação, histórico Git, evolução no período, testes, instruções de uso, licença, mídia, remoto, dados e padrões de exposição sensível do repositório local.

Não foram realizados: alteração de código, arquitetura, dados, testes ou interface; execução de commit/push; publicação; aceite de termos; criação de conta; submissão.

## 4. Fontes oficiais utilizadas

O registro detalhado está em [BW_01_SOURCE_REGISTER.md](BW_01_SOURCE_REGISTER.md). As fontes principais são:

1. OpenAI Build Week — https://openai.com/build-week/
2. Devpost Overview — https://openai.devpost.com/
3. Official Rules — https://openai.devpost.com/rules
4. Schedule — https://openai.devpost.com/details/dates
5. Resources — https://openai.devpost.com/resources
6. Update/checklist oficial — https://openai.devpost.com/updates/45362-openai-build-week-halfway-there-where-are-you

## 5. Resumo executivo

O PROTEUS **não está apto no estado atual** por dois grupos independentes de bloqueios:

1. **Territorial/jurídico:** as Official Rules excluem expressamente indivíduos residentes e organizações domiciliadas no Brasil. A residência ou o domicílio do entrante efetivo não foi fornecido e não é inferido nesta auditoria. Para o cenário solicitado — submissão por participante residente no Brasil — a resposta normativa é negativa. Um representante meramente nominal não sana a inelegibilidade.
2. **Pacote de submissão:** mesmo sob a hipótese de um entrante genuinamente elegível, faltam evidência verificável de GPT-5.6/Codex no período, delimitação do trabalho novo, `/feedback` Codex Session ID, descrição/categoria, vídeo público com áudio, acesso comprovado ao repositório, README específico, inglês/tradução, acesso gratuito de teste e decisões de propriedade/licença.

Há base técnica relevante: 110 testes passaram; existem instruções de execução; e o Git registra 10 commits após o início do período, com 57 arquivos alterados, 8.965 inserções e 181 remoções em relação ao último commit anterior. Essa evolução não prova, isoladamente, que Codex ou GPT-5.6 foi usado, nem distingue adequadamente o que será julgado.

## 6. Requisitos obrigatórios

- entrante elegível, maior de idade, em território permitido e sem conflito proibido;
- equipe/organização com representante autorizado e também elegível;
- projeto construído com Codex e GPT-5.6 em uma das quatro categorias;
- projeto instalável, executável e coerente com a demonstração;
- para projeto preexistente: extensão significativa após 13/07/2026 e documentação que separe trabalho anterior e novo, com evidência datada de Codex/GPT-5.6;
- descrição do projeto e categoria;
- demonstração com menos de 3 minutos, áudio sobre o que foi construído e como Codex e GPT-5.6 foram usados, publicada de modo público no YouTube;
- URL de repositório público com licença relevante ou privado compartilhado com `testing@devpost.com` e `build-week-event@openai.com`;
- README que registre colaboração com Codex, aceleração, decisões e contribuição de GPT-5.6/Codex, além de instruções claras;
- `/feedback` Codex Session ID da thread em que a maioria da funcionalidade central foi construída;
- acesso gratuito e irrestrito ao projeto para julgamento até o fim do período de avaliação;
- materiais em inglês ou com tradução em inglês;
- trabalho original, de titularidade do entrante, sem violação de PI, privacidade, marca ou licença;
- submissão completa até 21/07/2026 às 17:00 PT.

## 7. Requisitos recomendados

- manter o repositório limpo, testável e com dados de exemplo;
- começar pela clareza do problema e do público real;
- explicitar por que GPT-5.6 é adequado ao problema;
- gravar e revisar a demo antecipadamente;
- oferecer método simples de teste, sem reconstrução desnecessária;
- alinhar texto, vídeo e comportamento observado;
- preparar narrativa de impacto e diferenciação sem extrapolar evidências.

## 8. Critérios de avaliação

O Stage One é eliminatório e verifica adequação ao tema e aplicação razoável das ferramentas/APIs/SDKs exigidas. No Stage Two, quatro critérios têm peso igual:

1. **Implementação tecnológica:** uso profundo e hábil de Codex; esforço genuíno; implementação funcional e não trivial.
2. **Design:** experiência completa, coerente e executável, não apenas prova de conceito.
3. **Impacto potencial:** problema real, público real e solução demonstrada de forma crível.
4. **Qualidade da ideia:** criatividade, novidade e diferenciação.

## 9. Condições de elegibilidade

### 9.1 Brasil

As Official Rules, §3, incluem o Brasil na lista expressa de territórios proibidos. Portanto:

- pessoa residente no Brasil: **não elegível**;
- organização domiciliada no Brasil: **não elegível**;
- equipe/organização: deve nomear representante autorizado que satisfaça os requisitos, mas isso não autoriza representação fictícia ou transferência nominal para contornar a regra;
- situação do entrante real: **não verificada**, pois identidade, idade, residência, vínculo e modalidade não foram apresentados.

### 9.2 Outros controles humanos

Devem ser confirmados idade de maioridade, país suportado pela API, ausência de vínculo proibido com Sponsor/Administrator, ausência de apoio financeiro/preferencial vedado e autoridade do representante.

## 10. Regras para projetos preexistentes

O PROTEUS pode, em tese, concorrer como projeto preexistente, mas somente o trabalho novo é avaliado. As regras exigem extensão significativa com Codex e/ou GPT-5.6 após 13/07/2026 09:00 PT e documentação clara que distinga baseline e novo trabalho.

Evidência local favorável:

- base anterior ao período: `ec7f83cfa94973cdbe1d50acd157f8e4383c4740`;
- 10 commits após a abertura do período;
- 57 arquivos alterados, 8.965 inserções e 181 remoções;
- commits funcionais/de teste incluem `d153b7a`, `a1dc51a` e `1b75536`.

Limitação: mensagens de commit e documentos genéricos sobre Codex não demonstram que Codex/GPT-5.6 produziu a extensão elegível. Também não existe um changelog Build Week que separe baseline, mudança, sessão e commit.

## 11. Exigências relativas ao GPT-5.6 e ao Codex

- O projeto deve ser construído com **Codex usando GPT-5.6**.
- O vídeo deve explicar como ambos foram usados.
- O README deve descrever colaboração, aceleração, decisões e contribuição de ambos.
- Projeto preexistente deve provar uso no período por logs timestampados, commits datados ou equivalente.
- Deve ser fornecido o `/feedback` Session ID da thread central.

O PROTEUS declara no README uma arquitetura determinística e sem dependência de IA generativa. Isso não é, por si só, proibido: as regras não formulam uma exigência autônoma e inequívoca de que a aplicação use a OpenAI API em runtime. Contudo, o uso de Codex/GPT-5.6 na construção é obrigatório e o Stage One menciona as APIs/SDKs exigidas. A ausência total de narrativa/evidência específica cria risco eliminatório e não pode ser suprida por inferência.

## 12. Exigências relativas ao vídeo

- menos de 3 minutos;
- demonstração clara e funcional;
- áudio explicando o que foi construído e como Codex e GPT-5.6 foram usados;
- público no YouTube;
- sem marcas, música ou material protegido de terceiros sem permissão.

Há um render local de 111,966667 segundos, H.264, 1920×1080, 30 fps. Sua duração se enquadra, mas a documentação registra ausência de áudio, finalidade institucional e ausência de publicação. Logo, ele não é uma demonstração Build Week conforme.

## 13. Exigências relativas ao repositório e README

O remoto configurado é `https://github.com/hendersonmauriciobatista-png/sistema-analise-agua.git`. Uma consulta pública não autenticada retornou 404, o que pode significar privado ou inexistente; a visibilidade não foi confirmada. Não há evidência de compartilhamento com os dois e-mails oficiais.

O repositório local contém README, Quick Start e User Guide. O Quick Start cobre ambiente, instalação e execução, e 110 testes passaram. Porém:

- o README principal não consolida setup, dados de exemplo e teste para os juízes;
- não há seção Build Week, GPT-5.6, colaboração Codex ou decisões-chave;
- não há licença de primeiro nível;
- a árvore está suja, com modificações e muitos arquivos não rastreados;
- os ativos de mídia locais não aparecem no conjunto rastreado por Git.

## 14. Licenciamento, propriedade intelectual e direitos concedidos

Não existe `LICENSE`, `COPYING` ou `NOTICE` de primeiro nível. Foram encontrados apenas arquivos de licença do OpenCV dentro de ferramentas audiovisuais locais e não rastreadas. A dependência declarada `PyQt5`, os dados, a marca, as contribuições, o audiovisual e os demais componentes ainda exigem revisão humana de titularidade e licença.

As regras mantêm a PI com o autor, mas concedem ao Sponsor licença não exclusiva para julgamento. Também autorizam promoção da submissão e uso de nome, imagem, voz e semelhança dos contribuidores durante o evento e por três anos; a cláusula de publicidade prevê uso mundial, em mídias existentes ou futuras, sem pagamento ou revisão, salvo proibição legal. Aceitar essas condições é decisão humana/jurídica.

## 15. Prazos, formato, categorias e prêmios

- registro: 09/07/2026 10:00 PT a 21/07/2026 17:00 PT;
- submissão: 13/07/2026 09:00 PT a 21/07/2026 17:00 PT;
- vencedor anunciado por volta de 12/08/2026 14:00 PT;
- categorias: Apps for Your Life, Work and Productivity, Developer Tools e Education;
- prêmio total anunciado: US$ 100.000, com primeiro e segundo lugar em cada categoria.

`Work and Productivity` parece a categoria mais próxima do PROTEUS, mas é recomendação preliminar sujeita à decisão do entrante. Há divergência oficial sobre o fim do julgamento; as Official Rules prevalecem e indicam 05/08/2026 17:00 PT.

## 16. Evidências existentes no PROTEUS

- aplicação Python/PyQt5 com organização modular e documentação extensa;
- README, Quick Start e User Guide;
- 110 testes executados com resultado `OK` em 18/07/2026;
- histórico Git com evolução após a abertura do período;
- dados de exemplo versionados em CSV/JSON;
- vídeo local com duração inferior a 3 minutos;
- documentos que registram uso recorrente de Codex em atividades de governança/pesquisa;
- varredura nominal e por padrões sem arquivo de segredo ou credencial identificado;
- CSVs inspecionados têm medições ambientais/hídricas e não exibiram campos pessoais nas amostras verificadas.

## 17. Evidências ausentes

- elegibilidade, idade, residência/domicílio e autoridade do entrante;
- registro/rascunho Devpost;
- mapa de trabalho anterior versus novo;
- logs Codex e prova GPT-5.6 no período;
- `/feedback` Session ID;
- categoria e descrição final;
- vídeo Build Week com áudio e URL pública;
- acesso válido ao repositório para os juízes;
- licença relevante ou prova de compartilhamento privado;
- README específico em inglês;
- teste independente da GUI congelada;
- declaração de autoria, direitos e licenças;
- aceite humano informado dos termos e direitos de publicidade.

## 18. Segurança e exposição

### Método

Foram pesquisados, sem imprimir valores: nomes típicos de credenciais; extensões de chaves; padrões de token/API key/senha/segredo; caminhos locais; arquivos temporários rastreados; cabeçalhos e amostras de dados.

### Resultado

- nenhum segredo ou credencial foi detectado pelos padrões aplicados;
- nenhum arquivo temporário típico foi encontrado no conjunto rastreado;
- quatro arquivos locais de mídia/projeto contêm caminhos absolutos ou marcadores de ambiente local; esses arquivos estão sob `media/`, atualmente não rastreada;
- não foram observados campos pessoais nas amostras dos CSVs principais;
- existem muitos documentos e ativos não rastreados, alguns declarados internos ou não autorizados para publicação; o pacote exato precisa de revisão humana antes de qualquer compartilhamento.

Conclusão: não há segredo detectado que obrigue suspensão imediata, mas a varredura é baseada em padrões e não prova ausência absoluta. A publicação continua bloqueada até revisão do pacote congelado.

## 19. Riscos, lacunas e dependências

### Riscos bloqueantes

1. inelegibilidade de entrante residente/domiciliado no Brasil;
2. ausência de prova sobre o entrante real;
3. ausência de evidência específica de GPT-5.6/Codex no período;
4. ausência de Session ID;
5. vídeo não conforme e não publicado;
6. repositório inacessível/não compartilhado e sem licença de primeiro nível;
7. titularidade, permissões e direitos de publicidade não decididos;
8. árvore local não congelada e com materiais internos/não rastreados;
9. materiais de submissão sem inglês/tradução;
10. prazo curto e sem rascunho de submissão comprovado.

### Dependências

As adequações dependem primeiro de uma decisão humana verdadeira sobre elegibilidade. Depois, dependem do autor da implementação para sessões/logs, do titular para PI/licença, do responsável técnico para pacote testável e do entrante para vídeo, publicação, termos e submissão.

## 20. Matriz de conformidade

Legenda de fontes: F-01 a F-06 conforme [registro de fontes](BW_01_SOURCE_REGISTER.md).

| ID | Requisito | Fonte oficial | Obrigatoriedade | Evidência no PROTEUS | Status | Lacuna | Ação necessária | Criticidade |
|---|---|---|---|---|---|---|---|---|
| BW-EL-01 | Maioridade do entrante | F-03 §3 | Obrigatório | nenhuma | NÃO VERIFICADO | idade/identidade ausentes | BW-A01 | BLOQUEANTE |
| BW-EL-02 | Residência/domicílio elegível | F-03 §3 | Obrigatório | cenário Brasil solicitado; entrante real não identificado | NÃO CONFORME | Brasil é expressamente excluído | BW-A01/A02 | BLOQUEANTE |
| BW-EL-03 | Representante elegível e autorizado | F-03 §3/Submission | Condicional | nenhuma | NÃO VERIFICADO | modalidade/vínculo ausentes | BW-A01/A02 | BLOQUEANTE |
| BW-EL-04 | Ausência de conflito/apoio vedado | F-03 §§3–4 | Obrigatório | nenhuma declaração | NÃO VERIFICADO | conflito não avaliado pelo titular | BW-A03/A04 | ALTA |
| BW-PR-01 | Extensão significativa após 13/07 | F-03 §4 | Obrigatório para preexistente | 10 commits; 57 arquivos; mudanças funcionais/testes | CONFORME COM RESSALVA | uso das ferramentas não provado | BW-A05/A07 | BLOQUEANTE |
| BW-PR-02 | Separar baseline e trabalho novo | F-03 §4 | Obrigatório | Git permite reconstrução, sem documento específico | NÃO CONFORME | delimitação ausente | BW-A05 | BLOQUEANTE |
| BW-PR-03 | Evidência datada de Codex/GPT-5.6 | F-03 §4 | Obrigatório | commits datados; sem logs GPT-5.6/Codex vinculados | NÃO CONFORME | prova causal ausente | BW-A06/A07 | BLOQUEANTE |
| BW-TL-01 | Construído com Codex e GPT-5.6 | F-02/F-03 §4 | Obrigatório | referências genéricas a Codex; nenhuma a GPT-5.6 | NÃO CONFORME | uso exigido não demonstrado | BW-A07 | BLOQUEANTE |
| BW-TL-02 | OpenAI API em runtime | F-03 §§4/7 | Não estabelecido autonomamente | README declara ausência de IA generativa | NÃO APLICÁVEL | Stage One ainda exige ferramentas aplicáveis | documentar interpretação verdadeira | MÉDIA |
| BW-FN-01 | Instalar e executar consistentemente | F-03 §4 | Obrigatório | Quick Start; 110 testes OK | CONFORME COM RESSALVA | GUI não validada nesta auditoria | BW-A16/A17 | ALTA |
| BW-FN-02 | Comportamento igual ao texto/vídeo | F-03 §4 | Obrigatório | sem vídeo/descrição Build Week | NÃO CONFORME | comparação impossível | BW-A14/A23 | BLOQUEANTE |
| BW-SU-01 | Registro e campos obrigatórios | F-03 §§1/4 | Obrigatório | nenhuma evidência | NÃO VERIFICADO | rascunho/conta fora do escopo | BW-A19 | BLOQUEANTE |
| BW-SU-02 | Categoria selecionada | F-02/F-03 §4 | Obrigatório | Work and Productivity é hipótese | NÃO CONFORME | decisão do entrante ausente | BW-A08 | ALTA |
| BW-SU-03 | Descrição de funcionalidades | F-02/F-03 §4 | Obrigatório | README institucional não é descrição final | NÃO CONFORME | texto de submissão ausente | BW-A09 | BLOQUEANTE |
| BW-VD-01 | Vídeo com menos de 3 minutos | F-02/F-03 §4 | Obrigatório | render local de 111,966667 s | CONFORME | duração compatível | ainda validar corte final | ALTA |
| BW-VD-02 | Demo com áudio sobre Codex e GPT-5.6 | F-02/F-03 §4 | Obrigatório | render é silencioso e institucional | NÃO CONFORME | conteúdo/áudio ausentes | BW-A14 | BLOQUEANTE |
| BW-VD-03 | Vídeo público no YouTube | F-02/F-03 §4 | Obrigatório | nenhuma URL | NÃO CONFORME | publicação ausente | BW-A15 | BLOQUEANTE |
| BW-VD-04 | Direitos de marcas/música/materiais | F-03 §4 | Obrigatório | documentação evita áudio não licenciado | NÃO VERIFICADO | autorizações completas ausentes | BW-A04/A14 | BLOQUEANTE |
| BW-RP-01 | URL acessível para julgamento | F-02/F-03 §4 | Obrigatório | remote existe; API pública retorna 404 | NÃO CONFORME | acesso não comprovado | BW-A11/A12 | BLOQUEANTE |
| BW-RP-02 | Público com licença ou privado compartilhado | F-02/F-03 §4 | Obrigatório | sem licença raiz e sem prova de compartilhamento | NÃO CONFORME | opção não satisfeita | BW-A11/A13 | BLOQUEANTE |
| BW-RP-03 | README com setup, execução e dados | F-02/F-05 | Obrigatório operacional | Quick Start separado e dados versionados | CONFORME COM RESSALVA | README não consolida experiência do juiz | BW-A10 | ALTA |
| BW-RP-04 | README sobre Codex, decisões e GPT-5.6 | F-02/F-03 §4 | Obrigatório | ausente | NÃO CONFORME | narrativa técnica ausente | BW-A10 | BLOQUEANTE |
| BW-RP-05 | `/feedback` Codex Session ID | F-02/F-03 §4 | Obrigatório | ausente | NÃO CONFORME | identificador ausente | BW-A06 | BLOQUEANTE |
| BW-TS-01 | Acesso gratuito e irrestrito para teste | F-03 §4 | Obrigatório | clone/acesso e execução do juiz não comprovados | NÃO CONFORME | pacote de teste ausente | BW-A16 | BLOQUEANTE |
| BW-LG-01 | Inglês ou tradução em inglês | F-03 §4 | Obrigatório | materiais principais em português | NÃO CONFORME | tradução integral ausente | BW-A09/A10/A14 | BLOQUEANTE |
| BW-IP-01 | Originalidade e titularidade exclusiva | F-03 §4 | Obrigatório | não há declaração/contratos | NÃO VERIFICADO | exige decisão jurídica | BW-A04 | BLOQUEANTE |
| BW-IP-02 | Licenças de OSS, dados e integrações | F-03 §4 | Obrigatório | PyQt5; dados; licenças OpenCV apenas em mídia local | NÃO VERIFICADO | inventário/licenças incompletos | BW-A04/A13 | BLOQUEANTE |
| BW-SC-01 | Ausência de segredos no pacote | Segurança pré-publicação | Obrigatório interno | scan por nomes/padrões sem achados | CONFORME COM RESSALVA | pacote final ainda não congelado | BW-A18 | BLOQUEANTE |
| BW-SC-02 | PII e dados publicáveis | F-03 §§4/8 | Obrigatório | amostras sem campos pessoais | CONFORME COM RESSALVA | revisão integral/titularidade pendente | BW-A04/A18 | ALTA |
| BW-SC-03 | Sem temporários/caminhos/materiais internos | Segurança pré-publicação | Obrigatório interno | 4 arquivos de mídia com caminhos locais; muitos não rastreados | NÃO CONFORME | pacote não saneado/congelado | BW-A12/A18 | BLOQUEANTE |
| BW-JU-01 | Implementação técnica não trivial | F-03 §7 | Avaliação | código modular, testes e histórico | CONFORME COM RESSALVA | escopo novo e Codex não demonstrados | BW-A05/A07 | ALTA |
| BW-JU-02 | Produto coerente e executável | F-03 §7 | Avaliação | aplicação e guias existem | CONFORME COM RESSALVA | teste externo/demo ausentes | BW-A16/A23 | ALTA |
| BW-JU-03 | Impacto crível para público real | F-03 §7 | Avaliação | proposta hídrica e adoção documentadas | CONFORME COM RESSALVA | evidência/narrativa competitiva insuficiente | BW-A21 | ALTA |
| BW-JU-04 | Criatividade, novidade e diferenciação | F-03 §7 | Avaliação | nenhuma comparação Build Week | NÃO VERIFICADO | diferenciação não sustentada | BW-A22 | MÉDIA |
| BW-RI-01 | Ciência dos direitos/termos/publicidade | F-03 §§8/11/14–16 | Obrigatório para entrar | nenhuma decisão humana | NÃO VERIFICADO | aceite fora da autoridade da GP | BW-A03 | BLOQUEANTE |
| BW-DL-01 | Submissão completa até 21/07 17:00 PT | F-02/F-03 §1 | Obrigatório | ainda não submetido | NÃO CONFORME | todas as dependências abertas | BW-A19/A20 | BLOQUEANTE |

### Contagem da matriz

| Status | Quantidade |
|---|---:|
| CONFORME | 1 |
| CONFORME COM RESSALVA | 8 |
| NÃO CONFORME | 17 |
| NÃO VERIFICADO | 9 |
| NÃO APLICÁVEL | 1 |
| **Total** | **36** |

## 21. Veredito preliminar

**NÃO APTO NO ESTADO ATUAL**

Fundamentação:

- o cenário de participação por residente no Brasil é expressamente vedado;
- a elegibilidade do entrante real não foi comprovada;
- há 17 não conformidades atuais, várias eliminatórias;
- faltam os artefatos centrais de comprovação e submissão;
- o tempo restante não autoriza presumir decisões jurídicas, direitos ou publicações.

O veredito não é `AUDITORIA SUSPENSA`: regras, prazo e condição territorial puderam ser confirmados, e nenhum segredo foi detectado. Também não é apenas `ELEGIBILIDADE NÃO CONFIRMADA`, porque, além do fato pessoal pendente, o pacote técnico-documental é objetivamente não conforme em múltiplos requisitos obrigatórios.

## 22. Recomendação fundamentada

Executar primeiro BW-A01/BW-A02 do [plano de ação](BW_01_ACTION_PLAN.md). Se o entrante for residente/domiciliado no Brasil, encerrar a tentativa. Se existir entrante genuinamente elegível, com participação e direitos reais, seguir o caminho crítico sem contorno nominal e somente submeter após fechamento das lacunas P0.

## 23. Pontos que exigem decisão humana

- identidade, idade, residência/domicílio e modalidade do entrante;
- legitimidade do vínculo de equipe/organização e representante;
- aceite das regras, termos, privacidade, publicidade e arbitragem;
- titularidade, autoria, marca, dados, licenças e permissões;
- categoria e narrativa final;
- escolha público/licenciado versus privado/compartilhado;
- gravação/publicação do vídeo;
- disponibilização gratuita para teste;
- submissão do formulário.

## 24. Integridade da execução

Foram criados apenas documentos de auditoria e atualizados HISTORY/ROADMAP dentro da autorização. Nenhum código, arquitetura, banco, teste, interface ou licença foi alterado. Nenhum commit, push, publicação, conta, aceite ou submissão foi realizado.

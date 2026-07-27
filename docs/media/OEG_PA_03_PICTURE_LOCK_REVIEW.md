# OEG-PA-03 — Revisão Editorial Controlada para Picture Lock

Data: 18/07/2026
Autoridade visual: `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive`
SHA-256 da autoridade: `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`
Parecer editorial: **PICTURE LOCK REPROVADO**

## 1. Objetivo

Determinar se a montagem visual oficial do vídeo institucional do PROTEUS está editorialmente apta para congelamento definitivo da imagem e início da pós-produção de áudio.

Esta OEG revisa somente a autoridade definida pela OEG-PA-02. Não grava, cria ou incorpora narração, música ou efeitos; não realiza mixagem, masterização ou exportação institucional final.

## 2. Metodologia

A revisão combinou quatro camadas de evidência:

1. **Autoridade primária:** leitura da estrutura MLT do projeto Kdenlive, de seus in/out, ordem, duração, trilhas e cortes.
2. **Inspeção visual:** exame dos quadros correspondentes às 12 cenas e dos pares anterior/posterior dos 11 pontos de corte.
3. **Análise temporal:** detecção de trechos sem mudança visual por `freezedetect` com limiar de -50 dB e duração mínima de 1,5 s; detecção de quadros pretos; conferência dos 3.240 frames a 30 fps.
4. **Compatibilidade narrativa:** comparação das durações com o guia e o plano de sincronização da narração SC001–SC012, sem produzir ou inserir áudio.

O render-base preexistente de 108 segundos foi utilizado exclusivamente como **proxy observacional fiel da timeline** para análise de frames e cortes. Ele não substituiu o `.kdenlive` como referência editorial, não recebeu autoridade e não foi alterado. Uma folha temporária dos pontos de corte foi gerada fora do repositório e não integra o pacote audiovisual.

Não houve edição ou salvamento do projeto, alteração de mídia, criação de versão audiovisual, render final ou exportação institucional.

### 2.1 Limitação de validação humana

A inspeção visual desta execução foi assistida por análise computacional e amostragem integral das cenas e cortes. Não houve sessão humana presencial de playback contínuo, em tempo real e tela cheia. Como a OEG exige revisão editorial humana controlada, essa ausência é uma limitação bloqueante para um parecer positivo de Picture Lock, ainda que os achados objetivos já revelem ajustes materiais.

## 3. Critérios de avaliação

Cada cena foi avaliada nos seguintes eixos:

- continuidade com as cenas anterior e posterior;
- coerência na progressão narrativa SC001–SC012;
- duração e equilíbrio rítmico;
- tempo disponível para locução e leitura da interface;
- enquadramento, nitidez e estabilidade;
- legibilidade e densidade visual;
- pertinência do conteúdo exibido;
- capacidade de sustentar congelamento definitivo sem recaptura.

Os pareceres possíveis são: **Aprovada**, **Aprovada com ressalvas**, **Requer ajuste** e **Requer recaptura**.

## 4. Evidências globais da montagem

| Evidência | Resultado editorial |
|---|---|
| Ordem | SC001 → SC012 preservada |
| Duração | 108,000 s / 3.240 frames |
| Cortes | 11 cortes secos; sem gaps, sobreposições ou transições editoriais |
| Quadros pretos | nenhum intervalo detectado |
| Enquadramento | 1920×1080 consistente; interface integralmente enquadrada |
| Nitidez | adequada para o material de captura; não há evidência de desfoque ou escala incorreta |
| Movimento | quase todas as cenas permanecem visualmente estáticas durante o respectivo plano |
| Áudio | ausente, conforme escopo e baseline |
| Encerramento | SC012 termina por corte no fim da timeline; não existe cartela, fade ou crédito editável na autoridade |

### 4.1 Ritmo observado

O detector de imobilidade identificou:

- SC001 estática durante seus 9,0 s;
- SC002 com dois holds de aproximadamente 7,5 s e 4,33 s, separados por alteração breve;
- SC003–SC011 essencialmente estáticas por toda a duração de cada cena;
- SC012 essencialmente estática até o fim do arquivo.

Estabilidade não é defeito por si só. Entretanto, nesta montagem ela se converte em cadência de slideshow: planos de 8 a 12 segundos com pouca ou nenhuma progressão interna. O plano de voz prevê leituras de 3,48 a 5,42 segundos e registra 52,98 segundos agregados de margem para pausas e sincronização. Essa folga favorece locução calma, mas também cria risco de permanência visual excessiva, sobretudo em SC002 e SC005, e não compensa a baixa hierarquia de SC008 e SC009.

## 5. Avaliação individual das 12 cenas

| Cena | Duração | Continuidade e conteúdo | Ritmo e qualidade visual | Parecer |
|---|---:|---|---|---|
| SC001 — Home | 9,0 s | Abertura de marca clara; introduz identidade e conecta corretamente ao contexto institucional | Logo e chamada possuem boa hierarquia e nitidez; o plano é totalmente estático e longo para a locução estimada de 3,48 s | **Aprovada com ressalvas** |
| SC002 — Sobre | 12,0 s | Mantém o eixo institucional e faz ponte para a plataforma; corte de entrada é semanticamente coerente | É a cena mais longa; há dois longos holds e mudança breve. A locução estimada ocupa somente 4,09 s | **Requer ajuste** |
| SC003 — Plataforma | 8,3 s | A seção “Por que o PROTEUS existe?” sustenta missão, visão e valores e mantém progressão lógica | Enquadramento e hierarquia adequados; conteúdo permanece estático, mas o tempo é compatível com a locução de 4,97 s | **Aprovada com ressalvas** |
| SC004 — Dashboard | 9,2 s | A tela “Como o PROTEUS funciona?” explica camadas e responsabilidades; transição para a operação é coerente | Título é legível; tabela secundária é densa. Plano estático, com margem de 3,75 s sobre a locução | **Aprovada com ressalvas** |
| SC005 — Qualidade da Água | 11,3 s | Primeira demonstração operacional forte; gráfico e indicadores correspondem ao tema narrativo | Visual limpo e estável, mas o hold integral é longo; locução estimada de 4,97 s deixa 6,29 s de margem | **Requer ajuste** |
| SC006 — Dados Ambientais | 8,1 s | Expande corretamente o contexto após qualidade da água | Tabela e estados são reconhecíveis, porém textos e múltiplas colunas são pequenos para leitura detalhada; ausência de movimento orientador | **Aprovada com ressalvas** |
| SC007 — Consumo e Distribuição | 8,5 s | Continuidade funcional adequada; introduz consumo, volume e perdas | Tabela domina o plano e possui baixa variação visual; leitura fina depende de tela grande, embora a função geral seja identificável | **Aprovada com ressalvas** |
| SC008 — Relatórios | 8,6 s | A posição antes de análise é coerente, mas a cena mostra principalmente saída textual bruta | Grande área vazia, bloco de texto pequeno e pouca hierarquia. O quadro não comunica “relatórios” com força institucional suficiente | **Requer ajuste** |
| SC009 — Previsão Analítica | 8,3 s | A posição entre relatórios e governança é conceitualmente correta | Saída textual pequena no canto superior, grande área ociosa, baixa legibilidade e ausência de elemento analítico visual dominante. É o ponto mais fraco da montagem | **Requer recaptura** |
| SC010 — Governança Operacional | 8,0 s | Recupera a força narrativa após SC009; estados, eventos e rastreabilidade são pertinentes | Cores e blocos criam hierarquia melhor; tabelas continuam densas, mas a leitura macro é clara | **Aprovada com ressalvas** |
| SC011 — Painel Executivo | 8,2 s | Eleva corretamente a narrativa para síntese executiva | Cards superiores são legíveis e dão hierarquia; tabela inferior é densa, porém secundária | **Aprovada com ressalvas** |
| SC012 — Dossiê Final | 8,5 s | Fecha corretamente a progressão funcional no dossiê | O conteúdo é denso e estático; o término ocorre sem tratamento visual editável de encerramento na autoridade | **Requer ajuste** |

### 5.1 Consolidação dos pareceres

| Classificação | Cenas | Quantidade |
|---|---|---:|
| Aprovada | nenhuma | 0 |
| Aprovada com ressalvas | SC001, SC003, SC004, SC006, SC007, SC010, SC011 | 7 |
| Requer ajuste | SC002, SC005, SC008, SC012 | 4 |
| Requer recaptura | SC009 | 1 |

A ausência de cenas sem ressalva não significa que toda a seleção esteja inadequada. Ela demonstra que o Assembly ainda conserva características de montagem preliminar: planos estáticos, interfaces densas e finalização visual externa ao projeto editável.

## 6. Achados

### 6.1 Achados favoráveis

1. A sequência SC001–SC012 é coerente: identidade → fundamento → arquitetura → operação → análise → governança → síntese.
2. Não existem gaps, sobreposições, quadros pretos ou cortes tecnicamente corrompidos.
3. Os 11 cortes são visualmente limpos e não apresentam flashes ou enquadramentos incompatíveis.
4. A identidade cromática, o enquadramento 16:9 e a nitidez são consistentes.
5. Todas as cenas possuem duração suficiente para os textos de narração já planejados.
6. SC001, SC003, SC005, SC010 e SC011 possuem elementos visuais capazes de sustentar seus respectivos conceitos, apesar das ressalvas de ritmo.

### 6.2 Achados impeditivos

1. **SC009 não está apta ao congelamento:** exige recaptura ou substituição por uma visualização analítica com hierarquia, ocupação de quadro e legibilidade compatíveis com o restante do filme.
2. **SC008 exige ajuste editorial:** a saída textual e a grande área vazia enfraquecem a comunicação institucional.
3. **O ritmo não está resolvido:** a predominância de planos integralmente estáticos e a ampla margem de locução não demonstram, sem playback humano, que 108 segundos sejam a duração editorial definitiva.
4. **O encerramento não está resolvido na autoridade:** SC012 termina sem fade, cartela final ou decisão explícita por corte seco. O tratamento existente no derivado auxiliar não pode ser presumido como parte da timeline oficial.
5. **Não houve sessão humana integral de playback:** requisito expresso desta OEG para a aprovação editorial final.

## 7. Ressalvas

- Os textos pequenos das interfaces podem ser suficientes como textura informacional, mas não como informação que o espectador deva ler integralmente. Essa intenção precisa ser formalizada na próxima revisão.
- A estabilidade das capturas é alta; o problema observado é monotonia potencial, não tremor ou falha técnica.
- A ausência de áudio é correta nesta etapa. Nenhuma conclusão de ritmo dependeu de música ou voz já produzida; foram usados somente os tempos planejados.
- Fades, legendas e cartela do derivado visual V1 são referências auxiliares e não corrigem a autoridade enquanto não forem deliberadamente incorporados a uma nova versão editável.
- Esta OEG não determina que todo plano receba animação. Ela exige que duração e movimento — inclusive a opção deliberada por imagem estática — sejam aprovados em playback contínuo.

## 8. Recomendações

### 8.1 Ajustes bloqueantes antes de nova revisão

1. Criar, sob autorização editorial específica, uma nova versão derivada do projeto — sem sobrescrever o Assembly Cut V1.
2. Recapturar ou substituir SC009 por uma tela de previsão/analytics que apresente resultado principal legível, hierarquia visual clara e ocupação equilibrada do quadro.
3. Reenquadrar, ampliar ou substituir SC008 para tornar a saída de relatórios imediatamente reconhecível; evitar bloco textual pequeno cercado por área vazia.
4. Reavaliar a duração de SC002 e SC005 em playback contínuo; encurtar os holds ou introduzir progressão visual somente se a revisão humana confirmar perda de ritmo.
5. Definir e implementar na versão editável o encerramento visual: corte seco deliberado, fade e/ou cartela final. Créditos devem ser decididos antes do Picture Lock se alterarem a duração da imagem.

### 8.2 Verificações da próxima candidata

1. Executar playback humano integral, em tempo real e tela cheia, com registro de data, ambiente e revisor.
2. Revalidar os 11 cortes, a legibilidade de SC006, SC007, SC010, SC011 e SC012 e o ritmo global.
3. Registrar nova duração, mapa de cenas, hash do projeto e relação de derivação com o Assembly Cut V1.
4. Somente após aprovação dessa candidata emitir Picture Lock e liberar gravação/sincronização de áudio.

## 9. Decisão sobre pós-produção de áudio

**A imagem não pode ser congelada nesta versão.**

Consequentemente:

- a gravação de narração não está liberada como produção final sincronizada;
- música, efeitos, edição de voz, mixagem e masterização permanecem suspensos;
- os textos e planos de voz podem permanecer preservados documentalmente, mas não devem ser tratados como sincronização definitiva;
- nenhuma exportação institucional final está autorizada.

## 10. Parecer editorial final

**PICTURE LOCK REPROVADO.**

A montagem possui continuidade técnica, ordem narrativa coerente, enquadramento consistente e nenhuma ruptura de arquivo. Contudo, não está editorialmente pronta para congelamento definitivo porque:

- SC009 requer recaptura;
- SC008, SC002, SC005 e SC012 requerem ajuste;
- o encerramento visual não existe na autoridade editável;
- a cadência predominantemente estática ainda precisa ser deliberada em playback humano contínuo;
- o requisito de revisão humana integral não foi satisfeito nesta execução assistida.

O Assembly Cut V1 permanece íntegro como autoridade visual e não foi modificado. Ele deve servir de origem imutável para uma futura candidata de Picture Lock, não receber o status de Picture Lock em seu estado atual.

**PARECER: `PICTURE_LOCK_REPROVADO — AJUSTES_EDITORIAIS_E_RECAPTURA_SC009_OBRIGATÓRIOS`.**

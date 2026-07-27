# OEG-PA-04 — Remediação Editorial da SC009

Data: 18/07/2026
Natureza: preparação técnica, sem execução de captura ou edição
Autoridade preservada: `media/proteus_institutional_video/project/PROTEUS_ASSEMBLY_CUT_V1.kdenlive`
SHA-256 da autoridade: `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B`
Parecer: **PLANO DE RECAPTURA APROVADO PARA EXECUÇÃO FUTURA CONTROLADA**

## 1. Objetivo

Definir, de forma reproduzível e auditável, como produzir uma nova captura candidata para a SC009 — Previsão Analítica, eliminando as não conformidades editoriais registradas na OEG-PA-03 sem substituir a cena atual, editar a timeline ou alterar qualquer outra cena.

Esta OEG produz somente o plano. A gravação, a seleção de tomada e a futura substituição exigem execução e validação posteriores.

## 2. Baseline preservado

| Elemento | Baseline |
|---|---|
| Projeto autoritativo | `PROTEUS_ASSEMBLY_CUT_V1.kdenlive` |
| SHA-256 do projeto | `F6196B29ECDB82846193065F38C28D59DADF355C61DE2193309549920ADA936B` |
| Fonte atual da SC009 | `media/proteus_institutional_video/SC009.mp4` |
| SHA-256 da fonte atual | `342BECB6183492320FD4A087E55F4CAA3C0FC8120FDA36CBE43E7DDCF28E1B94` |
| Fonte atual | H.264, 1920×1080, 30 fps, 8,766667 s |
| Trecho usado na timeline | 00:00:00.300–00:00:08.567 |
| Duração na timeline | 249 frames / 8,300 s |
| Posição na timeline | 00:01:15.000–00:01:23.300 |
| Cena anterior | SC008 — Relatórios |
| Cena posterior | SC010 — Governança Operacional |

A nova gravação deverá ser preservada como candidata independente. Não poderá sobrescrever `SC009.mp4`, alterar o `.kdenlive` ou assumir autoridade antes de aprovação formal.

## 3. Diagnóstico completo

### 3.1 Defeitos observados

1. **Predomínio textual:** o quadro atual apresenta conteúdo técnico semelhante a saída textual, sem uma visualização dominante que comunique análise.
2. **Baixa ocupação útil:** o conteúdo concentra-se na região superior/esquerda e deixa grande área do quadro sem função narrativa.
3. **Hierarquia insuficiente:** não existe um primeiro elemento inequívoco para o olhar; score, tendência e alerta não formam níveis visuais reconhecíveis.
4. **Legibilidade baixa:** o texto relevante é pequeno para exibição institucional e não pode ser compreendido confortavelmente durante 8,3 segundos.
5. **Ausência de movimento significativo:** a captura permanece essencialmente estática durante todo o trecho utilizado.
6. **Mensagem incompleta:** a locução prevista afirma que a tela apresenta “tendências, alertas e Water Health Score”, mas esses três resultados não aparecem como unidades visuais claras no quadro atual.
7. **Queda de força editorial:** SC008 já possui saída textual e baixa hierarquia; repetir padrão semelhante em SC009 cria um bloco visualmente fraco antes da SC010, que recupera cards, cores e tabela estruturada.

### 3.2 Impacto editorial

- o espectador reconhece uma tela técnica, mas não identifica rapidamente o resultado analítico principal;
- a promessa narrativa de transformação de dados em sinais não é demonstrada visualmente;
- a cena interrompe a progressão Relatórios → Analytics → Governança porque não diferencia consolidação textual de interpretação analítica;
- a grande área vazia e o plano estático fazem a duração parecer maior do que seus 8,3 segundos;
- a entrada em SC010 produz aumento abrupto de hierarquia e densidade, evidenciando a fragilidade de SC009.

### 3.3 Causa-raiz

A interface atual de `PrevisaoAnaliticaPage` já oferece os componentes adequados:

- título “Previsao Analitica”;
- subtítulo “Tendencias deterministicas, alertas preventivos e Water Health Score”;
- card de Water Health Score com valor, status e explicações;
- tabela de tendências com domínio, métrica, direção e médias;
- tabela de alertas com severidade, domínio, métrica, mensagem e evidência.

A não conformidade decorre da captura selecionada, que não apresenta esse estado funcional carregado com hierarquia e dados suficientes. Não é necessário alterar código ou criar nova funcionalidade; é necessário recapturar corretamente a tela existente.

### 3.4 Por que ajustes simples não resolvem

| Ajuste sobre a captura atual | Motivo da insuficiência |
|---|---|
| Crop | elimina área vazia, mas não cria score, tendências e alertas visualmente diferenciados |
| Zoom digital | amplia texto técnico de baixo valor e pode reduzir nitidez; a hierarquia continua ausente |
| Pan | movimenta o enquadramento sobre conteúdo inadequado, sem melhorar a mensagem |
| Animação de cursor | aponta para elementos que não possuem força visual suficiente |
| Texto ou gráfico sobreposto | cria conteúdo externo à aplicação e enfraquece a autenticidade da demonstração |
| Correção de cor/contraste | melhora aparência, mas não corrige composição, semântica ou ocupação do quadro |
| Aumento da duração | prolonga a exposição da mesma deficiência |

Conclusão diagnóstica: **a recaptura é necessária porque a informação visual exigida não existe de forma adequada nos pixels da tomada atual**.

## 4. Estado obrigatório da aplicação

Antes de abrir o gravador, preparar a aplicação sem modificar seu código:

1. utilizar somente dados fictícios e não sensíveis;
2. garantir histórico suficiente em mais de uma data para cálculo de tendências de qualidade e consumo;
3. garantir um Water Health Score numérico, com status oficial e explicação não vazia;
4. garantir pelo menos duas linhas úteis na tabela de tendências, evitando que todas apareçam como `dados_insuficientes`;
5. garantir pelo menos um alerta preventivo demonstrativo, com severidade, métrica, mensagem e evidência legíveis;
6. abrir a página **Previsão Analítica** e executar a atualização antes do início da gravação;
7. conferir que título, subtítulo, score, tendências e alertas estão simultaneamente presentes;
8. manter o tema e a navegação lateral iguais aos das SC008 e SC010;
9. fechar terminal, editor, explorador de arquivos, logs e qualquer janela externa;
10. desativar notificações do sistema operacional.

Os dados deverão ser preparados antes da tomada. Não digitar, cadastrar, excluir ou alterar registros durante a gravação.

## 5. Plano de recaptura

### 5.1 Configuração técnica

| Parâmetro | Especificação obrigatória |
|---|---|
| Fonte | captura exclusiva da janela “Sistema de Analise de Agua v1.0” |
| Resolução da aplicação | 1920×1080 |
| Resolução base/saída | 1920×1080 |
| Proporção | 16:9 |
| Escala do sistema | 100%; não alterar durante a sessão |
| Frame rate | 30 fps constante |
| Codec | H.264 |
| Bitrate | 12.000–20.000 Kbps |
| Intervalo de keyframe | 2 s |
| Filtro de escala | Lanczos, se houver escala; preferir captura sem redimensionamento |
| Áudio | desativado |
| Cor | SDR/Rec.709; HDR desativado |
| Captura | janela da aplicação, sem desktop, barra de tarefas ou outras janelas |

Usar o perfil OBS `PROTEUS_FILM_OFFICIAL_SCENES` e a coleção `PROTEUS_WINDOW_CAPTURE`, conforme o guia existente.

### 5.2 Enquadramento

- capturar a janela completa, sem cortar a barra lateral ou a área de conteúdo;
- manter a barra lateral visível para continuidade espacial com SC008 e SC010;
- posicionar o título e o subtítulo no alto do conteúdo;
- preservar integralmente o card de Water Health Score no terço superior;
- exibir cabeçalhos e pelo menos duas linhas úteis da tabela de tendências;
- exibir cabeçalhos e pelo menos uma linha útil da tabela de alertas;
- manter o botão “Atualizar Analise” visível apenas se couber naturalmente, sem torná-lo o foco;
- não usar crop ou zoom digital durante a tomada;
- não permitir que o cursor cubra valores, status, cabeçalhos ou mensagens.

Se os cinco blocos essenciais não couberem simultaneamente em 1920×1080 a 100%, a tomada deverá ser interrompida. Não reduzir a aplicação até tornar o texto ilegível; registrar a limitação para nova deliberação.

### 5.3 Percurso visual

A cena deve apresentar um único percurso contínuo, sem cliques e sem rolagem:

| Tempo útil | Ação visual | Finalidade |
|---:|---|---|
| 0,0–1,0 s | quadro estável; cursor repousado na margem direita inferior, fora das tabelas | permitir reconhecimento da tela e corte limpo vindo de SC008 |
| 1,0–2,8 s | deslocamento lento até uma linha representativa da tabela de tendências | introduzir o primeiro sinal analítico |
| 2,8–4,6 s | deslocamento lento até o alerta preventivo principal | mostrar consequência interpretativa e evidência |
| 4,6–6,7 s | deslocamento controlado até o card de Water Health Score | concluir no resultado agregado de maior hierarquia |
| 6,7–8,3 s | cursor sai para uma área neutra; quadro permanece estável | criar respiro e preparar o corte para SC010 |

Regras do movimento:

- velocidade uniforme, aproximada de 250–400 pixels por segundo;
- sem aceleração brusca, círculos, tremor ou retorno desnecessário;
- sem clique, seleção de linha, tooltip ou mudança de foco;
- no máximo três movimentos direcionais principais;
- cursor visível somente como guia discreto;
- nenhuma rolagem, pois ela comprometeria a leitura e a continuidade do plano curto.

### 5.4 Duração e handles

Para preservar a estrutura futura da timeline:

- gravar de 10,3 a 12,0 segundos brutos;
- manter pelo menos 1,0 segundo de handle estável antes do percurso;
- manter pelo menos 1,0 segundo de handle estável após o percurso;
- garantir um segmento editorial contínuo de **249 frames / 8,300 segundos**;
- a futura substituição deverá manter exatamente a duração atual da SC009, salvo nova autorização de estrutura.

A tomada não deve ser acelerada ou retimada. O movimento deve nascer com velocidade adequada na gravação original.

### 5.5 Elementos obrigatórios

Devem permanecer identificáveis durante toda a janela útil:

1. título **Previsao Analitica**;
2. referência explícita a **Tendencias deterministicas, alertas preventivos e Water Health Score**;
3. Water Health Score numérico e respectivo status;
4. pelo menos uma explicação do score;
5. pelo menos duas tendências úteis, com domínio, métrica e direção;
6. pelo menos um alerta, com severidade e evidência;
7. navegação lateral e identidade visual do PROTEUS;
8. indicação visual de que os sinais são determinísticos, sem menção a Machine Learning ou IA generativa.

### 5.6 Elementos proibidos

- terminal, console, traceback, logs ou código-fonte;
- desktop, barra de tarefas, notificações ou outra aplicação;
- dados pessoais, clientes reais, localidades sensíveis ou identificadores não autorizados;
- estado vazio, `--`, tabela sem dados ou predomínio de `dados_insuficientes`;
- alegações de IA generativa, Machine Learning, previsão autônoma, laudo ou decisão regulatória;
- digitação, alteração de dados persistidos ou acionamento funcional durante a tomada;
- zoom agressivo, rolagem rápida, cursor nervoso ou clique sem função narrativa;
- áudio de sistema, microfone ou notificação sonora.

## 6. Nomenclatura e preservação do candidato

Durante a execução futura, usar nomes que não colidam com a fonte vigente:

```text
media/proteus_institutional_video/official_scenes/raw/SC009_ANALYTICS_RECAPTURE_CANDIDATE_T01.mp4
media/proteus_institutional_video/official_scenes/raw/SC009_ANALYTICS_RECAPTURE_CANDIDATE_T02.mp4
media/proteus_institutional_video/official_scenes/raw/SC009_ANALYTICS_RECAPTURE_CANDIDATE_T03.mp4
```

Gravar no mínimo três tomadas com o mesmo estado de dados e o mesmo percurso. Nenhuma deverá ser renomeada para `SC009.mp4` nesta etapa.

Após avaliação posterior, a tomada selecionada poderá ser copiada para a área `approved/` com nome de candidato aprovado, hash próprio e registro de proveniência. A aprovação da mídia não implica substituição automática na timeline.

## 7. Critérios de aceitação

### 7.1 Critérios editoriais bloqueantes

A tomada candidata somente poderá avançar se todos os itens abaixo forem aprovados:

| ID | Critério | Evidência exigida |
|---|---|---|
| CA-01 | continuidade clara entre Relatórios, Analytics e Governança | revisão dos cortes SC008→candidata e candidata→SC010 |
| CA-02 | score, tendências e alertas reconhecíveis em até 2 segundos | playback em tela cheia por revisor humano |
| CA-03 | hierarquia dominante no score e hierarquia secundária nas tabelas | inspeção visual a 100% |
| CA-04 | ocupação equilibrada, sem grande área vazia sem função | frame de referência e playback |
| CA-05 | movimento natural e estável | playback a velocidade normal |
| CA-06 | percurso completo em 8,3 s sem pressa | contagem de frames e playback |
| CA-07 | textos essenciais legíveis em exibição 1920×1080 | revisão humana em tela cheia |
| CA-08 | nenhum elemento proibido | inspeção quadro a quadro e checklist |
| CA-09 | nenhum dado é alterado durante a gravação | registro operacional e comparação do estado antes/depois |
| CA-10 | imagem final é compatível com corte seco para SC010 | inspeção do último frame e simulação de corte |

Falha em qualquer item CA-01–CA-10 reprova a tomada.

### 7.2 Critérios técnicos bloqueantes

- vídeo H.264, 1920×1080, 30 fps constante, 16:9;
- segmento utilizável contínuo de pelo menos 249 frames;
- decodificação integral sem erro;
- nenhum frame preto, congelamento involuntário, tearing, flicker ou notificação;
- nenhum frame duplicado causado por perda de captura;
- áudio ausente ou stream totalmente descartado antes de futura integração;
- início e fim com handles estáveis;
- SHA-256 calculado e registrado;
- tamanho, duração, codec, frame rate e quantidade de frames registrados por `ffprobe`;
- reprodução aprovada em velocidade normal e inspeção dos frames inicial, intermediário e final.

### 7.3 Critério semântico

A cena deve demonstrar, sem texto externo adicional:

> dados históricos são transformados em tendências, alertas preventivos e Water Health Score por processamento determinístico.

Ela não pode sugerir previsão autônoma, decisão automática, certificação, laudo ou autoridade regulatória.

## 8. Checklist operacional para gravação

### 8.1 Antes da gravação

- [ ] Confirmar que o projeto Kdenlive e `SC009.mp4` não serão abertos para edição.
- [ ] Registrar hash da autoridade e da SC009 atual.
- [ ] Confirmar dados fictícios, consistentes e sem informação sensível.
- [ ] Confirmar score numérico, explicações, duas tendências úteis e pelo menos um alerta.
- [ ] Abrir Previsão Analítica e atualizar a análise antes de iniciar o OBS.
- [ ] Confirmar ausência de terminal, logs, janelas externas e notificações.
- [ ] Configurar janela, OBS, 1920×1080, 30 fps, H.264 e áudio desativado.
- [ ] Posicionar cursor na área neutra inicial.
- [ ] Fazer teste de cinco segundos e revisar legibilidade/estabilidade.
- [ ] Definir o nome `..._T01.mp4` antes de gravar.

### 8.2 Durante cada tomada

- [ ] Manter um segundo inicial estável.
- [ ] Executar exatamente o percurso tendências → alerta → score.
- [ ] Não clicar, rolar, digitar ou acionar atualização.
- [ ] Não cobrir valores ou cabeçalhos com o cursor.
- [ ] Manter velocidade uniforme e no máximo três movimentos principais.
- [ ] Manter pelo menos um segundo final estável.
- [ ] Encerrar sem alternar janela ou revelar o desktop.

### 8.3 Após cada tomada

- [ ] Reproduzir integralmente em velocidade normal e tela cheia.
- [ ] Validar continuidade com os últimos frames de SC008 e primeiros de SC010.
- [ ] Conferir score, tendências, alerta e explicação.
- [ ] Conferir ausência de notificações, dados sensíveis e elementos proibidos.
- [ ] Executar validação de codec, resolução, fps, duração, frames e decodificação.
- [ ] Calcular SHA-256.
- [ ] Registrar tomada, data, operador, estado de dados, configuração OBS e resultado.
- [ ] Classificar a tomada como candidata, rejeitada ou selecionada para auditoria posterior.
- [ ] Não substituir arquivo, timeline ou manifesto de autoridade nesta OEG.

## 9. Registro mínimo de proveniência da execução futura

Para cada tomada, preservar:

- nome e caminho do arquivo;
- data/hora e responsável pela captura;
- branch, commit e estado do repositório da aplicação;
- versão do Python, PyQt, sistema operacional e OBS;
- escala do sistema e resolução da janela;
- identificadores ou hashes dos datasets demonstrativos, sem copiar dados sensíveis para o relatório;
- configuração de vídeo do OBS;
- duração, número de frames, codec, bitrate, streams e SHA-256;
- checklist preenchido;
- justificativa da tomada selecionada e das rejeitadas.

Essas evidências permitem reproduzir a captura e provar que a candidata resulta da aplicação existente, não de uma composição externa.

## 10. Preservação da autoridade

Durante esta OEG:

- o Assembly Cut V1 permanece a única autoridade visual;
- a SC009 vigente permanece referenciada e inalterada;
- nenhuma mídia candidata foi gravada;
- nenhuma substituição foi executada;
- nenhuma edição de timeline, render institucional ou exportação final foi realizada;
- nenhuma outra cena foi avaliada ou modificada.

Uma futura captura será apenas **candidata à substituição**. Sua promoção exige, no mínimo:

1. auditoria técnica e editorial da tomada;
2. aprovação explícita da candidata;
3. autorização específica para criar uma nova versão derivada do projeto;
4. substituição controlada sem sobrescrever o Assembly Cut V1;
5. nova revisão de Picture Lock.

## 11. Parecer técnico

**PLANO DE RECAPTURA TECNICAMENTE SUFICIENTE E APROVADO PARA EXECUÇÃO FUTURA.**

A SC009 deve ser recapturada diretamente na página Previsão Analítica carregada com dados demonstrativos, em 1920×1080 e 30 fps, preservando simultaneamente Water Health Score, explicações, tendências e alertas. O percurso deve durar 8,3 segundos úteis, usar movimento lento do cursor na ordem tendências → alerta → score, começar e terminar em estabilidade e evitar qualquer clique, rolagem ou alteração de dados.

A correção elimina a não conformidade porque substitui a saída textual de baixa hierarquia por uma demonstração autêntica dos componentes visuais já existentes na aplicação, mantendo continuidade com SC008 e SC010.

**PARECER: `SC009_RECAPTURE_PLAN_APROVADO — EXECUÇÃO_E_SUBSTITUIÇÃO_AINDA_NÃO_AUTORIZADAS`.**

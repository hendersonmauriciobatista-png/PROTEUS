# GP-RG-07 - Protocolo De Independencia Dos Avaliadores

## 1. Objetivo

Preservar separacao metodologica entre Avaliador A e Avaliador B desde a distribuicao do pacote ate o congelamento das conclusoes individuais.

## 2. Controles Obrigatorios

| Controle | Aplicacao |
|---|---|
| contextos | duas instancias novas com `fork_turns=none` |
| simultaneidade | execucao paralela, sem resultado de uma disponivel ao prompt da outra |
| instrucao | mensagem textual identica, variando somente letra e arquivo de destino |
| entradas | somente os 13 artefatos hashados no plano |
| saidas | A escreve apenas `RG_07_EXECUTION_A.md`; B apenas `RG_07_EXECUTION_B.md` |
| comunicacao | proibida entre avaliadores; coordenador nao envia esclarecimentos apos inicio |
| leitura proibida | todos os `RG_06_*.md`, HISTORY, ROADMAP, arquivos `RG_07_EXECUTION_*` alheios, matriz, auditoria e encerramento |
| filesystem | compartilhado, mas leitura limitada por instrucao e declaracao final |
| congelamento | coordenador calcula hashes imediatamente apos ambos encerrarem |
| comparacao | somente coordenador, depois do duplo congelamento |

## 3. Prompt Comum Congelado

Texto comum, com substituicoes `<AVALIADOR>` e `<ARQUIVO>` apenas:

> Voce e o Avaliador <AVALIADOR> da GP-RG-07. Execute independentemente a OEG-RG-06 usando somente os 13 artefatos enumerados em `docs/research/RG_07_EXPERIMENT_PLAN.md` e seguindo integralmente as secoes 5 e 6 desse plano. Leia tambem `docs/research/RG_07_INDEPENDENCE_PROTOCOL.md`. Nao leia nenhum arquivo RG_06, HISTORY, ROADMAP, a execucao do outro avaliador ou futuros documentos RG_07. Nao se comunique com outro agente e nao crie subagentes. Primeiro crie <ARQUIVO> contendo identidade, verificacao de hashes e pre-registro; somente em uma segunda edicao do mesmo arquivo acrescente selecao, execucao, resultados e encerramento. Escreva apenas nesse arquivo. Use somente evidencias do pacote, registre ausencias e nao promova hipoteses. Ao finalizar, declare explicitamente os arquivos lidos e que nao acessou conclusoes do outro avaliador.

## 4. Incidentes E Suspensao

Suspender se:

* um avaliador declarar leitura de conclusao alheia;
* hash de entrada divergir;
* qualquer artefato do pacote for alterado;
* coordenador fornecer orientacao assimetrica apos inicio;
* avaliador precisar de fonte externa para concluir;
* arquivo individual for editado por terceiro antes do congelamento.

Fonte adicional necessaria e registrada como MA-05; nao e consultada. Erro operacional menor deve ser preservado, classificado e nunca corrigido silenciosamente.

## 5. Verificacao De Independencia

Cada avaliador deve declarar:

1. contexto separado recebido;
2. lista exata de arquivos lidos;
3. ausencia de comunicacao;
4. ausencia de leitura de RG-06 e da execucao alheia;
5. nenhuma fonte externa usada;
6. nenhuma conclusao modificada apos contato com o coordenador.

O coordenador verifica timestamps/hashes e nao infere estados internos. Independencia e uma propriedade do arranjo observavel, nao do raciocinio interno.

## 6. Cadeia Da Decisao De Independencia

Premissas: isolamento de contexto e igualdade de entrada sao necessarios. Evidencias: recursos de agentes separados, prompt congelado e pacote hashado. Inferencia: o arranjo reduz intercambio de conclusoes observavel. Fundamentacao: paralelismo, escrita exclusiva e ausencia de mensagens eliminam os canais previstos, exceto filesystem/plataforma comuns. Decisao: classificar A/B como metodologicamente independentes se todos os controles observaveis forem atendidos. Validacao: auditoria posterior confrontara declaracoes, arquivos e hashes.

Limitacoes: nao ha isolamento fisico, organizacional ou tecnologico; mesma plataforma pode produzir dependencia comum. Ambiguidade: `inter-harnesses` e atendido apenas como duas instancias de harness, nao como tecnologias heterogeneas. Alternativas descartadas: passagens sequenciais no mesmo contexto e consenso durante execucao. Confianca: MEDIA.

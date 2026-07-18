# GP-RG-08 — Critérios de Classificação da Integridade e Executabilidade

## 1. Objetivo

Converter os resultados do preflight RG-08 em uma classificação reproduzível e em decisão operacional inequívoca, sem confundir completude parcial com autorização experimental.

## 2. Unidades e códigos

Cada verificação recebe um dos estados:

- `ATENDIDO`: evidência objetiva satisfaz o teste;
- `ATENDIDO_COM_RESSALVA`: teste essencial satisfeito, com limitação não bloqueante identificada;
- `NAO_ATENDIDO`: evidência demonstra falha;
- `NAO_VERIFICADO`: evidência suficiente não foi obtida;
- `NAO_APLICAVEL`: teste legitimamente fora do desenho, com justificativa.

Para requisito obrigatório, `NAO_VERIFICADO` tem o mesmo efeito operacional de `NAO_ATENDIDO`. `NAO_APLICAVEL` não pode ser usado para requisito que o Manifesto ou procedimento torna necessário.

## 3. Falhas bloqueantes

É bloqueante qualquer ocorrência que envolva:

1. autoridade ou escopo ausente;
2. Manifesto ausente, ambíguo ou não congelado;
3. artefato obrigatório ausente;
4. ID/versão obrigatória ambígua;
5. localizador obrigatório não resolvível;
6. hash/tamanho obrigatório divergente ou não verificável;
7. anexo obrigatório indisponível;
8. referência obrigatória órfã;
9. permissão, formato ou ferramenta que impeça passo obrigatório;
10. necessidade de fonte externa não congelada;
11. assimetria não pre-registrada entre avaliadores comparáveis;
12. risco não resolvido de confidencialidade, propriedade ou custódia;
13. passo obrigatório sem entrada, instrumento, denominador, regra ou destino;
14. mutação após congelamento sem nova versão.

Falhas não bloqueantes são apenas as que não alteram passo obrigatório, entrada, caso, instrumento, denominador, interpretação, independência, custódia ou possibilidade de auditoria. Devem ser registradas e justificadas; conveniência ou prazo não rebaixa criticidade.

## 4. Classificações

### 4.1 INTEGRALMENTE EXECUTÁVEL

Critérios cumulativos:

- todos os requisitos aplicáveis `ATENDIDO`;
- zero falhas bloqueantes;
- zero ressalvas que afetem o procedimento;
- pacote congelado, certificado e reprodutível no ambiente declarado;
- rechecagem independente ou separação de papéis atendida conforme o desenho.

Efeito: `GO`, limitado ao pacote, versão, ambiente e validade do certificado.

### 4.2 EXECUTÁVEL COM RESSALVAS

Critérios cumulativos:

- todos os requisitos bloqueantes `ATENDIDO`;
- zero `NAO_ATENDIDO`/`NAO_VERIFICADO` em item obrigatório;
- uma ou mais ressalvas não bloqueantes, cada uma com evidência, impacto, responsável e tratamento;
- nenhuma ressalva altera igualdade de entradas, procedimento, caso, métrica, interpretação ou custódia;
- autoridade experimental aceita explicitamente as ressalvas antes do início.

Efeito: `GO CONDICIONAL`. Ressalva nova ou agravada invalida o certificado.

### 4.3 PARCIALMENTE EXECUTÁVEL

Critérios:

- parte identificável do pacote e do procedimento pode ser percorrida;
- ao menos uma falha bloqueia o experimento completo, mas o acervo restante preserva utilidade para diagnóstico, preparação ou futura correção versionada;
- o alcance executável e o não executável podem ser separados sem inventar resultados.

Efeito: **`NO-GO` para o experimento completo**. Permite somente correção/novo congelamento sob autoridade adequada ou atividade diagnóstica explicitamente autorizada. Não permite “executar até onde der”.

Exemplo histórico não retroativo: a condição observada na RG-07 — 12/13 artefatos resolvidos e uma OEG obrigatória sem localizador — corresponde ao padrão conceitual desta classe, mas RG-07 mantém seu próprio estado aprovado e não é reclassificada por este documento.

### 4.4 NÃO EXECUTÁVEL

Critérios — qualquer um suficiente:

- autoridade, Manifesto ou procedimento essencial inexistente;
- composição do pacote não determinável;
- múltiplas falhas bloqueantes impedem delimitar uma parte executável segura;
- integridade/custódia comprometida;
- pacote mutável, corrompido ou substituído sem versão;
- execução exigiria inferência, memória, fonte externa ou correção retroativa incompatível com o desenho.

Efeito: `NO-GO`; isolar quando houver risco de integridade/confidencialidade e acionar governança.

## 5. Regra decisória

```text
se existe falha bloqueante:
    se existe subconjunto diagnosticável, delimitado e íntegro:
        PARCIALMENTE EXECUTÁVEL / NO-GO
    senão:
        NÃO EXECUTÁVEL / NO-GO
senão se existe ressalva não bloqueante:
    EXECUTÁVEL COM RESSALVAS / GO CONDICIONAL
senão:
    INTEGRALMENTE EXECUTÁVEL / GO
```

Contagem ou percentual de itens aprovados não substitui essa regra. Uma única falha bloqueante basta para `NO-GO`.

## 6. Matriz de impacto

| Classificação | Artefatos obrigatórios | Resolução/hash | Procedimento integral | Decisão | Correção permitida |
|---|---|---|---|---|---|
| INTEGRALMENTE EXECUTÁVEL | completos | verificados | sim | GO | nova versão para qualquer mudança |
| EXECUTÁVEL COM RESSALVAS | completos | verificados | sim | GO CONDICIONAL | tratar ressalva sem mutação silenciosa |
| PARCIALMENTE EXECUTÁVEL | falha bloqueante delimitada | parcial | não | NO-GO | corrigir, recongelar e reverificar |
| NÃO EXECUTÁVEL | indeterminados/comprometidos | insuficientes | não | NO-GO | reconstruir pacote sob nova versão/autoridade |

## 7. Precedência de ausências

1. primeiro registrar o estado do item (`AUSENTE`, `NAO_COLETADO`, `NAO_APLICAVEL`, `PERDIDO` ou `RETIDO`);
2. depois avaliar se o item é obrigatório para algum passo;
3. se obrigatório, classificar o requisito `NAO_ATENDIDO` ou `NAO_VERIFICADO` e aplicar `NO-GO`;
4. métricas e hipóteses do experimento permanecem `NAO_TESTADO` quando nenhuma unidade substantiva chegou a existir; o incidente do gate recebe sua própria classificação;
5. `TESTE_INCONCLUSIVO` só descreve teste iniciado sem conclusão válida, conforme regra pre-registrada; não deve substituir automaticamente código de ausência.

Esta precedência é prospectiva e não altera os estados divergentes preservados na RG-07.

## 8. Cadeia de fundamentação da classificação

- **Premissas:** execução integral exige todos os itens bloqueantes; percentuais podem ocultar dependência crítica.
- **Evidências:** A/B da RG-07 obtiveram 12/13 hashes e ainda assim não puderam iniciar a seleção; RG-05 manda suspender diante de entrada obrigatória inacessível.
- **Inferência:** classificação deve considerar criticidade, não maioria numérica.
- **Fundamentação:** um artefato único pode controlar autoridade, instrumento ou procedimento inteiro.
- **Decisão:** somente as duas classes sem falha bloqueante geram `GO`; `PARCIALMENTE EXECUTÁVEL` gera `NO-GO`.
- **Limitações:** criticidade deve ser declarada antes do preflight e pode exigir julgamento auditável.
- **Validação:** a matriz, a regra decisória e o checklist produzem o mesmo efeito para uma falha obrigatória.

## 9. Limitações

- limiares quantitativos não foram calibrados;
- classificação ainda não foi testada por avaliadores independentes;
- exemplos derivam de acervo interno;
- a autoridade humana continua responsável por aceitar ressalvas não bloqueantes;
- nenhuma classe positiva demonstra validade científica.


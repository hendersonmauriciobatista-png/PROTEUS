# GP-RG-09 — Plano do Experimento Sintético GX-PKG

## 1. Identidade e congelamento lógico

| Campo | Registro |
|---|---|
| GP | GP-RG-09 |
| Autoridade | OEG-RG-09, referenciada à DF-RG-09 aprovada |
| Natureza | primeiro piloto sintético do Gate GX-PKG |
| Data | 18/07/2026 |
| Protocolo | `RG_08_PACKAGE_INTEGRITY_PROTOCOL.md`, RG08-PIP v1.0 |
| Checklist | `RG_08_EXECUTABILITY_CHECKLIST.md`, CK-01 a CK-36 |
| Classificação | `RG_08_CLASSIFICATION_CRITERIA.md` |
| Estado deste plano | PRE-REGISTRADO ANTES DAS PASSAGENS DE VERIFICAÇÃO |

Este plano congela hipóteses, casos, falhas, resultados esperados, procedimento, métricas e interpretação. Os hashes finais dos fixtures serão registrados em `RG_09_TEST_CASES.md` antes da execução. Nenhum critério RG-08 será alterado durante o piloto.

## 2. Objetivo

Testar, em ambiente controlado e sem conteúdo experimental real, se a aplicação integral de GX-PKG:

1. distingue corretamente as quatro classes RG-08;
2. emite `GO`, `GO CONDICIONAL` e `NO-GO` conforme a criticidade;
3. impede início diante de falha bloqueante;
4. produz decisões rastreáveis;
5. repete os mesmos resultados em duas passagens separadas no mesmo ambiente.

## 3. Hipóteses e estados permitidos

### H1-RG09

A aplicação integral do protocolo GX-PKG identifica corretamente situações GO/NO-GO antes do início e bloqueia pacotes insuficientes.

### H0-RG09

O protocolo não identifica corretamente as situações ou permite início de pacote insuficiente.

Estados de encerramento deste piloto: `APOIADA_NO_CONTEXTO_SINTETICO_TESTADO`, `PARCIALMENTE_APOIADA`, `CONTRARIADA_NO_CONTEXTO_TESTADO`, `TESTE_INCONCLUSIVO` ou `NAO_TESTADA`. Nenhum estado implica validade universal.

## 4. Unidade de análise

- unidade primária: decisão completa GX-PKG por caso e passagem;
- unidades secundárias: 36 checks por caso, classificação, decisão, falha/ressalva e cadeia de fundamentação;
- amostra: quatro casos sintéticos × duas passagens = oito decisões;
- total de avaliações de check: 4 × 2 × 36 = 288.

## 5. Casos e injeções congeladas

| Caso | Construção | Injeção deliberada | Resultado esperado |
|---|---|---|---|
| A | pacote mínimo completo, identificado, resolvível, hashado, acessível e congelado | nenhuma | INTEGRALMENTE EXECUTÁVEL — GO |
| B | mesmo núcleo completo do A | rótulo descritivo legado no input, declarado como ressalva não bloqueante; IDs, versão, caminho, hash e instruções canônicas permanecem coerentes | EXECUTÁVEL COM RESSALVAS — GO CONDICIONAL |
| C | autoridade, procedimento, instrumento e contrato acessíveis | `input.md` obrigatório declarado no Manifesto, porém fisicamente ausente e sem hash observável | PARCIALMENTE EXECUTÁVEL — NO-GO |
| D | somente declaração do cenário, sem pacote operacional | Manifesto, autoridade, procedimento, instrumentos e entradas ausentes | NÃO EXECUTÁVEL — NO-GO |

A criticidade foi definida antes da execução. Nenhuma falha será adicionada, removida ou rebaixada após a observação dos resultados.

## 6. Ambiente e fontes permitidas

- workspace local `C:\Users\Guiuliano\SistemaAnaliseAgua`;
- raiz dos fixtures: `docs/research/rg09_fixtures/`;
- ferramentas observáveis: PowerShell `Test-Path`, `Get-Item`, `Get-FileHash` e leitura UTF-8;
- algoritmo: SHA-256;
- fontes permitidas: OEG-RG-09, instrumentos RG-08 e fixtures congelados RG-09;
- informação externa: proibida;
- alterações em RG-08: proibidas;
- conteúdo de RG-06/RG-07: somente antecedente documental, não entrada dos casos.

## 7. Procedimento congelado

### Preparação

1. criar fixtures conforme seção 5;
2. calcular hashes dos artefatos existentes;
3. preencher Manifestos A/B/C;
4. registrar bytes/hashes finais e congelamento em `RG_09_TEST_CASES.md`;
5. não modificar fixtures após esse ponto.

### Passagem V1

1. aplicar CK-01 a CK-36 a A, B, C e D;
2. verificar cada artefato por existência, resolução, bytes e SHA-256;
3. realizar dry-run apenas por metadados e sequência, sem experimento substantivo;
4. classificar pela regra RG-08;
5. registrar decisão e cadeia de sete elementos.

### Passagem V2

1. iniciar nova invocação de verificação no mesmo ambiente;
2. repetir os mesmos 36 checks sem alterar V1, fixtures ou critérios;
3. classificar independentemente do texto final de V1, usando os mesmos instrumentos;
4. comparar estados, classes e decisões somente após V2.

As passagens usam o mesmo Harness e ambiente. Portanto, medem repetibilidade operacional, não independência humana, tecnológica ou inter-harnesses.

## 8. Métricas pre-registradas

| ID | Métrica | Numerador/denominador | Critério deste piloto |
|---|---|---|---|
| M09-01 | acurácia de classe V1 | classes esperadas obtidas / 4 | 4/4 para apoio integral contextual |
| M09-02 | acurácia de decisão V1 | decisões esperadas obtidas / 4 | 4/4 |
| M09-03 | acurácia de classe V2 | classes esperadas obtidas / 4 | 4/4 |
| M09-04 | concordância de classe V1/V2 | classes idênticas / 4 | 4/4 |
| M09-05 | concordância de decisão V1/V2 | decisões idênticas / 4 | 4/4 |
| M09-06 | concordância de checks | estados idênticos V1/V2 / 144 | 144/144 |
| M09-07 | falsos GO | C/D classificados com GO / 2 | 0/2 |
| M09-08 | falsos NO-GO | A/B classificados com NO-GO / 2 | 0/2 |
| M09-09 | decisões com cadeia completa | decisões com sete campos / 8 | 8/8 |
| M09-10 | ambiguidades relevantes | ambiguidades que impedem classificação / 4 | 0 |

Não serão calculados coeficientes inferenciais. Os casos e resultados esperados foram construídos a partir das próprias regras, de modo que a análise é teste de coerência operacional, não estimativa de desempenho em população real.

## 9. Regras de interpretação

H1-RG09 recebe `APOIADA_NO_CONTEXTO_SINTETICO_TESTADO` somente se M09-01 a M09-09 atingirem os critérios e M09-10 for zero. Qualquer falso GO contraria H1 no contexto. Divergência entre V1/V2 produz no máximo apoio parcial ou teste inconclusivo conforme impacto. Necessidade de alterar RG-08 suspende a GP.

H0-RG09 não é “provada falsa”; se H1 atingir os critérios, registrar que H0 não recebeu apoio nos quatro cenários testados.

## 10. Controle de desvios e suspensão

- mudança em caso, falha, criticidade, check, classe esperada ou métrica após congelamento: D3, suspender interpretação confirmatória;
- modificação de RG-08: suspender GP;
- classificação sem cadeia completa: suspender o caso;
- fonte externa necessária: suspender o caso;
- fixture alterado após congelamento: invalidar as duas passagens e emitir nova versão somente sob autoridade.

## 11. Cadeia da decisão de início

- **Premissas:** OEG-RG-09 autoriza quatro cenários sintéticos e RG-08 fornece critérios congelados.
- **Evidências:** sete instrumentos/produtos RG-08 existem; os quatro resultados esperados são impostos pela OEG-RG-09.
- **Inferências:** casos mínimos com injeções explícitas permitem testar coerência e bloqueio antes de qualquer experimento real.
- **Fundamentação:** construção sintética controla a verdade de referência e evita repetir RG-07.
- **Decisão:** executar quatro casos em duas passagens após congelar fixtures e hashes.
- **Limitações:** mesmo Harness, amostra pequena e casos derivados do protocolo.
- **Validação:** plano define antecipadamente casos, métricas, estados, parada e resultados esperados.

## 12. Estado pré-execução

**PLANO CONGELADO — EXECUÇÃO CONDICIONADA AO REGISTRO DOS FIXTURES E HASHES EM RG_09_TEST_CASES.**


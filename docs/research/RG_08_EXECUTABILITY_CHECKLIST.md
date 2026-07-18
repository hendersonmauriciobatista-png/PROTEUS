# GP-RG-08 — Checklist de Executabilidade do Pacote Experimental

## 1. Instruções

Preencher antes de qualquer leitura substantiva. Estados permitidos: `ATENDIDO`, `ATENDIDO_COM_RESSALVA`, `NAO_ATENDIDO`, `NAO_VERIFICADO`, `NAO_APLICAVEL`. Todo estado exige evidência/localizador; `NAO_APLICAVEL` exige justificativa.

Para item obrigatório, `NAO_ATENDIDO` ou `NAO_VERIFICADO` gera falha bloqueante. Uma única falha bloqueante impede `GO`.

## 2. Cabeçalho

| Campo | Preenchimento |
|---|---|
| `verification_id` |  |
| `package_id` / versão |  |
| experimento / procedimento |  |
| `package_root` |  |
| digest do pacote/Manifesto |  |
| ambiente e ferramentas |  |
| curador |  |
| verificador |  |
| autoridade decisora |  |
| início/fim do preflight |  |

## 3. Checklist obrigatório

| ID | Verificação | Criticidade padrão | Estado | Evidência/localizador | Observação/ação |
|---|---|---|---|---|---|
| CK-01 | ato de autoridade existe, é identificável e cobre preparação/preflight | BLOQUEANTE |  |  |  |
| CK-02 | autoridade de início experimental está definida ou explicitamente condicionada ao certificado | BLOQUEANTE |  |  |  |
| CK-03 | experimento, escopo, procedimento e restrições estão univocamente identificados | BLOQUEANTE |  |  |  |
| CK-04 | Manifesto possui ID, versão, raiz, ambiente, responsáveis e timestamp | BLOQUEANTE |  |  |  |
| CK-05 | todos os passos obrigatórios têm entradas, instrumentos, agentes e saídas mapeados | BLOQUEANTE |  |  |  |
| CK-06 | todos os itens estão classificados antes do teste como obrigatórios/condicionais/opcionais | BLOQUEANTE |  |  |  |
| CK-07 | cada artefato possui ID e versão únicos | BLOQUEANTE |  |  |  |
| CK-08 | todos os artefatos obrigatórios existem fisicamente | BLOQUEANTE |  |  |  |
| CK-09 | cada localizador obrigatório resolve sem pesquisa, memória ou esclarecimento | BLOQUEANTE |  |  |  |
| CK-10 | cada resolução conduz a exatamente um alvo autorizado | BLOQUEANTE |  |  |  |
| CK-11 | nenhum localizador obrigatório escapa da raiz/depósito autorizado | BLOQUEANTE |  |  |  |
| CK-12 | todos os anexos obrigatórios estão presentes e inventariados | BLOQUEANTE |  |  |  |
| CK-13 | bytes observados coincidem com o Manifesto | BLOQUEANTE |  |  |  |
| CK-14 | SHA-256 observado coincide para todos os itens obrigatórios | BLOQUEANTE |  |  |  |
| CK-15 | algoritmo, ferramenta e momento de hash estão registrados | ALTA |  |  |  |
| CK-16 | referências cruzadas obrigatórias resolvem para ID/versão existente | BLOQUEANTE |  |  |  |
| CK-17 | instruções usam os mesmos nomes, IDs e versões do Manifesto | BLOQUEANTE |  |  |  |
| CK-18 | pre-registro e instrumentos aplicáveis estão presentes e congelados | BLOQUEANTE |  |  |  |
| CK-19 | métricas possuem entradas e denominadores disponíveis | BLOQUEANTE |  |  |  |
| CK-20 | estados e regras de interpretação citados estão identificados e acessíveis | BLOQUEANTE |  |  |  |
| CK-21 | formatos podem ser lidos pelas ferramentas declaradas | BLOQUEANTE |  |  |  |
| CK-22 | papéis previstos possuem permissões mínimas necessárias | BLOQUEANTE |  |  |  |
| CK-23 | destinos de saída existem, são graváveis e separados quando necessário | BLOQUEANTE |  |  |  |
| CK-24 | dry-run não substantivo percorre todos os passos obrigatórios | BLOQUEANTE |  |  |  |
| CK-25 | nenhum passo depende de fonte externa não congelada | BLOQUEANTE |  |  |  |
| CK-26 | confidencialidade, propriedade, retenção e acesso estão aprovados | BLOQUEANTE |  |  |  |
| CK-27 | papéis e acumulações estão declarados | ALTA |  |  |  |
| CK-28 | cópias entregues a avaliadores comparáveis têm o mesmo digest | BLOQUEANTE |  |  |  |
| CK-29 | instruções de independência e canais proibidos estão declarados quando aplicáveis | BLOQUEANTE |  |  |  |
| CK-30 | pacote está congelado contra alteração silenciosa | BLOQUEANTE |  |  |  |
| CK-31 | Manifesto/digest foi recalculado após o congelamento | BLOQUEANTE |  |  |  |
| CK-32 | toda ressalva possui alcance, impacto, responsável e aceite requerido | ALTA |  |  |  |
| CK-33 | regras de incidente, parada, desvio e nova versão estão presentes | BLOQUEANTE |  |  |  |
| CK-34 | cada executor dispõe de procedimento de rechecagem pré-início | BLOQUEANTE |  |  |  |
| CK-35 | rastreabilidade liga cada item ao passo que o consome e a seus dependentes | BLOQUEANTE |  |  |  |
| CK-36 | Registro de Verificação pode ser congelado e auditado | BLOQUEANTE |  |  |  |

## 4. Verificação por artefato

Repetir para cada item do Manifesto:

| Artifact ID | Obrigatoriedade | Localizador declarado | Alvo canônico observado | Bytes | SHA-256 | Acesso | Referências | Estado |
|---|---|---|---|---:|---|---|---|---|
|  |  |  |  |  |  |  |  |  |

## 5. Resumo

| Estado | Quantidade |
|---|---:|
| ATENDIDO |  |
| ATENDIDO_COM_RESSALVA |  |
| NAO_ATENDIDO |  |
| NAO_VERIFICADO |  |
| NAO_APLICAVEL |  |
| falhas bloqueantes |  |

## 6. Classificação e decisão

| Campo | Registro |
|---|---|
| classificação | INTEGRALMENTE EXECUTÁVEL / EXECUTÁVEL COM RESSALVAS / PARCIALMENTE EXECUTÁVEL / NÃO EXECUTÁVEL |
| decisão | GO / GO CONDICIONAL / NO-GO |
| ressalvas aceitas |  |
| condições de validade |  |
| evento que exige novo preflight |  |
| assinatura/identidade do verificador |  |
| decisão da autoridade experimental |  |

## 7. Cadeia da decisão do gate

- **Premissas:**
- **Evidências:**
- **Inferências:**
- **Fundamentação:**
- **Decisão:**
- **Limitações:**
- **Validação:**

Nenhum campo da cadeia pode ser omitido. Evidência deve apontar para o Manifesto, check ou registro observável; texto genérico de confiança não substitui o teste.

## 8. Teste interno do checklist

- A OEG-RG-06 ausente do localizador na RG-07 falharia CK-09 e CK-24, independentemente de os outros 12 itens passarem.
- Pela regra de classificação, isso produziria `PARCIALMENTE EXECUTÁVEL / NO-GO` prospectivamente.
- Este teste de mesa valida coerência entre documentos RG-08; não reclassifica nem reexecuta RG-07.


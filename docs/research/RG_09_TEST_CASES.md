# GP-RG-09 — Casos Sintéticos Congelados

## 1. Estado de congelamento

| Campo | Registro |
|---|---|
| Plano | `RG_09_SYNTHETIC_EXPERIMENT_PLAN.md` |
| Raiz | `docs/research/rg09_fixtures/` |
| Algoritmo | SHA-256 |
| Congelamento observado | 2026-07-18T19:51:43-03:00 |
| Regra | nenhuma alteração após este registro; divergência invalida a execução |
| Fonte externa | proibida |

O digest agregado foi calculado sobre linhas UTF-8 `nome|bytes|SHA-256`, ordenadas por nome, incluindo o Manifesto quando existente. Ele identifica o conjunto usado neste piloto; não substitui os hashes individuais.

## 2. Caso A — Integralmente executável

### Construção

Pacote mínimo com autoridade, procedimento, input, instrumento, contrato de saída e Manifesto. Todas as referências usam IDs estáveis e caminhos relativos.

| Arquivo | Bytes | SHA-256 |
|---|---:|---|
| `authority.md` | 182 | `0E9079616C14B593DCB7063ABB9943B48B8DC1ACAA18F2812C8AA3A07B568766` |
| `input.md` | 96 | `E4AFF957D4DE54BF7F0555C7D53AB6037DEA5E19634C7EC9B159FD3241725281` |
| `instrument.md` | 162 | `85D145C863E2DFE93F1A8AC45D043258FF35BBFC96EB5F20B788FEB121AA46C0` |
| `output_contract.md` | 173 | `3BE8F2E4AC36011845F7DB614DC00E783680B2B00970973C2D59C8190E211DDB` |
| `package_manifest.md` | 1521 | `3A6F094F8AA163EBDAE08CEBC5D5456CB2614EAC1F0A580602C71961FD154FCA` |
| `procedure.md` | 288 | `63B804E5676F3DB2619BC480473A67A62874D7C2974FD01C6B7B68A6B8F2DEBD` |

Digest agregado: `E5CE270B374820BC5FF74ECE438BEC5FFBAF771FE59F3F96FA9BF200337E9FEC`.

Falha injetada: nenhuma.

Resultado esperado congelado: **INTEGRALMENTE EXECUTÁVEL — GO**.

## 3. Caso B — Executável com ressalva

### Construção

Pacote completo. `INPUT-B-v1` preserva o rótulo descritivo legado `Input Draft`; resolução, instruções, IDs, versão, caminho e hash usam valores canônicos. A ressalva não altera entrada, procedimento, denominador, interpretação, acesso, igualdade ou custódia.

| Arquivo | Bytes | SHA-256 |
|---|---:|---|
| `authority.md` | 182 | `DCFE43A947E8C9896E93FEAD8D7030149FC773824124E76623AEB45184CCB91C` |
| `input.md` | 234 | `E6E72B05903EF01839CD537DBA05004D411CEBE7481EAEAB12669DCB4BE401FA` |
| `instrument.md` | 161 | `A65ED755EE4A822B11BE90C7FB1A54142CF8EAEF3BCBD40B3C67736F8401B1B9` |
| `output_contract.md` | 173 | `01654223C3658511F6CF2C29747AF9C803E86C2491704FAB1157C3645509FCEA` |
| `package_manifest.md` | 1874 | `620FDDE14841F212E7B165AD4DEFCABF4C0B8E094332984EFE0F8ACA31709E2F` |
| `procedure.md` | 349 | `BD1BB55E3F15A8225B11D166007FE94A1BB90192A63B2A089D67F17D3F7E492E` |

Digest agregado: `1666178FCC711E5B0BD78EF2BE0B80FC2BD5F6BC3A4DA1F4177384C3917CE342`.

Resultado esperado congelado: **EXECUTÁVEL COM RESSALVAS — GO CONDICIONAL**.

## 4. Caso C — Parcialmente executável

### Construção

Manifesto, autoridade, procedimento, instrumento e contrato existem. O procedimento exige `INPUT-C-v1`; o Manifesto declara `input.md` obrigatório, mas o arquivo foi deliberadamente omitido e não possui bytes/hash observáveis.

| Arquivo existente | Bytes | SHA-256 |
|---|---:|---|
| `authority.md` | 182 | `C69DA573F365C8A0B48E4554976AC590AA972B225CCADEFFC81F6D4AA744E36B` |
| `instrument.md` | 178 | `4F3551ABC7A9B88E8BC33D3E30DB66EF193EA1ACFBF2424627A1B37500D20F65` |
| `output_contract.md` | 173 | `C6CB915AE440C9FBB48B38FA82A4D73D4CA60A6721D36B6F9BEF129AE9A99ABA` |
| `package_manifest.md` | 1746 | `3DF8B67038DBEE944B5680C3AC6E0018E522CC14E69E62BB0634042F22D38380` |
| `procedure.md` | 244 | `9ACD4D2E30AAE8C965DCBDB8A45B4A462305414011CCA714027A977CB809A308` |

Digest agregado dos arquivos presentes: `BD350FE96AB18160F893EE176278659C64CF9023361AC92F28D52B5CECAA9A98`.

Falha congelada: `input.md` obrigatório `AUSENTE`; é vedado criá-lo durante V1/V2.

Resultado esperado congelado: **PARCIALMENTE EXECUTÁVEL — NO-GO**.

## 5. Caso D — Não executável

### Construção

Não há pacote operacional: Manifesto, autoridade, procedimento, input, instrumento e contrato estão ausentes. Existe somente uma declaração externa do cenário para permitir auditoria da injeção.

| Arquivo de controle | Bytes | SHA-256 |
|---|---:|---|
| `SCENARIO_DECLARATION.md` | 316 | `C635F56126ED4ABA427BE9AE278904A940E9F593E57643F02C0469DDE5C9739B` |

Digest do controle do cenário: `A70D603D777636780A2EC8771788AE42662D5D18BB4EC73691AA237B82B8F362`.

O arquivo de controle não é Manifesto nem satisfaz qualquer dependência do pacote.

Resultado esperado congelado: **NÃO EXECUTÁVEL — NO-GO**.

## 6. Comparabilidade

- A e B testam classes positivas; C e D testam classes negativas.
- C preserva subconjunto íntegro e diagnosticável; D não delimita pacote executável.
- As falhas são deliberadas e conhecidas, adequadas para teste de coerência, mas reduzem realismo e cegamento.
- Os casos não testam corrupção sutil, permissões reais multiusuário, links simbólicos, plataformas distintas, formatos binários ou fontes remotas.

## 7. Cadeia da decisão de congelamento

- **Premissas:** verdade de referência exige injeções fixas antes da classificação.
- **Evidências:** arquivos, bytes, hashes e digests acima foram observados após montagem.
- **Inferências:** qualquer alteração posterior destruiria comparabilidade entre V1 e V2.
- **Fundamentação:** RG-08 vincula certificado à versão/digest e proíbe correção in-place.
- **Decisão:** congelar quatro casos nos estados documentados e iniciar V1/V2 sem mutação.
- **Limitações:** digest agregado é convenção deste piloto; não é Merkle tree padronizada.
- **Validação:** tabelas permitem recalcular cada hash e o digest agregado antes de cada passagem.

## 8. Estado

**CASOS E RESULTADOS ESPERADOS CONGELADOS — PASSAGENS V1/V2 AUTORIZADAS PELO PLANO RG-09.**


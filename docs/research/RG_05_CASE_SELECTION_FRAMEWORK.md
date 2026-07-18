# GP-RG-05 — Framework De Selecao E Classificacao De Casos

## 1. Objetivo

Definir criterios anteriores aos resultados para registrar, triar, classificar, comparar e selecionar futuros casos GDC-R. Este documento registra candidatos, mas nao seleciona nem aplica qualquer caso.

## 2. Principios

1. selecao deve decorrer de questao/OV, nao de resultado esperado;
2. casos favoraveis e contrarios sao igualmente elegiveis;
3. falha, conflito, revisao e incompletude sao fontes relevantes;
4. documentacao minima e requisito, nao garantia de qualidade;
5. confidencialidade e propriedade prevalecem sobre conveniencia;
6. comparabilidade e declarada antes da coleta;
7. portfolio deve reduzir dependencia do ecossistema fundador;
8. exclusao recebe motivo e permanece no registro;
9. nenhuma pontuacao substitui julgamento fundamentado;
10. DGA-01 exige diversidade progressiva.

## 3. Registro De Candidatos

Todo candidato recebe:

* `candidate_id`;
* titulo neutro;
* dominio;
* tipo de decisao;
* retrospectivo/prospectivo;
* agente(s) possiveis;
* estado da decisao;
* acervo disponivel;
* revisoes/conflitos conhecidos sem antecipar resultado;
* sensibilidade/confidencialidade;
* OV/QE potencial;
* origem da indicacao;
* conflitos de interesse;
* status e motivo.

Status: `REGISTRADO`, `EM_TRIAGEM`, `ELEGIVEL`, `ELEGIVEL_COM_RESSALVAS`, `INELEGIVEL`, `ADIADO`, `SELECIONADO_POR_DELIBERACAO`.

Nesta GP, todos os CP-01 a CP-05 permanecem `REGISTRADOS` ou condicionados; nenhum recebe `SELECIONADO_POR_DELIBERACAO`.

## 4. Criterios Obrigatorios De Inclusao

| ID | Criterio | Evidencia requerida |
|---|---|---|
| CI-01 | decisao identificavel | registro ou autoridade capaz de delimitar D |
| CI-02 | documentacao suficiente para a fase | inventario preliminar de entradas |
| CI-03 | fatos e interpretacoes distinguiveis em principio | fontes/metodos e registros interpretativos identificaveis |
| CI-04 | relevancia real, nao exercicio inventado apenas para confirmar | impacto/uso declarado |
| CI-05 | auditabilidade posterior possivel | custodia e acesso definidos |
| CI-06 | nao depender exclusivamente de memoria oral | pelo menos uma fonte documental observavel |
| CI-07 | complexidade compativel com fase | classificacao e justificativa |
| CI-08 | confidencialidade/propriedade trataveis | autorizacao, redacao ou ambiente controlado |
| CI-09 | versao e escopo congelaveis | Manifesto candidato |
| CI-10 | possibilidade de evidencia contraria | condicoes contrarias predefiniveis |

Falha em CI-01, CI-05, CI-06, CI-08 ou CI-10 e bloqueante. Outros podem gerar `ELEGIVEL_COM_RESSALVAS` somente com justificativa previa.

## 5. Criterios De Exclusao

| ID | Excluir quando | Motivo |
|---|---|---|
| CE-01 | caso escolhido porque resultado favoravel ja e conhecido | viés de confirmacao/selecao |
| CE-02 | inexistem artefatos e o caso e retrospectivo | impossibilidade de reconstrucao auditavel |
| CE-03 | decisao nao pode ser delimitada | unidade invalida |
| CE-04 | propriedade/confidencialidade nao autorizam uso | risco material |
| CE-05 | pesquisadores nao podem declarar conflito de interesse | auditabilidade comprometida |
| CE-06 | comparador e apresentado como equivalente sem base | inferencia causal invalida |
| CE-07 | caso exige mudar criterios apos conhecer resultado | pre-registro inviavel |
| CE-08 | uso cria risco humano/material desproporcional | seguranca/etica |
| CE-09 | caso depende de inferir estado interno de agente | fora do objeto |
| CE-10 | fase E sem formalizacao de indicadores do monitoramento | bloqueio deliberado |

Exclusao nao apaga o candidato; preserva motivo, data/ordem e autoridade.

## 6. Dimensoes De Classificacao

### 6.1 Dominio

`SOFTWARE`, `AUDITORIA`, `DOCUMENTACAO`, `PESQUISA`, `GESTAO`, `EDITORIAL`, `OPERACIONAL`, `MONITORAMENTO`, `OUTRO`, com descricao obrigatoria.

### 6.2 Temporalidade

`RETROSPECTIVO`, `PROSPECTIVO`, `HIBRIDO`.

### 6.3 Tipo De Agente

`HUMANO`, `INSTITUCIONAL`, `IA`, `HUMANO_IA`, `MULTIAGENTE`, sem presumir equivalencia ou independencia.

### 6.4 Complexidade

| Nivel | Indicadores documentais |
|---|---|
| `C1_BAIXA` | uma D, poucos elementos, sem revisao material |
| `C2_MEDIA` | multiplas E/I/F ou uma revisao/conflito |
| `C3_ALTA` | D dependentes, multiplas versoes/conflitos/agentes |
| `C4_SISTEMICA` | cadeias paralelas/convergentes, alto impacto ou escopo amplo |

### 6.5 Maturidade Documental

`MINIMA`, `PARCIAL`, `ESTRUTURADA`, `VERSIONADA`, `DESCONHECIDA`.

### 6.6 Fenomenos Presentes

* revisao parcial/total;
* validacao negativa/inconclusiva;
* conflito E/I/F/D/V;
* propagacao multinivel;
* paralelismo/convergencia;
* informacao incompleta;
* decisao de nao acao;
* substituicao/obsolescencia.

### 6.7 Sensibilidade

`PUBLICA`, `INTERNA`, `CONFIDENCIAL`, `RESTRITA`, `NAO_CLASSIFICADA`.

## 7. Triagem Em Gates

| Gate | Pergunta | Resultado |
|---|---|---|
| GC-00 | existe autorizacao para triar? | nao: manter registrado |
| GC-01 | CI bloqueantes atendidos? | nao: inelegivel/adiado |
| GC-02 | OV/QE e fase sao coerentes? | nao: reformular antes de selecionar |
| GC-03 | documentacao foi inventariada sem analisar resultados-alvo? | nao: risco de contaminacao |
| GC-04 | riscos, propriedade e acesso sao trataveis? | nao: excluir/adiar |
| GC-05 | conflitos de interesse e papeis sao governaveis? | nao: excluir/mitigar |
| GC-06 | comparador, se usado, possui equivalencia defensavel? | nao: descritivo apenas |
| GC-07 | caso contribui para diversidade ou teste necessario? | registrar contribuicao |
| GC-08 | pre-registro pode ser concluido antes da aplicacao? | nao: nao selecionar |
| GC-09 | autoridade delibera selecao? | somente entao `SELECIONADO` |

## 8. Matriz De Priorizacao Previa

Pontuacao e apenas apoio a deliberacao e deve ser calculada antes dos resultados.

| Dimensao | 0 | 1 | 2 |
|---|---|---|---|
| alinhamento OV/QE | indireto | parcial | direto |
| suficiencia documental | insuficiente | com lacunas trataveis | suficiente |
| auditabilidade | improvavel | condicionada | clara |
| evidencia contraria | nao identificavel | limitada | claramente possivel |
| diversidade DGA-01 | repete contexto | varia uma dimensao | dominio/agente externo/distinto |
| fenomeno dinamico | ausente | simples | revisao/conflito/propagacao relevante |
| viabilidade etica/juridica | bloqueada | condicionada | autorizavel |
| independencia avaliativa | inviavel | parcial | viavel |

Regras:

* criterio bloqueante nao e compensado por pontuacao;
* pesos, limiar e desempate devem ser pre-registrados pela GP executora;
* pontuacao nao pode ser alterada apos exame do resultado;
* candidatos excluidos permanecem visiveis;
* portfolio pode incluir caso de baixa pontuacao se necessario para evidencia contraria, com justificativa.

## 9. Selecao Contra Viés De Confirmacao

Medidas candidatas:

1. registrar universo de candidatos antes da selecao;
2. separar proponente, triador e deliberador quando viavel;
3. ocultar resultado conhecido do triador quando possivel;
4. incluir casos incompletos, revistos, conflitantes ou negativos;
5. usar regra de selecao pre-registrada;
6. publicar motivos de inclusao/exclusao;
7. limitar substituicao de caso apos inicio;
8. classificar substituicao como desvio quando resultado ja conhecido;
9. reservar ao menos um caso externo para OV-08;
10. nao usar apenas casos produzidos pelos autores da GDC-R.

Medidas reduzem riscos; nao os eliminam.

## 10. Adequacao Por Fase

| Fase | Caso adequado | Caso inadequado |
|---|---|---|
| A retrospectiva | D concluida, acervo preservado, lacunas auditaveis | apenas memoria oral |
| B prospectiva | D aberta, escopo controlavel, eventos registraveis | risco alto sem governanca/consentimento |
| C independente | pacote congelavel, dois avaliadores | dependência inevitavel de conhecimento tacito nao compartilhavel |
| D multidominio | portfolio com diferencas substantivas e nucleo comum | variacoes cosmeticas do mesmo dominio |
| E monitoramento | indicadores/limites formalizados | EUREKA ainda sem autoridade suficiente |

## 11. Casos-Piloto Candidatos

| ID | Candidato | Fase potencial | Contribuicao | Limitacoes/bloqueios | Estado nesta GP |
|---|---|---|---|---|---|
| CP-01 | decisao editorial do video institucional do PROTEUS | A/C | origem historica, revisao preservada | contaminacao/conhecimento previo; um dominio interno | REGISTRADO — NAO SELECIONADO |
| CP-02 | decisao arquitetural do PROTEUS | A ou B | relacoes tecnicas, alternativas e impactos | risco de dependencia interna e escopo amplo | REGISTRADO — NAO SELECIONADO |
| CP-03 | separacao da pesquisa em repositorio proprio | B | governanca patrimonial/estrategica | decisao pode influenciar custodia da propria pesquisa | REGISTRADO — NAO SELECIONADO |
| CP-04 | alerta de maturidade documental ICFACTORY | E | monitoramento e recomendacao | bloqueado ate indicadores/limites formalizados | REGISTRADO — ADIADO |
| CP-05 | caso externo ou multidominio | A/B/C/D | reduz dependencia ICFACTORY/PROTEUS | ainda nao identificado/autorizado | CATEGORIA CANDIDATA — NAO SELECIONADA |

Nenhuma avaliacao de resultado, aplicacao GDC-R ou pontuacao foi realizada.

## 12. Portfolio Minimo Candidato Para DGA-01

Uma futura alegacao progressiva sobre DGA-01 exige, no minimo metodologico proposto:

* mais de um dominio;
* ao menos um caso externo ao ecossistema fundador;
* mais de um tipo de agente ou composicao;
* ao menos um caso retrospectivo e um prospectivo;
* ao menos um caso com falha, conflito ou revisao;
* extensoes de dominio identificadas separadamente do nucleo.

Isso e requisito de desenho candidato, nao quantidade suficiente comprovada para generalidade.

## 13. Pareamento De Grupos

Quando houver GDC-R versus convencional, parear ou ajustar descritivamente:

* tipo/impacto de D;
* volume e maturidade de entrada;
* experiencia dos agentes;
* prazo/recursos;
* retrospectiva/prospectiva;
* numero de revisoes/conflitos;
* acesso a informacao;
* sensibilidade.

Cada diferenca recebe status: `EQUIVALENTE`, `APROXIMADA`, `NAO_EQUIVALENTE` ou `DESCONHECIDA`. Comparacao causal e proibida se diferencas materiais nao forem controladas.

## 14. Confidencialidade E Propriedade

Antes da selecao:

* identificar proprietario/custodiante;
* obter autoridade de uso;
* classificar sensibilidade;
* definir minimizacao/redacao;
* separar acesso de auditoria e publicacao;
* registrar material nao disponibilizado e impacto;
* proibir envio a agente/servico nao autorizado;
* definir retencao e descarte governado;
* impedir que anonimização destrua proveniencia necessaria.

## 15. Substituicao E Retirada De Caso

Caso pode ser retirado por risco, autorizacao, corrupcao de dados ou inelegibilidade descoberta.

Se resultado ja for conhecido:

* preservar registro da retirada;
* classificar desvio;
* nao substituir silenciosamente;
* aplicar a mesma regra de selecao ao substituto;
* relatar impacto sobre vies de selecao.

## 16. Deliberacao Para GP-RG-06

GP-RG-06 deve produzir antes da aplicacao:

1. registro completo dos candidatos considerados;
2. gates GC-00 a GC-09;
3. pontuacao/regra pre-registrada quando usada;
4. decisao formal de selecao;
5. justificativa de inclusao/exclusao;
6. pacote de confidencialidade/propriedade;
7. pre-registro experimental completo.

Este framework nao escolhe CP-01 nem qualquer outro candidato.

## 17. Limitacoes

* criterios nao foram aplicados;
* pesos/limiares nao estao calibrados;
* universo de candidatos e incompleto;
* candidatos internos dominam o registro atual;
* caso externo ainda nao foi identificado;
* elegibilidade documental pode favorecer organizacoes mais maduras;
* neutralidade do framework nao prova DGA-01 empiricamente.

## 18. Estado Final

**FRAMEWORK DE SELECAO FORMALIZADO — NENHUM CASO SELECIONADO OU EXECUTADO**

# GP-RG-08 — Impactos Arquiteturais na Metodologia GDC-R

## 1. Objetivo

Identificar como a Verificação de Executabilidade e Integridade do Pacote se incorpora prospectivamente ao fluxo experimental sem modificar a arquitetura epistemológica P/E/I/F/D/V, os resultados RG-06/RG-07 ou os gates RG-05 já registrados.

## 2. Natureza do impacto

O impacto é **metodológico-operacional e de governança**, não uma alteração dos seis conceitos da cadeia. Manifesto de pacote, Registro de Verificação e Certificado GX-PKG são artefatos de controle, assim como o Manifesto da cadeia é controle estrutural e não novo conceito epistemológico.

## 3. Fluxo anterior e fluxo proposto

### Fluxo anterior observado

`autoridade → seleção/pre-registro → inventário/hashes → distribuição → execução → incidentes → encerramento`

RG-05 já exigia GX-03 e pacote obrigatório; RG-06 verificou seus hashes no pre-registro. Na RG-07, o inventário registrou um artefato por nome/bytes/hash, mas a distribuição não continha uma forma resolvível de obtê-lo.

### Fluxo prospectivo

`autoridade de preparação → desenho/pre-registro preliminar → montagem → Manifesto → congelamento → GX-PKG/preflight → certificado → autoridade de início → distribuição por digest → rechecagem do executor → execução → auditoria de uso do pacote`

O certificado não elimina GX-00 a GX-11. Ele fornece evidência objetiva para os gates relacionados a autorização, congelamento, pre-registro, acesso, instrumentos, incidentes e custódia.

## 4. Novo componente: GX-PKG

| Aspecto | Definição |
|---|---|
| tipo | gate preventivo de executabilidade e integridade |
| entrada | pacote candidato, Manifesto, procedimento, ambiente e autoridade |
| processo | RG08-PIP + checklist |
| saída | pacote certificado, classe e GO/NO-GO |
| posição | após congelamento e antes do início substantivo |
| falha | não iniciar; corrigir sob nova versão ou acionar governança |
| limite | não avalia hipótese, verdade do conteúdo ou qualidade decisória |

## 5. Artefatos arquiteturais adicionais

| ID | Artefato | Função | Estado de versionamento |
|---|---|---|---|
| APKG-01 | Manifesto do Pacote | identidade, composição, localizadores, hashes, criticidade e dependências | imutável por versão |
| APKG-02 | Mapa Passo–Dependência | prova de suficiência operacional | congelado com o procedimento |
| APKG-03 | Registro de Verificação | evidência check a check | congelado ao final do preflight |
| APKG-04 | Certificado GX-PKG | classificação e GO/NO-GO | válido somente para digest/ambiente declarados |
| APKG-05 | Registro de Distribuição | digest/cópia por executor | criado antes do início |
| APKG-06 | Declaração de Rechecagem | confirmação do executor | criada antes da leitura substantiva |
| APKG-07 | Log de Incidentes do Pacote | indisponibilidade, mutação e desvios | append-only/versionado |

## 6. Relação com RG-03

- identidade única e Manifesto: coerentes com INV-01/RI-01;
- proveniência: coerente com INV-06/RI-03;
- referências resolvíveis: coerentes com AP-10 e testes estruturais mínimos;
- preservação histórica: coerente com PM-08, INV-16–20 e governança de versões;
- integridade do pacote permanece distinta da integridade da cadeia: pacote íntegro pode conter cadeia `NAO_CONFORME`, como observado em RG-06.

Nenhuma RI, INV, relação ou tipo de nó é reescrito por esta GP.

## 7. Relação com os gates RG-05

| Gate existente | Contribuição do GX-PKG | Alteração retroativa? |
|---|---|---|
| GX-00 | distingue autoridade de preparação de autoridade de início | não |
| GX-03 | produz evidência de que congelamento inclui resolução/acesso, não só inventário | não |
| GX-04 | confronta pre-registro com itens realmente entregues | não |
| GX-05 | verifica custódia, propriedade e permissões | não |
| GX-06 | verifica distribuição simétrica e acessos por papel | não |
| GX-07 | verifica disponibilidade de instrumentos, métricas e denominadores | não |
| GX-08 | desloca falhas detectáveis para antes da execução e preserva regra de incidente | não |
| GX-11 | permite auditar se o pacote usado coincide com o certificado | não |

## 8. Requisitos para futuras OEGs experimentais

Futura OEG deve, no mínimo:

1. identificar a autoridade para montagem e preflight;
2. exigir `package_id`, versão, raiz e digest;
3. referenciar RG08-PIP e versão do checklist;
4. exigir classificação positiva para início;
5. proibir fonte externa e substituição não congelada;
6. exigir rechecagem por executor antes do caso;
7. definir tratamento de divergência após certificação;
8. identificar autoridade que aceita ressalvas;
9. vincular saídas ao digest recebido;
10. preservar resultados anteriores sem correção retroativa.

Modelo de cláusula:

> A execução substantiva somente poderá iniciar após certificado GX-PKG vigente para o `package_id`, versão, digest e ambiente declarados, classificado como INTEGRALMENTE EXECUTÁVEL ou EXECUTÁVEL COM RESSALVAS e rechecado pelo executor. Divergência, ausência ou fonte adicional produz NO-GO/suspensão conforme o protocolo aplicável.

## 9. Impactos de governança

- cria responsabilidade explícita do Curador do Pacote;
- separa verificação de executabilidade da avaliação do caso;
- torna auditável a passagem entre preparação e execução;
- exige autoridade explícita para aceitar ressalvas;
- impede que busca ad hoc repare falha de distribuição;
- converte mudança do pacote em evento versionado;
- permite auditoria posterior do digest efetivamente usado.

## 10. Impactos sobre RG-06 e RG-07

### RG-06

Permanece concluída com ressalvas. Seus hashes e regras de suspensão são evidência de antecedente, mas o piloto não é recertificado por RG-08.

### RG-07

Permanece suspensa e encerrada como `TESTE_INCONCLUSIVO`. A falha NC-RG07-01 fundamenta o novo controle. Não se fornece agora o caminho ausente, não se recalculam estados e não se altera A/B.

## 11. Riscos introduzidos

| Risco | Mitigação |
|---|---|
| burocratização excessiva | proporcionalidade; campos condicionais justificados |
| verificador contaminado pelo caso | dry-run por metadados/fixture e leitura substantiva mínima |
| falsa confiança pelo hash | declarar que hash não prova verdade ou segurança |
| papel acumulado | declarar ressalva e preferir verificação independente |
| certificado obsoleto | validade vinculada a digest, ambiente e evento de mudança |
| correção silenciosa durante preflight | nova versão obrigatória após falha |
| tratar classe positiva como validação | cláusula explícita de não equivalência |

## 12. Cadeias de fundamentação

### D08-ARQ-01 — Impacto aditivo, não substitutivo

- **Premissas:** OEG-RG-08 proíbe modificar resultados e metodologia anterior sem fundamento; RG-05 já possui gates aprovados.
- **Evidências:** a lacuna está entre inventário/congelamento e entrega executável, não na ausência completa de regras de parada.
- **Inferência:** um gate complementar resolve a lacuna sem renumerar ou reescrever gates existentes.
- **Fundamentação:** preserva autoridade histórica e oferece evidência adicional aos gates aplicáveis.
- **Decisão:** GX-PKG é camada aditiva de governança.
- **Limitações:** compatibilidade operacional ainda deve ser pilotada.
- **Validação:** a matriz da seção 7 mostra contribuição sem substituição para cada gate.

### D08-ARQ-02 — Não criar novo conceito epistemológico

- **Premissas:** executabilidade descreve condição de entrada, não conteúdo de P/E/I/F/D/V.
- **Evidências:** RG-03 já distingue controles estruturais de conceitos epistemológicos.
- **Inferência:** tratar certificado como novo nó confundiria governança do experimento com cadeia do caso.
- **Fundamentação:** separação evita promoção conceitual sem validação.
- **Decisão:** artefatos APKG são controles metodológicos externos à cadeia substantiva.
- **Limitações:** podem ser citados como evidência em decisões de início/encerramento.
- **Validação:** nenhum documento RG-03 foi alterado e os tipos P/E/I/F/D/V permanecem intactos.

## 13. Estado final

**IMPACTO ARQUITETURAL PROSPECTIVO DEFINIDO: GX-PKG E SETE ARTEFATOS DE CONTROLE, SEM ALTERAÇÃO RETROATIVA OU PROMOÇÃO METODOLÓGICA UNIVERSAL.**


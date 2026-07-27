# BW-01 — Registro de Fontes Oficiais

## Identificação

- GP: GP-BW-01 — Auditoria de Elegibilidade OpenAI Build Week
- Data de acesso: 18/07/2026
- Critério: fontes primárias da OpenAI e da página oficial do desafio no Devpost
- Idioma das fontes: inglês

## Registro

| ID | Título da fonte | Organização responsável | URL | Seção utilizada | Informação confirmada | Observações | Nível de autoridade |
|---|---|---|---|---|---|---|---|
| F-01 | OpenAI Build Week | OpenAI | https://openai.com/build-week/ | Challenge, key dates e FAQ | participação com projeto novo ou existente; entregáveis gerais; quatro dimensões de avaliação; uso cuidadoso de GPT-5.6 e Codex | Página institucional remete às regras e ao Devpost para detalhes vinculantes | Primária institucional |
| F-02 | OpenAI Build Week — Overview | OpenAI / Devpost | https://openai.devpost.com/ | Requirements, tracks, what to submit e prizes | quatro categorias; projeto funcional com Codex e GPT-5.6; descrição; vídeo público no YouTube com menos de 3 minutos e áudio; repositório; README; `/feedback` Session ID; US$ 100.000 em prêmios | Página oficial de submissão; em conflito, prevalecem as Official Rules | Primária operacional |
| F-03 | OpenAI Build Week Official Rules | OpenAI / Devpost | https://openai.devpost.com/rules | §§ 1, 3–9, 11–12 e 15–16 | datas; elegibilidade; exclusão expressa do Brasil; projetos preexistentes; requisitos de vídeo, repositório, README, Session ID, idioma, teste, autoria, PI, julgamento, direitos concedidos e desclassificação | Fonte normativa principal. As próprias regras declaram prevalência em caso de conflito | Primária normativa — máxima |
| F-04 | OpenAI Build Week — Schedule | OpenAI / Devpost | https://openai.devpost.com/details/dates | Schedule | submissões de 13/07/2026 09:00 PDT a 21/07/2026 17:00 PDT; anúncio em 12/08/2026 | Diverge das Official Rules quanto ao período de julgamento; não usado para substituir as regras | Primária operacional |
| F-05 | OpenAI Build Week — Resources | OpenAI / Devpost | https://openai.devpost.com/resources | Tools & Setup; Pointers & Tips | créditos promocionais esgotados; free tier permitido; vídeo com voice-over; repositório testável, instruções e dados de exemplo | Recomendações oficiais, não substituem requisitos normativos | Primária orientativa |
| F-06 | Build Week halfway update | OpenAI / Devpost | https://openai.devpost.com/updates/45362-openai-build-week-halfway-there-where-are-you | Submission checklist | núcleo funcional, Session ID, vídeo público, acesso ao repositório e README; voz de vídeo gerada por IA é aceita, enquanto a descrição deve refletir a voz do participante | Atualização oficial complementar | Primária orientativa |

## Hierarquia e divergências

1. As **Official Rules** são a fonte vinculante e declaram prevalência sobre formulário, website, publicidade e demais materiais.
2. A página institucional da OpenAI informa julgamento de 22/07 a 07/08; o Schedule do Devpost informa 22/07 a 09/08; as Official Rules informam 22/07 10:00 PT a 05/08 17:00 PT. A auditoria adota as Official Rules e registra a divergência, que não altera o prazo de submissão.
3. O prazo de submissão é consistente nas fontes operacionais e normativas: **21/07/2026 às 17:00 Pacific Time**. Em 21/07/2026, a diferença esperada para Brasília é de quatro horas; portanto, 21:00 BRT é uma conversão inferida, não um horário publicado. Deve-se operar pelo relógio do Devpost.
4. A página institucional usa linguagem global, mas ressalva as regras oficiais. A exclusão expressa do Brasil nas Official Rules controla a análise territorial.

## Fontes incorporadas, mas não analisadas separadamente

As Official Rules incorporam os Termos de Serviço e a Política de Privacidade do Devpost. A aceitação desses instrumentos é decisão humana e não foi realizada nesta GP:

- https://info.devpost.com/terms
- https://info.devpost.com/privacy

## Limitações da consulta

- A skill `openai-docs` foi usada para orientar a pesquisa a fontes oficiais. O conector MCP oficial de documentação não estava disponível e sua instalação local falhou por `Access Denied`; a consulta prosseguiu diretamente nas páginas oficiais da OpenAI e do Devpost.
- A URL remota local aponta para `https://github.com/hendersonmauriciobatista-png/sistema-analise-agua.git`. Em consulta não autenticada, a API pública do GitHub respondeu `404`. Isso não distingue repositório privado de repositório inexistente e, portanto, a visibilidade foi classificada como **não confirmada**, não como privada.
- As regras podem ser alteradas. É necessária nova leitura humana imediatamente antes de eventual submissão.

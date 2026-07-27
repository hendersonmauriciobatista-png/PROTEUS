# BW-01 — Plano de Ação para OpenAI Build Week

## Estado inicial

- Data-base: 18/07/2026
- Prazo oficial: 21/07/2026, 17:00 Pacific Time
- Veredito de origem: **NÃO APTO NO ESTADO ATUAL**
- Regra de precedência: nenhuma ação técnica supera a inelegibilidade territorial do entrante.

## Regra de parada

Se o entrante pretendido for residente ou domiciliado no Brasil, a regra oficial o exclui. Nesse caso, **não submeter** e não usar representante nominal, conta de terceiro ou organização sem vínculo/autoria reais para contornar a regra. Só faz sentido executar as demais ações se houver um indivíduo, equipe ou organização genuinamente elegível, com participação, representação, autoria e direitos demonstráveis.

## Ações priorizadas

| ID | Descrição | Requisito relacionado | Prioridade | Criticidade | Responsável sugerido | Dependências | Esforço estimado | Prazo interno sugerido | Evidência de conclusão | Status inicial |
|---|---|---|---|---|---|---|---|---|---|---|
| BW-A01 | Confirmar documentalmente identidade, idade de maioridade, residência/domicílio e modalidade do entrante | BW-EL-01/02/03 | P0 | BLOQUEANTE | Titular jurídico | decisão humana | 30–60 min | 18/07 | declaração verdadeira e documentos disponíveis para verificação, sem inclusão no repositório | PENDENTE |
| BW-A02 | Se o entrante for do Brasil, encerrar a tentativa de submissão; se houver entrante elegível real, validar sua autoria, vínculo e representação sem simulação | BW-EL-02/03 | P0 | BLOQUEANTE | Titular jurídico + entrante | BW-A01 | 1–2 h | 18/07 | decisão assinada e trilha de autorização | PENDENTE |
| BW-A03 | Ler e decidir humanamente sobre Official Rules, Termos Devpost, privacidade, publicidade, licença de julgamento e arbitragem | BW-RI-01 | P0 | BLOQUEANTE | Entrante / assessoria jurídica | BW-A01 | 1–3 h | 18/07 | aceite consciente registrado fora de segredos | PENDENTE |
| BW-A04 | Confirmar autoria, titularidade exclusiva, permissões de colaboradores, dados, marca e materiais audiovisuais | BW-IP-01/02/03 | P0 | BLOQUEANTE | Titular jurídico | BW-A02 | 2–6 h | 19/07 | inventário de direitos e autorizações | PENDENTE |
| BW-A05 | Distinguir claramente baseline anterior de trabalho novo após 13/07/2026 | BW-PR-01/02 | P0 | BLOQUEANTE | Responsável técnico | BW-A02 | 2–4 h | 19/07 | changelog Build Week com commits/arquivos/funcionalidades | PENDENTE |
| BW-A06 | Obter o `/feedback` Codex Session ID da thread onde a maioria da funcionalidade central elegível foi construída | BW-RP-05 | P0 | BLOQUEANTE | Autor da implementação | BW-A02 | 15–30 min | 19/07 | Session ID válido inserido no formulário, sem inventar identificador | PENDENTE |
| BW-A07 | Reunir logs Codex datados e evidência verificável de uso do GPT-5.6 dentro do período | BW-PR-03/BW-TL-01 | P0 | BLOQUEANTE | Autor da implementação | BW-A05/A06 | 1–3 h | 19/07 | logs/session e mapa para commits, preservando dados sensíveis | PENDENTE |
| BW-A08 | Definir e documentar a categoria; `Work and Productivity` é hipótese inicial, não decisão da auditoria | BW-SU-02 | P0 | ALTA | Entrante | BW-A02 | 30 min | 19/07 | categoria selecionada com justificativa | PENDENTE |
| BW-A09 | Preparar descrição em inglês do problema, solução, funcionalidade e abordagem | BW-SU-03/BW-LG-01 | P0 | BLOQUEANTE | Entrante | BW-A05/A08 | 2–4 h | 19/07 | texto final revisado pelo entrante | PENDENTE |
| BW-A10 | Adequar o README de submissão: setup, execução, dados de exemplo, plataforma, Codex, decisões e GPT-5.6 | BW-RP-03/04 | P0 | BLOQUEANTE | Responsável técnico | BW-A05/A07 | 3–5 h | 20/07 | README em inglês ou com tradução integral e teste por terceiro | PENDENTE |
| BW-A11 | Decidir repositório público com licença relevante ou privado compartilhado com os dois e-mails oficiais | BW-RP-01/02 | P0 | BLOQUEANTE | Titular + responsável Git | BW-A03/A04 | 1–3 h | 20/07 | URL acessível; licença válida ou confirmação de compartilhamento | PENDENTE |
| BW-A12 | Limpar e congelar um estado reproduzível, resolvendo alterações locais e excluindo do pacote caminhos locais/ativos internos indevidos | BW-SC-03/BW-RP-01 | P0 | BLOQUEANTE | Responsável Git | BW-A04/A11 | 2–5 h | 20/07 | árvore limpa ou tag/commit de submissão, sem modificar histórico indevidamente | PENDENTE |
| BW-A13 | Executar revisão completa de licença das dependências e dados; decidir licença de primeiro nível se o repo for público | BW-IP-02/BW-RP-02 | P0 | BLOQUEANTE | Titular + responsável técnico | BW-A04/A11 | 3–6 h | 20/07 | SBOM/inventário e licença aprovada | PENDENTE |
| BW-A14 | Gravar demonstração funcional específica da Build Week, com menos de 3 minutos e áudio explicando Codex e GPT-5.6 | BW-VD-01/02 | P0 | BLOQUEANTE | Entrante | BW-A05/A07/A10 | 4–8 h | 20/07 | arquivo final <3 min, revisão de conteúdo e direitos | PENDENTE |
| BW-A15 | Publicar o vídeo como público no YouTube e inserir o link | BW-VD-03 | P0 | BLOQUEANTE | Entrante | BW-A03/A04/A14 | 30–60 min | 20/07 | URL pública testada sem login | PENDENTE |
| BW-A16 | Disponibilizar teste gratuito e irrestrito até o fim do julgamento, com instruções e dados de exemplo | BW-TS-01 | P0 | BLOQUEANTE | Responsável técnico | BW-A10/A11/A12 | 2–4 h | 20/07 | teste por máquina limpa/terceiro | PENDENTE |
| BW-A17 | Reexecutar testes e validar inicialização da GUI na plataforma declarada | BW-FN-01/02 | P0 | ALTA | QA técnico | BW-A12 | 1–2 h | 20/07 | log de 110+ testes e checklist visual da versão congelada | PENDENTE |
| BW-A18 | Repetir varredura de segredos, PII, caminhos locais, temporários e materiais internos sobre o pacote exato de submissão | BW-SC-01/02/03 | P0 | BLOQUEANTE | Segurança / responsável Git | BW-A12 | 1–2 h | 20/07 | relatório sem valores de segredo e aprovação humana | PENDENTE |
| BW-A19 | Registrar-se, preencher todos os campos e salvar rascunho; não aceitar nem enviar em nome de terceiro | BW-SU-01/BW-DL-01 | P0 | BLOQUEANTE | Entrante elegível | BW-A01–A18 | 1–2 h | 20/07 | rascunho completo conferido | PENDENTE |
| BW-A20 | Revisar novamente regras e relógio do Devpost e efetuar submissão antes do prazo | BW-DL-01 | P0 | BLOQUEANTE | Entrante elegível | BW-A19 | 30–60 min | 21/07 até 15:00 PT | recibo da submissão | PENDENTE |
| BW-A21 | Fortalecer narrativa de impacto com público, problema e resultado demonstrável | BW-JU-03 | P1 | ALTA | Produto | BW-A08/A09 | 2–3 h | 19/07 | narrativa e evidências coerentes no texto/vídeo | PENDENTE |
| BW-A22 | Explicitar novidade e diferenciação frente a soluções existentes, sem alegações não comprovadas | BW-JU-04 | P1 | MÉDIA | Produto | BW-A09 | 1–2 h | 20/07 | seção comparativa revisada | PENDENTE |
| BW-A23 | Ensaiar demo completa em tempo e corrigir inconsistências entre código, texto e vídeo | BW-FN-02/BW-JU-02 | P1 | ALTA | Entrante + QA | BW-A14/A16/A17 | 1–2 h | 20/07 | checklist de ensaio aprovado | PENDENTE |
| BW-A24 | Preparar plano de suporte durante o julgamento e manter acesso estável | BW-TS-01 | P2 | MÉDIA | Responsável técnico | BW-A16 | 1 h + monitoramento | 21/07 | responsável e janela de suporte definidos | PENDENTE |

## Caminho crítico

`BW-A01 → BW-A02 → BW-A03/BW-A04 → BW-A05/BW-A07 → BW-A10/BW-A11/BW-A14 → BW-A12/BW-A16/BW-A18 → BW-A19 → BW-A20`

## Decisões que esta GP não toma

- não escolhe ou cria um entrante;
- não aceita termos;
- não declara direitos de propriedade intelectual;
- não altera licença;
- não publica repositório ou vídeo;
- não envia formulário;
- não implementa funcionalidade.

# PI-04 - Auditoria De Prontidao Audiovisual Do PROTEUS

## Objetivo

Registrar a prontidao tecnica do repositorio e do ambiente local para producao do Animatic Institucional v1 do PROTEUS.

## Tecnologia Da Aplicacao

* Linguagem: Python.
* Interface: PyQt5.
* Persistencia: CSV e JSON locais.
* Inicializacao principal: `python main.py`.
* Ambiente funcional detectado: `venv\Scripts\python.exe` com PyQt5 instalado.

## Forma Correta De Inicializacao

Com ambiente virtual:

```powershell
.\venv\Scripts\python.exe main.py
```

Para captura automatizada offscreen:

```powershell
.\venv\Scripts\python.exe .\media\proteus_institutional_video\scripts\capture_animatic_assets.py
```

## Resolucao Recomendada

* Captura: 1280x720 para animatic leve.
* Producao final recomendada: 1920x1080.
* Proporcao: 16:9.

## Telas Disponiveis

* Projeto de Monitoramento.
* Dashboard.
* Painel Executivo.
* Qualidade da Agua.
* Consumo e Distribuicao.
* Dados Ambientais.
* Relatorios.
* Previsao Analitica.
* Governanca Operacional.

## Dados De Exemplo Disponiveis

Arquivos detectados:

* `data/qualidade_agua_medicoes.csv`;
* `data/dados_ambientais_medicoes.csv`;
* `data/consumo_distribuicao_medicoes.csv`;
* `data/eventos_operacionais.json`;
* `data/projeto_monitoramento.json`;
* catalogos, configuracoes e politicas do nucleo hidrico em JSON.

Os dados sao suficientes para capturas demonstrativas, com ressalva de revisao visual antes de qualquer producao final.

## Estado Visual Das Telas

As telas carregam em modo offscreen com identidade visual existente e sem necessidade de alterar codigo funcional.

As capturas estaticas sao adequadas para animatic. A avaliacao de legibilidade fina deve ser repetida na etapa de producao final em 1920x1080.

## Viabilidade De Captura Automatizada

Viavel com ressalvas.

Foi possivel instanciar a aplicacao PyQt5 em modo offscreen e gerar PNGs reais das telas principais, sem abrir janela interativa e sem alterar dados.

## Viabilidade De Gravacao Em Video

Nao viavel no ambiente atual.

Motivo: `ffmpeg` e `ffprobe` nao foram detectados no PATH, e bibliotecas locais equivalentes como `cv2`, `imageio` e `moviepy` nao estavam disponiveis.

## Viabilidade De Geracao De Audio Provisorio

Nao viavel no ambiente atual.

Nao foi detectada ferramenta local adequada para voz provisoria generica. Nao houve instalacao de dependencias nem acesso a servicos externos.

## Ferramentas Detectadas

| Ferramenta | Estado | Uso na PI-04 |
| --- | --- | --- |
| Python global | Disponivel | Inspecao auxiliar |
| Pillow global | Disponivel | Nao utilizado na producao oficial |
| venv Python | Disponivel | Captura PyQt offscreen |
| PyQt5 no venv | Disponivel | Geracao de capturas e cartelas |
| ffmpeg | Ausente | Bloqueia MP4 local |
| ffprobe | Ausente | Bloqueia validacao tecnica de MP4 |
| cv2 | Ausente | Nao utilizado |
| imageio | Ausente | Nao utilizado |
| moviepy | Ausente | Nao utilizado |

## Limitacoes

* MP4 nao gerado no ambiente atual.
* Narracao provisoria em audio nao gerada.
* Sem trilha sonora ou ambiencia, por ausencia de ativos licenciados.
* Capturas sao estaticas, nao gravacoes de interacao.
* Capturas foram feitas em 1280x720 para animatic leve, nao em 1920x1080 final.
* Execucao direta de `build_animatic_v1.ps1` bloqueada pela politica local de execucao de scripts do Windows.

## Riscos

* Legibilidade pode exigir recaptura em 1920x1080.
* Algumas telas podem precisar de preenchimento visual adicional antes da producao final.
* Insercao futura de audio deve preservar licenciamento e nao imitar pessoa real.
* Exportacao MP4 depende de ferramenta local autorizada.
* Reproducao do build em PowerShell depende de permissao local para executar scripts.
* O animatic nao deve ser tratado como video final.

## Parecer De Prontidao

Classificacao final: PRONTO COM RESSALVAS.

Justificativa: o ambiente permite gerar capturas reais e pacote reprodutivel, mas nao permite exportar MP4 nem audio provisorio sem ferramenta adicional.

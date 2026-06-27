# Princípios Arquiteturais

## PA-01 - Separação Entre Seleção E Execução De Políticas

O Monitoramento Hídrico separa seleção de política e execução de avaliação.

Regras:

* O Policy Engine seleciona qual política deve ser aplicada.
* Motores especializados executam avaliações.
* O Policy Engine não executa avaliação.
* Motores especializados não escolhem política.
* Políticas podem apontar para motores observacionais, normativos futuros ou internos futuros.

Motivação:

* Preservar rastreabilidade.
* Evitar mistura entre avaliação observacional e conformidade legal.
* Permitir evolução incremental conforme a filosofia ICFACTORY.
* Facilitar testes isolados de seleção e execução.

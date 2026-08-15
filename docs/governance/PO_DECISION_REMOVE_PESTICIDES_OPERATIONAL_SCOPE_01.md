# Decisao Supersedente — Remocao de Agrotoxicos do Escopo

## Identificacao

- Caso: PROTEUS
- Operacao: REMOVE_PESTICIDES_FROM_OPERATIONAL_SCOPE_01
- Autoridade: Product Owner
- Natureza: decisao supersedente de escopo

## Decisao

O parametro generico `agrotoxicos` foi removido do escopo operacional e planejado do PROTEUS.

A decisao decorre da insuficiencia semantica do parametro agregado, da ambiguidade de unidade nos ativos existentes e da dependencia de uma camada laboratorial incompatível com o escopo do PROTEUS.

O PROTEUS nao implementara nem planejara integracao laboratorial ou modelo especifico de pesticidas. Nenhum placeholder arquitetural ou item de roadmap e criado por esta decisao. Qualquer reintroducao exige nova decisao explicita do Product Owner.

## Preservacao Historica

Os arquivos `data/qualidade_agua_medicoes.csv` e `data/eventos_operacionais.json` permanecem preservados sem alteracao ou reinterpretacao. Valores e eventos genericos existentes sao exclusivamente historicos e nao constituem evidencia operacional atual, cientifica ou regulatoria.

Nenhuma unidade foi selecionada como autoridade para os valores historicos.

## Efeito Operacional

- nao existe nova entrada generica de agrotoxicos;
- o valor generico nao e exibido no historico operacional atual;
- o parametro nao participa de mapeamento, avaliacao agregada, tendencias, alertas, Water Score, prioridades ou sinais executivos;
- a coluna CSV legada permanece apenas para compatibilidade de leitura e preservacao historica;
- o catalogo classifica o registro como `OUT_OF_SCOPE` e informa: “Parametro descontinuado — fora do escopo do PROTEUS.”

## Limites

Esta decisao nao interpreta dados historicos, nao escolhe unidade, nao cria requisitos laboratoriais e nao modifica registros historicos.

"""
Vocabulario oficial de status para comunicacao PA-01A.

Os codigos tecnicos do motor observacional permanecem nos seus modulos de origem.
Este modulo governa apenas rotulos comunicados a usuarios e camadas consumidoras.
"""

STATUS_CONTEXT_OBSERVATIONAL = "observacional"
STATUS_CONTEXT_ANALYTICAL_SCORE = "score_analitico"
STATUS_CONTEXT_EXECUTIVE = "executivo_observacional"

QUALITY_STATUS_OBSERVATIONAL_NORMAL = "Avaliacao observacional normal"
QUALITY_STATUS_OBSERVATIONAL_ATTENTION = "Avaliacao observacional requer atencao"
QUALITY_STATUS_OBSERVATIONAL_CRITICAL = "Avaliacao observacional critica"
QUALITY_STATUS_OBSERVATIONAL_NOT_EVALUABLE = "Avaliacao observacional nao avaliavel"
OBSERVATIONAL_ENGINE_STATUS_NORMAL = "Avaliacao observacional normal"
OBSERVATIONAL_ENGINE_STATUS_ATTENTION = "Avaliacao observacional em atencao"
OBSERVATIONAL_ENGINE_STATUS_CRITICAL = "Avaliacao observacional critica"
OBSERVATIONAL_ENGINE_STATUS_NOT_EVALUABLE = "Avaliacao observacional nao avaliavel"

WATER_HEALTH_SCORE_NO_DATA = "Score analitico sem dados"
WATER_HEALTH_SCORE_EXCELLENT = "Score analitico excelente"
WATER_HEALTH_SCORE_GOOD = "Score analitico bom"
WATER_HEALTH_SCORE_ATTENTION = "Score analitico em atencao"
WATER_HEALTH_SCORE_CRITICAL = "Score analitico critico"
WATER_HEALTH_SCORE_VERY_CRITICAL = "Score analitico muito critico"

EXECUTIVE_STATUS_OBSERVATIONAL_NORMAL = "Executivo observacional normal"
EXECUTIVE_STATUS_OBSERVATIONAL_ATTENTION = "Executivo observacional em atencao"
EXECUTIVE_STATUS_OBSERVATIONAL_CRITICAL = "Executivo observacional critico"

STATUS_SEMANTICS = {
    QUALITY_STATUS_OBSERVATIONAL_NORMAL: {
        "context": STATUS_CONTEXT_OBSERVATIONAL,
        "origin": "monitoramento_hidrico.adapters",
        "meaning": "Resultados avaliaveis nao indicam atencao ou criticidade observacional.",
        "not_meaning": "Nao representa conformidade legal, sanitaria, ambiental ou regulatoria.",
    },
    QUALITY_STATUS_OBSERVATIONAL_ATTENTION: {
        "context": STATUS_CONTEXT_OBSERVATIONAL,
        "origin": "monitoramento_hidrico.adapters",
        "meaning": "Ao menos um resultado observacional exige atencao ou acompanhamento.",
        "not_meaning": "Nao representa laudo, infracao regulatoria ou decisao operacional final.",
    },
    QUALITY_STATUS_OBSERVATIONAL_CRITICAL: {
        "context": STATUS_CONTEXT_OBSERVATIONAL,
        "origin": "monitoramento_hidrico.adapters",
        "meaning": "Ao menos um resultado observacional apresenta criticidade.",
        "not_meaning": "Nao representa laudo, infracao regulatoria ou decisao operacional final.",
    },
    QUALITY_STATUS_OBSERVATIONAL_NOT_EVALUABLE: {
        "context": STATUS_CONTEXT_OBSERVATIONAL,
        "origin": "monitoramento_hidrico.adapters",
        "meaning": "Nao existem resultados avaliaveis para agregar.",
        "not_meaning": "Nao representa seguranca, perigo, ausencia de risco ou alerta.",
    },
    WATER_HEALTH_SCORE_NO_DATA: {
        "context": STATUS_CONTEXT_ANALYTICAL_SCORE,
        "origin": "analytics.scoring",
        "meaning": "Nao ha dados suficientes para calcular o score analitico.",
        "not_meaning": "Nao representa ausencia de risco real.",
    },
    WATER_HEALTH_SCORE_EXCELLENT: {
        "context": STATUS_CONTEXT_ANALYTICAL_SCORE,
        "origin": "analytics.scoring",
        "meaning": "Score preventivo em faixa alta, calculado a partir dos sinais disponiveis.",
        "not_meaning": "Nao representa certificacao de qualidade da agua.",
    },
    WATER_HEALTH_SCORE_GOOD: {
        "context": STATUS_CONTEXT_ANALYTICAL_SCORE,
        "origin": "analytics.scoring",
        "meaning": "Score preventivo em faixa boa, calculado a partir dos sinais disponiveis.",
        "not_meaning": "Nao representa certificacao de qualidade da agua.",
    },
    WATER_HEALTH_SCORE_ATTENTION: {
        "context": STATUS_CONTEXT_ANALYTICAL_SCORE,
        "origin": "analytics.scoring",
        "meaning": "Score preventivo em faixa que recomenda acompanhamento.",
        "not_meaning": "Nao representa decisao operacional automatica.",
    },
    WATER_HEALTH_SCORE_CRITICAL: {
        "context": STATUS_CONTEXT_ANALYTICAL_SCORE,
        "origin": "analytics.scoring",
        "meaning": "Score preventivo em faixa critica para priorizacao de acompanhamento.",
        "not_meaning": "Nao representa laudo tecnico ou conformidade regulatoria.",
    },
    WATER_HEALTH_SCORE_VERY_CRITICAL: {
        "context": STATUS_CONTEXT_ANALYTICAL_SCORE,
        "origin": "analytics.scoring",
        "meaning": "Score preventivo em faixa muito critica para priorizacao de acompanhamento.",
        "not_meaning": "Nao representa laudo tecnico ou conformidade regulatoria.",
    },
    EXECUTIVE_STATUS_OBSERVATIONAL_NORMAL: {
        "context": STATUS_CONTEXT_EXECUTIVE,
        "origin": "executive.rules",
        "meaning": "Sinais consolidados nao indicam prioridade executiva imediata.",
        "not_meaning": "Nao substitui decisao humana ou avaliacao tecnica externa.",
    },
    EXECUTIVE_STATUS_OBSERVATIONAL_ATTENTION: {
        "context": STATUS_CONTEXT_EXECUTIVE,
        "origin": "executive.rules",
        "meaning": "Sinais consolidados indicam acompanhamento executivo.",
        "not_meaning": "Nao substitui decisao humana ou avaliacao tecnica externa.",
    },
    EXECUTIVE_STATUS_OBSERVATIONAL_CRITICAL: {
        "context": STATUS_CONTEXT_EXECUTIVE,
        "origin": "executive.rules",
        "meaning": "Sinais consolidados indicam priorizacao executiva.",
        "not_meaning": "Nao substitui decisao humana ou avaliacao tecnica externa.",
    },
}

OBSERVATIONAL_ENGINE_STATUS_LABELS = {
    "NORMAL": OBSERVATIONAL_ENGINE_STATUS_NORMAL,
    "ATENCAO": OBSERVATIONAL_ENGINE_STATUS_ATTENTION,
    "CRITICO": OBSERVATIONAL_ENGINE_STATUS_CRITICAL,
    "NAO_AVALIAVEL": OBSERVATIONAL_ENGINE_STATUS_NOT_EVALUABLE,
}


def semantic_status_labels():
    return tuple(STATUS_SEMANTICS.keys())


def observational_status_label(status):
    return OBSERVATIONAL_ENGINE_STATUS_LABELS.get(status, str(status))


def aggregate_observational_status(statuses):
    statuses = tuple(statuses)
    if "CRITICO" in statuses:
        return QUALITY_STATUS_OBSERVATIONAL_CRITICAL
    if "ATENCAO" in statuses:
        return QUALITY_STATUS_OBSERVATIONAL_ATTENTION
    if "NORMAL" in statuses:
        return QUALITY_STATUS_OBSERVATIONAL_NORMAL
    return QUALITY_STATUS_OBSERVATIONAL_NOT_EVALUABLE

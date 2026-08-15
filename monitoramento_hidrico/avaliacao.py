from .catalog import CATALOG_PATH, load_parametros_hidricos
from .models import ResultadoAvaliacaoObservacional


STATUS_NORMAL = "NORMAL"
STATUS_ATENCAO = "ATENCAO"
STATUS_CRITICO = "CRITICO"
STATUS_NAO_AVALIAVEL = "NAO_AVALIAVEL"

SEVERIDADE_BAIXA = "baixa"
SEVERIDADE_MEDIA = "media"
SEVERIDADE_ALTA = "alta"
SEVERIDADE_NENHUMA = "nenhuma"

MARGEM_ATENCAO = 0.20
ORIGEM_LIMITE_OBSERVACIONAL = "catalogo:limite_observacional"
OBSERVACAO_NAO_LEGAL = (
    "Avaliacao observacional baseada em limite operacional inicial; "
    "nao representa conformidade legal ou normativa."
)


class AvaliacaoObservacionalService:
    def __init__(self, catalog_path=CATALOG_PATH):
        self.catalog_path = catalog_path

    def avaliar(self, parametro_id, valor):
        parametro = self._obter_parametro(parametro_id)
        if parametro is None:
            return _resultado_nao_avaliavel(
                parametro_id,
                valor,
                "Parametro inexistente no catalogo de monitoramento hidrico.",
                "catalogo:parametro_inexistente",
            )

        if parametro.status != "ACTIVE":
            return _resultado_nao_avaliavel(
                parametro.codigo,
                valor,
                "Parametro fora do escopo operacional; avaliacao nao realizada.",
                "catalogo:parametro_fora_escopo_operacional",
            )

        if parametro.tipo_valor != "numerico":
            return _resultado_nao_avaliavel(
                parametro.codigo,
                valor,
                "Parametro textual, booleano ou observacional ainda nao avaliado por este motor.",
                "catalogo:tipo_valor",
            )

        limite = parametro.limite_observacional
        if not limite:
            return _resultado_nao_avaliavel(
                parametro.codigo,
                valor,
                "Parametro sem limite observacional cadastrado.",
                "catalogo:sem_limite_observacional",
            )

        valor_numerico = _to_float(valor)
        if valor_numerico is None:
            return _resultado_nao_avaliavel(
                parametro.codigo,
                valor,
                "Valor informado nao e numerico.",
                ORIGEM_LIMITE_OBSERVACIONAL,
            )

        minimo = _to_float(limite.get("min"))
        maximo = _to_float(limite.get("max"))
        if minimo is None and maximo is None:
            return _resultado_nao_avaliavel(
                parametro.codigo,
                valor,
                "Limite observacional sem minimo ou maximo numerico.",
                ORIGEM_LIMITE_OBSERVACIONAL,
            )

        if _dentro_do_limite(valor_numerico, minimo, maximo):
            return ResultadoAvaliacaoObservacional(
                parametro_id=parametro.codigo,
                valor_avaliado=valor,
                status=STATUS_NORMAL,
                mensagem="Valor dentro do limite observacional cadastrado.",
                severidade=SEVERIDADE_BAIXA,
                origem_limite=ORIGEM_LIMITE_OBSERVACIONAL,
                observacoes=OBSERVACAO_NAO_LEGAL,
            )

        if _fora_proximo(valor_numerico, minimo, maximo):
            return ResultadoAvaliacaoObservacional(
                parametro_id=parametro.codigo,
                valor_avaliado=valor,
                status=STATUS_ATENCAO,
                mensagem="Valor fora do limite observacional, proximo da faixa cadastrada.",
                severidade=SEVERIDADE_MEDIA,
                origem_limite=ORIGEM_LIMITE_OBSERVACIONAL,
                observacoes=OBSERVACAO_NAO_LEGAL,
            )

        return ResultadoAvaliacaoObservacional(
            parametro_id=parametro.codigo,
            valor_avaliado=valor,
            status=STATUS_CRITICO,
            mensagem="Valor muito fora do limite observacional cadastrado.",
            severidade=SEVERIDADE_ALTA,
            origem_limite=ORIGEM_LIMITE_OBSERVACIONAL,
            observacoes=OBSERVACAO_NAO_LEGAL,
        )

    def _obter_parametro(self, parametro_id):
        for parametro in load_parametros_hidricos(self.catalog_path):
            if parametro.codigo == parametro_id:
                return parametro
        return None


def avaliar_parametro_observacional(parametro_id, valor, catalog_path=CATALOG_PATH):
    return AvaliacaoObservacionalService(catalog_path).avaliar(parametro_id, valor)


def _resultado_nao_avaliavel(parametro_id, valor, mensagem, origem_limite):
    return ResultadoAvaliacaoObservacional(
        parametro_id=parametro_id,
        valor_avaliado=valor,
        status=STATUS_NAO_AVALIAVEL,
        mensagem=mensagem,
        severidade=SEVERIDADE_NENHUMA,
        origem_limite=origem_limite,
        observacoes=OBSERVACAO_NAO_LEGAL,
    )


def _to_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _dentro_do_limite(valor, minimo, maximo):
    if minimo is not None and valor < minimo:
        return False
    if maximo is not None and valor > maximo:
        return False
    return True


def _fora_proximo(valor, minimo, maximo):
    if minimo is not None and valor < minimo:
        margem = _margem(minimo, maximo)
        return valor >= minimo - margem
    if maximo is not None and valor > maximo:
        margem = _margem(minimo, maximo)
        return valor <= maximo + margem
    return False


def _margem(minimo, maximo):
    if minimo is not None and maximo is not None:
        referencia = abs(maximo - minimo)
    else:
        referencia = abs(maximo if maximo is not None else minimo)

    if referencia == 0:
        referencia = 1.0

    return referencia * MARGEM_ATENCAO

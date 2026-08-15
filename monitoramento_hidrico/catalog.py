import json
from dataclasses import asdict
from pathlib import Path

from .models import CategoriaParametro, ParametroAmbientalContextual, ParametroHidrico, PerfilOperacional


BASE_DIR = Path(__file__).resolve().parent.parent
CATALOG_PATH = BASE_DIR / "data" / "monitoramento_hidrico_catalogo.json"


def load_catalog(path=CATALOG_PATH):
    catalog_path = Path(path)
    with catalog_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_perfis_operacionais(path=CATALOG_PATH):
    catalog = load_catalog(path)
    return [PerfilOperacional(**item) for item in catalog.get("perfis_operacionais", [])]


def load_categorias_parametros(path=CATALOG_PATH):
    catalog = load_catalog(path)
    return [CategoriaParametro(**item) for item in catalog.get("categorias_parametros", [])]


def load_parametros_hidricos(path=CATALOG_PATH):
    catalog = load_catalog(path)
    return [_build_parametro_hidrico(item) for item in catalog.get("parametros_hidricos", [])]


def load_parametros_ambientais_contextuais(path=CATALOG_PATH):
    catalog = load_catalog(path)
    return [
        ParametroAmbientalContextual(**item)
        for item in catalog.get("parametros_ambientais_contextuais", [])
    ]


def listar_parametros_por_perfil(perfil_operacional, path=CATALOG_PATH):
    return [
        parametro
        for parametro in load_parametros_hidricos(path)
        if parametro.status == "ACTIVE" and perfil_operacional in parametro.aplicabilidade_perfis
    ]


def listar_parametros_por_categoria(categoria, path=CATALOG_PATH):
    return [
        parametro
        for parametro in load_parametros_hidricos(path)
        if parametro.status == "ACTIVE" and parametro.categoria == categoria
    ]


def obter_metadados_parametro(codigo, path=CATALOG_PATH):
    for parametro in load_parametros_hidricos(path):
        if parametro.codigo == codigo:
            return asdict(parametro)
    raise ValueError(f"Parametro inexistente no catalogo: {codigo}")


def validar_metadados_parametros(path=CATALOG_PATH):
    perfis = {perfil.codigo for perfil in load_perfis_operacionais(path)}
    categorias = {categoria.codigo for categoria in load_categorias_parametros(path)}
    tipos_validos = {"numerico", "texto", "booleano", "observacional"}
    status_validos = {"ACTIVE", "INACTIVE", "DEPRECATED", "OUT_OF_SCOPE"}

    for parametro in load_parametros_hidricos(path):
        if not parametro.codigo or not parametro.nome:
            raise ValueError("Parametro hidrico sem codigo ou nome.")
        if parametro.categoria not in categorias:
            raise ValueError(f"Categoria invalida para parametro: {parametro.codigo}")
        if parametro.tipo_valor not in tipos_validos:
            raise ValueError(f"Tipo de valor invalido para parametro: {parametro.codigo}")
        if parametro.status not in status_validos:
            raise ValueError(f"Status invalido para parametro: {parametro.codigo}")
        if parametro.tipo_valor == "numerico" and not parametro.unidade_medida:
            raise ValueError(f"Parametro numerico sem unidade de medida: {parametro.codigo}")
        if not parametro.aplicabilidade_perfis:
            raise ValueError(f"Parametro sem aplicabilidade por perfil: {parametro.codigo}")
        for perfil in parametro.aplicabilidade_perfis:
            if perfil not in perfis:
                raise ValueError(f"Perfil invalido para parametro {parametro.codigo}: {perfil}")

    return True


def _build_parametro_hidrico(item):
    parametro = dict(item)
    if not parametro.get("unidade_medida"):
        parametro["unidade_medida"] = parametro.get("unidade")
    if not parametro.get("unidade"):
        parametro["unidade"] = parametro.get("unidade_medida")
    return ParametroHidrico(**parametro)

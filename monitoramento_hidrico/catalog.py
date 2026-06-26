import json
from pathlib import Path

from .models import CategoriaParametro, ParametroHidrico, PerfilOperacional


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
    return [ParametroHidrico(**item) for item in catalog.get("parametros_hidricos", [])]

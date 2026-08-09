import json
from dataclasses import asdict
from pathlib import Path

from .catalog import (
    CATALOG_PATH,
    load_categorias_parametros,
    load_parametros_hidricos,
    load_perfis_operacionais,
)
from .models import ConfiguracaoOperacional


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIGURACOES_PATH = BASE_DIR / "data" / "monitoramento_hidrico_configuracoes.json"


class ConfiguracaoOperacionalService:
    def __init__(self, catalog_path=CATALOG_PATH, configuracoes_path=CONFIGURACOES_PATH):
        self.catalog_path = Path(catalog_path)
        self.configuracoes_path = Path(configuracoes_path)
        self.perfis = {perfil.codigo for perfil in load_perfis_operacionais(self.catalog_path)}
        self.categorias = {categoria.codigo for categoria in load_categorias_parametros(self.catalog_path)}
        self.parametros = {parametro.codigo for parametro in load_parametros_hidricos(self.catalog_path)}

    def criar_a_partir_de_perfil(
        self,
        identificador,
        nome,
        perfil_operacional_base,
        categorias_habilitadas=None,
        parametros_habilitados=None,
        observacoes="",
    ):
        configuracao = ConfiguracaoOperacional(
            identificador=identificador,
            nome=nome,
            perfil_operacional_base=perfil_operacional_base,
            categorias_habilitadas=_unique(categorias_habilitadas or []),
            parametros_habilitados=_unique(parametros_habilitados or []),
            observacoes=observacoes,
        )
        self.validar_configuracao(configuracao)
        return configuracao

    def habilitar_categoria(self, configuracao, categoria_codigo):
        self._validar_categoria(categoria_codigo)
        _append_unique(configuracao.categorias_habilitadas, categoria_codigo)
        return configuracao

    def desabilitar_categoria(self, configuracao, categoria_codigo):
        configuracao.categorias_habilitadas = [
            categoria for categoria in configuracao.categorias_habilitadas if categoria != categoria_codigo
        ]
        return configuracao

    def habilitar_parametro(self, configuracao, parametro_codigo):
        self._validar_parametro(parametro_codigo)
        _append_unique(configuracao.parametros_habilitados, parametro_codigo)
        return configuracao

    def desabilitar_parametro(self, configuracao, parametro_codigo):
        configuracao.parametros_habilitados = [
            parametro for parametro in configuracao.parametros_habilitados if parametro != parametro_codigo
        ]
        return configuracao

    def validar_configuracao(self, configuracao):
        if not configuracao.identificador:
            raise ValueError("Configuracao operacional sem identificador.")
        if not configuracao.nome:
            raise ValueError("Configuracao operacional sem nome.")
        self._validar_perfil(configuracao.perfil_operacional_base)

        for categoria in configuracao.categorias_habilitadas:
            self._validar_categoria(categoria)
        for parametro in configuracao.parametros_habilitados:
            self._validar_parametro(parametro)

        return True

    def salvar_configuracoes(self, configuracoes, path=None):
        destino = Path(path or self.configuracoes_path)
        destino.parent.mkdir(parents=True, exist_ok=True)
        for configuracao in configuracoes:
            self.validar_configuracao(configuracao)

        payload = {
            "versao_configuracoes": "GP-A10",
            "configuracoes": [asdict(configuracao) for configuracao in configuracoes],
        }
        with destino.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
            file.write("\n")

    def carregar_configuracoes(self, path=None):
        origem = Path(path or self.configuracoes_path)
        with origem.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        configuracoes = [
            ConfiguracaoOperacional(**item) for item in payload.get("configuracoes", [])
        ]
        for configuracao in configuracoes:
            self.validar_configuracao(configuracao)

        return configuracoes

    def resolver_configuracao_por_perfil_ativo(self, perfil_operacional_ativo, configuracoes=None):
        candidatas = [
            configuracao
            for configuracao in (
                self.carregar_configuracoes() if configuracoes is None else configuracoes
            )
            if configuracao.perfil_operacional_base == perfil_operacional_ativo
        ]
        if not candidatas:
            raise ValueError(
                "Nenhuma configuracao operacional corresponde ao perfil ativo: "
                f"{perfil_operacional_ativo}"
            )
        if len(candidatas) > 1:
            raise ValueError(
                "Mais de uma configuracao operacional corresponde ao perfil ativo: "
                f"{perfil_operacional_ativo}"
            )
        return candidatas[0]

    def _validar_perfil(self, perfil_codigo):
        if perfil_codigo not in self.perfis:
            raise ValueError(f"Perfil operacional inexistente no catalogo: {perfil_codigo}")

    def _validar_categoria(self, categoria_codigo):
        if categoria_codigo not in self.categorias:
            raise ValueError(f"Categoria inexistente no catalogo: {categoria_codigo}")

    def _validar_parametro(self, parametro_codigo):
        if parametro_codigo not in self.parametros:
            raise ValueError(f"Parametro inexistente no catalogo: {parametro_codigo}")


def _unique(values):
    unique_values = []
    for value in values:
        _append_unique(unique_values, value)
    return unique_values


def _append_unique(values, value):
    if value not in values:
        values.append(value)

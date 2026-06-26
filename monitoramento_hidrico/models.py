from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class PerfilOperacional:
    codigo: str
    nome: str
    descricao: str = ""


@dataclass(frozen=True)
class CategoriaParametro:
    codigo: str
    nome: str
    descricao: str = ""


@dataclass(frozen=True)
class ParametroHidrico:
    codigo: str
    nome: str
    categoria: str
    unidade: Optional[str] = None
    descricao: str = ""


@dataclass
class ConfiguracaoOperacional:
    identificador: str
    nome: str
    perfil_operacional_base: str
    categorias_habilitadas: list[str] = field(default_factory=list)
    parametros_habilitados: list[str] = field(default_factory=list)
    observacoes: str = ""

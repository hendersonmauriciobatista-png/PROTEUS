from dataclasses import dataclass
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
